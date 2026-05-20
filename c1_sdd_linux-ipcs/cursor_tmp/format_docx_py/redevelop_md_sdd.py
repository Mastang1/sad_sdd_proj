# -*- coding: utf-8 -*-
"""
按 ASPICE SWE.3 要求重构 md_sdd_0519.md：
- 第 2 章改为「架构符合性与软件单元划分」（非 SWE.2 架构章）
- 增加软件单元 ID、组件-单元映射
- 全部插图改为 SVG
- 修正源码路径与函数表单元 ID

用法: python format_docx_py/redevelop_md_sdd.py
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

MD = MD_SDD_0519
import re
from pathlib import Path


CH2_NEW = r'''# 2 Architectural Compliance and Software Unit Identification
# 2 架构符合性与软件单元划分

本章满足 ASPICE SWE.3 对详细设计与软件架构（SWE.2）一致性的要求。**权威软件架构基线**为参考文献 [2] `ipcs-architecture.pdf`（组件 ID、端口 P1–P8）。本章不另立架构基线，仅提供：**架构符合性摘要**、**软件单元划分**、**组件 ID→软件单元 ID 映射**，以及 SDD 特有的部署与 Linux 实现细化。

## 2.1 Compliance with Software Architectural Design（SWE.2 符合性）

| 项 | 说明 |
|---|---|
| 架构基线文档 | ipcs-architecture.pdf（参考文献 [2]） |
| 组件 ID | Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp、Drv_Ipcs_Osal_Cmp、Drv_Ipcs_Hal_Cmp、Drv_Ipcs_Conf_Cmp、Drv_Ipcs_Linux_Adapt_Cmp |
| 端口 | P1 IF_AppSvc、P2 IF_CfgIn、P3 IF_Queue、P4 IF_OSAbst、P5 IF_HWAbst、P7 IF_PlatformOS、P8 IF_PlatformHW |
| SDD 与架构关系 | 第 3–5 章各函数/文件设计均可追溯至下表软件单元 ID 及架构组件 ID（见 §2.3、§6.2） |

架构静态结构、组件职责与运行场景的完整描述见 `ipcs-architecture.pdf`；下列端口与源码对应关系为评审追溯摘要：

| 端口 | 接口 | 提供方（架构组件） | 需要方 | 源码实现入口 |
|---|---|---|---|---|
| P1 | IF_AppSvc | Drv_Ipcs_Core_Cmp | 应用/集成层 | ipcs/ipcs_cores/ipc-shm.h 非 static API |
| P2 | IF_CfgIn | Drv_Ipcs_Conf_Cmp | Core / OSAL / HAL | IPCS_SHM_*_CFG_TYPE、ipcf_Ip_Cfg*.h |
| P3 | IF_Queue | Drv_Ipcs_Queue_Cmp | Drv_Ipcs_Core_Cmp | ipcs/ipcs_cores/ipc-queue.c |
| P4 | IF_OSAbst | Drv_Ipcs_Osal_Cmp（逻辑） | Drv_Ipcs_Core_Cmp | ipcs/mcu/os/* 或 ipcs/mpu/os_*（见 §2.3） |
| P5 | IF_HWAbst | Drv_Ipcs_Hal_Cmp（逻辑） | Core / OSAL | ipcs/mcu/hw/ 或 ipcs/mpu/hw/c1/ |
| P7 | IF_PlatformOS | OS 执行环境 | OSAL / Linux Adapt | 见 §2.5 |
| P8 | IF_PlatformHW | HW 执行环境 | HAL | MSCM/IRQ |

## 2.2 Software Unit Identification（软件单元划分）

软件单元按**源文件/编译单元**划分，每个单元分配唯一 **SW-Unit-ID**，供第 3–5 章详细设计引用。

| SW-Unit-ID | 源文件（ipcs/） | 架构组件 ID | 部署变体（L1/L2） |
|---|---|---|---|
| SWU_IPCS_CORE_SHM | ipcs_cores/ipc-shm.c | Drv_Ipcs_Core_Cmp | 全部（Linux 用户库或内核内嵌） |
| SWU_IPCS_CORE_QUEUE | ipcs_cores/ipc-queue.c | Drv_Ipcs_Queue_Cmp | 全部 |
| SWU_IPCS_CORE_UTIL | ipcs_cores/ipc-util.c | Drv_Ipcs_Core_Cmp | 全部 |
| SWU_IPCS_CORE_TYPES | ipcs_cores/ipc-types.h | Drv_Ipcs_Conf_Cmp | 全部 |
| SWU_IPCS_HAL_MCU | mcu/hw/ipc-hw.c | Drv_Ipcs_Hal_Cmp | RTOS 部署变体 |
| SWU_IPCS_HAL_LINUX | mpu/hw/c1/ipc-hw.c | Drv_Ipcs_Hal_Cmp | Linux 部署变体（内核） |
| SWU_IPCS_OSAL_AUTOSAR | mcu/os/autosar/ipc-os-autosar.c | Drv_Ipcs_Osal_Cmp | RTOS / AUTOSAR OS 实现 |
| SWU_IPCS_OSAL_FREERTOS | mcu/os/freertos/ipc-os-freertos.c | Drv_Ipcs_Osal_Cmp | RTOS / FreeRTOS 实现 |
| SWU_IPCS_OSAL_THREADX | mcu/os/threadx/ipc-os-threadx.c | Drv_Ipcs_Osal_Cmp | RTOS / ThreadX 实现 |
| SWU_IPCS_OSAL_HDR | mcu/os/ipc-os.h | Drv_Ipcs_Osal_Cmp | RTOS（接口声明） |
| SWU_IPCS_LINUX_OS_UIO | mpu/os_uio/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / UIO 实现（User Glue） |
| SWU_IPCS_LINUX_OS_CDEV | mpu/os_cdev/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / CDEV 实现（User Glue） |
| SWU_IPCS_LINUX_OS_KERN | mpu/os_kernel/ipc-os.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / 全内核实现 |
| SWU_IPCS_LINUX_UIO_KO | mpu/os_kernel/ipc-uio.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / UIO 实现（Kernel Backend） |
| SWU_IPCS_LINUX_CDEV_KO | mpu/os_kernel/ipc-cdev.c | Drv_Ipcs_Linux_Adapt_Cmp | Linux / CDEV 实现（Kernel Backend） |

## 2.3 Component ID to Software Unit Mapping（组件 ID → 软件单元 ID）

| 架构组件 ID | 软件单元 ID（实现载体） | 说明 |
|---|---|---|
| Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | 对外 API 与实例/通道逻辑在 ipc-shm.c |
| Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | 队列在 ipc-queue.c |
| Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES、外部 ipcf_Ip_Cfg*.h | 配置类型与工程配置头 |
| Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_*（RTOS）或 SWU_IPCS_LINUX_OS_*（Linux 用户 Glue）+ 内核协同 | 随 L2 实现切换 |
| Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU 或 SWU_IPCS_HAL_LINUX | RTOS 单址空间；Linux 特权访问在内核 |
| Drv_Ipcs_Linux_Adapt_Cmp | SWU_IPCS_LINUX_* 组合 | 全内核：KERN+HAL_LINUX；UIO/CDEV：OS_UIO/CDEV + UIO_KO/CDEV_KO + HAL_LINUX |

第 3 章及以下各函数说明表中的 **软件单元 ID** 字段引用上表；**对应软件架构 ID** 引用架构组件。

## 2.4 Deployment Variants（部署变体 L1/L2）

| L1 部署变体 | L2 实现 | 源码根目录 | 主要软件单元 ID |
|---|---|---|---|
| RTOS 部署变体 | FreeRTOS 实现 | ipcs/mcu/os/freertos/ | SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_HAL_MCU |
| RTOS 部署变体 | ThreadX 实现 | ipcs/mcu/os/threadx/ | SWU_IPCS_OSAL_THREADX、SWU_IPCS_HAL_MCU |
| RTOS 部署变体 | AUTOSAR OS 实现 | ipcs/mcu/os/autosar/ | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_HAL_MCU |
| Linux 部署变体 | 全内核实现 | ipcs/mpu/os_kernel/ | SWU_IPCS_LINUX_OS_KERN、SWU_IPCS_HAL_LINUX |
| Linux 部署变体 | UIO 实现 | ipcs/mpu/os_uio/ + os_kernel/ | SWU_IPCS_LINUX_OS_UIO、SWU_IPCS_LINUX_UIO_KO、SWU_IPCS_HAL_LINUX |
| Linux 部署变体 | CDEV 实现 | ipcs/mpu/os_cdev/ + os_kernel/ | SWU_IPCS_LINUX_OS_CDEV、SWU_IPCS_LINUX_CDEV_KO、SWU_IPCS_HAL_LINUX |

构建选型：Linux 用户态库使用 `IPCS_OS=uio` 或 `IPCS_OS=cdev`（见 ipcs/mpu 各实现 Makefile）。Baremetal 不在本文档范围。

## 2.5 External Dependencies（外部依赖与运行环境）

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

## 2.6 Linux Implementation Refinement（Linux 实现细化）

`Drv_Ipcs_Linux_Adapt_Cmp` 在架构上不拆分用户/内核。SDD 实现单元如下（不新增架构组件 ID）：

| 实现单元 | 说明 | 典型路径 |
|---|---|---|
| User-Space Adaptation Glue | 用户库内 `ipcsOs*`/`ipcsHw*`；HAL Facade 经 ioctl/UIO 转发 | mpu/os_uio/ipc-os.c、mpu/os_cdev/ipc-os.c |
| Kernel Backend | 中断、MSCM、实例初始化 | mpu/os_kernel/ipc-uio.c、ipc-cdev.c、mpu/hw/c1/ipc-hw.c |
| In-Kernel Monolith | Core+OSAL+HAL 于单内核模块 | mpu/os_kernel/ipc-os.c |

| API（逻辑 P4/P5） | 用户 Glue | 内核 Backend |
|---|---|---|
| ipcsOsInit / ipcsOsFree | os_uio/os_cdev ipc-os.c | ioctl / UIO 配置 |
| ipcsOsGetLocalShm / GetRemoteShm | mmap /dev/mem | — |
| ipcsOsPollChannels | 用户线程 + UIO read / cdev poll | ISR 唤醒 |
| ipcsHwInit / ipcsHwFree | dummy（内核处理） | ipc-hw.c |
| ipcsHwIrqEnable/Disable/Notify | UIO write 或 ioctl | ipc-hw.c |

'''

# function name -> (unit_id, component_id)
FUNC_UNIT = {
    # Core external
    "ipcsShmInit": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmFree": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmAcquireBuf": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmReleaseBuf": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmTx": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmUnmanagedAcquire": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmUnmanagedTx": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmIsRemoteReady": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmPollChannels": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    # Queue
    "ipcsQueuePop": ("SWU_IPCS_CORE_QUEUE", "Drv_Ipcs_Queue_Cmp"),
    "ipcsQueuePush": ("SWU_IPCS_CORE_QUEUE", "Drv_Ipcs_Queue_Cmp"),
    "ipcsQueueInit": ("SWU_IPCS_CORE_QUEUE", "Drv_Ipcs_Queue_Cmp"),
    "ipcsQueueCheckIntegrity": ("SWU_IPCS_CORE_QUEUE", "Drv_Ipcs_Queue_Cmp"),
    "ipcsQueueMemSize": ("SWU_IPCS_CORE_QUEUE", "Drv_Ipcs_Queue_Cmp"),
    # Core internal
    "getChannel": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "getManagedChan": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "getUnmanagedChan": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsCheckUchanIntegrity": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsCheckMchanIntegrity": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsChannelRx": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsInstanceIsFree": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmRx": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsBufPoolInit": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsGetTotalBufPerChan": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "managedChannelInit": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "unmanagedChannelInit": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmInitChannel": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "getChanMemmapSize": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmInitChannels": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsShmInitInstance": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "findPoolForBuf": ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"),
    "ipcsMemcpy": ("SWU_IPCS_CORE_UTIL", "Drv_Ipcs_Core_Cmp"),
}

# HAL defaults RTOS; chapter 4 section uses MCU
HAL_FUNCS = {
    f"ipcsHw{i}" for i in (
        "GetCoreIndexM7", "GetCoreIndexA53", "SetRemoteCore", "SetLocalCore",
        "SetCore", "SetTxIrqIdx", "SetRxIrqIdx", "SetIrqIdx", "Init", "Free",
        "IrqEnable", "IrqDisable", "IrqNotify", "IrqClear", "FlushCache",
        "FlushCacheLocal", "FlushCacheRemote", "GetRxIrq",
    )
}
for h in HAL_FUNCS:
    FUNC_UNIT[f"ipcsHw{h}"] = ("SWU_IPCS_HAL_MCU", "Drv_Ipcs_Hal_Cmp")

OS_FUNCS_DEFAULT = ("SWU_IPCS_OSAL_AUTOSAR", "Drv_Ipcs_Osal_Cmp")
for o in (
    "ipcsOsInit", "ipcsOsFree", "ipcsOsGetLocalShm", "ipcsOsGetRemoteShm",
    "ipcsOsPollChannels", "ipcsShmSoftirq", "ipcsShmHardirq", "ipcsShmHardirqInstance",
    "ipcsShmSoftIrq", "ipcsShmHardIrq",
):
    FUNC_UNIT.setdefault(o, OS_FUNCS_DEFAULT)

_HEADING_RE = re.compile(r"^###\s+(3\.2\.\d+|3\.3\.\d+|3\.4\.\d+)\s+(\w+)")
_MEDIA_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(md_sdd_0519_media/image\d+\.png\)"
)
_CH2_START = re.compile(r"^# 2 Software Architecture", re.M)
_CH2_END = re.compile(r"^# 3 公共详细设计", re.M)


def _svg_for_section(section: str) -> Path | None:
    parts = section.split(".")
    if len(parts) != 3:
        return None
    _, minor, patch = parts
    if minor == "2":
        p = FILES_32_SVGS / f"3_2_{patch}.svg"
    elif minor in ("3", "4"):
        p = FLOW_SVGS / f"3_{minor}_{patch}.svg"
        if not p.is_file() and minor == "4":
            alt = FLOW_SVGS / f"tx_3_4_{patch}.svg"
            if alt.is_file():
                p = alt
    else:
        return None
    return p if p.is_file() else None


def replace_images(md: str) -> str:
    last_section: str | None = None
    out: list[str] = []
    for line in md.splitlines(keepends=True):
        hm = _HEADING_RE.match(line)
        if hm:
            last_section = hm.group(1)
            func = hm.group(2)
            # OSAL block detection by section number ranges in ch4
            if last_section.startswith("3.4.4") and func.startswith("ipcsOs"):
                pass  # autosar block 41-48
            if last_section.startswith("3.4.5") and "ipcsOs" in func or "Softirq" in func:
                FUNC_UNIT.setdefault(func, ("SWU_IPCS_OSAL_FREERTOS", "Drv_Ipcs_Osal_Cmp"))
            if last_section.startswith("3.4.5") and func in ("ipcsShmHardirq", "ipcsShmHardirqInstance", "ipcsShmSoftirq"):
                FUNC_UNIT.setdefault(func, ("SWU_IPCS_OSAL_FREERTOS", "Drv_Ipcs_Osal_Cmp"))
            if last_section >= "3.4.56" or last_section in ("3.4.56", "3.4.57", "3.4.58", "3.4.59", "3.4.61", "3.4.62", "3.4.63"):
                if func.startswith("ipcsOs") or "Soft" in func or "Hard" in func:
                    FUNC_UNIT.setdefault(func, ("SWU_IPCS_OSAL_THREADX", "Drv_Ipcs_Osal_Cmp"))

        def repl(m: re.Match[str]) -> str:
            alt = m.group(1) or "diagram"
            if last_section:
                svg = _svg_for_section(last_section)
                if svg:
                    rel = rel_to_workspace(svg).as_posix()
                    return f"![{alt}]({rel})"
            return m.group(0)

        line = _MEDIA_IMG_RE.sub(repl, line)
        # image86.png special
        line = line.replace(
            "md_sdd_0519_media/image86.png",
            "cursor_tmp/flow_svgs/3_3_1.svg",
        )
        line = line.replace("md_sdd_0519_media/image40.png", "files_32_svgs/3_2_9.svg")
        out.append(line)
    return "".join(out)


def inject_unit_ids(md: str) -> str:
    """在函数表中加入软件单元 ID；修正架构 ID 行。"""
    lines = md.splitlines(keepends=True)
    current_func: str | None = None
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        hm = re.match(r"^### 3\.(3|4)\.\d+ (\w+)", line)
        if hm:
            current_func = hm.group(2)

        if current_func and "<td>对应软件架构ID</td>" in line:
            unit, comp = FUNC_UNIT.get(current_func, ("SWU_IPCS_CORE_SHM", "Drv_Ipcs_Core_Cmp"))
            # next line has component
            if i + 1 < len(lines) and "colspan" in lines[i + 1]:
                # replace component if wrong
                lines[i + 1] = re.sub(
                    r"<td colspan=\"4\">[^<]+</td>",
                    f'<td colspan="4">{comp}</td>',
                    lines[i + 1],
                )
            out.append(line)
            if i + 1 < len(lines):
                out.append(lines[i + 1])
                i += 2
            out.append(
                f'<tr>\n<td>软件单元 ID</td>\n<td colspan="4">{unit}</td>\n</tr>\n'
            )
            continue

        # fix file paths in tables
        line = line.replace("common/ipc-", "ipcs/ipcs_cores/ipc-")
        line = line.replace("hw/ipc-hw", "ipcs/mcu/hw/ipc-hw")
        line = line.replace("os/freertos", "ipcs/mcu/os/freertos")
        line = line.replace("os/threadx", "ipcs/mcu/os/threadx")
        line = line.replace("os/autosar", "ipcs/mcu/os/autosar")
        out.append(line)
        i += 1
    return "".join(out)


def replace_chapter2(md: str) -> str:
    start = _CH2_START.search(md)
    end = _CH2_END.search(md)
    if not start or not end or end.start() <= start.start():
        raise RuntimeError("cannot find chapter 2 boundaries")
    return md[: start.start()] + CH2_NEW + md[end.start() :]


def update_contents(md: str) -> str:
    old = """- 2 Software Architecture软件架构
  - 2.1 架构分层与组件
  - 2.2 组件关系与端口
  - 2.3 运行场景
  - 2.4 部署变体与实现（L1/L2）
  - 2.5 外部依赖与运行环境
  - 2.6 Linux 部署变体架构细化（SDD Refinement）"""
    new = """- 2 Architectural Compliance and Software Unit Identification 架构符合性与软件单元划分
  - 2.1 Compliance with Software Architectural Design（SWE.2 符合性）
  - 2.2 Software Unit Identification（软件单元划分）
  - 2.3 Component ID to Software Unit Mapping（组件→单元映射）
  - 2.4 Deployment Variants（部署变体 L1/L2）
  - 2.5 External Dependencies（外部依赖）
  - 2.6 Linux Implementation Refinement（Linux 实现细化）"""
    return md.replace(old, new)


def update_ch6(md: str) -> str:
    extra = """
| SW-Unit-ID | 函数/设计章节出处 | 源文件 |
|---|---|---|
| SWU_IPCS_CORE_SHM | §3.3、§3.4（Core 内部函数） | ipcs/ipcs_cores/ipc-shm.c |
| SWU_IPCS_CORE_QUEUE | §3.4.1–3.4.5 | ipcs/ipcs_cores/ipc-queue.c |
| SWU_IPCS_HAL_MCU | §4.6 HAL、§4.3–4.5 OSAL | ipcs/mcu/hw/ipc-hw.c |
| SWU_IPCS_LINUX_OS_UIO | §5.4 | ipcs/mpu/os_uio/ipc-os.c |

"""
    marker = "## 6.2 架构—设计—源码追溯矩阵"
    if marker in md and "SW-Unit-ID | 函数/设计章节出处" not in md:
        return md.replace(
            marker + "\n\n| 架构组件 ID |",
            marker + "\n\n### 6.2.1 软件单元追溯（节选）\n" + extra + "| 架构组件 ID |",
        )
    return md


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    md = update_contents(md)
    md = replace_chapter2(md)
    md = replace_images(md)
    md = inject_unit_ids(md)
    md = update_ch6(md)
  # verify no png left in image refs
    if "md_sdd_0519_media" in md or re.search(r"!\[[^\]]*\]\([^)]+\.png\)", md):
        n = len(re.findall(r"\.png\)", md))
        print(f"[warn] {n} .png image references remain")
    else:
        print("[ok] all diagram references use SVG (no md_sdd_0519_media png)")
    MD.write_text(md, encoding="utf-8")
    print(f"Wrote {MD}")


if __name__ == "__main__":
    main()
