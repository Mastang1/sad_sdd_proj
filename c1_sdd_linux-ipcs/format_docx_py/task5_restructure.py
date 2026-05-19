# -*- coding: utf-8 -*-
"""
task-5: 拆分第 2 章、新增第 3 章「三层架构与 Linux 适配架构」，顺延后续章号。
用法: python format_docx_py/task5_restructure.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "md_sdd_0519.md"

CH3_NEW = r'''# 3 IPCS Layered Architecture and Linux Adaptation Architecture
# 3 IPCS 三层架构与 Linux 适配架构

本章说明 IPCS **固定不变的三层接口契约**（SHM / OSAL / HAL）及 Linux 部署变体对 `Drv_Ipcs_Linux_Adapt_Cmp` 的两种实现形态。内容为 SDD 对架构 pdf 的**实现级细化**，不新增架构组件 ID。软件单元 ID 见 §2.2；各层详细函数设计见第 4–6 章。

## 3.1 Three-Layer Model and Interface Contracts（三层模型与接口契约）

IPCS 采用三层架构，层间通过**固定接口契约**耦合，契约在 RTOS 与 Linux 各 L2 实现间保持不变：

| 层级 | 架构组件 | 契约头文件 | 主要 API（示例） | 职责 |
|---|---|---|---|---|
| SHM 层 | Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp | ipc-shm.h、ipc-queue.h | ipcsShmInit、ipcsShmTx、ipcsQueuePush | 协议、通道、缓冲池、对外应用服务（P1/P3） |
| OSAL 层 | Drv_Ipcs_Osal_Cmp | ipc-os.h（RTOS）/ 用户库同名符号（Linux UIO/CDEV） | ipcsOsInit、ipcsOsGetLocalShm、ipcsOsPollChannels | 实例生命周期、共享内存视图、收包调度、中断上下文联结（P4） |
| HAL 层 | Drv_Ipcs_Hal_Cmp | ipc-hw.h | ipcsHwInit、ipcsHwIrqNotify、ipcsHwFlushCache* | MSCM/IRQ、缓存一致性、核索引（P5） |

**契约不变性**：`ipcs/ipcs_cores` 中的 Core 仅依赖 OSAL/HAL **头文件声明**的符号；不因部署变体改变调用序列或函数原型。配置类型由 Drv_Ipcs_Conf_Cmp（P2）注入。

层间调用关系（逻辑）：

```
应用 → [P1] ipcsShm* (SHM)
         → [P4] ipcsOs* (OSAL)
         → [P5] ipcsHw* (HAL) → [P8] 硬件
```

## 3.2 RTOS Deployment Variant（RTOS 部署变体层间实现）

RTOS 部署变体在**单地址空间**内分别实现 OSAL 与 HAL，与三层契约一一对应：

| 层级 | 软件单元 ID | 源文件 |
|---|---|---|
| SHM | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE | ipcs_cores/ipc-shm.c、ipc-queue.c |
| OSAL | SWU_IPCS_OSAL_*（随 L2） | mcu/os/{autosar,freertos,threadx}/ipc-os-*.c |
| HAL | SWU_IPCS_HAL_MCU | mcu/hw/ipc-hw.c |

Core 对 `ipcsOs*` / `ipcsHw*` 的调用直接进入真实实现，**无代理层**。

## 3.3 Linux Adapt Component and Two Implementation Patterns（Linux 适配组件与两种实现形态）

架构基线（`ipcs-architecture.pdf`）将 Linux 侧 OS/硬件相关能力归纳为逻辑组件 **Drv_Ipcs_Linux_Adapt_Cmp**。为满足 §3.1 中 OSAL/HAL **接口契约**，SDD 定义两种 L2 实现形态：

| L2 实现 | 形态概要 | Linux 适配组件物理构成 |
|---|---|---|
| **UIO 实现** / **CDEV 实现** | 用户态库 + 内核模块 | **用户侧代理**（满足 P4/P5 契约）+ **内核侧真实 OSAL/HW 实现** |
| **全内核实现** | 单内核模块，无用户代理 | **内核 OSAL**（`mpu/os_kernel/ipc-os.c`）+ **内核 HAL**（`mpu/hw/c1/ipc-hw.c`），与 RTOS 同态 |

## 3.4 UIO/CDEV：User-Side Proxy and Kernel-Side Implementation（用户侧代理与内核侧实现）

适用于 **UIO 实现**、**CDEV 实现**（`ipcs/mpu/os_uio/`、`ipcs/mpu/os_cdev/` + `ipcs/mpu/os_kernel/`）。

### 3.4.1 设计原则

1. **用户侧接口契约**：用户库导出与 RTOS **相同原型** 的 `ipcsOs*`、`ipcsHw*`（见 `mpu/os_uio/ipc-os.h` 或 `mpu/os_cdev/ipc-os.h`），Core（`ipcs_cores`）链接用户库时层间契约与 RTOS 一致。
2. **用户侧实现本质**：对 **操作系统能力**（模块加载、mmap、pthread、ioctl/UIO 等）与 **硬件操作**（IRQ 通知等）的**代理**；`ipcsHwInit`/`ipcsHwFree` 等可为空实现或转发桩，注释标明特权逻辑在内核。
3. **内核侧真实实现**：`ipc-uio.c` / `ipc-cdev.c` 完成实例注册、ISR、wait_queue/UIO 回调；**真实** `ipcsHw*` 在 `mpu/hw/c1/ipc-hw.c` 中实现（MSCM、IRQ 使能/通知/清除等）。

### 3.4.2 软件单元划分（UIO/CDEV）

| 角色 | SW-Unit-ID | 源文件 | 与三层契约关系 |
|---|---|---|---|
| SHM（用户库内嵌 Core） | SWU_IPCS_CORE_* | ipcs_cores/* | 与 §3.1 SHM 层一致 |
| Linux Adapt — 用户侧代理 | SWU_IPCS_LINUX_OS_UIO 或 SWU_IPCS_LINUX_OS_CDEV | mpu/os_uio/ipc-os.c 或 mpu/os_cdev/ipc-os.c | **满足** P4/P5 **契约**；实现为代理 |
| Linux Adapt — 内核 Backend | SWU_IPCS_LINUX_UIO_KO 或 SWU_IPCS_LINUX_CDEV_KO | mpu/os_kernel/ipc-uio.c 或 ipc-cdev.c | 内核 OS 集成、唤醒用户收包 |
| HAL（内核） | SWU_IPCS_HAL_LINUX | mpu/hw/c1/ipc-hw.c | **真实** P5 实现 |

逻辑组件映射：`Drv_Ipcs_Linux_Adapt_Cmp` = 用户侧代理单元 + 内核 Backend 单元 + 协同 HAL；**不**将用户代理误标为完整 OSAL/HAL 实现。

### 3.4.3 典型调用链（发送侧）

`ipcsShmTx`（用户 Core）→ `ipcsHwIrqNotify`（用户**代理**）→ UIO write / cdev ioctl → 内核 `ipcsHwIrqNotify`（`ipc-hw.c`）→ MSCM。

## 3.5 In-Kernel Implementation: Same Form as RTOS（全内核实现）

适用于 **全内核实现**（`ipcs/mpu/os_kernel/ipc-os.c` + `ipcs/mpu/hw/c1/ipc-hw.c`）。

- **无用户侧代理**：Core、OSAL、HAL 均链接入内核模块（如 `ipc-shm-dev.ko`），应用通过内核导出接口或配套模块 API 使用。
- **Linux 适配组件**由以下两单元构成，与 RTOS 一样在**同一特权域**完成 P4/P5，仅 OS 环境不同：
  - **OSAL 实现**：`ipcs/mpu/os_kernel/ipc-os.c`（`SWU_IPCS_LINUX_OS_KERN`）
  - **HAL 实现**：`ipcs/mpu/hw/c1/ipc-hw.c`（`SWU_IPCS_HAL_LINUX`）
- 层间契约仍按 §3.1；Core 在内核内调用 `ipcsOs*` / `ipcsHw*`，**无**跨用户/内核代理。

## 3.6 Interface Contract vs Implementation Location（契约与实现位置对照）

| API（P4/P5） | RTOS | Linux UIO/CDEV 用户侧 | Linux UIO/CDEV 内核侧 | Linux 全内核 |
|---|---|---|---|---|
| ipcsOsInit / ipcsOsFree | mcu/os/*/ipc-os-*.c | os_uio/os_cdev ipc-os.c（代理） | ipc-uio.c / ipc-cdev.c | os_kernel/ipc-os.c |
| ipcsOsGetLocalShm / GetRemoteShm | 真实映射 | mmap /dev/mem（代理） | — | os_kernel/ipc-os.c |
| ipcsOsPollChannels | 真实调度 | 用户 RX 线程 + UIO read / poll（代理） | ISR 唤醒 | os_kernel/ipc-os.c |
| ipcsHwInit / ipcsHwFree | ipc-hw.c | dummy / 注释由内核处理 | ipc-hw.c（init 路径） | ipc-hw.c |
| ipcsHwIrqEnable/Disable/Notify/Clear | ipc-hw.c | UIO write / ioctl（代理） | ipc-hw.c | ipc-hw.c |
| ipcsHwFlushCache* | ipc-hw.c | 按需代理或内核 | ipc-hw.c | ipc-hw.c |

'''

CONTENTS_OLD = """- 2 Architectural Compliance and Software Unit Identification 架构符合性与软件单元划分
  - 2.1 Compliance with Software Architectural Design（SWE.2 符合性）
  - 2.2 Software Unit Identification（软件单元划分）
  - 2.3 Component ID to Software Unit Mapping（组件→单元映射）
  - 2.4 Deployment Variants（部署变体 L1/L2）
  - 2.5 External Dependencies（外部依赖）
  - 2.6 Linux Implementation Refinement（Linux 实现细化）
- 3 公共详细设计（跨部署变体共享）"""

CONTENTS_NEW = """- 2 Architectural Compliance and Software Unit Identification 架构符合性与软件单元划分
  - 2.1 Compliance with Software Architectural Design（SWE.2 符合性）
  - 2.2 Software Unit Identification（软件单元划分）
  - 2.3 Component ID to Software Unit Mapping（组件→单元映射）
  - 2.4 Deployment Variants（部署变体 L1/L2）
  - 2.5 External Dependencies（外部依赖）
- 3 IPCS Layered Architecture and Linux Adaptation Architecture IPCS 三层架构与 Linux 适配架构
  - 3.1 Three-Layer Model and Interface Contracts（三层模型与接口契约）
  - 3.2 RTOS Deployment Variant（RTOS 部署变体层间实现）
  - 3.3 Linux Adapt Component and Two Implementation Patterns（Linux 适配组件与两种实现形态）
  - 3.4 UIO/CDEV：User-Side Proxy and Kernel-Side Implementation（用户侧代理与内核侧实现）
  - 3.5 In-Kernel Implementation（全内核实现）
  - 3.6 Interface Contract vs Implementation Location（契约与实现位置对照）
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
  - 6.1 与架构关系及实现形态
  - 6.2 源码与构建结构
  - 6.3 全内核实现
  - 6.4 UIO 实现
  - 6.5 CDEV 实现
  - 6.6 接口实现分布表
  - 6.7 Linux 动态详细设计
  - 6.8 Linux 全局变量与私有类型
- 7 Traceability and Consistency Evidence 追溯与一致性证据
  - 7.1 SWE.3 覆盖说明
  - 7.2 架构—设计—源码追溯矩阵
  - 7.3 源码核对结果
  - 7.4 接口判定规则"""

CH2_INTRO_OLD = (
    "本章满足 ASPICE SWE.3 对详细设计与软件架构（SWE.2）一致性的要求。**权威软件架构基线**为参考文献 [2] "
    "`ipcs-architecture.pdf`（组件 ID、端口 P1–P8）。本章不另立架构基线，仅提供：**架构符合性摘要**、"
    "**软件单元划分**、**组件 ID→软件单元 ID 映射**，以及 SDD 特有的部署与 Linux 实现细化。"
)

CH2_INTRO_NEW = (
    "本章满足 ASPICE SWE.3 对详细设计与软件架构（SWE.2）一致性的要求，**功能限定**为：与 SWE.2 基线的一致性声明、"
    "软件单元划分、组件—单元映射、部署变体索引及外部依赖。**权威架构基线**为参考文献 [2] `ipcs-architecture.pdf`。"
    "三层接口契约及 Linux 适配的两种实现形态见 **第 3 章**；跨变体共享与变体专属详细设计见第 4–6 章。"
)


def remove_section_26(md: str) -> str:
    start = md.find("## 2.6 Linux Implementation Refinement")
    end = md.find("\n# 3 公共详细设计")
    if start < 0 or end < 0:
        raise RuntimeError("2.6 or ch3 marker not found")
    return md[:start].rstrip() + "\n\n" + md[end + 1 :]


def bump_chapter_numbers(md: str) -> str:
    """旧 3–6 章 → 4–7 章（先高后低，避免重复替换）。"""
    for old, new in [(6, 7), (5, 6), (4, 5), (3, 4)]:
        md = re.sub(rf"^# {old} ", f"# {new} ", md, flags=re.M)
        md = re.sub(rf"^## {old}\.", f"## {new}.", md, flags=re.M)
        md = re.sub(rf"^### {old}\.", f"### {new}.", md, flags=re.M)
        md = re.sub(rf"^#### {old}\.", f"#### {new}.", md, flags=re.M)
    return md


def update_cross_refs(md: str) -> str:
    """仅替换明确指向旧章节的引用，避免误改新第 3 章内的 §3.x。"""
    reps = [
        ("第 3–5 章", "第 4–6 章"),
        ("第 4、5 章", "第 5、6 章"),
        ("见第 4、5 章", "见第 5、6 章"),
        ("§3–§5", "§4–§6"),
        ("§2.1–2.2", "§2.1–2.3"),
        ("Linux 用户/内核划分以 §2.6", "Linux 用户/内核划分以 §3.4–§3.5"),
        ("§3.4.1–3.4.5", "§4.4.1–4.4.5"),
        ("§3.3、§3.4（Core", "§4.3、§4.4（Core"),
        ("§4.6 HAL", "§5.6 HAL"),
        ("§4.2、§4.6", "§5.2、§5.6"),
        ("§5、§2.6", "§6、§3.6"),
        ("§5.4–5.5", "§6.4–6.5"),
        ("§5.3", "§6.3"),
        ("§5.4", "§6.4"),
        ("§4.3", "§5.3"),
        ("§4.4", "§5.4"),
        ("§4.5", "§5.5"),
        ("与架构双向追溯 | §6.2", "与架构双向追溯 | §7.2"),
        ("与架构设计一致 | §2 全章", "与架构设计一致 | §2–§3"),
        ("§2.6、§5.6", "§3.6、§6.6"),
        ("§2.6、§6.6", "§3.6、§6.6"),
        ("见 §2.6、§6.6", "见 §3.6、§6.6"),
    ]
    for a, b in reps:
        md = md.replace(a, b)
    return md


def patch_ch2_mapping(md: str) -> str:
    old = """| Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_*（RTOS）或 SWU_IPCS_LINUX_OS_*（Linux 用户 Glue）+ 内核协同 | 随 L2 实现切换 |
| Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU 或 SWU_IPCS_HAL_LINUX | RTOS 单址空间；Linux 特权访问在内核 |
| Drv_Ipcs_Linux_Adapt_Cmp | SWU_IPCS_LINUX_* 组合 | 全内核：KERN+HAL_LINUX；UIO/CDEV：OS_UIO/CDEV + UIO_KO/CDEV_KO + HAL_LINUX |"""
    new = """| Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_*（RTOS）；Linux 全内核：SWU_IPCS_LINUX_OS_KERN；Linux UIO/CDEV：用户库**契约代理** + 内核 Backend | 见 §3.1、§3.4–§3.5 |
| Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU（RTOS）；SWU_IPCS_HAL_LINUX（Linux 内核真实实现） | Linux UIO/CDEV 用户侧为 P5 **代理** |
| Drv_Ipcs_Linux_Adapt_Cmp | 见 §3.3 | **全内核**：`os_kernel/ipc-os.c` + `hw/c1/ipc-hw.c`；**UIO/CDEV**：用户代理 + `ipc-uio.c`/`ipc-cdev.c` + `ipc-hw.c` |"""
    return md.replace(old, new)


def patch_unit_table_notes(md: str) -> str:
    old = "| SWU_IPCS_LINUX_OS_UIO | mpu/os_uio/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / UIO 实现（User Glue） |"
    new = "| SWU_IPCS_LINUX_OS_UIO | mpu/os_uio/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / UIO 实现（**用户侧 P4/P5 契约代理**） |"
    md = md.replace(old, new)
    old2 = "| SWU_IPCS_LINUX_OS_CDEV | mpu/os_cdev/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / CDEV 实现（User Glue） |"
    new2 = "| SWU_IPCS_LINUX_OS_CDEV | mpu/os_cdev/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / CDEV 实现（**用户侧 P4/P5 契约代理**） |"
    md = md.replace(old2, new2)
    old3 = "| SWU_IPCS_LINUX_OS_KERN | mpu/os_kernel/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / 全内核实现 |"
    new3 = "| SWU_IPCS_LINUX_OS_KERN | mpu/os_kernel/ipc-os.c | Drv_Ipcs_Osal_Cmp（逻辑）/ Linux Adapt | Linux / 全内核 **OSAL 实现**（无用户代理） |"
    return md.replace(old3, new3)


def patch_ch4_definition(md: str) -> str:
    """原 3.1 Definition：Glue 定义改为引用第 3 章。"""
    old = """**User-Space Adaptation Glue（用户态适配胶水）**：Linux UIO/CDEV 实现中，于用户库内提供与 RTOS 同名的 `ipcsOs*`/`ipcsHw*` 符号；其中 `ipcsHwInit/Free` 为空实现，IRQ 相关 API 通过 ioctl 或 UIO 命令转发至内核 Backend。该单元为 Drv_Ipcs_Linux_Adapt_Cmp 的 SDD 实现子单元，非架构 pdf 新增组件。

本章描述 **跨部署变体共享** 的 Core、Queue、配置类型；RTOS/Linux 专属 OSAL/HAL 见第 4、5 章。"""
    new = """本章描述 **跨部署变体共享** 的 Core、Queue、配置类型（SHM 层）。OSAL/HAL 接口契约及 Linux 用户侧代理与内核实现划分见 **§3.1–§3.6**；RTOS 专属实现见第 5 章；Linux 变体实现见第 6 章。"""
    return md.replace(old, new)


def patch_linux_ch(md: str) -> str:
    old51 = """## 6.1 与架构关系及 Refinement

逻辑架构见 ipcs-architecture.pdf 中 Drv_Ipcs_Linux_Adapt_Cmp。实现级用户/内核划分见 **§3.6**，本节给出三种 L2 实现的文件与行为说明。"""
    new51 = """## 6.1 与架构关系及实现形态

逻辑架构见 `ipcs-architecture.pdf` 中 **Drv_Ipcs_Linux_Adapt_Cmp**。三层契约与两种实现形态（用户侧代理 + 内核实现 / 全内核同 RTOS 态）见 **第 3 章**。本节给出三种 L2 实现的源码与行为说明。"""
    md = md.replace(old51, new51)

    old53 = """## 6.3 全内核实现

驱动逻辑（Core、OSAL、HAL）均位于内核模块 `ipc-shm-dev.ko`（os_kernel/ipc-os.c 与 mpu/hw/c1/ipc-hw.c）。应用通过内核导出符号或配套接口使用，无用户态 Glue。中断采用 tasklet 延迟处理（ipcsShmSoftirq）。"""
    new53 = """## 6.3 全内核实现

**Linux 适配组件**由内核中以下两文件构成（**无用户侧代理**，层间形态与 RTOS 一致）：

| 单元 | 源文件 | 层级 |
|---|---|---|
| SWU_IPCS_LINUX_OS_KERN | `ipcs/mpu/os_kernel/ipc-os.c` | OSAL（P4）真实实现 |
| SWU_IPCS_HAL_LINUX | `ipcs/mpu/hw/c1/ipc-hw.c` | HAL（P5）真实实现 |

Core（`ipcs_cores`）与上述单元链接入内核模块 `ipc-shm-dev.ko`。应用通过内核导出符号或配套接口使用。中断采用 tasklet 延迟处理（`ipcsShmSoftirq`）。"""
    md = md.replace(old53, new53)

    old54 = """### 6.4.1 User-Space Glue

文件：ipcs/mpu/os_uio/ipc-os.c。职责：模块加载、/dev/mem mmap 共享内存、打开 UIO 设备、pthread 收包线程；`ipcsHw*` 经 `write(uio_fd, cmd)` 转发（ipcsSendUioCmd）。"""
    new54 = """### 6.4.1 用户侧代理（User-Side Proxy）

文件：`ipcs/mpu/os_uio/ipc-os.c`（SWU_IPCS_LINUX_OS_UIO）。**接口契约**：导出与 RTOS 同原型的 `ipcsOs*`/`ipcsHw*`，供 Core 链接。**实现**：对 OS（finit_module、mmap、pthread）与 HW（经 UIO 的 IRQ 命令）的**代理**；`ipcsHwInit`/`ipcsHwFree` 为空实现，IRQ 经 `write(uio_fd, cmd)`（`ipcsSendUioCmd`）转发至内核。"""
    md = md.replace(old54, new54)

    old542 = """### 6.4.2 Kernel Backend

文件：ipcs/mpu/os_kernel/ipc-uio.c、ipcs/mpu/hw/c1/ipc-hw.c。职责：UIO 注册、hardirq（ipcsShmUioHandler）、irqcontrol 中调用真实 ipcsHwIrqEnable/Disable/Notify。"""
    new542 = """### 6.4.2 内核侧实现（Kernel Backend + HAL）

| 文件 | 单元 | 职责 |
|---|---|---|
| `ipcs/mpu/os_kernel/ipc-uio.c` | SWU_IPCS_LINUX_UIO_KO | UIO 注册、hardirq（`ipcsShmUioHandler`）、实例与唤醒用户收包 |
| `ipcs/mpu/hw/c1/ipc-hw.c` | SWU_IPCS_HAL_LINUX | **真实** `ipcsHwIrqEnable/Disable/Notify/Clear` 及 MSCM 访问 |"""
    md = md.replace(old542, new542)

    old55 = """### 6.5.1 User-Space Glue

文件：ipcs/mpu/os_cdev/ipc-os.c。职责：打开 /dev/ipc-shm-cdev、ioctl 初始化实例；`ipcsHwIrqEnable/Disable/Notify` 使用 IPC_CDEV_CMD_* ioctl。"""
    new55 = """### 6.5.1 用户侧代理（User-Side Proxy）

文件：`ipcs/mpu/os_cdev/ipc-os.c`（SWU_IPCS_LINUX_OS_CDEV）。**契约**同 §6.4.1；**实现**：打开 `/dev/ipc-shm-cdev`、ioctl 初始化；`ipcsHwIrqEnable/Disable/Notify` 以 `IPC_CDEV_CMD_*` ioctl **代理**至内核。"""
    md = md.replace(old55, new55)

    old552 = """### 6.5.2 Kernel Backend

文件：ipcs/mpu/os_kernel/ipc-cdev.c。职责：字符设备、wait_queue、ISR 与 ioctl 处理。"""
    new552 = """### 6.5.2 内核侧实现（Kernel Backend + HAL）

| 文件 | 单元 | 职责 |
|---|---|---|
| `ipcs/mpu/os_kernel/ipc-cdev.c` | SWU_IPCS_LINUX_CDEV_KO | 字符设备、wait_queue、ISR、ioctl |
| `ipcs/mpu/hw/c1/ipc-hw.c` | SWU_IPCS_HAL_LINUX | **真实** HAL（P5） |"""
    md = md.replace(old552, new552)

    old56 = """## 6.6 接口实现分布表

完整映射见 **§3.6** 表；UIO/CDEV 用户态 `ipcsHwInit/Free` 为 dummy，注释标明由内核模块处理。"""
    new56 = """## 6.6 接口实现分布表

完整 **契约 vs 实现位置** 见 **§3.6**。UIO/CDEV 用户态 `ipcsHwInit/Free` 为 dummy，特权逻辑在 `ipc-hw.c` 与 Backend 模块中完成。"""
    return md.replace(old56, new56)


def patch_ch7_traceability(md: str) -> str:
    """更新第 7 章（原第 6 章）目录与 SWE.3 表。"""
    md = md.replace(
        "- 6 Traceability and Consistency Evidence 追溯与一致性证据\n"
        "  - 6.1 SWE.3 覆盖说明\n"
        "  - 6.2 架构—设计—源码追溯矩阵\n"
        "  - 6.3 源码核对结果\n"
        "  - 6.4 接口判定规则",
        "- 7 Traceability and Consistency Evidence 追溯与一致性证据\n"
        "  - 7.1 SWE.3 覆盖说明\n"
        "  - 7.2 架构—设计—源码追溯矩阵\n"
        "  - 7.3 源码核对结果\n"
        "  - 7.4 接口判定规则",
    )
    md = md.replace(
        "| 详细设计描述软件单元 | §3–§5 Files 与各函数单元 |",
        "| 详细设计描述软件单元 | §4–§6 Files 与各函数单元 |",
    )
    md = md.replace(
        "| 定义软件单元接口 | §3.3 对外 API；§4/§5 OSAL/HAL；§2.6、§5.6 分布表 |",
        "| 定义软件单元接口 | §4.3 对外 API；§5/§6 OSAL/HAL；§3.6、§6.6 分布表 |",
    )
    md = md.replace(
        "| 定义动态行为 | §3.7、§4.7、§5.7 及各函数 processing flow |",
        "| 定义动态行为 | §4.7、§5.7、§6.7 及各函数 processing flow |",
    )
    md = md.replace(
        "| 与架构双向追溯 | §6.2；§2.1–2.2 |",
        "| 与架构双向追溯 | §7.2；§2.1–2.3；§3 |",
    )
    md = md.replace(
        "| 与架构设计一致 | §2 全章及 §2.6 Refinement 声明 |",
        "| 与架构设计一致 | §2–§3（契约与 Linux 适配形态） |",
    )
    md = md.replace("## 6.1 SWE.3", "## 7.1 SWE.3")
    md = md.replace("## 6.2 架构", "## 7.2 架构")
    md = md.replace("### 6.2.1", "### 7.2.1")
    md = md.replace("## 6.3 源码", "## 7.3 源码")
    md = md.replace("## 6.4 对外", "## 7.4 对外")
    md = md.replace(
        "| SWU_IPCS_CORE_SHM | §3.3、§3.4（Core 内部函数） |",
        "| SWU_IPCS_CORE_SHM | §4.3、§4.4（Core 内部函数） |",
    )
    md = md.replace(
        "| SWU_IPCS_CORE_QUEUE | §3.4.1–3.4.5 |",
        "| SWU_IPCS_CORE_QUEUE | §4.4.1–4.4.5 |",
    )
    md = md.replace(
        "| SWU_IPCS_HAL_MCU | §4.6 HAL、§4.3–4.5 OSAL |",
        "| SWU_IPCS_HAL_MCU | §5.6 HAL、§5.3–5.5 OSAL |",
    )
    md = md.replace(
        "| SWU_IPCS_LINUX_OS_UIO | §5.4 |",
        "| SWU_IPCS_LINUX_OS_UIO | §6.4（用户侧代理） |",
    )
    md = md.replace(
        "ipcs/ipcs_cores/ipc-shm.c | §3.2、§3.3–3.4 |",
        "ipcs/ipcs_cores/ipc-shm.c | §4.2、§4.3–4.4 |",
    )
    md = md.replace(
        "ipcs/ipcs_cores/ipc-queue.c | §3.2、§3.4.1–3.4.5 |",
        "ipcs/ipcs_cores/ipc-queue.c | §4.2、§4.4.1–4.4.5 |",
    )
    md = md.replace(
        "ipcs/ipcs_cores/ipc-util.c | §3.2、§3.4.23 |",
        "ipcs/ipcs_cores/ipc-util.c | §4.2、§4.4.23 |",
    )
    md = md.replace(
        "ipcs/ipcs_cores/ipc-types.h | §3.6 |",
        "ipcs/ipcs_cores/ipc-types.h | §4.6 |",
    )
    md = md.replace(
        "ipcs/mcu/hw/ipc-hw.c | §4.2、§4.6 |",
        "ipcs/mcu/hw/ipc-hw.c | §5.2、§5.6 |",
    )
    md = md.replace(
        "ipcs/mcu/os/autosar/ipc-os-autosar.c | §4.3 |",
        "ipcs/mcu/os/autosar/ipc-os-autosar.c | §5.3 |",
    )
    md = md.replace(
        "ipcs/mcu/os/freertos/ipc-os-freertos.c | §4.4 |",
        "ipcs/mcu/os/freertos/ipc-os-freertos.c | §5.4 |",
    )
    md = md.replace(
        "ipcs/mcu/os/threadx/ipc-os-threadx.c | §4.5 |",
        "ipcs/mcu/os/threadx/ipc-os-threadx.c | §5.5 |",
    )
    md = md.replace(
        "ipcs/mpu/os_kernel/ipc-os.c | §5.3 |",
        "ipcs/mpu/os_kernel/ipc-os.c | §6.3（全内核 OSAL） |",
    )
    md = md.replace(
        "ipcs/mpu/os_uio/ipc-os.c | §5.4 | UIO 用户 Glue |",
        "ipcs/mpu/os_uio/ipc-os.c | §6.4 | UIO 用户侧 P4/P5 代理 |",
    )
    md = md.replace(
        "ipcs/mpu/os_cdev/ipc-os.c | §5.5 | CDEV 用户 Glue |",
        "ipcs/mpu/os_cdev/ipc-os.c | §6.5 | CDEV 用户侧 P4/P5 代理 |",
    )
    md = md.replace(
        "ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c | §5.4–5.5 |",
        "ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c | §6.4–6.5 |",
    )
    md = md.replace(
        "ipcs/mpu/hw/c1/ipc-hw.c | §5、§2.6 |",
        "ipcs/mpu/hw/c1/ipc-hw.c | §6、§3.6 | Linux 内核 HAL 真实实现 |",
    )
    md = md.replace(
        "实现位置随部署变体见 §2.6、§5.6 |",
        "实现位置随部署变体见 §3.6、§6.6 |",
    )
    md = md.replace(
        "| Glue | 对用户库导出符号，非应用直接调用；属 Linux Adapt 实现单元 |",
        "| 用户侧代理 | 用户库内 `ipcsOs*`/`ipcsHw*` 满足 P4/P5 契约，实现为转发；属 Linux Adapt（§3.4） |",
    )
    return md


def add_version_row(md: str) -> str:
    if "V0.4" in md:
        return md
    row = "| V0.4 | 2026.5.19 | Cursor Agent | Draft | 拆分第 2 章；新增第 3 章三层架构与 Linux 适配；勘误 UIO/CDEV 代理与全内核形态 |\n"
    return md.replace(
        "| V0.3 | 2026.5.19 | Cursor Agent | Draft | 第 2 章改为架构符合性与软件单元划分",
        row + "| V0.3 | 2026.5.19 | Cursor Agent | Draft | 第 2 章改为架构符合性与软件单元划分",
    )


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    md = md.replace(CONTENTS_OLD, CONTENTS_NEW)
    md = md.replace(CH2_INTRO_OLD, CH2_INTRO_NEW)
    md = md.replace(
        "| SDD 与架构关系 | 第 3–5 章各函数/文件设计均可追溯至下表软件单元 ID 及架构组件 ID（见 §2.3、§6.2） |",
        "| SDD 与架构关系 | 第 4–6 章各函数/文件设计可追溯至软件单元 ID 及架构组件 ID（§2.3、§3、§7.2） |",
    )
    md = patch_ch2_mapping(md)
    md = patch_unit_table_notes(md)
    md = remove_section_26(md)
    md = bump_chapter_numbers(md)
    # 在旧第 3 章（现第 4 章）前插入新第 3 章
    marker = "# 4 公共详细设计"
    if marker not in md:
        raise RuntimeError("chapter 4 marker missing after bump")
    md = md.replace(marker, CH3_NEW + "\n" + marker, 1)
    md = patch_ch4_definition(md)
    md = patch_linux_ch(md)
    md = update_cross_refs(md)
    md = patch_ch7_traceability(md)
    md = add_version_row(md)
    MD.write_text(md, encoding="utf-8")
    print(f"Wrote {MD}")


if __name__ == "__main__":
    main()
