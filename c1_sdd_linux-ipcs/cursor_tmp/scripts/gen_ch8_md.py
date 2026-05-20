#!/usr/bin/env python3
"""Generate chapter 8 traceability markdown block."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQ_JSON = ROOT / "cursor_tmp" / "req_allocation_24.json"
OUT = ROOT / "cursor_tmp" / "ch8_traceability.md"

COMP_UNITS: dict[str, list[str]] = {
    "Drv_Ipcs_Core_Cmp": ["SWU_IPCS_CORE_SHM", "SWU_IPCS_CORE_UTIL"],
    "Drv_Ipcs_Queue_Cmp": ["SWU_IPCS_CORE_QUEUE"],
    "Drv_Ipcs_Conf_Cmp": ["SWU_IPCS_CORE_TYPES"],
    "Drv_Ipcs_Osal_Cmp": [
        "SWU_IPCS_OSAL_AUTOSAR",
        "SWU_IPCS_OSAL_FREERTOS",
        "SWU_IPCS_OSAL_THREADX",
        "SWU_IPCS_LINUX_OS_KERN",
    ],
    "Drv_Ipcs_Hal_Cmp": ["SWU_IPCS_HAL_MCU", "SWU_IPCS_HAL_LINUX"],
    "Drv_Ipcs_Linux_Adapt_Cmp": [
        "SWU_IPCS_LINUX_OS_UIO",
        "SWU_IPCS_LINUX_OS_CDEV",
        "SWU_IPCS_LINUX_OS_KERN",
        "SWU_IPCS_LINUX_UIO_KO",
        "SWU_IPCS_LINUX_CDEV_KO",
    ],
}

UNIT_CODE: dict[str, str] = {
    "SWU_IPCS_CORE_SHM": "`ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`",
    "SWU_IPCS_CORE_QUEUE": "`ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h`",
    "SWU_IPCS_CORE_UTIL": "`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h`",
    "SWU_IPCS_CORE_TYPES": "`ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h`",
    "SWU_IPCS_OSAL_AUTOSAR": "`ipcs/mcu/os/autosar/ipc-os-autosar.c`",
    "SWU_IPCS_OSAL_FREERTOS": "`ipcs/mcu/os/freertos/ipc-os-freertos.c`",
    "SWU_IPCS_OSAL_THREADX": "`ipcs/mcu/os/threadx/ipc-os-threadx.c`",
    "SWU_IPCS_HAL_MCU": "`ipcs/mcu/hw/ipc-hw.c`",
    "SWU_IPCS_HAL_LINUX": "`ipcs/mpu/hw/c1/ipc-hw.c`",
    "SWU_IPCS_LINUX_OS_KERN": "`ipcs/mpu/os_kernel/ipc-os.c`",
    "SWU_IPCS_LINUX_OS_UIO": "`ipcs/mpu/os_uio/ipc-os.c`",
    "SWU_IPCS_LINUX_OS_CDEV": "`ipcs/mpu/os_cdev/ipc-os.c`",
    "SWU_IPCS_LINUX_UIO_KO": "`ipcs/mpu/os_kernel/ipc-uio.c`",
    "SWU_IPCS_LINUX_CDEV_KO": "`ipcs/mpu/os_kernel/ipc-cdev.c`",
}

UNIT_SECTION: dict[str, str] = {
    "SWU_IPCS_CORE_SHM": "§4",
    "SWU_IPCS_CORE_QUEUE": "§4",
    "SWU_IPCS_CORE_UTIL": "§4",
    "SWU_IPCS_CORE_TYPES": "§4.6",
    "SWU_IPCS_OSAL_AUTOSAR": "§5.3",
    "SWU_IPCS_OSAL_FREERTOS": "§5.4",
    "SWU_IPCS_OSAL_THREADX": "§5.5",
    "SWU_IPCS_HAL_MCU": "§5.6",
    "SWU_IPCS_HAL_LINUX": "§6.8",
    "SWU_IPCS_LINUX_OS_KERN": "§6.3",
    "SWU_IPCS_LINUX_OS_UIO": "§6.4",
    "SWU_IPCS_LINUX_OS_CDEV": "§6.6",
    "SWU_IPCS_LINUX_UIO_KO": "§6.5",
    "SWU_IPCS_LINUX_CDEV_KO": "§6.7",
}

ALL_DRV = list(COMP_UNITS.keys())


def clean_summary(s: str) -> str:
    s = s.replace("\n", "")
    return re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", s)


def parse_components(raw: str) -> list[str]:
    raw = raw.replace("（传输层实现）", "").strip()
    comps: list[str] = []
    if "过程类" in raw:
        comps.append("过程类")
    if "全组件" in raw or "～" in raw or "~" in raw:
        comps.extend(ALL_DRV)
        comps.append("Drv_Ipcs_Linux_Adapt_Cmp")
    else:
        comps.extend(re.findall(r"Drv_Ipcs_\w+", raw))
    if not comps and "过程类" in raw:
        comps.append("过程类")
    return list(dict.fromkeys(comps))


def units_for(comp: str) -> str:
    if comp == "过程类":
        return "—（过程类；非运行时软件单元）"
    u = COMP_UNITS.get(comp, [])
    return "、".join(u) if u else "—"


def code_for(comp: str) -> str:
    if comp == "过程类":
        return "—"
    u = COMP_UNITS.get(comp, [])
    files = [UNIT_CODE[x] for x in u if x in UNIT_CODE]
    return "；".join(files) if files else "—"


def section_for(comp: str) -> str:
    if comp == "过程类":
        return "—"
    u = COMP_UNITS.get(comp, [])
    secs = sorted({UNIT_SECTION[x] for x in u if x in UNIT_SECTION})
    return "、".join(secs) if secs else "—"


def main() -> None:
    reqs = json.loads(REQ_JSON.read_text(encoding="utf-8"))
    lines = [
        "# 8 双向追溯与一致性 (Bidirectional Traceability and Consistency)",
        "",
        "## 8.1 追溯性策略与声明 (Traceability Statement)",
        "",
        "本章节旨在建立并证明本模块的软件详细设计与上游（软件需求、软件架构）以及下游（物理源代码）之间的双向追溯关系，以满足 ASPICE 规范中 SWE.3.BP4 的核心要求。",
        "",
        "本追溯矩阵确保了各层级设计的一致性（Consistency）与完整性：上游 `ipcs-architecture.pdf` §2.4 需求分配表中的架构组件均在本文档软件单元与 `ipcs/` 源码中落实；函数级设计见第 4–6 章。过程类需求（安全、构建、测试流程等）由项目 SWE 工作产品承担，不在 SDD 软件单元表中展开实现。",
        "",
        "需求—组件映射真源：`ipcs-architecture.pdf` §2.4 REQUIREMENTS ALLOCATION（V1.0，2026-04-16）。组件—单元映射真源：本文档 §2.1–§2.2。",
        "",
        "## 8.2 需求-架构-设计-代码 双向追溯矩阵 (Bidirectional Traceability Matrix)",
        "",
        "下表按架构文档 §2.4 逐条展开：同一需求 ID 若分配多个架构组件，则分多行；「本详细设计单元 ID」与「物理源代码实体」来自 §2.2 与 §2.1。",
        "",
        "| 软件需求 ID (SWE.1) | 需求简述 | 架构组件 ID (SWE.2) | 本详细设计单元 ID (SWE.3 Unit) | 物理源代码实体 (Code) | 设计章节 | 追溯关系及设计覆盖说明 |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in reqs:
        rid = r["id"]
        summary = clean_summary(r["summary"])
        note = clean_summary(r["notes"])
        for comp in parse_components(r["components"]):
            lines.append(
                "| {rid} | {sum} | {comp} | {units} | {code} | {sec} | {note} |".format(
                    rid=rid,
                    sum=summary,
                    comp=comp,
                    units=units_for(comp),
                    code=code_for(comp),
                    sec=section_for(comp),
                    note=note if comp != "过程类" else (note or r.get("components", "")),
                )
            )

    lines.extend(
        [
            "",
            "## 8.3 软件单元与源码索引（与 §2 一致）",
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
            "对外应用 API（`ipcs-shm.h` 非 static）：`ipcsShmInit`、`ipcsShmFree`、`ipcsShmAcquireBuf`、`ipcsShmReleaseBuf`、`ipcsShmTx`、`ipcsShmUnmanagedAcquire`、`ipcsShmUnmanagedTx`、`ipcsShmIsRemoteReady`、`ipcsShmPollChannels` — 设计见 §4.3，与 §3.3 一致。",
            "",
        ]
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(lines)} lines -> {OUT}")


if __name__ == "__main__":
    main()
