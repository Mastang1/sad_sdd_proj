# -*- coding: utf-8 -*-
r"""
仅执行任务 7（TF / final_sdd.docx）
==================================

依照 ``prompt-format.md`` **任务 7**，在**不执行**任务 1～6 的前提下，仅对 TF 做：

**3.2 Files 节**

- 删除 **3.2.1～3.2.18** 中**每个插图段落之后紧邻一行**、且形如 ``3.2.x …``（如
  ``3.2.2 ipc-queue.c 头文件依赖（组件 UML）``）的**单行说明段落**。
- 仅删除上述说明段；插图与其它正文、标题一律不动。

**3.3 / 3.4 节**

- 删除每个插图下、内容含 ``processing flow`` 且行首为 ``3.3.*`` / ``3.4.*`` 的说明行
  （例如 ``3.3.1 processing flow``）。
- 在**每张插图段落之前**插入单独一段，文本为 ``processing flow``，段落格式与任务 3 正文一致：
  微软雅黑、11 pt、不粗体，无首行缩进，单倍行距，段前段后 0 磅。

**依赖**::

    pip install python-docx

**使用方式**（仓库根目录 ``c1_sdd``）::

    python format_docx_py/format_tf_task_7.py
    python format_docx_py/format_tf_task_7.py "C:\\tangyapeng\\docs\\StarGather\\c1_sdd\\final_sdd.docx"

脚本**直接覆盖保存** TF；若 Word 正打开该文件，请先关闭。

实现位于同目录 ``format_final_sdd.py`` 中的 ``apply_task7_caption_and_processing_flow``。

版本：与 TF / prompt-format 配套。
"""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document

from format_final_sdd import (
    DEFAULT_TF,
    apply_task7_caption_and_processing_flow,
)


def _tf_path() -> Path:
    """
    解析命令行中的 TF 路径；缺省为工作区 ``final_sdd.docx``。

    :return: 绝对路径
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return DEFAULT_TF.resolve()


def main() -> None:
    """打开 TF，执行任务 7 并保存。"""
    tf = _tf_path()
    if not tf.is_file():
        print(f"未找到 TF：{tf}", file=sys.stderr)
        sys.exit(1)

    doc = Document(str(tf))
    stats = apply_task7_caption_and_processing_flow(doc)
    doc.save(str(tf))
    print(
        "处理完成并已保存：",
        tf,
        f"\n  任务7a 已删 3.2 图下编号说明行: {stats['n_delete_32']} 段",
        f"\n  任务7b 3.3/3.4 已插入图前 processing flow 并删原说明: {stats['n_move_processing_flow']} 处",
    )


if __name__ == "__main__":
    main()
