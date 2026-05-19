/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2018,2021 NXP
 */
#ifndef IPC_OS_H
#define IPC_OS_H

#include <linux/module.h>

#define DRIVER_NAME	"ipc-shm-dev"

/* softirq work budget used to prevent CPU starvation */
#define IPC_SOFTIRQ_BUDGET 128

#define IPC_SHM_INSTANCE_DISABLED   0
#define IPC_SHM_INSTANCE_ENABLED    1

/* convenience wrappers for printing errors and debug messages */
#define shm_fmt(fmt) DRIVER_NAME": %s(): "fmt
#define shm_err(fmt, ...) pr_err(shm_fmt(fmt), __func__, ##__VA_ARGS__)
#define shm_dbg(fmt, ...) pr_debug(shm_fmt(fmt), __func__, ##__VA_ARGS__)

/* forward declarations */
struct IPCS_SHM_CFG_TYPE;

/* function declarations */
int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		int (*rx_cb)(const uint8_t, int));
void ipcsOsFree(const uint8_t instance);
uintptr_t ipcsOsGetLocalShm(const uint8_t instance);
uintptr_t ipcsOsGetRemoteShm(const uint8_t instance);
void *ipcsOsMapIntc(void);
void ipcsOsUnmapIntc(void *addr);
int ipcsOsPollChannels(const uint8_t instance);

#endif /* IPC_OS_H */
