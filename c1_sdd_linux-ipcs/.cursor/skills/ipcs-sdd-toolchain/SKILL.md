---
name: ipcs-sdd-toolchain
description: >-
  IPCS SDD 工具链：PlantUML 活动图/序列图/§3.2 组件图、md_sdd_0519→final_sdd.docx、
  HTML 函数表与一致性校验。修改 processing flow、重生成 SVG、同步 Word 或维护
  cursor_tmp 脚本时使用。执行任何 Python 流水线前须先读门禁与脚本总表。
---

# IPCS SDD 工具链

## 必读真源（按优先级）

0. **`cursor_tmp/mem_info.md`** — 新会话**先 Read**，首条回复写 3–5 条记忆摘要（§1.1）；收尾按情况更新  
1. `.cursorrules` — 格式死命令、修改范围、SVG/HTML 专规、§1.1 记忆、§2.1 门禁  
2. **`cursor_tmp/SDD_TOOLCHAIN.md`** — 脚本总表、管线 A–E、章节↔slug 映射、验证清单  
3. 代码真源：`linux_ch6_flows.py`、`emit_puml.py`、`ipcs/` 源码  

## 执行前门禁（未完成则禁止跑脚本）

对照 `SDD_TOOLCHAIN.md` §1：

- **G1** 任务归类到管线 A / B / C / D / E 或「一次性」  
- **G2** 在 §2 选定脚本，确认覆盖范围与任务一致  
- **G3** Init/goto/复杂分支：**禁止**默认 `regenerate_processing_flows.py` 批量覆盖；改 `linux_ch6_flows` / `emit_puml` 后 `-checkonly`  

若现有脚本不满足需求：**先**改脚本或手册映射，**再**执行。

## 管线速查

| 管线 | 何时用 | 命令要点 |
|------|--------|----------|
| **A** | 单函数/Init 活动图（推荐） | 改 `linux_ch6_flows.FLOWS` → `render_linux_ch6_flows.py` |
| **B** | 全量刷新 puml/svg | `emit_puml` → `render_linux_ch6_flows` → `render_flow_svgs` → `render_scenario_sequences` |
| **C** | 交付 Word | `md0519_to_final_sdd.py`（含 ACTIVITY 流程图小四缩放）→ `validate_md_docx_consistency.py`（须 PASS） |
| **D** | 仅序列图 §5.7/§6.9 | `scenario_sequence_flows.py` → `render_scenario_sequences.py` |
| **E** | 仅 §3.2 组件图 | `gen_section32_component_diagrams.py` |

## 禁止（高频错误）

- 批量 `regenerate_processing_flows.py` 后不校验 → 坏图（`else/endif`、goto 节点）  
- 先 regenerate 再 `emit_puml`（覆盖修复）  
- ThreadX 用 `3_4_56` 而非 **`tx_3_4_56`**  
- `render_flow_svgs` 渲染 `*_seq_*`（序列图用 `render_scenario_sequences`）  

## 闭环

改图后：`plantuml -checkonly` → 管线 C → **validate PASS**（约 166 图、138 HTML 表）。

## 交付回复格式

1. 勾选 G1–G3  
2. 列出执行的命令与改动的真源文件（puml 字典 / emit / md）  
3. validate 结果（PASS/FAIL + 失败项）  
