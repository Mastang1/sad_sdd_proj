/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2018-2023 NXP
 */
#include <linux/ioport.h>
#include <linux/io.h>
#include <linux/interrupt.h>
#include <linux/of_irq.h>
#include <linux/of_address.h>
#include <linux/version.h>

#include "ipc-os.h"
#include "ipc-hw.h"
#include "ipc-shm.h"

#define DRIVER_VERSION	"0.1"

/* Device tree MSCM node compatible property (search key) */
#if defined(PLATFORM_FLAVOR_s32g2) || defined(PLATFORM_FLAVOR_s32g3) || \
	defined(PLATFORM_FLAVOR_s32r45)
	#define DT_INTC_NODE_COMP "nxp,s32cc-mscm"
#elif defined(PLATFORM_FLAVOR_s32v234)
	#define DT_INTC_NODE_COMP "fsl,s32v234-mscm"
#else
	#error "Platform not supported"
#endif


/**
 * struct IPCS_OS_PRIV_INSTANCE_TYPE - OS specific private data each instance
 * @shm_size:           local/remote shared memory size
 * @local_phys_shm:     local shared memory physical address
 * @remote_phys_shm:    remote shared memory physical address
 * @local_virt_shm:     local shared memory virtual address
 * @remote_virt_shm:    remote shared memory virtual address
 * @irq_num:            Linux IRQ number
 * @state:              state to indicate whether instance is initialized
 */
struct IPCS_OS_PRIV_INSTANCE_TYPE {
	int shm_size;
	uintptr_t local_phys_shm;
	uintptr_t remote_phys_shm;
	uintptr_t local_virt_shm;
	uintptr_t remote_virt_shm;
	int irq_num;
	int state;
};

/**
 * struct IPCS_OS_PRIV_TYPE - OS specific private data
 * @id:             private data per instance
 * @rx_cb:          upper layer rx callback
 * @irq_num_init:   array to save all initialized irq
 */
static struct IPCS_OS_PRIV_TYPE {
	struct IPCS_OS_PRIV_INSTANCE_TYPE id[IPC_SHM_MAX_INSTANCES];
	int (*rx_cb)(const uint8_t instance, int budget);
	int irq_num_init[IPC_SHM_MAX_INSTANCES];
} priv;

static void ipcsShmSoftirq(unsigned long arg);
#if LINUX_VERSION_CODE < KERNEL_VERSION(5, 10, 0)
static DECLARE_TASKLET(ipc_shm_rx_tasklet, ipcsShmSoftirq, 0);
#else
static DECLARE_TASKLET_OLD(ipc_shm_rx_tasklet, ipcsShmSoftirq);
#endif

/* sotfirq routine for deferred interrupt handling */
static void ipcsShmSoftirq(unsigned long arg)
{
	int work = 0;
	unsigned long budget = IPC_SOFTIRQ_BUDGET;
	uint8_t i = 0;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
					|| (priv.id[i].irq_num == IPC_IRQ_NONE))
			continue;

		/* call upper layer callback until work is done */
		do {
			work = priv.rx_cb(i, budget);
			/* work not done, yield and wait for reschedule */
			tasklet_schedule(&ipc_shm_rx_tasklet);
		} while (work >= budget);

		/* work done, re-enable irq */
		ipcsHwIrqEnable(i);
	}
}

/* driver interrupt service routine */
static irqreturn_t ipcsShmHardirq(int irq, void *dev)
{
	uint8_t i = 0;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
					|| (priv.id[i].irq_num == IPC_IRQ_NONE))
			continue;

		/* disable notifications from remote */
		ipcsHwIrqDisable(i);

		/* clear notification */
		ipcsHwIrqClear(i);
	}

	tasklet_schedule(&ipc_shm_rx_tasklet);

	return IRQ_HANDLED;
}

/**
 * ipcsShmOsInit() - OS specific initialization code
 * @instance:	 instance id
 * @cfg:         configuration parameters
 * @rx_cb:	rx callback to be called from rx softirq
 *
 * Return: 0 on success, error code otherwise
 */
int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		int (*rx_cb)(const uint8_t, int))
{
	struct device_node *mscm = NULL;
	struct resource *res;
	int err;
	int i;

	if (!rx_cb)
		return -EINVAL;

	/* check valid instance */
	if ((instance > IPC_SHM_MAX_INSTANCES) || (instance < 0))
		return -EINVAL;

	/* request and map local physical shared memory */
	res = request_mem_region((phys_addr_t)cfg->local_shm_addr,
				 cfg->shm_size, DRIVER_NAME" local");
	if (!res) {
		shm_err("Unable to reserve local shm region\n");
		return -EADDRINUSE;
	}

	priv.id[instance].local_virt_shm
		= (uintptr_t)ioremap(cfg->local_shm_addr, cfg->shm_size);
	if (!priv.id[instance].local_virt_shm) {
		err = -ENOMEM;
		goto err_release_local_region;
	}

	/* request and map remote physical shared memory */
	res = request_mem_region((phys_addr_t)cfg->remote_shm_addr,
				 cfg->shm_size, DRIVER_NAME" remote");
	if (!res) {
		shm_err("Unable to reserve remote shm region\n");
		err = -EADDRINUSE;
		goto err_unmap_local_shm;
	}

	priv.id[instance].remote_virt_shm
		= (uintptr_t)ioremap(cfg->remote_shm_addr, cfg->shm_size);
	if (!priv.id[instance].remote_virt_shm) {
		err = -ENOMEM;
		goto err_release_remote_region;
	}

	/* save params */
	priv.id[instance].shm_size = cfg->shm_size;
	priv.id[instance].local_phys_shm = cfg->local_shm_addr;
	priv.id[instance].remote_phys_shm = cfg->remote_shm_addr;
	priv.rx_cb = rx_cb;

	if (cfg->inter_core_rx_irq == IPC_IRQ_NONE) {
		priv.id[instance].irq_num = IPC_IRQ_NONE;
	} else {
		/* get interrupt number from device tree */
		mscm = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP);
		if (!mscm) {
			shm_err("Unable to find MSCM node in device tree\n");
			err = -ENXIO;
			goto err_unmap_remote_shm;
		}
		priv.id[instance].irq_num
			= of_irq_get(mscm, ipcsHwGetRxIrq(instance));
		shm_dbg("Rx IRQ of instance %d = %d\n",
			instance, priv.id[instance].irq_num);
		of_node_put(mscm); /* release refcount to mscm DT node */
	}

	/* check duplicate irq number */
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (priv.id[instance].irq_num == priv.irq_num_init[i]) {
			priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED;
			return 0;
		}
	}
	priv.irq_num_init[instance] = priv.id[instance].irq_num;

	if (priv.id[instance].irq_num != IPC_IRQ_NONE) {
		/* init rx interrupt */
		err = request_irq(priv.id[instance].irq_num, ipcsShmHardirq,
							0, DRIVER_NAME, &priv);
		if (err) {
			shm_err("Request interrupt %d failed\n",
						priv.id[instance].irq_num);
			goto err_unmap_remote_shm;
		}
	}

	priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED;

	return 0;

err_unmap_remote_shm:
	iounmap((void *)cfg->remote_shm_addr);
err_release_remote_region:
	release_mem_region((phys_addr_t)cfg->remote_shm_addr, cfg->shm_size);
err_unmap_local_shm:
	iounmap((void *)cfg->local_shm_addr);
err_release_local_region:
	release_mem_region((phys_addr_t)cfg->local_shm_addr, cfg->shm_size);

	return err;
}

/**
 * ipcsOsFree() - free OS specific resources
 */
void ipcsOsFree(const uint8_t instance)
{
	priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;
	/* disable hardirq */
	ipcsHwIrqDisable(instance);

	/* kill softirq task */
	tasklet_kill(&ipc_shm_rx_tasklet);

	/* only free irq if irq number is requested */
	if (priv.irq_num_init[instance] != 0) {
		free_irq(priv.id[instance].irq_num, &priv);
		priv.irq_num_init[instance] = 0;
	}

	iounmap((void *)priv.id[instance].remote_virt_shm);
	release_mem_region((phys_addr_t)priv.id[instance].remote_phys_shm,
		priv.id[instance].shm_size);
	iounmap((void *)priv.id[instance].local_virt_shm);
	release_mem_region((phys_addr_t)priv.id[instance].local_phys_shm,
		priv.id[instance].shm_size);
}

/**
 * ipcsOsGetLocalShm() - get local shared mem address
 */
uintptr_t ipcsOsGetLocalShm(const uint8_t instance)
{
	return priv.id[instance].local_virt_shm;
}

/**
 * ipcsOsGetRemoteShm() - get remote shared mem address
 */
uintptr_t ipcsOsGetRemoteShm(const uint8_t instance)
{
	return priv.id[instance].remote_virt_shm;
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

/**
 * ipcsOsPollChannels() - invoke rx callback configured at initialization
 *
 * Not implemented for Linux.
 *
 * Return: work done, error code otherwise
 */
int ipcsOsPollChannels(const uint8_t instance)
{
	/* the softirq will handle rx operation if rx interrupt is configured */
	if (priv.id[instance].irq_num == IPC_IRQ_NONE) {
		if (priv.rx_cb != NULL) {
			return priv.rx_cb(instance, IPC_SOFTIRQ_BUDGET);
		} else {
			return -EINVAL;
		}
	}

	return -EOPNOTSUPP;
}

/* module init function */
static int __init shm_mod_init(void)
{
	shm_dbg("driver version %s init\n", DRIVER_VERSION);
	return 0;
}

/* module exit function */
static void __exit shm_mod_exit(void)
{
	shm_dbg("driver version %s exit\n", DRIVER_VERSION);
}

EXPORT_SYMBOL(ipcsShmInit);
EXPORT_SYMBOL(ipcsShmFree);
EXPORT_SYMBOL(ipcsShmAcquireBuf);
EXPORT_SYMBOL(ipcsShmReleaseBuf);
EXPORT_SYMBOL(ipcsShmTx);
EXPORT_SYMBOL(ipcsShmUnmanagedAcquire);
EXPORT_SYMBOL(ipcsShmUnmanagedTx);
EXPORT_SYMBOL(ipcsShmIsRemoteReady);
EXPORT_SYMBOL(ipcsShmPollChannels);

module_init(shm_mod_init);
module_exit(shm_mod_exit);

MODULE_AUTHOR("NXP");
MODULE_LICENSE("Dual BSD/GPL");
MODULE_ALIAS(DRIVER_NAME);
MODULE_DESCRIPTION("NXP Shared Memory Inter-Processor Communication Driver");
MODULE_VERSION(DRIVER_VERSION);
