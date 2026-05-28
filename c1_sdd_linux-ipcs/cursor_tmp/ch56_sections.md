## 5.1 Definition定义

RTOS 部署变体在单地址空间内实现 Drv_Ipcs_Osal_Cmp 与 Drv_Ipcs_Hal_Cmp：OS 实现三选一（FreeRTOS、ThreadX、AUTOSAR OS），HAL 位于 `ipcs/mcu/hw/` 并由三种 OS 实现共用。通信核心仍使用第 4 章 `ipcs/ipcs_cores` 与 `ipc-shm.h` 对外 API。

本章描述 RTOS 侧 OSAL/HAL 源文件与头文件依赖；函数级设计见 §5.3–§5.7。Baremetal 源码存在于 `ipcs/mcu/os/baremetal/`，不纳入本文档范围（见 §1.3）。

## 5.2 Files

### 5.2.1 文件列表

| 组件 | 文件 |
|---|---|
| Drv_Ipcs_Hal_Cmp | ipcs/mcu/hw/ipc-hw-platform.h |
| Drv_Ipcs_Hal_Cmp | ipcs/mcu/hw/ipc-hw.c |
| Drv_Ipcs_Hal_Cmp | ipcs/mcu/hw/ipc-hw.h |
| Drv_Ipcs_Osal_Cmp | ipcs/mcu/os/autosar/ipc-os-autosar.c |
| Drv_Ipcs_Osal_Cmp | ipcs/mcu/os/freertos/ipc-os-freertos.c |
| Drv_Ipcs_Osal_Cmp | ipcs/mcu/os/ipc-os.h |
| Drv_Ipcs_Osal_Cmp | ipcs/mcu/os/threadx/ipc-os-threadx.c |
| （构建） | ipcs/mcu/ipc-shm-rtos.mk |

### 5.2.2 ipc-hw-platform.h

描述：

> ipcs/mcu/hw/ipc-hw-platform.h 属于 Drv_Ipcs_Hal_Cmp / 平台定义。

依赖关系：

C1_M7_COMMON.h、C1_SCB.h、C1_MSCM.h（与 `ipcs/mcu/hw/ipc-hw-platform.h` 一致）

![RTOS ipc-hw-platform.h 头文件依赖](cursor_tmp/files_32_svgs/5_2_02.svg)

### 5.2.3 ipc-hw.c

描述：

> ipcs/mcu/hw/ipc-hw.c 属于 Drv_Ipcs_Hal_Cmp / IPCS-HAL。

依赖关系：

ipc-shm.h、ipc-os.h、ipc-hw.h、ipc-hw-platform.h（与 `ipcs/mcu/hw/ipc-hw.c` 中 #include 顺序一致）

![RTOS ipc-hw.c 头文件依赖](cursor_tmp/files_32_svgs/5_2_03.svg)

### 5.2.4 ipc-hw.h

描述：

> ipcs/mcu/hw/ipc-hw.h 属于 Drv_Ipcs_Hal_Cmp / IPCS-HAL。

依赖关系：

本头文件未 #include 工程内其他头文件（仅 HAL API 声明）。

![RTOS ipc-hw.h 头文件依赖](cursor_tmp/files_32_svgs/5_2_04.svg)

### 5.2.5 ipc-os-autosar.c

描述：

> ipcs/mcu/os/autosar/ipc-os-autosar.c 属于 Drv_Ipcs_Osal_Cmp / AUTOSAR OS 实现。

依赖关系：

Os.h、ipc-shm.h、ipc-os.h、ipc-hw.h（与 `ipcs/mcu/os/autosar/ipc-os-autosar.c` 中 #include 顺序一致）

![RTOS ipc-os-autosar.c 头文件依赖](cursor_tmp/files_32_svgs/5_2_05.svg)

### 5.2.6 ipc-os-freertos.c

描述：

> ipcs/mcu/os/freertos/ipc-os-freertos.c 属于 Drv_Ipcs_Osal_Cmp / FreeRTOS 实现。

依赖关系：

ipc-shm.h、ipc-os.h、ipc-hw.h、FreeRTOS.h、task.h（与 `ipcs/mcu/os/freertos/ipc-os-freertos.c` 一致）

![RTOS ipc-os-freertos.c 头文件依赖](cursor_tmp/files_32_svgs/5_2_06.svg)

### 5.2.7 ipc-os.h

描述：

> ipcs/mcu/os/ipc-os.h 属于 Drv_Ipcs_Osal_Cmp / IPCS-OSAL。

依赖关系：

本头文件未 #include 工程内其他头文件（OSAL 宏与 API 声明）。

![RTOS ipc-os.h 头文件依赖](cursor_tmp/files_32_svgs/5_2_07.svg)

### 5.2.8 ipc-os-threadx.c

描述：

> ipcs/mcu/os/threadx/ipc-os-threadx.c 属于 Drv_Ipcs_Osal_Cmp / ThreadX 实现。

依赖关系：

ipc-shm.h、ipc-os.h、ipc-hw.h、tx_api.h、tx_event_flags.h（与 `ipcs/mcu/os/threadx/ipc-os-threadx.c` 一致）

![RTOS ipc-os-threadx.c 头文件依赖](cursor_tmp/files_32_svgs/5_2_08.svg)

### 5.2.9 ipc-shm-rtos.mk

描述：

> ipcs/mcu/ipc-shm-rtos.mk 为 RTOS 侧构建集成 Makefile，声明参与编译的 Core/OSAL/HAL 源文件集合。

依赖关系：

构建描述文件，无 C 头文件 #include 依赖图。

---

## 6.1 Definition定义

Linux 部署变体通过 `ipcs/mpu` 实现 Drv_Ipcs_Linux_Adapt_Cmp 与 Drv_Ipcs_Hal_Cmp：UIO、CDEV 为用户侧代理加内核 Backend；全内核形态将 OSAL 与 HAL 均置于内核模块（见 §3.3）。通信核心仍使用第 4 章 `ipcs/ipcs_cores`。

本章描述 Linux 侧源文件与头文件依赖；单元函数设计见 §6.3–§6.10。

## 6.2 Files

### 6.2.1 文件列表

| 组件 | 文件 |
|---|---|
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_uio/ipc-os.c |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_uio/ipc-os.h |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_cdev/ipc-os.c |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_cdev/ipc-os.h |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-os.c |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-os.h |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-uio.c |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-uio.h |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-cdev.c |
| Drv_Ipcs_Linux_Adapt_Cmp | ipcs/mpu/os_kernel/ipc-cdev.h |
| Drv_Ipcs_Hal_Cmp | ipcs/mpu/hw/c1/ipc-hw.c |
| Drv_Ipcs_Hal_Cmp | ipcs/mpu/hw/c1/ipc-hw-platform.h |
| Drv_Ipcs_Hal_Cmp | ipcs/mpu/hw/ipc-hw.h |

### 6.2.2 ipc-os.c（UIO 用户侧）

描述：

> ipcs/mpu/os_uio/ipc-os.c 属于 Drv_Ipcs_Linux_Adapt_Cmp / UIO 用户侧代理。

依赖关系：

fcntl.h、unistd.h、stdio.h、sys/mman.h、sys/syscall.h、pthread.h、stdlib.h、dirent.h、ipc-os.h、ipc-hw.h、ipc-shm.h、ipc-uio.h（与 `ipcs/mpu/os_uio/ipc-os.c` 中 #include 顺序一致）

![Linux UIO ipc-os.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_02.svg)

### 6.2.3 ipc-os.h（UIO 用户侧）

描述：

> ipcs/mpu/os_uio/ipc-os.h 属于 Drv_Ipcs_Linux_Adapt_Cmp / UIO 用户侧 OSAL 头。

依赖关系：

errno.h、stdint.h、stdbool.h、string.h、stdio.h；无 ipcs 内其他头文件。

![Linux UIO ipc-os.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_03.svg)

### 6.2.4 ipc-os.c（CDEV 用户侧）

描述：

> ipcs/mpu/os_cdev/ipc-os.c 属于 Drv_Ipcs_Linux_Adapt_Cmp / CDEV 用户侧代理。

依赖关系：

fcntl.h、unistd.h、stdio.h、sys/mman.h、sys/syscall.h、sys/ioctl.h、pthread.h、stdlib.h、dirent.h、ipc-os.h、ipc-hw.h、ipc-shm.h、ipc-cdev.h（与 `ipcs/mpu/os_cdev/ipc-os.c` 一致）

![Linux CDEV ipc-os.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_04.svg)

### 6.2.5 ipc-os.h（CDEV 用户侧）

描述：

> ipcs/mpu/os_cdev/ipc-os.h 属于 Drv_Ipcs_Linux_Adapt_Cmp / CDEV 用户侧 OSAL 头。

依赖关系：

errno.h、stdint.h、stdbool.h、string.h、stdio.h；无 ipcs 内其他头文件。

![Linux CDEV ipc-os.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_05.svg)

### 6.2.6 ipc-os.c（全内核 OSAL）

描述：

> ipcs/mpu/os_kernel/ipc-os.c 属于 Drv_Ipcs_Linux_Adapt_Cmp / 全内核 OSAL 实现。

依赖关系：

linux/ioport.h、linux/io.h、linux/interrupt.h、linux/of_irq.h、linux/of_address.h、linux/version.h、ipc-os.h、ipc-hw.h、ipc-shm.h（与 `ipcs/mpu/os_kernel/ipc-os.c` 一致）

![Linux 全内核 ipc-os.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_06.svg)

### 6.2.7 ipc-os.h（全内核 OSAL）

描述：

> ipcs/mpu/os_kernel/ipc-os.h 属于 Drv_Ipcs_Linux_Adapt_Cmp / 内核 OSAL 头。

依赖关系：

linux/module.h

![Linux 全内核 ipc-os.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_07.svg)

### 6.2.8 ipc-uio.c

描述：

> ipcs/mpu/os_kernel/ipc-uio.c 属于 Drv_Ipcs_Linux_Adapt_Cmp / UIO 内核 Backend。

依赖关系：

linux/module.h、linux/platform_device.h、linux/mod_devicetable.h、linux/uio_driver.h、linux/cdev.h、ipc-shm.h、ipc-os.h、ipc-hw.h、ipc-uio.h（与 `ipcs/mpu/os_kernel/ipc-uio.c` 一致）

![Linux ipc-uio.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_08.svg)

### 6.2.9 ipc-uio.h

描述：

> ipcs/mpu/os_kernel/ipc-uio.h 属于 Drv_Ipcs_Linux_Adapt_Cmp / UIO 命令与宏定义。

依赖关系：

本头文件无 #include（UIO 命令宏）。

![Linux ipc-uio.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_09.svg)

### 6.2.10 ipc-cdev.c

描述：

> ipcs/mpu/os_kernel/ipc-cdev.c 属于 Drv_Ipcs_Linux_Adapt_Cmp / CDEV 内核 Backend。

依赖关系：

linux/module.h、linux/kernel.h、linux/fs.h、linux/cdev.h、linux/interrupt.h、linux/of_irq.h、linux/of_address.h、linux/wait.h、asm/errno.h、ipc-os.h、ipc-hw.h、ipc-shm.h、ipc-cdev.h（与 `ipcs/mpu/os_kernel/ipc-cdev.c` 一致）

![Linux ipc-cdev.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_10.svg)

### 6.2.11 ipc-cdev.h

描述：

> ipcs/mpu/os_kernel/ipc-cdev.h 属于 Drv_Ipcs_Linux_Adapt_Cmp / CDEV ioctl 定义。

依赖关系：

linux/ioctl.h、sys/ioctl.h

![Linux ipc-cdev.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_11.svg)

### 6.2.12 ipc-hw.c

描述：

> ipcs/mpu/hw/c1/ipc-hw.c 属于 Drv_Ipcs_Hal_Cmp / Linux HAL 实现。

依赖关系：

linux/io.h、ipc-shm.h、ipc-os.h、ipc-hw.h、ipc-hw-platform.h（与 `ipcs/mpu/hw/c1/ipc-hw.c` 一致）

![Linux ipc-hw.c 头文件依赖](cursor_tmp/files_32_svgs/6_2_12.svg)

### 6.2.13 ipc-hw-platform.h

描述：

> ipcs/mpu/hw/c1/ipc-hw-platform.h 属于 Drv_Ipcs_Hal_Cmp / Linux 平台定义。

依赖关系：

本头文件无 #include（核索引与 MSCM 寄存器布局宏）。

![Linux ipc-hw-platform.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_13.svg)

### 6.2.14 ipc-hw.h

描述：

> ipcs/mpu/hw/ipc-hw.h 属于 Drv_Ipcs_Hal_Cmp / HAL API 声明（Linux 构建包含路径）。

依赖关系：

本头文件无 #include（HAL API 声明）。

![Linux ipc-hw.h 头文件依赖](cursor_tmp/files_32_svgs/6_2_14.svg)
