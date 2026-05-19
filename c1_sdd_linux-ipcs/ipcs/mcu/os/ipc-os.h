/**
 * IPC Shared Memory Driver - Real-Time OS Abstraction Layer API
 *
 * Copyright 2018,2021,2023 NXP
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
#ifndef IPC_OS_H
#define IPC_OS_H

#if defined(__cplusplus)
extern "C"{
#endif

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_OS_VENDOR_ID                    43
#define IPC_OS_AR_RELEASE_MAJOR_VERSION     4
#define IPC_OS_AR_RELEASE_MINOR_VERSION     7
#define IPC_OS_AR_RELEASE_REVISION_VERSION  0
#define IPC_OS_SW_MAJOR_VERSION             4
#define IPC_OS_SW_MINOR_VERSION             0
#define IPC_OS_SW_PATCH_VERSION             1

/* softirq work budget used to prevent CPU starvation */
#define IPC_SOFTIRQ_BUDGET 128

#define IPC_SHM_INSTANCE_DISABLED   0
#define IPC_SHM_INSTANCE_ENABLED    1

sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		sint32 (*rx_cb)(const uint8, sint32));
void ipcsOsFree(const uint8 instance);
uintptr_t ipcsOsGetLocalShm(const uint8 instance);
uintptr_t ipcsOsGetRemoteShm(const uint8 instance);
sint32 ipcsOsPollChannels(const uint8 instance);

#if defined USING_OS_XOS
void ipcsShmHardirq(void *arg);
#elif defined USING_OS_ZEPHYR
void ipcsShmHardirq(const void *arg);
#else
void ipcsShmHardirq(void);
#endif
void ipcsShmHardirqInstance(const uint8 instance);

#if defined(__cplusplus)
}
#endif

#endif /* IPC_OS_H */
