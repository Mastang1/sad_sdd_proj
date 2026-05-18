/*
 * IPC Shared Memory Driver - API Implementation
 *
 * Copyright 2018-2019,2022-2023 NXP
 * All Rights Reserved.
 *
 * NXP Confidential. This software is owned or controlled by NXP and may only be
 * used strictly in accordance with the applicable license terms. By expressly
 * accepting such terms or by downloading, installing, activating and/or otherwise
 * using the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to be
 * bound by the applicable license terms, then you may not retain, install,
 * activate or otherwise use the software.
 *
 */
#ifndef IPC_SHM_H
#define IPC_SHM_H

#if defined(__cplusplus)
extern "C"{
#endif

#include "ipc-types.h"
#include "ipcf_Ip_Cfg.h"

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_SHM_VENDOR_ID                    43
#define IPC_SHM_MODULE_ID                    255
#define IPC_SHM_AR_RELEASE_MAJOR_VERSION     4
#define IPC_SHM_AR_RELEASE_MINOR_VERSION     7
#define IPC_SHM_AR_RELEASE_REVISION_VERSION  0
#define IPC_SHM_SW_MAJOR_VERSION             4
#define IPC_SHM_SW_MINOR_VERSION             0
#define IPC_SHM_SW_PATCH_VERSION             1

/*
 * FILE VERSION CHECKS
 */
/* Check if ipc-shm.h file and ipcf_Ip_Cfg.h configuration header file are of the same vendor */
#if (IPC_SHM_VENDOR_ID != IPCF_IP_CFG_VENDOR_ID)
	#error "ipc-shm.h and ipcf_Ip_Cfg.h have different vendor IDs"
#endif
/* Check if ipc-shm.h file and ipcf_Ip_Cfg.h configuration header file are of the same Autosar version */
#if ((IPC_SHM_AR_RELEASE_MAJOR_VERSION != IPCF_IP_CFG_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_MINOR_VERSION != IPCF_IP_CFG_AR_RELEASE_MINOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_REVISION_VERSION != IPCF_IP_CFG_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-shm.h and ipcf_Ip_Cfg.h are different"
#endif
/* Check if ipc-shm.h file and ipcf_Ip_Cfg.h configuration header file are of the same software version */
#if ((IPC_SHM_SW_MAJOR_VERSION != IPCF_IP_CFG_SW_MAJOR_VERSION) || \
	(IPC_SHM_SW_MINOR_VERSION != IPCF_IP_CFG_SW_MINOR_VERSION) || \
	(IPC_SHM_SW_PATCH_VERSION != IPCF_IP_CFG_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-shm.h and ipcf_Ip_Cfg.h are different"
#endif

/**
 * ipcsShmInit() - initialize shared memory device
 * @cfg:              configuration parameters
 *
 * Function is non-reentrant.
 *
 * Return: 0 on success, error code otherwise
 */
sint32 ipcsShmInit(const struct IPCS_SHM_INSTANCES_CFG_TYPE *cfg);

/**
 * ipcsShmFree() - release all instances of shared memory device
 *
 * Function is non-reentrant.
 */
void ipcsShmFree(void);

/**
 * ipcsShmAcquireBuf() - request a buffer for the given channel
 * @instance:       instance id
 * @chan_id:        channel index
 * @mem_size:           required size
 *
 * Function used only for managed channels where buffer management is enabled.
 * Function is thread-safe for different channels but not for the same channel.
 *
 * Return: pointer to the buffer base address or NULL if buffer not found
 */
void *ipcsShmAcquireBuf(const uint8 instance, sint32 chan_id, uint32 mem_size);

/**
 * ipcsShmReleaseBuf() - release a buffer for the given channel
 * @instance:       instance id
 * @chan_id:        channel index
 * @buf:            buffer pointer
 *
 * Function used only for managed channels where buffer management is enabled.
 * Function is thread-safe for different channels but not for the same channel.
 *
 * Return: 0 on success, error code otherwise
 */
sint32 ipcsShmReleaseBuf(const uint8 instance, sint32 chan_id, const void *buf);

/**
 * ipcsShmTx() - send data on given channel and notify remote
 * @instance:       instance id
 * @chan_id:        channel index
 * @buf:            buffer pointer
 * @size:           size of data written in buffer
 *
 * Function used only for managed channels where buffer management is enabled.
 * Function is thread-safe for different channels but not for the same channel.
 *
 * Return: 0 on success, error code otherwise
 */
sint32 ipcsShmTx(const uint8 instance, sint32 chan_id, void *buf, uint32 size);

/**
 * ipcsShmUnmanagedAcquire() - acquire the unmanaged channel local memory
 * @instance:       instance id
 * @chan_id:        channel index
 *
 * Function used only for unmanaged channels. The memory must be acquired only
 * once after the channel is initialized. There is no release function needed.
 * Function is thread-safe for different channels but not for the same channel.
 *
 * Return: pointer to the channel memory or NULL if invalid channel
 */
void *ipcsShmUnmanagedAcquire(const uint8 instance, sint32 chan_id);

/**
 * ipcsShmUnmanagedTx() - notify remote that data has been written in channel
 * @instance:       instance id
 * @chan_id:        channel index
 *
 * Function used only for unmanaged channels. It can be used after the channel
 * memory has been acquired whenever is needed to signal remote that new data
 * is available in channel memory.
 * Function is thread-safe for different channels but not for the same channel.
 *
 * Return: 0 on success, error code otherwise
 */
sint32 ipcsShmUnmanagedTx(const uint8 instance, sint32 chan_id);

/**
 * ipcsShmIsRemoteReady() - check whether remote is initialized
 * @instance:        instance id
 *
 * Function used to check if the remote is initialized and ready to receive
 * messages. It should be invoked at least before the first transmit operation.
 * Function is thread-safe.
 *
 * Return: 0 if remote is initialized, error code otherwise
 */
sint32 ipcsShmIsRemoteReady(const uint8 instance);

/**
 * ipcsShmPollChannels() - poll the channels for available messages to process
 * @instance:        instance id
 *
 * This function handles all channels using a fair handling algorithm: all
 * channels are treated equally and no channel is starving.
 * Function is thread-safe for different instances but not for same instance.
 *
 * Return: number of messages processed, error code otherwise
 */
sint32 ipcsShmPollChannels(const uint8 instance);

#if defined(__cplusplus)
}
#endif

#endif /* IPC_SHM_H */
