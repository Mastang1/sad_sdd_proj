/**
 * IPC Shared Memory Driver - Zephyr Specific Implementation
 *
 * Copyright 2021-2023 NXP
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

#include "tx_api.h"
#include "tx_event_flags.h"


#define IPCS_THREADX_DATA_EVENT_FLAG        (uint32)0x00000001
#define IPCS_THREADX_QUIT_REQ_EVENT_FLAG    (uint32)0x00000002
#define IPCS_THREADX_QUIT_ACK_EVENT_FLAG    (uint32)0x00000004

#ifndef IPC_SOFTIRQ_STACK_SIZE
    #define IPC_SOFTIRQ_STACK_SIZE ((uint32) 512U) /* bytes */
#endif
#ifndef IPC_SOFTIRQ_PRIORITY
    #define IPC_SOFTIRQ_PRIORITY (1U)
#endif

static void ipcsShmSoftIrq(uint32 ulInput);

/**
 * struct ipc_os_priv_u8Instance - OS specific private data per u8Instance
 * @localShm:      local shared memory address
 * @remoteShm:     remote shared memory address
 * @state:         state of u8Instance
 * @rxIrqNum:      rx interrupt number
 */
typedef struct
{
    uintptr_t localShm;
    uintptr_t remoteShm;
    sint32 state;
    sint32 rxIrqNum;
    sint32 (*rxCallback)(const uint8 u8Instance, sint32 budget);
}IPC_OS_PRIV_INSTANCE_T;

/**
 * struct IPCS_OS_PRIV_TYPE - OS specific private data
 * @id:            private data per u8Instance
 * @rxCallback:    upper layer rx callback
 * @softIrqHandle: rx task handle used by the ISR to notify the rx task
 * @taskIsInitialized: flag to know if the softirq task is initialized
 */
static struct
{
    IPC_OS_PRIV_INSTANCE_T id[IPC_SHM_MAX_INSTANCES];

    TX_EVENT_FLAGS_GROUP softIrqEvents;
    uint8 ipcSoftIrqStack[IPC_SOFTIRQ_STACK_SIZE];
    TX_THREAD softIrqHandle;
    sint32 taskIsInitialized;
} ipc_os_priv;

/**
 * ipcsOsInit() - OS specific initialization code
 * @cfg:       configuration parameters
 * @rxCallback:    rx callback to be called from rx softirq
 *
 * When inter_core_rx_irq is disabled by passing IPC_IRQ_NONE as value, the
 * softirq task will not be created.
 *
 * Return: 0 on success, -ENOMEM if the softirq task creation
 * failed, -EINVAL for invalid parameter rxCallback
 */
sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg,
                  sint32 (*rx_cb)(const uint8 instance, sint32 budget))
{
    sint32 err = -IPC_SHM_E_INVAL;
    uint32 osStatus = 0U;
    CHAR SOFT_ISR_NAME[] = "ipc_soft_irq";

    if ( (rx_cb != NULL) && (cfg != NULL) )
    {
        /* save params */
        ipc_os_priv.id[instance].localShm = cfg->local_shm_addr;
        ipc_os_priv.id[instance].remoteShm = cfg->remote_shm_addr;
        ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED;
        ipc_os_priv.id[instance].rxCallback = rx_cb;
        ipc_os_priv.id[instance].rxIrqNum = cfg->inter_core_rx_irq;
        if((ipc_os_priv.taskIsInitialized != 0) || (ipc_os_priv.id[instance].rxIrqNum == IPC_IRQ_NONE) )
        {
            err = IPC_SHM_E_OK;
        }
        else
        {
            /* Create semaphore */
            osStatus = tx_event_flags_create(&ipc_os_priv.softIrqEvents, SOFT_ISR_NAME);
            if(osStatus != TX_SUCCESS)
            {
                err = -IPC_SHM_E_NOMEM;
            }
            else
            {
                /* Create thread */
                osStatus = tx_thread_create(&ipc_os_priv.softIrqHandle, (CHAR *)SOFT_ISR_NAME, &ipcsShmSoftIrq, 0U,
                                            (void *)&ipc_os_priv.ipcSoftIrqStack[0], IPC_SOFTIRQ_STACK_SIZE,
                                            IPC_SOFTIRQ_PRIORITY, IPC_SOFTIRQ_PRIORITY, TX_NO_TIME_SLICE, TX_AUTO_START);
                if(osStatus != TX_SUCCESS)
                {
                    err = -IPC_SHM_E_NOMEM;
                }
                else
                {
                    ipc_os_priv.taskIsInitialized = 1;
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
    uint32 u32ActualFlags = 0x00;
    /* Send exit request */
    (void)tx_event_flags_set(&ipc_os_priv.softIrqEvents, IPCS_THREADX_QUIT_REQ_EVENT_FLAG, TX_OR);
    /* Wait for exit completion response */
    (void)tx_event_flags_get(&ipc_os_priv.softIrqEvents, IPCS_THREADX_QUIT_ACK_EVENT_FLAG,
                             TX_OR_CLEAR, &u32ActualFlags, 100);

    /* disable notifications from remote */
    ipcsHwIrqDisable(instance);

    /* clear private data */
    ipc_os_priv.id[instance].rxCallback = NULL;
    ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;

    /* Globally unique resource */
    if (ipc_os_priv.id[instance].rxIrqNum != IPC_IRQ_NONE)
    {
        if (ipc_os_priv.taskIsInitialized != 0)
        {
            ipc_os_priv.taskIsInitialized = 0;
            (void)tx_thread_terminate(&ipc_os_priv.softIrqHandle);
            (void)tx_thread_delete(&ipc_os_priv.softIrqHandle);
            (void)tx_event_flags_delete(&ipc_os_priv.softIrqEvents);
            /* TODO: clear task stack */
        }
    }
}

/**
 * ipcsShmSoftIrq() - task acting as deferred interrupt handler
 *
 * This task waits to be signaled by the interrupt handler, then calls the upper
 * layer callback registered with ipcsOsInit(). If ipcsOsFree() is called,
 * task execution terminates. Memory is freed next time the idle task is run.
 */
static void ipcsShmSoftIrq(uint32 ulInput)
{
    (void)ulInput;
    sint32 work = 0;
    uint32 u32ActualFlags = 0x00;
    uint32 status = TX_FEATURE_NOT_ENABLED;
    uint8 i = 0U;

    while(1)
    {
        /* Wait for event flag 0. */
        status = tx_event_flags_get(&ipc_os_priv.softIrqEvents, IPCS_THREADX_DATA_EVENT_FLAG | IPCS_THREADX_QUIT_REQ_EVENT_FLAG,
                                    TX_OR_CLEAR, &u32ActualFlags, TX_WAIT_FOREVER);
        /* Check status. */
        if (status == TX_SUCCESS)
        {
            /* Data reception and process */
            if((u32ActualFlags & IPCS_THREADX_DATA_EVENT_FLAG) == IPCS_THREADX_DATA_EVENT_FLAG)
            {
                for (i = 0U; i < IPC_SHM_MAX_INSTANCES; i++)
                {
                    if (ipc_os_priv.id[i].state != IPC_SHM_INSTANCE_DISABLED)
                    {
                        if(ipc_os_priv.id[i].rxIrqNum != IPC_IRQ_NONE)
                        {
                            do
                            {
                                /* call upper layer callback */
                                work = ipc_os_priv.id[i].rxCallback((const uint8)i, IPC_SOFTIRQ_BUDGET);

                                /* yield and wait for reschedule */
                                tx_thread_relinquish();
                            } while (work >= IPC_SOFTIRQ_BUDGET);
                        }
                    }
                }

                for (i = 0U; i < IPC_SHM_MAX_INSTANCES; i++)
                {
                    if (ipc_os_priv.id[i].state != IPC_SHM_INSTANCE_DISABLED)
                    {
                        /* work done, re-enable irq */
                        ipcsHwIrqEnable(i);
                    }
                }
            }

            /* Quit process flow */
            if((u32ActualFlags & IPCS_THREADX_QUIT_REQ_EVENT_FLAG) == IPCS_THREADX_QUIT_REQ_EVENT_FLAG)
            {
                (void)tx_event_flags_set(&ipc_os_priv.softIrqEvents, IPCS_THREADX_QUIT_ACK_EVENT_FLAG, TX_OR);
                break;
            }
        } /* if (status == TX_SUCCESS) */
    } /*while(1)*/
}

/**
 * ipcsShmHardIrq() - driver interrupt service routine
 */
void ipcsShmHardIrq(void)
{
    uint8 i = 0U;
    /* The macro is defined in threadx source code */
    uint32 taskCriticalStatusFromIsr = tx_interrupt_control(TX_INT_DISABLE);
    for (i = 0U; i < (uint8)IPC_SHM_MAX_INSTANCES; i++)
    {
        if (ipc_os_priv.id[i].state != IPC_SHM_INSTANCE_DISABLED)
        {
            /* disable notifications from remote */
            ipcsHwIrqDisable(i);
            /* clear notification */
            ipcsHwIrqClear(i);
        }
    }
    (void)tx_event_flags_set(&ipc_os_priv.softIrqEvents, IPCS_THREADX_DATA_EVENT_FLAG, TX_OR);
    (void)tx_interrupt_control(taskCriticalStatusFromIsr);
}

/**
 * ipcsOsGetLocalShm() - get local shared mem address
 */
uintptr_t ipcsOsGetLocalShm(const uint8 instance)
{
    return ipc_os_priv.id[instance].localShm;
}

/**
 * ipcsOsGetRemoteShm() - get remote shared mem address
 */
uintptr_t ipcsOsGetRemoteShm(const uint8 instance)
{
    return ipc_os_priv.id[instance].remoteShm;
}

/**
 * ipcsOsPollChannels() - invoke rx callback configured at initialization
 *
 * Return: work done, error code otherwise
 */
sint32 ipcsOsPollChannels(const uint8 instance)
{
    sint32 err = IPC_SHM_E_OK;
    /* the softirq will handle rx operation if rx interrupt is configured */
    if (ipc_os_priv.id[instance].rxIrqNum == IPC_IRQ_NONE)
    {
        if (ipc_os_priv.id[instance].rxCallback != NULL)
        {
            err = ipc_os_priv.id[instance].rxCallback(instance, IPC_SOFTIRQ_BUDGET);
        }
    }
    else
    {
        err = -IPC_SHM_E_INVAL;
    }

    return err;
}

#if defined(__cplusplus)
}
#endif
