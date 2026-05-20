# -*- coding: utf-8 -*-
"""Emit all flow_umls/*.puml aligned to IPCS_49 sources (82 diagrams).

After editing, regenerate SVGs:

    python scripts/render_flow_svgs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
from workspace_paths import (
    WORKSPACE_ROOT,
    CURSOR_TMP,
    FINAL_SDD_DOCX,
    MD_SDD_0519,
    IPCS_SDD_MD,
    FLOW_SVGS,
    FLOW_UMLS,
    FILES_32_SVGS,
    FILES_32_UMLS,
    MERMAID_SVGS,
    MEDIA_DIR,
    DOCX_RASTER,
    FORMAT_DOCX_PY,
    SCRIPTS,
    VALIDATE_REPORT,
    PANDOC_REFERENCE,
    PANDOC_MD0519,
    BODY_MD0519,
    PANDOC_FOR_WORD,
    BODY_GENERATED,
    PLANTUML_JAR,
    pandoc_resource_path_str,
    plantuml_jar_candidates,
    rel_to_workspace,
)

OUT = FLOW_UMLS
import textwrap
from pathlib import Path

from ipc_flow_remainder import add_flows_remainder



def H(title: str) -> str:
    return textwrap.dedent(
        f"""\
        @startuml
        !pragma layout smetana
        skinparam conditionStyle insideDiamond
        skinparam linetype ortho
        title {title}
        """
    ).rstrip()


def W(slug: str, title: str, body: str) -> None:
    p = OUT / f"{slug}.puml"
    b = textwrap.dedent(body).strip().replace("\\&", "&")
    p.write_text(H(title) + "\n" + b + "\n@enduml\n", encoding="utf-8")


def emit() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # --- 3.3 ipcs-shm.c public API ---
    W(
        "3_3_1",
        "ipcsShmInit",
        """
        start
        :uint8 i = 0; sint32 err = -IPC_SHM_E_INVAL;
        if (cfg != NULL?) then (yes)
          if ((cfg->num_instances > IPC_SHM_MAX_INSTANCES) || (cfg->num_instances == 0u)?) then (yes)
            :err = -IPC_SHM_E_INVAL;
          else (no)
            while (i < cfg->num_instances?)
              :err = ipcsShmInitInstance(i, \&cfg->shm_cfg[i]);;
              if (err != IPC_SHM_E_OK?) then (yes)
                break
              else (no)
                :i++;;
              endif
            endwhile
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )

    W(
        "3_3_2",
        "ipcsShmFree",
        """
        start
        :uint8 i = 0;
        repeat
          if (ipcsInstanceIsFree(i) == IPC_SHM_INSTANCE_USED?) then (yes)
            :ipc_shm_priv_data[i].global->state = IPC_SHM_STATE_CLEAR;
            :ipc_shm_priv_data[i].global = NULL;
            :ipcsHwFlushCacheLocal(i);
            :ipcsHwIrqDisable(i);
            :ipcsOsFree(i);
            :ipcsHwFree(i);
          else (no)
          endif
          :i++;
        repeat while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
        stop
        """,
    )

    W(
        "3_3_3",
        "ipcsShmAcquireBuf",
        """
        start
        :uintptr_t buf_addr = NULL;
        :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :chan = getManagedChan(instance, chan_id);
          if ((chan == NULL) || (mem_size == 0u) || (ipcsCheckMchanIntegrity(chan) != OK)?) then (yes)
            :buf_addr = NULL;
          else (no)
            :pool_id loop 0..chan->num_pools-1;;
            note right
              for each pool_id: if mem_size > pool->buf_size continue;
              if ipcsQueuePop(pool->bd_queue,\&bd)==0 break
            end note
            if (pool_id == chan->num_pools?) then (yes)
              :buf_addr = NULL;
            else (no)
              :buf_addr = pool->local_pool_addr + bd.buf_id * pool->buf_size;
            endif
          endif
        else (no)
        endif
        :return (void *)buf_addr;
        stop
        """,
    )

    W(
        "3_3_4",
        "ipcsShmReleaseBuf",
        """
        start
        :struct IPCS_MANAGED_CHANNEL_TYPE *chan; struct IPCS_SHM_POOL_TYPE *pool; struct IPCS_SHM_BD_TYPE bd; sint32 err = -IPC_SHM_E_INVAL;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :chan = getManagedChan(instance, chan_id);
          if ((chan != NULL) && (buf != NULL)?) then (yes)
            :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);
            :err = ipcsCheckMchanIntegrity(chan);
            if (err == IPC_SHM_E_OK?) then (yes)
              :bd.pool_id = findPoolForBuf(chan,(uintptr_t)buf,1);;
              if (bd.pool_id != -1?) then (yes)
                :pool = \&chan->pools[bd.pool_id];
                :bd.buf_id = ((uintptr_t)buf - pool->remote_pool_addr) / pool->buf_size;
                :bd.data_size = 0;
                :err = ipcsQueuePush(\&pool->bd_queue,\&bd);
              else (no)
                :err = -IPC_SHM_E_INVAL;
              endif
            else (no)
            endif
          else (no)
          endif
        else (no)
        endif
        :ipcsHwFlushCacheLocal(instance);
        :return err;
        stop
        """,
    )

    W(
        "3_3_5",
        "ipcsShmTx",
        """
        start
        :struct IPCS_MANAGED_CHANNEL_TYPE *chan; struct IPCS_SHM_POOL_TYPE *pool; struct IPCS_SHM_BD_TYPE bd; sint32 err = -IPC_SHM_E_INVAL;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :chan = getManagedChan(instance, chan_id);
          if ((chan != NULL) && (buf != NULL) && (size != 0u)?) then (yes)
            :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);
            :err = ipcsCheckMchanIntegrity(chan);
            if (err == IPC_SHM_E_OK?) then (yes)
              :bd.pool_id = findPoolForBuf(chan,(uintptr_t)buf,0);;
              if (bd.pool_id != -1?) then (yes)
                :pool = \&chan->pools[bd.pool_id];
                :bd.buf_id = ((uintptr_t)buf - pool->local_pool_addr) / pool->buf_size;
                :bd.data_size = size;
                :err = ipcsQueuePush(\&chan->bd_queue,\&bd);
                if (err == IPC_SHM_E_OK?) then (yes)
                  :ipcsHwFlushCacheLocal(instance);
                  :ipcsHwIrqNotify(instance);
                endif
              else (no)
                :err = -IPC_SHM_E_INVAL;
              endif
            else (no)
            endif
          else (no)
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )

    W(
        "3_3_6",
        "ipcsShmUnmanagedAcquire",
        """
        start
        :struct IPCS_UNMANAGED_CHANNEL_TYPE *chan = NULL; uint8_t *umng_mem = NULL;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);;
          :chan = getUnmanagedChan(instance, chan_id);;
          if ((chan != NULL) && (ipcsCheckUchanIntegrity(chan) == OK)?) then (yes)
            :umng_mem = chan->local_mem->mem;
          else (no)
          endif
        else (no)
        endif
        :return (void *)umng_mem;
        stop
        """,
    )

    W(
        "3_3_7",
        "ipcsShmUnmanagedTx",
        """
        start
        :struct IPCS_UNMANAGED_CHANNEL_TYPE *chan = NULL; sint32 err = -IPC_SHM_E_INVAL;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :chan = getUnmanagedChan(instance, chan_id);;
          if (chan != NULL?) then (yes)
            :ipcsHwFlushCacheLocal(instance); ipcsHwFlushCacheRemote(instance);;
            :err = ipcsCheckUchanIntegrity(chan);;
            if (err == IPC_SHM_E_OK?) then (yes)
              :chan->local_mem->tx_count++;;
              :ipcsHwFlushCacheLocal(instance);;
              :ipcsHwIrqNotify(instance);;
            endif
          else (no)
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )

    W(
        "3_3_8",
        "ipcsShmIsRemoteReady",
        """
        start
        :struct IPCS_SHM_GLOBAL_TYPE *remote_global; sint32 err = -IPC_SHM_E_INVAL;
        :ipcsHwFlushCacheRemote(instance);;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :remote_global = (struct IPCS_SHM_GLOBAL_TYPE *)ipcsOsGetRemoteShm(instance);;
          if (remote_global->state != IPC_SHM_STATE_READY?) then (yes)
            :err = -IPC_SHM_E_NOT_READY;
          else (no)
            :err = IPC_SHM_E_OK;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )

    W(
        "3_3_9",
        "ipcsShmPollChannels",
        """
        start
        :struct IPCS_SHM_GLOBAL_TYPE *remote_global; sint32 err = -IPC_SHM_E_INVAL;
        :ipcsHwFlushCacheRemote(instance);;
        if (ipcsInstanceIsFree(instance) == IPC_SHM_INSTANCE_USED?) then (yes)
          :remote_global = (struct IPCS_SHM_GLOBAL_TYPE *)ipcsOsGetRemoteShm(instance);;
          if (remote_global->state != IPC_SHM_STATE_READY?) then (yes)
            :err = -IPC_SHM_E_NOT_READY;
          else (no)
            :err = ipcsOsPollChannels(instance);;
          endif
        else (no)
        endif
        :return err;
        stop
        """,
    )

    add_flows_remainder(W)


if __name__ == "__main__":
    emit()
    n = len(list(OUT.glob("*.puml")))
    print(f"Wrote {n} diagrams to {OUT}")
