/**
 * IPC Shared Memory Driver - Bare Metal Specific Implementation
 *
 * Copyright 2018,2021-2023 NXP
 * All Rights Reserved.
 *
 * NXP Confidential. This software is owned or controlled by NXP and may only be
 * used strictly in accordance with the applicable license terms. By expressly
 * accepting such terms or by downloading, installing, activating and/or otherwise
 * using the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to be
 * bound by the applicable license terms, then you may not retain, install,
 * activate or otherwise use the software.
 */
#if defined(__cplusplus)
extern "C"{
#endif

#include "ipc-shm.h"
#include "ipc-os.h"
#include "ipc-hw.h"

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_OS_VENDOR_ID_C                    43
#define IPC_OS_AR_RELEASE_MAJOR_VERSION_C     4
#define IPC_OS_AR_RELEASE_MINOR_VERSION_C     7
#define IPC_OS_AR_RELEASE_REVISION_VERSION_C  0
#define IPC_OS_SW_MAJOR_VERSION_C             4
#define IPC_OS_SW_MINOR_VERSION_C             0
#define IPC_OS_SW_PATCH_VERSION_C             1

/*
 * FILE VERSION CHECKS
 */
/* Check if ipc-os-baremetal.c file and ipc-shm.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_SHM_VENDOR_ID)
	#error "ipc-os-baremetal.c and ipc-shm.h have different vendor IDs"
#endif
/* Check if ipc-os-baremetal.c file and ipc-shm.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_SHM_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_SHM_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_SHM_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-baremetal.c and ipc-shm.h are different"
#endif
/* Check if ipc-os-baremetal.c file and ipc-shm.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_SHM_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_SHM_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_SHM_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-baremetal.c and ipc-shm.h are different"
#endif

/* Check if ipc-os-baremetal.c file and ipc-os.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_OS_VENDOR_ID)
	#error "ipc-os-baremetal.c and ipc-os.h have different vendor IDs"
#endif
/* Check if ipc-os-baremetal.c file and ipc-os.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_OS_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_OS_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_OS_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-baremetal.c and ipc-os.h are different"
#endif
/* Check if ipc-os-baremetal.c file and ipc-os.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_OS_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_OS_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_OS_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-baremetal.c and ipc-os.h are different"
#endif

/* Check if ipc-os-baremetal.c file and ipc-hw.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_HW_VENDOR_ID)
	#error "ipc-os-baremetal.c and ipc-hw.h have different vendor IDs"
#endif
/* Check if ipc-os-baremetal.c file and ipc-hw.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_HW_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_HW_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_HW_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-baremetal.c and ipc-hw.h are different"
#endif
/* Check if ipc-os-baremetal.c file and ipc-hw.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_HW_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_HW_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_HW_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-baremetal.c and ipc-hw.h are different"
#endif

/**
 * struct IPCS_OS_PRIV_INSTANCE_TYPE - OS specific private data per instance
 * @local_shm:      local shared memory address
 * @remote_shm:     remote shared memory address
 * @rx_irq_num:     rx interrupt number
 * @state:          state to indicate whether instance is initialized
 */
struct IPCS_OS_PRIV_INSTANCE_TYPE {
	uintptr_t local_shm;
	uintptr_t remote_shm;
	sint32 state;
	sint32 rx_irq_num;
};

/**
 * struct IPCS_OS_PRIV_TYPE_TYPE - OS specific private data
 * @id:             private data per instance
 * @rx_cb:          upper layer rx callback
 */
static struct IPCS_OS_PRIV_TYPE_TYPE {
	struct IPCS_OS_PRIV_INSTANCE_TYPE id[IPC_SHM_MAX_INSTANCES];
	sint32 (*rx_cb)(const uint8 instance, sint32 budget);
} ipc_os_priv;

/**
 * ipcsOsInit() - OS specific initialization code
 * @instance:   instance id
 * @cfg:        configuration parameters
 * @rx_cb:      rx callback to be called from interrupt handler
 *
 * Return: IPC_SHM_E_OK on success, -IPC_SHM_E_INVAL for invalid parameter rx_cb
 */
sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		sint32 (*rx_cb)(const uint8, sint32))
{
	sint32 err = -IPC_SHM_E_INVAL;

	if (rx_cb != NULL) {
		/* save params */
		ipc_os_priv.id[instance].local_shm = cfg->local_shm_addr;
		ipc_os_priv.id[instance].remote_shm = cfg->remote_shm_addr;
		ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED;
		ipc_os_priv.rx_cb = rx_cb;
		ipc_os_priv.id[instance].rx_irq_num = cfg->inter_core_rx_irq;
		err = IPC_SHM_E_OK;
	}

	return err;
}

/**
 * ipcsOsFree() - free OS specific resources
 * @instance:   instance id
 */
void ipcsOsFree(const uint8 instance)
{
	/* clear private data */
	ipc_os_priv.rx_cb = NULL;
	ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;

	/* disable notifications from remote */
	ipcsHwIrqDisable(instance);
}

/**
 * ipcsShmHardirq() - driver interrupt service routine
 *
 * This function is set as core to core ISR by the application.
 */
void ipcsShmHardirq(void)
{
	sint32 work = 0;
	uint8 i = 0;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (ipc_os_priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
			continue;
		/* disable notifications from remote */
		ipcsHwIrqDisable(i);

		/* clear notification */
		ipcsHwIrqClear(i);
	}

	/* call upper layer callback for all non-polling instances */
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((ipc_os_priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
				|| (ipc_os_priv.id[i].rx_irq_num == IPC_IRQ_NONE))
			continue;

		/* call upper layer callback until work is done */
		do {
			work = ipc_os_priv.rx_cb(i, IPC_SOFTIRQ_BUDGET);
		} while (work >= IPC_SOFTIRQ_BUDGET);
	}

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (ipc_os_priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
			continue;
		/* enable notifications from remote */
		ipcsHwIrqEnable(i);
	}
}

/**
 * ipcsShmHardirqInstance() - driver interrupt service routine
 *
 * This function is set as core to core ISR by the application.
 */
void ipcsShmHardirqInstance(const uint8 instance)
{
	sint32 work = 0;

	if (ipc_os_priv.id[instance].state != IPC_SHM_INSTANCE_DISABLED) {
		/* disable notifications from remote */
		ipcsHwIrqDisable(instance);
		/* clear notification */
		ipcsHwIrqClear(instance);
		/* call upper layer callback for all non-polling instances */
		if (ipc_os_priv.id[instance].rx_irq_num != IPC_IRQ_NONE) {
			/* call upper layer callback until work is done */
			do {
				work = ipc_os_priv.rx_cb(instance, IPC_SOFTIRQ_BUDGET);
			} while (work >= IPC_SOFTIRQ_BUDGET);

			/* enable notifications from remote */
			ipcsHwIrqEnable(instance);
		}
	}
}

/**
 * ipcsOsGetLocalShm() - get local shared mem address
 * @instance:   instance id
 */
uintptr_t ipcsOsGetLocalShm(const uint8 instance)
{
	return ipc_os_priv.id[instance].local_shm;
}

/**
 * ipcsOsGetRemoteShm() - get remote shared mem address
 * @instance:   instance id
 */
uintptr_t ipcsOsGetRemoteShm(const uint8 instance)
{
	return ipc_os_priv.id[instance].remote_shm;
}

/**
 * ipcsOsPollChannels() - invoke rx callback configured at initialization
 *
 * Return: work done, error code otherwise
 */
sint32 ipcsOsPollChannels(const uint8 instance)
{
	sint32 err = -IPC_SHM_E_NOTSUP;

	/* the softirq will handle rx operation if rx interrupt is configured */
	if (ipc_os_priv.id[instance].rx_irq_num == IPC_IRQ_NONE) {
		if (ipc_os_priv.rx_cb != NULL) {
			err = ipc_os_priv.rx_cb(instance, IPC_SOFTIRQ_BUDGET);
		} else {
			err = -IPC_SHM_E_INVAL;
		}
	}

	return err;
}

#if defined(__cplusplus)
}
#endif
