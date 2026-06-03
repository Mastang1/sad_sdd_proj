# IPCS Driver SDD 评审演讲稿提纲

> 现场：`fuck.docx` · 分发：`final.pdf` · SWE.3 Draft V1.1 · 主讲：倘亚朋

---

## 0. 开场

### 问候与材料
- 今天评审 IPCS Driver 软件详细设计（SWE.3）
- 现场用 Word 演示；会后请阅 `final.pdf`

### 一句话定位
- 架构组件 → **13 个 SWU** → RTOS 三 OS + Linux 三种部署 → **§7 双向追溯至源码**

### 本轮评审边界
- **审**：单元划分、三层契约、接口/动态设计、追溯闭合
- **不审**：代码 bug 走查、性能数据、AUTOSAR 安全证据全文

### 文档体量
- 13 SWU · 138 张活动图 · 函数五列表 · 26 条需求追溯

---

## 1. §1 简介（3 min）

### 文档目的
- 满足 SWE.3：静态结构 + 接口 + 类型 + 动态行为

### 设计范围
- Core/Queue 全变体共享
- RTOS：FreeRTOS / ThreadX / AUTOSAR + MCU HAL
- Linux：UIO / CDEV / 全内核

### 上游输入
- 软件需求、架构 PDF（待评审）、ASPICE SWE.3

---

## 2. §2 软件单元划分（10 min）

### 划分原则
- **一个 `.c` = 一个 SWU**；`.h` 是契约，不单列

### 三组单元
- **Core**：SHM / QUEUE / UTIL
- **RTOS**：三 OSAL + HAL_MCU
- **Linux**：OS_UIO、OS_CDEV、OS_KERN、UIO_KO、CDEV_KO、HAL_LINUX

### 组件映射结论
- 架构组件 → SWU 一一可追踪
- Linux Adapt 拆成用户代理 + KO + HAL，是 **Refinement**，不是遗漏

### 核心句
- 「§2 是全文的地图，后面每一章都在这张地图上填细节。」

---

## 3. §3 分层与部署变体（20 min）★ 重点

### 三层契约（§3.1）
- **SHM**：应用面 — `ipcsShmInit` / `ipcsShmTx` / `ipcsShmPollChannels`
- **OSAL**：映射与调度 — `ipcsOsGetLocalShm` / `ipcsOsPollChannels`
- **HAL**：硬件中断 — `ipcsHwIrqNotify` / `ipcsHwIrqEnable`
- Core 只认契约，不感知具体 OS 或 Linux 形态

### 展示图 1：Core 三层（if_impl_cores）
- SHM 向下只依赖 OSAL/HAL 接口，不跨层

### RTOS 部署（§3.2）
- 展示图 2：同地址空间，Core 直调 OSAL/HAL
- 三 OS 共用 HAL_MCU，差异仅在 OSAL 实现

### Linux 三种形态（§3.3）
- **UIO**：用户 OS_UIO 代理 → UIO_KO → HAL
- **CDEV**：用户 OS_CDEV 代理 → CDEV_KO → HAL
- **全内核**：无用户代理，OS_KERN 在内核完成 OSAL

### 设计亮点
- Core **零修改** 跨所有变体复用
- UIO 用户侧 `ipcsHwInit/Free` 为空：初始化权在 KO（§3.3.1 设计规定）
- Linux 用户库 **导出同名 `ipcsOs*`/`ipcsHw*`**，是契约代理，不是第二套 API

### 核心句
- 「变体差异全部收敛在 OSAL/HAL，Core 是稳定内核。」

---

## 4. §4 公共软件单元（15 min）

### 章节结构
- 文件结构 → 外部接口 → 内部函数 → 类型 → 动态设计

### 外部 API 故事线（选 3 个）
- `ipcsShmInit`：实例 + 通道 + 池 + 下层初始化
- `ipcsShmTx`：managed 发送主路径
- `ipcsShmPollChannels`：IRQ 与轮询统一收包（IPCS_039）

### 函数设计表模式
- 五列表：原型 / 描述 / 参数 / 返回值 / SWU ID + 活动图
- 质疑任一行：**需求 → 组件 → SWU → 函数 → 图 → 源码**，五跳定位

### 内部设计要点（§4.4）
- 队列 `ipcsQueue*` 与通道 `getChannel*` 解耦
- `ipcsShmRx` 收包路径 HAL 不感知队列

### 讲解原则
- 讲 **模式**，不逐函数念表；代表函数看一张 flow 即可

---

## 5. §5 RTOS 部署变体（12 min）

### 结构说明
- §5.1/5.2 与 §4 镜像，降低阅读成本

### OSAL 三实现（§5.3–5.5）
- 接口集相同；差异在任务、中断、同步原语映射

### HAL_MCU（§5.6）
- 核间中断、cache、平台核索引

### 动态设计（§5.9）
- 展示 **1 条序列图**：Init → Tx → Rx 通知
- RTOS 无用户态切换，IRQ 直达任务/软中断模型

### 核心句
- 「三个 OS 是换引擎，底盘 Core 不变。」

---

## 6. §6 Linux 部署变体（15 min）

### 章节导航
- §6.3 OS_KERN · §6.4 OS_UIO · §6.5 UIO_KO
- §6.6 OS_CDEV · §6.7 CDEV_KO · §6.8 HAL_LINUX
- §6.9 动态序列图
- **提醒**：§6.7 是 CDEV KO，不是第 7 章追溯

### UIO vs CDEV
- UIO：`ipcsSendUioCmd` 写 fd 转发 HW 命令
- CDEV：ioctl 控制 + mmap 共享内存

### 动态设计（§6.9）
- 展示 **1 条序列图**：用户态 Tx → KO → HAL 发 IRQ → 对端 Rx
- 强调同名符号跨地址空间仍满足 §3.1 契约

### 核心句
- 「Linux 难点在用户/内核切分，SDD 用 Refinement 把它写清楚了。」

---

## 7. §7 双向追溯（10 min）★ 收尾

### 追溯策略（§7.1）
- SWE.1 需求 → SWE.2 架构组件 → SWE.3 单元 → `ipcs/` 代码

### 矩阵演示（§7.2）
- 打开 26 行五列表
- 现场读 **一行完整链路**（建议 IPCS_018 零拷贝 或 IPCS_036 变体裁剪）
- 需求 ID → 组件 → SWU → 代码路径 → 设计覆盖说明

### 结论句
- **26 条分配需求均有架构组件 + SWU + 代码实体**，满足 SWE.3.BP4

---

## 8. 总结陈词（2 min）

### 三条 takeaway
1. **13 SWU、三层契约**，Core 跨变体复用
2. **RTOS 与 Linux** 差异收敛在 OSAL/HAL，Linux 有 Refinement
3. **§7 追溯闭合**，需求可追到源码

### 建议结论
- 架构 PDF 基线确认前提下，**建议通过 SWE.3 详细设计评审**
- 条件项：架构基线发布后核对组件 ID；AUTOSAR 安全证据另案；项目选定 Linux 变体后配置裁剪

---

## 9. Q&A

### 预备答点（按需）
- SDD 与架构 PDF：Refinement 关系，非偏离
- 13 SWU 划分：按 `.c`，Conf 在类型头文件
- 活动图与代码：真源 `ipcs/` + 工具链校验
- UIO 用户 HAL 空实现：设计规定，KO 负责 Init/Free
- 追溯 26 行：覆盖分配需求子集，已剔过程类伪追溯

### 收尾
- 记录 action item，会后更新文档与 PDF
- 感谢评委

---

## 附：节奏备忘

| 段 | 时长 | 切忌 |
|---|:---:|---|
| 0 开场 | 5 min | 冗长背景 |
| §1 | 3 min | 念参考文件表 |
| §2 | 10 min | 跳过映射表 |
| §3 | 20 min | 不讲 Linux 三种形态对比 |
| §4–§6 | 42 min | 逐函数念参数 |
| §7 | 10 min | 不演示矩阵一行 |
| Q&A | 15–30 min | 现场大改版式 |

**总时长**：约 90–120 min
