# -*- coding: utf-8 -*-
"""Generate PlantUML component diagrams (pale khaki) for ipcs_sdd.md section 3.2."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "scripts" / "plantuml.jar"
OUT_SVG = ROOT / "files_32_svgs"
OUT_PUML = ROOT / "files_32_umls"

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


def w(name: str, body: str) -> None:
    OUT_PUML.mkdir(parents=True, exist_ok=True)
    (OUT_PUML / f"{name}.puml").write_text(HEADER + body.strip() + "\n@enduml\n", encoding="utf-8")


def main() -> None:
    if not JAR.is_file():
        sys.exit(f"missing {JAR}")

    w(
        "3_2_2",
        """
left to right direction
title common/ipc-queue.c — #include 依赖（组件视图）
component [common/ipc-queue.c] as SRC
component [ipc-shm.h] as H0
component [ipc-queue.h] as H1
component [ipc-util.h] as H2
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
""",
    )

    w(
        "3_2_3",
        """
title common/ipc-queue.h — 无 IPCS_49 内其他头文件
component [common/ipc-queue.h] as H
note right of H
  除标准版本信息外，无工程内其他 .h 依赖
end note
""",
    )

    w(
        "3_2_4",
        """
left to right direction
title common/ipc-shm.c — #include 依赖
component [common/ipc-shm.c] as SRC
component [ipc-shm.h] as H0
component [ipc-os.h] as H1
component [ipc-hw.h] as H2
component [ipc-queue.h] as H3
SRC ..> H0 : #include
SRC ..> H1 : #include
SRC ..> H2 : #include
SRC ..> H3 : #include
""",
    )

    w(
        "3_2_5",
        """
title common/ipc-shm.h — #include 依赖
component [common/ipc-shm.h] as SRC
component [ipc-types.h] as H0
component [ipcf_Ip_Cfg.h] as H1 <<config>>
SRC ..> H0 : #include
SRC ..> H1 : #include
""",
    )

    w(
        "3_2_6",
        """
title common/ipc-types.h — 条件与配置头依赖
component [common/ipc-types.h] as R
package "NO_STDINT_H == 0" {
  component [<stdint.h>] as U1 <<system>>
  component [<stddef.h>] as U2 <<system>>
  component [<errno.h>] as U3 <<system>>
}
package "NO_STDINT_H != 0" {
  component [uintptr_t 等\\\n(CPU_* 定义)] as CPU <<macros>>
}
component [Mcal.h] as M <<external>>
component [ipcf_Ip_Cfg_Defines.h] as D <<config>>
R ..> M : #include
R ..> D : #include
R ..> U1 : 条件
R ..> U2 : 条件
R ..> U3 : 条件
R ..> CPU : else
""",
    )

    w(
        "3_2_7",
        """
left to right direction
title common/ipc-util.c — #include 依赖
component [common/ipc-util.c] as SRC
component [ipc-shm.h] as H0
component [ipc-util.h] as H1
SRC ..> H0 : #include
SRC ..> H1 : #include
""",
    )

    w(
        "3_2_8",
        """
title common/ipc-util.h — 无 IPCS_49 内其他头文件
component [common/ipc-util.h] as H
note right of H : 工程内无其他 .h #include
""",
    )

    w(
        "3_2_9",
        """
title hw/ipc-hw-platform.h — 平台条件头
component [hw/ipc-hw-platform.h] as P
component [S32G399A_M7_COMMON.h] as S1 <<S32G3XX>>
component [S32G399A_SCB.h] as S2 <<S32G3XX>>
component [S32G399A_MSCM.h] as S3 <<S32G3XX>>
P ..> S1 : ifdef S32G3XX
P ..> S2 : ifdef S32G3XX
P ..> S3 : ifdef S32G3XX
note bottom of P : 未定义 S32G3XX 则无上述平台寄存器头
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
