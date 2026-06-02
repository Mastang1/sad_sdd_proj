# IPCS SDD 工具链手册（`cursor_tmp/SDD_TOOLCHAIN.md`）

> **用途**：新 Agent Session、维护人员执行 Python 流水线前的**唯一脚本索引**。  
> **优先级**：`.cursorrules`（死命令）> 本手册 > 脚本默认行为。  
> **跨会话记忆**：新 Session 先读 `cursor_tmp/mem_info.md`（§1.1），再读本手册。  
> **路径**：所有命令均在**工作区根目录**执行；脚本内 `import workspace_paths`，禁止硬编码路径。

---

## 0. 交付物与目录

| 路径 | 说明 |
|------|------|
| `md_sdd_0519.md` | SDD Markdown 真源 |
| `final_sdd.docx` | Word 交付物 |
| `ipcs/` | C 源码真源（流程图须据此） |
| `cursor_tmp/flow_umls/*.puml` | PlantUML 中间件 |
| `cursor_tmp/flow_svgs/*.svg` | MD/DOCX 引用的插图 |
| `cursor_tmp/files_32_umls/`、`files_32_svgs/` | §3.2 组件图 |
| `plantuml.jar` | 工作区根目录 |

---

## 1. 执行前三步门禁（强制，AI 与人工均遵守）

在运行**任意** `cursor_tmp/**/*.py` 前，必须完成下表并**书面确认**（可在回复中列表勾选）：

| 步 | 动作 | 未通过则 |
|----|------|----------|
| **G1 任务归类** | 将用户任务映射到 §3 的一条管线（A/B/C/D/E）或标明「一次性维护」 | 禁止跑全量脚本 |
| **G2 脚本选型** | 在 §2 总表中选定脚本；确认**不会**覆盖未授权文件（如 hand-written `linux_ch6_flows.py`） | 禁止执行 |
| **G3 需求差异** | 若任务涉及 Init/goto/多分支：禁止默认 `regenerate_processing_flows.py` 批量生成；须改 `linux_ch6_flows.py` / `emit_puml.py` / `ipc_flow_remainder.py` | 须先改真源再渲染 |

**辅助命令（不替代 G1–G4 判断）**：

```bash
python cursor_tmp/scripts/sdd_preflight.py
python cursor_tmp/scripts/sdd_preflight.py --md-svg
```

**改脚本本身**：若 G2 表明现有脚本**不满足**任务（缺 slug、错误覆盖、缺 ThreadX `tx_*` 等），须**先**修改 Python 真源或手册 §4 映射，再执行；不得带着已知错误参数强行跑流水线。

---

## 2. 脚本总表

| 脚本 | 功能 | 适用任务 | 输入 → 输出 | 前置 | 覆盖风险 | 复用 |
|------|------|----------|-------------|------|----------|------|
| `workspace_paths.py` | 路径常量 | 被其他脚本 import | — | — | — | 是 |
| `scripts/emit_puml.py` | 写出 §3.3/3.4、§4、§5 等 `flow_umls/*.puml` | 管线 B；公共 API/内部函数活动图 | 源码逻辑 → `flow_umls/` | — | **覆盖**同名 slug | 是 |
| `scripts/ipc_flow_remainder.py` | `emit_puml` 注册的剩余图（含 **`tx_3_4_*`** ThreadX） | 与 emit 联用 | 嵌入 emit | emit | 覆盖 | 是 |
| `format_docx_py/linux_ch6_flows.py` | Linux 第 6 章活动图**正文真源**（FLOWS 字典） | **管线 A**（推荐）单函数/Init | 手写 PlantUML 体 | — | 仅 render 时写 `.puml` | 是 |
| `format_docx_py/render_linux_ch6_flows.py` | `FLOWS` → `flow_umls/linux_*` → SVG | 改 Linux 6.x 流程图后必跑 | `linux_ch6_flows` → `flow_svgs/` | java/plantuml | 覆盖 `linux_*` puml/svg | 是 |
| `scripts/render_flow_svgs.py` | 渲染**活动图**（排除 `*_seq_*`） | 管线 B；emit 或 hand puml 之后 | `flow_umls/*.puml` → `flow_svgs/` | plantuml.jar | 批量覆盖 svg | 是 |
| `format_docx_py/scenario_sequence_flows.py` | 生成 §5.7/§6.9 序列图 puml | 跨单元场景序列图 | Python 常量 → `*_seq_*.puml` | — | 覆盖 seq puml | 是 |
| `format_docx_py/render_scenario_sequences.py` | 仅渲染序列图 SVG | 序列图变更后 | `*_seq_*.puml` → svg | plantuml | 覆盖 seq svg | 是 |
| `scripts/gen_section32_component_diagrams.py` | §3.2 组件图 | 头文件依赖图 | → `files_32_*` | — | 覆盖 §3.2 图 | 是 |
| `format_refer/format_refer.docx` | Word 版式/页眉页脚模板 | 管线 C 套用 | — | 勿删 | — |
| `format_docx_py/apply_format_refer.py` | 中间态正文合并进模板 + HF 校验 | 被 md0519 调用 | body docx + 模板 → docx | 模板存在 | 覆盖 docx HF | 是 |
| `format_docx_py/md0519_to_final_sdd.py` | MD→DOCX 主入口 | **管线 C** 交付 | `md_sdd_0519.md` → `final_sdd.docx` | MD+SVG+模板 | 覆盖 docx | 是 |
| `format_docx_py/format_final_sdd.py` | TF 版式、插图比例、删占位 | 被 md0519 调用 | docx | — | 改版式 | 是 |
| `format_docx_py/scale_flow_diagram_typography.py` | ACTIVITY 流程图按 viewBox+字号设宽（Word 内约五号） | **管线 C 末步**（md0519 自动调用）；可单独补跑 | docx | format 后 | 改 ACTIVITY extent | 是 |
| `format_docx_py/svg_typography_scale.py` | 流程图目标宽度计算（被 scale 脚本 import） | — | — | — | — | 是 |
| `format_docx_py/html_table_utils.py` | HTML 函数表剥离/后插入 | 被 md0519 调用 | md html → docx 表 | — | 改表 | 是 |
| `format_docx_py/validate_md_docx_consistency.py` | MD/DOCX 一致性 + viewBox | **管线 C 必跑** | md+docx → report | docx 已生成 | 只读 | 是 |
| `scripts/regenerate_processing_flows.py` | C→活动图启发式批量 | **慎用**；仅实验或全量重刷且接受质检 | `ipcs/`+md → puml | — | **破坏** hand-written 图 | 是 |
| `format_docx_py/c_to_activity.py` | 被 regenerate 调用 | 不单独跑 | C 函数体 | — | — | 是 |
| `scripts/convert_ch6_function_tables.py` | 第 6 章 pipe→HTML 表 | 一次性结构迁移 | md | — | 改 md 表 | 一次性 |
| `scripts/restructure_ch56_headings.py` | 第 5/6 章标题重组 | 一次性 | md | — | 改结构 | 一次性 |
| `scripts/fix_md_h3_blank_lines.py` | `###` 前空行 | Pandoc H3 | md | — | 改 md | 按需 |
| `scripts/docx_to_md.py` | DOCX→MD | 反向同步（慎用） | docx → md | — | 覆盖 md | 按需 |
| `scripts/sdd_preflight.py` | 打印 G1–G5 提醒；检查 plantuml / MD svg | **执行前** | — | 只读 | 是 |

---

## 3. 标准管线

### 管线 A — 单函数活动图（**推荐**，尤其 Init / goto）

```text
1. 读 ipcs/ 对应 .c 函数体
2. 改 linux_ch6_flows.FLOWS["<slug>"] 或 emit_puml/ipc_flow_remainder 中 W("<slug>", ...)
3. java -jar plantuml.jar -checkonly cursor_tmp/flow_umls/<slug>.puml  （或 render_linux_ch6_flows 只写该 slug）
4. python cursor_tmp/format_docx_py/render_linux_ch6_flows.py
5. 确认 md_sdd_0519.md 仍引用 cursor_tmp/flow_svgs/<slug>.svg（路径一般不变）
6. 若需 Word：管线 C
```

**PlantUML 书写约束**（Init 常见错误）：

- 早退：`if (cond?) then (yes)` → `:return err;` → `stop` → `endif`（**不要**在 `stop` 后再写 `else (no)`）
- 禁止活动节点写 `goto xxx;`；改为「失败路径 + 清理动作」或 `note right: cleanup at err_*`
- `&` 在标签中写作 `\&`

### 管线 B — 插图全量刷新（维护日）

```bash
python cursor_tmp/scripts/emit_puml.py
python cursor_tmp/format_docx_py/render_linux_ch6_flows.py
python cursor_tmp/scripts/render_flow_svgs.py
python cursor_tmp/format_docx_py/render_scenario_sequences.py
# 可选 §3.2：
python cursor_tmp/scripts/gen_section32_component_diagrams.py
```

**顺序不可乱**：`emit_puml` 会覆盖 `3_*`/`tx_*` 等；**之后**再 `render_linux_ch6_flows` 覆盖 `linux_*`。

### 管线 C — MD → DOCX 闭环（交付必跑）

```bash
python cursor_tmp/format_docx_py/md0519_to_final_sdd.py
python cursor_tmp/format_docx_py/validate_md_docx_consistency.py
```

**期望**：`RESULT: PASS`；约 **183** 插图、**138** HTML 函数表、viewBox 宽高比一致；ACTIVITY 流程图经 typography 缩放（报告 `cursor_tmp/flow_typography_scale_report.txt`）。

**仅补跑流程图字号缩放**（已有 docx、跳过 MD 转换）::

```bash
python cursor_tmp/format_docx_py/scale_flow_diagram_typography.py
```

### 管线 D — 仅序列图

```bash
# 改 format_docx_py/scenario_sequence_flows.py 后：
python cursor_tmp/format_docx_py/render_scenario_sequences.py
# 若交付 Word：管线 C
```

### 管线 E — 仅 §3.2 组件图

```bash
python cursor_tmp/scripts/gen_section32_component_diagrams.py
# 若交付 Word：管线 C
```

---

## 4. 章节 ↔ slug ↔ 源码（易错映射）

| MD 章节 | SWU / 说明 | slug 前缀 | 定义文件示例 |
|---------|------------|-----------|--------------|
| §6.3 | 全内核 OS | `linux_6_3_*` | `ipcs/mpu/os_kernel/ipc-os.c` |
| §6.4 | UIO 用户代理 | `linux_6_4_*` | `ipcs/mpu/os_uio/ipc-os.c` |
| §6.5 | UIO KO | `linux_6_4_17`…（标题可能写 6.5.x） | `ipcs/mpu/os_kernel/ipc-uio.c` |
| §6.6 | CDEV 用户 | `linux_6_5_1`… | `ipcs/mpu/os_cdev/ipc-os.c` |
| §6.7 | CDEV KO | `linux_6_5_18` `ipcsCdevOsInit` 等 | `ipcs/mpu/os_kernel/ipc-cdev.c` |
| §6.8 | Linux HAL | `linux_6_6_*` | `ipcs/mpu/hw/c1/ipc-hw.c` |
| §4.4 ThreadX | **必须** `tx_3_4_*` | **非** `3_4_56` | `ipcs/mcu/os/threadx/ipc-os-threadx.c` |
| §5.7 / §6.9 | 场景序列图 | `rtos_seq_*` / `linux_seq_*` | `scenario_sequence_flows.py` |

**注意**：文档「第 7 章」= SWE.3 追溯（**无** processing flow）；Linux Init 多在 **§6.3–6.8**。

---

## 5. 限制与反模式

| 禁止 | 原因 |
|------|------|
| 批量 `regenerate_processing_flows.py` 后不做 `-checkonly` / 不跑 validate | 易产生 `else/endif` 乱序、PlantUML 语法错误 |
| 先 regenerate 再 `emit_puml` | emit 覆盖 hand-written 修复 |
| `rasterize_svg_refs_for_docx` | 违反 §5；Windows 路径问题 |
| 用活动图代替 §5.7/§6.9 序列图 | 违反 §5.1 |
| 修改未在任务中指定的 MD 章节/插图 | 违反 §3 |

---

## 6. 闭环验证清单

### L1 — 单图语法（改图后）

```bash
java -jar plantuml.jar -checkonly cursor_tmp/flow_umls/<slug>.puml
```

### L2 — MD 引用存在

```bash
# 期望：missing count = 0
python -c "import re, pathlib; md=pathlib.Path('md_sdd_0519.md').read_text(encoding='utf-8'); svgs=set(re.findall(r'flow_svgs/([^)]+\\.svg)', md)); missing=[s for s in svgs if not (pathlib.Path('cursor_tmp/flow_svgs')/s).exists()]; print(len(svgs), 'missing', len(missing))"
```

### L3 — 交付一致（必跑）

```bash
python cursor_tmp/format_docx_py/validate_md_docx_consistency.py
```

报告：`cursor_tmp/validate_md_docx_report.txt`。须 **PASS**（无 ERROR）。

### L4 — Init 图人工抽检（可选）

- 图中无孤立文字 `else (no)`、`endif` 当步骤
- 与 `ipcs/` 中函数主路径一致（尤其 `ipcsOsInit` 打开模块/mmap/ioctl 顺序）

---

## 7. 新 Session 首条消息模板

```markdown
请先阅读 `.cursorrules` §2.1 与 `cursor_tmp/SDD_TOOLCHAIN.md`，完成 G1–G3 门禁后再执行脚本。

任务：<具体章节/函数/slug>
管线：<A|B|C>
禁止：regenerate 批量覆盖（除非明确授权）、rasterize SVG、改动范围外章节。

完成后：列出已执行命令；`validate_md_docx_consistency.py` 须 PASS。
```

---

## 8. 维护

- 增删脚本 → 更新 §2 与 §3。
- 变更基准数字（166/138）→ 同步 §6 与 `.cursorrules` §6.4。
- Project Skill：`.cursor/skills/ipcs-sdd-toolchain/SKILL.md`（摘要 + 链到本文件）。

**基线记录（2026-05-20）**：validate PASS；166 图；138 HTML 函数表。
