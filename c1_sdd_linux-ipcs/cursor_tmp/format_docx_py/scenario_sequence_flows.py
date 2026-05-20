# -*- coding: utf-8 -*-
"""
Cross-unit scenario sequence diagrams for §5.7 (RTOS) and §6.7 (Linux).

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
APP -> CORE : ipcsShmInit(cfg)
activate CORE
CORE -> CORE : ipcsShmInitInstance(instance, cfg)
CORE -> HAL : ipcsHwInit(instance, cfg)
note right of HAL
  Map MSCM, validate core/IRQ indices,
  ipcsHwIrqDisable until channels ready
end note
HAL --> CORE : IPC_SHM_E_OK
CORE -> OSAL : ipcsOsInit(instance, cfg, ipcsShmRx)
note right of OSAL
  Save shm addresses; create event flags
  and softirq thread (if Rx IRQ enabled)
end note
OSAL --> CORE : IPC_SHM_E_OK
CORE -> CORE : ipcsShmInitChannels(instance, cfg)
CORE -> QUEUE : ipcsQueueInit per channel
QUEUE --> CORE : ok
CORE -> HAL : ipcsHwIrqClear(instance)
CORE -> HAL : ipcsHwIrqEnable(instance)
CORE -> CORE : state = READY; flush cache
CORE --> APP : IPC_SHM_E_OK
deactivate CORE
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
APP -> CORE : ipcsShmAcquireBuf(instance, chan)
CORE --> APP : local buffer pointer
APP -> APP : fill payload
APP -> CORE : ipcsShmTx(instance, chan, buf, size)
activate CORE
CORE -> CORE : validate channel / push BD ring
CORE -> QUEUE : ipcsQueuePush(remote ring, BD)
QUEUE --> CORE : IPC_SHM_E_OK
CORE -> HAL : ipcsHwIrqNotify(instance)
note right of HAL
  writel MSCM IRCPnIGRn to remote core
end note
HAL -> REMOTE : inter-core interrupt
deactivate CORE
CORE --> APP : IPC_SHM_E_OK
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
REMOTE -> HAL : Rx IRQ (MSCM)
activate HAL
HAL -> OSAL : ipcsShmHardIrq()
activate OSAL
OSAL -> HAL : ipcsHwIrqDisable(i) / ipcsHwIrqClear(i)
OSAL -> OSAL : tx_event_flags_set(DATA_EVENT_FLAG)
deactivate HAL
OSAL -> OSAL : ipcsShmSoftIrq thread wakes
OSAL -> CORE : rxCallback(instance, budget) / ipcsShmRx
activate CORE
loop until work < budget
  CORE -> QUEUE : ipcsQueuePop / channel dispatch
  CORE -> APP : application rx_cb(chan, buf)
  APP --> CORE : handled count
end
deactivate CORE
OSAL -> HAL : ipcsHwIrqEnable(i)
deactivate OSAL
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
APP_L -> CORE_L : ipcsShmUnmanagedAcquire(instance, chan)
CORE_L --> APP_L : local unmanaged memory
APP_L -> CORE_L : write payload to local mem
APP_L -> CORE_L : ipcsShmUnmanagedTx(instance, chan)
activate CORE_L
CORE_L -> CORE_L : increment tx_count
CORE_L -> HAL : ipcsHwIrqNotify(instance)
HAL -> REMOTE : inter-core interrupt
deactivate CORE_L
REMOTE -> CORE_R : ISR / softirq path
CORE_R -> CORE_R : compare tx_count, invoke rx_cb
CORE_R --> REMOTE : expose remote mem to app
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
  HAL -> OSAL : hardware IRQ
  OSAL -> CORE : deferred ipcsShmRx via softirq thread
else polling (IPC_IRQ_NONE)
  APP -> CORE : ipcsShmPollChannels(instance)
  CORE -> OSAL : ipcsOsPollChannels(instance)
  note right of OSAL
    Directly calls registered rx_cb
    with IPC_SOFTIRQ_BUDGET
  end note
  OSAL -> CORE : ipcsShmRx(instance, budget)
end
CORE --> APP : work done / channels serviced
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
APP -> CORE : ipcsShmInit(cfg)
CORE -> UIO_USR : ipcsOsInit(instance, cfg, ipcsShmRx)
activate UIO_USR
UIO_USR -> UIO_USR : finit_module(ipc-shm-uio.ko)
UIO_USR -> UIO_USR : open /dev/ipc-cdev-uio, /dev/mem
UIO_USR -> UIO_USR : mmap local and remote SHM
UIO_USR -> UIO_KO : write(IPC_UIO_CDEV_DATA_TYPE)
activate UIO_KO
UIO_KO -> UIO_KO : ipcsUioInit(data)
UIO_KO -> HAL : ipcsHwInit(instance, cfg)
HAL --> UIO_KO : 0
UIO_KO -> UIO_KO : uio_register_device / request IRQ
deactivate UIO_KO
UIO_USR -> UIO_USR : get_uio_dev_name; open /dev/uioX
UIO_USR -> UIO_USR : pthread_create(ipcsShmSoftirq)
deactivate UIO_USR
UIO_USR --> CORE : 0
CORE -> CORE : ipcsShmInitChannels ...
CORE --> APP : success
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
APP -> CORE : ipcsShmInit(cfg)
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
HAL --> CDEV_KO : 0
CDEV_KO -> CDEV_KO : request_irq(ipcsShmHardirq)
deactivate CDEV_KO
deactivate CDEV_USR
CDEV_USR --> CORE : 0
CORE --> APP : success
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
MOD -> CORE : ipcsShmInit(cfg)
CORE -> OSAL : ipcsOsInit(instance, cfg, ipcsShmRx)
activate OSAL
OSAL -> OSAL : request_mem_region + ioremap SHM
OSAL -> OSAL : of_irq_get; request_irq(ipcsShmHardirq)
note right of OSAL
  tasklet ipcsShmSoftirq scheduled from hardirq
end note
deactivate OSAL
OSAL --> CORE : 0
CORE --> MOD : success
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
CORE -> UIO_USR : ipcsHwIrqNotify(instance) from ipcsShmTx
UIO_USR -> UIO_USR : ipcsSendUioCmd(uio_fd, TRIGGER)
UIO_USR -> UIO_KO : write / UIO irqcontrol
UIO_KO -> HAL : ipcsHwIrqNotify(instance)
HAL -> REMOTE : MSCM directed interrupt
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
CORE -> CDEV_USR : ipcsHwIrqNotify(instance)
CDEV_USR -> CDEV_KO : ioctl(TRIGGER_TX_IRQ, instance)
CDEV_KO -> HAL : ipcsHwIrqNotify(instance)
HAL -> REMOTE : MSCM directed interrupt
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
REMOTE -> HAL : Rx IRQ
HAL -> UIO_KO : ipcsShmUioHandler
activate UIO_KO
UIO_KO -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
UIO_KO --> UIO_USR : UIO event (read unblocks)
deactivate UIO_KO
UIO_USR -> UIO_USR : pthread: read(uio_fd)
UIO_USR -> CORE : rx_cb(instance, budget) / ipcsShmRx
loop work >= budget
  CORE -> CORE : drain channels
end
UIO_USR -> UIO_USR : ipcsHwIrqEnable via UIO write
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
REMOTE -> HAL : Rx IRQ
HAL -> CDEV_KO : ipcsShmHardirq
activate CDEV_KO
CDEV_KO -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
CDEV_KO -> CDEV_KO : wake_up_interruptible(wait_queue)
deactivate CDEV_KO
CDEV_USR -> CDEV_KO : read(/dev/ipc-shm-cdev) returns
CDEV_USR -> CORE : rx_cb(i, budget) per instance
CDEV_USR -> CDEV_USR : ipcsHwIrqEnable via ioctl
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
REMOTE -> HAL : Rx IRQ
HAL -> OSAL : ipcsShmHardirq
activate OSAL
OSAL -> HAL : ipcsHwIrqDisable / ipcsHwIrqClear
OSAL -> OSAL : tasklet_schedule(ipcsShmSoftirq)
deactivate OSAL
OSAL -> CORE : priv.rx_cb(i, budget)
loop work >= budget
  CORE -> CORE : ipcsShmRx drain
  OSAL -> OSAL : tasklet_schedule (yield)
end
OSAL -> HAL : ipcsHwIrqEnable(i)
@enduml
""",
}

ALL_DIAGRAMS = {**RTOS_DIAGRAMS, **LINUX_DIAGRAMS}
