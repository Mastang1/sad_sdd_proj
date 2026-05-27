# -*- coding: utf-8 -*-
"""
Cross-unit scenario sequence diagrams for §4.7 (Core logic), §5.7 (RTOS), §6.7 (Linux).

Render: python format_docx_py/render_scenario_sequences.py
"""

from __future__ import annotations

from scenario_seq_common import (
    COLOR_CORE,
    COLOR_HAL,
    COLOR_LINUX_KO,
    COLOR_LINUX_USER,
    COLOR_OSAL_LINUX,
    COLOR_OSAL_RTOS,
    COLOR_QUEUE,
    COLOR_REMOTE,
    SEQ_HEADER,
    participant,
)

P = participant

CORE_DIAGRAMS: dict[str, str] = {
    "core_seq_init": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("Drv_Ipcs_Hal_Cmp", "ipcs-hw.h", "HAL", COLOR_HAL)
    + "\n"
    + P("Drv_Ipcs_Osal_Cmp", "ipc-os.h", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> CORE : ipcsShmInitInstance(instance, cfg)
CORE -> HAL : ipcsHwInit(instance, cfg)
activate HAL
note right of HAL
  Variant HAL: map HW resources,
  validate IRQ/core indices,
  disable notify until channels ready
end note
HAL --> CORE : IPC_SHM_E_OK
deactivate HAL
CORE -> OSAL : ipcsOsInit(instance, cfg, ipcsShmRx)
activate OSAL
note right of OSAL
  Variant OSAL: save SHM addresses,
  register deferred Rx dispatch
end note
OSAL --> CORE : IPC_SHM_E_OK
deactivate OSAL
CORE -> CORE : ipcsShmInitChannels(instance, cfg)
CORE -> QUEUE : ipcsQueueInit per channel
activate QUEUE
QUEUE --> CORE : IPC_SHM_E_OK
deactivate QUEUE
CORE -> HAL : ipcsHwIrqClear(instance)
activate HAL
CORE -> HAL : ipcsHwIrqEnable(instance)
HAL --> CORE : IPC_SHM_E_OK
deactivate HAL
CORE -> CORE : state = READY; flush cache
CORE --> APP : IPC_SHM_E_OK
deactivate CORE
deactivate APP
@enduml
""",
    "core_seq_tx_managed": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + "\n"
    + P("Drv_Ipcs_Hal_Cmp", "ipcs-hw.h", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmAcquireBuf(instance, chan, size)
activate CORE
CORE -> QUEUE : ipcsQueuePop(local free BD ring)
activate QUEUE
QUEUE --> CORE : BD / buffer address
deactivate QUEUE
CORE --> APP : local buffer pointer
APP -> APP : fill payload
APP -> CORE : ipcsShmTx(instance, chan, buf, size)
CORE -> CORE : validate channel / build BD
CORE -> QUEUE : ipcsQueuePush(remote BD ring, BD)
activate QUEUE
QUEUE --> CORE : IPC_SHM_E_OK
deactivate QUEUE
CORE -> HAL : ipcsHwIrqNotify(instance)
activate HAL
note right of HAL
  Variant HAL: signal remote core
end note
HAL -> REMOTE : inter-core notification
activate REMOTE
deactivate REMOTE
deactivate HAL
CORE --> APP : IPC_SHM_E_OK
deactivate CORE
deactivate APP
@enduml
""",
    "core_seq_rx_managed": SEQ_HEADER
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("Drv_Ipcs_Hal_Cmp", "ipcs-hw.h", "HAL", COLOR_HAL)
    + "\n"
    + P("Drv_Ipcs_Osal_Cmp", "ipc-os.h", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + "\n"
    + P("Application", "rx_cb", "APP", "#FAF0E0")
    + """

autonumber
activate REMOTE
REMOTE -> HAL : inter-core notification
activate HAL
HAL -> OSAL : deferred Rx entry (variant)
activate OSAL
note right of OSAL
  Variant OSAL: IRQ disable/clear,
  schedule softirq or poll hook
end note
OSAL -> CORE : ipcsShmRx(instance, budget)
activate CORE
loop work < budget
  CORE -> CORE : ipcsChannelRx(instance, chan, budget)
  CORE -> QUEUE : ipcsQueuePop(remote BD ring)
  activate QUEUE
  QUEUE --> CORE : BD
  deactivate QUEUE
  CORE -> APP : rx_cb(instance, chan, buf, size)
  activate APP
  APP -> CORE : ipcsShmReleaseBuf(instance, chan, buf)
  APP --> CORE : IPC_SHM_E_OK
  deactivate APP
end
CORE --> OSAL : work done
deactivate CORE
OSAL -> HAL : re-enable notification (variant)
activate HAL
deactivate HAL
deactivate OSAL
deactivate HAL
deactivate REMOTE
@enduml
""",
    "core_seq_unmanaged": SEQ_HEADER
    + P("Application (local)", "caller", "APP_L", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE_L", COLOR_CORE)
    + "\n"
    + P("Drv_Ipcs_Hal_Cmp", "ipcs-hw.h", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "peer instance", "CORE_R", COLOR_CORE)
    + """

autonumber
activate APP_L
APP_L -> CORE_L : ipcsShmUnmanagedAcquire(instance, chan)
activate CORE_L
CORE_L --> APP_L : local unmanaged memory
APP_L -> CORE_L : write payload to local mem
APP_L -> CORE_L : ipcsShmUnmanagedTx(instance, chan)
CORE_L -> CORE_L : increment tx_count
CORE_L -> HAL : ipcsHwIrqNotify(instance)
activate HAL
HAL -> REMOTE : inter-core notification
activate REMOTE
REMOTE -> CORE_R : OSAL/HAL Rx path
activate CORE_R
CORE_R -> CORE_R : ipcsChannelRx: compare tx_count
note right of CORE_R
  If remote tx_count changed,
  invoke rx_cb with remote mem
end note
CORE_R --> REMOTE : rx_cb done
deactivate CORE_R
deactivate REMOTE
deactivate HAL
deactivate CORE_L
deactivate APP_L
@enduml
""",
    "core_seq_irq_poll": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("Drv_Ipcs_Osal_Cmp", "ipc-os.h", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("Drv_Ipcs_Hal_Cmp", "ipcs-hw.h", "HAL", COLOR_HAL)
    + """

autonumber
alt inter_core_rx_irq != IPC_IRQ_NONE
  activate HAL
  HAL -> OSAL : hardware notification
  activate OSAL
  OSAL -> CORE : ipcsShmRx(instance, budget)
  activate CORE
  loop fair channel dispatch
    CORE -> CORE : ipcsChannelRx per channel
  end
  CORE --> OSAL : channels serviced
  deactivate CORE
  deactivate OSAL
  deactivate HAL
else polling (IPC_IRQ_NONE)
  activate APP
  APP -> CORE : ipcsShmPollChannels(instance)
  activate CORE
  CORE -> OSAL : ipcsOsPollChannels(instance)
  activate OSAL
  note right of OSAL
    Variant OSAL: invoke registered
    rx_cb with IPC_SOFTIRQ_BUDGET
  end note
  OSAL -> CORE : ipcsShmRx(instance, budget)
  deactivate OSAL
  CORE --> APP : work done / channels serviced
  deactivate CORE
  deactivate APP
end
@enduml
""",
}

RTOS_DIAGRAMS: dict[str, str] = {
    "rtos_seq_init": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_HAL_MCU", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("SWU_IPCS_OSAL_THREADX", "ipc-os-threadx.c", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> CORE : ipcsShmInitInstance(instance, cfg)
CORE -> HAL : ipcsHwInit(instance, cfg)
activate HAL
note right of HAL
  Map MSCM, validate core/IRQ indices,
  ipcsHwIrqDisable until channels ready
end note
HAL --> CORE : IPC_SHM_E_OK
deactivate HAL
CORE -> OSAL : ipcsOsInit(instance, cfg, ipcsShmRx)
activate OSAL
note right of OSAL
  Save shm addresses; create event flags
  and softirq thread (if Rx IRQ enabled)
end note
OSAL --> CORE : IPC_SHM_E_OK
deactivate OSAL
CORE -> CORE : ipcsShmInitChannels(instance, cfg)
CORE -> QUEUE : ipcsQueueInit per channel
activate QUEUE
QUEUE --> CORE : ok
deactivate QUEUE
CORE -> HAL : ipcsHwIrqClear(instance)
activate HAL
CORE -> HAL : ipcsHwIrqEnable(instance)
HAL --> CORE : ok
deactivate HAL
CORE -> CORE : state = READY; flush cache
CORE --> APP : IPC_SHM_E_OK
deactivate CORE
deactivate APP
@enduml
""",
    "rtos_seq_tx_managed": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + "\n"
    + P("SWU_IPCS_HAL_MCU", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmAcquireBuf(instance, chan)
activate CORE
CORE --> APP : local buffer pointer
APP -> APP : fill payload
APP -> CORE : ipcsShmTx(instance, chan, buf, size)
CORE -> CORE : validate channel / push BD ring
CORE -> QUEUE : ipcsQueuePush(remote ring, BD)
activate QUEUE
QUEUE --> CORE : IPC_SHM_E_OK
deactivate QUEUE
CORE -> HAL : ipcsHwIrqNotify(instance)
activate HAL
note right of HAL
  writel MSCM IRCPnIGRn to remote core
end note
HAL -> REMOTE : inter-core interrupt
activate REMOTE
deactivate REMOTE
deactivate HAL
CORE --> APP : IPC_SHM_E_OK
deactivate CORE
deactivate APP
@enduml
""",
    "rtos_seq_rx_managed": SEQ_HEADER
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_HAL_MCU", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("SWU_IPCS_OSAL_THREADX", "ipc-os-threadx.c", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_CORE_QUEUE", "ipc-queue.c", "QUEUE", COLOR_QUEUE)
    + "\n"
    + P("Application", "rx_cb", "APP", "#FAF0E0")
    + """

autonumber
activate REMOTE
REMOTE -> HAL : Rx IRQ (MSCM)
activate HAL
HAL -> OSAL : ipcsShmHardIrq()
activate OSAL
OSAL -> HAL : ipcsHwIrqDisable(i) / ipcsHwIrqClear(i)
deactivate HAL
OSAL -> OSAL : tx_event_flags_set(DATA_EVENT_FLAG)
OSAL -> OSAL : ipcsShmSoftIrq thread wakes
OSAL -> CORE : rxCallback(instance, budget) / ipcsShmRx
activate CORE
loop until work < budget
  CORE -> QUEUE : ipcsQueuePop / channel dispatch
  activate QUEUE
  CORE -> APP : application rx_cb(chan, buf)
  activate APP
  APP --> CORE : handled count
  deactivate APP
  deactivate QUEUE
end
deactivate CORE
OSAL -> HAL : ipcsHwIrqEnable(i)
activate HAL
deactivate HAL
deactivate OSAL
deactivate REMOTE
@enduml
""",
    "rtos_seq_unmanaged": SEQ_HEADER
    + P("Application (local)", "caller", "APP_L", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE_L", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_HAL_MCU", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "peer instance", "CORE_R", COLOR_CORE)
    + """

autonumber
activate APP_L
APP_L -> CORE_L : ipcsShmUnmanagedAcquire(instance, chan)
activate CORE_L
CORE_L --> APP_L : local unmanaged memory
APP_L -> CORE_L : write payload to local mem
APP_L -> CORE_L : ipcsShmUnmanagedTx(instance, chan)
CORE_L -> CORE_L : increment tx_count
CORE_L -> HAL : ipcsHwIrqNotify(instance)
activate HAL
HAL -> REMOTE : inter-core interrupt
activate REMOTE
REMOTE -> CORE_R : ISR / softirq path
activate CORE_R
CORE_R -> CORE_R : compare tx_count, invoke rx_cb
CORE_R --> REMOTE : expose remote mem to app
deactivate CORE_R
deactivate REMOTE
deactivate HAL
deactivate CORE_L
deactivate APP_L
@enduml
""",
    "rtos_seq_irq_poll": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "ipc-shm.c", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_OSAL_THREADX", "ipc-os-threadx.c", "OSAL", COLOR_OSAL_RTOS)
    + "\n"
    + P("SWU_IPCS_HAL_MCU", "ipc-hw.c", "HAL", COLOR_HAL)
    + """

autonumber
alt inter_core_rx_irq != IPC_IRQ_NONE
  activate HAL
  HAL -> OSAL : hardware IRQ
  activate OSAL
  OSAL -> CORE : deferred ipcsShmRx via softirq thread
  activate CORE
  CORE --> OSAL : channels serviced
  deactivate CORE
  deactivate OSAL
  deactivate HAL
else polling (IPC_IRQ_NONE)
  activate APP
  APP -> CORE : ipcsShmPollChannels(instance)
  activate CORE
  CORE -> OSAL : ipcsOsPollChannels(instance)
  activate OSAL
  note right of OSAL
    Directly calls registered rx_cb
    with IPC_SOFTIRQ_BUDGET
  end note
  OSAL -> CORE : ipcsShmRx(instance, budget)
  deactivate OSAL
  CORE --> APP : work done / channels serviced
  deactivate CORE
  deactivate APP
end
@enduml
""",
}

LINUX_DIAGRAMS: dict[str, str] = {
    "linux_seq_uio_init": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_UIO", "os_uio/ipc-os.c", "UIO_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_LINUX_UIO_KO", "ipc-uio.c", "UIO_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> UIO_USR : ipcsOsInit(instance, cfg, ipcsShmRx)
activate UIO_USR
UIO_USR -> UIO_USR : finit_module(ipc-shm-uio.ko)
UIO_USR -> UIO_USR : open /dev/ipc-cdev-uio, /dev/mem
UIO_USR -> UIO_USR : mmap local and remote SHM
UIO_USR -> UIO_KO : write(IPC_UIO_CDEV_DATA_TYPE)
activate UIO_KO
UIO_KO -> UIO_KO : ipcsUioInit(data)
UIO_KO -> HAL : ipcsHwInit(instance, cfg)
activate HAL
HAL --> UIO_KO : 0
deactivate HAL
UIO_KO -> UIO_KO : uio_register_device / request IRQ
deactivate UIO_KO
UIO_USR -> UIO_USR : get_uio_dev_name; open /dev/uioX
UIO_USR -> UIO_USR : pthread_create(ipcsShmSoftirq)
deactivate UIO_USR
UIO_USR --> CORE : 0
CORE -> CORE : ipcsShmInitChannels ...
CORE --> APP : success
deactivate CORE
deactivate APP
@enduml
""",
    "linux_seq_cdev_init": SEQ_HEADER
    + P("Application", "caller", "APP", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_CDEV", "os_cdev/ipc-os.c", "CDEV_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_LINUX_CDEV_KO", "ipc-cdev.c", "CDEV_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + """

autonumber
activate APP
APP -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> CDEV_USR : ipcsOsInit(instance, cfg, ipcsShmRx)
activate CDEV_USR
CDEV_USR -> CDEV_USR : finit_module; open /dev/ipc-shm-cdev
CDEV_USR -> CDEV_USR : mmap local and remote SHM
CDEV_USR -> CDEV_USR : pthread_create(global ipcsShmSoftirq)
CDEV_USR -> CDEV_KO : ioctl(SET_INSTANCE)
CDEV_USR -> CDEV_KO : ioctl(INIT_INSTANCE, cfg)
activate CDEV_KO
CDEV_KO -> CDEV_KO : ipcsCdevOsInit(instance, cfg)
CDEV_KO -> HAL : ipcsHwInit(instance, cfg)
activate HAL
HAL --> CDEV_KO : 0
deactivate HAL
CDEV_KO -> CDEV_KO : request_irq(ipcsShmHardirq)
deactivate CDEV_KO
deactivate CDEV_USR
CDEV_USR --> CORE : 0
CORE --> APP : success
deactivate CORE
deactivate APP
@enduml
""",
    "linux_seq_kernel_init": SEQ_HEADER
    + P("Kernel module", "caller", "MOD", "#FAF0E0")
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "linked in kernel", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_KERN", "ipc-os.c", "OSAL", COLOR_OSAL_LINUX)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + """

autonumber
activate MOD
MOD -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> OSAL : ipcsOsInit(instance, cfg, ipcsShmRx)
activate OSAL
OSAL -> OSAL : request_mem_region + ioremap SHM
OSAL -> HAL : ipcsHwInit(instance, cfg)
activate HAL
HAL --> OSAL : 0
deactivate HAL
OSAL -> OSAL : of_irq_get; request_irq(ipcsShmHardirq)
note right of OSAL
  tasklet ipcsShmSoftirq scheduled from hardirq
end note
deactivate OSAL
OSAL --> CORE : 0
CORE --> MOD : success
deactivate CORE
deactivate MOD
@enduml
""",
    "linux_seq_uio_tx_notify": SEQ_HEADER
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_UIO", "os_uio/ipc-os.c", "UIO_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_LINUX_UIO_KO", "ipc-uio.c", "UIO_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + """

autonumber
activate CORE
CORE -> UIO_USR : ipcsHwIrqNotify(instance) from ipcsShmTx
activate UIO_USR
UIO_USR -> UIO_USR : ipcsSendUioCmd(uio_fd, TRIGGER)
UIO_USR -> UIO_KO : write / UIO irqcontrol
activate UIO_KO
UIO_KO -> HAL : ipcsHwIrqNotify(instance)
activate HAL
HAL -> REMOTE : MSCM directed interrupt
activate REMOTE
deactivate REMOTE
deactivate HAL
deactivate UIO_KO
deactivate UIO_USR
deactivate CORE
@enduml
""",
    "linux_seq_cdev_tx_notify": SEQ_HEADER
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_CDEV", "os_cdev/ipc-os.c", "CDEV_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_LINUX_CDEV_KO", "ipc-cdev.c", "CDEV_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + """

autonumber
activate CORE
CORE -> CDEV_USR : ipcsHwIrqNotify(instance)
activate CDEV_USR
CDEV_USR -> CDEV_KO : ioctl(TRIGGER_TX_IRQ, instance)
activate CDEV_KO
CDEV_KO -> HAL : ipcsHwIrqNotify(instance)
activate HAL
HAL -> REMOTE : MSCM directed interrupt
activate REMOTE
deactivate REMOTE
deactivate HAL
deactivate CDEV_KO
deactivate CDEV_USR
deactivate CORE
@enduml
""",
    "linux_seq_uio_rx": SEQ_HEADER
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("SWU_IPCS_LINUX_UIO_KO", "ipc-uio.c", "UIO_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_UIO", "os_uio/ipc-os.c", "UIO_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + """

autonumber
activate REMOTE
REMOTE -> HAL : Rx IRQ
activate HAL
HAL -> UIO_KO : ipcsShmUioHandler
activate UIO_KO
UIO_KO -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
deactivate HAL
UIO_KO --> UIO_USR : UIO event (read unblocks)
deactivate UIO_KO
activate UIO_USR
UIO_USR -> UIO_USR : pthread: read(uio_fd)
UIO_USR -> CORE : rx_cb(instance, budget) / ipcsShmRx
activate CORE
loop work >= budget
  CORE -> CORE : drain channels
end
deactivate CORE
UIO_USR -> UIO_USR : ipcsHwIrqEnable via UIO write
deactivate UIO_USR
deactivate REMOTE
@enduml
""",
    "linux_seq_cdev_rx": SEQ_HEADER
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("SWU_IPCS_LINUX_CDEV_KO", "ipc-cdev.c", "CDEV_KO", COLOR_LINUX_KO)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_CDEV", "os_cdev/ipc-os.c", "CDEV_USR", COLOR_LINUX_USER)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "user lib", "CORE", COLOR_CORE)
    + """

autonumber
activate REMOTE
REMOTE -> HAL : Rx IRQ
activate HAL
HAL -> CDEV_KO : ipcsShmHardirq
activate CDEV_KO
CDEV_KO -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
deactivate HAL
CDEV_KO -> CDEV_KO : wake_up_interruptible(wait_queue)
deactivate CDEV_KO
activate CDEV_USR
CDEV_USR -> CDEV_KO : read(/dev/ipc-shm-cdev) returns
activate CDEV_KO
deactivate CDEV_KO
CDEV_USR -> CORE : rx_cb(i, budget) per instance
activate CORE
deactivate CORE
CDEV_USR -> CDEV_USR : ipcsHwIrqEnable via ioctl
deactivate CDEV_USR
deactivate REMOTE
@enduml
""",
    "linux_seq_kernel_rx": SEQ_HEADER
    + P("Remote core", "peer", "REMOTE", COLOR_REMOTE)
    + "\n"
    + P("SWU_IPCS_HAL_LINUX", "ipc-hw.c", "HAL", COLOR_HAL)
    + "\n"
    + P("SWU_IPCS_LINUX_OS_KERN", "ipc-os.c", "OSAL", COLOR_OSAL_LINUX)
    + "\n"
    + P("SWU_IPCS_CORE_SHM", "kernel", "CORE", COLOR_CORE)
    + """

autonumber
activate REMOTE
REMOTE -> HAL : Rx IRQ
activate HAL
HAL -> OSAL : ipcsShmHardirq
activate OSAL
OSAL -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
deactivate HAL
OSAL -> OSAL : tasklet_schedule(ipcsShmSoftirq)
OSAL -> CORE : priv.rx_cb(i, budget)
activate CORE
loop work >= budget
  CORE -> CORE : ipcsShmRx drain
  OSAL -> OSAL : tasklet_schedule (yield)
end
deactivate CORE
OSAL -> HAL : ipcsHwIrqEnable(i)
activate HAL
deactivate HAL
deactivate OSAL
deactivate REMOTE
@enduml
""",
}

ALL_DIAGRAMS = {**CORE_DIAGRAMS, **RTOS_DIAGRAMS, **LINUX_DIAGRAMS}
