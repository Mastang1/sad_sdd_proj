# -*- coding: utf-8 -*-
r"""
仅执行任务 3 与任务 6（TF / final_sdd.docx）
==========================================

依照工作区 ``prompt-format.md``，在**不改任务 1、2、4、5** 的前提下，只对 TF 做：

- **任务 3**：正文样式段落 — 微软雅黑、**11 pt**、不粗体；无首行缩进；单倍行距；段前段后 0 磅。
  不修改标题、目录（Compact）、题注等。保存前做**标题完整性检测**（确保标题文本未被改写）。
- **任务 6**：主文档流中**含插图或图表**的段落（``python-docx`` 的 ``document.paragraphs``，
  **不含**表格单元格内段落）：**无缩进**、**居中对齐**（相对页面版式，而非单元格内对齐）。

**依赖**::

    pip install python-docx

**使用方式**（在仓库根目录 ``c1_sdd`` 下执行，默认 TF 为同目录 ``final_sdd.docx``）::

    python format_docx_py/format_tf_tasks_3_6.py
    python format_docx_py/format_tf_tasks_3_6.py "C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx"

脚本**直接覆盖保存**目标文件；若 Word 正在打开该文件，请先关闭再运行。

实现复用同目录下 ``format_final_sdd.py`` 中的函数，便于与全套任务脚本保持同一套规则。

版本：与 TF / prompt-format 配套。
"""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document

from format_final_sdd import (
    DEFAULT_TF,
    assert_heading_integrity,
    format_body_paragraphs,
    format_figure_chart_paragraphs_layout,
    snapshot_heading_state,
)


def _tf_path() -> Path:
    """
    解析命令行中的 TF 路径；未给出时使用工作区约定默认路径。

    :return: 绝对路径
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return DEFAULT_TF.resolve()


def main() -> None:
    """打开 TF，执行任务 3、6，校验标题后保存。"""
    tf = _tf_path()
    if not tf.is_file():
        print(f"未找到 TF：{tf}", file=sys.stderr)
        sys.exit(1)

    doc = Document(str(tf))
    headings_ref = snapshot_heading_state(doc)

    n_body = format_body_paragraphs(doc)
    n_layout = format_figure_chart_paragraphs_layout(doc)

    headings_after = snapshot_heading_state(doc)
    assert_heading_integrity(headings_ref, headings_after)

    doc.save(str(tf))
    print(
        "处理完成并已保存：",
        tf,
        f"\n  任务3 正文段落: {n_body}",
        f"\n  任务6 插图/图表段落（居中、无缩进）: {n_layout}",
        "\n  标题完整性: 通过",
    )


if __name__ == "__main__":
    main()
