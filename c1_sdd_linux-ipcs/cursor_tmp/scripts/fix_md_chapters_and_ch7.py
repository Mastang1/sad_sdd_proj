#!/usr/bin/env python3
"""Fix md_sdd_0519.md chapter numbering and rewrite productized ch.7 traceability."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"
REQ_JSON = ROOT / "cursor_tmp" / "req_allocation_24.json"

# SDD matrix: exclude non-runtime / non-ipcs traceability (still in architecture §2.4)
EXCLUDED: dict[str, str] = {
    "IPCS_009": "架构分层与依赖方向；由第 3 章三层契约与 `ipcs/` 目录划分体现",
    "IPCS_011": "Windows 主机构建、工具链与桩；归属集成工程，非 `ipcs/` 运行时",
    "IPCS_013": "模糊测试与安服验证手段；归属 SWE.5 / 安全验证计划",
    "IPCS_030": "编码规范与静态分析；归属项目过程与 CI",
    "IPCS_038": "组织级质量流程；归属项目管理，架构文档为 SWE.2 产物",
}

# Per-requirement SDD trace (one row each); units/code scoped to this repo
TRACE: dict[str, dict[str, str]] = {
    "IPCS_001": {
        "arch": "Drv_Ipcs_Core_Cmp（主责）；协同 Queue、Osal、Hal、Conf",
        "units": "SWU_IPCS_CORE_SHM/UTIL/QUEUE、SWU_IPCS_CORE_TYPES；OSAL/HAL 各部署变体单元（§2.1）",
        "code": "`ipcs/ipcs_cores/*`；`ipcs/mcu/os/*`；`ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/**`",
        "sec": "§3–§6",
        "note": "端到端实例/通道/队列/映射/通知；见 §3.4 与各 OS 实现",
    },
    "IPCS_002": {
        "arch": "Drv_Ipcs_Osal_Cmp",
        "units": "SWU_IPCS_OSAL_AUTOSAR",
        "code": "`ipcs/mcu/os/autosar/ipc-os-autosar.c`",
        "sec": "§5.3",
        "note": "ASIL-D 目标分解与证据在独立安全工件；SDD 仅追溯 AutoSAR OSAL 集成边界",
    },
    "IPCS_003": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp；平台相关 Drv_Ipcs_Hal_Cmp",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE、SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`；`ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c`",
        "sec": "§4、§5.6、§6.8",
        "note": "可移植逻辑在 Core/Queue；字节序与平台差异在 HAL",
    },
    "IPCS_005": {
        "arch": "Drv_Ipcs_Osal_Cmp",
        "units": "SWU_IPCS_OSAL_AUTOSAR",
        "code": "`ipcs/mcu/os/autosar/ipc-os-autosar.c`",
        "sec": "§5.3",
        "note": "CDD/OS 封装与调度；配置由集成方 `ipcf_Ip_Cfg*.h` 提供",
    },
    "IPCS_006": {
        "arch": "Drv_Ipcs_Osal_Cmp",
        "units": "SWU_IPCS_OSAL_THREADX",
        "code": "`ipcs/mcu/os/threadx/ipc-os-threadx.c`",
        "sec": "§5.5",
        "note": "ThreadX 任务/中断/同步原语映射",
    },
    "IPCS_010": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`",
        "sec": "§4",
        "note": "传输路径可观测性由可选编译/钩子支持；非生产最小集强制项",
    },
    "IPCS_012": {
        "arch": "Drv_Ipcs_Core_Cmp、Queue、Osal、Hal",
        "units": "§2.1 所列 Core/OSAL/HAL 单元",
        "code": "`ipcs/` 各单元源文件",
        "sec": "§4–§6",
        "note": "OSAL/HAL 契约可注入 mock；测试工程属 SWE.5，接口边界见 §4.3",
    },
    "IPCS_014": {
        "arch": "Drv_Ipcs_Core_Cmp、Queue、Conf",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`、`ipc-types.h`",
        "sec": "§4、§4.6",
        "note": "多 channel 与共享内存布局",
    },
    "IPCS_015": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`",
        "sec": "§4.4",
        "note": "单通道队列语义与收发顺序",
    },
    "IPCS_016": {
        "arch": "Drv_Ipcs_Core_Cmp、Queue、Conf",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`、`ipc-types.h`",
        "sec": "§4、§4.6",
        "note": "pool 与多队列管理",
    },
    "IPCS_017": {
        "arch": "Drv_Ipcs_Core_Cmp、Osal、Conf",
        "units": "SWU_IPCS_CORE_SHM、OSAL 各变体、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`；各 `ipc-os-*.c`",
        "sec": "§4、§5、§6.3–6.6",
        "note": "多 instance 与每核 OSAL 执行/中断模型",
    },
    "IPCS_018": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`",
        "sec": "§4.3–§4.4",
        "note": "BD/指针零拷贝路径",
    },
    "IPCS_019": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Osal_Cmp",
        "units": "SWU_IPCS_CORE_SHM、OSAL 各变体",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`；`ipcsOsPollChannels` 等",
        "sec": "§4、§5、§6",
        "note": "异步回调由 OSAL 触发，Core 分发",
    },
    "IPCS_020": {
        "arch": "Drv_Ipcs_Core_Cmp、Conf + 集成内存布局",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-types.h`；工程 `ipcf_Ip_Cfg*.h`",
        "sec": "§4、§4.6",
        "note": "分区与访问边界由配置与 SoC/OS MPU 共同保证",
    },
    "IPCS_021": {
        "arch": "Drv_Ipcs_Core_Cmp、Conf",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`；`ipcsShmUnmanaged*`（§4.3）",
        "sec": "§4.3、§4.4",
        "note": "unmanaged 通道模型",
    },
    "IPCS_022": {
        "arch": "Drv_Ipcs_Core_Cmp、Queue、Osal、Hal",
        "units": "Core/Queue/OSAL/HAL 单元（§2.1）",
        "code": "`ipcs/ipcs_cores/*`；OSAL/HAL 实现文件",
        "sec": "§4–§6",
        "note": "序列号/队列状态与 IRQ 通知协调",
    },
    "IPCS_023": {
        "arch": "Drv_Ipcs_Core_Cmp、Drv_Ipcs_Queue_Cmp",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_QUEUE",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-queue.c`",
        "sec": "§4",
        "note": "共享内存提交顺序；与 IPCS_039 轮询补偿协同",
    },
    "IPCS_024": {
        "arch": "Drv_Ipcs_Osal_Cmp、Conf",
        "units": "SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/mcu/os/autosar/ipc-os-autosar.c`、`ipc-types.h`",
        "sec": "§5.3、§4.6",
        "note": "R4.4+ 集成接口与配置模型",
    },
    "IPCS_025": {
        "arch": "Drv_Ipcs_Conf_Cmp",
        "units": "SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-types.h`；`ipcf_Ip_Cfg*.h`",
        "sec": "§4.6",
        "note": "池数量/大小由集成配置定义，Core/Queue 消费",
    },
    "IPCS_028": {
        "arch": "Drv_Ipcs_Hal_Cmp、Drv_Ipcs_Osal_Cmp",
        "units": "SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX、OSAL 各变体",
        "code": "`ipcs/mcu/hw/ipc-hw.c`、`ipcs/mpu/hw/c1/ipc-hw.c`；各 OSAL",
        "sec": "§5.6、§6.8、§5–§6 OSAL",
        "note": "核间中断通知：HAL 平台实现 + OSAL 挂接",
    },
    "IPCS_029": {
        "arch": "Drv_Ipcs_Core_Cmp、Queue、Osal",
        "units": "SWU_IPCS_CORE_*、OSAL 单元",
        "code": "`ipcs/ipcs_cores/*`；`ipcs/mcu/os/*`、`ipcs/mpu/os_*`",
        "sec": "§4–§6",
        "note": "静态池/队列维度；无动态堆分配",
    },
    "IPCS_031": {
        "arch": "Drv_Ipcs_Core_Cmp、Conf",
        "units": "SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_TYPES",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-types.h`",
        "sec": "§4",
        "note": "多 instance 独立 SHM/IRQ 配置",
    },
    "IPCS_034": {
        "arch": "Drv_Ipcs_Core_Cmp",
        "units": "SWU_IPCS_CORE_SHM",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`、`ipc-shm.h`",
        "sec": "§4.3",
        "note": "公共 API 入参校验",
    },
    "IPCS_035": {
        "arch": "Drv_Ipcs_Core_Cmp",
        "units": "SWU_IPCS_CORE_SHM",
        "code": "`ipcs/ipcs_cores/ipc-shm.c`",
        "sec": "§4.3–§4.4",
        "note": "managed/unmanaged 与 channel 类型一致性",
    },
    "IPCS_036": {
        "arch": "Drv_Ipcs_Core_Cmp～Linux_Adapt、Conf",
        "units": "§2.1 全部软件单元（按部署裁剪链接）",
        "code": "`ipcs/` 树；Linux 见 `ipcs/mpu/**`",
        "sec": "§3–§6",
        "note": "编译选项与部署变体裁剪",
    },
    "IPCS_039": {
        "arch": "Drv_Ipcs_Osal_Cmp、Drv_Ipcs_Hal_Cmp",
        "units": "OSAL/HAL 各变体",
        "code": "`ipcsShmPollChannels` 等（§4.3.9）",
        "sec": "§4.3.9、§5–§6 OSAL",
        "note": "IRQ_NONE 轮询路径",
    },
}


def clean_summary(s: str) -> str:
    s = s.replace("\n", "")
    return re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", s)


def build_ch7() -> str:
    reqs = json.loads(REQ_JSON.read_text(encoding="utf-8"))
    lines = [
        "# 7 双向追溯与一致性 (Bidirectional Traceability and Consistency)",
        "",
        "## 7.1 追溯性策略与声明 (Traceability Statement)",
        "",
        "本章节满足 ASPICE SWE.3.BP4：建立**本 SDD 范围内**软件单元与物理源码对上游软件架构（SWE.2）及已分配软件需求（SWE.1）的可验证追溯，并支持变更影响分析。",
        "",
        "追溯原则：",
        "",
        "- **真源**：需求—组件分配见 `ipcs-architecture.pdf` §2.4；组件—单元见本文档 §2.1–§2.2；函数级行为见 §4–§6。",
        "- **一行一需求**：矩阵每行对应一条 `IPCS_*`，且均能落到 `ipcs/` 内具体源文件与 SW-Unit-ID（产品化 SDD 不写“空单元”占位行）。",
        "- **过程类需求不纳入实现矩阵**：构建/组织过程/独立安全证据等不在本驱动 SDD 内展开实现，集中于 §7.3 说明与上游工作产品引用，避免伪追溯。",
        "- **防镀金**：§7.4 单元索引与 §2.1 一致；`ipcs/` 中纳入设计的文件均可在矩阵或 §4–§6 中找到设计描述。",
        "",
        "## 7.2 需求-架构-设计-代码 双向追溯矩阵 (Bidirectional Traceability Matrix)",
        "",
        "下表仅包含在 `ipcs/` 源码与本文档 §4–§6 中**可验证实现**的需求项（共 26 条）。协同组件写入「架构组件」列，不拆为多行。",
        "",
        "| 软件需求 ID (SWE.1) | 需求简述 | 架构组件 ID (SWE.2) | 本详细设计单元 ID (SWE.3) | 物理源代码与设计章节 | 追溯关系及设计覆盖说明 |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in reqs:
        rid = r["id"]
        if rid in EXCLUDED:
            continue
        t = TRACE.get(rid)
        if not t:
            continue
        summary = clean_summary(r["summary"])
        lines.append(
            f"| {rid} | {summary} | {t['arch']} | {t['units']} | {t['code']}（{t['sec']}） | {t['note']} |"
        )

    lines.extend(
        [
            "",
            "## 7.3 不纳入本 SDD 实现矩阵的需求说明",
            "",
            "下列条目在架构 §2.4 中分配为**过程类**或**非 `ipcs/` 运行时**职责；不在 §7.2 中重复占位，以免削弱双向追溯可信度。",
            "",
            "| 软件需求 ID | 需求简述 | 排除原因 | 追溯归属 |",
            "| :--- | :--- | :--- | :--- |",
        ]
    )
    for r in reqs:
        rid = r["id"]
        if rid not in EXCLUDED:
            continue
        lines.append(
            f"| {rid} | {clean_summary(r['summary'])} | {EXCLUDED[rid]} | 架构 §2.4；项目 SWE/集成工作产品 |"
        )

    lines.extend(
        [
            "",
            "## 7.4 软件单元与物理源码索引",
            "",
            "与 §2.1 一致；函数级设计见 §4–§6 各 `###` 小节。",
            "",
            "| SW-Unit-ID | 源码文件 | 详细设计章节 |",
            "| :--- | :--- | :--- |",
            "| SWU_IPCS_CORE_SHM | ipcs/ipcs_cores/ipc-shm.c | §4.2–§4.4 |",
            "| SWU_IPCS_CORE_QUEUE | ipcs/ipcs_cores/ipc-queue.c | §4.2、§4.4 |",
            "| SWU_IPCS_CORE_UTIL | ipcs/ipcs_cores/ipc-util.c | §4.2、§4.4 |",
            "| SWU_IPCS_CORE_TYPES | ipcs/ipcs_cores/ipc-types.h | §4.6 |",
            "| SWU_IPCS_OSAL_AUTOSAR | ipcs/mcu/os/autosar/ipc-os-autosar.c | §5.3 |",
            "| SWU_IPCS_OSAL_FREERTOS | ipcs/mcu/os/freertos/ipc-os-freertos.c | §5.4 |",
            "| SWU_IPCS_OSAL_THREADX | ipcs/mcu/os/threadx/ipc-os-threadx.c | §5.5 |",
            "| SWU_IPCS_HAL_MCU | ipcs/mcu/hw/ipc-hw.c | §5.6 |",
            "| SWU_IPCS_LINUX_OS_KERN | ipcs/mpu/os_kernel/ipc-os.c | §6.3 |",
            "| SWU_IPCS_LINUX_OS_UIO | ipcs/mpu/os_uio/ipc-os.c | §6.4 |",
            "| SWU_IPCS_LINUX_UIO_KO | ipcs/mpu/os_kernel/ipc-uio.c | §6.5 |",
            "| SWU_IPCS_LINUX_OS_CDEV | ipcs/mpu/os_cdev/ipc-os.c | §6.6 |",
            "| SWU_IPCS_LINUX_CDEV_KO | ipcs/mpu/os_kernel/ipc-cdev.c | §6.7 |",
            "| SWU_IPCS_HAL_LINUX | ipcs/mpu/hw/c1/ipc-hw.c | §6.8 |",
            "",
            "对外应用 API（`ipcs-shm.h`）：`ipcsShmInit`、`ipcsShmFree`、`ipcsShmAcquireBuf`、`ipcsShmReleaseBuf`、"
            "`ipcsShmTx`、`ipcsShmUnmanagedAcquire`、`ipcsShmUnmanagedTx`、`ipcsShmIsRemoteReady`、"
            "`ipcsShmPollChannels` — 见 §4.3。",
            "",
        ]
    )
    return "\n".join(lines)


def reorder_ch5(block: str) -> str:
    parts = re.split(r"(?=^## 5\.\d+ )", block, flags=re.M)
    if not parts:
        return block
    header = parts[0]
    sections: dict[int, str] = {}
    for p in parts[1:]:
        m = re.match(r"^## 5\.(\d+)", p)
        if m:
            sections[int(m.group(1))] = p
    order = [1, 2, 3, 4, 5, 6, 7]
    return header + "".join(sections[k] for k in order if k in sections)


def renumber_65_67(text: str) -> str:
    # 6.5.17..28 -> 6.5.1..12
    m65 = list(
        re.finditer(
            r"^## 6\.5 SWU_IPCS_LINUX_UIO_KO.*?(?=^## 6\.6 )",
            text,
            flags=re.M | re.S,
        )
    )
    if m65:
        seg = m65[0].group(0)
        new_seg = seg
        n = 0
        for old in range(17, 29):
            n += 1
            new_seg = new_seg.replace(f"### 6.5.{old} ", f"### 6.5.{n} ")
        text = text[: m65[0].start()] + new_seg + text[m65[0].end() :]

    m67 = list(
        re.finditer(
            r"^## 6\.7 SWU_IPCS_LINUX_CDEV_KO.*?(?=^## 6\.8 )",
            text,
            flags=re.M | re.S,
        )
    )
    if m67:
        seg = m67[0].group(0)
        new_seg = seg
        n = 0
        for old in range(12, 22):
            n += 1
            new_seg = new_seg.replace(f"### 6.7.{old} ", f"### 6.7.{n} ")
        text = text[: m67[0].start()] + new_seg + text[m67[0].end() :]
    return text


def fix_52_numbering(block: str) -> str:
    """5.2.0 文件列表置于 5.2.1 前，消除重复 5.2.1 编号。"""
    block = block.replace("### 5.2.0 RTOS 文件列表", "### 5.2.1 RTOS 文件列表")
    block = block.replace(
        "### 5.2.1 ipc-hw-platform.h\n\n描述：",
        "### 5.2.0 ipc-hw-platform.h（概要）\n\n描述：",
    )
    block = block.replace(
        "### 5.2.1 ipc-hw-platform.h（文件依赖详述）",
        "### 5.2.2 ipc-hw-platform.h（文件依赖详述）",
    )
    for old, new in [
        ("### 5.2.2 ipc-hw.c", "### 5.2.3 ipc-hw.c"),
        ("### 5.2.3 ipc-hw.h", "### 5.2.4 ipc-hw.h"),
        ("### 5.2.4 ipc-shm-rtos.mk", "### 5.2.5 ipc-shm-rtos.mk"),
        ("### 5.2.5 ipc-os-autosar.c", "### 5.2.6 ipc-os-autosar.c"),
        ("### 5.2.6 ipc-os-freertos.c", "### 5.2.7 ipc-os-freertos.c"),
        ("### 5.2.7 ipc-os.h", "### 5.2.8 ipc-os.h"),
        ("### 5.2.8 ipc-os-threadx.c", "### 5.2.9 ipc-os-threadx.c"),
    ]:
        block = block.replace(old, new)
    return block


def main() -> None:
    text = MD.read_text(encoding="utf-8")

    # TOC: chapter 8 -> 7
    text = text.replace(
        "- 8 双向追溯与一致性 (Bidirectional Traceability and Consistency)\n"
        "  - 8.1 追溯性策略与声明\n"
        "  - 8.2 需求-架构-设计-代码 双向追溯矩阵\n"
        "  - 8.3 软件单元与源码索引",
        "- 7 双向追溯与一致性 (Bidirectional Traceability and Consistency)\n"
        "  - 7.1 追溯性策略与声明\n"
        "  - 7.2 需求-架构-设计-代码 双向追溯矩阵\n"
        "  - 7.3 不纳入本 SDD 实现矩阵的需求说明\n"
        "  - 7.4 软件单元与物理源码索引",
    )

    # Version row
    text = text.replace(
        "| V0.9 | 2026.5.20 | Cursor Agent | Draft | 新增第 8 章双向追溯矩阵（架构 §2.4 × §2 单元 × 源码）；替换原第 7 章追溯节 |",
        "| V0.9 | 2026.5.20 | Cursor Agent | Draft | 新增第 7 章双向追溯矩阵（架构 §2.4 × §2 单元 × 源码） |\n"
        "| V1.0 | 2026.5.20 | Cursor Agent | Draft | 章节序号连贯（5.x 重排、6.5/6.7 子节）；第 7 章追溯矩阵产品化（剔除过程类伪追溯行） |",
    )

    ch5_start = text.find("# 5 RTOS")
    ch6_start = text.find("# 6 Linux")
    ch7_marker = text.find("# 8 双向追溯")
    if ch7_marker < 0:
        ch7_marker = text.find("# 7 双向追溯")

    if ch5_start >= 0 and ch6_start > ch5_start:
        ch5 = text[ch5_start:ch6_start]
        ch5 = fix_52_numbering(ch5)
        ch5 = reorder_ch5(ch5)
        text = text[:ch5_start] + ch5 + text[ch6_start:]

    ch6_start = text.find("# 6 Linux")
    ch7_marker = text.find("# 8 双向追溯")
    if ch7_marker < 0:
        ch7_marker = text.find("# 7 双向追溯")
    if ch6_start >= 0 and ch7_marker > ch6_start:
        mid = renumber_65_67(text[ch6_start:ch7_marker])
        text = text[:ch6_start] + mid + build_ch7()

    MD.write_text(text, encoding="utf-8")
    print(f"Updated {MD}")


if __name__ == "__main__":
    main()
