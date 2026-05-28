#!/usr/bin/env python3
"""Generate §5.2 / §6.2 component dependency diagrams (pale khaki, no title)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
from workspace_paths import FILES_32_SVGS, FILES_32_UMLS, PLANTUML_JAR, WORKSPACE_ROOT

HEADER = """@startuml
skinparam backgroundColor #FFFCF5
skinparam component {
  BackgroundColor #F5E6CC
  BorderColor #8B7355
  FontSize 11
}
skinparam package {
  BackgroundColor #FAF0E0
  BorderColor #A08060
}
skinparam arrowColor #5C4033
skinparam note {
  BackgroundColor #FFF8E8
  BorderColor #B89968
}
"""

# (slug, rel_path, [(dep, stereotype)], note|None, left_to_right)
DIAGRAMS: list[tuple] = [
    (
        "5_2_02",
        "ipcs/mcu/hw/ipc-hw-platform.h",
        [
            ("C1_M7_COMMON.h", "platform"),
            ("C1_SCB.h", "platform"),
            ("C1_MSCM.h", "platform"),
        ],
        None,
        True,
    ),
    (
        "5_2_03",
        "ipcs/mcu/hw/ipc-hw.c",
        [
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-hw-platform.h", None),
        ],
        None,
        True,
    ),
    (
        "5_2_04",
        "ipcs/mcu/hw/ipc-hw.h",
        [],
        "仅 HAL API 声明，无工程内其他 .h #include",
        False,
    ),
    (
        "5_2_05",
        "ipcs/mcu/os/autosar/ipc-os-autosar.c",
        [
            ("<Os.h>", "autosar"),
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
        ],
        None,
        False,
    ),
    (
        "5_2_06",
        "ipcs/mcu/os/freertos/ipc-os-freertos.c",
        [
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("FreeRTOS.h", "kernel"),
            ("task.h", "kernel"),
        ],
        None,
        True,
    ),
    (
        "5_2_07",
        "ipcs/mcu/os/ipc-os.h",
        [],
        "OSAL API 声明，无工程内其他 .h #include",
        False,
    ),
    (
        "5_2_08",
        "ipcs/mcu/os/threadx/ipc-os-threadx.c",
        [
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("tx_api.h", "threadx"),
            ("tx_event_flags.h", "threadx"),
        ],
        None,
        True,
    ),
    (
        "6_2_02",
        "ipcs/mpu/os_uio/ipc-os.c",
        [
            ("fcntl.h", "posix"),
            ("unistd.h", "posix"),
            ("stdio.h", "posix"),
            ("sys/mman.h", "posix"),
            ("sys/syscall.h", "posix"),
            ("pthread.h", "posix"),
            ("stdlib.h", "posix"),
            ("dirent.h", "posix"),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-shm.h", None),
            ("ipc-uio.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_03",
        "ipcs/mpu/os_uio/ipc-os.h",
        [
            ("errno.h", "posix"),
            ("stdint.h", "posix"),
            ("stdbool.h", "posix"),
            ("string.h", "posix"),
            ("stdio.h", "posix"),
        ],
        "用户侧 OSAL 头；无 ipcs 内其他头",
        False,
    ),
    (
        "6_2_04",
        "ipcs/mpu/os_cdev/ipc-os.c",
        [
            ("fcntl.h", "posix"),
            ("unistd.h", "posix"),
            ("stdio.h", "posix"),
            ("sys/mman.h", "posix"),
            ("sys/syscall.h", "posix"),
            ("sys/ioctl.h", "posix"),
            ("pthread.h", "posix"),
            ("stdlib.h", "posix"),
            ("dirent.h", "posix"),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-shm.h", None),
            ("ipc-cdev.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_05",
        "ipcs/mpu/os_cdev/ipc-os.h",
        [
            ("errno.h", "posix"),
            ("stdint.h", "posix"),
            ("stdbool.h", "posix"),
            ("string.h", "posix"),
            ("stdio.h", "posix"),
        ],
        "用户侧 OSAL 头；无 ipcs 内其他头",
        False,
    ),
    (
        "6_2_06",
        "ipcs/mpu/os_kernel/ipc-os.c",
        [
            ("linux/ioport.h", "linux"),
            ("linux/io.h", "linux"),
            ("linux/interrupt.h", "linux"),
            ("linux/of_irq.h", "linux"),
            ("linux/of_address.h", "linux"),
            ("linux/version.h", "linux"),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-shm.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_07",
        "ipcs/mpu/os_kernel/ipc-os.h",
        [("linux/module.h", "linux")],
        "内核 OSAL 头",
        False,
    ),
    (
        "6_2_08",
        "ipcs/mpu/os_kernel/ipc-uio.c",
        [
            ("linux/module.h", "linux"),
            ("linux/platform_device.h", "linux"),
            ("linux/mod_devicetable.h", "linux"),
            ("linux/uio_driver.h", "linux"),
            ("linux/cdev.h", "linux"),
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-uio.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_09",
        "ipcs/mpu/os_kernel/ipc-uio.h",
        [],
        "UIO 命令宏；无 #include",
        False,
    ),
    (
        "6_2_10",
        "ipcs/mpu/os_kernel/ipc-cdev.c",
        [
            ("linux/module.h", "linux"),
            ("linux/kernel.h", "linux"),
            ("linux/fs.h", "linux"),
            ("linux/cdev.h", "linux"),
            ("linux/interrupt.h", "linux"),
            ("linux/of_irq.h", "linux"),
            ("linux/of_address.h", "linux"),
            ("linux/wait.h", "linux"),
            ("asm/errno.h", "linux"),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-shm.h", None),
            ("ipc-cdev.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_11",
        "ipcs/mpu/os_kernel/ipc-cdev.h",
        [
            ("linux/ioctl.h", "linux"),
            ("sys/ioctl.h", "posix"),
        ],
        "ioctl 命令定义",
        False,
    ),
    (
        "6_2_12",
        "ipcs/mpu/hw/c1/ipc-hw.c",
        [
            ("linux/io.h", "linux"),
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-hw-platform.h", None),
        ],
        None,
        True,
    ),
    (
        "6_2_13",
        "ipcs/mpu/hw/c1/ipc-hw-platform.h",
        [],
        "Linux 平台核索引与 MSCM 寄存器布局定义；无 #include",
        False,
    ),
    (
        "6_2_14",
        "ipcs/mpu/hw/ipc-hw.h",
        [],
        "HAL API 声明（Linux 与 RTOS 共用头文件路径）",
        False,
    ),
]


def stereotype(st: str | None) -> str:
    if not st:
        return ""
    return f" <<{st}>>"


def build_body(
    rel_path: str,
    deps: list[tuple[str, str | None]],
    note: str | None,
    ltr: bool,
) -> str:
    name = rel_path.split("/")[-1]
    lines: list[str] = []
    if ltr:
        lines.append("left to right direction")
    lines.append(f'component [{name}] as SRC')
    if not deps and note:
        lines.append(f"note right of SRC : {note}")
        return "\n".join(lines) + "\n"
    for i, (dep, st) in enumerate(deps):
        label = dep if dep.startswith("<") or "/" in dep else dep
        lines.append(f'component [{label}] as H{i}{stereotype(st)}')
    for i, (dep, _) in enumerate(deps):
        lines.append(f"SRC ..> H{i}")
    if note:
        lines.append(f"note bottom of SRC : {note}")
    return "\n".join(lines) + "\n"


def main() -> int:
    if not PLANTUML_JAR.is_file():
        print(f"missing {PLANTUML_JAR}", file=sys.stderr)
        return 1
    FILES_32_UMLS.mkdir(parents=True, exist_ok=True)
    FILES_32_SVGS.mkdir(parents=True, exist_ok=True)
    puml_paths: list[Path] = []
    for slug, rel, deps, note, ltr in DIAGRAMS:
        body = build_body(rel, deps, note, ltr)
        p = FILES_32_UMLS / f"{slug}.puml"
        p.write_text(HEADER + body + "@enduml\n", encoding="utf-8")
        puml_paths.append(p)
    subprocess.check_call(
        [
            "java",
            "-jar",
            str(PLANTUML_JAR),
            "-charset",
            "UTF-8",
            "-tsvg",
            "-o",
            str(FILES_32_SVGS),
            *[str(p) for p in puml_paths],
        ]
    )
    print(f"wrote {len(puml_paths)} diagrams -> {FILES_32_SVGS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
