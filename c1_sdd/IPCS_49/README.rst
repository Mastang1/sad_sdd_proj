=========================================================
IPCF Shared Memory Driver for Real-Time Operating Systems
=========================================================

:Copyright: 2023 NXP

Overview
========
The IPCF Shared Memory driver for RTOS enables communication over shared memory
with another application running on a different core of the same processor. This
driver is part of the Inter-Platform Communication Framework (IPCF).

The driver is accompanied by a sample application which demonstrates a ping-pong
message communication with another sample application (for more details see
the readme from the sample directory).

HW Platforms
------------
The supported processors are listed in the release notes document.

SW Platforms
------------
The supported SW platforms are listed in the release notes document.

The compilers used for driver validation are listed in the release notes
document.

Integration with RTOS
=====================
To integrate this driver into a real-time application import ipc-shm-rtos.mk
in the application makefile.

The following variables must be set by the caller makefile:
 * SHM_PLATFORM      - hardware platform to build the driver for
 * SHM_OS_TARGET     - target RTOS to build the driver for
 * SHM_DRIVER_PATH   - path to the driver directory

The ipc-shm-rtos.mk makefile will produce the next variables:
 * SHM_DRIVER_SRC_DIR       - source driver directories
 * SHM_DRIVER_INCLUDES_DIRS - included driver directories
 * SHM_DRIVER_INCLUDE_FILES - list driver include files
 * SHM_DRIVER_SOURCE_FILES  - list driver source files
 * SHM_DRIVER_OUT_FILES     - list driver object files

The compiler, assembler and linker flags used for building the IPCF driver are
from NXP RTD. The driver doesn't need any additional flags.

The name of the interrupt handler must be **ipcsShmHardirq** when MSCM is used
and the callback function from RX channel **ipcsShmMruNotification** when the MRU is used

Integration with NXP RTOS
-------------------------
For integration with any NXP RTOS:
 - a category 2 ISR must be registered for each instance for the configured RX
   external IRQ, moreover the ISR attribute IsrFunction must be named
   **ipcsShmHardirq** when MSMC is used
 - an ISR must be registered for the configured MU RX IRQ with the following
   handler name: **ipcsShmMuNotification** when MU is used
 - an interrupt notification function must be set for the receiving channel named
   **ipcsShmMruNotification** when the MRU is used
 - an extended, non-preemptive task, without autostart and with higher
   priority than other tasks using shared memory driver must be configured
   with the following name: **ipcsShmSoftirq**
 - two events must be configured to be used in **ipcsShmSoftirq** task:
    * IPC_EVENT_RX_IRQ: triggered  when a message has been received from the remote core
    * IPC_EVENT_OS_FREE: triggered by the user application to call ipcsShmFree()

Note: the user application must not interfere with any of the OS objects above,
other than the configuration of ISR and task priorities and the task stack size

Integration with FreeRTOS
-------------------------
For integration with FreeRTOS:
 - an ISR must be registered for the configured RX external IRQ with the
   following handler name: **ipcsShmHardirq** when MSMC is used
 - an ISR must be registered for the configured MU RX IRQ with the following
   handler name: **ipcsShmMuNotification** when MU is used
 - an interrupt notification function must be set for the receiving channel named
   **ipcsShmMruNotification** when the MRU is used
 - a task with IPC_SOFTIRQ_PRIORITY priority must be created to be used by the shared
   memory driver and must be configured with the following name: **ipcsShmSoftirq**

Integration with Zephyr
-----------------------
For integration with Zephyr:
 - an ISR must be registered for the configured RX external IRQ with the
   following handler name: **ipcsShmHardirq** when MSMC is used
 - an ISR must be registered for the configured MU RX IRQ with the following
   handler name: **ipcsShmMuNotification** when MU is used
 - an interrupt notification function must be set for the receiving channel named
   **ipcsShmMruNotification** when the MRU is used
 - a thread with IPC_SOFTIRQ_PRIORITY priority and IPC_SOFTIRQ_STACK_SIZE stack
   size is created by the shared memory driver for deferred interrupt
   processing

Integration with XOS
--------------------
For integration with XOS:
 - an ISR must be registered for the configured RX external IRQ with the
   following handler name: **ipcsShmHardirq** when MSMC is used
 - an ISR must be registered for the configured MU RX IRQ with the following
   handler name: **ipcsShmMuNotification** when MU is used
 - an interrupt notification function must be set for the receiving channel named
   **ipcsShmMruNotification** when the MRU is used
 - a thread with IPC_SOFTIRQ_PRIORITY priority and IPC_SOFTIRQ_STACK_SIZE stack
   size is created by the shared memory driver for deferred interrupt
   processing

Integration in Baremetal
------------------------
For integration in Baremetal:
 - an ISR must be registered for the configured RX external IRQ with the
   following handler name: **ipcsShmHardirq** when MSMC is used
 - an ISR must be registered for the configured MU RX IRQ with the following
   handler name: **ipcsShmMuNotification** when MU is used
 - an interrupt notification function must be set for the receiving channel named
   **ipcsShmMruNotification** when the MRU is used

Configuration Notes
===================
There are five hardware-related parameters that can be configured at the driver
API level: TX and RX inter-core interrupt IDs, local core ID, remote core ID and
trusted cores.

The interrupt IDs are MSCM core-to-core directed interrupt IDs or MU/MRU interrupt
sources. Users can only choose to use MSCM, MU or MRU driver for the corresponding
instances between cores.

In case of using the MSCM core-to-core directed interrupt, the interrupt IDs for each
platform can be selected from the RTD header files (ex: INT0_IRQn or MSCM_INT0_IRQn)
or IPC_IRQ_NONE for the polling method.

The TX and RX interrupts can be disabled by setting their IDs to IPC_IRQ_NONE.
When the RX (or TX) interrupt is disabled, the local (or remote) application must
check for incoming messages by invoking the function ipcsShmPollChannels().
Disabling both TX and RX interrupt is allowed.

The local and remote core IDs configuration is divided into core type and core
index. Supported values for core type and index are defined in IPCS_SHM_CORE_TYPE_E
and IPCS_SHM_CORE_INDEX_E enums. Local core ID and trusted cores configuration is
reserved for use in Linux shared memory driver and has no effect in this
implementation. Local and remote core IDs also have no effect when MU or MRU
are used.

For ARM platforms a default value can be assigned to the remote core ID by choosing
IPC_CORE_DEFAULT as the core type. When using this default value the core index
is automatically chosen by the driver.

Cautions
========
The user must zero set the shared SRAM memory area before initializing the driver.

This driver provides direct access to physical memory that is mapped as
non-cachable by default. To use cached memory the symbol D_CACHE_ENABLE needs
to be defined.

Therefore, applications should make only aligned accesses in the shared memory
buffers. Caution should be used when working with functions that may do unaligned
accesses (e.g., string processing functions).

The driver ensures freedom from interference between local and remote memory domains
by executing all write operations only in the local memory.

The driver is thread safe as long as only one thread is pushing and only one
thread is popping: Single-Producer - Single-Consumer.

This thread safety is lock-free and needs one additional sentinel element in
the ring buffers between the write and read indexes that is never written.

The driver is thread safe for different instances but not for same instance.

The driver ensures that a managed channel will no longer be used (by both sides)
in case a memory overflow occurs and corrupts the buffer descriptor.

The driver ensures that an unmanaged channel will no longer be used (by both sides)
in case a memory overflow occurs and corrupts the index.

The driver does not ensure the integrity and correctness of the data if the
length exceeds the configured maximum length.
