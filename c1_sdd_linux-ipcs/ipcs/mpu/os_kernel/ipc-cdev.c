/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2023 NXP
 */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/interrupt.h>
#include <linux/of_irq.h>
#include <linux/of_address.h>
#include <linux/wait.h>
#include <asm/errno.h>

#define DEVICE_NAME		"ipc-shm-cdev"
#define DRIVER_VERSION	"2.0"

#define IPC_CDEV_SLEEP_QUEUE	0
#define IPC_CDEV_WAKE_QUEUE		1

/* Device tree MSCM node compatible property (search key) */
#if defined(PLATFORM_FLAVOR_s32g2) || defined(PLATFORM_FLAVOR_s32g3) || \
	defined(PLATFORM_FLAVOR_s32r45)
	#define DT_INTC_NODE_COMP "nxp,s32cc-mscm"
#elif defined(PLATFORM_FLAVOR_s32v234)
	#define DT_INTC_NODE_COMP "fsl,s32v234-mscm"
#else
	#error "Platform not supported"
#endif

#include "ipc-os.h"
#include "ipc-hw.h"
#include "ipc-shm.h"
#include "ipc-cdev.h"

/**
 * struct IPCS_OS_PRIV_INSTANCE_TYPE - OS specific private data for an instance
 * @state:      instance state (initialized or not)
 * @irq_num:    rx interrupt number using to request irq
 */
struct IPCS_OS_PRIV_INSTANCE_TYPE {
	int state;
	int irq_num;
};

/**
 * struct IPCS_CDEV_PRIV_TYPE_TYPE - OS specific private data
 * @dev_is_opened:      to check if device is open or not
 * @target_instance:    instance to be initialized
 * @wait_queue_flag:    flag to wake up the wait queue
 * @irq_num_init:       array to save all initialized irq
 * @wait_queue:         variable use for wait queue operation
 * @dev_major_num:      major number is dynamically allocated when initialize
 * @ipc_class:          class use to create device file in /dev
 * @ipc_cdev:           variable use for character device
 * @instance_id:        private data per instance
 */
struct IPCS_CDEV_PRIV_TYPE_TYPE {
	char dev_is_opened;
	uint8_t target_instance;
	uint8_t wait_queue_flag;
	int irq_num_init[IPC_SHM_MAX_INSTANCES];
	wait_queue_head_t wait_queue;
	dev_t dev_major_num;
	struct class *ipc_class;
	struct cdev ipc_cdev;
	struct IPCS_OS_PRIV_INSTANCE_TYPE instance_id[IPC_SHM_MAX_INSTANCES];
} ipc_cdev_priv;


/* driver interrupt service routine */
static irqreturn_t ipcsShmHardirq(int irq, void *dev)
{
	uint8_t i = 0;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((ipc_cdev_priv.instance_id[i].state
				== IPC_SHM_INSTANCE_DISABLED)
			|| (ipc_cdev_priv.instance_id[i].irq_num
				== IPC_IRQ_NONE))
			continue;

		/* disable notifications from remote */
		ipcsHwIrqDisable(i);

		/* clear notification */
		ipcsHwIrqClear(i);
	}

	shm_dbg("Waking up the queue...\n");
	ipc_cdev_priv.wait_queue_flag = (uint8_t)IPC_CDEV_WAKE_QUEUE;
	wake_up_interruptible(&ipc_cdev_priv.wait_queue);

	return IRQ_HANDLED;
}

/**
 * ipcsOsMapIntc() - I/O memory map interrupt controller register space
 *
 * I/O memory map the inter-core interrupts HW block (MSCM for ARM processors)
 */
void *ipcsOsMapIntc(void)
{
	struct device_node *node = NULL;
	struct resource res;
	int err;

	/* get DT node */
	node = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP);
	if (!node) {
		shm_err("Unable to find MSCM node in device tree\n");
		return NULL;
	}

	/* get base address from DT node */
	err = of_address_to_resource(node, 0, &res);
	of_node_put(node);
	if (err) {
		shm_err("Unable to read regs address from DT MSCM node\n");
		return NULL;
	}

	/* map configuration register space */
	return ioremap(res.start, resource_size(&res));
}

/**
 * ipcsOsMapIntc() - I/O memory unmap interrupt controller register space
 */
void ipcsOsUnmapIntc(void *addr)
{
	iounmap(addr);
}

/*
 * ipcsCdevOpen() - open operation will respond to a open request
 *                   from user-space
 */
static int ipcsCdevOpen(struct inode *inode, struct file *file)
{
	if (ipc_cdev_priv.dev_is_opened) {
		shm_dbg("File is already opened!\n");
		return -EBUSY;
	}
	ipc_cdev_priv.dev_is_opened++;

	shm_dbg("File is opened!\n");
	return 0;
}

/*
 * ipcsCdevRelease() - release operation will respond to a close request
 *                      from user-space
 */
static int ipcsCdevRelease(struct inode *inode, struct file *file)
{
	ipc_cdev_priv.dev_is_opened--;
	shm_dbg("File is closed!\n");
	/* TODO: unregisted interrupt */

	return 0;
}

/*
 * ipcsCdevRead() - read operation will respond to a read request
 *                   from user-space
 */
static ssize_t ipcsCdevRead(struct file *file, char __user *user_buffer,
						size_t size, loff_t *offset)
{
	shm_dbg("Wait queue for IRQ\n");
	wait_event_interruptible(ipc_cdev_priv.wait_queue,
			ipc_cdev_priv.wait_queue_flag != IPC_CDEV_SLEEP_QUEUE);
	ipc_cdev_priv.wait_queue_flag = (uint8_t)IPC_CDEV_SLEEP_QUEUE;

	return 0;
}

/* init hw and request irq from kernel space */
static int ipcsCdevOsInit(const uint8_t instance,
					const struct IPCS_SHM_CFG_TYPE *cfg)
{
	int i, err;
	struct device_node *mscm = NULL;

	/* Initialize hw */
	err = ipcsHwInit(instance, cfg);
	if (err) {
		shm_err("Failed to initialize hw for instance %d", instance);
		return err;
	}

	if (cfg->inter_core_rx_irq == IPC_IRQ_NONE) {
		ipc_cdev_priv.instance_id[instance].irq_num = IPC_IRQ_NONE;
	} else {
		/* get interrupt number from device tree */
		mscm = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP);
		if (!mscm) {
			shm_err("Unable to find MSCM node in device tree\n");
			return -ENXIO;
		}
		ipc_cdev_priv.instance_id[instance].irq_num
			= of_irq_get(mscm, ipcsHwGetRxIrq(instance));
		shm_dbg("Rx IRQ of instance %d = %d\n", instance,
			ipc_cdev_priv.instance_id[instance].irq_num);
		of_node_put(mscm); /* release refcount to mscm DT node */
	}

	/* check duplicate irq number */
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (ipc_cdev_priv.instance_id[instance].irq_num
					== ipc_cdev_priv.irq_num_init[i]) {
			ipc_cdev_priv.instance_id[instance].state
				= IPC_SHM_INSTANCE_ENABLED;
			return 0;
		}
	}
	ipc_cdev_priv.irq_num_init[instance]
		= ipc_cdev_priv.instance_id[instance].irq_num;

	if (ipc_cdev_priv.instance_id[instance].irq_num != IPC_IRQ_NONE) {
		/* init rx interrupt */
		err = request_irq(ipc_cdev_priv.instance_id[instance].irq_num,
				ipcsShmHardirq, 0, DRIVER_NAME,
				&ipc_cdev_priv);
		if (err) {
			shm_err("Request interrupt %d failed\n",
				ipc_cdev_priv.instance_id[instance].irq_num);
			return -ENXIO;
		}
	}

	ipc_cdev_priv.instance_id[instance].state = IPC_SHM_INSTANCE_ENABLED;
	return 0;
}

/*
 * ipcsCdevIoctl() - ioctl operation will respond to a ioctl request
 *                    from user-space
 */
static long ipcsCdevIoctl(struct file *file, unsigned int ioctl_cmd,
						unsigned long ioctl_arg)
{
	struct IPCS_SHM_CFG_TYPE *tmp_cfg;
	int err;

	switch (ioctl_cmd) {
	case IPC_CDEV_CMD_SET_INSTANCE:
		ipc_cdev_priv.target_instance = (uint8_t)ioctl_arg;
		shm_dbg("Set target instance %d\n",
			ipc_cdev_priv.target_instance);
		break;
	case IPC_CDEV_CMD_INIT_INSTANCE:
		tmp_cfg = (struct IPCS_SHM_CFG_TYPE *)
			kmalloc(sizeof(struct IPCS_SHM_CFG_TYPE), GFP_KERNEL);
		if (copy_from_user(tmp_cfg,
				(struct IPCS_SHM_CFG_TYPE *)ioctl_arg,
				sizeof(struct IPCS_SHM_CFG_TYPE))) {
			shm_err("Fail to get struct \"IPCS_SHM_CFG_TYPE\"\n");
			return -EFAULT;
		}
		err = ipcsCdevOsInit(ipc_cdev_priv.target_instance, tmp_cfg);
		kfree(tmp_cfg);
		if (err) {
			shm_err("Initialize instance %d error\n",
				ipc_cdev_priv.target_instance);
			/* Free memory after initialized */
			return -EINVAL;
		}
		shm_dbg("Initialized instance %d\n",
			ipc_cdev_priv.target_instance);
		/* Free memory after initialized */
		break;
	case IPC_CDEV_CMD_DISABLE_RX_IRQ:
		shm_dbg("Disable rx instance %ld\n", ioctl_arg);
		ipcsHwIrqDisable((uint8_t)ioctl_arg);
		break;
	case IPC_CDEV_CMD_ENABLE_RX_IRQ:
		shm_dbg("Enable rx instance %ld\n", ioctl_arg);
		ipcsHwIrqEnable((uint8_t)ioctl_arg);
		break;
	case IPC_CDEV_CMD_TRIGGER_TX_IRQ:
		shm_dbg("Trigger tx instance %ld\n", ioctl_arg);
		ipcsHwIrqNotify((uint8_t)ioctl_arg);
		break;
	default:
		return -ENOTTY;
	}

	return 0;
}

/* File operations */
static const struct file_operations ipc_cdev_fops = {
	.open = ipcsCdevOpen,
	.release = ipcsCdevRelease,
	.read = ipcsCdevRead,
	.unlocked_ioctl = ipcsCdevIoctl,
};

static int ipcsCdevInit(void)
{
	int err;

	/* Dynamic allocate device major number */
	err = alloc_chrdev_region(
			&ipc_cdev_priv.dev_major_num,
			0,
			1,
			DEVICE_NAME);
	if (err != 0) {
		/* report error */
		shm_err("Failed to register device!\n");
		return err;
	}
	/* Create class and init character device */
	ipc_cdev_priv.ipc_class = class_create(THIS_MODULE, DEVICE_NAME);
	cdev_init(&ipc_cdev_priv.ipc_cdev, &ipc_cdev_fops);
	ipc_cdev_priv.ipc_cdev.owner = THIS_MODULE;
	cdev_add(&ipc_cdev_priv.ipc_cdev, ipc_cdev_priv.dev_major_num, 1);
	/* Create device file in /dev with name is DEVICE_NAME */
	device_create(ipc_cdev_priv.ipc_class, NULL,
			ipc_cdev_priv.dev_major_num,
			NULL, DEVICE_NAME);
	/* Initialize variable */
	ipc_cdev_priv.dev_is_opened = 0;
	ipc_cdev_priv.wait_queue_flag = (uint8_t)IPC_CDEV_SLEEP_QUEUE;
	/* Initialize wait queue */
	init_waitqueue_head(&ipc_cdev_priv.wait_queue);
	shm_dbg("Device created!\n");

	return 0;
}

static void ipcsCdevClean(void)
{
	int i;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((ipc_cdev_priv.instance_id[i].state
			== IPC_SHM_INSTANCE_DISABLED)
				|| (ipc_cdev_priv.instance_id[i].irq_num
					== IPC_IRQ_NONE))
			continue;
		/* disable notifications from remote */
		ipcsHwIrqDisable(i);
		ipc_cdev_priv.instance_id[i].state
			= IPC_SHM_INSTANCE_DISABLED;
		/* only free irq if irq number is requested */
		if (ipc_cdev_priv.irq_num_init[i] != 0) {
			free_irq(ipc_cdev_priv.instance_id[i].irq_num,
						&ipc_cdev_priv);
			ipc_cdev_priv.irq_num_init[i] = 0;
		}
	}
	cdev_del(&ipc_cdev_priv.ipc_cdev);
	device_destroy(ipc_cdev_priv.ipc_class, ipc_cdev_priv.dev_major_num);
	class_destroy(ipc_cdev_priv.ipc_class);
	unregister_chrdev_region(ipc_cdev_priv.dev_major_num, 1);
	shm_dbg("Device deleted!\n");
}

module_init(ipcsCdevInit)
module_exit(ipcsCdevClean)

MODULE_AUTHOR("NXP");
MODULE_LICENSE("Dual BSD/GPL");
MODULE_ALIAS(DEVICE_NAME);
MODULE_DESCRIPTION("NXP ShM Inter-Processor Communication User-Kernel Driver");
MODULE_VERSION(DRIVER_VERSION);
