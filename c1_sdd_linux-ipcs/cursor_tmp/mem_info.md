# IPCS SDD 会话记忆

> **真源**：`cursor_tmp/mem_info.md`（仅此一份）。跨会话可续事实；细则见链指针，**不复述**手册全文。  
> **体量**：建议 ≤120 行，硬上限 150；过期删、合并进「稳定决策」。

## meta

| 项 | 值 |
|----|-----|
| updated | 2026-05-28 (task-12 ch3 interface rel) |
| validate | PASS — 182 svg / 138 HTML 表 / viewBox 182/182 |

## 当前焦点

- §3.1–§3.3 接口关系组件图已生成（4 SVG）；真源 `gen_ch3_interface_rel_diagrams.py`。
- SDD 工具链已文档化；新 Session 先读本文件 + `SDD_TOOLCHAIN.md` + §2.1 门禁。

## 稳定决策

- 插图仅 SVG；MD→DOCX 禁止 rasterize；闭环 `md0519_to_final_sdd` → `validate` 须 PASS。
- Init/goto 图：PlantUML 早退 `if → return → stop → endif`；禁止 `stop` 后多余 `else (no)`；禁止节点写 `goto`。
- ThreadX 流程图 slug 为 **`tx_3_4_*`**，不是 `3_4_56`。
- 文档「§6.7」= CDEV KO；「第 7 章」= SWE.3 双向追溯矩阵（26 条，五列，无 §7.3 排除表）。
- 脚本顺序：全量时 `emit_puml` → `render_linux_ch6_flows` → `render_flow_svgs`；勿先 regenerate 再 emit。

## 指针

| 主题 | 路径 |
|------|------|
| 规则 / 门禁 G1–G5 | `.cursorrules` §2.1 |
| 脚本与管线 A–E | `cursor_tmp/SDD_TOOLCHAIN.md` |
| Skill | `.cursor/skills/ipcs-sdd-toolchain/SKILL.md` |
| Linux 第 6 章活动图真源 | `cursor_tmp/format_docx_py/linux_ch6_flows.py` |
| 执行前检查 | `python cursor_tmp/scripts/sdd_preflight.py --md-svg` |

## 上轮增量

- task-12：§3.1 增「接口符号」列；§3.2/§3.3 插入 4 张 IF_AppSvc/IF_OSAbst/IF_HWAbst 组件关系 SVG；`final_sdd.docx`/`final.pdf` 已同步。

## 禁踩坑

- `regenerate_processing_flows` 批量覆盖 hand-written 图 → PlantUML 语法/else 乱序。
- `linux_ch6_flows` 勿被未校验的自动同步写坏（曾 git 恢复过 `linux_6_3_9`）。
- 上下文 >150K 时建议新 Session，依赖本文件而非长对话历史。
