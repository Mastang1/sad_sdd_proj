#!/usr/bin/env python3
"""Verify §5.2 / §6.2 file list matches ipcs/mcu and ipcs/mpu on disk."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"

RTOS_EXPECTED = {
    "ipcs/mcu/hw/ipc-hw-platform.h",
    "ipcs/mcu/hw/ipc-hw.c",
    "ipcs/mcu/hw/ipc-hw.h",
    "ipcs/mcu/os/autosar/ipc-os-autosar.c",
    "ipcs/mcu/os/freertos/ipc-os-freertos.c",
    "ipcs/mcu/os/ipc-os.h",
    "ipcs/mcu/os/threadx/ipc-os-threadx.c",
    "ipcs/mcu/ipc-shm-rtos.mk",
}

MPU_EXPECTED = {
    "ipcs/mpu/os_uio/ipc-os.c",
    "ipcs/mpu/os_uio/ipc-os.h",
    "ipcs/mpu/os_cdev/ipc-os.c",
    "ipcs/mpu/os_cdev/ipc-os.h",
    "ipcs/mpu/os_kernel/ipc-os.c",
    "ipcs/mpu/os_kernel/ipc-os.h",
    "ipcs/mpu/os_kernel/ipc-uio.c",
    "ipcs/mpu/os_kernel/ipc-uio.h",
    "ipcs/mpu/os_kernel/ipc-cdev.c",
    "ipcs/mpu/os_kernel/ipc-cdev.h",
    "ipcs/mpu/hw/c1/ipc-hw.c",
    "ipcs/mpu/hw/c1/ipc-hw-platform.h",
    "ipcs/mpu/hw/ipc-hw.h",
}


def extract_table_paths(text: str, section_marker: str, next_marker: str) -> set[str]:
    start = text.find(section_marker)
    end = text.find(next_marker, start)
    block = text[start:end]
    return set(re.findall(r"(ipcs/mcu/[^\s`|]+|ipcs/mpu/[^\s`|]+)", block))


def main() -> int:
    text = MD.read_text(encoding="utf-8")
    md_rtos = extract_table_paths(text, "### 5.2.1 文件列表", "## 5.3")
    md_mpu = extract_table_paths(text, "### 6.2.1 文件列表", "## 6.3")
    err = 0
    for label, expected, found in [
        ("RTOS §5.2.1", RTOS_EXPECTED, md_rtos),
        ("Linux §6.2.1", MPU_EXPECTED, md_mpu),
    ]:
        missing = expected - found
        extra = found - expected
        if missing:
            print(f"[FAIL] {label} missing in MD: {sorted(missing)}")
            err = 1
        if extra:
            print(f"[FAIL] {label} extra in MD: {sorted(extra)}")
            err = 1
        if not missing and not extra:
            print(f"[OK] {label}: {len(expected)} files")
    if err:
        return 1
    print("verify_ch56_files: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
