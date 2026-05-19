/**
 * IPC Shared Memory Driver - Hardware Platform Abstraction Layer API
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
#ifndef IPC_HW_H
#define IPC_HW_H

#if defined(__cplusplus)
extern "C"{
#endif

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_HW_VENDOR_ID                    43
#define IPC_HW_AR_RELEASE_MAJOR_VERSION     4
#define IPC_HW_AR_RELEASE_MINOR_VERSION     4
#define IPC_HW_AR_RELEASE_REVISION_VERSION  0
#define IPC_HW_SW_MAJOR_VERSION             4
#define IPC_HW_SW_MINOR_VERSION             10
#define IPC_HW_SW_PATCH_VERSION             0

sint8 ipcsHwInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg);
void ipcsHwFree(const uint8 instance);
void ipcsHwIrqEnable(const uint8 instance);
void ipcsHwIrqDisable(const uint8 instance);
void ipcsHwIrqNotify(const uint8 instance);
void ipcsHwIrqClear(const uint8 instance);
void ipcsHwFlushCacheLocal(const uint8 instance);
void ipcsHwFlushCacheRemote(const uint8 instance);

#if defined(S32K358) || defined(S32K388)
void ipcsShmMuNotification(void);
#endif

#if defined(S32N) || defined(S32ZE)
void ipcsShmMruNotification(uint8 RxChannelId, const uint32 *RxBuffer, uint8 BufferSize);
#endif

#if defined(__cplusplus)
}
#endif

#endif /* IPC_HW_H */
