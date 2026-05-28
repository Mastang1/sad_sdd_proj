# -*- coding: utf-8 -*-
"""Generate §3.2 / §3.3 interface–SWU component relationship diagrams (4 SVGs).

Fixed-coordinate SVG layout: top-to-bottom dependency, orthogonal edges,
no crossing, no lines through components.  Interface = circle lollipop;
SWU = pale-khaki component with <<Implement>> stereotype.
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
from workspace_paths import FILES_32_SVGS

BG = "#FFFCF5"
COMP_FILL = "#F5E6CC"
COMP_BORDER = "#8B7355"
PKG_FILL = "#FAF0E0"
PKG_BORDER = "#A08060"
IF_FILL = "#F1F1F1"
IF_BORDER = "#181818"
EDGE = "#5C4033"


class Diagram:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._parts: list[str] = []
        self._boxes: list[tuple[float, float, float, float]] = []

    def _register_box(self, x: float, y: float, w: float, h: float) -> None:
        self._boxes.append((x, y, x + w, y + h))

    def package(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self._register_box(x, y, w, h)
        tab = min(110.0, w * 0.35)
        self._parts.append(
            f'<path d="M{x},{y} L{x + tab},{y} L{x + tab + 8},{y + 18} '
            f'L{x + w},{y + 18} L{x + w},{y + h} L{x},{y + h} Z" '
            f'fill="{PKG_FILL}" stroke="{PKG_BORDER}" stroke-width="1.5"/>'
        )
        self._parts.append(
            f'<line x1="{x}" y1="{y + 18}" x2="{x + tab + 8}" y2="{y + 18}" '
            f'stroke="{PKG_BORDER}" stroke-width="1.5"/>'
        )
        self._parts.append(
            f'<text x="{x + 6}" y="{y + 14}" font-family="sans-serif" '
            f'font-size="13" font-weight="bold" fill="#000">{html.escape(label)}</text>'
        )

    def component(self, x: float, y: float, w: float, h: float, swu_id: str) -> tuple[float, float, float, float]:
        self._register_box(x, y, w, h)
        self._parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" ry="3" '
            f'fill="{COMP_FILL}" stroke="{COMP_BORDER}" stroke-width="0.8"/>'
        )
        self._parts.append(
            f'<rect x="{x + w - 18}" y="{y + 5}" width="12" height="8" '
            f'fill="{COMP_FILL}" stroke="{COMP_BORDER}" stroke-width="0.6"/>'
        )
        self._parts.append(
            f'<text x="{x + w / 2}" y="{y + 22}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="10" font-style="italic" fill="#000">'
            f"&lt;&lt;Implement&gt;&gt;</text>"
        )
        self._parts.append(
            f'<text x="{x + w / 2}" y="{y + 38}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="10" fill="#000">{html.escape(swu_id)}</text>'
        )
        return (x, y, w, h)

    def app_box(self, cx: float, y: float) -> tuple[float, float, float, float]:
        w, h = 64.0, 36.0
        x = cx - w / 2
        self._register_box(x, y, w, h)
        self._parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" ry="3" '
            f'fill="{COMP_FILL}" stroke="{COMP_BORDER}" stroke-width="0.8"/>'
        )
        self._parts.append(
            f'<text x="{cx}" y="{y + 22}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="11" fill="#000">APP</text>'
        )
        return (x, y, w, h)

    def interface(self, cx: float, cy: float, label: str) -> tuple[float, float]:
        self._register_box(cx - 10, cy - 10, 20, 20)
        self._parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="7" fill="{IF_FILL}" '
            f'stroke="{IF_BORDER}" stroke-width="0.8"/>'
        )
        self._parts.append(
            f'<text x="{cx}" y="{cy + 24}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="12" fill="#000">{html.escape(label)}</text>'
        )
        return (cx, cy)

    @staticmethod
    def _box_anchor(box: tuple[float, float, float, float], side: str) -> tuple[float, float]:
        x, y, w, h = box
        if side == "top":
            return (x + w / 2, y)
        if side == "bottom":
            return (x + w / 2, y + h)
        if side == "left":
            return (x, y + h / 2)
        if side == "right":
            return (x + w, y + h / 2)
        raise ValueError(side)

    @staticmethod
    def _if_anchor(cx: float, cy: float, side: str) -> tuple[float, float]:
        if side == "top":
            return (cx, cy - 7)
        if side == "bottom":
            return (cx, cy + 7)
        if side == "left":
            return (cx - 7, cy)
        if side == "right":
            return (cx + 7, cy)
        raise ValueError(side)

    def edge(
        self,
        points: list[tuple[float, float]],
        *,
        arrow: str = "last",
    ) -> None:
        if len(points) < 2:
            return
        d = f"M{points[0][0]},{points[0][1]}"
        for px, py in points[1:]:
            d += f" L{px},{py}"
        self._parts.append(
            f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.1" '
            f'marker-end="url(#arrow)"/>'
        )

    def v_edge(self, x1: float, y1: float, x2: float, y2: float, lane_x: float | None = None) -> None:
        if abs(x1 - x2) < 0.5:
            self.edge([(x1, y1), (x2, y2)])
            return
        lx = lane_x if lane_x is not None else x1
        self.edge([(x1, y1), (lx, y1), (lx, y2), (x2, y2)])

    def save(self, path: Path) -> None:
        svg = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}">\n'
            f'<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
            f'refX="7" refY="4" orient="auto" markerUnits="strokeWidth">'
            f'<polygon points="0,0 8,4 0,8" fill="{EDGE}"/></marker></defs>\n'
            f'<rect width="100%" height="100%" fill="{BG}"/>\n'
            + "\n".join(self._parts)
            + "\n</svg>\n"
        )
        path.write_text(svg, encoding="utf-8")


def _center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, w, h = box
    return (x + w / 2, y + h / 2)


def gen_rtos(path: Path) -> None:
    d = Diagram(520, 640)
    cx = 260.0

    app = d.app_box(cx, 12)
    if_app_x, if_app_y = d.interface(cx, 72, "IF_AppSvc")
    core_shm = d.component(170, 130, 180, 48, "SWU_IPCS_CORE_SHM")
    core_q = d.component(170, 210, 180, 48, "SWU_IPCS_CORE_QUEUE")
    if_os_x, if_os_y = d.interface(150, 310, "IF_OSAbst")
    if_hw_x, if_hw_y = d.interface(390, 310, "IF_HWAbst")
    os_ar = d.component(20, 400, 150, 48, "SWU_IPCS_OSAL_AUTOSAR")
    os_fr = d.component(185, 400, 150, 48, "SWU_IPCS_OSAL_FREERTOS")
    os_tx = d.component(350, 400, 150, 48, "SWU_IPCS_OSAL_THREADX")
    hal = d.component(310, 520, 160, 48, "SWU_IPCS_HAL_MCU")

    d.v_edge(*d._box_anchor(app, "bottom"), if_app_x, if_app_y - 7)
    d.v_edge(*d._box_anchor(core_shm, "top"), if_app_x - 20, if_app_y + 7, lane_x=240)
    d.v_edge(*d._box_anchor(core_q, "top"), *_center(core_shm), lane_x=150)
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_os_x, if_os_y - 7, lane_x=120)
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_hw_x, if_hw_y - 7, lane_x=450)
    d.v_edge(*d._box_anchor(os_ar, "top"), if_os_x, if_os_y + 7, lane_x=95)
    d.v_edge(*d._box_anchor(os_fr, "top"), if_os_x, if_os_y + 7, lane_x=260)
    d.v_edge(*d._box_anchor(os_tx, "top"), if_os_x, if_os_y + 7, lane_x=425)
    d.v_edge(*d._box_anchor(hal, "top"), if_hw_x, if_hw_y + 7)
    d.v_edge(*d._box_anchor(os_fr, "bottom"), if_hw_x, if_hw_y + 7, lane_x=470)

    d.save(path)


def gen_uio(path: Path) -> None:
    d = Diagram(520, 720)
    cx = 260.0

    app = d.app_box(cx, 12)
    if_app_x, if_app_y = d.interface(cx, 72, "IF_AppSvc")
    d.package(20, 118, 480, 360, "User Space")
    if_os_x, if_os_y = d.interface(150, 200, "IF_OSAbst")
    if_hw_x, if_hw_y = d.interface(390, 200, "IF_HWAbst")
    core_shm = d.component(170, 250, 180, 48, "SWU_IPCS_CORE_SHM")
    core_q = d.component(170, 320, 180, 48, "SWU_IPCS_CORE_QUEUE")
    os_uio = d.component(175, 400, 170, 48, "SWU_IPCS_LINUX_OS_UIO")

    d.package(120, 500, 280, 190, "Kernel Space")
    uio_ko = d.component(150, 540, 170, 48, "SWU_IPCS_LINUX_UIO_KO")
    hal = d.component(150, 620, 170, 48, "SWU_IPCS_HAL_LINUX")

    d.v_edge(*d._box_anchor(app, "bottom"), if_app_x, if_app_y - 7)
    d.v_edge(*d._box_anchor(core_shm, "top"), if_app_x, if_app_y + 7, lane_x=210)
    d.v_edge(*d._box_anchor(core_q, "top"), *_center(core_shm))
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_os_x, if_os_y - 7, lane_x=120)
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_hw_x, if_hw_y - 7, lane_x=450)
    d.v_edge(*d._box_anchor(os_uio, "top"), if_os_x, if_os_y + 7, lane_x=110)
    d.v_edge(*d._box_anchor(os_uio, "top"), if_hw_x, if_hw_y + 7, lane_x=430)
    d.v_edge(*d._box_anchor(os_uio, "bottom"), *_center(uio_ko))
    d.v_edge(*d._box_anchor(uio_ko, "bottom"), *_center(hal))

    d.save(path)


def gen_cdev(path: Path) -> None:
    d = Diagram(520, 720)
    cx = 260.0

    app = d.app_box(cx, 12)
    if_app_x, if_app_y = d.interface(cx, 72, "IF_AppSvc")
    d.package(20, 118, 480, 360, "User Space")
    if_os_x, if_os_y = d.interface(150, 200, "IF_OSAbst")
    if_hw_x, if_hw_y = d.interface(390, 200, "IF_HWAbst")
    core_shm = d.component(170, 250, 180, 48, "SWU_IPCS_CORE_SHM")
    core_q = d.component(170, 320, 180, 48, "SWU_IPCS_CORE_QUEUE")
    os_cdev = d.component(170, 400, 180, 48, "SWU_IPCS_LINUX_OS_CDEV")

    d.package(120, 500, 280, 190, "Kernel Space")
    cdev_ko = d.component(150, 540, 180, 48, "SWU_IPCS_LINUX_CDEV_KO")
    hal = d.component(150, 620, 180, 48, "SWU_IPCS_HAL_LINUX")

    d.v_edge(*d._box_anchor(app, "bottom"), if_app_x, if_app_y - 7)
    d.v_edge(*d._box_anchor(core_shm, "top"), if_app_x, if_app_y + 7, lane_x=210)
    d.v_edge(*d._box_anchor(core_q, "top"), *_center(core_shm))
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_os_x, if_os_y - 7, lane_x=120)
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_hw_x, if_hw_y - 7, lane_x=450)
    d.v_edge(*d._box_anchor(os_cdev, "top"), if_os_x, if_os_y + 7, lane_x=110)
    d.v_edge(*d._box_anchor(os_cdev, "top"), if_hw_x, if_hw_y + 7, lane_x=430)
    d.v_edge(*d._box_anchor(os_cdev, "bottom"), *_center(cdev_ko))
    d.v_edge(*d._box_anchor(cdev_ko, "bottom"), *_center(hal))

    d.save(path)


def gen_kern(path: Path) -> None:
    d = Diagram(520, 680)
    cx = 260.0

    app = d.app_box(cx, 12)
    if_app_x, if_app_y = d.interface(cx, 72, "IF_AppSvc")
    d.package(20, 118, 480, 540, "Kernel Space")
    if_os_x, if_os_y = d.interface(150, 200, "IF_OSAbst")
    if_hw_x, if_hw_y = d.interface(390, 200, "IF_HWAbst")
    core_shm = d.component(170, 250, 180, 48, "SWU_IPCS_CORE_SHM")
    core_q = d.component(170, 320, 180, 48, "SWU_IPCS_CORE_QUEUE")
    os_kern = d.component(115, 400, 190, 48, "SWU_IPCS_LINUX_OS_KERN")
    hal = d.component(310, 520, 170, 48, "SWU_IPCS_HAL_LINUX")

    d.v_edge(*d._box_anchor(app, "bottom"), if_app_x, if_app_y - 7)
    d.v_edge(*d._box_anchor(core_shm, "top"), if_app_x, if_app_y + 7, lane_x=210)
    d.v_edge(*d._box_anchor(core_q, "top"), *_center(core_shm))
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_os_x, if_os_y - 7, lane_x=120)
    d.v_edge(*d._box_anchor(core_shm, "bottom"), if_hw_x, if_hw_y - 7, lane_x=450)
    d.v_edge(*d._box_anchor(os_kern, "top"), if_os_x, if_os_y + 7, lane_x=100)
    d.v_edge(*d._box_anchor(hal, "top"), if_hw_x, if_hw_y + 7)
    d.v_edge(*d._box_anchor(os_kern, "left"), if_hw_x, if_hw_y + 7, lane_x=70)

    d.save(path)


def main() -> None:
    FILES_32_SVGS.mkdir(parents=True, exist_ok=True)
    outputs = {
        "3_2_rtos_if_rel": gen_rtos,
        "3_3_1_uio_if_rel": gen_uio,
        "3_3_2_cdev_if_rel": gen_cdev,
        "3_3_3_kern_if_rel": gen_kern,
    }
    for slug, fn in outputs.items():
        fn(FILES_32_SVGS / f"{slug}.svg")
    print(f"wrote {len(outputs)} component diagrams -> {FILES_32_SVGS}/")


if __name__ == "__main__":
    main()
