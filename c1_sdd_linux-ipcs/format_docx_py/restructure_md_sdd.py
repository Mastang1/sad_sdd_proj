# -*- coding: utf-8 -*-
"""
重组 md_sdd_0519.md：按 ASPICE SWE.3 计划拆分为第 1–6 章。
用法（仓库根目录）: python format_docx_py/restructure_md_sdd.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "md_sdd_0519.md"
DST = ROOT / "md_sdd_0519.md"

NEW_CONTENTS = """## CONTENTS 目录

- 1 INTRODUCTION简介
  - 1.1 Confidentiality 保密性
  - 1.2 Purpose of the document文档目的
  - 1.3 Scope范围
  - 1.4 References 参考文件
  - 1.5 Abbreviations缩略语
- 2 Software Architecture软件架构
  - 2.1 架构分层与组件
  - 2.2 组件关系与端口
  - 2.3 运行场景
  - 2.4 部署变体与实现（L1/L2）
  - 2.5 外部依赖与运行环境
  - 2.6 Linux 部署变体架构细化（SDD Refinement）
- 3 公共详细设计（跨部署变体共享）
  - 3.1 Definition定义
  - 3.2 Files
  - 3.3 External Interfaces外部接口
  - 3.4 Internal Functions 内部函数
  - 3.5 Global variants 全局变量
  - 3.6 Data Structure 类型定义
  - 3.7 Dynamic Detailed Design 动态详细设计
- 4 RTOS 部署变体详细设计
  - 4.1 总述
  - 4.2 Files 与依赖
  - 4.3 AUTOSAR OS 实现
  - 4.4 FreeRTOS 实现
  - 4.5 ThreadX 实现
  - 4.6 HAL 单元设计（MCU 共用）
  - 4.7 RTOS 动态详细设计
- 5 Linux 部署变体详细设计
  - 5.1 与架构关系及 Refinement
  - 5.2 源码与构建结构
  - 5.3 全内核实现
  - 5.4 UIO 实现
  - 5.5 CDEV 实现
  - 5.6 接口实现分布表
  - 5.7 Linux 动态详细设计
  - 5.8 Linux 全局变量与私有类型
- 6 Traceability and Consistency Evidence 追溯与一致性证据
  - 6.1 SWE.3 覆盖说明
  - 6.2 架构—设计—源码追溯矩阵
  - 6.3 源码核对结果
  - 6.4 接口判定规则
"""

CH2_EXTENSIONS = """
## 2.4 部署变体与实现（L1/L2）

工程在集成时首先选择 **L1 部署变体**（互斥二选一），再在对应分支下选择 **L2 实现**（互斥多选一）。

| L1 部署变体 | L2 实现 | 源码根目录 | 架构组件 |
|---|---|---|---|
| RTOS 部署变体 | FreeRTOS 实现 | ipcs/mcu/os/freertos/ | Drv_Ipcs_Osal_Cmp + Drv_Ipcs_Hal_Cmp |
| RTOS 部署变体 | ThreadX 实现 | ipcs/mcu/os/threadx/ | 同上 |
| RTOS 部署变体 | AUTOSAR OS 实现 | ipcs/mcu/os/autosar/ | 同上 |
| Linux 部署变体 | 全内核实现 | ipcs/mpu/os_kernel/ | Drv_Ipcs_Linux_Adapt_Cmp（含 Core/OSAL/HAL 于内核模块） |
| Linux 部署变体 | UIO 实现 | ipcs/mpu/os_uio/ + ipcs/mpu/os_kernel/ | Drv_Ipcs_Linux_Adapt_Cmp |
| Linux 部署变体 | CDEV 实现 | ipcs/mpu/os_cdev/ + ipcs/mpu/os_kernel/ | Drv_Ipcs_Linux_Adapt_Cmp |

构建选型示例：Linux 用户态库构建使用 `IPCS_OS=uio` 或 `IPCS_OS=cdev`（见 ipcs/mpu 各实现 Makefile）。Baremetal 源码不在本文档范围。

## 2.5 外部依赖与运行环境

| 依赖类别 | 依赖项 | 使用方 | 源码/配置依据 |
|---|---|---|---|
| 硬件 | MSCM 核间中断、共享内存物理区 | HAL | ipcs/mcu/hw/、ipcs/mpu/hw/c1/ |
| 硬件 | 平台寄存器头（S32G 等） | HAL | ipc-hw-platform.h |
| RTOS 软件 | FreeRTOS（task.h 等） | FreeRTOS 实现 | ipcs/mcu/os/freertos/ |
| RTOS 软件 | ThreadX kernel/device | ThreadX 实现 | ipcs/mcu/os/threadx/ |
| RTOS 软件 | AUTOSAR Os.h | AUTOSAR OS 实现 | ipcs/mcu/os/autosar/ |
| Linux 软件 | 内核模块 API、UIO 子系统 | 全内核 / UIO 实现 | ipcs/mpu/os_kernel/ |
| Linux 软件 | 字符设备、ioctl、pthread | CDEV / UIO 用户库 | ipcs/mpu/os_cdev/、os_uio/ |
| Linux 软件 | /dev/mem、mmap | UIO/CDEV 用户 Glue | os_uio/ipc-os.c、os_cdev/ipc-os.c |
| 构建/配置 | ipcf_Ip_Cfg*.h、PLATFORM_FLAVOR | 全部变体 | 集成工程配置 |

上述依赖通过端口 P7（IF_PlatformOS）与 P8（IF_PlatformHW）由外部环境与驱动交换；详细设计中的接口表见第 3–5 章。

## 2.6 Linux 部署变体架构细化（SDD Refinement）

ipcs-architecture.pdf 将 Linux 侧定义为逻辑组件 **Drv_Ipcs_Linux_Adapt_Cmp**，未拆分用户态与内核态。本 SDD 在不新增架构组件 ID 的前提下，将该逻辑组件 **细化（Refinement）** 为下列实现单元：

| 实现单元 | 说明 | 典型路径 |
|---|---|---|
| User-Space Adaptation Glue | 用户态库内实现 `ipcsOs*` 及 `ipcsHw*` 符号；HAL 中为 ioctl/UIO 代理，满足 Core 对 IF_OSAbst/IF_HWAbst 的链接 | ipcs/mpu/os_uio/ipc-os.c、ipcs/mpu/os_cdev/ipc-os.c |
| Kernel Backend | 内核模块：中断、MSCM 寄存器访问、实例初始化 | ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c、ipcs/mpu/hw/c1/ipc-hw.c |
| In-Kernel Monolith | 全内核实现：Core+OSAL+HAL 均在内核模块 | ipcs/mpu/os_kernel/ipc-os.c + hw |

**表：逻辑组件 → 实现单元映射（Linux）**

| 架构逻辑组件 | 全内核实现 | UIO 实现 | CDEV 实现 |
|---|---|---|---|
| Drv_Ipcs_Core_Cmp | 内核模块内 | 用户库 ipcs_cores | 用户库 ipcs_cores |
| Drv_Ipcs_Osal_Cmp（逻辑） | os_kernel/ipc-os.c | User Glue + 内核协同 | User Glue + 内核协同 |
| Drv_Ipcs_Hal_Cmp（逻辑） | mpu/hw/c1/ipc-hw.c | 内核 ipc-hw.c；用户侧 Facade | 同 UIO |
| Drv_Ipcs_Linux_Adapt_Cmp | 单 .ko | 用户库 + ipc-shm-uio.ko | 用户库 + ipc-shm-cdev.ko |

**表：IF_OSAbst / IF_HWAbst 主要 API 实现分布（Linux UIO/CDEV）**

| API | 用户 Glue | 内核 Backend |
|---|---|---|
| ipcsOsInit / ipcsOsFree | os_uio/os_cdev ipc-os.c | ioctl / UIO 配置路径 |
| ipcsOsGetLocalShm / GetRemoteShm | mmap /dev/mem | — |
| ipcsOsPollChannels | 用户线程 + UIO read / cdev poll | ISR 唤醒 |
| ipcsHwInit / ipcsHwFree | dummy（注释：kernel 处理） | ipc-hw.c |
| ipcsHwIrqEnable/Disable/Notify | UIO write 或 ioctl | ipc-hw.c（UIO 经 irqcontrol 调真 HAL） |

Linux UIO/CDEV 下，Core 仍在用户态调用与 RTOS 相同的 `ipcsOs*`/`ipcsHw*` 接口名；物理执行跨用户态与内核态，逻辑架构端口 P4/P5 不变。
"""

CH3_1_UPDATE = """## 3.1 Definition定义

IPCS Driver 是面向同一 SoC 内不同处理核心的 shared memory 通信驱动。公共部分（ipcs/ipcs_cores）实现 IPCF Shared Memory 协议核心，支持 managed/unmanaged channel、中断通知与 polling、多 instance/channel。

**User-Space Adaptation Glue（用户态适配胶水）**：Linux UIO/CDEV 实现中，于用户库内提供与 RTOS 同名的 `ipcsOs*`/`ipcsHw*` 符号；其中 `ipcsHwInit/Free` 为空实现，IRQ 相关 API 通过 ioctl 或 UIO 命令转发至内核 Backend。该单元为 Drv_Ipcs_Linux_Adapt_Cmp 的 SDD 实现子单元，非架构 pdf 新增组件。

本章描述 **跨部署变体共享** 的 Core、Queue、配置类型；RTOS/Linux 专属 OSAL/HAL 见第 4、5 章。
"""

CH3_5_CORE = """## 3.5 Global variants 全局变量

本节仅列出 ipcs/ipcs_cores 内通信核心私有数据。RTOS/Linux 实现侧私有数据见第 4、5 章。

| 全局变量名称 | 全局变量类型 | 全局变量范围 | 全局变量描述 | 全局变量的存储RAM区 |
|---|---|---|---|---|
| ipc_shm_priv_data | static struct IPCS_SHM_PRIV_TYPE [IPC_SHM_MAX_INSTANCES] | ipcs/ipcs_cores/ipc-shm.c | IPCS shm private data | 源码未显式指定 |
"""

CH3_7 = """## 3.7 Dynamic Detailed Design 动态详细设计

本节描述与部署变体无关的 **逻辑** 数据路径（Core + Queue）。变体相关的 OSAL/HAL/跨边界路径见第 4.7、5.7 节。

### 3.7.1 初始化流程

按架构：应用调用 ipcsShmInit → 逐 instance 调用 HAL 初始化、OSAL 初始化、channel 初始化（具体 HAL/OSAL 实现见第 4/5 章）。

### 3.7.2 Managed 发送流程

ipcsShmAcquireBuf → 填充数据 → ipcsShmTx → queue push BD → HAL 通知远端。

### 3.7.3 Managed 接收与释放流程

OSAL 触发 ipcsShmRx → ipcsChannelRx → 应用回调 → ipcsShmReleaseBuf。

### 3.7.4 Unmanaged 发送与接收流程

ipcsShmUnmanagedAcquire / ipcsShmUnmanagedTx；接收侧检查 tx_count。

### 3.7.5 中断与轮询流程

OSAL 注册 hardirq/softirq 或 polling（ipcsShmPollChannels）；Core 按预算分发 channel。
"""

CH4_HEADER = """# 4 RTOS 部署变体详细设计

## 4.1 总述

RTOS 部署变体在 **单地址空间** 内完整实现 Drv_Ipcs_Osal_Cmp 与 Drv_Ipcs_Hal_Cmp。L2 实现三选一：FreeRTOS、ThreadX、AUTOSAR OS。HAL 平台代码位于 ipcs/mcu/hw/，由三种 OS 实现共用。

## 4.2 Files 与依赖

"""

CH5 = """# 5 Linux 部署变体详细设计

## 5.1 与架构关系及 Refinement

逻辑架构见 ipcs-architecture.pdf 中 Drv_Ipcs_Linux_Adapt_Cmp。实现级用户/内核划分见 **§2.6**，本节给出三種 L2 实现的文件与行为说明。

## 5.2 源码与构建结构

| 部件 | 路径 | 产物 |
|---|---|---|
| 通信核心（共享） | ipcs/ipcs_cores/ | libipc-shm 用户库（UIO/CDEV）或编入内核（全内核） |
| UIO 用户 Glue | ipcs/mpu/os_uio/ipc-os.c | libipc-shm.a |
| CDEV 用户 Glue | ipcs/mpu/os_cdev/ipc-os.c | libipc-shm.a |
| 内核 Backend | ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c | ipc-shm-uio.ko、ipc-shm-cdev.ko |
| 全内核 OSAL | ipcs/mpu/os_kernel/ipc-os.c | ipc-shm-dev.ko |
| HAL（Linux） | ipcs/mpu/hw/c1/ipc-hw.c | 链接入上述 .ko |

## 5.3 全内核实现

驱动逻辑（Core、OSAL、HAL）均位于内核模块 `ipc-shm-dev.ko`（os_kernel/ipc-os.c 与 mpu/hw/c1/ipc-hw.c）。应用通过内核导出符号或配套接口使用，无用户态 Glue。中断采用 tasklet 延迟处理（ipcsShmSoftirq）。

## 5.4 UIO 实现

### 5.4.1 User-Space Glue

文件：ipcs/mpu/os_uio/ipc-os.c。职责：模块加载、/dev/mem mmap 共享内存、打开 UIO 设备、pthread 收包线程；`ipcsHw*` 经 `write(uio_fd, cmd)` 转发（ipcsSendUioCmd）。

### 5.4.2 Kernel Backend

文件：ipcs/mpu/os_kernel/ipc-uio.c、ipcs/mpu/hw/c1/ipc-hw.c。职责：UIO 注册、hardirq（ipcsShmUioHandler）、irqcontrol 中调用真实 ipcsHwIrqEnable/Disable/Notify。

## 5.5 CDEV 实现

### 5.5.1 User-Space Glue

文件：ipcs/mpu/os_cdev/ipc-os.c。职责：打开 /dev/ipc-shm-cdev、ioctl 初始化实例；`ipcsHwIrqEnable/Disable/Notify` 使用 IPC_CDEV_CMD_* ioctl。

### 5.5.2 Kernel Backend

文件：ipcs/mpu/os_kernel/ipc-cdev.c。职责：字符设备、wait_queue、ISR 与 ioctl 处理。

## 5.6 接口实现分布表

完整映射见 **§2.6** 表；UIO/CDEV 用户态 `ipcsHwInit/Free` 为 dummy，注释标明由内核模块处理。

## 5.7 Linux 动态详细设计

### 5.7.1 UIO/CDEV 初始化与模块加载

用户 Glue：finit_module 加载 .ko → open cdev/uio → ioctl/UIO 传配置 → mmap shm → 创建 RX 线程。

### 5.7.2 发送与 IRQ 通知

Core（用户）ipcsShmTx → ipcsHwIrqNotify → UIO write 或 cdev ioctl → 内核 ipcsHwIrqNotify → MSCM。

### 5.7.3 接收路径

内核 ISR → 禁用/清除 IRQ → 唤醒用户（UIO event / cdev poll）→ 用户线程调用 rx_cb → ipcsShmRx。

## 5.8 Linux 全局变量与私有类型

用户态：struct IPCS_OS_PRIV_TYPE（os_uio/os_cdev ipc-os.c）。内核态：各模块 priv（ipc_cdev_priv、UIO priv 等）。详见源码 struct 定义。
"""

CH6 = """# 6 Traceability and Consistency Evidence 追溯与一致性证据

## 6.1 SWE.3 覆盖说明

| SWE.3 过程结果 / 实践 | 文档落点 |
|---|---|
| 详细设计描述软件单元 | §3–§5 Files 与各函数单元 |
| 定义软件单元接口 | §3.3 对外 API；§4/§5 OSAL/HAL；§2.6、§5.6 分布表 |
| 定义动态行为 | §3.7、§4.7、§5.7 及各函数 processing flow |
| 与架构双向追溯 | §6.2；§2.1–2.2 |
| 与架构设计一致 | §2 全章及 §2.6 Refinement 声明 |
| 软件单元可实现 | ipcs/ 源码路径与构建说明 |

## 6.2 架构—设计—源码追溯矩阵

| 架构组件 ID | L1/L2 | 主要源码 |
|---|---|---|
| Drv_Ipcs_Core_Cmp | 全部 | ipcs/ipcs_cores/ipc-shm.c |
| Drv_Ipcs_Queue_Cmp | 全部 | ipcs/ipcs_cores/ipc-queue.c |
| Drv_Ipcs_Conf_Cmp | 全部 | ipcs/ipcs_cores/ipc-types.h |
| Drv_Ipcs_Osal_Cmp | RTOS L2 | ipcs/mcu/os/*/ipc-os-*.c |
| Drv_Ipcs_Hal_Cmp | RTOS L2 | ipcs/mcu/hw/ipc-hw.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux 全内核 | ipcs/mpu/os_kernel/ipc-os.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux UIO | os_uio/ipc-os.c + os_kernel/ipc-uio.c |
| Drv_Ipcs_Linux_Adapt_Cmp | Linux CDEV | os_cdev/ipc-os.c + os_kernel/ipc-cdev.c |

## 6.3 源码核对结果

- 输入基准目录：ipcs/（ipcs_cores、mcu、mpu）
- 第 3 章函数设计覆盖 ipcs_cores 内 Core/Queue 单元
- 第 4 章覆盖 mcu 侧 OSAL/HAL（不含 Baremetal 详细设计）
- 第 5 章覆盖 mpu 三种 Linux 实现

## 6.4 对外/内部接口判定规则

| 类型 | 规则 |
|---|---|
| 对外（应用） | ipcs/ipcs_cores/ipc-shm.h 中声明且 ipcs-shm.c 中非 static 的 API |
| OSAL/HAL | 以 ipc-os.h、ipc-hw.h 声明；实现位置随部署变体见 §2.6、§5.6 |
| Glue | 对用户库导出符号，非应用直接调用；属 Linux Adapt 实现单元 |
| 内部 | static 函数及仅单元内使用的类型 |
"""


def transform_rtos_block(text: str) -> str:
    """将原 2744 行起的 RTOS 附录转为第 4 章结构。"""
    text = text.replace("# 3.2.9 ipc-hw-platform.h", "### 4.2.1 ipc-hw-platform.h")
    text = text.replace("## definition定义", "#### 文件私有数据（RTOS）")
    text = text.replace("## Files 文件", "#### 文件列表（RTOS MCU）")
    text = text.replace("| Drv_Ipcs_Osal_Cmp / Baremetal 变体 |", "| （Baremetal 不在本文档范围） |")
    text = text.replace("os/baremetal/ipc-os-baremetal.c", "—")
    text = text.replace("## HAL单元函数实现", "## 4.6 HAL 单元设计（MCU 共用）")
    text = text.replace("## OSAL(autosar OS)函数实现", "## 4.3 AUTOSAR OS 实现")
    text = text.replace("## OSAL(FREERTOS) 函数实现", "## 4.4 FreeRTOS 实现")
    text = text.replace("## OSAL(THREADX) 函数实现", "## 4.5 ThreadX 实现")
    text = text.replace("## Dynamic Detailed Design 动态详细设计", "## 4.7 RTOS 动态详细设计")
    text = text.replace("### TODO 核心场景流程", "### 4.7.1 核心场景流程（RTOS）")
    # 函数编号：HAL/OSAL 段保留原 3.4.x 以免大规模重写表格
    return text


def path_replace(text: str) -> str:
    repl = [
        ("IPCS_49/", "ipcs/"),
        ("common/ipc-", "ipcs/ipcs_cores/ipc-"),
        ("common/ipc-queue", "ipcs/ipcs_cores/ipc-queue"),
        ("| common/ipc", "| ipcs/ipcs_cores/ipc"),
        ("hw/ipc-hw", "ipcs/mcu/hw/ipc-hw"),
        ("ipcs/mcu/os/freertos", "ipcs/mcu/os/freertos"),  # idempotent
        ("ipcs/mcu/os/threadx", "ipcs/mcu/os/threadx"),
        ("ipcs/mcu/os/autosar", "ipcs/mcu/os/autosar"),
        # only prefix bare os/ paths under mcu context in tables
        ("| os/freertos", "| ipcs/mcu/os/freertos"),
        ("| os/threadx", "| ipcs/mcu/os/threadx"),
        ("| os/autosar", "| ipcs/mcu/os/autosar"),
        (" os/freertos/", " ipcs/mcu/os/freertos/"),
        (" os/threadx/", " ipcs/mcu/os/threadx/"),
        (" os/autosar/", " ipcs/mcu/os/autosar/"),
        (" os/ipc-os.h", " ipcs/mcu/os/ipc-os.h"),
    ]
    for a, b in repl:
        text = text.replace(a, b)
    return text


def main():
    lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)

    # 定位
    idx_contents = next(i for i, l in enumerate(lines) if l.startswith("## CONTENTS"))
    idx_ch1 = next(i for i, l in enumerate(lines) if l.startswith("# 1 INTRODUCTION"))
    idx_ch2 = next(i for i, l in enumerate(lines) if l.startswith("# 2 Software"))
    idx_ch3 = next(i for i, l in enumerate(lines) if l.startswith("# 3 Software"))
    idx_ch3_1 = next(i for i, l in enumerate(lines) if l.strip() == "## 3.1 Definition定义")
    idx_ch3_5 = next(i for i, l in enumerate(lines) if l.startswith("## 3.5 Gobal"))
    idx_ch3_7_old = next(i for i, l in enumerate(lines) if l.startswith("## 3.7 Dynamic"))
    idx_rtos_start = next(i for i, l in enumerate(lines) if l.startswith("# 3.2.9 ipc-hw-platform"))
    idx_linux = next(i for i, l in enumerate(lines) if l.startswith("# Linux部署变体"))

    header = "".join(lines[:idx_contents])
    ch1_ch2_through_23 = "".join(lines[idx_ch1:idx_ch3_1])
    idx_ch3_2 = next(i for i, l in enumerate(lines) if l.startswith("## 3.2 Files"))
    idx_ch3_6 = next(i for i, l in enumerate(lines) if l.startswith("## 3.6 Data Structure"))
    ch3_files_through_34 = "".join(lines[idx_ch3_2:idx_ch3_5])
    ch3_6_only = "".join(lines[idx_ch3_6:idx_ch3_7_old])

    rtos_block = "".join(lines[idx_rtos_start:idx_linux])
    rtos_block = transform_rtos_block(rtos_block)

    # 修订 ch1-ch2 片段
    intro = ch1_ch2_through_23
    intro = intro.replace(
        "为 IPCS Driver RTOS shared memory 实现建立软件详细设计",
        "为 IPCS Driver（RTOS 与 Linux 部署变体）建立软件详细设计",
    )
    intro = intro.replace(
        "## 1.3 Scope范围\n\n本文档适用于 IPCS_49/ 中的 IPC Shared Memory Driver for Real-Time Operating Systems 源码。该源码覆盖 IPCS-SHM 核心、队列与缓冲管理、OSAL 的 AutoSAR/Baremetal/FreeRTOS/Threadx 变体、HAL 的 MSCM 核间中断实现、公共配置数据类型和构建集成文件。\n\nipcs-architecture.pdf 中定义了 Linux 部署适配组件 Drv_Ipcs_Linux_Adapt_Cmp，但 IPCS_49/ 本次输入源码未包含 Linux 适配实现文件。因此本文只在架构边界中保留该组件名称，不对其软件单元、函数或数据结构进行实现级详细设计。",
        "## 1.3 Scope范围\n\n本文档适用于 ipcs/ 目录下的 IPC Shared Memory Driver 源码，包括：\n\n- ipcs/ipcs_cores/：跨部署变体共享的通信核心与队列；\n- ipcs/mcu/：RTOS 部署变体（FreeRTOS、ThreadX、AUTOSAR OS 实现，不含 Baremetal 详细设计）；\n- ipcs/mpu/：Linux 部署变体（全内核、UIO、CDEV 实现）。\n\n逻辑架构以 ipcs-architecture.pdf 为准；Linux 用户/内核划分以 §2.6 Refinement 描述。",
    )
    intro = intro.replace("| 4 | IPCS_49/ IPCF", "| 4 | ipcs/ IPCF")
    abbr_add = "\n| Deployment Variant | 部署变体（L1：RTOS / Linux） |\n| Implementation | 实现（L2：如 FreeRTOS 实现、UIO 实现） |\n| User-Space Glue | 用户态适配胶水（Linux UIO/CDEV 用户库内 OSAL/HAL 代理） |\n| Refinement | 架构细化：SDD 对逻辑组件的实现分解，不新增架构 ID |\n| In-Kernel | 全内核实现 |\n| CDEV | Character Device 实现 |\n"
    intro = intro.replace("| UIO | Userspace I/O |\n", "| UIO | Userspace I/O |\n" + abbr_add)

    arch = """IPCS Driver 软件架构采用 ipcs-architecture.pdf 中定义的分层与组件命名。实现源码位于 ipcs/：ipcs_cores 映射 IPCS-SHM 与配置类型；mcu 映射 RTOS 部署变体下 OSAL/HAL；mpu 映射 Linux 部署变体。

## 2.1 架构分层与组件

| 架构层级 | 组件 ID | 组件名称 | 本源码映射 | 职责 |
|---|---|---|---|---|
| IPCS-SHM | Drv_Ipcs_Core_Cmp | 通信核心组件 | ipcs/ipcs_cores/ipc-shm.c, ipc-shm.h | 提供对外 IPCS API；管理实例、通道、shared memory 布局与接收分发 |
| IPCS-SHM | Drv_Ipcs_Queue_Cmp | 队列与缓冲管理组件 | ipcs/ipcs_cores/ipc-queue.c, ipc-queue.h | 共享内存双环 lock-free FIFO |
| IPCS-OSAL | Drv_Ipcs_Osal_Cmp | OS 适配组件 | ipcs/mcu/os/（L2 实现三选一） | shared memory 视图、中断与 polling（RTOS） |
| IPCS-HAL | Drv_Ipcs_Hal_Cmp | HW 适配组件 | ipcs/mcu/hw/；Linux 为 mpu/hw/c1/ | MSCM 核间中断与 cache |
| 配置 | Drv_Ipcs_Conf_Cmp | 配置组件 | ipcs/ipcs_cores/ipc-types.h，外部 ipcf_Ip_Cfg*.h | instance/channel/IRQ 配置 |
| Linux 部署适配 | Drv_Ipcs_Linux_Adapt_Cmp | Linux 部署适配组件 | ipcs/mpu/ | 全内核 / UIO / CDEV；§2.6 细化 |

## 2.2 组件关系与端口

| 端口 | 接口 | 提供方 | 需要方 | 源码对应 |
|---|---|---|---|---|
| P1 | IF_AppSvc | Drv_Ipcs_Core_Cmp | 应用/集成层 | ipc-shm.h 中 9 个非 static API |
| P2 | IF_CfgIn | Drv_Ipcs_Conf_Cmp | Core / OSAL / HAL | IPCS_SHM_*_CFG_TYPE |
| P3 | IF_Queue | Drv_Ipcs_Queue_Cmp | Drv_Ipcs_Core_Cmp | ipcsQueueInit, Push, Pop 等 |
| P4 | IF_OSAbst | Drv_Ipcs_Osal_Cmp（逻辑） | Drv_Ipcs_Core_Cmp | ipcsOsInit, ipcsOsFree, ipcsOsGet*Shm, ipcsOsPollChannels |
| P5 | IF_HWAbst | Drv_Ipcs_Hal_Cmp（逻辑） | Core / OSAL | ipcsHwInit, ipcsHwIrq*, ipcsHwFlushCache* |
| P7 | IF_PlatformOS | OS 执行环境 | OSAL / Linux Adapt | FreeRTOS、ThreadX、AUTOSAR OS；Linux 内核/用户库 |
| P8 | IF_PlatformHW | HW 执行环境 | HAL | MSCM/IRQ |

注：Linux UIO/CDEV 下 P4/P5 符号在用户库中由 Glue 提供，特权操作在内核 Backend 完成（§2.6）。

## 2.3 运行场景

IPCS-SHM 初始化时按配置逐个 instance 调用 HAL 初始化、OSAL 初始化和 channel 初始化。发送路径中，managed channel 通过 pool queue 获取 buffer，发送时提交 BD 并触发 HAL 通知；unmanaged channel 递增 tx_count 并通知远端。接收路径由 OSAL 的 hardirq/softirq 或 polling 触发 Core 接收分发。Linux UIO/CDEV 实现中，Core 运行于用户态库，中断与 MSCM 访问在内核模块完成。
"""
    # 替换 2.1-2.3：从 intro 中提取 ch1 和 ch2 title
    idx_21 = intro.find("## 2.1")
    if idx_21 >= 0:
        intro = intro[:idx_21] + arch + CH2_EXTENSIONS

    # 3.2.1 仅 cores 文件
    files_list = """### 3.2.1 文件列表

| 组件 | 文件 |
|---|---|
| Drv_Ipcs_Queue_Cmp | ipcs/ipcs_cores/ipc-queue.c |
| Drv_Ipcs_Queue_Cmp | ipcs/ipcs_cores/ipc-queue.h |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-shm.c |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-shm.h |
| Drv_Ipcs_Conf_Cmp | ipcs/ipcs_cores/ipc-types.h |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-util.c |
| Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-util.h |

"""
    import re
    ch3_files = ch3_files_through_34
    ch3_files = re.sub(
        r"### 3\.2\.1 文件列表\n\n\| 组件 \| 文件 \|\n\|---\|---\|\n(?:\|[^\n]+\n)+",
        files_list.strip() + "\n\n",
        ch3_files,
        count=1,
    )

    out = []
    out.append(header)
    out.append(NEW_CONTENTS)
    out.append("\n")
    out.append(intro)
    out.append("\n# 3 公共详细设计（跨部署变体共享）\n\n")
    out.append(CH3_1_UPDATE)
    out.append("\n")
    out.append(ch3_files)
    out.append("\n")
    out.append(CH3_5_CORE)
    out.append("\n")
    out.append(ch3_6_only)
    out.append("\n")
    out.append(CH3_7)
    out.append("\n")
    out.append(CH4_HEADER)
    out.append(rtos_block)
    out.append("\n")
    out.append(CH5)
    out.append("\n")
    out.append(CH6)

    result = path_replace("".join(out))
    result = result.replace(
        "本节严格按照 reference.md 的函数说明表格格式描述外部接口。按照任务要求，只有 IPCS_49/common/ipc-shm.c 中的非静态接口为对外接口。",
        "本节描述对外应用接口（ipcs/ipcs_cores/ipc-shm.c 中非 static API）。",
    )
    # 清理 3.5 表中误入的 RTOS 行（若 path_replace 后仍存在）
    for stale in [
        "| ipc_hw_priv |",
        "| ipc_os_priv |",
        "| softirq_stack |",
    ]:
        pass  # CH3_5_CORE 已替换整节

    DST.write_text(result, encoding="utf-8")
    print(f"Wrote {DST} ({len(result)} chars)")


if __name__ == "__main__":
    main()
