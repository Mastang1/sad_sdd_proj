/**
 * IPC Shared Memory Driver - AutosarOS Specific Implementation
 *
 * Copyright 2018-2019,2021-2023 NXP
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

#include <Os.h>

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
/* Check if ipc-os-autosar.c file and ipc-shm.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_SHM_VENDOR_ID)
	#error "ipc-os-autosar.c and ipc-shm.h have different vendor IDs"
#endif
/* Check if ipc-os-autosar.c file and ipc-shm.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_SHM_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_SHM_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_SHM_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-autosar.c and ipc-shm.h are different"
#endif
/* Check if ipc-os-autosar.c file and ipc-shm.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_SHM_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_SHM_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_SHM_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-autosar.c and ipc-shm.h are different"
#endif

/* Check if ipc-os-autosar.c file and ipc-os.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_OS_VENDOR_ID)
	#error "ipc-os-autosar.c and ipc-os.h have different vendor IDs"
#endif
/* Check if ipc-os-autosar.c file and ipc-os.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_OS_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_OS_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_OS_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-autosar.c and ipc-os.h are different"
#endif
/* Check if ipc-os-autosar.c file and ipc-os.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_OS_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_OS_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_OS_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-autosar.c and ipc-os.h are different"
#endif

/* Check if ipc-os-autosar.c file and ipc-hw.h file are of the same vendor */
#if (IPC_OS_VENDOR_ID_C != IPC_HW_VENDOR_ID)
	#error "ipc-os-autosar.c and ipc-hw.h have different vendor IDs"
#endif
/* Check if ipc-os-autosar.c file and ipc-hw.h file are of the same Autosar version */
#if ((IPC_OS_AR_RELEASE_MAJOR_VERSION_C != IPC_HW_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_OS_AR_RELEASE_MINOR_VERSION_C != IPC_HW_AR_RELEASE_MINOR_VERSION) || \
	(IPC_OS_AR_RELEASE_REVISION_VERSION_C != IPC_HW_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-os-autosar.c and ipc-hw.h are different"
#endif
/* Check if ipc-os-autosar.c file and ipc-hw.h file are of the same software version */
#if ((IPC_OS_SW_MAJOR_VERSION_C != IPC_HW_SW_MAJOR_VERSION) || \
	(IPC_OS_SW_MINOR_VERSION_C != IPC_HW_SW_MINOR_VERSION) || \
	(IPC_OS_SW_PATCH_VERSION_C != IPC_HW_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-os-autosar.c and ipc-hw.h are different"
#endif

/**
 * enum msg_receive - used to indicate notification received for a new message
 *
 * @MSG_NOT_RECEIVED: no new message received from the remote core
 * @MSG_IS_RECEIVED: new message received from the remote core
 */
enum msg_receive {
	MSG_NOT_RECEIVED = 0U,
	MSG_IS_RECEIVED = 1U,
};

/**
 * struct IPCS_OS_PRIV_INSTANCE_TYPE - OS specific memory address
 * @local_shm:      local shared memory address
 * @remote_shm:     remote shared memory address
 * @rx_irq_num:     rx interrupt number
 * @state:          state to indicate whether instance is initialized
 * @msg_received:   state to indicate notification received for a new message
 * @isr_id_handler: the name of OsIsr defined to handle the interrupt
 */
struct IPCS_OS_PRIV_INSTANCE_TYPE {
	uintptr_t local_shm;
	uintptr_t remote_shm;
	sint32 state;
	sint32 rx_irq_num;
	sint32 msg_received;
	ISRType isr_id_handler;
};

/**
 * struct IPCS_OS_PRIV_TYPE_TYPE - OS specific private data
 * @addr:           local and remote memory address for each instance
 * @rx_cb:          upper layer rx callback
 * @task_is_initialized: flag to know if the softirq task is initialized
 */
static struct IPCS_OS_PRIV_TYPE_TYPE {
	struct IPCS_OS_PRIV_INSTANCE_TYPE id[IPC_SHM_MAX_INSTANCES];
	sint32 (*rx_cb)(const uint8 instance, sint32 budget);
	sint32 task_is_initialized;
} ipc_os_priv;

/**
 * ipcsOsInit() - OS specific initialization code
 * @cfg:        configuration parameters
 * @rx_cb:      rx callback to be called from rx softirq
 *
 * When inter_core_rx_irq is disabled by passing IPC_IRQ_NONE as value, the
 * softirq task will not be activated.
 *
 * Return: IPC_SHM_E_OK on success, -IPC_SHM_E_NOTSUP if softirq task not in
 *         suspended state or softirq activation failed, -IPC_SHM_E_INVAL for
 *         invalid parameter rx_cb
 */
sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		sint32 (*rx_cb)(const uint8, sint32))
{
	StatusType os_status = (StatusType)E_OK;
	TaskStateType task_state = SUSPENDED;
	sint32 err = -IPC_SHM_E_INVAL;

	if (rx_cb != NULL) {
		/* save params */
		ipc_os_priv.id[instance].local_shm = cfg->local_shm_addr;
		ipc_os_priv.id[instance].remote_shm = cfg->remote_shm_addr;
		ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED;
		ipc_os_priv.rx_cb = rx_cb;
		ipc_os_priv.id[instance].rx_irq_num = cfg->inter_core_rx_irq;
		ipc_os_priv.id[instance].msg_received = (sint32)MSG_NOT_RECEIVED;
		ipc_os_priv.id[instance].isr_id_handler = cfg->isr_id_handler;

		if ((ipc_os_priv.id[instance].rx_irq_num == IPC_IRQ_NONE)
			|| (ipc_os_priv.task_is_initialized != 0)) {
			/* softirq is not needed when polling */
			err = IPC_SHM_E_OK;
		} else {
			/* check if softirq task is suspended */
			(void)GetTaskState(ipcsShmSoftirq, (TaskStateRefType)&task_state);
			if (task_state != SUSPENDED) {
				err = -IPC_SHM_E_NOTSUP;
			} else {
				/* activate softirq task */
				os_status = ActivateTask(ipcsShmSoftirq);
				if (os_status != (StatusType)E_OK) {
					err = -IPC_SHM_E_NOTSUP;
				} else {
					ipc_os_priv.task_is_initialized = 1;
					err = IPC_SHM_E_OK;
				}
			}
		}
	}

	return err;
}

/**
 * ipcsOsFree() - free OS specific resources
 */
void ipcsOsFree(const uint8 instance)
{
	StatusType os_status = (StatusType)E_OK; /* used for debugging */

	/* disable notifications from remote */
	ipcsHwIrqDisable(instance);

	/* clear private data */
	ipc_os_priv.rx_cb = NULL;
	ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;

	if (ipc_os_priv.id[instance].rx_irq_num != IPC_IRQ_NONE) {
		/* disable notifications from remote */
		os_status = DisableInterruptSource(ipc_os_priv.id[instance].isr_id_handler);
		(void) os_status;

		/* kill deferred interrupt handler task if no instance exist */
		if (ipc_os_priv.task_is_initialized != 0) {
			os_status = SetEvent(ipcsShmSoftirq,
				(uint32)IPC_EVENT_OS_FREE);
			(void) os_status;
			ipc_os_priv.task_is_initialized = 0;
		}
	}
}

/**
 * ipcsShmSoftirq() - task acting as deferred interrupt handler
 *
 * This task waits to be signaled by the interrupt handler and calls the upper
 * layer callback registeres with ipcsShmInit(). If ipcsOsFree() is called,
 * the task receives a different signal and proceeds to its termination.
 */
TASK(ipcsShmSoftirq)
{
	StatusType os_status = (StatusType)E_OK; /* used for debugging */
	EventMaskType event = 0x0;
	sint32 work = 0;
	uint8 i = 0;

	for ( ; ; ) {
		/* wait for any event */
		os_status = WaitEvent((uint32)IPC_EVENT_RX_IRQ |
			(uint32)IPC_EVENT_OS_FREE);
		(void) os_status;

		/* get event bits state */
		os_status = GetEvent(ipcsShmSoftirq, (EventMaskRefType)&event);
		(void) os_status;

		if ((event & (uint32) IPC_EVENT_OS_FREE) != 0u) {
			os_status = ClearEvent((uint32) IPC_EVENT_OS_FREE);
			(void) os_status;
			os_status = TerminateTask();
			(void) os_status;
		}

		/* call upper layer callback for all non-polling instances */
		for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
			if ((ipc_os_priv.id[i].state == IPC_SHM_INSTANCE_DISABLED)
				|| (ipc_os_priv.id[i].msg_received == (sint32)MSG_NOT_RECEIVED)
				|| (ipc_os_priv.id[i].rx_irq_num == IPC_IRQ_NONE))
				continue;

			do {
				/* call upper layer callback */
				work = ipc_os_priv.rx_cb(i, IPC_SOFTIRQ_BUDGET);

				/* yield and wait for reschedule */
				os_status = Schedule();
				(void) os_status;
			} while (work >= IPC_SOFTIRQ_BUDGET);
			/* reset the flag used to notify  message received */
			ipc_os_priv.id[i].msg_received = (sint32)MSG_NOT_RECEIVED;
		}

		/* work done, clear event */
		os_status = ClearEvent((uint32) IPC_EVENT_RX_IRQ);
		(void) os_status;

		/* prepare to receiving the interrupt */
		for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
			if ((ipc_os_priv.id[i].state != IPC_SHM_INSTANCE_DISABLED)
				&& (ipc_os_priv.id[i].rx_irq_num != IPC_IRQ_NONE)) {
				/* clear irq notification */
				ipcsHwIrqClear(i);

				/* re-enable irq routing for all instances */
				os_status = EnableInterruptSource(ipc_os_priv.id[i].isr_id_handler,
						TRUE);
				(void) os_status;
			}
		}
	}
}

/**
 * ipcsShmHardirq() - driver interrupt service routine
 */
void ipcsShmHardirq(void)
{
	StatusType os_status = (StatusType)E_OK; /* used for debugging */
	uint8 i = 0;

	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if ((ipc_os_priv.id[i].state != IPC_SHM_INSTANCE_DISABLED)
			&& (ipc_os_priv.id[i].rx_irq_num != IPC_IRQ_NONE)) {

			/* disable notifications from remote */
			os_status = DisableInterruptSource(ipc_os_priv.id[i].isr_id_handler);
			(void) os_status;

			/* set the flag for each instance */
			ipc_os_priv.id[i].msg_received = (sint32)MSG_IS_RECEIVED;
		}
	}
	/* signal the deferred interrupt handler */
	os_status = SetEvent(ipcsShmSoftirq, (uint32) IPC_EVENT_RX_IRQ);
	(void) os_status;
}

/**
 * ipcsShmHardirqInstance() - driver interrupt service routine
 *
 * This function is set as core to core ISR by the application.
 */
void ipcsShmHardirqInstance(const uint8 instance)
{
	StatusType os_status = (StatusType)E_OK; /* used for debugging */

	if ((ipc_os_priv.id[instance].state != IPC_SHM_INSTANCE_DISABLED)
		&& (ipc_os_priv.id[instance].rx_irq_num != IPC_IRQ_NONE)) {

		/* disable notifications from remote */
		os_status = DisableInterruptSource(ipc_os_priv.id[instance].isr_id_handler);
		(void) os_status;

		/* set the flag used to notify message is received */
		if (ipc_os_priv.id[instance].msg_received == (sint32)MSG_NOT_RECEIVED) {
			ipc_os_priv.id[instance].msg_received = (sint32)MSG_IS_RECEIVED;
		}

		/* signal the deferred interrupt handler */
		os_status = SetEvent(ipcsShmSoftirq, (uint32) IPC_EVENT_RX_IRQ);
		(void) os_status;
	}
}

/**
 * ipcsOsGetLocalShm() - get local shared mem address
 */
uintptr_t ipcsOsGetLocalShm(const uint8 instance)
{
	return ipc_os_priv.id[instance].local_shm;
}

/**
 * ipcsOsGetRemoteShm() - get remote shared mem address
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
