/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2019,2021-2023 NXP
 */
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/mod_devicetable.h>
#include <linux/uio_driver.h>
#include <linux/cdev.h>

#include "ipc-shm.h"
#include "ipc-os.h"
#include "ipc-hw.h"
#include "ipc-uio.h"

#define IPC_CDEV_NAME		"ipc-cdev-uio"
#define IPC_UIO_NAME		"ipc-shm-uio"
#define IPC_UIO_VERSION		"2.0"

static DEFINE_MUTEX(mmap_device_mutex);
/**
 * struct IPCS_UIO_PRIV_TYPE_TYPE - IPCS SHM UIO device data
 * @state:      instance state (initialized or not)
 * @irq_num:    rx interrupt number using to request irq
 * @dev:        Linux device capabilities
 * @refcnt:     reference counter to allow a single UIO device open at a time
 * @info:       UIO device capabilities
 * @data:       Chrdev private data to get user space configuration
 * @uio_name:   UIO device name
 */
struct IPCS_UIO_PRIV_TYPE_TYPE {
	int state;
	int irq_num;
	struct device *dev;
	atomic_t refcnt;
	struct uio_info info;
	struct IPCS_UIO_CDEV_DATA_TYPE data;
	char uio_name[32];
};

/**
 * struct IPCS_PDEV_PRIV_TYPE_TYPE - IPCS SHM platform device data
 * @major:           chrdev major number which is allocated dynamically
 * @irq_num_init:    interrupt index for each instance
 * @ipc_pdev:        Linux platform device capabilities
 * @pdev_reg:        Platform device register
 * @cdev_class:      class use to create device file in /dev
 * @cdev:            variable use for character device
 * @uio_id:          IPCS SHM UIO device data for each instance
 */
struct IPCS_PDEV_PRIV_TYPE_TYPE {
	dev_t major;
	int irq_num_init[IPC_SHM_MAX_INSTANCES];
	struct platform_device *ipc_pdev;
	void __iomem *pdev_reg;
	struct class *cdev_class;
	struct cdev cdev;
	struct IPCS_UIO_PRIV_TYPE_TYPE uio_id[IPC_SHM_MAX_INSTANCES];
} ipc_pdev_priv;

/**
 * ipcsShmUioOpen() - open operation will respond to a open UIO request
 */
static int ipcsShmUioOpen(struct uio_info *info, struct inode *inode)
{
	struct IPCS_UIO_PRIV_TYPE_TYPE *priv = info->priv;

	if (!atomic_dec_and_test(&priv->refcnt)) {
		shm_err("%s device already opened\n", info->name);
		atomic_inc(&priv->refcnt);
		return -EBUSY;
	}

	return 0;
}

/**
 * ipcsShmUioRelease() - release operation will respond to a close UIO request
 */
static int ipcsShmUioRelease(struct uio_info *info, struct inode *inode)
{
	struct IPCS_UIO_PRIV_TYPE_TYPE *priv = info->priv;

	atomic_inc(&priv->refcnt);

	return 0;
}
/**
 * ipcsShmUioIrqcontrol() - irqcontrol operation will respond to
 *                            a irqcontrol UIO request
 */
static int ipcsShmUioIrqcontrol(struct uio_info *dev_info, int cmd)
{
	struct IPCS_UIO_PRIV_TYPE_TYPE *info = dev_info->priv;
	uint8_t instance = info->data.instance;

	switch (cmd) {
	case IPC_UIO_DISABLE_CMD:
		ipcsHwIrqDisable(instance);
		break;
	case IPC_UIO_ENABLE_CMD:
		ipcsHwIrqEnable(instance);
		break;
	case IPC_UIO_TRIGGER_CMD:
		ipcsHwIrqNotify(instance);
		break;
	default:
		break;
	}
	return 0;
}

/* hardirq handler */
static irqreturn_t ipcsShmUioHandler(int irq, struct uio_info *dev_info)
{
	struct IPCS_UIO_PRIV_TYPE_TYPE *info = dev_info->priv;
	uint8_t instance = info->data.instance;

	ipcsHwIrqDisable(instance);
	ipcsHwIrqClear(instance);

	/* return IRQ_HANDLED to trigger uio_event_notify() to user-space */
	return IRQ_HANDLED;
}

/**
 * ipcsUioInit() - Initialize an UIO and ipcs hw
 * @IPCS_UIO_CDEV_DATA_TYPE:    Chrdev private data from user space
 * Return: 0 on Success, error code otherwise
 */
static int ipcsUioInit(struct IPCS_UIO_CDEV_DATA_TYPE *data)
{
	int err, irq, i;
	int instance = data->instance;
	struct IPCS_SHM_CFG_TYPE *cfg = &data->cfg;

	err = sprintf(ipc_pdev_priv.uio_id[instance].uio_name,
						"instance_%d", instance);
	/* init MSCM HW for MSI inter-core interrupts */
	err = ipcsHwInit(instance, cfg);
	if (err)
		return err;

	if (cfg->inter_core_rx_irq == IPC_IRQ_NONE)
		return 0;
	/* get Linux IRQ number */
	irq = platform_get_irq(ipc_pdev_priv.ipc_pdev,
						cfg->inter_core_rx_irq);
	if (irq < 0) {
		shm_dbg("Failed to get IRQ\n");
		return irq;
	}
	shm_dbg("GIC Rx IRQ = %d\n", irq);

	/* check duplicate irq number */
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (irq == ipc_pdev_priv.irq_num_init[i]) {
			shm_dbg("Can't create UIO device with same irq %d\n",
				irq);
			return -EFAULT;
		}
	}
	ipc_pdev_priv.irq_num_init[instance] = irq;
	ipc_pdev_priv.uio_id[instance].dev
					= &ipc_pdev_priv.ipc_pdev->dev;
	/* Register UIO device */
	atomic_set(&ipc_pdev_priv.uio_id[instance].refcnt, 1);
	ipc_pdev_priv.uio_id[instance].info.version = IPC_UIO_VERSION;
	ipc_pdev_priv.uio_id[instance].info.name
				= ipc_pdev_priv.uio_id[instance].uio_name;
	ipc_pdev_priv.uio_id[instance].info.irq
				= ipc_pdev_priv.irq_num_init[instance];
	ipc_pdev_priv.uio_id[instance].info.irq_flags = 0;
	ipc_pdev_priv.uio_id[instance].info.handler = ipcsShmUioHandler;
	ipc_pdev_priv.uio_id[instance].info.irqcontrol = ipcsShmUioIrqcontrol;
	ipc_pdev_priv.uio_id[instance].info.open = ipcsShmUioOpen;
	ipc_pdev_priv.uio_id[instance].info.release = ipcsShmUioRelease;
	ipc_pdev_priv.uio_id[instance].info.priv
			= &ipc_pdev_priv.uio_id[instance];

	err = uio_register_device(
			ipc_pdev_priv.uio_id[instance].dev,
			&ipc_pdev_priv.uio_id[instance].info);
	if (err) {
		shm_dbg("UIO registration failed\n");
		return err;
	}
	ipc_pdev_priv.uio_id[instance].state = IPC_SHM_INSTANCE_ENABLED;

	/* Get minor number of UIO */


	return 0;
}

/**
 * ipcsCdevOpen() - open operation will respond to a open request
 *                   from user-space
 */
static int ipcsCdevOpen(struct inode *inode, struct file *filp)
{
	if (!mutex_trylock(&mmap_device_mutex)) {
		shm_dbg("Another process is accessing the device\n");
		return -EBUSY;
	}

	filp->private_data = &ipc_pdev_priv;

	return 0;
}
/**
 * ipcsCdevRelease() - release operation will respond to a close request
 *                      from user-space
 */
static int ipcsCdevRelease(struct inode *inode, struct file *filp)
{
	mutex_unlock(&mmap_device_mutex);

	filp->private_data = NULL;
	return 0;
}

/**
 * ipcsCdevWrite() - write operation will respond to a write request
 *                    from user-space
 */
static ssize_t ipcsCdevWrite(struct file *file, const char __user *user_buffer,
					size_t size, loff_t *offset)
{
	int err;
	struct IPCS_UIO_CDEV_DATA_TYPE data;

	/* read data from user buffer to my_data->buffer */
	if (copy_from_user(&data, user_buffer,
			sizeof(struct IPCS_UIO_CDEV_DATA_TYPE)))
		return -EFAULT;

	if (data.instance >= IPC_SHM_MAX_INSTANCES)
		return -EINVAL;

	ipc_pdev_priv.uio_id[data.instance].data = data;
	err = ipcsUioInit(&ipc_pdev_priv.uio_id[data.instance].data);
	if (err) {
		shm_err("Failed to initialized UIO device\n");
		return err;
	}

	return sizeof(struct IPCS_UIO_CDEV_DATA_TYPE);
}

/* File operations */
static const struct file_operations ipc_cdev_fops = {
	.owner = THIS_MODULE,
	.open = ipcsCdevOpen,
	.release = ipcsCdevRelease,
	.write = ipcsCdevWrite,
};

/* Platform driver probe methods */
static int ipcsShmUioProbe(struct platform_device *pdev)
{
	int err;
	int i;
	struct resource *res;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		ipc_pdev_priv.uio_id[i].irq_num = IPC_IRQ_NONE;
		ipc_pdev_priv.irq_num_init[i] = IPC_IRQ_NONE;
	}

	platform_set_drvdata(pdev, ipc_pdev_priv.uio_id);
	ipc_pdev_priv.ipc_pdev = pdev;

	/* map MSCM register configuration space */
	res = platform_get_resource(ipc_pdev_priv.ipc_pdev,
						IORESOURCE_MEM, 0);
	ipc_pdev_priv.pdev_reg = devm_ioremap_resource(
				&ipc_pdev_priv.ipc_pdev->dev,
				res);
	if (IS_ERR_OR_NULL(ipc_pdev_priv.pdev_reg)) {
		shm_err("Failed to map MSCM register space\n");
		return -ENOMEM;
	}

	/* Create a chrdev to initial user-kernel communication */
	/* Dynamic allocate device major number */
	err = alloc_chrdev_region(&ipc_pdev_priv.major, 0, 1,
					IPC_CDEV_NAME);
	if (err < 0) {
		shm_err("Failed to alloc chrdev region\n");
		goto fail_alloc_chrdev_region;
	}
	cdev_init(&ipc_pdev_priv.cdev, &ipc_cdev_fops);
	err = cdev_add(&ipc_pdev_priv.cdev, ipc_pdev_priv.major, 1);
	if (err < 0) {
		shm_err("Failed to add cdev\n");
		goto fail_add_cdev;
	}
	ipc_pdev_priv.cdev_class = class_create(THIS_MODULE, IPC_CDEV_NAME);
	if (!ipc_pdev_priv.cdev_class) {
		err = -EEXIST;
		shm_err("Failed to create class\n");
		goto fail_create_class;
	}
	if (!device_create(ipc_pdev_priv.cdev_class, NULL,
			ipc_pdev_priv.major, NULL, IPC_CDEV_NAME)) {
		err = -EINVAL;
		shm_err("Failed to create device\n");
		goto fail_create_device;
	}
	mutex_init(&mmap_device_mutex);
	shm_dbg("%s registered with major %d\n",
			IPC_CDEV_NAME, MAJOR(ipc_pdev_priv.major));

	shm_dbg("device ready\n");

	return 0;

fail_create_device:
	class_destroy(ipc_pdev_priv.cdev_class);
fail_create_class:
	cdev_del(&ipc_pdev_priv.cdev);
fail_add_cdev:
	unregister_chrdev_region(ipc_pdev_priv.major, 1);
fail_alloc_chrdev_region:
	return err;
}


/* Platform driver remove methods */
static int ipcsShmUioRemove(struct platform_device *pdev)
{
	int i;

	device_destroy(ipc_pdev_priv.cdev_class, ipc_pdev_priv.major);
	class_destroy(ipc_pdev_priv.cdev_class);
	cdev_del(&ipc_pdev_priv.cdev);
	unregister_chrdev_region(ipc_pdev_priv.major, 1);
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (ipc_pdev_priv.uio_id[i].state
				== IPC_SHM_INSTANCE_ENABLED) {
			ipc_pdev_priv.uio_id[i].state
					= IPC_SHM_INSTANCE_DISABLED;
			if (ipc_pdev_priv.irq_num_init[i] == IPC_IRQ_NONE)
				continue;
			uio_unregister_device(&ipc_pdev_priv.uio_id[i].info);
		}
	}

	shm_dbg("device removed\n");

	return 0;
}

void *ipcsOsMapIntc(void)
{
	return ipc_pdev_priv.pdev_reg;
}

void ipcsOsUnmapIntc(void *addr)
{
	/* Dummy implementation. Not used by UIO. */
}

static const struct of_device_id ipc_shm_ids[] = {
	{ .compatible = "fsl,s32v234-mscm", },
	{ .compatible = "nxp,s32cc-mscm", },
	{}
};

MODULE_DEVICE_TABLE(of, ipc_shm_ids);

static struct platform_driver ipc_shm_driver = {
	.driver = {
		.name = IPC_UIO_NAME,
		.of_match_table = ipc_shm_ids,
	},
	.probe = ipcsShmUioProbe,
	.remove = ipcsShmUioRemove,
};

module_platform_driver(ipc_shm_driver);

MODULE_AUTHOR("NXP");
MODULE_LICENSE("Dual BSD/GPL");
MODULE_ALIAS(IPC_UIO_NAME);
MODULE_DESCRIPTION("NXP ShM Inter-Processor Communication UIO Driver");
MODULE_VERSION(IPC_UIO_VERSION);
