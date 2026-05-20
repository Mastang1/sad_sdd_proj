# -*- coding: utf-8 -*-
"""Post-fix md_sdd_0519.md: HTML tables, unit IDs, ch4 numbering."""
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


BROKEN = re.compile(
    r"(<td colspan=\"4\">[^<]+</td>)\n<tr>\n<td>软件单元 ID</td>\n"
    r"<td colspan=\"4\">([^<]+)</td>\n</tr>\n</tr>",
    re.MULTILINE,
)


def fix_broken_tables(md: str) -> str:
    return BROKEN.sub(
        r"\1\n</tr>\n<tr>\n<td>软件单元 ID</td>\n<td colspan=\"4\">\2</td>\n</tr>",
        md,
    )


def renumber_ch4_files(md: str) -> str:
    mapping = {
        "### 3.2.10 ipc-hw.c": "### 4.2.2 ipc-hw.c",
        "### 3.2.11 ipc-hw.h": "### 4.2.3 ipc-hw.h",
        "### 3.2.12 ipc-shm-rtos.mk": "### 4.2.4 ipc-shm-rtos.mk",
        "### 3.2.13 ipc-os-autosar.c": "### 4.2.5 ipc-os-autosar.c",
        "### 3.2.14 ipc-os-freertos.c": "### 4.2.6 ipc-os-freertos.c",
        "### 3.2.16 ipc-os.h": "### 4.2.7 ipc-os.h",
        "### ipc-hw-platform.h": "### 4.2.1 ipc-hw-platform.h（文件依赖详述）",
        "### ipc-os- threadx.c": "### 4.2.8 ipc-os-threadx.c",
    }
    for old, new in mapping.items():
        md = md.replace(old, new)
    return md.replace(
        "### 文件列表\n\n| 组件 | 文件 |",
        "### 4.2.0 RTOS 文件列表\n\n| 组件 | 文件 |",
    )


def renumber_hal_funcs(md: str) -> str:
    lines = md.splitlines(keepends=True)
    out: list[str] = []
    in_hal = False
    hal_idx = 0
    for line in lines:
        if line.startswith("## 4.6 HAL"):
            in_hal = True
            hal_idx = 0
        elif in_hal and line.startswith("## 4.3 "):
            in_hal = False
        if in_hal:
            m = re.match(r"^### 3\.4\.(\d+) (ipcsHw\w+)", line)
            if m:
                hal_idx += 1
                line = f"### 4.6.{hal_idx} {m.group(2)}\n"
        out.append(line)
    return "".join(out)


def fix_hal_arch_and_unit(md: str) -> str:
    """HAL 块内错误地将架构 ID 标为 Core、单元标为 SHM。"""
    parts = md.split("## 4.6 HAL")
    if len(parts) < 2:
        return md
    head, rest = parts[0], "## 4.6 HAL" + parts[1]
    hal, tail = rest.split("## 4.3 AUTOSAR", 1)
    hal = hal.replace("Drv_Ipcs_Core_Cmp", "Drv_Ipcs_Hal_Cmp")
    hal = re.sub(
        r"(<td>软件单元 ID</td>\s*\n<td colspan=\"4\">)SWU_IPCS_CORE_SHM(</td>)",
        r"\1SWU_IPCS_HAL_MCU\2",
        hal,
    )
    return head + hal + "## 4.3 AUTOSAR" + tail


def fix_osal_section_unit(md: str, start_marker: str, end_marker: str, unit: str) -> str:
    parts = md.split(start_marker, 1)
    if len(parts) < 2:
        return md
    head, rest = parts[0] + start_marker, parts[1]
    if end_marker in rest:
        body, tail = rest.split(end_marker, 1)
    else:
        body, tail = rest, ""
    body = re.sub(
        r"(<td>软件单元 ID</td>\s*\n<td colspan=\"4\">)SWU_IPCS_OSAL_\w+(</td>)",
        rf"\1{unit}\2",
        body,
    )
    return head + body + end_marker + tail


def update_ch6_audit(md: str) -> str:
    audit = """## 6.3 源码核对结果

核对基准：`ipcs/` 目录（2026-05-19），与本文档设计条目一致。

| 路径 | 纳入章节 | 说明 |
|---|---|---|
| ipcs/ipcs_cores/ipc-shm.c | §3.2、§3.3–3.4 | Core 对外/内部 API 与源码一致 |
| ipcs/ipcs_cores/ipc-queue.c | §3.2、§3.4.1–3.4.5 | 队列单元 |
| ipcs/ipcs_cores/ipc-util.c | §3.2、§3.4.23 | memcpy 等工具 |
| ipcs/ipcs_cores/ipc-types.h | §3.6 | 配置与 BD 类型 |
| ipcs/mcu/hw/ipc-hw.c | §4.2、§4.6 | RTOS HAL；`ipcsHw*` 与 §4.6 一致 |
| ipcs/mcu/os/autosar/ipc-os-autosar.c | §4.3 | AUTOSAR OSAL |
| ipcs/mcu/os/freertos/ipc-os-freertos.c | §4.4 | FreeRTOS OSAL |
| ipcs/mcu/os/threadx/ipc-os-threadx.c | §4.5 | ThreadX OSAL |
| ipcs/mcu/os/baremetal/ipc-os-baremetal.c | — | 不在 SDD 范围 |
| ipcs/mpu/os_kernel/ipc-os.c | §5.3 | 全内核实现 |
| ipcs/mpu/os_uio/ipc-os.c | §5.4 | UIO 用户 Glue |
| ipcs/mpu/os_cdev/ipc-os.c | §5.5 | CDEV 用户 Glue |
| ipcs/mpu/os_kernel/ipc-uio.c、ipc-cdev.c | §5.4–5.5 | 内核 Backend |
| ipcs/mpu/hw/c1/ipc-hw.c | §5、§2.6 | Linux 内核 HAL |

对外 API（`ipcs-shm.h`）：`ipcsShmInit`、`ipcsShmFree`、`ipcsShmAcquireBuf`、`ipcsShmReleaseBuf`、`ipcsShmTx`、`ipcsShmUnmanagedAcquire`、`ipcsShmUnmanagedTx`、`ipcsShmIsRemoteReady`、`ipcsShmPollChannels` — 与 §3.3 一致。

"""
    return re.sub(
        r"## 6\.3 源码核对结果\n\n.*?(?=\n## 6\.4 )",
        audit,
        md,
        flags=re.DOTALL,
    )


def fix_escaped_colspan(md: str) -> str:
    return md.replace('colspan=\\"4\\"', 'colspan="4"')


def fix_hal_units_only(md: str) -> str:
    parts = md.split("## 4.6 HAL", 1)
    if len(parts) < 2:
        return md
    head, rest = parts[0], "## 4.6 HAL" + parts[1]
    hal, tail = rest.split("## 4.3 AUTOSAR", 1)
    hal = hal.replace(
        "SWU_IPCS_CORE_SHM</td>",
        "SWU_IPCS_HAL_MCU</td>",
    )
    return head + hal + "## 4.3 AUTOSAR" + tail


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    md = fix_escaped_colspan(md)
    md = fix_hal_units_only(md)
    md = fix_broken_tables(md)
    md = renumber_ch4_files(md)
    md = renumber_hal_funcs(md)
    md = fix_hal_arch_and_unit(md)
    md = fix_osal_section_unit(md, "## 4.4 FreeRTOS", "## 4.5 ThreadX", "SWU_IPCS_OSAL_FREERTOS")
    md = fix_osal_section_unit(md, "## 4.5 ThreadX", "# 5 Linux", "SWU_IPCS_OSAL_THREADX")
    md = update_ch6_audit(md)
    MD.write_text(md, encoding="utf-8")
    print("Post-fix complete")


if __name__ == "__main__":
    main()
