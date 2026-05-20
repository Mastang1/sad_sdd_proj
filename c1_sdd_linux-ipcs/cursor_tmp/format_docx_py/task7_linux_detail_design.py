# -*- coding: utf-8 -*-
r"""
task-7：完善 ``md_sdd_0519.md`` 中 Linux 部署变体详细设计。

使用方式（在仓库根目录执行）::

    python format_docx_py/task7_linux_detail_design.py

脚本行为：

1. 读取 ``ipcs/mpu`` 下 Linux 用户侧代理、内核 Backend、全内核 OSAL、Linux HAL 源码。
2. 根据源码函数签名生成第 6 章函数设计表；表格采用 Markdown 表格，便于后续 Pandoc/python-docx 转换。
3. 在 ``flow_umls/`` 生成 PlantUML 活动图源码；SVG 由 ``format_docx_py/render_linux_ch6_flows.py``
   通过 ``plantuml.jar`` 渲染（仓库根目录或 ``scripts/plantuml.jar``）。
4. 在第 3 章插入分层/部署静态图，在第 6 章插入 Linux 关键场景流程图和所有函数处理流程图。
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
import html
import re
from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True)
class Unit:
    title: str
    arch_id: str
    unit_id: str
    source: str
    header: str
    role: str
    functions: list[str]


UNITS: list[Unit] = [
    Unit(
        "全内核 OSAL 单元函数",
        "Drv_Ipcs_Osal_Cmp / Drv_Ipcs_Linux_Adapt_Cmp",
        "SWU_IPCS_LINUX_OS_KERN",
        "ipcs/mpu/os_kernel/ipc-os.c",
        "ipcs/mpu/os_kernel/ipc-os.h",
        "Linux 全内核实现中的 OSAL，完成内核态共享内存映射、IRQ 注册、tasklet 延迟处理和轮询入口。",
        [
            "ipcsShmSoftirq",
            "ipcsShmHardirq",
            "ipcsOsInit",
            "ipcsOsFree",
            "ipcsOsGetLocalShm",
            "ipcsOsGetRemoteShm",
            "ipcsOsMapIntc",
            "ipcsOsUnmapIntc",
            "ipcsOsPollChannels",
            "shm_mod_init",
            "shm_mod_exit",
        ],
    ),
    Unit(
        "UIO 用户侧代理单元函数",
        "Drv_Ipcs_Linux_Adapt_Cmp",
        "SWU_IPCS_LINUX_OS_UIO",
        "ipcs/mpu/os_uio/ipc-os.c",
        "ipcs/mpu/os_uio/ipc-os.h",
        "UIO 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 UIO fd、/dev/mem、pthread 转发到内核。",
        [
            "line_from_file",
            "line_match",
            "get_uio_dev_name",
            "ipcsShmSoftirq",
            "ipcsOsInit",
            "ipcsOsFree",
            "ipcsOsGetLocalShm",
            "ipcsOsGetRemoteShm",
            "ipcsOsPollChannels",
            "ipcsSendUioCmd",
            "ipcsHwIrqEnable",
            "ipcsHwIrqDisable",
            "ipcsHwIrqNotify",
            "ipcsHwInit",
            "ipcsHwFree",
        ],
    ),
    Unit(
        "UIO 内核 Backend 单元函数",
        "Drv_Ipcs_Linux_Adapt_Cmp",
        "SWU_IPCS_LINUX_UIO_KO",
        "ipcs/mpu/os_kernel/ipc-uio.c",
        "ipcs/mpu/os_kernel/ipc-uio.h",
        "UIO 内核 Backend，注册 UIO 设备和初始 cdev 通道，处理中断并把事件交给用户侧代理。",
        [
            "ipcsShmUioOpen",
            "ipcsShmUioRelease",
            "ipcsShmUioIrqcontrol",
            "ipcsShmUioHandler",
            "ipcsUioInit",
            "ipcsCdevOpen",
            "ipcsCdevRelease",
            "ipcsCdevWrite",
            "ipcsShmUioProbe",
            "ipcsShmUioRemove",
            "ipcsOsMapIntc",
            "ipcsOsUnmapIntc",
        ],
    ),
    Unit(
        "CDEV 用户侧代理单元函数",
        "Drv_Ipcs_Linux_Adapt_Cmp",
        "SWU_IPCS_LINUX_OS_CDEV",
        "ipcs/mpu/os_cdev/ipc-os.c",
        "ipcs/mpu/os_cdev/ipc-os.h",
        "CDEV 用户库代理，向 SHM Core 提供同名 OSAL/HAL 契约符号，并通过 cdev ioctl/poll/mmap 与内核通信。",
        [
            "ipcsOsInit",
            "ipcsOsFree",
            "ipcsOsGetLocalShm",
            "ipcsOsGetRemoteShm",
            "ipcsOsPollChannels",
            "ipcsHwIrqEnable",
            "ipcsHwIrqDisable",
            "ipcsHwIrqNotify",
            "ipcsHwInit",
            "ipcsHwFree",
        ],
    ),
    Unit(
        "CDEV 内核 Backend 单元函数",
        "Drv_Ipcs_Linux_Adapt_Cmp",
        "SWU_IPCS_LINUX_CDEV_KO",
        "ipcs/mpu/os_kernel/ipc-cdev.c",
        "ipcs/mpu/os_kernel/ipc-cdev.h",
        "CDEV 内核 Backend，提供字符设备、wait queue、ioctl 和 ISR 处理。",
        [
            "ipcsShmHardirq",
            "ipcsOsMapIntc",
            "ipcsOsUnmapIntc",
            "ipcsCdevOpen",
            "ipcsCdevRelease",
            "ipcsCdevRead",
            "ipcsCdevOsInit",
            "ipcsCdevIoctl",
            "ipcsCdevInit",
            "ipcsCdevClean",
        ],
    ),
    Unit(
        "Linux HAL 单元函数",
        "Drv_Ipcs_Hal_Cmp",
        "SWU_IPCS_HAL_LINUX",
        "ipcs/mpu/hw/c1/ipc-hw.c",
        "ipcs/mpu/hw/ipc-hw.h",
        "Linux 内核侧 HAL，完成 MSCM 映射、核索引解析、IRQ 使能/禁止/通知/清除等硬件操作。",
        [
            "ipcsHwGetRxIrq",
            "ipcsHwInit",
            "_ipcsHwInit",
            "ipcsHwFree",
            "ipcsHwIrqEnable",
            "ipcsHwIrqDisable",
            "ipcsHwIrqNotify",
            "ipcsHwIrqClear",
        ],
    ),
]


DESCRIPTIONS = {
    "ipcsShmSoftirq": "延迟收包处理，遍历实例并调用上层 rx_cb，完成后重新使能 IRQ。",
    "ipcsShmHardirq": "硬中断处理，禁止并清除远端通知，中断后续处理交给 tasklet 或等待队列。",
    "ipcsOsInit": "初始化指定实例的 Linux OSAL 资源，建立共享内存映射、记录回调并配置接收中断。",
    "ipcsOsFree": "释放指定实例 OSAL 资源，关闭线程/设备、解除映射并清理状态。",
    "ipcsOsGetLocalShm": "返回本地共享内存虚拟地址。",
    "ipcsOsGetRemoteShm": "返回远端共享内存虚拟地址。",
    "ipcsOsMapIntc": "映射或返回中断控制器寄存器空间。",
    "ipcsOsUnmapIntc": "释放中断控制器寄存器映射或提供对应空实现。",
    "ipcsOsPollChannels": "在轮询模式下触发 rx_cb 处理接收通道。",
    "shm_mod_init": "Linux 全内核模块初始化入口。",
    "shm_mod_exit": "Linux 全内核模块退出入口。",
    "line_from_file": "读取 sysfs 文件中的一行内容。",
    "line_match": "比较 sysfs 文件内容与目标过滤字符串。",
    "get_uio_dev_name": "在 sysfs 中查找匹配实例的 UIO 设备名。",
    "ipcsSendUioCmd": "向 UIO fd 写入命令，代理 IRQ 使能、禁止或通知。",
    "ipcsHwIrqEnable": "使能指定实例接收中断；用户侧为转发代理，内核侧访问硬件。",
    "ipcsHwIrqDisable": "禁止指定实例接收中断；用户侧为转发代理，内核侧访问硬件。",
    "ipcsHwIrqNotify": "通知远端有数据可用；用户侧为转发代理，内核侧触发硬件中断。",
    "ipcsHwInit": "初始化 HAL 资源；用户侧为空实现，内核侧映射并配置 MSCM/IRQ。",
    "ipcsHwFree": "释放 HAL 资源；用户侧为空实现，内核侧释放映射状态。",
    "ipcsShmUioOpen": "处理 UIO 设备打开请求并维护引用计数。",
    "ipcsShmUioRelease": "处理 UIO 设备关闭请求并恢复引用计数。",
    "ipcsShmUioIrqcontrol": "处理 UIO irqcontrol 命令并调用 HAL IRQ 操作。",
    "ipcsShmUioHandler": "UIO 中断处理，禁止并清除 IRQ，返回 IRQ_HANDLED 唤醒用户态。",
    "ipcsUioInit": "根据用户配置初始化 UIO 实例、HAL 与 IRQ，并注册 UIO 设备。",
    "ipcsCdevOpen": "处理字符设备打开请求。",
    "ipcsCdevRelease": "处理字符设备关闭请求。",
    "ipcsCdevWrite": "接收用户侧 UIO 配置并初始化对应 UIO 设备。",
    "ipcsShmUioProbe": "平台驱动 probe，映射 MSCM 资源并创建设备节点。",
    "ipcsShmUioRemove": "平台驱动 remove，注销设备并释放 UIO 实例。",
    "ipcsCdevRead": "阻塞等待内核接收中断唤醒。",
    "ipcsCdevOsInit": "初始化 CDEV 后端实例、HAL 和接收 IRQ。",
    "ipcsCdevIoctl": "处理 CDEV 用户侧 ioctl 命令，包括实例初始化和 IRQ 操作代理。",
    "ipcsCdevInit": "CDEV 模块初始化，创建字符设备和 wait queue。",
    "ipcsCdevClean": "CDEV 模块清理，禁止 IRQ、释放中断并销毁字符设备。",
    "ipcsHwGetRxIrq": "返回指定实例使用的 MSCM 接收中断索引。",
    "_ipcsHwInit": "HAL 底层初始化，供 Linux UIO 等内核路径复用。",
    "ipcsHwIrqClear": "清除指定实例接收中断状态。",
}


def _read_source(rel: str) -> str:
    return (WORKSPACE_ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def extract_signature(source_text: str, func: str) -> str:
    pattern = re.compile(
        rf"(^[a-zA-Z_][\w\s\*\n]*?\b{re.escape(func)}\s*\([^;{{]*?\))\s*\{{",
        re.MULTILINE,
    )
    m = pattern.search(source_text)
    if not m:
        return f"{func}(...)"
    sig = " ".join(m.group(1).split())
    return sig


def return_type(signature: str, func: str) -> str:
    prefix = signature.split(func, 1)[0].strip()
    prefix = re.sub(r"\bstatic\b", "", prefix).strip()
    return prefix or "-"


def params(signature: str) -> list[tuple[str, str]]:
    m = re.search(r"\((.*)\)", signature)
    if not m:
        return []
    raw = m.group(1).strip()
    if not raw or raw == "void":
        return []
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in raw:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    items = []
    for p in parts:
        p = p.strip()
        fp = re.search(r"\(\s*\*\s*(\w+)\s*\)", p)
        if fp:
            name = fp.group(1)
        else:
            name = p.split()[-1].replace("*", "").strip()
        items.append((name, p))
    return items


def flow_steps(func: str, unit: Unit) -> list[str]:
    if func in {"ipcsHwIrqEnable", "ipcsHwIrqDisable", "ipcsHwIrqNotify"}:
        if "os_uio" in unit.source:
            return ["Start", "Build UIO command", "write command to UIO fd", "Kernel UIO irqcontrol executes HAL operation", "End"]
        if "os_cdev" in unit.source:
            return ["Start", "Build CDEV ioctl command", "ioctl to kernel cdev", "Kernel backend executes HAL operation", "End"]
        return ["Start", "Validate instance", "Access MSCM IRQ register", "Update enable/notify state", "End"]
    if func in {"ipcsHwInit", "_ipcsHwInit"}:
        return ["Start", "Read configuration", "Map MSCM register space", "Validate IRQ/core settings", "Store HAL private data", "End"]
    if func == "ipcsOsInit":
        return ["Start", "Validate instance/config", "Map shared memory", "Store callback/private state", "Configure IRQ or polling path", "End"]
    if "Hardirq" in func or "Handler" in func:
        return ["IRQ entry", "Find active instance", "Disable IRQ", "Clear IRQ", "Wake deferred/user processing", "IRQ_HANDLED"]
    if "Softirq" in func:
        return ["Deferred entry", "Iterate enabled instances", "Call rx callback", "Reschedule if budget exhausted", "Re-enable IRQ", "End"]
    if "Probe" in func or func.endswith("Init") or func in {"ipcsUioInit", "ipcsCdevInit", "ipcsCdevOsInit"}:
        return ["Start", "Allocate/register kernel resources", "Initialize private data", "Request or register IRQ/device", "Return status"]
    if "Remove" in func or "Clean" in func or "Free" in func or "exit" in func:
        return ["Start", "Disable active IRQ/resources", "Release mappings/devices", "Clear private state", "End"]
    if "Open" in func:
        return ["Start", "Check open/reference state", "Record private data", "Return status"]
    if "Release" in func:
        return ["Start", "Release open/reference state", "Clear private data", "Return status"]
    if "Read" in func:
        return ["Start", "Wait on queue/event", "Clear wake flag", "Return to user"]
    if "Ioctl" in func or "Irqcontrol" in func:
        return ["Start", "Decode command", "Dispatch to init/IRQ operation", "Return status"]
    if "Get" in func or "Map" in func:
        return ["Start", "Read private data or device tree", "Return address/index"]
    return ["Start", "Execute source-defined logic", "Update state or return value", "End"]


def write_puml_and_svg(name: str, title: str, steps: list[str]) -> str:
    FLOW_UMLS.mkdir(exist_ok=True)
    FLOW_SVGS.mkdir(exist_ok=True)
    puml = FLOW_UMLS / f"{name}.puml"
    svg = FLOW_SVGS / f"{name}.svg"
    puml_lines = [
        "@startuml",
        "!pragma layout smetana",
        "skinparam conditionStyle insideDiamond",
        "skinparam linetype ortho",
        "start",
    ]
    for s in steps[1:-1] if steps and steps[0].lower().startswith("start") else steps:
        puml_lines.append(f":{s};")
    puml_lines.extend(["stop", "@enduml", ""])
    puml.write_text("\n".join(puml_lines), encoding="utf-8")

    width = 920
    box_h = 44
    gap = 24
    top = 52
    height = top + len(steps) * (box_h + gap) + 34
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;font-size:15px;fill:#222}.title{font-size:19px;font-weight:bold}.box{fill:#fff8dc;stroke:#555;stroke-width:1.2}.line{stroke:#555;stroke-width:1.2;marker-end:url(#arrow)}</style>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#555"/></marker></defs>',
        f'<text x="{width/2}" y="28" text-anchor="middle" class="title">{html.escape(title)}</text>',
    ]
    x = 110
    y = top
    w = width - 220
    for idx, step in enumerate(steps):
        svg_parts.append(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{box_h}" rx="8"/>')
        svg_parts.append(f'<text x="{width/2}" y="{y + 28}" text-anchor="middle">{html.escape(step)}</text>')
        if idx < len(steps) - 1:
            svg_parts.append(f'<line class="line" x1="{width/2}" y1="{y + box_h}" x2="{width/2}" y2="{y + box_h + gap - 5}"/>')
        y += box_h + gap
    svg_parts.append("</svg>")
    svg.write_text("\n".join(svg_parts), encoding="utf-8")
    return rel_to_workspace(svg).as_posix()


def function_table(unit: Unit, func: str, index: str, sig: str) -> str:
    from function_table_html import build_function_table_html

    desc = DESCRIPTIONS.get(func, f"实现 {unit.role} 中的 {func} 处理逻辑。")
    ret = return_type(sig, func)
    param_lines = params(sig)
    if param_lines:
        param_text = "<br>".join(f"`{n}`: `{t}`" for n, t in param_lines)
    else:
        param_text = "-"
    svg_rel = write_puml_and_svg(
        f"linux_{index.replace('.', '_')}_{func}",
        f"{index} {func}",
        flow_steps(func, unit),
    )
    table = build_function_table_html(
        arch_id=unit.arch_id,
        unit_id=unit.unit_id,
        description=desc,
        prototype=sig,
        constraints=f"按 `{unit.source}` 中的入参检查、实例状态和内核资源状态执行",
        params_text=param_text,
        return_type=ret,
        def_file=unit.source,
        decl_file=unit.header,
    )
    return f"""### {index} {func}

{table}

processing flow

![{index} {func} processing flow]({svg_rel})

"""


def scenario_diagram(name: str, title: str, steps: list[str]) -> str:
    rel = write_puml_and_svg(name, title, steps)
    return f"![{title}]({rel})"


def build_linux_chapter() -> str:
    sections = [
        "# 6 Linux 部署变体详细设计",
        "",
        "## 6.1 总述",
        "",
        "本章描述 `ipcs/mpu` 中 Linux 部署变体的详细设计。UIO 与 CDEV 采用用户侧代理加内核 Backend 的形态；全内核实现不使用用户侧代理，OSAL 与 HAL 均在内核模块中运行。",
        "",
        "## 6.2 源码与构建结构",
        "",
        "| 部件 | 路径 | 产物 / 角色 |",
        "|---|---|---|",
        "| 通信核心（共享） | `ipcs/ipcs_cores/` | 用户库或内核模块共用 Core |",
        "| UIO 用户侧代理 | `ipcs/mpu/os_uio/ipc-os.c` | 用户库，满足 OSAL/HAL 契约并转发到 UIO Backend |",
        "| CDEV 用户侧代理 | `ipcs/mpu/os_cdev/ipc-os.c` | 用户库，满足 OSAL/HAL 契约并转发到 CDEV Backend |",
        "| UIO 内核 Backend | `ipcs/mpu/os_kernel/ipc-uio.c` | UIO 平台驱动与初始 cdev 通道 |",
        "| CDEV 内核 Backend | `ipcs/mpu/os_kernel/ipc-cdev.c` | 字符设备、ioctl、wait queue 与 ISR |",
        "| 全内核 OSAL | `ipcs/mpu/os_kernel/ipc-os.c` | 全内核实现的 OSAL |",
        "| Linux HAL | `ipcs/mpu/hw/c1/ipc-hw.c` | MSCM/IRQ 硬件操作 |",
        "",
        "## 6.3 全内核实现函数设计",
        "",
        "全内核实现由 `ipcs/mpu/os_kernel/ipc-os.c` 与 `ipcs/mpu/hw/c1/ipc-hw.c` 构成，无用户侧代理。",
        "",
    ]
    counter = 1
    source_cache: dict[str, str] = {}
    for unit in UNITS:
        if "UIO 用户" in unit.title:
            sections.extend(["## 6.4 UIO 实现函数设计", "", unit.role, ""])
            counter = 1
        elif "UIO 内核" in unit.title:
            sections.extend(["### 6.4.16 UIO 内核 Backend 函数", ""])
            counter = 17
        elif "CDEV 用户" in unit.title:
            sections.extend(["## 6.5 CDEV 实现函数设计", "", unit.role, ""])
            counter = 1
        elif "CDEV 内核" in unit.title:
            sections.extend(["### 6.5.11 CDEV 内核 Backend 函数", ""])
            counter = 12
        elif "Linux HAL" in unit.title:
            sections.extend(["## 6.6 Linux HAL 函数设计", "", unit.role, ""])
            counter = 1
        elif "全内核" in unit.title:
            sections.extend([f"### 6.3.0 {unit.title}", ""])
            counter = 1
        source_cache.setdefault(unit.source, _read_source(unit.source))
        for func in unit.functions:
            sig = extract_signature(source_cache[unit.source], func)
            if "全内核" in unit.title:
                idx = f"6.3.{counter}"
            elif "UIO" in unit.title:
                idx = f"6.4.{counter}"
            elif "CDEV" in unit.title:
                idx = f"6.5.{counter}"
            else:
                idx = f"6.6.{counter}"
            sections.append(function_table(unit, func, idx, sig))
            counter += 1

    sections.extend(
        [
            "## 6.7 Linux 关键场景流程",
            "",
            "### 6.7.1 UIO 初始化流程",
            "",
            scenario_diagram(
                "linux_scenario_uio_init",
                "Linux UIO initialization scenario",
                [
                    "User calls ipcsOsInit",
                    "Load ipc-shm-uio kernel module",
                    "Write IPCS_UIO_CDEV_DATA_TYPE to cdev",
                    "Kernel ipcsUioInit initializes HAL and registers UIO",
                    "User maps local/remote shared memory",
                    "User creates RX pthread",
                ],
            ),
            "",
            "### 6.7.2 CDEV 初始化流程",
            "",
            scenario_diagram(
                "linux_scenario_cdev_init",
                "Linux CDEV initialization scenario",
                [
                    "User opens /dev/ipc-shm-cdev",
                    "User sends SET_INSTANCE ioctl",
                    "User sends INIT_INSTANCE ioctl with IPCS_SHM_CFG_TYPE",
                    "Kernel ipcsCdevOsInit initializes HAL and requests IRQ",
                    "User maps shared memory and starts RX path",
                ],
            ),
            "",
            "### 6.7.3 全内核初始化流程",
            "",
            scenario_diagram(
                "linux_scenario_kernel_init",
                "Linux in-kernel initialization scenario",
                [
                    "Kernel module initializes",
                    "Core calls ipcsOsInit",
                    "OSAL maps local/remote shared memory",
                    "HAL maps MSCM and configures IRQ",
                    "OSAL requests IRQ and registers rx callback",
                    "Instance enabled",
                ],
            ),
            "",
            "### 6.7.4 UIO/CDEV 发送通知流程",
            "",
            scenario_diagram(
                "linux_scenario_tx_irq",
                "Linux user-to-kernel IRQ notify scenario",
                [
                    "User Core calls ipcsShmTx",
                    "User proxy calls ipcsHwIrqNotify",
                    "UIO write or CDEV ioctl transfers command",
                    "Kernel backend dispatches to Linux HAL",
                    "Linux HAL writes MSCM notification",
                    "Remote core receives interrupt",
                ],
            ),
            "",
            "### 6.7.5 接收唤醒流程",
            "",
            scenario_diagram(
                "linux_scenario_rx",
                "Linux receive wakeup scenario",
                [
                    "Remote notification arrives",
                    "Kernel ISR disables and clears IRQ",
                    "UIO event or CDEV wait queue wakes user",
                    "User RX thread calls rx callback / poll path",
                    "Core executes ipcsShmRx",
                    "IRQ re-enabled when work is complete",
                ],
            ),
            "",
            "## 6.8 Linux 全局变量与私有类型",
            "",
            "| 源文件 | 关键类型 / 变量 | 用途 |",
            "|---|---|---|",
            "| `ipcs/mpu/os_uio/ipc-os.c` | `struct IPCS_OS_PRIV_TYPE_TYPE ipc_os_priv` | 用户侧 fd、mmap 地址、RX 线程与回调状态 |",
            "| `ipcs/mpu/os_cdev/ipc-os.c` | `priv` / `IPCS_OS_PRIV_TYPE` | CDEV 用户侧 fd、共享内存映射和代理状态 |",
            "| `ipcs/mpu/os_kernel/ipc-os.c` | `priv` | 全内核实例状态、共享内存地址、IRQ 和 rx_cb |",
            "| `ipcs/mpu/os_kernel/ipc-uio.c` | `ipc_pdev_priv` | UIO 平台设备、cdev、UIO 实例和 IRQ 状态 |",
            "| `ipcs/mpu/os_kernel/ipc-cdev.c` | `ipc_cdev_priv` | 字符设备、wait queue、目标实例和 IRQ 状态 |",
            "| `ipcs/mpu/hw/c1/ipc-hw.c` | `ipc_hw_priv[]` | MSCM、IRQ、核索引和平台私有状态 |",
            "",
        ]
    )
    return "\n".join(sections)


def build_arch_static_diagram() -> tuple[str, str]:
    puml_name = "architecture_layered_linux_variants"
    FLOW_UMLS.mkdir(exist_ok=True)
    puml = FLOW_UMLS / f"{puml_name}.puml"
    puml.write_text(
        "\n".join(
            [
                "@startuml",
                "!pragma layout smetana",
                "skinparam linetype ortho",
                "skinparam componentStyle rectangle",
                "component SHM",
                "component OSAL",
                "component HAL",
                "component RTOS",
                "component Linux_User_Proxy",
                "component Linux_Kernel_Backend",
                "SHM --> OSAL",
                "SHM --> HAL",
                "OSAL --> RTOS",
                "OSAL --> Linux_User_Proxy",
                "Linux_User_Proxy --> Linux_Kernel_Backend",
                "Linux_Kernel_Backend --> HAL",
                "@enduml",
                "",
            ]
        ),
        encoding="utf-8",
    )
    rel = write_puml_and_svg(
        puml_name,
        "IPCS layered architecture and Linux deployment variants",
        [
            "SHM Core (ipcs_cores)",
            "Fixed OSAL/HAL contract",
            "RTOS: direct OSAL/HAL implementation",
            "Linux UIO/CDEV: user-side proxy",
            "Linux UIO/CDEV: kernel backend + Linux HAL",
            "Linux in-kernel: OSAL + HAL in kernel module",
        ],
    )
    return puml_name, rel


def insert_arch_diagram(md: str) -> str:
    _, rel = build_arch_static_diagram()
    block = (
        "### 3.1.1 分层与部署实现静态图\n\n"
        "下图描述 SHM、OSAL、HAL 三层契约，以及 RTOS、Linux UIO/CDEV、Linux 全内核三类实现位置。\n\n"
        f"![IPCS layered architecture and Linux deployment variants]({rel})\n\n"
    )
    if "### 3.1.1 分层与部署实现静态图" in md:
        md = re.sub(
            r"### 3\.1\.1 分层与部署实现静态图\n\n.*?(?=\n## 3\.2 )",
            block,
            md,
            flags=re.DOTALL,
        )
        return md
    marker = "\n## 3.2 RTOS 部署变体\n"
    return md.replace(marker, "\n" + block + marker.lstrip(), 1)


def update_toc(md: str) -> str:
    md = md.replace(
        "  - 3.3.1 UIO/CDEV 实现（用户侧代理与内核实现）\n"
        "  - 3.3.2 全内核实现\n"
        "  - 3.4 OSAL/HAL 实现位置对照",
        "  - 3.3.1 UIO 实现\n"
        "  - 3.3.2 CDEV 实现\n"
        "  - 3.3.3 全内核实现\n"
        "  - 3.4 OSAL/HAL 实现位置对照",
    )
    md = md.replace(
        "  - 6.3 全内核实现\n"
        "  - 6.4 UIO 实现\n"
        "  - 6.5 CDEV 实现\n"
        "  - 6.6 接口实现分布表\n"
        "  - 6.7 Linux 动态详细设计\n"
        "  - 6.8 Linux 全局变量与私有类型",
        "  - 6.3 全内核实现函数设计\n"
        "  - 6.4 UIO 实现函数设计\n"
        "  - 6.5 CDEV 实现函数设计\n"
        "  - 6.6 Linux HAL 函数设计\n"
        "  - 6.7 Linux 关键场景流程\n"
        "  - 6.8 Linux 全局变量与私有类型",
    )
    return md


def replace_linux_chapter(md: str) -> str:
    start = md.index("# 6 Linux 部署变体详细设计")
    end = md.index("# 7 Traceability and Consistency Evidence")
    return md[:start] + build_linux_chapter() + "\n" + md[end:]


def add_version(md: str) -> str:
    if "| V0.7 |" in md:
        return md
    row = "| V0.7 | 2026.5.19 | Cursor Agent | Draft | 完善 Linux 部署变体函数设计、关键场景 SVG 与分层静态图 |\n"
    return md.replace("| V0.6 |", row + "| V0.6 |", 1)


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    md = add_version(md)
    md = update_toc(md)
    md = insert_arch_diagram(md)
    md = replace_linux_chapter(md)
    MD.write_text(md, encoding="utf-8")
    print("task-7 Linux detailed design generated")


if __name__ == "__main__":
    main()
