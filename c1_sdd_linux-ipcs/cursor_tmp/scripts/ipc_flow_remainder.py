# -*- coding: utf-8 -*-
"""RemainingPlantUMLdiagrams3_4_1..3_4_73 (register with W(slug,title,body))."""
from __future__ import annotations

from typing import Callable


def add_flows_remainder(W: Callable[..., None]) -> None:
    # --- ipc-queue.c / ipc-queue.h ---
    W(
        "3_4_1",
        "ipcsQueuePop",
        """
        start
        :write = queue->pop_ring->write; read = queue->push_ring->read; err = -IPC_SHM_E_INVAL;
        if ((queue != NULL) && (buf != NULL)?) then (yes)
          if (read == write?) then (yes)
            :err = -IPC_SHM_E_NO_QUEUE;
          else (no)
            :src = \&queue->pop_ring->data[read * elem_size];;
            :ipcsMemcpy(buf, src, elem_size);;
            :queue->push_ring->read = (read + 1u) %% queue->elem_num;;
            :err = IPC_SHM_E_OK;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_2",
        "ipcsQueuePush",
        """
        start
        :write = queue->push_ring->write; read = queue->pop_ring->read; err = -IPC_SHM_E_INVAL;
        if ((queue != NULL) && (buf != NULL)?) then (yes)
          if (((write + 1u) %% queue->elem_num) == read?) then (yes)
            :err = -IPC_SHM_E_NOMEM;
          else (no)
            :dst = \&queue->push_ring->data[write * elem_size];;
            :ipcsMemcpy(dst, buf, elem_size);;
            :queue->push_ring->write = (write + 1u) %% queue->elem_num;;
            :err = IPC_SHM_E_OK;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_3",
        "ipcsQueueInit",
        """
        start
        :err = -IPC_SHM_E_INVAL;
        if ((queue!=NULL)&&(push_ring_addr!=NULL)&&(pop_ring_addr!=NULL)&&(elem_num!=0)&&(elem_size!=0)&&((elem_size%%8)==0)?) then (yes)
          :queue->elem_num = elem_num + 1u;
          :queue->elem_size = elem_size;
          :queue->push_ring = (struct IPCS_RING_TYPE *)push_ring_addr;
          :queue->push_ring->sentinel = IPC_QUEUE_SENTINEL;
          :queue->push_ring->write = 0; queue->push_ring->read = 0;
          :queue->pop_ring = (struct IPCS_RING_TYPE *)pop_ring_addr;
          :err = IPC_SHM_E_OK;
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_4",
        "ipcsQueueCheckIntegrity",
        """
        start
        :err = -IPC_SHM_E_INTEGRITY;
        if ((IPC_QUEUE_SENTINEL == queue->pop_ring->sentinel) && (IPC_QUEUE_SENTINEL == queue->push_ring->sentinel)?) then (yes)
          :err = IPC_SHM_E_OK;
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_5",
        "ipcsQueueMemSize",
        """
        start
        :return (uint32)sizeof(struct IPCS_RING_TYPE) + (uint32)queue->elem_num * (uint32)queue->elem_size;
        stop
        """,
    )

    # --- ipc-shm.c static helpers ---
    W(
        "3_4_6",
        "getChannel",
        """
        start
        :struct IPCS_SHM_CHANNEL_TYPE *channel = NULL;
        if ((chan_id < 0) || (chan_id >= ipc_shm_priv_data[instance].num_channels)?) then (yes)
          :channel = NULL;
        else (no)
          :channel = \&ipc_shm_priv_data[instance].channels[chan_id];;
        endif
        :return channel;
        stop
        """,
    )
    W(
        "3_4_7",
        "getManagedChan",
        """
        start
        :struct IPCS_MANAGED_CHANNEL_TYPE *channel = NULL; struct IPCS_SHM_CHANNEL_TYPE *chan = getChannel(instance,chan_id);
        if ((chan == NULL) || (chan->type != IPC_SHM_MANAGED)?) then (yes)
          :channel = NULL;
        else (no)
          :channel = \&chan->ch.mng;;
        endif
        :return channel;
        stop
        """,
    )
    W(
        "3_4_8",
        "getUnmanagedChan",
        """
        start
        :struct IPCS_UNMANAGED_CHANNEL_TYPE *channel = NULL; struct IPCS_SHM_CHANNEL_TYPE *chan = getChannel(instance,chan_id);
        if ((chan == NULL) || (chan->type != IPC_SHM_UNMANAGED)?) then (yes)
          :channel = NULL;
        else (no)
          :channel = \&chan->ch.umng;;
        endif
        :return channel;
        stop
        """,
    )
    W(
        "3_4_9",
        "ipcsCheckUchanIntegrity",
        """
        start
        :err = -IPC_SHM_E_INTEGRITY;
        if ((local sentinel == IPC_UCHAN_SENTINEL)&&(remote sentinel == IPC_UCHAN_SENTINEL)?) then (yes)
          :err = IPC_SHM_E_OK;
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_10",
        "ipcsCheckMchanIntegrity",
        """
        start
        :err = IPC_SHM_E_OK; uint8 pool_id; struct IPCS_SHM_POOL_TYPE *pool=NULL;
        if (ipcsQueueCheckIntegrity(\&mchan->bd_queue) == IPC_SHM_E_OK?) then (yes)
          :pool_id = 0;
          while (pool_id < mchan->num_pools?)
            :pool = \&mchan->pools[pool_id];;
            if (ipcsQueueCheckIntegrity(\&pool->bd_queue) != IPC_SHM_E_OK?) then (yes)
              :err = -IPC_SHM_E_INTEGRITY;
            endif
            :pool_id++;;
          endwhile
        else (no)
          :err = -IPC_SHM_E_INTEGRITY;
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_11",
        "ipcsChannelRx",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id]\nmchan = &chan->ch.mng\nuchan = &chan->ch.umng\nwork = 0;;
        if (cfg->type == IPC_SHM_UNMANAGED?) then (yes)
          :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);;
          :work = 0;
          if (ipcsCheckUchanIntegrity(uchan) == OK?) then (yes)
            :remote_tx_count = uchan->remote_mem->tx_count;;
            if (remote_tx_count != uchan->remote_tx_count?) then (yes)
              :uchan->remote_tx_count = remote_tx_count;;
              :uchan->rx_cb(uchan->cb_arg, instance, chan->id, (void*)uchan->remote_mem->mem);;
              :work = budget;;
            endif
          endif
        else (no)
          :work = 0;
          while (work < budget?)
            :result = ipcsQueuePop(\&mchan->bd_queue,\&bd);;
            if (result != IPC_SHM_E_OK?) then (yes)
              break
            else (no)
              :pool = \&mchan->pools[bd.pool_id];;
              :buf_offset = pool->buf_size * bd.buf_id;;
              :buf_addr = pool->remote_pool_addr + buf_offset;;
              :mchan->rx_cb(mchan->cb_arg, instance, chan->id, (void*)buf_addr, bd.data_size);;
              :work++;;
            endif
          endwhile
        endif
        :return work;
        stop
        """,
    )
    W(
        "3_4_12",
        "ipcsInstanceIsFree",
        """
        start
        :err = IPC_SHM_INSTANCE_ERROR;
        if (instance < IPC_SHM_MAX_INSTANCES?) then (yes)
          if ((global==NULL) || (global->state==IPC_SHM_STATE_CLEAR)?) then (yes)
            :err = IPC_SHM_INSTANCE_FREE;
          else (no)
            :err = IPC_SHM_INSTANCE_USED;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_13",
        "ipcsShmRx",
        """
        start
        :num_chans = ipc_shm_priv_data[instance].num_channels\nchan_budget = 0\nchan_work = 0\nmore_work = 1\nwork = 0\ni = 0;;
        while ((work < budget) && (more_work > 0)?)
          :chan_budget = (budget-work)/num_chans;;
          if (chan_budget == 0?) then (yes)
            :chan_budget = 1;
          else (no)
          endif
          :more_work = 0;;
          :ipcsHwFlushCacheRemote(instance);;
          :i = 0;
          while (i < num_chans?)
            :chan_work = ipcsChannelRx(instance,(sint32)i,chan_budget);;
            :work += chan_work;;
            if (chan_work == chan_budget?) then (yes)
              :more_work = 1;
            endif
            :i++;;
          endwhile
        endwhile
        :return work;
        stop
        """,
    )
    W(
        "3_4_14",
        "ipcsBufPoolInit",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id].ch.mng\npool = &chan->pools[pool_id]\nlocal_shm = mng_pool.local_pool_shm\nremote_shm = mng_pool.remote_pool_shm\nerr = -IPC_SHM_E_INVAL; i = 0;;
        if (cfg->num_bufs <= IPC_SHM_MAX_BUFS_PER_POOL?) then (yes)
          :pool->num_bufs = cfg->num_bufs; pool->buf_size = cfg->buf_size;;
          :err = ipcsQueueInit(\&pool->bd_queue, pool->num_bufs, (uint8)sizeof(struct IPCS_SHM_BD_TYPE), local_shm, remote_shm);;
          if (err == IPC_SHM_E_OK?) then (yes)
            :queue_mem_size = ipcsQueueMemSize(\&pool->bd_queue);;
            :pool->local_pool_addr = local_shm + queue_mem_size;
            :pool->remote_pool_addr = remote_shm + queue_mem_size;
            :pool->shm_size = queue_mem_size + cfg->buf_size * cfg->num_bufs;;
            if ((local_shm + pool->shm_size) > (local_shm_base + shm_size)?) then (yes)
              :err = -IPC_SHM_E_NOMEM;
            else (no)
              :i = 0;
              while (i < pool->num_bufs?)
                :bd.pool_id = (sint16)pool_id\nbd.buf_id = i\nbd.data_size = 0;;
                :err = ipcsQueuePush(\&pool->bd_queue,\&bd);;
                if (err != IPC_SHM_E_OK?) then (yes)
                  break
                else (no)
                  :i++;;
                endif
              endwhile
            endif
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_15",
        "ipcsGetTotalBufPerChan",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id].ch.mng\nerr = -IPC_SHM_E_INVAL\nprev = 0\ntotal_bufs = 0\ni = 0;;
        if ((cfg->num_pools > 0u) && (cfg->num_pools <= IPC_SHM_MAX_POOLS)?) then (yes)
          :err = IPC_SHM_E_OK; chan->rx_cb = cfg->rx_cb; chan->cb_arg = cfg->cb_arg; chan->num_pools = cfg->num_pools;;
          :i = 0;
          while (i < chan->num_pools?)
            :pool_cfg = \&cfg->pools[i];;
            if (pool_cfg->buf_size < prev?) then (yes)
              :err = -IPC_SHM_E_INVAL;
            else (no)
              :prev = pool_cfg->buf_size; total_bufs += pool_cfg->num_bufs;;
            endif
            if ((err != IPC_SHM_E_OK) || (total_bufs > IPC_SHM_MAX_BUFS_PER_CHANNEL)?) then (yes)
              :err = -IPC_SHM_E_INVAL;
              break
            endif
            :i++;;
          endwhile
        else (no)
        endif
        if (err != IPC_SHM_E_OK?) then (yes)
          :total_bufs = 0u;
        endif
        :return total_bufs;
        stop
        """,
    )

    W(
        "3_4_16",
        "managedChannelInit",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id].ch.mng\nerr = -IPC_SHM_E_INVAL\ntotal_bufs = ipcsGetTotalBufPerChan(instance, chan_id, cfg)\nqueue_mem_size = 0\ni = 0;;
        :mng_pool_addr.local_pool_shm = (uintptr_t)NULL\nmng_pool_addr.remote_pool_shm = (uintptr_t)NULL;;
        if (total_bufs != 0u?) then (yes)
          :err = ipcsQueueInit(\&chan->bd_queue,(uint16)total_bufs,sizeof BD,local_shm,remote_shm);;
          if (err == IPC_SHM_E_OK?) then (yes)
            :queue_mem_size = ipcsQueueMemSize(\&chan->bd_queue);;
            :mng_pool_addr.local_pool_shm = local_shm + queue_mem_size;
            :mng_pool_addr.remote_pool_shm = remote_shm + queue_mem_size;;
            if ((mng_pool_addr.local_pool_shm + queue_mem_size) > (ipcsOsGetLocalShm(instance) + shm_size)?) then (yes)
              :err = -IPC_SHM_E_NOMEM;
            else (no)
              :i = 0;
              while ((err == IPC_SHM_E_OK) && (i < chan->num_pools)?)
                :err = ipcsBufPoolInit(instance, chan_id,i,mng_pool_addr,\&cfg->pools[i]);;
                if (err != IPC_SHM_E_OK?) then (yes)
                  break
                else (no)
                  :mng_pool_addr.local_pool_shm += chan->pools[i].shm_size\nmng_pool_addr.remote_pool_shm += chan->pools[i].shm_size;;
                  :i++;;
                endif
              endwhile
            endif
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_17",
        "unmanagedChannelInit",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id].ch.umng\nerr = -IPC_SHM_E_INVAL;;
        if (cfg->size <= IPC_SHM_MAX_UMNG_SIZE?) then (yes)
          :chan->size = cfg->size\nchan->rx_cb = cfg->rx_cb\nchan->cb_arg = cfg->cb_arg;;
          :chan->local_mem = (struct IPCS_CHANNEL_UMEM_TYPE *)local_shm\nchan->remote_mem = (struct IPCS_CHANNEL_UMEM_TYPE *)remote_shm;;
          :local sentinel = IPC_UCHAN_SENTINEL; local tx_count = 0; remote_tx_copy = 0;;
          :err = IPC_SHM_E_OK;
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_18",
        "ipcsShmInitChannel",
        """
        start
        :chan = &ipc_shm_priv_data[instance].channels[chan_id]\nerr = -IPC_SHM_E_INVAL;;
        if (cfg != NULL?) then (yes)
          :chan->id = chan_id; chan->type = cfg->type;;
          if (cfg->type == IPC_SHM_MANAGED?) then (yes)
            if ((cfg->ch.managed.rx_cb==NULL)||(cfg->ch.managed.pools==NULL)?) then (yes)
              :err = -IPC_SHM_E_INVAL;
            else (no)
              :err = managedChannelInit(instance, chan_id, local_shm, remote_shm, \&cfg->ch.managed);;
            endif
          elseif (cfg->type == IPC_SHM_UNMANAGED?) then (yes)
            if (cfg->ch.unmanaged.rx_cb==NULL?) then (yes)
              :err = -IPC_SHM_E_INVAL;
            else (no)
              :err = unmanagedChannelInit(instance, chan_id, local_shm, remote_shm, \&cfg->ch.unmanaged);;
            endif
          else (IPC_SHM other type?)
            :err = -IPC_SHM_E_INVAL;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_19",
        "getChanMemmapSize",
        """
        start
        if (chan->type == IPC_SHM_UNMANAGED?) then (yes)
          :mapped_mem_size = (uint32)(sizeof(struct IPCS_CHANNEL_UMEM_TYPE)+chan->ch.umng.size);
        else (no)
          :mchan = \&chan->ch.mng; mapped_mem_size = ipcsQueueMemSize(\&mchan->bd_queue);;
          :uint8 idx = 0;
          while (idx < mchan->num_pools?)
            :mapped_mem_size += mchan->pools[idx].shm_size;;
            :idx++;;
          endwhile
        endif
        :return mapped_mem_size;
        stop
        """,
    )
    W(
        "3_4_20",
        "ipcsShmInitChannels",
        """
        start
        :local_shm = ipcsOsGetLocalShm(instance)\nremote_shm = ipcsOsGetRemoteShm(instance)\nglobal = (struct IPCS_SHM_GLOBAL_TYPE *)local_shm;;
        :local_chan = local_shm + sizeof(struct IPCS_SHM_GLOBAL_TYPE)\nremote_chan = remote_shm + sizeof(struct IPCS_SHM_GLOBAL_TYPE)\nerr = -IPC_SHM_E_INVAL;;
        :i = 0;
        while (i < ipc_shm_priv_data[instance].num_channels?)
          :err = ipcsShmInitChannel(instance,i,local_chan,remote_chan,\&cfg->channels[i]);;
          if (err == IPC_SHM_E_OK?) then (yes)
            :chan_size = getChanMemmapSize(instance, i)\nlocal_chan += chan_size\nremote_chan += chan_size;;
            :i++;;
          else (no)
            :ipcsOsFree(instance); ipcsHwFree(instance);;
            break
          endif
        endwhile
        :return err;
        stop
        """,
    )
    W(
        "3_4_21",
        "ipcsShmInitInstance",
        """
        start
        :sint32 err = -IPC_SHM_E_INVAL;
        if ((cfg != NULL)&&(local/remote shm != NULL)&&(num_channels>=1u)&&(num_channels<=IPC_SHM_MAX_CHANNELS)?) then (yes)
          :ipc_shm_priv_data[instance].shm_size = cfg->shm_size\nipc_shm_priv_data[instance].num_channels = cfg->num_channels;;
          :err = ipcsHwInit(instance,cfg);;
          if (err == IPC_SHM_E_OK?) then (yes)
            :err = ipcsOsInit(instance,cfg,ipcsShmRx);;
            if (err != IPC_SHM_E_OK?) then (yes)
              :ipcsHwFree(instance);;
            else (no)
              :err = ipcsShmInitChannels(instance,cfg);;
              if (err == IPC_SHM_E_OK?) then (yes)
                :ipcsHwIrqClear(instance); ipcsHwIrqEnable(instance);;
                :global->state = IPC_SHM_STATE_READY;;
                :ipcsHwFlushCacheLocal(instance);;
              endif
            endif
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_22",
        "findPoolForBuf",
        """
        start
        :pool_index = -1; uint8 pool_id = 0;
        while (pool_id < chan->num_pools?)
          :pool = \&chan->pools[pool_id];;
          if (remote==1?) then (yes)
            :addr = pool->remote_pool_addr;
          else (no)
            :addr = pool->local_pool_addr;
          endif
          :pool_size = num_bufs * buf_size;;
          if ((buf >= addr) && (buf < addr+pool_size)?) then (yes)
            :pool_index = (sint16)pool_id; break;
          endif
          :pool_id++;;
        endwhile
        :return pool_index;
        stop
        """,
    )
    W(
        "3_4_23",
        "ipcsMemcpy",
        """
        start
        :tmp_dst/tmp_src iterators; uint32 i=0;
        if ((dst!=NULL)&&(src!=NULL)?) then (yes)
          while (i < data_size?)
            :tmp_dst[i]=tmp_src[i];;
            :i++;;
          endwhile
        endif
        stop
        """,
    )

    W(
        "3_4_24",
        "ipcsHwGetCoreIndexM7",
        """
        start
        if (index==IPC_CORE_INDEX_0?) then (yes)
          :core_index=(sint8)IPC_M7_0;
        elseif (index==IPC_CORE_INDEX_1?) then (yes)
          :core_index=(sint8)IPC_M7_1;
        elseif (index==IPC_CORE_INDEX_2?) then (yes)
          :core_index=(sint8)IPC_M7_2;
        elseif (index==IPC_CORE_INDEX_3?) then (yes)
          :core_index=(sint8)IPC_M7_3;
        else (no)
          :core_index=-IPC_SHM_E_INVAL;
        endif
        :return core_index;
        stop
        """,
    )
    W(
        "3_4_25",
        "ipcsHwGetCoreIndexA53",
        """
        start
        if (index==IPC_CORE_INDEX_0?) then (yes)
          :core_index=(sint8)IPC_A53_0;
        elseif (index==IPC_CORE_INDEX_1?) then (yes)
          :core_index=(sint8)IPC_A53_1;
        elseif (index==IPC_CORE_INDEX_2?) then (yes)
          :core_index=(sint8)IPC_A53_2;
        elseif (index==IPC_CORE_INDEX_3?) then (yes)
          :core_index=(sint8)IPC_A53_3;
        elseif (index==IPC_CORE_INDEX_4?) then (yes)
          :core_index=(sint8)IPC_A53_4;
        elseif (index==IPC_CORE_INDEX_5?) then (yes)
          :core_index=(sint8)IPC_A53_5;
        elseif (index==IPC_CORE_INDEX_6?) then (yes)
          :core_index=(sint8)IPC_A53_6;
        elseif (index==IPC_CORE_INDEX_7?) then (yes)
          :core_index=(sint8)IPC_A53_7;
        else (no)
          :core_index=-IPC_SHM_E_INVAL;
        endif
        :return core_index;
        stop
        """,
    )
    W(
        "3_4_26",
        "ipcsHwSetRemoteCore",
        """
        start
        :sint8 err=-IPC_SHM_E_INVAL; sint8 core_idx=0;;
        if (remote_core.type==IPC_CORE_A53?) then (yes)
          if ((remote index 0..7)?) then (yes)
            :core_idx=ipcsHwGetCoreIndexA53((uint8)cfg->remote_core.index);;
            if (core_idx>=(sint8)IPC_A53_0?) then (yes)
              :ipc_hw_priv[instance].remote_core=(uint8)core_idx;;
              :err=IPC_SHM_E_OK;
            endif
          endif
        elseif (remote_core.type==IPC_CORE_M7?) then (yes)
          if ((remote index 0..3)?) then (yes)
            :core_idx=ipcsHwGetCoreIndexM7((uint8)cfg->remote_core.index);;
            if (core_idx>=(sint8)IPC_M7_0?) then (yes)
              :ipc_hw_priv[instance].remote_core=(uint8)core_idx;;
              :err=IPC_SHM_E_OK;
            endif
          endif
        else (no)
          :err=-IPC_SHM_E_INVAL;
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_27",
        "ipcsHwSetLocalCore",
        """
        start
        :sint8 err=-IPC_SHM_E_INVAL; sint8 core_idx=0;;
        if (local_core.type==IPC_CORE_A53?) then (yes)
          if ((local index 0..7)?) then (yes)
            :core_idx=ipcsHwGetCoreIndexA53((uint8)cfg->local_core.index);;
            if (core_idx>=(sint8)IPC_A53_0?) then (yes)
              :ipc_hw_priv[instance].local_core=(uint8)core_idx;;
              :err=IPC_SHM_E_OK;
            endif
          endif
        elseif (local_core.type==IPC_CORE_M7?) then (yes)
          if ((local index 0..3)?) then (yes)
            :core_idx=ipcsHwGetCoreIndexM7((uint8)cfg->local_core.index);;
            if (core_idx>=(sint8)IPC_M7_0?) then (yes)
              :ipc_hw_priv[instance].local_core=(uint8)core_idx;;
              :err=IPC_SHM_E_OK;
            endif
          endif
        else (no)
          :err=-IPC_SHM_E_INVAL;
        endif
        :return err;
        stop
        """,
    )

    W(
        "3_4_28",
        "ipcsHwSetCore",
        """
        start
        :err=IPC_SHM_E_OK; uint8 local_core_idx=(uint8)(IP_MSCM->CPXNUM & MSCM_CPXNUM_CPN_MASK);;
        :err = ipcsHwSetRemoteCore(instance,cfg);;
        if (err == IPC_SHM_E_OK?) then (yes)
          :err = ipcsHwSetLocalCore(instance,cfg);;
        endif
        if (err == IPC_SHM_E_OK?) then (yes)
          if ((remote!=local)&&(local==local_core_idx)?) then (yes)
            :err=IPC_SHM_E_OK;
          else (no)
            :err=-IPC_SHM_E_INVAL;
          endif
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_29",
        "ipcsHwSetTxIrqIdx",
        """
        start
        :sint8 err=IPC_SHM_E_OK; uint16 irq=(uint16)cfg->inter_core_tx_irq;;
        :ipc_hw_priv[instance].mscm_tx_irq = cfg->inter_core_tx_irq;;
        if (cfg->inter_core_tx_irq == IPC_IRQ_NONE?) then (yes)
          :ipc_hw_priv[instance].mscm_tx_irq = IPC_IRQ_NONE;
        elseif (irq == MSCM_INT0_IRQn?) then (yes)
          :msi_tx_irq = 0u;
        elseif (irq == MSCM_INT1_IRQn?) then (yes)
          :msi_tx_irq = 1u;
        elseif (irq == MSCM_INT2_IRQn?) then (yes)
          :msi_tx_irq = 2u;
        elseif (irq == MSCM_INT3_IRQn?) then (yes)
          :msi_tx_irq = 5u;
        elseif (irq == MSCM_INT4_IRQn?) then (yes)
          :msi_tx_irq = 6u;
        elseif (irq == MSCM_INT5_IRQn?) then (yes)
          :msi_tx_irq = 7u;
        elseif (irq == MSCM_INT6_IRQn?) then (yes)
          :msi_tx_irq = 8u;
        elseif (irq == MCSCM_INT7_IRQn?) then (yes)
          :msi_tx_irq = 9u;
        elseif (irq == MCSCM_INT8_IRQn?) then (yes)
          :msi_tx_irq = 10u;
        elseif (irq == MCSCM_INT9_IRQn?) then (yes)
          :msi_tx_irq = 11u;
        elseif (irq == MCSCM_INT10_IRQn?) then (yes)
          :msi_tx_irq = 12u;
        elseif (irq == MCSCM_INT11_IRQn?) then (yes)
          :msi_tx_irq = 13u;
        else (no)
          :err = -IPC_SHM_E_INVAL;
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_30",
        "ipcsHwSetRxIrqIdx",
        """
        start
        :sint8 err=IPC_SHM_E_OK; uint16 irq=(uint16)cfg->inter_core_rx_irq;;
        :ipc_hw_priv[instance].mscm_rx_irq = cfg->inter_core_rx_irq;;
        if (cfg->inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
          :ipc_hw_priv[instance].mscm_rx_irq = IPC_IRQ_NONE;
        elseif (irq == MSCM_INT0_IRQn?) then (yes)
          :msi_rx_irq = 0u;
        elseif (irq == MSCM_INT1_IRQn?) then (yes)
          :msi_rx_irq = 1u;
        elseif (irq == MSCM_INT2_IRQn?) then (yes)
          :msi_rx_irq = 2u;
        elseif (irq == MSCM_INT3_IRQn?) then (yes)
          :msi_rx_irq = 5u;
        elseif (irq == MSCM_INT4_IRQn?) then (yes)
          :msi_rx_irq = 6u;
        elseif (irq == MSCM_INT5_IRQn?) then (yes)
          :msi_rx_irq = 7u;
        elseif (irq == MSCM_INT6_IRQn?) then (yes)
          :msi_rx_irq = 8u;
        elseif (irq == MCSCM_INT7_IRQn?) then (yes)
          :msi_rx_irq = 9u;
        elseif (irq == MCSCM_INT8_IRQn?) then (yes)
          :msi_rx_irq = 10u;
        elseif (irq == MCSCM_INT9_IRQn?) then (yes)
          :msi_rx_irq = 11u;
        elseif (irq == MCSCM_INT10_IRQn?) then (yes)
          :msi_rx_irq = 12u;
        elseif (irq == MCSCM_INT11_IRQn?) then (yes)
          :msi_rx_irq = 13u;
        else (no)
          :err = -IPC_SHM_E_INVAL;
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_31",
        "ipcsHwSetIrqIdx",
        """
        start
        :err=IPC_SHM_E_OK;;
        if ((cfg->inter_core_rx_irq==cfg->inter_core_tx_irq)&&(cfg->inter_core_rx_irq!=IPC_IRQ_NONE)?) then (yes)
          :err=-IPC_SHM_E_INVAL;
        else (no)
          :err=ipcsHwSetTxIrqIdx(instance,cfg);;
          if (err == IPC_SHM_E_OK?) then (yes)
            :err=ipcsHwSetRxIrqIdx(instance,cfg);;
          endif
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_32",
        "ipcsHwInit",
        """
        start
        :err=IPC_SHM_E_OK;;
        :err = ipcsHwSetCore(instance,cfg);;
        if (err == IPC_SHM_E_OK?) then (yes)
          :err = ipcsHwSetIrqIdx(instance,cfg);;
        endif
        if (err == IPC_SHM_E_OK?) then (yes)
          :ipc_hw_priv[instance].shm_size = cfg->shm_size;;
          :ipcsHwIrqDisable(instance);;
          :ipcsHwIrqClear(instance);;
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_33",
        "ipcsHwFree",
        """
        start
        :ipcsHwIrqClear(instance);;
        stop
        """,
    )
    W(
        "3_4_34",
        "ipcsHwIrqEnable",
        """
        start
        if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
          note right
            unless USING_OS_AUTOSAROS compile flag set IRSPRC enable bit
          end note
          :IP_MSCM->IRSPRC[ipc_hw_priv[instance].mscm_rx_irq] |= ((uint16)1u << (ipc_hw_priv[instance].local_core - (uint8)IPC_M7_0 + 1u));;
        else (no)
        endif
        stop
        """,
    )
    W(
        "3_4_35",
        "ipcsHwIrqDisable",
        """
        start
        if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
          note right
            unless USING_OS_AUTOSAROS clear IRSPRC bit
          end note
          :IP_MSCM->IRSPRC[ipc_hw_priv[instance].mscm_rx_irq] &= ~((uint16)1u << (ipc_hw_priv[instance].local_core - (uint8)IPC_M7_0 + 1u));;
        endif
        stop
        """,
    )
    W(
        "3_4_36",
        "ipcsHwIrqNotify",
        """
        start
        if (mscm_tx_irq != IPC_IRQ_NONE?) then (yes)
          :remote_core = ipc_hw_priv[instance].remote_core\nmsi_tx_index = ipc_hw_priv[instance].msi_tx_irq;;
          :IPC_MSCM_IRCPnIRx->IRCPnIRx[remote_core][msi_tx_index].IPC_IGR |= IPC_MSCM_IRCPnIGRx_INT_EN;;
        endif
        stop
        """,
    )
    W(
        "3_4_37",
        "ipcsHwIrqClear",
        """
        start
        if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
          :local_core = ipc_hw_priv[instance].local_core\nremote_core = ipc_hw_priv[instance].remote_core\nmsi_rx_index = ipc_hw_priv[instance].msi_rx_irq;;
          if ((IPC_M7_0 <= remote_core <= IPC_M7_3)?) then (yes)
            :IPC_ISR = (1<<remote_core);;
          else (no)
            :IPC_ISR = IPC_MSCM_IRCPnISRx_CLEAR_A53;;
          endif
        endif
        stop
        """,
    )
    W(
        "3_4_38",
        "ipcsHwFlushCache static",
        """
        start
        if (IPC_D_CACHE_ENABLE defined?) then (yes)
          :MCAL_DATA_SYNC_BARRIER(); MCAL_INSTRUCTION_SYNC_BARRIER();;
          repeat
            :S32_SCB->DCCIMVAC = data_addr_tmp;;
            :data_addr_tmp += IPC_DCACHE_LINE_SIZE;;
            :data_size_tmp -= IPC_DCACHE_LINE_SIZE;;
          repeat while (data_size_tmp > 0?) is (yes)
          :MCAL_DATA_SYNC_BARRIER(); MCAL_INSTRUCTION_SYNC_BARRIER();;
        else (no)
        endif
        stop
        """,
    )
    W(
        "3_4_39",
        "ipcsHwFlushCacheLocal",
        """
        start
        if (IPC_D_CACHE_ENABLE defined?) then (yes)
          :data_addr = ipcsOsGetLocalShm(instance)\ndata_size = ipc_hw_priv[instance].shm_size\ntmp_size = data_size + (data_addr & (IPC_DCACHE_LINE_SIZE - 1U))\ntmp_addr = data_addr;;
          :ipcsHwFlushCache(tmp_addr,tmp_size);;
        else (no)
          :(void)instance;
        endif
        stop
        """,
    )
    W(
        "3_4_40",
        "ipcsHwFlushCacheRemote",
        """
        start
        if (IPC_D_CACHE_ENABLE defined?) then (yes)
          :data_addr = ipcsOsGetRemoteShm(instance)\ndata_size = ipc_hw_priv[instance].shm_size\ntmp_size = data_size + (data_addr & (IPC_DCACHE_LINE_SIZE - 1U))\ntmp_addr = data_addr;;
          :ipcsHwFlushCache(tmp_addr,tmp_size);;
        else (no)
          :(void)instance;
        endif
        stop
        """,
    )

    # --- os/autosar/ipc-os-autosar.c ---
    W(
        "3_4_41",
        "ipcsOsInit autosar",
        """
        start
        :StatusType os_status=E_OK; TaskStateType task_state=SUSPENDED; err=-IPC_SHM_E_INVAL;;
        if (rx_cb != NULL?) then (yes)
          :ipc_os_priv.id[instance].local_shm = cfg->local_shm_addr\nipc_os_priv.id[instance].remote_shm = cfg->remote_shm_addr\nipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED\nipc_os_priv.rx_cb = rx_cb\nipc_os_priv.id[instance].rx_irq_num = cfg->inter_core_rx_irq\nipc_os_priv.id[instance].msg_received = MSG_NOT_RECEIVED\nipc_os_priv.id[instance].isr_id_handler = cfg->isr_id_handler;;
          if ((rx_irq==IPC_IRQ_NONE)||(task_is_initialized!=0)?) then (yes)
            :err = IPC_SHM_E_OK;
          else (no)
            :GetTaskState(ipcsShmSoftirq,\&task_state);;
            if (task_state != SUSPENDED?) then (yes)
              :err=-IPC_SHM_E_NOTSUP;
            else (no)
              :os_status=ActivateTask(ipcsShmSoftirq);;
              if (os_status != E_OK?) then (yes)
                :err=-IPC_SHM_E_NOTSUP;
              else (no)
                :task_is_initialized=1;;
                :err=IPC_SHM_E_OK;
              endif
            endif
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_42",
        "ipcsOsFree autosar",
        """
        start
        :ipcsHwIrqDisable(instance);;
        :rx_cb=NULL; id[inst].state=DISABLED;;
        if (rx_irq != IPC_IRQ_NONE?) then (yes)
          :DisableInterruptSource(isr_id_handler);;
          if (task_is_initialized!=0?) then (yes)
            :SetEvent(ipcsShmSoftirq,IPC_EVENT_OS_FREE);;
            :task_is_initialized=0;;
          endif
        endif
        stop
        """,
    )
    W(
        "3_4_43",
        "TASK ipcsShmSoftirq autosar",
        """
        start
        while (forever?) is (yes)
          :os_status = WaitEvent(IPC_EVENT_RX_IRQ | IPC_EVENT_OS_FREE);;
          :os_status = GetEvent(ipcsShmSoftirq, \&event);;
          if ((event \& IPC_EVENT_OS_FREE) != 0?) then (yes)
            :os_status = ClearEvent(IPC_EVENT_OS_FREE);;
            :os_status = TerminateTask();;
            stop
          else (no)
          endif
          :i = 0;
          while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
            if ((id[i].state == IPC_SHM_INSTANCE_DISABLED)||(id[i].msg_received == MSG_NOT_RECEIVED)||(id[i].rx_irq_num == IPC_IRQ_NONE)?) then (yes)
            else (no)
              repeat
                :work = ipc_os_priv.rx_cb(i, IPC_SOFTIRQ_BUDGET);;
                :os_status = Schedule();;
              repeat while (work >= IPC_SOFTIRQ_BUDGET?) is (yes)
              :id[i].msg_received = MSG_NOT_RECEIVED;;
            endif
            :i++;
          endwhile (no)
          :os_status = ClearEvent(IPC_EVENT_RX_IRQ);;
          :i = 0;
          while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
            if ((id[i].state != IPC_SHM_INSTANCE_DISABLED) \&\& (id[i].rx_irq_num != IPC_IRQ_NONE)?) then (yes)
              :ipcsHwIrqClear(i);;
              :os_status = EnableInterruptSource(id[i].isr_id_handler, TRUE);;
            else (no)
            endif
            :i++;
          endwhile (no)
        endwhile (no)
        stop
        """,
    )
    W(
        "3_4_44",
        "ipcsShmHardirq autosar",
        """
        start
        :i = 0;
        while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
          if ((id[i].state != IPC_SHM_INSTANCE_DISABLED) \&\& (id[i].rx_irq_num != IPC_IRQ_NONE)?) then (yes)
            :os_status = DisableInterruptSource(id[i].isr_id_handler);;
            :id[i].msg_received = MSG_IS_RECEIVED;;
          else (no)
          endif
          :i++;
        endwhile (no)
        :os_status = SetEvent(ipcsShmSoftirq, IPC_EVENT_RX_IRQ);;
        stop
        """,
    )
    W(
        "3_4_45",
        "ipcsShmHardirqInstance autosar",
        """
        start
        if ((id[instance].state != IPC_SHM_INSTANCE_DISABLED) \&\& (id[instance].rx_irq_num != IPC_IRQ_NONE)?) then (yes)
          :os_status = DisableInterruptSource(id[instance].isr_id_handler);;
          if (id[instance].msg_received == MSG_NOT_RECEIVED?) then (yes)
            :id[instance].msg_received = MSG_IS_RECEIVED;;
          endif
          :os_status = SetEvent(ipcsShmSoftirq, IPC_EVENT_RX_IRQ);;
        else (no)
        endif
        stop
        """,
    )
    W(
        "3_4_46",
        "ipcsOsGetLocalShm autosar",
        """
        start
        :return ipc_os_priv.id[instance].local_shm;
        stop
        """,
    )
    W(
        "3_4_47",
        "ipcsOsGetRemoteShm autosar",
        """
        start
        :return ipc_os_priv.id[instance].remote_shm;
        stop
        """,
    )
    W(
        "3_4_48",
        "ipcsOsPollChannels autosar",
        """
        start
        :err=-IPC_SHM_E_NOTSUP;;
        if (rx_irq == IPC_IRQ_NONE?) then (yes)
          if (rx_cb != NULL?) then (yes)
            :err = rx_cb(instance,IPC_SOFTIRQ_BUDGET);;
          else (no)
            :err=-IPC_SHM_E_INVAL;;
          endif
        endif
        :return err;
        stop
        """,
    )

    # --- §5.4 FreeRTOS (md refs 3_4_49..55; baremetal out of doc scope) ---
    W(
        "3_4_49",
        "ipcsOsInit FreeRTOS",
        """
        start
        :err=-IPC_SHM_E_INVAL;;
        if (rx_cb != NULL?) then (yes)
          :id[instance].local_shm = cfg->local_shm_addr; id[instance].remote_shm = cfg->remote_shm_addr;;
          :id[instance].state = IPC_SHM_INSTANCE_ENABLED; ipc_os_priv.rx_cb = rx_cb;;
          :id[instance].rx_irq_num = cfg->inter_core_rx_irq; id[instance].msg_received = MSG_NOT_RECEIVED;;
          if ((id[instance].rx_irq_num == IPC_IRQ_NONE)||(task_is_initialized != 0)?) then (yes)
            :err = IPC_SHM_E_OK;;
          else (no)
            :os_status = xTaskCreate(ipcsShmSoftirq, "softirq", IPC_SOFTIRQ_STACK_SIZE, NULL, IPC_SOFTIRQ_PRIORITY, \&softirq_handle);;
            if (os_status != pdPASS?) then (yes)
              :err=-IPC_SHM_E_NOMEM;;
            else (no)
              :task_is_initialized=1;;
              :err = IPC_SHM_E_OK;;
            endif
          endif
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_50",
        "ipcsOsFree FreeRTOS",
        """
        start
        :HwIrqDisable(instance);;
        :rx_cb=NULL; state=DISABLED;;
        if (rx_irq != IPC_IRQ_NONE?) then (yes)
          if (task_is_initialized!=0?) then (yes)
            :vTaskDelete(softirq_handle);;
            :task_is_initialized=0;;
          endif
        endif
        stop
        """,
    )
    W(
        "3_4_51",
        "ipcsShmHardirq FreeRTOS",
        """
        start
        :higher_prio_task_woken = pdFALSE;;
        :task_critical_status_from_isr = taskENTER_CRITICAL_FROM_ISR();;
        :i = 0;
        while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
          if (id[i].state == DISABLED?) then (yes)
          else (no)
            :ipcsHwIrqDisable(i);;
            :ipcsHwIrqClear(i);;
            :id[i].msg_received = MSG_IS_RECEIVED;;
          endif
          :i++;
        endwhile (no)
        :vTaskNotifyGiveFromISR(softirq_handle, \&higher_prio_task_woken);;
        :taskEXIT_CRITICAL_FROM_ISR(task_critical_status_from_isr);;
        :portYIELD_FROM_ISR(higher_prio_task_woken);;
        stop
        """,
    )
    W(
        "3_4_52",
        "ipcsShmHardirqInstance FreeRTOS",
        """
        start
        :higher_prio_task_woken = pdFALSE;;
        :task_critical_status_from_isr = taskENTER_CRITICAL_FROM_ISR();;
        if (id[instance].state != DISABLED?) then (yes)
          :ipcsHwIrqDisable(instance);;
          :ipcsHwIrqClear(instance);;
          if (msg_received == MSG_NOT_RECEIVED?) then (yes)
            :msg_received = MSG_IS_RECEIVED;;
          endif
          :vTaskNotifyGiveFromISR(softirq_handle, \&higher_prio_task_woken);;
        endif
        :taskEXIT_CRITICAL_FROM_ISR(task_critical_status_from_isr);;
        :portYIELD_FROM_ISR(higher_prio_task_woken);;
        stop
        """,
    )
    W(
        "3_4_53",
        "ipcsOsGetLocalShm baremetal",
        """
        start
        :return ipc_os_priv.id[instance].local_shm;
        stop
        """,
    )
    W(
        "3_4_54",
        "ipcsOsGetRemoteShm baremetal",
        """
        start
        :return ipc_os_priv.id[instance].remote_shm;
        stop
        """,
    )
    W(
        "3_4_55",
        "ipcsOsPollChannels baremetal",
        """
        start
        :err=-IPC_SHM_E_NOTSUP;;
        if (rx_irq == IPC_IRQ_NONE?) then (yes)
          if (rx_cb != NULL?) then (yes)
            :err = rx_cb(instance,budget);;
          else (no)
            :err=-IPC_SHM_E_INVAL;;
          endif
        endif
        :return err;
        stop
        """,
    )

    # --- os/freertos/ipc-os-freertos.c ---
    W(
        "3_4_56",
        "ipcsOsInit FreeRTOS",
        """
        start
        :err=-IPC_SHM_E_INVAL;;
        if (rx_cb != NULL?) then (yes)
          :id[instance].local_shm = cfg->local_shm_addr; id[instance].remote_shm = cfg->remote_shm_addr;;
          :id[instance].state = IPC_SHM_INSTANCE_ENABLED; ipc_os_priv.rx_cb = rx_cb;;
          :id[instance].rx_irq_num = cfg->inter_core_rx_irq; id[instance].msg_received = MSG_NOT_RECEIVED;;
          if ((id[instance].rx_irq_num == IPC_IRQ_NONE)||(task_is_initialized != 0)?) then (yes)
            :err = IPC_SHM_E_OK;;
          else (no)
            :os_status = xTaskCreate(ipcsShmSoftirq, "softirq", IPC_SOFTIRQ_STACK_SIZE, NULL, IPC_SOFTIRQ_PRIORITY, \&softirq_handle);;
            if (os_status != pdPASS?) then (yes)
              :err=-IPC_SHM_E_NOMEM;;
            else (no)
              :task_is_initialized=1;;
              :err = IPC_SHM_E_OK;;
            endif
          endif
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_57",
        "ipcsOsFree FreeRTOS",
        """
        start
        :HwIrqDisable(instance);;
        :rx_cb=NULL; state=DISABLED;;
        if (rx_irq != IPC_IRQ_NONE?) then (yes)
          if (task_is_initialized!=0?) then (yes)
            :vTaskDelete(softirq_handle);;
            :task_is_initialized=0;;
          endif
        endif
        stop
        """,
    )
    W(
        "3_4_58",
        "ipcsShmSoftirq FreeRTOS",
        """
        start
        :(void) ulTaskNotifyTake(pdTRUE, portMAX_DELAY);;
        while (forever?) is (yes)
          :i = 0;
          while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
            if ((state==DISABLED)||(msg_received==MSG_NOT_RECEIVED)||(rx_irq==IPC_IRQ_NONE)?) then (yes)
            else (no)
              repeat
                :work = ipc_os_priv.rx_cb(i, IPC_SOFTIRQ_BUDGET);;
                :taskYIELD();;
              repeat while (work >= IPC_SOFTIRQ_BUDGET?) is (yes)
              :id[i].msg_received = MSG_NOT_RECEIVED;;
            endif
            :i++;
          endwhile (no)
          :i = 0;
          while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
            if (state != DISABLED?) then (yes)
              :ipcsHwIrqEnable(i);;
            else (no)
            endif
            :i++;
          endwhile (no)
          :(void) ulTaskNotifyTake(pdTRUE, portMAX_DELAY);;
        endwhile (no)
        stop
        """,
    )
    W(
        "3_4_59",
        "ipcsShmHardirq FreeRTOS",
        """
        start
        :taskENTER_CRITICAL_FROM_ISR;;
        :for instances not DISABLED HwDisable+HwClear+MSG_IS_RECEIVED;;
        :vTaskNotifyGiveFromISR(ipc_os_priv.softirq_handle,...);;
        :taskEXIT_CRITICAL_FROM_ISR;;
        :portYIELD_FROM_ISR(..);;
        stop
        """,
    )
    W(
        "3_4_60",
        "ipcsShmHardirqInstance FreeRTOS",
        """
        start
        :taskENTER_CRITICAL_FROM_ISR;;
        if (state!=DISABLED?) then (yes)
          :HwDisable; HwClear;;
          if (msg_received == MSG_NOT_RECEIVED?) then (yes)
            :msg_received=MSG_IS_RECEIVED;;
          endif
          :vTaskNotifyGiveFromISR(..);;
        endif
        :taskEXIT_CRITICAL_FROM_ISR;;
        :portYIELD_FROM_ISR(..);;
        stop
        """,
    )
    W(
        "3_4_61",
        "ipcsOsGetLocalShm FreeRTOS",
        """
        start
        :return ipc_os_priv.id[instance].local_shm;;
        stop
        """,
    )
    W(
        "3_4_62",
        "ipcsOsGetRemoteShm FreeRTOS",
        """
        start
        :return ipc_os_priv.id[instance].remote_shm;;
        stop
        """,
    )
    W(
        "3_4_63",
        "ipcsOsPollChannels FreeRTOS",
        """
        start
        :err=-IPC_SHM_E_NOTSUP;;
        if (rx_irq == IPC_IRQ_NONE?) then (yes)
          if (rx_cb != NULL?) then (yes)
            :err = rx_cb(instance,IPC_SOFTIRQ_BUDGET);;
          else (no)
            :err=-IPC_SHM_E_INVAL;;
          endif
        endif
        :return err;
        stop
        """,
    )

    # --- os/zephyr/ipc-os-zephyr.c ---
    W(
        "3_4_64",
        "ipcsShmSoftirq Zephyr",
        """
        start
        :(void) err = k_sem_take(\&rx_sem,K_FOREVER); __ASSERT_NO_MSG;;
        :Repeated body from ipc-os-zephyr.c k_sem_take then instance loop;;
        note right
          when irq!=NONE call irq_enable before ipcsHwIrqEnable instance
        end note
        :k_sem_take(\&rx_sem,K_FOREVER) again at loop tail;
        stop
        """,
    )
    W(
        "3_4_65",
        "ipcsShmHardirq Zephyr",
        """
        start
        :for alive instances irq_disable?(if IRQ!=NONE);;
        :HwIrqDisable; HwIrqClear; MSG_IS_RECEIVED per instance;;
        :k_sem_give(\&ipc_os_priv.rx_sem);;
        stop
        """,
    )
    W(
        "3_4_66",
        "ipcsShmHardirqInstance Zephyr",
        """
        start
        if (state!=DISABLED?) then (yes)
          :irq_disable if rx_irq configured;;
          :HwDisable; HwClear;;
          if (msg_received == MSG_NOT_RECEIVED?) then (yes)
            :msg_received = MSG_IS_RECEIVED;;
          endif
          :k_sem_give(\&ipc_os_priv.rx_sem);;
        endif
        stop
        """,
    )
    W(
        "3_4_67",
        "ipcsOsMemMap Zephyr",
        """
        start
        if (CONFIG_MMU defined?) then (yes)
          :z_phys_map local + remote;;
        else (no)
          :virtual = physical;;
        endif
        stop
        """,
    )
    W(
        "3_4_68",
        "ipcsOsMemUnmap Zephyr",
        """
        start
        if (CONFIG_MMU defined?) then (yes)
          :z_phys_unmap(local); z_phys_unmap(remote);;
        endif
        stop
        """,
    )
    W(
        "3_4_69",
        "ipcsOsInit Zephyr",
        """
        start
        :Build ipc_irqs table via DT preprocessor (SAF85 S32ZE S32K3XX blocks);;
        :err = IPC_SHM_E_OK;;
        if (rx_cb guard or DT irq index violation from ipc-os-zephyr.c init checks?) then (yes)
          :err = -IPC_SHM_E_INVAL;;
        else (no)
          if (cfg->inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
            :ipc_os_priv.id[instance].rx_irq_num = IPC_IRQ_NONE;;
          else (no)
            :ipc_os_priv.id[instance].rx_irq_num = ipc_irqs[cfg->inter_core_rx_irq - IPC_INT_DIFF];;
            if (ipc_soft_thread_is_initialized == IPC_THREAD_IS_INIT?) then (yes)
              :irq_enable((uint32)ipc_os_priv.id[instance].rx_irq_num);;
            else (no)
              :BUILD_ASSERT dynamic interrupts; perform k_sem_init and k_thread_create ipcsShmSoftirq;;
              if (softirq_id == NULL?) then (yes)
                :err = -IPC_SHM_E_NOMEM;;
              else (no)
                :irq_enable((uint32)ipc_os_priv.id[instance].rx_irq_num);;
                :ipc_soft_thread_is_initialized = IPC_THREAD_IS_INIT;;
              endif
            endif
          endif
          if (err == IPC_SHM_E_OK?) then (yes)
            :copy local_shm remote_shm shm_size state rx_cb msg_received;;
            :ipcsOsMemMap(instance);;
          endif
        endif
        :return err;
        stop
        """,
    )
    W(
        "3_4_70",
        "ipcsOsFree Zephyr",
        """
        start
        if (rx_irq!=IPC_IRQ_NONE?) then (yes)
          :irq_disable((uint32)rx_irq);;
        endif
        :HwIrqDisable(instance);;
        :rx_cb=NULL; DISABLED;;
        :ipcsOsMemUnmap(instance);;
        :k_thread_abort(softirq_id); k_sem_reset;;
        :ipc_soft_thread_is_initialized = NOT_INIT;;
        stop
        """,
    )
    W(
        "3_4_71",
        "ipcsOsGetLocalShm Zephyr",
        """
        start
        :return local_shm_virt;;
        stop
        """,
    )
    W(
        "3_4_72",
        "ipcsOsGetRemoteShm Zephyr",
        """
        start
        :return remote_shm_virt;;
        stop
        """,
    )
    W(
        "3_4_73",
        "ipcsOsPollChannels Zephyr",
        """
        start
        :err=-IPC_SHM_E_NOTSUP;;
        if (rx_irq == IPC_IRQ_NONE?) then (yes)
          if (rx_cb != NULL?) then (yes)
            :err = rx_cb(instance,IPC_SOFTIRQ_BUDGET);;
          else (no)
            :err=-IPC_SHM_E_INVAL;;
          endif
        endif
        :return err;
        stop
        """,
    )

    # --- ThreadX (md_sdd_0519 §4.4 refs tx_3_4_*.svg) ---
    W(
        "tx_3_4_56",
        "ipcsOsInit ThreadX",
        """
        start
        :err = -IPC_SHM_E_INVAL;
        if ((rx_cb != NULL) && (cfg != NULL)?) then (yes)
          :ipc_os_priv.id[instance].localShm = cfg->local_shm_addr\nipc_os_priv.id[instance].remoteShm = cfg->remote_shm_addr\nipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED\nipc_os_priv.id[instance].rxCallback = rx_cb\nipc_os_priv.id[instance].rxIrqNum = cfg->inter_core_rx_irq;;
          if ((taskIsInitialized != 0) || (rxIrqNum == IPC_IRQ_NONE)?) then (yes)
            :err = IPC_SHM_E_OK;;
          else (no)
            :osStatus = tx_event_flags_create(&softIrqEvents);;
            if (osStatus != TX_SUCCESS?) then (yes)
              :err = -IPC_SHM_E_NOMEM;;
            else (no)
              :osStatus = tx_thread_create(softIrqHandle, ipcsShmSoftIrq);;
              if (osStatus != TX_SUCCESS?) then (yes)
                :err = -IPC_SHM_E_NOMEM;;
              else (no)
                :taskIsInitialized = 1;;
                :err = IPC_SHM_E_OK;;
              endif
            endif
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )
    W(
        "tx_3_4_57",
        "ipcsOsFree ThreadX",
        """
        start
        :tx_event_flags_set(QUIT_REQ); tx_event_flags_get(QUIT_ACK);;
        :ipcsHwIrqDisable(instance);;
        :rxCallback = NULL; state = DISABLED;;
        if (rxIrqNum != IPC_IRQ_NONE?) then (yes)
          if (taskIsInitialized != 0?) then (yes)
            :taskIsInitialized = 0;;
            :tx_thread_terminate; tx_thread_delete; tx_event_flags_delete;;
          endif
        endif
        stop
        """,
    )
    W(
        "tx_3_4_58",
        "ipcsShmSoftIrq ThreadX",
        """
        start
        while (1?)
          :tx_event_flags_get(DATA | QUIT_REQ);;
          if (DATA flag?) then (yes)
            while (i < IPC_SHM_MAX_INSTANCES?)
              if (instance enabled and rxIrqNum != IPC_IRQ_NONE?) then (yes)
                repeat
                  :work = rxCallback(i, IPC_SOFTIRQ_BUDGET);;
                  :tx_thread_relinquish;;
                repeat while (work >= IPC_SOFTIRQ_BUDGET?) is (yes)
              endif
              :i++;
            endwhile (no)
            :ipcsHwIrqEnable all enabled instances;;
          endif
          if (QUIT_REQ?) then (yes)
            :tx_event_flags_set(QUIT_ACK); break;
          endif
        endwhile (no)
        stop
        """,
    )
    W(
        "tx_3_4_59",
        "ipcsShmHardIrq ThreadX",
        """
        start
        :taskCriticalStatus = tx_interrupt_control(TX_INT_DISABLE);;
        while (i < IPC_SHM_MAX_INSTANCES?)
          if (state != DISABLED?) then (yes)
            :ipcsHwIrqDisable(i); ipcsHwIrqClear(i);;
          endif
          :i++;
        endwhile (no)
        :tx_event_flags_set(DATA_EVENT_FLAG);;
        :tx_interrupt_control(restore);;
        stop
        """,
    )
    W(
        "tx_3_4_61",
        "ipcsOsGetLocalShm ThreadX",
        """
        start
        :return ipc_os_priv.id[instance].localShm;
        stop
        """,
    )
    W(
        "tx_3_4_62",
        "ipcsOsGetRemoteShm ThreadX",
        """
        start
        :return ipc_os_priv.id[instance].remoteShm;
        stop
        """,
    )
    W(
        "tx_3_4_63",
        "ipcsOsPollChannels ThreadX",
        """
        start
        :err = IPC_SHM_E_OK;
        if (rxIrqNum == IPC_IRQ_NONE?) then (yes)
          if (rxCallback != NULL?) then (yes)
            :err = rxCallback(instance, IPC_SOFTIRQ_BUDGET);;
          else (no)
          endif
        else (no)
          :err = -IPC_SHM_E_INVAL;
        endif
        :return err;
        stop
        """,
    )
