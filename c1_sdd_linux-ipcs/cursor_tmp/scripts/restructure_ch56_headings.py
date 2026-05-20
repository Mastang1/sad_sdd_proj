# -*- coding: utf-8 -*-
"""Restructure md_sdd_0519.md chapter 5/6 level-2 headings and split Linux user/kernel units."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"
BACKUP = ROOT / "cursor_tmp" / f"md_sdd_0519_backup_{datetime.now():%Y%m%d_%H%M%S}.md"

CH5_H2 = {
    "## 5.3 AUTOSAR OS 实现": "## 5.3 SWU_IPCS_OSAL_AUTOSAR 软件单元设计",
    "## 5.4 FreeRTOS 实现": "## 5.4 SWU_IPCS_OSAL_FREERTOS 软件单元设计",
    "## 5.5 ThreadX 实现": "## 5.5 SWU_IPCS_OSAL_THREADX 软件单元设计",
    "## 5.6 HAL 单元设计（MCU 共用）": "## 5.6 SWU_IPCS_HAL_MCU 软件单元设计",
}

MARK_UIO_KO = "### 6.4.16 UIO 内核 Backend 函数"
MARK_CDEV_KO = "### 6.5.11 CDEV 内核 Backend 函数"


def renumber_block(text: str, old_prefix: str, new_prefix: str) -> str:
    """Renumber ### headings and optional ![caption]( paths' caption prefix only."""

    text = re.sub(
        rf"^### {re.escape(old_prefix)}(\.\d+[^\n]*)",
        rf"### {new_prefix}\1",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        rf"(!\[){re.escape(old_prefix)}(\.\d+)",
        rf"\g<1>{new_prefix}\2",
        text,
    )
    return text


def extract_between(text: str, start: str, end: str | None) -> tuple[str, str, str]:
    i = text.index(start)
    if end is None:
        return text[:i], text[i:], ""
    j = text.index(end, i + len(start))
    return text[:i], text[i:j], text[j:]


def main() -> None:
    shutil.copy2(MD, BACKUP)
    text = MD.read_text(encoding="utf-8")

    for old, new in CH5_H2.items():
        text = text.replace(old, new)

    # TOC
    toc_old_new = [
        ("  - 5.3 AUTOSAR OS 实现", "  - 5.3 SWU_IPCS_OSAL_AUTOSAR 软件单元设计"),
        ("  - 5.4 FreeRTOS 实现", "  - 5.4 SWU_IPCS_OSAL_FREERTOS 软件单元设计"),
        ("  - 5.5 ThreadX 实现", "  - 5.5 SWU_IPCS_OSAL_THREADX 软件单元设计"),
        ("  - 5.6 HAL 单元设计（MCU 共用）", "  - 5.6 SWU_IPCS_HAL_MCU 软件单元设计"),
        ("  - 6.3 全内核实现函数设计", "  - 6.3 SWU_IPCS_LINUX_OS_KERN 软件单元设计"),
        ("  - 6.4 UIO 实现函数设计", "  - 6.4 SWU_IPCS_LINUX_OS_UIO 软件单元设计"),
        ("  - 6.5 CDEV 实现函数设计", "  - 6.5 SWU_IPCS_LINUX_UIO_KO 软件单元设计"),
        ("  - 6.6 Linux HAL 函数设计", "  - 6.6 SWU_IPCS_LINUX_OS_CDEV 软件单元设计"),
    ]
    # TOC needs full new structure - replace block
    old_toc_6 = """  - 6.3 全内核实现函数设计
  - 6.4 UIO 实现函数设计
  - 6.5 CDEV 实现函数设计
  - 6.6 Linux HAL 函数设计
  - 6.7 Linux 关键场景流程
  - 6.8 Linux 全局变量与私有类型"""
    new_toc_6 = """  - 6.3 SWU_IPCS_LINUX_OS_KERN 软件单元设计
  - 6.4 SWU_IPCS_LINUX_OS_UIO 软件单元设计
  - 6.5 SWU_IPCS_LINUX_UIO_KO 软件单元设计
  - 6.6 SWU_IPCS_LINUX_OS_CDEV 软件单元设计
  - 6.7 SWU_IPCS_LINUX_CDEV_KO 软件单元设计
  - 6.8 Linux HAL 函数设计
  - 6.9 Linux 关键场景流程
  - 6.10 Linux 全局变量与私有类型"""
    text = text.replace(old_toc_6, new_toc_6)
    for old, new in [
        ("  - 5.3 AUTOSAR OS 实现", "  - 5.3 SWU_IPCS_OSAL_AUTOSAR 软件单元设计"),
        ("  - 5.4 FreeRTOS 实现", "  - 5.4 SWU_IPCS_OSAL_FREERTOS 软件单元设计"),
        ("  - 5.5 ThreadX 实现", "  - 5.5 SWU_IPCS_OSAL_THREADX 软件单元设计"),
        ("  - 5.6 HAL 单元设计（MCU 共用）", "  - 5.6 SWU_IPCS_HAL_MCU 软件单元设计"),
    ]:
        text = text.replace(old, new)

    ch6_end_marker = "# 7 Traceability and Consistency Evidence 追溯与一致性证据"
    pre, ch6_body, ch7_on = extract_between(text, "# 6 Linux 部署变体详细设计", ch6_end_marker)

    # Split ch6_body sections
    parts = {}
    markers = [
        ("h61", "## 6.1 总述", "## 6.2 源码与构建结构"),
        ("h62", "## 6.2 源码与构建结构", "## 6.3 全内核实现函数设计"),
        ("s63", "## 6.3 全内核实现函数设计", "## 6.4 UIO 实现函数设计"),
        ("s64", "## 6.4 UIO 实现函数设计", "## 6.5 CDEV 实现函数设计"),
        ("s65", "## 6.5 CDEV 实现函数设计", "## 6.6 Linux HAL 函数设计"),
        ("s66", "## 6.6 Linux HAL 函数设计", "## 6.7 Linux 关键场景流程"),
        ("s67", "## 6.7 Linux 关键场景流程", "## 6.8 Linux 全局变量与私有类型"),
        ("s68", "## 6.8 Linux 全局变量与私有类型", None),
    ]
    chunks: dict[str, str] = {}
    pos = 0
    for key, start, end in markers:
        i = ch6_body.index(start, pos)
        if end:
            j = ch6_body.index(end, i + 1)
            chunks[key] = ch6_body[i:j]
            pos = j
        else:
            chunks[key] = ch6_body[i:]

    sec63 = chunks["s63"]
    sec63 = sec63.replace(
        "## 6.3 全内核实现函数设计",
        "## 6.3 SWU_IPCS_LINUX_OS_KERN 软件单元设计\n\n"
        "源码：`ipcs/mpu/os_kernel/ipc-os.c`。全内核部署变体**无用户侧代理**，OSAL 仅内核侧实现；HAL 见 §6.8。\n",
    )
    sec63 = re.sub(r"^### 6\.3\.0 全内核 OSAL 单元函数\s*\n", "", sec63, flags=re.MULTILINE)
    sec63 = re.sub(
        r"\n+全内核实现由 `ipcs/mpu/os_kernel/ipc-os\.c` 与 `ipcs/mpu/hw/c1/ipc-hw\.c` 构成，无用户侧代理。\n+",
        "\n",
        sec63,
    )

    sec64_full = chunks["s64"]
    split_i = sec64_full.index(MARK_UIO_KO)
    uio_user = sec64_full[:split_i]
    uio_ko = sec64_full[split_i + len(MARK_UIO_KO) + 1 :]
    uio_user = uio_user.replace(
        "## 6.4 UIO 实现函数设计\n\nUIO 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 UIO fd、/dev/mem、pthread 转发到内核。\n",
        "## 6.4 SWU_IPCS_LINUX_OS_UIO 软件单元设计\n\n"
        "源码：`ipcs/mpu/os_uio/ipc-os.c`。用户侧 OSAL/HAL **契约代理**（`ipcsOs*`、`ipcsHw*` 同名符号），通过 UIO fd、`/dev/mem`、pthread 转发至 §6.5 内核 Backend；**不**直接操作 MSCM 硬件。\n",
    )
    uio_ko = renumber_block(uio_ko, "6.4", "6.5")
    uio_ko = (
        "## 6.5 SWU_IPCS_LINUX_UIO_KO 软件单元设计\n\n"
        "源码：`ipcs/mpu/os_kernel/ipc-uio.c`。UIO 内核 Backend：UIO 设备注册、中断处理、向用户态传递事件；与 §6.8 HAL 协同完成硬件 IRQ。\n"
        + uio_ko.lstrip()
    )

    sec65_full = chunks["s65"]
    split_j = sec65_full.index(MARK_CDEV_KO)
    cdev_user = sec65_full[:split_j]
    cdev_ko = sec65_full[split_j + len(MARK_CDEV_KO) + 1 :]
    cdev_user = cdev_user.replace(
        "## 6.5 CDEV 实现函数设计\n\nCDEV 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 cdev ioctl/poll/mmap 与内核通信。\n",
        "## 6.6 SWU_IPCS_LINUX_OS_CDEV 软件单元设计\n\n"
        "源码：`ipcs/mpu/os_cdev/ipc-os.c`。用户侧 OSAL/HAL **契约代理**，通过字符设备 ioctl/poll/mmap 与 §6.7 内核 Backend 通信；`ipcsHwInit`/`ipcsHwFree` 为空实现（硬件初始化在内核）。\n",
    )
    cdev_user = renumber_block(cdev_user, "6.5", "6.6")
    cdev_ko = renumber_block(cdev_ko, "6.5", "6.7")
    cdev_ko = (
        "## 6.7 SWU_IPCS_LINUX_CDEV_KO 软件单元设计\n\n"
        "源码：`ipcs/mpu/os_kernel/ipc-cdev.c`。CDEV 内核 Backend：字符设备、ioctl、wait queue、ISR 与实例初始化。\n"
        + cdev_ko.lstrip()
    )

    sec66 = chunks["s66"].replace("## 6.6 Linux HAL 函数设计", "## 6.8 Linux HAL 函数设计")
    sec66 = renumber_block(sec66, "6.6", "6.8")

    sec67 = chunks["s67"].replace("## 6.7 Linux 关键场景流程", "## 6.9 Linux 关键场景流程")
    sec67 = sec67.replace("第 6.3–6.6 节", "第 6.3–6.8 节")
    sec67 = renumber_block(sec67, "6.7", "6.9")

    sec68 = chunks["s68"].replace(
        "## 6.8 Linux 全局变量与私有类型", "## 6.10 Linux 全局变量与私有类型"
    )

    new_ch6 = (
        "# 6 Linux 部署变体详细设计\n\n"
        + chunks["h61"]
        + chunks["h62"]
        + sec63
        + uio_user
        + uio_ko
        + cdev_user
        + cdev_ko
        + sec66
        + sec67
        + sec68
    )

    text = pre + new_ch6 + ch7_on
    MD.write_text(text, encoding="utf-8")
    print(f"backup: {BACKUP}")
    print("wrote:", MD)


if __name__ == "__main__":
    main()
