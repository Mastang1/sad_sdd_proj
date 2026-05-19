/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2023 NXP
 */
#ifndef IPC_OS_H
#define IPC_OS_H

#include <errno.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>

/* softirq work budget used to prevent CPU starvation */
#define IPC_SOFTIRQ_BUDGET 128u

#define IPC_SHM_INSTANCE_DISABLED   0
#define IPC_SHM_INSTANCE_ENABLED    1

/* convenience wrappers for printing errors and debug messages */
#define pr_fmt(fmt) "ipc-shm-uio-lib: %s(): "fmt
#define shm_err(fmt, ...) printf(pr_fmt(fmt), __func__, ##__VA_ARGS__)
#ifdef DEBUG
#define shm_dbg(fmt, ...) printf(pr_fmt(fmt), __func__, ##__VA_ARGS__)
#else
#define shm_dbg(fmt, ...)
#endif

/* forward declarations */
struct IPCS_SHM_CFG_TYPE;

/* function declarations */
int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg,
		int (*rx_cb)(const uint8_t, int));
void ipcsOsFree(const uint8_t instance);
uintptr_t ipcsOsGetLocalShm(const uint8_t instance);
uintptr_t ipcsOsGetRemoteShm(const uint8_t instance);
int ipcsOsPollChannels(const uint8_t instance);

#endif /* IPC_OS_H */
