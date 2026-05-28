# -*- coding: utf-8 -*-
"""Generate PlantUML component diagrams (pale khaki) for ipcs_sdd.md section 3.2."""
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

JAR = PLANTUML_JAR
OUT_SVG = FILES_32_SVGS
OUT_PUML = FILES_32_UMLS
import subprocess
import sys
from pathlib import Path


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

# §4.2 Files — ipcs/ipcs_cores/ component diagrams (slug 3_2_2 .. 3_2_8)
CH4_DIAGRAMS = [
    (
        "3_2_2",
        "ipcs/ipcs_cores/ipc-queue.c",
        [("ipc-shm.h", None), ("ipc-queue.h", None), ("ipc-util.h", None)],
        None,
        True,
    ),
    (
        "3_2_3",
        "ipcs/ipcs_cores/ipc-queue.h",
        [],
        "除标准版本信息外，无工程内其他 .h 依赖",
        False,
    ),
    (
        "3_2_4",
        "ipcs/ipcs_cores/ipc-shm.c",
        [
            ("ipc-shm.h", None),
            ("ipc-os.h", None),
            ("ipc-hw.h", None),
            ("ipc-queue.h", None),
        ],
        None,
        True,
    ),
    (
        "3_2_5",
        "ipcs/ipcs_cores/ipc-shm.h",
        [("ipc-types.h", None), ("ipcf_Ip_Cfg.h", "config")],
        None,
        False,
    ),
    (
        "3_2_6",
        "ipcs/ipcs_cores/ipc-types.h",
        None,  # special body
        False,
    ),
    (
        "3_2_7",
        "ipcs/ipcs_cores/ipc-util.c",
        [("ipc-shm.h", None), ("ipc-util.h", None)],
        None,
        True,
    ),
    (
        "3_2_8",
        "ipcs/ipcs_cores/ipc-util.h",
        [],
        "工程内无其他 .h #include",
        False,
    ),
]


def stereotype(st: str | None) -> str:
    if not st:
        return ""
    return f" <<{st}>>"


def build_ch4_body(
    rel_path: str,
    deps: list[tuple[str, str | None]] | None,
    note: str | None,
    ltr: bool,
) -> str:
    lines: list[str] = []
    if ltr:
        lines.append("left to right direction")
    lines.append(f"component [{rel_path}] as SRC")
    if deps is not None:
        for i, (dep, st) in enumerate(deps):
            lines.append(f"component [{dep}] as H{i}{stereotype(st)}")
        for i, _ in enumerate(deps):
            lines.append(f"SRC ..> H{i}")
    if note:
        lines.append(f"note right of SRC : {note}")
    return "\n".join(lines) + "\n"


def build_ch4_types_body() -> str:
    rel = "ipcs/ipcs_cores/ipc-types.h"
    return f"""component [{rel}] as R
package "NO_STDINT_H == 0" {{
  component [<stdint.h>] as U1 <<system>>
  component [<stddef.h>] as U2 <<system>>
  component [<errno.h>] as U3 <<system>>
}}
package "NO_STDINT_H != 0" {{
  component [uintptr_t 等\\\\n(CPU_* 定义)] as CPU <<macros>>
}}
component [Mcal.h] as M <<external>>
component [ipcf_Ip_Cfg_Defines.h] as D <<config>>
R ..> M
R ..> D
R ..> U1
R ..> U2
R ..> U3
R ..> CPU
"""


def write_ch4_diagrams() -> list[Path]:
    OUT_PUML.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for item in CH4_DIAGRAMS:
        slug = item[0]
        if slug == "3_2_6":
            body = build_ch4_types_body()
        else:
            _, rel, deps, note, ltr = item
            body = build_ch4_body(rel, deps, note, ltr)
        p = OUT_PUML / f"{slug}.puml"
        p.write_text(HEADER + body + "@enduml\n", encoding="utf-8")
        paths.append(p)
    return paths


def render_puml(paths: list[Path]) -> None:
    OUT_SVG.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "java",
            "-jar",
            str(JAR),
            "-charset",
            "UTF-8",
            "-tsvg",
            "-o",
            str(OUT_SVG),
            *[str(p) for p in paths],
        ]
    )


def w(name: str, body: str) -> None:
    OUT_PUML.mkdir(parents=True, exist_ok=True)
    (OUT_PUML / f"{name}.puml").write_text(
        HEADER + body.strip() + "\n@enduml\n", encoding="utf-8"
    )


def main() -> None:
    if not JAR.is_file():
        sys.exit(f"missing {JAR}")

    ch4_paths = write_ch4_diagrams()
    render_puml(ch4_paths)
    print(f"wrote {len(ch4_paths)} §4.2 .puml and SVG under {OUT_SVG}/")

    w(
        "3_2_9",
        """
left to right direction
component [ipcs/mcu/hw/ipc-hw-platform.h] as P
component [C1_M7_COMMON.h] as S1 <<platform>>
component [C1_SCB.h] as S2 <<platform>>
component [C1_MSCM.h] as S3 <<platform>>
P ..> S1
P ..> S2
P ..> S3
""",
    )

    w(
        "3_2_10",
        """
title hw/ipc-hw.c — #include 依赖
component [hw/ipc-hw.c] as SRC
component [ipc-shm.h] as H0
component [ipc-os.h] as H1
component [ipc-hw.h] as H2
component [ipc-hw-platform.h] as H3
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
SRC ..> H3 : #include
""",
    )

    w(
        "3_2_11",
        """
title hw/ipc-hw.h — HAL API，无 IPCS .h #include
component [hw/ipc-hw.h] as H
note right of H : 仅 HAL API 声明
""",
    )

    w(
        "3_2_13",
        """
title os/autosar/ipc-os-autosar.c — #include 依赖
component [os/autosar/ipc-os-autosar.c] as SRC
component [<Os.h>] as OH <<autosar>>
component [ipc-shm.h] as H1
component [ipc-os.h] as H2
component [ipc-hw.h] as H3
SRC ..> OH : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
SRC ..> H3 : #include
""",
    )

    w(
        "3_2_14",
        """
left to right direction
title os/baremetal/ipc-os-baremetal.c — #include 依赖
component [os/baremetal/ipc-os-baremetal.c] as SRC
component [ipc-shm.h] as H0
component [ipc-os.h] as H1
component [ipc-hw.h] as H2
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
""",
    )

    w(
        "3_2_15",
        """
left to right direction
title os/freertos/ipc-os-freertos.c — #include 依赖
component [os/freertos/ipc-os-freertos.c] as SRC
component [ipc-shm.h] as H0
component [ipc-os.h] as H1
component [ipc-hw.h] as H2
component [FreeRTOS.h] as F1 <<kernel>>
component [task.h] as F2 <<kernel>>
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
SRC ..> F1 : #include
SRC ..> F2 : #include
""",
    )

    w(
        "3_2_16",
        """
title os/ipc-os.h — OSAL 声明
component [os/ipc-os.h] as H
note right of H : 工程内无其他 IPCS .h #include
""",
    )

    w(
        "3_2_17",
        """
title os/zephyr/ipc-os-zephyr.c — #include 依赖
component [os/zephyr/ipc-os-zephyr.c] as SRC
component [ipc-shm.h] as H0
component [ipc-os.h] as H1
component [ipc-hw.h] as H2
component [<zephyr/sys/mem_manage.h>] as Z1 <<zephyr>>
component [<zephyr/kernel.h>] as Z2 <<zephyr>>
component [<zephyr/device.h>] as Z3 <<zephyr>>
component [Mru_Ip.h] as MR <<S32ZE>>
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
SRC ..> Z1 : #include
SRC ..> Z2 : #include
SRC ..> Z3 : #include
SRC ..> MR : #elif defined(S32ZE)
note bottom of MR
  SAF85/S32R41/S32K3XX 分支仅定义
  IPC_INT_* 宏，不含 Mru_Ip.h
end note
""",
    )

    OUT_SVG.mkdir(parents=True, exist_ok=True)
    pums = sorted(OUT_PUML.glob("*.puml"))
    subprocess.check_call(
        [
            "java",
            "-jar",
            str(JAR),
            "-charset",
            "UTF-8",
            "-tsvg",
            "-o",
            str(OUT_SVG),
            *[str(p) for p in pums],
        ]
    )
    print(f"wrote {len(pums)} .puml and SVG under {OUT_SVG}/")


if __name__ == "__main__":
    main()
