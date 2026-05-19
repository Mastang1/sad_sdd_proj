/* SPDX-License-Identifier: BSD-3-Clause */
/*
 * Copyright 2018-2019,2021,2023 NXP
 */
#ifndef IPC_HW_H
#define IPC_HW_H

int ipcsHwInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg);

void ipcsHwFree(const uint8_t instance);

int ipcsHwGetRxIrq(const uint8_t instance);

void ipcsHwIrqEnable(const uint8_t instance);

void ipcsHwIrqDisable(const uint8_t instance);

void ipcsHwIrqNotify(const uint8_t instance);

void ipcsHwIrqClear(const uint8_t instance);

struct IPCS_SHM_REMOTE_CORE_TYPE;
struct IPCS_SHM_LOCAL_CORE_TYPE;
int _ipcsHwInit(const uint8_t instance, int tx_irq, int rx_irq,
		 const struct IPCS_SHM_REMOTE_CORE_TYPE *remote_core,
		 const struct IPCS_SHM_LOCAL_CORE_TYPE *local_core, void *mscm_addr);

#endif /* IPC_HW_H */
