SW Detail Design Specification

For IPCS Driver

IPCS Driver软件详细设计规范

| ROLES角色 | Name姓名 | Department部门 | Date日期 |
|---|---|---|---|
| AUTHOR(S)作者： | 倘亚朋 | 软件研发部 | 2026.5.22 |
| REVIEWER(S)审查： | 安然/赵笃/喻明睿/张帅/伊焕利/肖敏元/倘亚朋/宋晓婷/栗瑞江/Wenke | 软件研发部 | 2026.5.22 |
| APPROVER (S)批准： | 安然 | 软件研发部 | 2026.5.22 |

| Version / 版本 | Date / 日期 | Editor / 编辑人 | Status / 文档状态 | Change description / 变更简述 |
|---|---|---|---|---|
| V0.1 | 2026.5.7 | Cursor Agent | Draft | Initial version for review，基于 ipcs 源码、reference.md、ipcs-architecture.pdf 与 aspice.pdf 生成 |
| V0.2 | 2026.5.19 | Cursor Agent | Draft | 按 ASPICE SWE.3 重构为第 1–6 章；新增 §2.4–2.6、Linux Refinement、第 5 章与第 6 章追溯 |
| V0.7 | 2026.5.19 | Cursor Agent | Draft | 完善 Linux 部署变体函数设计、关键场景 SVG 与分层静态图 |
| V0.8 | 2026.5.19 | Cursor Agent | Draft | §5.7/§6.7 跨单元场景改为 UML 序列图（PlantUML→SVG） |
| V0.6 | 2026.5.19 | Cursor Agent | Draft | 基于 ipcs 源码补强第 2、3 章；明确 UIO/CDEV 与全内核实现的用户侧/内核侧职责 |
| V0.5 | 2026.5.19 | Cursor Agent | Draft | 精简第 2 章为组件—单元映射；重写第 3 章分层与部署变体；清理目录重复项 |
| V0.4 | 2026.5.19 | Cursor Agent | Draft | 拆分第 2 章；新增第 3 章三层架构与 Linux 适配；勘误 UIO/CDEV 代理与全内核形态 |
| V0.3 | 2026.5.19 | Cursor Agent | Draft | 第 2 章改为架构符合性与软件单元划分；增加 SW-Unit-ID 与组件映射；插图全部 SVG；对照 ipcs/ 源码修订 |

## CONTENTS 目录

- 1 INTRODUCTION简介
  - 1.1 Confidentiality 保密性
  - 1.2 Purpose of the document文档目的
  - 1.3 Scope范围
  - 1.4 References 参考文件
  - 1.5 Abbreviations缩略语
- 2 软件单元划分 Software Unit Identification
  - 2.1 软件单元清单
  - 2.2 架构组件与软件单元映射
- 3 分层架构与部署变体设计
  - 3.1 三层架构与接口契约
  - 3.2 RTOS 部署变体
  - 3.3 Linux 部署变体
  - 3.3.1 UIO 实现
  - 3.3.2 CDEV 实现
  - 3.3.3 全内核实现
  - 3.4 OSAL/HAL 实现位置对照
- 4 公共详细设计（跨部署变体共享）
  - 4.1 Definition定义
  - 4.2 Files
  - 4.3 External Interfaces外部接口
  - 4.4 Internal Functions 内部函数
  - 4.5 Global variants 全局变量
  - 4.6 Data Structure 类型定义
  - 4.7 Dynamic Detailed Design 动态详细设计
- 5 RTOS 部署变体详细设计
  - 5.1 总述
  - 5.2 Files 与依赖
  - 5.3 AUTOSAR OS 实现
  - 5.4 FreeRTOS 实现
  - 5.5 ThreadX 实现
  - 5.6 HAL 单元设计（MCU 共用）
  - 5.7 RTOS 动态详细设计
- 6 Linux 部署变体详细设计
  - 6.1 总述
  - 6.2 源码与构建结构
  - 6.3 全内核实现函数设计
  - 6.4 UIO 实现函数设计
  - 6.5 CDEV 实现函数设计
  - 6.6 Linux HAL 函数设计
  - 6.7 Linux 关键场景流程
  - 6.8 Linux 全局变量与私有类型
- 7 Traceability and Consistency Evidence 追溯与一致性证据
  - 7.1 SWE.3 覆盖说明
  - 7.2 架构—设计—源码追溯矩阵
  - 7.3 源码核对结果
  - 7.4 接口判定规则

# 1 INTRODUCTION简介

## 1.1 Confidentiality 保密性

任何披露必须与负责的流程经理协调。

本文件过程说明仅限直接参与项目的人员查看。转让给其他方，尤其是 Star Gather 以外的合作伙伴，必须由项目负责人协调，并受开发合同中有关保密规定的约束。

## 1.2 Purpose of the document文档目的

本文档按照 SWE.3 Software Detailed Design and Unit Construction 的要求，为 IPCS Driver（RTOS 与 Linux 部署变体）建立软件详细设计。文档内容描述软件单元的静态结构、接口、数据结构、关键动态行为，并与 IPCS 软件架构中定义的组件和接口保持一致。

## 1.3 Scope范围

本文档适用于 ipcs/ 目录下的 IPC Shared Memory Driver 源码，包括：

- ipcs/ipcs_cores/：跨部署变体共享的通信核心与队列；
- ipcs/mcu/：RTOS 部署变体（FreeRTOS、ThreadX、AUTOSAR OS 实现，不含 Baremetal 详细设计）；
- ipcs/mpu/：Linux 部署变体（全内核、UIO、CDEV 实现）。

逻辑架构以 ipcs-architecture.pdf 为准；三层架构与 Linux 部署变体见第 3 章。

## 1.4 References 参考文件

| Reference ID / 编号 | Document Name / 文档名称 | Version / 版本 | Date / 日期 | Author / 作者 | Status / 状态 |
|---|---|---|---|---|---|
| 1 | Automotive SPICE® Process Assessment Model, SWE.3 Software Detailed Design and Unit Construction | 4.0 | 2023 | VDA | Release |
| 2 | IPCS Driver 软件架构设计 ipcs-architecture.pdf | 1.0 | 2026.4.16 | 倘亚朋 | 待评审 |
| 3 | reference.md 详细设计文档模板 | N/A | N/A | N/A | 模板输入 |
| 4 | ipcs/ IPCF Shared Memory Driver for Real-Time Operating Systems 源码 | SW 4.0.1 | 2023 | NXP | 源码输入 |

## 1.5 Abbreviations缩略语

| Abbreviation / 缩写 | Meaning/Explanation / 解释 |
|---|---|
| API | Application Programming Interface |
| AUTOSAR | AUTomotive Open System ARchitecture |
| BD | Buffer Descriptor |
| CDD | Complex Device Driver |
| HAL | Hardware Abstraction Layer |
| HW | Hardware |
| IPCF | Inter-Platform Communication Framework |
| IPCS | Inter-Processor Communication System |
| IRQ | Interrupt Request |
| ISR | Interrupt Service Routine |
| MMU | Memory Management Unit |
| MSCM | Multi-Core Shared Memory / Messaging interrupt controller as used by source naming |
| MRU | Messaging/Message Routing Unit, used by integration notes |
| MU | Messaging Unit, used by integration notes |
| OS | Operating System |
| OSAL | OS Abstraction Layer |
| RTOS | Real-Time Operating System |
| SHM | Shared Memory |
| SPSC | Single Producer Single Consumer |
| UIO | Userspace I/O |

| Deployment Variant | 部署变体（RTOS 部署变体 / Linux 部署变体） |
| Implementation | 实现（如 FreeRTOS 实现、UIO 实现、全内核实现） |
| User-Side Proxy | 用户侧代理（Linux UIO/CDEV 用户库：满足 P4/P5 契约，对 OS/HW 操作为转发实现） |
| Refinement | 架构细化：SDD 对逻辑组件的实现分解，不新增架构 ID |
| In-Kernel | 全内核实现 |
| CDEV | Character Device 实现 |

# 2 软件单元划分 Software Unit Identification

本章只定义软件单元及其与软件架构组件的映射关系。架构基线见参考文献 [2] `ipcs-architecture.pdf`；分层与部署变体设计见第 3 章；函数级详细设计见第 4–6 章。

## 2.1 软件单元清单

软件单元按源码文件或稳定接口头文件划分。

| SW-Unit-ID | 源码文件 | 说明 |
|---|---|---|
| SWU_IPCS_CORE_SHM | ipcs/ipcs_cores/ipc-shm.c | SHM Core，实现实例、通道、发送接收主流程 |
| SWU_IPCS_CORE_QUEUE | ipcs/ipcs_cores/ipc-queue.c | 环形队列实现 |
| SWU_IPCS_CORE_UTIL | ipcs/ipcs_cores/ipc-util.c | Core 工具函数 |
| SWU_IPCS_CORE_TYPES | ipcs/ipcs_cores/ipc-types.h | 公共类型、配置结构、BD 类型 |
| SWU_IPCS_HAL_MCU | ipcs/mcu/hw/ipc-hw.c | RTOS 部署变体 HAL 实现 |
| SWU_IPCS_HAL_LINUX | ipcs/mpu/hw/c1/ipc-hw.c | Linux 内核侧 HAL 实现 |
| SWU_IPCS_OSAL_AUTOSAR | ipcs/mcu/os/autosar/ipc-os-autosar.c | AUTOSAR OS 实现 |
| SWU_IPCS_OSAL_FREERTOS | ipcs/mcu/os/freertos/ipc-os-freertos.c | FreeRTOS 实现 |
| SWU_IPCS_OSAL_THREADX | ipcs/mcu/os/threadx/ipc-os-threadx.c | ThreadX 实现 |
| SWU_IPCS_OSAL_HDR | ipcs/mcu/os/ipc-os.h | RTOS OSAL 接口声明 |
| SWU_IPCS_LINUX_OS_UIO | ipcs/mpu/os_uio/ipc-os.c | UIO 用户侧 OSAL/HAL 契约代理 |
| SWU_IPCS_LINUX_OS_CDEV | ipcs/mpu/os_cdev/ipc-os.c | CDEV 用户侧 OSAL/HAL 契约代理 |
| SWU_IPCS_LINUX_OS_KERN | ipcs/mpu/os_kernel/ipc-os.c | Linux 全内核 OSAL 实现 |
| SWU_IPCS_LINUX_UIO_KO | ipcs/mpu/os_kernel/ipc-uio.c | UIO 内核 Backend |
| SWU_IPCS_LINUX_CDEV_KO | ipcs/mpu/os_kernel/ipc-cdev.c | CDEV 内核 Backend |

## 2.2 架构组件与软件单元映射

| 架构组件 ID | SW-Unit-ID | 适用范围 |
|---|---|---|
| Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | 全部部署变体 |
| Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | 全部部署变体 |
| Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES、工程配置 `ipcf_Ip_Cfg*.h` | 全部部署变体 |
| Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | RTOS 各 OS 实现、Linux 全内核实现 |
| Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | RTOS HAL、Linux 内核 HAL |
| Drv_Ipcs_Linux_Adapt_Cmp | SWU_IPCS_LINUX_OS_UIO、SWU_IPCS_LINUX_OS_CDEV、SWU_IPCS_LINUX_OS_KERN、SWU_IPCS_LINUX_UIO_KO、SWU_IPCS_LINUX_CDEV_KO、SWU_IPCS_HAL_LINUX | Linux 部署变体 |

第 4 章及以下函数说明表中的「软件单元 ID」引用本章；「对应软件架构 ID」引用 `ipcs-architecture.pdf` 中的架构组件 ID。

# 3 分层架构与部署变体设计

## 3.1 SHM / OSAL / HAL 三层接口契约

IPCS 采用 SHM、OSAL、HAL 三层结构。SHM 层位于 `ipcs/ipcs_cores`，只通过固定函数原型调用 OSAL 与 HAL；不同部署变体不得改变这些接口契约。

| 层 | 架构组件 | 接口文件 | 关键接口 | 设计约束 |
|---|---|---|---|---|
| SHM | Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp | `ipc-shm.h`、`ipc-queue.h` | `ipcsShmInit`、`ipcsShmTx`、`ipcsShmPollChannels` | 对上提供应用接口，对下只依赖 OSAL/HAL 契约 |
| OSAL | Drv_Ipcs_Osal_Cmp | `ipc-os.h` 或同名 Linux 用户侧符号 | `ipcsOsInit`、`ipcsOsGetLocalShm`、`ipcsOsPollChannels` | 提供共享内存映射、收包调度与中断上下文联结 |
| HAL | Drv_Ipcs_Hal_Cmp | `ipc-hw.h` | `ipcsHwInit`、`ipcsHwIrqNotify`、`ipcsHwIrqEnable` | 提供 MSCM/IRQ、缓存与平台核索引操作 |

该契约保证 `ipcs_cores` 可在 RTOS、Linux UIO、Linux CDEV、Linux 全内核实现间复用。

### 3.1.1 分层与部署实现静态图

下图描述 SHM、OSAL、HAL 三层契约，以及 RTOS、Linux UIO/CDEV、Linux 全内核三类实现位置。

![IPCS layered architecture and Linux deployment variants](cursor_tmp/flow_svgs/architecture_layered_linux_variants.svg)


## 3.2 RTOS 部署变体

RTOS 部署变体包括 FreeRTOS、ThreadX、AUTOSAR OS 三种实现。Baremetal 源码存在于 `ipcs/mcu/os/baremetal`，但不纳入本文档详细设计范围。

| 实现 | OSAL 源文件 | HAL 源文件 | 结构说明 |
|---|---|---|---|
| FreeRTOS 实现 | `ipcs/mcu/os/freertos/ipc-os-freertos.c` | `ipcs/mcu/hw/ipc-hw.c` | SHM、OSAL、HAL 位于同一地址空间 |
| ThreadX 实现 | `ipcs/mcu/os/threadx/ipc-os-threadx.c` | `ipcs/mcu/hw/ipc-hw.c` | SHM、OSAL、HAL 位于同一地址空间 |
| AUTOSAR OS 实现 | `ipcs/mcu/os/autosar/ipc-os-autosar.c` | `ipcs/mcu/hw/ipc-hw.c` | SHM、OSAL、HAL 位于同一地址空间 |

RTOS 部署变体中，Core 调用 `ipcsOs*` 与 `ipcsHw*` 时直接进入 OSAL/HAL 实现，不存在用户侧代理或内核 Backend。

## 3.3 Linux 部署变体

Linux 部署变体包括 UIO、CDEV、全内核三种实现。`ipcs-architecture.pdf` 中的 `Drv_Ipcs_Linux_Adapt_Cmp` 是逻辑组件；详细设计按源码进一步说明其用户侧与内核侧职责。

### 3.3.1 UIO 实现

UIO 实现由用户库代理、UIO 内核 Backend、Linux HAL 三部分组成。

| 部分 | 源码 | 设计职责 |
|---|---|---|
| 用户侧代理 | `ipcs/mpu/os_uio/ipc-os.c` | 导出 `ipcsOs*`、`ipcsHw*` 同名符号，满足 SHM 对 OSAL/HAL 的接口契约；完成 `/dev/mem` 映射、UIO 设备打开、RX 线程创建 |
| 内核 Backend | `ipcs/mpu/os_kernel/ipc-uio.c` | 注册 UIO 设备、处理中断、向用户侧传递事件 |
| 内核 HAL | `ipcs/mpu/hw/c1/ipc-hw.c` | 执行 MSCM 与 IRQ 相关真实硬件操作 |

用户侧 `ipcsHwIrqEnable`、`ipcsHwIrqDisable`、`ipcsHwIrqNotify` 通过 `ipcsSendUioCmd` 写 UIO fd 转发命令；`ipcsHwInit`、`ipcsHwFree` 是空实现，源码注释说明初始化和释放由内核 UIO 模块处理。

### 3.3.2 CDEV 实现

CDEV 实现由用户库代理、字符设备 Backend、Linux HAL 三部分组成。

| 部分 | 源码 | 设计职责 |
|---|---|---|
| 用户侧代理 | `ipcs/mpu/os_cdev/ipc-os.c` | 导出 `ipcsOs*`、`ipcsHw*` 同名符号，满足 SHM 对 OSAL/HAL 的接口契约；通过 `/dev/ipc-shm-cdev` 与内核通信 |
| 内核 Backend | `ipcs/mpu/os_kernel/ipc-cdev.c` | 提供字符设备、ioctl、wait queue、ISR 处理 |
| 内核 HAL | `ipcs/mpu/hw/c1/ipc-hw.c` | 执行 MSCM 与 IRQ 相关真实硬件操作 |

用户侧 `ipcsHwIrqEnable`、`ipcsHwIrqDisable`、`ipcsHwIrqNotify` 使用 `IPC_CDEV_CMD_*` ioctl 转发到内核；`ipcsHwInit`、`ipcsHwFree` 是空实现，源码注释说明由内核模块处理。

### 3.3.3 全内核实现

全内核实现不使用用户侧代理。Core、OSAL、HAL 均在内核模块中运行，形态与 RTOS 部署变体一致。

| 部分 | 源码 | 设计职责 |
|---|---|---|
| OSAL | `ipcs/mpu/os_kernel/ipc-os.c` | 实现 `ipcsOsInit`、`ipcsOsFree`、`ipcsOsGetLocalShm`、`ipcsOsGetRemoteShm`、`ipcsOsPollChannels` |
| HAL | `ipcs/mpu/hw/c1/ipc-hw.c` | 实现 `ipcsHwInit`、`ipcsHwIrqEnable`、`ipcsHwIrqDisable`、`ipcsHwIrqNotify`、`ipcsHwIrqClear` 等硬件操作 |

`ipcs/mpu/os_kernel/ipc-os.c` 使用 tasklet 进行延迟收包处理，`ipcs/mpu/hw/c1/ipc-hw.c` 负责映射 MSCM 并访问中断相关寄存器。

## 3.4 OSAL/HAL 实现位置对照

| 接口 | RTOS 部署变体 | Linux UIO 实现 | Linux CDEV 实现 | Linux 全内核实现 |
|---|---|---|---|---|
| `ipcsOsInit` / `ipcsOsFree` | `mcu/os/*/ipc-os-*.c` | 用户侧 `os_uio/ipc-os.c` + 内核 `ipc-uio.c` | 用户侧 `os_cdev/ipc-os.c` + 内核 `ipc-cdev.c` | `os_kernel/ipc-os.c` |
| `ipcsOsGetLocalShm` / `ipcsOsGetRemoteShm` | `mcu/os/*/ipc-os-*.c` | 用户侧 `/dev/mem` mmap | 用户侧 mmap | `os_kernel/ipc-os.c` |
| `ipcsOsPollChannels` | `mcu/os/*/ipc-os-*.c` | 用户 RX 线程，内核 UIO 事件唤醒 | 用户 poll / wait，内核字符设备唤醒 | `os_kernel/ipc-os.c` |
| `ipcsHwInit` / `ipcsHwFree` | `mcu/hw/ipc-hw.c` | 用户侧空实现，真实处理在内核 | 用户侧空实现，真实处理在内核 | `mpu/hw/c1/ipc-hw.c` |
| `ipcsHwIrqEnable` / `ipcsHwIrqDisable` / `ipcsHwIrqNotify` | `mcu/hw/ipc-hw.c` | 用户侧 UIO write 代理，内核 HAL 执行 | 用户侧 ioctl 代理，内核 HAL 执行 | `mpu/hw/c1/ipc-hw.c` |
| `ipcsHwFlushCache*` | `mcu/hw/ipc-hw.c` | Linux HAL / 内核路径 | Linux HAL / 内核路径 | `mpu/hw/c1/ipc-hw.c` |


# 4 公共详细设计（跨部署变体共享）

## 4.1 Definition定义

IPCS Driver 是面向同一 SoC 内不同处理核心的 shared memory 通信驱动。公共部分（ipcs/ipcs_cores）实现 IPCF Shared Memory 协议核心，支持 managed/unmanaged channel、中断通知与 polling、多 instance/channel。

本章描述跨部署变体共享的 Core、Queue、配置类型（SHM 层）。分层与部署变体见第 3 章；RTOS 实现见第 5 章；Linux 实现见第 6 章。

## 4.2 Files

### 4.2.1 文件列表

| 组件 | 文件 |
|---|---|
| Drv_Ipcs_Queue_Cmp | ipcs/ipcs_cores/ipc-queue.c |
| Drv_Ipcs_Queue_Cmp | ipcs/ipcs_cores/ipc-queue.h |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-shm.c |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-shm.h |
| Drv_Ipcs_Conf_Cmp | ipcs/ipcs_cores/ipc-types.h |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-util.c |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-util.h |


### 4.2.2 ipc-queue.c

描述：

> ipcs/ipcs_cores/ipc-queue.c 属于 Drv_Ipcs_Queue_Cmp / IPCS-SHM Queue。

依赖关系：

ipc-shm.h, ipc-queue.h, ipc-util.h（与 ipcs/ipcs_cores/ipc-queue.c 中 #include 顺序一致）

![image1.png](cursor_tmp/files_32_svgs/3_2_2.svg)

### 4.2.3 ipc-queue.h

描述：

> ipcs/ipcs_cores/ipc-queue.h 属于 Drv_Ipcs_Queue_Cmp / IPCS-SHM Queue。

依赖关系：

本头文件未 #include ipcs 内其他头文件（除标准版本宏定义外无外部文件依赖）。

![image2.png](cursor_tmp/files_32_svgs/3_2_3.svg)

### 4.2.4 ipc-shm.c

描述：

> ipcs/ipcs_cores/ipc-shm.c 属于 Drv_Ipcs_Core_Cmp / IPCS-SHM。

依赖关系：

ipc-shm.h, ipc-os.h, ipc-hw.h, ipc-queue.h（与 ipcs/ipcs_cores/ipc-shm.c 中 #include 顺序一致）

![image3.png](cursor_tmp/files_32_svgs/3_2_4.svg)

### 4.2.5 ipc-shm.h

描述：

> ipcs/ipcs_cores/ipc-shm.h 属于 Drv_Ipcs_Core_Cmp / IPCS-SHM。

依赖关系：

ipc-types.h, ipcf_Ip_Cfg.h（与 ipcs/ipcs_cores/ipc-shm.h 中 #include 一致；ipcf_Ip_Cfg.h 为工程配置头）

![image4.png](cursor_tmp/files_32_svgs/3_2_5.svg)

### 4.2.6 ipc-types.h

描述：

> ipcs/ipcs_cores/ipc-types.h 属于 Drv_Ipcs_Conf_Cmp / 配置数据类型。

依赖关系：

条件编译：NO_STDINT_H==0 时包含 <stdint.h>、<stddef.h>、<errno.h>；否则由 CPU 宏定义 uintptr_t 等；均包含 Mcal.h、ipcf_Ip_Cfg_Defines.h（与 ipcs/ipcs_cores/ipc-types.h 一致）。

![image5.png](cursor_tmp/files_32_svgs/3_2_6.svg)

### 4.2.7 ipc-util.c

描述：

> ipcs/ipcs_cores/ipc-util.c 属于 Drv_Ipcs_Core_Cmp 公共工具。

依赖关系：

ipc-shm.h, ipc-util.h（与 ipcs/ipcs_cores/ipc-util.c 中 #include 一致）

![image6.png](cursor_tmp/files_32_svgs/3_2_7.svg)

### 4.2.8 ipc-util.h

描述：

> ipcs/ipcs_cores/ipc-util.h 属于 Drv_Ipcs_Core_Cmp 公共工具。

依赖关系：

本头文件未 #include ipcs 内其他头文件。

![image7.png](cursor_tmp/files_32_svgs/3_2_8.svg)

## 4.3 External Interfaces外部接口

本节严格按照 reference.md 的函数说明表格格式描述外部接口。按照任务要求，只有 ipcs/ipcs/ipcs_cores/ipc-shm.c 中的非静态接口为对外接口。

### 4.3.1 ipcsShmInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数初始化配置中声明的所有 shared memory 通信实例，依次初始化 IPCS-HAL、IPCS-OSAL 和 IPCS-SHM channel 资源。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmInit(const struct IPCS_SHM_INSTANCES_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">Config 指针非空；num_instances 大于 0 且不超过 IPC_SHM_MAX_INSTANCES；每个 instance 的 shared memory 地址、channel 数量等配置有效。</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_INSTANCES_CFG_TYPE *</td>
<td>指向 IPCS shared memory instance 配置的指针</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK：初始化成功；-IPC_SHM_E_INVAL 或下层错误码：配置或初始化失败</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_001, IPCS_014, IPCS_016, IPCS_017, IPCS_020, IPCS_025, IPCS_028, IPCS_029, IPCS_031, IPCS_034</td>
</tr>
</tbody>
</table>

processing flow

![image8.png](cursor_tmp/flow_svgs/3_3_1.svg)

### 4.3.2 ipcsShmFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数释放所有已使用的 shared memory 通信实例，清除本端 ready 状态并释放 OS/HW 资源。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmFree(void)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">无输入参数；释放当前处于 IPC_SHM_INSTANCE_USED 状态的 instance。</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_001, IPCS_028, IPCS_029</td>
</tr>
</tbody>
</table>

processing flow

![image9.png](cursor_tmp/flow_svgs/3_3_2.svg)

### 4.3.3 ipcsShmAcquireBuf

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数在 managed channel 上按照请求长度获取本端发送 buffer。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void * ipcsShmAcquireBuf(const uint8 instance, sint32 chan_id, uint32 mem_size)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；chan_id 对应 managed channel；mem_size 非 0；managed channel 与 pool queue integrity 校验通过。</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td>I</td>
<td>mem_size</td>
<td>uint32</td>
<td>请求获取的 buffer 大小，单位为 byte</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">void *</td>
<td colspan="2">非 NULL：可写发送 buffer 地址；NULL：instance/channel/size/integrity 无效或无可用 buffer</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_016, IPCS_018, IPCS_025, IPCS_034, IPCS_035</td>
</tr>
</tbody>
</table>

processing flow

![image10.png](cursor_tmp/flow_svgs/3_3_3.svg)

### 4.3.4 ipcsShmReleaseBuf

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数在 managed channel 上释放接收完成的远端 buffer，并将 buffer descriptor 归还到对应 buffer pool 队列。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmReleaseBuf(const uint8 instance, sint32 chan_id, const void *buf)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；chan_id 对应 managed channel；buf 非空；managed channel integrity 校验通过；buf 属于某个远端 pool。</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td>I</td>
<td>buf</td>
<td>const void *</td>
<td>managed channel buffer 指针</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK：释放成功；负错误码：instance/channel/buf/integrity 无效或 queue push 失败</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_016, IPCS_018, IPCS_023, IPCS_034, IPCS_035</td>
</tr>
</tbody>
</table>

processing flow

![image11.png](cursor_tmp/flow_svgs/3_3_4.svg)

### 4.3.5 ipcsShmTx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数在 managed channel 上提交已写入的 buffer descriptor，并通过 IPCS-HAL 通知远端。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmTx(const uint8 instance, sint32 chan_id, void *buf, uint32 size)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；chan_id 对应 managed channel；buf 非空；size 非 0；managed channel integrity 校验通过；buf 属于某个本端 pool。</td>
</tr>
<tr>
<td rowspan="5">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td>I</td>
<td>buf</td>
<td>void *</td>
<td>managed channel buffer 指针</td>
</tr>
<tr>
<td>I</td>
<td>size</td>
<td>uint32</td>
<td>已写入 buffer 的有效数据大小，单位为 byte</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK：发送提交并通知成功；负错误码：instance/channel/buf/size/integrity 无效或 queue push 失败</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_001, IPCS_015, IPCS_018, IPCS_022, IPCS_023, IPCS_028, IPCS_034, IPCS_035</td>
</tr>
</tbody>
</table>

processing flow

![image12.png](cursor_tmp/flow_svgs/3_3_5.svg)

### 4.3.6 ipcsShmUnmanagedAcquire

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数获取 unmanaged channel 的本端通道内存入口。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void * ipcsShmUnmanagedAcquire(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；chan_id 对应 unmanaged channel；unmanaged channel integrity 校验通过。</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">void *</td>
<td colspan="2">非 NULL：unmanaged channel 本端内存地址；NULL：instance/channel/integrity 无效</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_021, IPCS_034, IPCS_035</td>
</tr>
</tbody>
</table>

processing flow

![image13.png](cursor_tmp/flow_svgs/3_3_6.svg)

### 4.3.7 ipcsShmUnmanagedTx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数在 unmanaged channel 上递增本端发送计数，并通过 IPCS-HAL 通知远端。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmUnmanagedTx(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；chan_id 对应 unmanaged channel；unmanaged channel integrity 校验通过。</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK：发送计数更新并通知成功；负错误码：instance/channel/integrity 无效</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_001, IPCS_021, IPCS_022, IPCS_028, IPCS_034, IPCS_035</td>
</tr>
</tbody>
</table>

processing flow

![image14.png](cursor_tmp/flow_svgs/3_3_7.svg)

### 4.3.8 ipcsShmIsRemoteReady

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数读取远端 shared memory 起始处的 ready 状态，判断对端是否初始化完成。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmIsRemoteReady(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；远端 shared memory 起始位置包含 IPCS_SHM_GLOBAL_TYPE。</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK：远端 ready；-IPC_SHM_E_NOT_READY：远端未 ready；-IPC_SHM_E_INVAL：instance 无效</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_001, IPCS_022, IPCS_034</td>
</tr>
</tbody>
</table>

processing flow

![image15.png](cursor_tmp/flow_svgs/3_3_8.svg)

### 4.3.9 ipcsShmPollChannels

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数在 polling 场景下推进当前 instance 的接收处理。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsShmPollChannels(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">instance 已初始化；远端 ready；OSAL 变体支持在 IPC_IRQ_NONE 场景下调用 polling 接收。</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">非负值：处理的消息数量；负错误码：instance 无效、远端未 ready 或 OSAL polling 不支持/无效</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.h</td>
</tr>
<tr>
<td>满足需求</td>
<td colspan="4">IPCS_019, IPCS_022, IPCS_023, IPCS_034, IPCS_039</td>
</tr>
</tbody>
</table>

processing flow

![image16.png](cursor_tmp/flow_svgs/3_3_9.svg)

## 4.4 Internal Functions 内部函数

本节严格按照 reference.md 的内部函数表格格式描述内部函数。除 3.3 中列出的 9 个对外接口之外，其余源码函数、跨组件调用接口和 OS task 单元均作为内部接口。

### 4.4.1 ipcsQueuePop

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Queue_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_QUEUE</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">removes element from queue</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsQueuePop(struct IPCS_QUEUE_TYPE *queue, void *buf)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>queue</td>
<td>struct IPCS_QUEUE_TYPE *</td>
<td>[IN] queue pointer</td>
</tr>
<tr>
<td>I</td>
<td>buf</td>
<td>void *</td>
<td>[OUT] pointer where to copy the removed element</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.h</td>
</tr>
</tbody>
</table>

processing flow

![image17.png](cursor_tmp/flow_svgs/3_4_1.svg)

### 4.4.2 ipcsQueuePush

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Queue_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_QUEUE</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">pushes element into the queue</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsQueuePush(struct IPCS_QUEUE_TYPE *queue, const void *buf)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>queue</td>
<td>struct IPCS_QUEUE_TYPE *</td>
<td>[IN] queue pointer</td>
</tr>
<tr>
<td>I</td>
<td>buf</td>
<td>const void *</td>
<td>[IN] pointer to element to be pushed into the queue</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.h</td>
</tr>
</tbody>
</table>

processing flow

![image18.png](cursor_tmp/flow_svgs/3_4_2.svg)

### 4.4.3 ipcsQueueInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Queue_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_QUEUE</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">initializes queue and maps push/pop rings in memory</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsQueueInit(struct IPCS_QUEUE_TYPE *queue, uint16 elem_num, uint8 elem_size, uintptr_t push_ring_addr, uintptr_t pop_ring_addr)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="6">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>queue</td>
<td>struct IPCS_QUEUE_TYPE *</td>
<td>[IN] queue pointer</td>
</tr>
<tr>
<td>I</td>
<td>elem_num</td>
<td>uint16</td>
<td>[IN] number of elements in queue</td>
</tr>
<tr>
<td>I</td>
<td>elem_size</td>
<td>uint8</td>
<td>[IN] element size in bytes (8-byte multiple)</td>
</tr>
<tr>
<td>I</td>
<td>push_ring_addr</td>
<td>uintptr_t</td>
<td>[IN] local addr where to map the push buffer ring</td>
</tr>
<tr>
<td>I</td>
<td>pop_ring_addr</td>
<td>uintptr_t</td>
<td>[IN] remote addr where to map the pop buffer ring</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.h</td>
</tr>
</tbody>
</table>

processing flow

![image19.png](cursor_tmp/flow_svgs/3_4_3.svg)

### 4.4.4 ipcsQueueCheckIntegrity

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Queue_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_QUEUE</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">check if the sentinel was not overwritten</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsQueueCheckIntegrity(struct IPCS_QUEUE_TYPE *queue)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>queue</td>
<td>struct IPCS_QUEUE_TYPE *</td>
<td>[IN] queue pointer</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.h</td>
</tr>
</tbody>
</table>

processing flow

![image20.png](cursor_tmp/flow_svgs/3_4_4.svg)

### 4.4.5 ipcsQueueMemSize

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Queue_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_QUEUE</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">return queue footprint in local mapped memory</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static inline uint32 ipcsQueueMemSize(struct IPCS_QUEUE_TYPE *queue)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>queue</td>
<td>struct IPCS_QUEUE_TYPE *</td>
<td>[IN] queue pointer</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uint32</td>
<td colspan="2">size of local mapped memory occupied by queue</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-queue.h</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image21.png](cursor_tmp/flow_svgs/3_4_5.svg)

### 4.4.6 getChannel

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数校验 channel id 并返回 IPCS shared memory channel 私有数据指针。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static inline struct IPCS_SHM_CHANNEL_TYPE * getChannel(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">struct IPCS_SHM_CHANNEL_TYPE *</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image22.png](cursor_tmp/flow_svgs/3_4_6.svg)

### 4.4.7 getManagedChan

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数校验 channel 是否为 managed 类型，并返回 managed channel 私有数据指针。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static inline struct IPCS_MANAGED_CHANNEL_TYPE * getManagedChan(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">struct IPCS_MANAGED_CHANNEL_TYPE *</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image23.png](cursor_tmp/flow_svgs/3_4_7.svg)

### 4.4.8 getUnmanagedChan

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数校验 channel 是否为 unmanaged 类型，并返回 unmanaged channel 私有数据指针。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static inline struct IPCS_UNMANAGED_CHANNEL_TYPE * getUnmanagedChan(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>IPCS shared memory channel 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">struct IPCS_UNMANAGED_CHANNEL_TYPE *</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image24.png](cursor_tmp/flow_svgs/3_4_8.svg)

### 4.4.9 ipcsCheckUchanIntegrity

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数检查 unmanaged channel 本端和远端 sentinel 是否保持完整。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsCheckUchanIntegrity(const struct IPCS_UNMANAGED_CHANNEL_TYPE *uchan)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>uchan</td>
<td>const struct IPCS_UNMANAGED_CHANNEL_TYPE *</td>
<td>源码参数</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image25.png](cursor_tmp/flow_svgs/3_4_9.svg)

### 4.4.10 ipcsCheckMchanIntegrity

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">该函数检查 managed channel 的 channel queue 及所有 pool queue sentinel 是否保持完整。</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsCheckMchanIntegrity(struct IPCS_MANAGED_CHANNEL_TYPE *mchan)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>mchan</td>
<td>struct IPCS_MANAGED_CHANNEL_TYPE *</td>
<td>源码参数</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image26.png](cursor_tmp/flow_svgs/3_4_10.svg)

### 4.4.11 ipcsChannelRx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">handle Rx for a single channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsChannelRx(const uint8 instance, sint32 chan_id, sint32 budget)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel id</td>
</tr>
<tr>
<td>I</td>
<td>budget</td>
<td>sint32</td>
<td>available work budget (number of messages to be processed)</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">work done</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image27.png](cursor_tmp/flow_svgs/3_4_11.svg)

### 4.4.12 ipcsInstanceIsFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">determine if the instance is used or not</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static uint8 ipcsInstanceIsFree(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uint8</td>
<td colspan="2">IPC_SHM_INSTANCE_FREE if instance is free,</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image28.png](cursor_tmp/flow_svgs/3_4_12.svg)

### 4.4.13 ipcsShmRx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">shm Rx handler, called from softirq</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsShmRx(const uint8 instance, sint32 budget)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>budget</td>
<td>sint32</td>
<td>available work budget (number of messages to be processed)</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">work done</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image29.png](cursor_tmp/flow_svgs/3_4_13.svg)

### 4.4.14 ipcsBufPoolInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">init buffer pool</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsBufPoolInit(const uint8 instance, sint32 chan_id, sint32 pool_id, struct IPCS_SHM_POOL_ADDR_TYPE mng_pool, const struct IPCS_SHM_POOL_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="6">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel index</td>
</tr>
<tr>
<td>I</td>
<td>pool_id</td>
<td>sint32</td>
<td>pool index in channel</td>
</tr>
<tr>
<td>I</td>
<td>mng_pool</td>
<td>struct IPCS_SHM_POOL_ADDR_TYPE</td>
<td>源码参数</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_POOL_CFG_TYPE *</td>
<td>channel configuration parameters</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK for success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image30.png](cursor_tmp/flow_svgs/3_4_14.svg)

### 4.4.15 ipcsGetTotalBufPerChan

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get total buffers of an managed channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static uint32 ipcsGetTotalBufPerChan(const uint8 instance, sint32 chan_id, const struct IPCS_SHM_MANAGED_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel id</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_MANAGED_CFG_TYPE *</td>
<td>managed channel configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uint32</td>
<td colspan="2">total buffers, 0 if error</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image31.png](cursor_tmp/flow_svgs/3_4_15.svg)

### 4.4.16 managedChannelInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">initialize managed channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 managedChannelInit(const uint8 instance, sint32 chan_id, uintptr_t local_shm, uintptr_t remote_shm, const struct IPCS_SHM_MANAGED_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="6">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel id</td>
</tr>
<tr>
<td>I</td>
<td>local_shm</td>
<td>uintptr_t</td>
<td>local shared memory</td>
</tr>
<tr>
<td>I</td>
<td>remote_shm</td>
<td>uintptr_t</td>
<td>remote shared memort</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_MANAGED_CFG_TYPE *</td>
<td>managed channel configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK for success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image32.png](cursor_tmp/flow_svgs/3_4_16.svg)

### 4.4.17 unmanagedChannelInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">initialize unmanaged channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 unmanagedChannelInit(const uint8 instance, sint32 chan_id, uintptr_t local_shm, uintptr_t remote_shm, const struct IPCS_SHM_UNMANAGED_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="6">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel id</td>
</tr>
<tr>
<td>I</td>
<td>local_shm</td>
<td>uintptr_t</td>
<td>local shared memory</td>
</tr>
<tr>
<td>I</td>
<td>remote_shm</td>
<td>uintptr_t</td>
<td>remote shared memort</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_UNMANAGED_CFG_TYPE *</td>
<td>unmanaged channel configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK for success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image33.png](cursor_tmp/flow_svgs/3_4_17.svg)

### 4.4.18 ipcsShmInitChannel

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">initialize a shared memory IPC channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsShmInitChannel(const uint8 instance, sint32 chan_id, uintptr_t local_shm, uintptr_t remote_shm, const struct IPCS_SHM_CHANNEL_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="6">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel index</td>
</tr>
<tr>
<td>I</td>
<td>local_shm</td>
<td>uintptr_t</td>
<td>local channel shared memory address</td>
</tr>
<tr>
<td>I</td>
<td>remote_shm</td>
<td>uintptr_t</td>
<td>remote channel shared memory address</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CHANNEL_CFG_TYPE *</td>
<td>channel configuration parameters</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">0 for success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image34.png](cursor_tmp/flow_svgs/3_4_18.svg)

### 4.4.19 getChanMemmapSize

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Get channel local mapped memory size</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static uint32 getChanMemmapSize(const uint8 instance, sint32 chan_id)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>chan_id</td>
<td>sint32</td>
<td>channel id</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uint32</td>
<td colspan="2">Channel memory size</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image35.png](cursor_tmp/flow_svgs/3_4_19.svg)

### 4.4.20 ipcsShmInitChannels

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">initialize all shared memory IPC channel</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsShmInitChannels(uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>ipc-shm instance configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">0 for success, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image36.png](cursor_tmp/flow_svgs/3_4_20.svg)

### 4.4.21 ipcsShmInitInstance

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Initialize only one instance shared memory device</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint32 ipcsShmInitInstance(uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>uint8</td>
<td>instance id</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>ipc-shm instance configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image37.png](cursor_tmp/flow_svgs/3_4_21.svg)

### 4.4.22 findPoolForBuf

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_SHM</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Find the pool that owns the specified buffer.</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint16 findPoolForBuf(struct IPCS_MANAGED_CHANNEL_TYPE *chan, uintptr_t buf, sint32 remote)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>chan</td>
<td>struct IPCS_MANAGED_CHANNEL_TYPE *</td>
<td>managed channel pointer</td>
</tr>
<tr>
<td>I</td>
<td>buf</td>
<td>uintptr_t</td>
<td>buffer pointer</td>
</tr>
<tr>
<td>I</td>
<td>remote</td>
<td>sint32</td>
<td>flag telling if buffer is from remote OS</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint16</td>
<td colspan="2">pool index on success, -1 otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-shm.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image38.png](cursor_tmp/flow_svgs/3_4_22.svg)

### 4.4.23 ipcsMemcpy

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Core_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_CORE_UTIL</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsMemcpy(void *dst, const void *src, uint32 data_size)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>dst</td>
<td>void *</td>
<td>目的地址指针</td>
</tr>
<tr>
<td>I</td>
<td>src</td>
<td>const void *</td>
<td>源地址指针</td>
</tr>
<tr>
<td>I</td>
<td>data_size</td>
<td>uint32</td>
<td>复制数据大小，单位为 byte</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-util.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/ipcs_cores/ipc-util.h</td>
</tr>
</tbody>
</table>

processing flow

![image39.png](cursor_tmp/flow_svgs/3_4_23.svg)


## 4.5 Global variants 全局变量

本节仅列出 ipcs/ipcs_cores 内通信核心私有数据。RTOS/Linux 实现侧私有数据见第 5、6 章。

| 全局变量名称 | 全局变量类型 | 全局变量范围 | 全局变量描述 | 全局变量的存储RAM区 |
|---|---|---|---|---|
| ipc_shm_priv_data | static struct IPCS_SHM_PRIV_TYPE [IPC_SHM_MAX_INSTANCES] | ipcs/ipcs_cores/ipc-shm.c | IPCS shm private data | 源码未显式指定 |

## 4.6 Data Structure 类型定义

### 4.6.1 struct IPCS_RING_TYPE

| Type | Name | Description |
|---|---|---|
| uint64 | sentinel | a magic word to ensure ring integrity |
| volatile uint32 | write | write index, position used to store next byte in the buffer |
| volatile uint32 | read | read index, read next byte from this position |
| uint8 | data[] | circular buffer |

### 4.6.2 struct IPCS_QUEUE_TYPE

| Type | Name | Description |
|---|---|---|
| uint16 | elem_num | number of elements in queue |
| uint8 | elem_size | element size in bytes (8-byte multiple) |
| struct IPCS_RING_TYPE | *push_ring | push buffer ring mapped in local shared memory |
| struct IPCS_RING_TYPE | *pop_ring | pop buffer ring mapped in remote shared memory |

### 4.6.3 enum IPCS_SHM_INSTANCE_STATE_E

| Name | Description |
|---|---|
| IPC_SHM_INSTANCE_USED | instance is used |
| IPC_SHM_INSTANCE_FREE | instance is free and can be used |
| IPC_SHM_INSTANCE_ERROR | there are some errors |

### 4.6.4 struct IPCS_SHM_POOL_ADDR_TYPE

| Type | Name | Description |
|---|---|---|
| uintptr_t | local_pool_shm | address of local buffer pool |
| uintptr_t | remote_pool_shm | address of remote buffer pool |

### 4.6.5 struct IPCS_SHM_BD_TYPE

| Type | Name | Description |
|---|---|---|
| sint16 | pool_id | index of buffer pool |
| uint16 | buf_id | index of buffer from buffer pool |
| uint32 | data_size | size of data written in buffer |

### 4.6.6 struct IPCS_SHM_POOL_TYPE

| Type | Name | Description |
|---|---|---|
| uint16 | num_bufs | number of buffers in pool |
| uint32 | buf_size | size of buffers |
| uint32 | shm_size | size of shared memory mapped by this pool (queue + bufs) |
| uintptr_t | local_pool_addr | address of local buffer pool |
| uintptr_t | remote_pool_addr | address of remote buffer pool |
| struct IPCS_QUEUE_TYPE | bd_queue | queue containing BDs of free buffers |

### 4.6.7 struct IPCS_MANAGED_CHANNEL_TYPE

| Type | Name | Description |
|---|---|---|
| struct IPCS_QUEUE_TYPE | bd_queue | queue containing BDs of sent/received buffers |
| uint8 | num_pools | number of buffer pools |
| struct IPCS_SHM_POOL_TYPE | pools[IPC_SHM_MAX_POOLS] | buffer pools private data |
| void (rx_cb)(void cb_arg, const uint8 instance, sint32 chan_id, void *buf, uint32 size) | rx_cb | receive callback |
| void | *cb_arg | optional receive callback argument |

### 4.6.8 struct IPCS_CHANNEL_UMEM_TYPE

| Type | Name | Description |
|---|---|---|
| uint32 | sentinel | magic word to ensure unmanaged channel integrity |
| volatile uint32 | tx_count | local channel Tx counter (it wraps around at max uint32) |
| uint8 | mem[] | local channel unmanaged memory buffer |

### 4.6.9 struct IPCS_UNMANAGED_CHANNEL_TYPE

| Type | Name | Description |
|---|---|---|
| uint32 | size | unmanaged channel memory size requested by app |
| struct IPCS_CHANNEL_UMEM_TYPE | *local_mem | 源码未提供描述 |
| struct IPCS_CHANNEL_UMEM_TYPE | *remote_mem | 源码未提供描述 |
| uint32 | remote_tx_count | copy of remote Tx counter |
| void (rx_cb)(void cb_arg, const uint8 instance, sint32 chan_id, void *buf) | rx_cb | receive callback |
| void | *cb_arg | optional receive callback argument |

### 4.6.10 struct IPCS_SHM_CHANNEL_TYPE

| Type | Name | Description |
|---|---|---|
| sint32 | id | channel id |
| enum IPCS_SHM_CHANNEL_TYPE_E | type | channel type (see IPCS_SHM_CHANNEL_TYPE_E) |
| struct IPCS_MANAGED_CHANNEL_TYPE | ch.mng | 源码未提供描述 |
| struct IPCS_UNMANAGED_CHANNEL_TYPE | ch.umng | 源码未提供描述 |

### 4.6.11 struct IPCS_SHM_GLOBAL_TYPE

| Type | Name | Description |
|---|---|---|
| uint64 | state | state to indicate whether local is initialized |

### 4.6.12 struct IPCS_SHM_PRIV_TYPE

| Type | Name | Description |
|---|---|---|
| uint32 | shm_size | local/remote shared memory size |
| uint8 | num_channels | number of shared memory channels |
| struct IPCS_SHM_CHANNEL_TYPE | channels[IPC_SHM_MAX_CHANNELS] | ipc channels private data |
| struct IPCS_SHM_GLOBAL_TYPE | *global | local global data shared with remote |

### 4.6.13 enum IPCS_SHM_CHANNEL_TYPE_E

| Name | Description |
|---|---|
| IPC_SHM_MANAGED | channel with buffer management enabled |
| IPC_SHM_UNMANAGED | buf mgmt disabled, app owns entire channel memory |

### 4.6.14 enum IPCS_SHM_CORE_TYPE_E

| Name | Description |
|---|---|
| IPC_CORE_DEFAULT | used for letting driver auto-select remote core type |
| IPC_CORE_A53 | ARM Cortex-A53 core |
| IPC_CORE_M7 | ARM Cortex-M7 core |
| IPC_CORE_M4 | ARM Cortex-M4 core |
| IPC_CORE_Z7 | PowerPC e200z7 core |
| IPC_CORE_Z4 | PowerPC e200z4 core |
| IPC_CORE_Z2 | PowerPC e200z2 core |
| IPC_CORE_R52 | ARM Cortex-R52 core |
| IPC_CORE_M33 | ARM Cortex-M33 core |
| IPC_CORE_BBE32 | Tensilica ConnX BBE32EP core |

### 4.6.15 enum IPCS_SHM_CORE_INDEX_E

| Name | Description |
|---|---|
| IPC_CORE_INDEX_0 | Processor index 0 |
| IPC_CORE_INDEX_1 | Processor index 1 |
| IPC_CORE_INDEX_2 | Processor index 2 |
| IPC_CORE_INDEX_3 | Processor index 3 |
| IPC_CORE_INDEX_4 | Processor index 4 |
| IPC_CORE_INDEX_5 | Processor index 5 |
| IPC_CORE_INDEX_6 | Processor index 6 |
| IPC_CORE_INDEX_7 | Processor index 7 |

### 4.6.16 struct IPCS_SHM_POOL_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| uint16 | num_bufs | number of buffers |
| uint32 | buf_size | buffer size |

### 4.6.17 struct IPCS_SHM_MANAGED_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| uint8 | num_pools | number of buffer pools |
| struct IPCS_SHM_POOL_CFG_TYPE | *pools | memory buffer pools parameters |
| void (rx_cb)(void cb_arg, const uint8 instance, sint32 chan_id, void *buf, uint32 size) | rx_cb | receive callback |
| void | *cb_arg | optional receive callback argument |

### 4.6.18 struct IPCS_SHM_UNMANAGED_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| uint32 | size | unmanaged channel memory size |
| void (rx_cb)(void cb_arg, const uint8 instance, sint32 chan_id, void *mem) | rx_cb | receive callback |
| void | *cb_arg | optional receive callback argument |

### 4.6.19 struct IPCS_SHM_CHANNEL_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| enum IPCS_SHM_CHANNEL_TYPE_E | type | channel type from &amp;enum IPCS_SHM_CHANNEL_TYPE_E |
| struct IPCS_SHM_MANAGED_CFG_TYPE | ch.managed | 源码未提供描述 |
| struct IPCS_SHM_UNMANAGED_CFG_TYPE | ch.unmanaged | 源码未提供描述 |

### 4.6.20 struct IPCS_SHM_REMOTE_CORE_TYPE

| Type | Name | Description |
|---|---|---|
| enum IPCS_SHM_CORE_TYPE_E | type | core type from &amp;enum IPCS_SHM_CORE_TYPE_E |
| enum IPCS_SHM_CORE_INDEX_E | index | core number |

### 4.6.21 struct IPCS_SHM_LOCAL_CORE_TYPE

| Type | Name | Description |
|---|---|---|
| enum IPCS_SHM_CORE_TYPE_E | type | core type from &amp;enum IPCS_SHM_CORE_TYPE_E |
| enum IPCS_SHM_CORE_INDEX_E | index | core number targeted by remote core interrupt |
| uint32 | trusted | trusted cores mask |

### 4.6.22 struct IPCS_SHM_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| uintptr_t | local_shm_addr | local shared memory physical address |
| uintptr_t | remote_shm_addr | remote shared memory physical address |
| uint32 | shm_size | local/remote shared memory size |
| sint32 | inter_core_tx_irq | inter-core interrupt reserved for shm driver Tx |
| sint32 | inter_core_rx_irq | inter-core interrupt reserved for shm driver Rx |
| uint8 | mru_tx_channel_id | mru channel index for shm driver Tx |
| uint8 | mru_rx_channel_id | mru channel index for shm driver Rx |
| struct IPCS_SHM_LOCAL_CORE_TYPE | local_core | local core targeted by remote core interrupt |
| struct IPCS_SHM_REMOTE_CORE_TYPE | remote_core | remote core to trigger the interrupt on |
| uint8 | num_channels | number of shared memory channels |
| struct IPCS_SHM_CHANNEL_CFG_TYPE * | channels | IPC channels parameters array |
| ISRType | isr_id_handler | the name of OsIsr defined to handle the interrupt |

### 4.6.23 struct IPCS_SHM_INSTANCES_CFG_TYPE

| Type | Name | Description |
|---|---|---|
| uint8 | num_instances | number of shared memory instances |
| struct IPCS_SHM_CFG_TYPE | *shm_cfg | IPC shm parameters array |


## 4.7 Dynamic Detailed Design 动态详细设计

本节描述与部署变体无关的 **逻辑** 数据路径（Core + Queue）。变体相关的 OSAL/HAL/跨边界路径见第 4.7、5.7 节。

### 4.7.1 初始化流程

按架构：应用调用 ipcsShmInit → 逐 instance 调用 HAL 初始化、OSAL 初始化、channel 初始化（具体 HAL/OSAL 实现见第 4/5 章）。

### 4.7.2 Managed 发送流程

ipcsShmAcquireBuf → 填充数据 → ipcsShmTx → queue push BD → HAL 通知远端。

### 4.7.3 Managed 接收与释放流程

OSAL 触发 ipcsShmRx → ipcsChannelRx → 应用回调 → ipcsShmReleaseBuf。

### 4.7.4 Unmanaged 发送与接收流程

ipcsShmUnmanagedAcquire / ipcsShmUnmanagedTx；接收侧检查 tx_count。

### 4.7.5 中断与轮询流程

OSAL 注册 hardirq/softirq 或 polling（ipcsShmPollChannels）；Core 按预算分发 channel。

# 5 RTOS 部署变体详细设计

## 5.1 总述

RTOS 部署变体在 **单地址空间** 内完整实现 Drv_Ipcs_Osal_Cmp 与 Drv_Ipcs_Hal_Cmp。OS 实现三选一：FreeRTOS、ThreadX、AUTOSAR OS。HAL 平台代码位于 ipcs/mcu/hw/，由三种实现共用。

## 5.2 Files 与依赖

### 5.2.1 ipc-hw-platform.h

描述：RTOS 部署变体 HAL 平台寄存器与 MSCM 定义；与具体 OS 实现（FreeRTOS/ThreadX/AUTOSAR OS）无关，由 ipcs/mcu/hw/ 共用。

#### 文件私有数据（RTOS）

| 全局变量名称 | 全局变量类型 | 全局变量范围 | 全局变量描述 | 全局变量的存储RAM区 |
|---|---|---|---|---|
| ipc_shm_priv_data | static struct IPCS_SHM_PRIV_TYPE [IPC_SHM_MAX_INSTANCES] | ipcs/ipcs_cores/ipc-shm.c | IPCS shm private data | 源码未显式指定 |
| ipc_hw_priv | static struct IPCS_HW_PRIV_TYPE_TYPE [IPC_SHM_MAX_INSTANCES] | ipcs/mcu/hw/ipc-hw.c | platform specific private data | 源码未显式指定 |
| ipc_os_priv | static struct IPCS_OS_PRIV_TYPE_TYPE | ipcs/mcu/os/autosar/ipc-os-autosar.c | AutoSAR OS specific private data | 源码未显式指定 |
| ipc_os_priv | static struct IPCS_OS_PRIV_TYPE_TYPE | ipcs/mcu/os/freertos/ipc-os-freertos.c | FreeRTOS OS specific private data | 源码未显式指定 |
| ipc_os_priv | static struct IPCS_OS_PRIV_TYPE_TYPE | ipcs/mcu/os/threadx/ipc-os-threadx.c | Threadx OS specific private data | 源码未显式指定 |
| softirq_stack | K_THREAD_STACK_DEFINE(softirq_stack, IPC_SOFTIRQ_STACK_SIZE) | ipcs/mcu/os/threadx/ipc-os-threadx.c | Threadx deferred interrupt handler stack | 源码未显式指定 |

#### 文件列表（RTOS MCU）

### 5.2.0 RTOS 文件列表

| 组件 | 文件 |
|---|---|
| Drv_Ipcs_Hal_Cmp / 平台定义 | ipcs/mcu/hw/ipc-hw-platform.h |
| Drv_Ipcs_Hal_Cmp / IPCS-HAL | ipcs/mcu/hw/ipc-hw.c |
| Drv_Ipcs_Hal_Cmp / IPCS-HAL | ipcs/mcu/hw/ipc-hw.h |
| Drv_Ipcs_Osal_Cmp / AUTOSAR OS 实现 | ipcs/mcu/os/autosar/ipc-os-autosar.c |
| Drv_Ipcs_Osal_Cmp / FreeRTOS 实现 | ipcs/mcu/os/freertos/ipc-os-freertos.c |
| Drv_Ipcs_Osal_Cmp / IPCS-OSAL | ipcs/mcu/os/ipc-os.h |
| Drv_Ipcs_Osal_Cmp / ThreadX 实现 | ipcs/mcu/os/threadx/ipc-os-threadx.c |

### 5.2.1 ipc-hw-platform.h（文件依赖详述）

描述：

> ipcs/mcu/hw/ipc-hw-platform.h 属于 Drv_Ipcs_Hal_Cmp / 平台定义。

依赖关系：

当定义 S32G3XX 时：S32G399A_M7_COMMON.h, S32G399A_SCB.h, S32G399A_MSCM.h（与 ipcs/mcu/hw/ipc-hw-platform.h 一致）

![image40.png](cursor_tmp/flow_svgs/3_4_23.svg)

### 5.2.2 ipc-hw.c

描述：

> ipcs/mcu/hw/ipc-hw.c 属于 Drv_Ipcs_Hal_Cmp / IPCS-HAL。

依赖关系：

ipc-shm.h, ipc-os.h, ipc-hw.h, ipc-hw-platform.h（与 ipcs/mcu/hw/ipc-hw.c 中 #include 一致）

![image41.png](cursor_tmp/files_32_svgs/3_2_10.svg)

### 5.2.3 ipc-hw.h

描述：

> ipcs/mcu/hw/ipc-hw.h 属于 Drv_Ipcs_Hal_Cmp / IPCS-HAL。

依赖关系：

本头文件未 #include 其他头文件（仅声明 HAL API）。

![image42.png](cursor_tmp/files_32_svgs/3_2_11.svg)

### 5.2.4 ipc-shm-rtos.mk

描述：

> ipc-shm-rtos.mk 属于 构建集成。

### 5.2.5 ipc-os-autosar.c

描述：

> ipcs/mcu/os/autosar/ipc-os-autosar.c 属于 Drv_Ipcs_Osal_Cmp / AUTOSAR OS 实现。

依赖关系：

<Os.h>, ipc-shm.h, ipc-os.h, ipc-hw.h（与 ipcs/mcu/os/autosar/ipc-os-autosar.c 中 #include 顺序一致）

![image43.png](cursor_tmp/files_32_svgs/3_2_13.svg)

### 5.2.6 ipc-os-freertos.c

描述：

> ipcs/mcu/os/freertos/ipc-os-freertos.c 属于 Drv_Ipcs_Osal_Cmp / FreeRTOS 实现。

依赖关系：

ipc-shm.h, ipc-os.h, ipc-hw.h, FreeRTOS.h, task.h（与 ipcs/mcu/os/freertos/ipc-os-freertos.c 一致）

![image45.png](cursor_tmp/files_32_svgs/3_2_14.svg)

### 5.2.7 ipc-os.h

描述：

> ipcs/mcu/os/ipc-os.h 属于 Drv_Ipcs_Osal_Cmp / IPCS-OSAL。

依赖关系：

本头文件未 #include 其他头文件（仅 OSAL 宏与 API 声明）。

![image46.png](cursor_tmp/files_32_svgs/3_2_16.svg)

### 5.2.8 ipc-os-threadx.c

描述：

> ipcs/mcu/os/threadx/ipc-os-threadx.c 属于 Drv_Ipcs_Osal_Cmp / ThreadX 实现。

依赖关系：

ipc-shm.h, ipc-os.h, ipc-hw.h, <threadx/sys/mem_manage.h>, <threadx/kernel.h>, <threadx/device.h>；当定义 S32ZE 时另含 Mru_Ip.h（见 ipcs/mcu/os/threadx/ipc-os-threadx.c 条件编译）

![image47.png](cursor_tmp/files_32_svgs/3_2_16.svg)

## 5.6 HAL 单元设计（MCU 共用）

本节严格按照 reference.md 的内部函数表格格式描述内部函数。除 3.3 中列出的 9 个对外接口之外，其余源码函数、跨组件调用接口和 OS task 单元均作为内部接口。

### 5.6.1 ipcsHwGetCoreIndexM7

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Validate and get core index if core type is m7</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwGetCoreIndexM7(uint8 index)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>index</td>
<td>uint8</td>
<td>core 或 IRQ 配置索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">core_index if core type is m7</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image48.png](cursor_tmp/flow_svgs/3_4_24.svg)

### 5.6.2 ipcsHwGetCoreIndexA53

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Validate and get core index if core type is a53</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwGetCoreIndexA53(uint8 index)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>index</td>
<td>uint8</td>
<td>core 或 IRQ 配置索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">core_index if core type is a53</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image49.png](cursor_tmp/flow_svgs/3_4_25.svg)

### 5.6.3 ipcsHwSetRemoteCore

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get remote core for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetRemoteCore(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid core</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image50.png](cursor_tmp/flow_svgs/3_4_26.svg)

### 5.6.4 ipcsHwSetLocalCore

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get local core for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetLocalCore(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid core</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image51.png](cursor_tmp/flow_svgs/3_4_27.svg)

### 5.6.5 ipcsHwSetCore

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get local and remote core for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetCore(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid core</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image52.png](cursor_tmp/flow_svgs/3_4_28.svg)

### 5.6.6 ipcsHwSetTxIrqIdx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get tx irq and msi index for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetTxIrqIdx(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid interrupt</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image53.png](cursor_tmp/flow_svgs/3_4_29.svg)

### 5.6.7 ipcsHwSetRxIrqIdx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get rx irq and msi index for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetRxIrqIdx(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid interrupt</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image54.png](cursor_tmp/flow_svgs/3_4_30.svg)

### 5.6.8 ipcsHwSetIrqIdx

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get irq and msi index for platform private data</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static sint8 ipcsHwSetIrqIdx(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>:     Local core type from ipcf configuration</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for invalid interrupt</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image55.png](cursor_tmp/flow_svgs/3_4_31.svg)

### 5.6.9 ipcsHwInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">platform specific initialization</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint8 ipcsHwInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>configuration parameters</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint8</td>
<td colspan="2">IPC_SHM_E_OK for success, -IPC_SHM_E_INVAL for either inter core</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image56.png](cursor_tmp/flow_svgs/3_4_32.svg)

### 5.6.10 ipcsHwFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">free hw resources</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwFree(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image57.png](cursor_tmp/flow_svgs/3_4_33.svg)

### 5.6.11 ipcsHwIrqEnable

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">enable notifications from remote</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwIrqEnable(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image58.png](cursor_tmp/flow_svgs/3_4_34.svg)

### 5.6.12 ipcsHwIrqDisable

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">disable notifications from remote</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwIrqDisable(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image59.png](cursor_tmp/flow_svgs/3_4_35.svg)

### 5.6.13 ipcsHwIrqNotify

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">notify remote that data is available</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwIrqNotify(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image60.png](cursor_tmp/flow_svgs/3_4_36.svg)

### 5.6.14 ipcsHwIrqClear

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">clear available data notification</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwIrqClear(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image61.png](cursor_tmp/flow_svgs/3_4_37.svg)

### 5.6.15 ipcsHwFlushCache

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static void ipcsHwFlushCache(uint32 data_addr, uint32 data_size)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="3">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>data_addr</td>
<td>uint32</td>
<td>源码参数</td>
</tr>
<tr>
<td>I</td>
<td>data_size</td>
<td>uint32</td>
<td>复制数据大小，单位为 byte</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">void</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image62.png](cursor_tmp/flow_svgs/3_4_38.svg)

### 5.6.16 ipcsHwFlushCacheLocal

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Clear and invalidate cache content</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwFlushCacheLocal(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image63.png](cursor_tmp/flow_svgs/3_4_39.svg)

### 5.6.17 ipcsHwFlushCacheRemote

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Hal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_HAL_MCU</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">Clear and invalidate cache content</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsHwFlushCacheRemote(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>instance id</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/hw/ipc-hw.h</td>
</tr>
</tbody>
</table>

processing flow

![image64.png](cursor_tmp/flow_svgs/3_4_40.svg)

### 4.6.24 enum IPCS_PROCESSOR_IDX_E

| Name | Description |
|---|---|
| IPC_A53_0 |  |
| IPC_A53_1 |  |
| IPC_A53_2 |  |
| IPC_A53_3 |  |
| IPC_M7_0 |  |
| IPC_M7_1 |  |
| IPC_M7_2 |  |
| IPC_M7_3 |  |
| IPC_A53_4 |  |
| IPC_A53_5 |  |
| IPC_A53_6 |  |
| IPC_A53_7 |  |

## 5.3 AUTOSAR OS 实现

### 4.4.41 ipcsOsInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">OS specific initialization code</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg, sint32 (*rx_cb)(const uint8, sint32))</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>rx_cb</td>
<td>sint32 (*rx_cb)(const uint8, sint32)</td>
<td>rx callback to be called from rx softirq</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, -IPC_SHM_E_NOTSUP if softirq task not in</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image65.png](cursor_tmp/flow_svgs/3_4_41.svg)

### 4.4.42 ipcsOsFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">free OS specific resources</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsOsFree(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image66.png](cursor_tmp/flow_svgs/3_4_42.svg)

### 4.4.43 ipcsShmSoftirq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">task acting as deferred interrupt handler</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">TASK(ipcsShmSoftirq)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image67.png](cursor_tmp/flow_svgs/3_4_43.svg)

### 4.4.44 ipcsShmHardirq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">driver interrupt service routine</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmHardirq(void)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image68.png](cursor_tmp/flow_svgs/3_4_44.svg)

### 4.4.45 ipcsShmHardirqInstance

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">driver interrupt service routine</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmHardirqInstance(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image69.png](cursor_tmp/flow_svgs/3_4_45.svg)

### 4.4.46 ipcsOsGetLocalShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get local shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetLocalShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image70.png](cursor_tmp/flow_svgs/3_4_46.svg)

### 4.4.47 ipcsOsGetRemoteShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get remote shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetRemoteShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image71.png](cursor_tmp/flow_svgs/3_4_47.svg)

### 4.4.48 ipcsOsPollChannels

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_AUTOSAR</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">invoke rx callback configured at initialization</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsPollChannels(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">work done, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/autosar/ipc-os-autosar.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image72.png](cursor_tmp/flow_svgs/3_4_48.svg)

### 4.6.25 enum msg_receive

| Name | Description |
|---|---|
| MSG_NOT_RECEIVED | no new message received from the remote core |
| MSG_IS_RECEIVED | new message received from the remote core |

### 4.6.26 struct IPCS_OS_PRIV_INSTANCE_TYPE

| Type | Name | Description |
|---|---|---|
| uintptr_t | local_shm | local shared memory address |
| uintptr_t | remote_shm | remote shared memory address |
| sint32 | state | state to indicate whether instance is initialized |
| sint32 | rx_irq_num | rx interrupt number |
| sint32 | msg_received | state to indicate notification received for a new message |
| ISRType | isr_id_handler | the name of OsIsr defined to handle the interrupt |
| sint32 (*rx_cb)(const uint8 instance, sint32 budget) | rx_cb | upper layer rx callback |

### 4.6.27 struct IPCS_OS_PRIV_TYPE_TYPE

| Type | Name | Description |
|---|---|---|
| struct IPCS_OS_PRIV_INSTANCE_TYPE | id[IPC_SHM_MAX_INSTANCES] | 源码未提供描述 |
| sint32 | task_is_initialized | flag to know if the softirq task is initialized |

## 5.4 FreeRTOS 实现

### 4.4.49 ipcsOsInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">OS specific initialization code</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg, sint32 (*rx_cb)(const uint8, sint32))</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>rx_cb</td>
<td>sint32 (*rx_cb)(const uint8, sint32)</td>
<td>rx callback to be called from rx softirq</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, -IPC_SHM_E_NOMEM if the softirq task creation</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image73.png](cursor_tmp/flow_svgs/3_4_49.svg)

### 4.4.50 ipcsOsFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">free OS specific resources</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsOsFree(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image74.png](cursor_tmp/flow_svgs/3_4_50.svg)

### 4.4.58 ipcsShmSoftirq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">task acting as deferred interrupt handler</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static void ipcsShmSoftirq(void)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">void</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![image75.png](cursor_tmp/flow_svgs/3_4_58.svg)

### 4.4.51 ipcsShmHardirq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">driver interrupt service routine</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmHardirq(void)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image76.png](cursor_tmp/flow_svgs/3_4_51.svg)

### 4.4.52 ipcsShmHardirqInstance

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">driver interrupt service routine</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmHardirqInstance(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image77.png](cursor_tmp/flow_svgs/3_4_52.svg)

### 4.4.53 ipcsOsGetLocalShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get local shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetLocalShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image78.png](cursor_tmp/flow_svgs/3_4_53.svg)

### 4.4.54 ipcsOsGetRemoteShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get remote shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetRemoteShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">源码返回值</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image79.png](cursor_tmp/flow_svgs/3_4_54.svg)

### 4.4.55 ipcsOsPollChannels

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_FREERTOS</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">invoke rx callback configured at initialization</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsPollChannels(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">work done, error code otherwise</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/freertos/ipc-os-freertos.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![image80.png](cursor_tmp/flow_svgs/3_4_55.svg)

### 4.6.30 enum msg_receive

| Name | Description |
|---|---|
| MSG_NOT_RECEIVED | no new message received from the remote core |
| MSG_IS_RECEIVED | new message received from the remote core |

### 4.6.31 struct IPCS_OS_PRIV_INSTANCE_TYPE

| Type | Name | Description |
|---|---|---|
| uintptr_t | local_shm | local shared memory address |
| uintptr_t | remote_shm | remote shared memory address |
| sint32 | state | state of instance |
| sint32 | rx_irq_num | rx interrupt number |
| sint32 | msg_received | state to indicate notification received for a new message |

### 4.6.32 struct IPCS_OS_PRIV_TYPE_TYPE

| Type | Name | Description |
|---|---|---|
| struct IPCS_OS_PRIV_INSTANCE_TYPE | id[IPC_SHM_MAX_INSTANCES] | private data per instance |
| sint32 (*rx_cb)(const uint8 instance, sint32 budget) | rx_cb | upper layer rx callback |
| TaskHandle_t | softirq_handle | rx task handle used by the ISR to notify the rx task |
| sint32 | task_is_initialized | flag to know if the softirq task is initialized |

## 5.5 ThreadX 实现

### 4.4.56 ipcsOsInit

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">OS specific initialization code. When inter_core_rx_irq is disabled by passing IPC_IRQ_NONE, the softirq task will not be created.</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsInit(const uint8 instance, const struct IPCS_SHM_CFG_TYPE *cfg, sint32 (*rx_cb)(const uint8 instance, sint32 budget))</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="4">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td>I</td>
<td>cfg</td>
<td>const struct IPCS_SHM_CFG_TYPE *</td>
<td>configuration parameters</td>
</tr>
<tr>
<td>I</td>
<td>rx_cb</td>
<td>sint32 (*rx_cb)(const uint8 instance, sint32 budget)</td>
<td>rx callback to be called from rx softirq</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">IPC_SHM_E_OK on success, -IPC_SHM_E_NOMEM if softirq task or event flags creation failed, -IPC_SHM_E_INVAL for invalid rx_cb or cfg</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.56 ipcsOsInit processing flow](cursor_tmp/flow_svgs/tx_3_4_56.svg)

### 4.4.57 ipcsOsFree

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">free OS specific resources</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsOsFree(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.57 ipcsOsFree processing flow](cursor_tmp/flow_svgs/tx_3_4_57.svg)

### 4.4.58 ipcsShmSoftIrq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">task acting as deferred interrupt handler. Waits on event flags, calls upper layer rx callback registered with ipcsOsInit(), re-enables IRQ when work is done. Terminates when ipcsOsFree() sets quit request.</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">static void ipcsShmSoftIrq(uint32 ulInput)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>ulInput</td>
<td>uint32</td>
<td>ThreadX thread entry parameter (unused)</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">void</td>
<td colspan="2">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">-</td>
</tr>
</tbody>
</table>

processing flow

![3.4.58 ipcsShmSoftIrq processing flow](cursor_tmp/flow_svgs/tx_3_4_58.svg)

### 4.4.59 ipcsShmHardIrq

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">driver interrupt service routine</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">void ipcsShmHardIrq(void)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="4">-</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.59 ipcsShmHardIrq processing flow](cursor_tmp/flow_svgs/tx_3_4_59.svg)

### 4.4.61 ipcsOsGetLocalShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get local shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetLocalShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">local shared memory address for instance</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.61 ipcsOsGetLocalShm processing flow](cursor_tmp/flow_svgs/tx_3_4_61.svg)

### 4.4.62 ipcsOsGetRemoteShm

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">get remote shared mem address</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">uintptr_t ipcsOsGetRemoteShm(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">uintptr_t</td>
<td colspan="2">remote shared memory address for instance</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.62 ipcsOsGetRemoteShm processing flow](cursor_tmp/flow_svgs/tx_3_4_62.svg)

### 4.4.63 ipcsOsPollChannels

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr>
<td>对应软件架构ID</td>
<td colspan="4">Drv_Ipcs_Osal_Cmp</td>
</tr>
<tr>
<td>软件单元 ID</td>
<td colspan="4">SWU_IPCS_OSAL_THREADX</td>
</tr>
<tr>
<td>函数说明</td>
<td colspan="4">invoke rx callback configured at initialization. The softirq task handles rx operation when rx interrupt is configured.</td>
</tr>
<tr>
<td>函数原型</td>
<td colspan="4">sint32 ipcsOsPollChannels(const uint8 instance)</td>
</tr>
<tr>
<td>制约条件</td>
<td colspan="4">-</td>
</tr>
<tr>
<td rowspan="2">输入/输出参数</td>
<td>I/O</td>
<td>参数名</td>
<td>数据类型</td>
<td>说明</td>
</tr>
<tr>
<td>I</td>
<td>instance</td>
<td>const uint8</td>
<td>IPCS shared memory instance 索引</td>
</tr>
<tr>
<td rowspan="2">返回值</td>
<td colspan="2">数据类型</td>
<td colspan="2">说明</td>
</tr>
<tr>
<td colspan="2">sint32</td>
<td colspan="2">work done when rx_irq is IPC_IRQ_NONE; IPC_SHM_E_OK if rx_irq configured but callback not invoked; -IPC_SHM_E_INVAL when rx interrupt is configured</td>
</tr>
<tr>
<td>函数定义文件</td>
<td colspan="4">ipcs/mcu/os/threadx/ipc-os-threadx.c</td>
</tr>
<tr>
<td>函数声明文件</td>
<td colspan="4">ipcs/mcu/os/ipc-os.h</td>
</tr>
</tbody>
</table>

processing flow

![3.4.63 ipcsOsPollChannels processing flow](cursor_tmp/flow_svgs/tx_3_4_63.svg)

### 4.6.35 struct IPCS_OS_PRIV_INSTANCE_TYPE

| Type | Name | Description |
|---|---|---|
| uintptr_t | local_shm | local shared memory address |
| uintptr_t | remote_shm | remote shared memory address |
| sint32 | state | state of instance |
| sint32 | rx_irq_num | rx interrupt number |
| sint32 (*rx_callback)(const uint8 instance, sint32 budget) | rx_callback | upper layer rx callback |

### 4.6.36 struct IPCS_OS_PRIV_TYPE_TYPE

| Type | Name | Description |
|---|---|---|
| IPC_OS_PRIV_INSTANCE_T | id[IPC_SHM_MAX_INSTANCES] | private data per instance |
| TX_EVENT_FLAGS_GROUP | soft_irq_events | event flags for softirq task signaling |
| uint8 | ipc_soft_irq_stack[IPC_SOFTIRQ_STACK_SIZE] | softirq thread stack |
| TX_THREAD | soft_irq_handle | rx softirq thread handle |
| sint32 | task_is_initialized | flag to know if the softirq task is initialized |

## 5.7 RTOS 动态详细设计

第 4 章各函数已给出单函数 processing flow（活动图）。本节描述 **跨软件单元** 的动态交互，采用 UML 序列图；纵轴生命线为软件单元 ID（见 §2.1），颜色与分层一致：Core/Queue 为浅蓝、OSAL 为浅绿、HAL 为淡卡其、远端核为浅紫。

| 场景 ID | 场景名称 | 涉及软件单元 | 源码依据 |
|---|---|---|---|
| RTOS-S01 | 初始化 | CORE_SHM、HAL_MCU、OSAL_THREADX、CORE_QUEUE | `ipcsShmInit` → `ipcsHwInit` → `ipcsOsInit` → `ipcsShmInitChannels` |
| RTOS-S02 | Managed 发送 | CORE_SHM、CORE_QUEUE、HAL_MCU | `ipcsShmTx` → `ipcsQueuePush` → `ipcsHwIrqNotify` |
| RTOS-S03 | Managed 接收 | HAL_MCU、OSAL_THREADX、CORE_SHM、CORE_QUEUE | `ipcsShmHardIrq` → softirq → `ipcsShmRx` |
| RTOS-S04 | Unmanaged 收发 | CORE_SHM、HAL_MCU | `ipcsShmUnmanagedTx` / 对端 `tx_count` 比对 |
| RTOS-S05 | 中断与轮询 | CORE_SHM、OSAL_THREADX、HAL_MCU | IRQ 路径 vs `ipcsShmPollChannels` |

> 以下 OSAL 交互以 **ThreadX 实现**（`SWU_IPCS_OSAL_THREADX`）为例；FreeRTOS、AUTOSAR OS 实现与 Core/HAL 的契约相同，仅 OS 原语不同。

### 5.7.1 初始化（RTOS-S01）

sequence diagram

![RTOS initialization sequence](cursor_tmp/flow_svgs/rtos_seq_init.svg)

### 5.7.2 Managed 发送（RTOS-S02）

sequence diagram

![RTOS managed transmit sequence](cursor_tmp/flow_svgs/rtos_seq_tx_managed.svg)

### 5.7.3 Managed 接收（RTOS-S03）

sequence diagram

![RTOS managed receive sequence](cursor_tmp/flow_svgs/rtos_seq_rx_managed.svg)

### 5.7.4 Unmanaged 收发（RTOS-S04）

sequence diagram

![RTOS unmanaged sequence](cursor_tmp/flow_svgs/rtos_seq_unmanaged.svg)

### 5.7.5 中断与轮询（RTOS-S05）

sequence diagram

![RTOS IRQ and polling sequence](cursor_tmp/flow_svgs/rtos_seq_irq_poll.svg)


# 6 Linux 部署变体详细设计

## 6.1 总述

本章描述 `ipcs/mpu` 中 Linux 部署变体的详细设计。UIO 与 CDEV 采用用户侧代理加内核 Backend 的形态；全内核实现不使用用户侧代理，OSAL 与 HAL 均在内核模块中运行。

## 6.2 源码与构建结构

| 部件 | 路径 | 产物 / 角色 |
|---|---|---|
| 通信核心（共享） | `ipcs/ipcs_cores/` | 用户库或内核模块共用 Core |
| UIO 用户侧代理 | `ipcs/mpu/os_uio/ipc-os.c` | 用户库，满足 OSAL/HAL 契约并转发到 UIO Backend |
| CDEV 用户侧代理 | `ipcs/mpu/os_cdev/ipc-os.c` | 用户库，满足 OSAL/HAL 契约并转发到 CDEV Backend |
| UIO 内核 Backend | `ipcs/mpu/os_kernel/ipc-uio.c` | UIO 平台驱动与初始 cdev 通道 |
| CDEV 内核 Backend | `ipcs/mpu/os_kernel/ipc-cdev.c` | 字符设备、ioctl、wait queue 与 ISR |
| 全内核 OSAL | `ipcs/mpu/os_kernel/ipc-os.c` | 全内核实现的 OSAL |
| Linux HAL | `ipcs/mpu/hw/c1/ipc-hw.c` | MSCM/IRQ 硬件操作 |

## 6.3 全内核实现函数设计

全内核实现由 `ipcs/mpu/os_kernel/ipc-os.c` 与 `ipcs/mpu/hw/c1/ipc-hw.c` 构成，无用户侧代理。

### 6.3.0 全内核 OSAL 单元函数

### 6.3.1 ipcsShmSoftirq

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 延迟收包处理，遍历实例并调用上层 rx_cb，完成后重新使能 IRQ。 |
| 函数原型 | `static void ipcsShmSoftirq(unsigned long arg)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `arg`: `unsigned long arg` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.1 ipcsShmSoftirq processing flow](cursor_tmp/flow_svgs/linux_6_3_1_ipcsShmSoftirq.svg)


### 6.3.2 ipcsShmHardirq

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 硬中断处理，禁止并清除远端通知，中断后续处理交给 tasklet 或等待队列。 |
| 函数原型 | `static irqreturn_t ipcsShmHardirq(int irq, void *dev)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `irq`: `int irq`<br>`dev`: `void *dev` |
| 返回值 | `irqreturn_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.2 ipcsShmHardirq processing flow](cursor_tmp/flow_svgs/linux_6_3_2_ipcsShmHardirq.svg)


### 6.3.3 ipcsOsInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 初始化指定实例的 Linux OSAL 资源，建立共享内存映射、记录回调并配置接收中断。 |
| 函数原型 | `int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg, int (*rx_cb)(const uint8_t, int))` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg`<br>`rx_cb`: `int (*rx_cb)(const uint8_t, int)` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.3 ipcsOsInit processing flow](cursor_tmp/flow_svgs/linux_6_3_3_ipcsOsInit.svg)


### 6.3.4 ipcsOsFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 释放指定实例 OSAL 资源，关闭线程/设备、解除映射并清理状态。 |
| 函数原型 | `void ipcsOsFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.4 ipcsOsFree processing flow](cursor_tmp/flow_svgs/linux_6_3_4_ipcsOsFree.svg)


### 6.3.5 ipcsOsGetLocalShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 返回本地共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetLocalShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.5 ipcsOsGetLocalShm processing flow](cursor_tmp/flow_svgs/linux_6_3_5_ipcsOsGetLocalShm.svg)


### 6.3.6 ipcsOsGetRemoteShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 返回远端共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetRemoteShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.6 ipcsOsGetRemoteShm processing flow](cursor_tmp/flow_svgs/linux_6_3_6_ipcsOsGetRemoteShm.svg)


### 6.3.7 ipcsOsMapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 映射或返回中断控制器寄存器空间。 |
| 函数原型 | `void *ipcsOsMapIntc(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `void *` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.7 ipcsOsMapIntc processing flow](cursor_tmp/flow_svgs/linux_6_3_7_ipcsOsMapIntc.svg)


### 6.3.8 ipcsOsUnmapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 释放中断控制器寄存器映射或提供对应空实现。 |
| 函数原型 | `void ipcsOsUnmapIntc(void *addr)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `addr`: `void *addr` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.8 ipcsOsUnmapIntc processing flow](cursor_tmp/flow_svgs/linux_6_3_8_ipcsOsUnmapIntc.svg)


### 6.3.9 ipcsOsPollChannels

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | 在轮询模式下触发 rx_cb 处理接收通道。 |
| 函数原型 | `int ipcsOsPollChannels(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.9 ipcsOsPollChannels processing flow](cursor_tmp/flow_svgs/linux_6_3_9_ipcsOsPollChannels.svg)


### 6.3.10 shm_mod_init

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | Linux 全内核模块初始化入口。 |
| 函数原型 | `static int __init shm_mod_init(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `int __init` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.10 shm_mod_init processing flow](cursor_tmp/flow_svgs/linux_6_3_10_shm_mod_init.svg)


### 6.3.11 shm_mod_exit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_KERN |
| 函数说明 | Linux 全内核模块退出入口。 |
| 函数原型 | `static void __exit shm_mod_exit(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `void __exit` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-os.h` |

processing flow

![6.3.11 shm_mod_exit processing flow](cursor_tmp/flow_svgs/linux_6_3_11_shm_mod_exit.svg)


## 6.4 UIO 实现函数设计

UIO 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 UIO fd、/dev/mem、pthread 转发到内核。

### 6.4.1 line_from_file

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 读取 sysfs 文件中的一行内容。 |
| 函数原型 | `static int line_from_file(char *filename, char *buf)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `filename`: `char *filename`<br>`buf`: `char *buf` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.1 line_from_file processing flow](cursor_tmp/flow_svgs/linux_6_4_1_line_from_file.svg)


### 6.4.2 line_match

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 比较 sysfs 文件内容与目标过滤字符串。 |
| 函数原型 | `static int line_match(char *filename, char *filter)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `filename`: `char *filename`<br>`filter`: `char *filter` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.2 line_match processing flow](cursor_tmp/flow_svgs/linux_6_4_2_line_match.svg)


### 6.4.3 get_uio_dev_name

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 在 sysfs 中查找匹配实例的 UIO 设备名。 |
| 函数原型 | `static int get_uio_dev_name(char *dev_name, const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `dev_name`: `char *dev_name`<br>`instance`: `const uint8_t instance` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.3 get_uio_dev_name processing flow](cursor_tmp/flow_svgs/linux_6_4_3_get_uio_dev_name.svg)


### 6.4.4 ipcsShmSoftirq

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 延迟收包处理，遍历实例并调用上层 rx_cb，完成后重新使能 IRQ。 |
| 函数原型 | `static void *ipcsShmSoftirq(void *arg)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `arg`: `void *arg` |
| 返回值 | `void *` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.4 ipcsShmSoftirq processing flow](cursor_tmp/flow_svgs/linux_6_4_4_ipcsShmSoftirq.svg)


### 6.4.5 ipcsOsInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 初始化指定实例的 Linux OSAL 资源，建立共享内存映射、记录回调并配置接收中断。 |
| 函数原型 | `int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg, int (*rx_cb)(const uint8_t, int))` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg`<br>`rx_cb`: `int (*rx_cb)(const uint8_t, int)` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.5 ipcsOsInit processing flow](cursor_tmp/flow_svgs/linux_6_4_5_ipcsOsInit.svg)


### 6.4.6 ipcsOsFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 释放指定实例 OSAL 资源，关闭线程/设备、解除映射并清理状态。 |
| 函数原型 | `void ipcsOsFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.6 ipcsOsFree processing flow](cursor_tmp/flow_svgs/linux_6_4_6_ipcsOsFree.svg)


### 6.4.7 ipcsOsGetLocalShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 返回本地共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetLocalShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.7 ipcsOsGetLocalShm processing flow](cursor_tmp/flow_svgs/linux_6_4_7_ipcsOsGetLocalShm.svg)


### 6.4.8 ipcsOsGetRemoteShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 返回远端共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetRemoteShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.8 ipcsOsGetRemoteShm processing flow](cursor_tmp/flow_svgs/linux_6_4_8_ipcsOsGetRemoteShm.svg)


### 6.4.9 ipcsOsPollChannels

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 在轮询模式下触发 rx_cb 处理接收通道。 |
| 函数原型 | `int ipcsOsPollChannels(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.9 ipcsOsPollChannels processing flow](cursor_tmp/flow_svgs/linux_6_4_9_ipcsOsPollChannels.svg)


### 6.4.10 ipcsSendUioCmd

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 向 UIO fd 写入命令，代理 IRQ 使能、禁止或通知。 |
| 函数原型 | `static void ipcsSendUioCmd(uint32_t uio_fd, int32_t cmd)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `uio_fd`: `uint32_t uio_fd`<br>`cmd`: `int32_t cmd` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.10 ipcsSendUioCmd processing flow](cursor_tmp/flow_svgs/linux_6_4_10_ipcsSendUioCmd.svg)


### 6.4.11 ipcsHwIrqEnable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 使能指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqEnable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.11 ipcsHwIrqEnable processing flow](cursor_tmp/flow_svgs/linux_6_4_11_ipcsHwIrqEnable.svg)


### 6.4.12 ipcsHwIrqDisable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 禁止指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqDisable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.12 ipcsHwIrqDisable processing flow](cursor_tmp/flow_svgs/linux_6_4_12_ipcsHwIrqDisable.svg)


### 6.4.13 ipcsHwIrqNotify

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 通知远端有数据可用；用户侧为转发代理，内核侧触发硬件中断。 |
| 函数原型 | `void ipcsHwIrqNotify(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.13 ipcsHwIrqNotify processing flow](cursor_tmp/flow_svgs/linux_6_4_13_ipcsHwIrqNotify.svg)


### 6.4.14 ipcsHwInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 初始化 HAL 资源；用户侧为空实现，内核侧映射并配置 MSCM/IRQ。 |
| 函数原型 | `int ipcsHwInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.14 ipcsHwInit processing flow](cursor_tmp/flow_svgs/linux_6_4_14_ipcsHwInit.svg)


### 6.4.15 ipcsHwFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_UIO |
| 函数说明 | 释放 HAL 资源；用户侧为空实现，内核侧释放映射状态。 |
| 函数原型 | `void ipcsHwFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_uio/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_uio/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_uio/ipc-os.h` |

processing flow

![6.4.15 ipcsHwFree processing flow](cursor_tmp/flow_svgs/linux_6_4_15_ipcsHwFree.svg)


### 6.4.16 UIO 内核 Backend 函数

### 6.4.17 ipcsShmUioOpen

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 处理 UIO 设备打开请求并维护引用计数。 |
| 函数原型 | `static int ipcsShmUioOpen(struct uio_info *info, struct inode *inode)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `info`: `struct uio_info *info`<br>`inode`: `struct inode *inode` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.17 ipcsShmUioOpen processing flow](cursor_tmp/flow_svgs/linux_6_4_17_ipcsShmUioOpen.svg)


### 6.4.18 ipcsShmUioRelease

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 处理 UIO 设备关闭请求并恢复引用计数。 |
| 函数原型 | `static int ipcsShmUioRelease(struct uio_info *info, struct inode *inode)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `info`: `struct uio_info *info`<br>`inode`: `struct inode *inode` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.18 ipcsShmUioRelease processing flow](cursor_tmp/flow_svgs/linux_6_4_18_ipcsShmUioRelease.svg)


### 6.4.19 ipcsShmUioIrqcontrol

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 处理 UIO irqcontrol 命令并调用 HAL IRQ 操作。 |
| 函数原型 | `static int ipcsShmUioIrqcontrol(struct uio_info *dev_info, int cmd)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `dev_info`: `struct uio_info *dev_info`<br>`cmd`: `int cmd` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.19 ipcsShmUioIrqcontrol processing flow](cursor_tmp/flow_svgs/linux_6_4_19_ipcsShmUioIrqcontrol.svg)


### 6.4.20 ipcsShmUioHandler

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | UIO 中断处理，禁止并清除 IRQ，返回 IRQ_HANDLED 唤醒用户态。 |
| 函数原型 | `static irqreturn_t ipcsShmUioHandler(int irq, struct uio_info *dev_info)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `irq`: `int irq`<br>`dev_info`: `struct uio_info *dev_info` |
| 返回值 | `irqreturn_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.20 ipcsShmUioHandler processing flow](cursor_tmp/flow_svgs/linux_6_4_20_ipcsShmUioHandler.svg)


### 6.4.21 ipcsUioInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 根据用户配置初始化 UIO 实例、HAL 与 IRQ，并注册 UIO 设备。 |
| 函数原型 | `static int ipcsUioInit(struct IPCS_UIO_CDEV_DATA_TYPE *data)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `data`: `struct IPCS_UIO_CDEV_DATA_TYPE *data` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.21 ipcsUioInit processing flow](cursor_tmp/flow_svgs/linux_6_4_21_ipcsUioInit.svg)


### 6.4.22 ipcsCdevOpen

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 处理字符设备打开请求。 |
| 函数原型 | `static int ipcsCdevOpen(struct inode *inode, struct file *filp)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `inode`: `struct inode *inode`<br>`filp`: `struct file *filp` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.22 ipcsCdevOpen processing flow](cursor_tmp/flow_svgs/linux_6_4_22_ipcsCdevOpen.svg)


### 6.4.23 ipcsCdevRelease

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 处理字符设备关闭请求。 |
| 函数原型 | `static int ipcsCdevRelease(struct inode *inode, struct file *filp)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `inode`: `struct inode *inode`<br>`filp`: `struct file *filp` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.23 ipcsCdevRelease processing flow](cursor_tmp/flow_svgs/linux_6_4_23_ipcsCdevRelease.svg)


### 6.4.24 ipcsCdevWrite

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 接收用户侧 UIO 配置并初始化对应 UIO 设备。 |
| 函数原型 | `static ssize_t ipcsCdevWrite(struct file *file, const char __user *user_buffer, size_t size, loff_t *offset)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `file`: `struct file *file`<br>`user_buffer`: `const char __user *user_buffer`<br>`size`: `size_t size`<br>`offset`: `loff_t *offset` |
| 返回值 | `ssize_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.24 ipcsCdevWrite processing flow](cursor_tmp/flow_svgs/linux_6_4_24_ipcsCdevWrite.svg)


### 6.4.25 ipcsShmUioProbe

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 平台驱动 probe，映射 MSCM 资源并创建设备节点。 |
| 函数原型 | `static int ipcsShmUioProbe(struct platform_device *pdev)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `pdev`: `struct platform_device *pdev` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.25 ipcsShmUioProbe processing flow](cursor_tmp/flow_svgs/linux_6_4_25_ipcsShmUioProbe.svg)


### 6.4.26 ipcsShmUioRemove

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 平台驱动 remove，注销设备并释放 UIO 实例。 |
| 函数原型 | `static int ipcsShmUioRemove(struct platform_device *pdev)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `pdev`: `struct platform_device *pdev` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.26 ipcsShmUioRemove processing flow](cursor_tmp/flow_svgs/linux_6_4_26_ipcsShmUioRemove.svg)


### 6.4.27 ipcsOsMapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 映射或返回中断控制器寄存器空间。 |
| 函数原型 | `void *ipcsOsMapIntc(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `void *` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.27 ipcsOsMapIntc processing flow](cursor_tmp/flow_svgs/linux_6_4_27_ipcsOsMapIntc.svg)


### 6.4.28 ipcsOsUnmapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_UIO_KO |
| 函数说明 | 释放中断控制器寄存器映射或提供对应空实现。 |
| 函数原型 | `void ipcsOsUnmapIntc(void *addr)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-uio.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `addr`: `void *addr` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-uio.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-uio.h` |

processing flow

![6.4.28 ipcsOsUnmapIntc processing flow](cursor_tmp/flow_svgs/linux_6_4_28_ipcsOsUnmapIntc.svg)


## 6.5 CDEV 实现函数设计

CDEV 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 cdev ioctl/poll/mmap 与内核通信。

### 6.5.1 ipcsOsInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 初始化指定实例的 Linux OSAL 资源，建立共享内存映射、记录回调并配置接收中断。 |
| 函数原型 | `int ipcsOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg, int (*rx_cb)(const uint8_t, int))` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg`<br>`rx_cb`: `int (*rx_cb)(const uint8_t, int)` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.1 ipcsOsInit processing flow](cursor_tmp/flow_svgs/linux_6_5_1_ipcsOsInit.svg)


### 6.5.2 ipcsOsFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 释放指定实例 OSAL 资源，关闭线程/设备、解除映射并清理状态。 |
| 函数原型 | `void ipcsOsFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.2 ipcsOsFree processing flow](cursor_tmp/flow_svgs/linux_6_5_2_ipcsOsFree.svg)


### 6.5.3 ipcsOsGetLocalShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 返回本地共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetLocalShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.3 ipcsOsGetLocalShm processing flow](cursor_tmp/flow_svgs/linux_6_5_3_ipcsOsGetLocalShm.svg)


### 6.5.4 ipcsOsGetRemoteShm

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 返回远端共享内存虚拟地址。 |
| 函数原型 | `uintptr_t ipcsOsGetRemoteShm(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `uintptr_t` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.4 ipcsOsGetRemoteShm processing flow](cursor_tmp/flow_svgs/linux_6_5_4_ipcsOsGetRemoteShm.svg)


### 6.5.5 ipcsOsPollChannels

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 在轮询模式下触发 rx_cb 处理接收通道。 |
| 函数原型 | `int ipcsOsPollChannels(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.5 ipcsOsPollChannels processing flow](cursor_tmp/flow_svgs/linux_6_5_5_ipcsOsPollChannels.svg)


### 6.5.6 ipcsHwIrqEnable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 使能指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqEnable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.6 ipcsHwIrqEnable processing flow](cursor_tmp/flow_svgs/linux_6_5_6_ipcsHwIrqEnable.svg)


### 6.5.7 ipcsHwIrqDisable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 禁止指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqDisable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.7 ipcsHwIrqDisable processing flow](cursor_tmp/flow_svgs/linux_6_5_7_ipcsHwIrqDisable.svg)


### 6.5.8 ipcsHwIrqNotify

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 通知远端有数据可用；用户侧为转发代理，内核侧触发硬件中断。 |
| 函数原型 | `void ipcsHwIrqNotify(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.8 ipcsHwIrqNotify processing flow](cursor_tmp/flow_svgs/linux_6_5_8_ipcsHwIrqNotify.svg)


### 6.5.9 ipcsHwInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 初始化 HAL 资源；用户侧为空实现，内核侧映射并配置 MSCM/IRQ。 |
| 函数原型 | `int ipcsHwInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.9 ipcsHwInit processing flow](cursor_tmp/flow_svgs/linux_6_5_9_ipcsHwInit.svg)


### 6.5.10 ipcsHwFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_OS_CDEV |
| 函数说明 | 释放 HAL 资源；用户侧为空实现，内核侧释放映射状态。 |
| 函数原型 | `void ipcsHwFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/os_cdev/ipc-os.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_cdev/ipc-os.c` |
| 函数声明文件 | `ipcs/mpu/os_cdev/ipc-os.h` |

processing flow

![6.5.10 ipcsHwFree processing flow](cursor_tmp/flow_svgs/linux_6_5_10_ipcsHwFree.svg)


### 6.5.11 CDEV 内核 Backend 函数

### 6.5.12 ipcsShmHardirq

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 硬中断处理，禁止并清除远端通知，中断后续处理交给 tasklet 或等待队列。 |
| 函数原型 | `static irqreturn_t ipcsShmHardirq(int irq, void *dev)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `irq`: `int irq`<br>`dev`: `void *dev` |
| 返回值 | `irqreturn_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.12 ipcsShmHardirq processing flow](cursor_tmp/flow_svgs/linux_6_5_12_ipcsShmHardirq.svg)


### 6.5.13 ipcsOsMapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 映射或返回中断控制器寄存器空间。 |
| 函数原型 | `void *ipcsOsMapIntc(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `void *` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.13 ipcsOsMapIntc processing flow](cursor_tmp/flow_svgs/linux_6_5_13_ipcsOsMapIntc.svg)


### 6.5.14 ipcsOsUnmapIntc

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 释放中断控制器寄存器映射或提供对应空实现。 |
| 函数原型 | `void ipcsOsUnmapIntc(void *addr)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `addr`: `void *addr` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.14 ipcsOsUnmapIntc processing flow](cursor_tmp/flow_svgs/linux_6_5_14_ipcsOsUnmapIntc.svg)


### 6.5.15 ipcsCdevOpen

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 处理字符设备打开请求。 |
| 函数原型 | `static int ipcsCdevOpen(struct inode *inode, struct file *file)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `inode`: `struct inode *inode`<br>`file`: `struct file *file` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.15 ipcsCdevOpen processing flow](cursor_tmp/flow_svgs/linux_6_5_15_ipcsCdevOpen.svg)


### 6.5.16 ipcsCdevRelease

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 处理字符设备关闭请求。 |
| 函数原型 | `static int ipcsCdevRelease(struct inode *inode, struct file *file)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `inode`: `struct inode *inode`<br>`file`: `struct file *file` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.16 ipcsCdevRelease processing flow](cursor_tmp/flow_svgs/linux_6_5_16_ipcsCdevRelease.svg)


### 6.5.17 ipcsCdevRead

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 阻塞等待内核接收中断唤醒。 |
| 函数原型 | `static ssize_t ipcsCdevRead(struct file *file, char __user *user_buffer, size_t size, loff_t *offset)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `file`: `struct file *file`<br>`user_buffer`: `char __user *user_buffer`<br>`size`: `size_t size`<br>`offset`: `loff_t *offset` |
| 返回值 | `ssize_t` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.17 ipcsCdevRead processing flow](cursor_tmp/flow_svgs/linux_6_5_17_ipcsCdevRead.svg)


### 6.5.18 ipcsCdevOsInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 初始化 CDEV 后端实例、HAL 和接收 IRQ。 |
| 函数原型 | `static int ipcsCdevOsInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.18 ipcsCdevOsInit processing flow](cursor_tmp/flow_svgs/linux_6_5_18_ipcsCdevOsInit.svg)


### 6.5.19 ipcsCdevIoctl

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | 处理 CDEV 用户侧 ioctl 命令，包括实例初始化和 IRQ 操作代理。 |
| 函数原型 | `static long ipcsCdevIoctl(struct file *file, unsigned int ioctl_cmd, unsigned long ioctl_arg)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `file`: `struct file *file`<br>`ioctl_cmd`: `unsigned int ioctl_cmd`<br>`ioctl_arg`: `unsigned long ioctl_arg` |
| 返回值 | `long` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.19 ipcsCdevIoctl processing flow](cursor_tmp/flow_svgs/linux_6_5_19_ipcsCdevIoctl.svg)


### 6.5.20 ipcsCdevInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | CDEV 模块初始化，创建字符设备和 wait queue。 |
| 函数原型 | `static int ipcsCdevInit(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.20 ipcsCdevInit processing flow](cursor_tmp/flow_svgs/linux_6_5_20_ipcsCdevInit.svg)


### 6.5.21 ipcsCdevClean

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Linux_Adapt_Cmp |
| 软件单元 ID | SWU_IPCS_LINUX_CDEV_KO |
| 函数说明 | CDEV 模块清理，禁止 IRQ、释放中断并销毁字符设备。 |
| 函数原型 | `static void ipcsCdevClean(void)` |
| 制约条件 | 按 `ipcs/mpu/os_kernel/ipc-cdev.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | - |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| 函数声明文件 | `ipcs/mpu/os_kernel/ipc-cdev.h` |

processing flow

![6.5.21 ipcsCdevClean processing flow](cursor_tmp/flow_svgs/linux_6_5_21_ipcsCdevClean.svg)


## 6.6 Linux HAL 函数设计

Linux 内核侧 HAL，完成 MSCM 映射、核索引解析、IRQ 使能/禁止/通知/清除等硬件操作。

### 6.6.1 ipcsHwGetRxIrq

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 返回指定实例使用的 MSCM 接收中断索引。 |
| 函数原型 | `int ipcsHwGetRxIrq(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.1 ipcsHwGetRxIrq processing flow](cursor_tmp/flow_svgs/linux_6_6_1_ipcsHwGetRxIrq.svg)


### 6.6.2 ipcsHwInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 初始化 HAL 资源；用户侧为空实现，内核侧映射并配置 MSCM/IRQ。 |
| 函数原型 | `int ipcsHwInit(const uint8_t instance, const struct IPCS_SHM_CFG_TYPE *cfg)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`cfg`: `const struct IPCS_SHM_CFG_TYPE *cfg` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.2 ipcsHwInit processing flow](cursor_tmp/flow_svgs/linux_6_6_2_ipcsHwInit.svg)


### 6.6.3 _ipcsHwInit

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | HAL 底层初始化，供 Linux UIO 等内核路径复用。 |
| 函数原型 | `int _ipcsHwInit(const uint8_t instance, int tx_irq, int rx_irq, const struct IPCS_SHM_REMOTE_CORE_TYPE *remote_core, const struct IPCS_SHM_LOCAL_CORE_TYPE *local_core, void *mscm_addr)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance`<br>`tx_irq`: `int tx_irq`<br>`rx_irq`: `int rx_irq`<br>`remote_core`: `const struct IPCS_SHM_REMOTE_CORE_TYPE *remote_core`<br>`local_core`: `const struct IPCS_SHM_LOCAL_CORE_TYPE *local_core`<br>`mscm_addr`: `void *mscm_addr` |
| 返回值 | `int` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.3 _ipcsHwInit processing flow](cursor_tmp/flow_svgs/linux_6_6_3__ipcsHwInit.svg)


### 6.6.4 ipcsHwFree

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 释放 HAL 资源；用户侧为空实现，内核侧释放映射状态。 |
| 函数原型 | `void ipcsHwFree(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.4 ipcsHwFree processing flow](cursor_tmp/flow_svgs/linux_6_6_4_ipcsHwFree.svg)


### 6.6.5 ipcsHwIrqEnable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 使能指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqEnable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.5 ipcsHwIrqEnable processing flow](cursor_tmp/flow_svgs/linux_6_6_5_ipcsHwIrqEnable.svg)


### 6.6.6 ipcsHwIrqDisable

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 禁止指定实例接收中断；用户侧为转发代理，内核侧访问硬件。 |
| 函数原型 | `void ipcsHwIrqDisable(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.6 ipcsHwIrqDisable processing flow](cursor_tmp/flow_svgs/linux_6_6_6_ipcsHwIrqDisable.svg)


### 6.6.7 ipcsHwIrqNotify

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 通知远端有数据可用；用户侧为转发代理，内核侧触发硬件中断。 |
| 函数原型 | `void ipcsHwIrqNotify(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.7 ipcsHwIrqNotify processing flow](cursor_tmp/flow_svgs/linux_6_6_7_ipcsHwIrqNotify.svg)


### 6.6.8 ipcsHwIrqClear

| 项 | 内容 |
|---|---|
| 对应软件架构 ID | Drv_Ipcs_Hal_Cmp |
| 软件单元 ID | SWU_IPCS_HAL_LINUX |
| 函数说明 | 清除指定实例接收中断状态。 |
| 函数原型 | `void ipcsHwIrqClear(const uint8_t instance)` |
| 制约条件 | 按 `ipcs/mpu/hw/c1/ipc-hw.c` 中的入参检查、实例状态和内核资源状态执行 |
| 输入/输出参数 | `instance`: `const uint8_t instance` |
| 返回值 | `void` |
| 函数定义文件 | `ipcs/mpu/hw/c1/ipc-hw.c` |
| 函数声明文件 | `ipcs/mpu/hw/ipc-hw.h` |

processing flow

![6.6.8 ipcsHwIrqClear processing flow](cursor_tmp/flow_svgs/linux_6_6_8_ipcsHwIrqClear.svg)


## 6.7 Linux 关键场景流程

第 6.3–6.6 节各函数已给出单函数 processing flow（活动图）。本节描述 **跨软件单元** 的动态交互，采用 UML 序列图；纵轴为软件单元 ID（§2.1），用户侧代理、内核 Backend、HAL 使用与 §5.7 相同的配色规则。

| 场景 ID | 场景名称 | 涉及软件单元 | 源码依据 |
|---|---|---|---|
| LIN-S01 | UIO 初始化 | CORE_SHM、LINUX_OS_UIO、LINUX_UIO_KO、HAL_LINUX | `ipcsOsInit`（os_uio）+ `ipcsCdevWrite`/`ipcsUioInit` |
| LIN-S02 | CDEV 初始化 | CORE_SHM、LINUX_OS_CDEV、LINUX_CDEV_KO、HAL_LINUX | `ipcsOsInit`（os_cdev）+ `ioctl` INIT |
| LIN-S03 | 全内核初始化 | CORE_SHM、LINUX_OS_KERN、HAL_LINUX | `ipcsOsInit`（os_kernel） |
| LIN-S04 | UIO 发送通知 | CORE_SHM、LINUX_OS_UIO、LINUX_UIO_KO、HAL_LINUX | `ipcsSendUioCmd` / `ipcsShmUioIrqcontrol` |
| LIN-S05 | CDEV 发送通知 | CORE_SHM、LINUX_OS_CDEV、LINUX_CDEV_KO、HAL_LINUX | `ioctl(TRIGGER_TX_IRQ)` |
| LIN-S06 | UIO 接收唤醒 | HAL_LINUX、LINUX_UIO_KO、LINUX_OS_UIO、CORE_SHM | `ipcsShmUioHandler` + pthread `read` |
| LIN-S07 | CDEV 接收唤醒 | HAL_LINUX、LINUX_CDEV_KO、LINUX_OS_CDEV、CORE_SHM | `ipcsShmHardirq` + `wait_queue` |
| LIN-S08 | 全内核接收 | HAL_LINUX、LINUX_OS_KERN、CORE_SHM | `ipcsShmHardirq` + tasklet |

### 6.7.1 UIO 初始化（LIN-S01）

sequence diagram

![Linux UIO initialization sequence](cursor_tmp/flow_svgs/linux_seq_uio_init.svg)

### 6.7.2 CDEV 初始化（LIN-S02）

sequence diagram

![Linux CDEV initialization sequence](cursor_tmp/flow_svgs/linux_seq_cdev_init.svg)

### 6.7.3 全内核初始化（LIN-S03）

sequence diagram

![Linux in-kernel initialization sequence](cursor_tmp/flow_svgs/linux_seq_kernel_init.svg)

### 6.7.4 UIO 发送通知（LIN-S04）

sequence diagram

![Linux UIO transmit notify sequence](cursor_tmp/flow_svgs/linux_seq_uio_tx_notify.svg)

### 6.7.5 CDEV 发送通知（LIN-S05）

sequence diagram

![Linux CDEV transmit notify sequence](cursor_tmp/flow_svgs/linux_seq_cdev_tx_notify.svg)

### 6.7.6 UIO 接收唤醒（LIN-S06）

sequence diagram

![Linux UIO receive wakeup sequence](cursor_tmp/flow_svgs/linux_seq_uio_rx.svg)

### 6.7.7 CDEV 接收唤醒（LIN-S07）

sequence diagram

![Linux CDEV receive wakeup sequence](cursor_tmp/flow_svgs/linux_seq_cdev_rx.svg)

### 6.7.8 全内核接收（LIN-S08）

sequence diagram

![Linux in-kernel receive sequence](cursor_tmp/flow_svgs/linux_seq_kernel_rx.svg)

## 6.8 Linux 全局变量与私有类型

| 源文件 | 关键类型 / 变量 | 用途 |
|---|---|---|
| `ipcs/mpu/os_uio/ipc-os.c` | `struct IPCS_OS_PRIV_TYPE_TYPE ipc_os_priv` | 用户侧 fd、mmap 地址、RX 线程与回调状态 |
| `ipcs/mpu/os_cdev/ipc-os.c` | `priv` / `IPCS_OS_PRIV_TYPE` | CDEV 用户侧 fd、共享内存映射和代理状态 |
| `ipcs/mpu/os_kernel/ipc-os.c` | `priv` | 全内核实例状态、共享内存地址、IRQ 和 rx_cb |
| `ipcs/mpu/os_kernel/ipc-uio.c` | `ipc_pdev_priv` | UIO 平台设备、cdev、UIO 实例和 IRQ 状态 |
| `ipcs/mpu/os_kernel/ipc-cdev.c` | `ipc_cdev_priv` | 字符设备、wait queue、目标实例和 IRQ 状态 |
| `ipcs/mpu/hw/c1/ipc-hw.c` | `ipc_hw_priv[]` | MSCM、IRQ、核索引和平台私有状态 |

# 7 Traceability and Consistency Evidence 追溯与一致性证据

## 7.1 SWE.3 覆盖说明

| SWE.3 过程结果 / 实践 | 文档落点 |
|---|---|
| 详细设计描述软件单元 | §4–§6 Files 与各函数单元 |
| 定义软件单元接口 | §4.3 对外 API；§5/§6 OSAL/HAL；§3.4、§6.6 |
| 定义动态行为 | §4.7、§5.7、§6.7 及各函数 processing flow |
| 与架构双向追溯 | §7.2；§2；§3 |
| 与架构设计一致 | §2–§3（三层契约与 Linux 适配形态） |
| 软件单元可实现 | ipcs/ 源码路径与构建说明 |

## 7.2 架构—设计—源码追溯矩阵

### 7.2.1 软件单元追溯（节选）

| SW-Unit-ID | 函数/设计章节出处 | 源文件 |
|---|---|---|
| SWU_IPCS_CORE_SHM | §5.3、§5.4（Core 内部函数） | ipcs/ipcs_cores/ipc-shm.c |
| SWU_IPCS_CORE_QUEUE | §5.4.1–4.4.5 | ipcs/ipcs_cores/ipc-queue.c |
| SWU_IPCS_HAL_MCU | §5.6 HAL、§5.3–4.5 OSAL | ipcs/mcu/hw/ipc-hw.c |
| SWU_IPCS_LINUX_OS_UIO | §6.4 | ipcs/mpu/os_uio/ipc-os.c |

| 架构组件 ID | 部署变体 / 实现 | 主要源码 |
|---|---|---|
| Drv_Ipcs_Core_Cmp | 全部 | ipcs/ipcs_cores/ipc-shm.c |
| Drv_Ipcs_Queue_Cmp | 全部 | ipcs/ipcs_cores/ipc-queue.c |
| Drv_Ipcs_Conf_Cmp | 全部 | ipcs/ipcs_cores/ipc-types.h |
| Drv_Ipcs_Osal_Cmp | RTOS 各 OS 实现 | ipcs/mcu/os/*/ipc-os-*.c |
| Drv_Ipcs_Hal_Cmp | RTOS 部署变体 | ipcs/mcu/hw/ipc-hw.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux 全内核 | ipcs/mpu/os_kernel/ipc-os.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux UIO | ipcs/mpu/os_uio/ipc-os.c + ipcs/mpu/os_kernel/ipc-uio.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux CDEV | ipcs/mpu/os_cdev/ipc-os.c + ipcs/mpu/os_kernel/ipc-cdev.c |

## 7.3 源码核对结果

核对基准：`ipcs/` 目录（2026-05-19），与本文档设计条目一致。

| 路径 | 纳入章节 | 说明 |
|---|---|---|
| ipcs/ipcs_cores/ipc-shm.c | §4.2、§4.3–4.4 | Core 对外/内部 API 与源码一致 |
| ipcs/ipcs_cores/ipc-queue.c | §3.2、§5.4.1–4.4.5 | 队列单元 |
| ipcs/ipcs_cores/ipc-util.c | §4.2、§4.4.23 | memcpy 等工具 |
| ipcs/ipcs_cores/ipc-types.h | §4.6 | 配置与 BD 类型 |
| ipcs/mcu/hw/ipc-hw.c | §5.2、§5.6 | RTOS HAL；`ipcsHw*` 与 §4.6 一致 |
| ipcs/mcu/os/autosar/ipc-os-autosar.c | §5.3 | AUTOSAR OSAL |
| ipcs/mcu/os/freertos/ipc-os-freertos.c | §5.4 | FreeRTOS OSAL |
| ipcs/mcu/os/threadx/ipc-os-threadx.c | §5.5 | ThreadX OSAL |
| ipcs/mcu/os/baremetal/ipc-os-baremetal.c | — | 不在 SDD 范围 |
| ipcs/mpu/os_kernel/ipc-os.c | §6.3 | 全内核实现 |
| ipcs/mpu/os_uio/ipc-os.c | §6.4 | UIO 用户侧 P4/P5 代理 |
| ipcs/mpu/os_cdev/ipc-os.c | §6.5 | CDEV 用户侧 P4/P5 代理 |
| ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c | §6.4–6.5 | 内核 Backend |
| ipcs/mpu/hw/c1/ipc-hw.c | §6、§3.4 | Linux 内核 HAL |

对外 API（`ipcs-shm.h`）：`ipcsShmInit`、`ipcsShmFree`、`ipcsShmAcquireBuf`、`ipcsShmReleaseBuf`、`ipcsShmTx`、`ipcsShmUnmanagedAcquire`、`ipcsShmUnmanagedTx`、`ipcsShmIsRemoteReady`、`ipcsShmPollChannels` — 与 §3.3 一致。


## 7.4 对外/内部接口判定规则

| 类型 | 规则 |
|---|---|
| 对外（应用） | ipcs/ipcs_cores/ipc-shm.h 中声明且 ipcs-shm.c 中非 static 的 API |
| OSAL/HAL | 以 ipc-os.h、ipc-hw.h 声明；实现位置见 §3.4、§6.6 |
| 用户侧代理 | 用户库内 `ipcsOs*`/`ipcsHw*` 满足 P4/P5 契约，实现为转发；属 Linux Adapt（§3.4） |
| 内部 | static 函数及仅单元内使用的类型 |
