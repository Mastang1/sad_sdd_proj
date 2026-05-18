| ROLES / 角色 | Name / 姓名 | Department / 部门 | Date / 日期 |
|---|---|---|---|
| AUTHOR(S) / 作者： | 孔繁鑫 | 软件研发部 | 2026.1.13 |
| REVIEWER(S) / 审查： | 安然/赵笃/喻明睿/张帅/伊焕利/肖敏元/孔繁鑫/宋晓婷/栗瑞江/Wenke | 软件研发部 | 2026.1.13 |
| APPROVER (S) / 批准： | 安然 | 软件研发部 | 2026.1.13 |

## Document history: 文档历史

| Version / 版本 | Date / 日期 | Editor / 编辑人 | Status / 文档状态 | Change description / 变更简述 |
|---|---|---|---|---|
| V0.1 | 2025.11.20 | 孔 | Draft | Initial version for review初版待评审 |

## CONTENTS 目录

- 1 INTRODUCTION简介
  - 1.1 Confidentiality 保密性
  - 1.2 Purpose of the document文档目的
  - 1.3 Scope范围
  - 1.4 References 参考文件
  - 1.5 Abbreviations缩略语
- 2 Software Architecture软件架构
- 3 Software DETAIL Design软件详细设计
  - 3.1 Definition定义
  - 3.2 Files
    - 3.2.1 文件列表
    - 3.2.2 Lin.c
    - 3.2.3 Lin_Hal.c
    - 3.2.4 Linflexd_Lin_HwDrv.c
    - 3.2.5 Lin_ASRExt.c
    - 3.2.6 Linflexd_Lin_HwDrv_Autosar.c
    - 3.2.7 Linflexd_Lin_HwDrv_Irq.c
    - 3.2.8 Lin.h
    - 3.2.9 Lin_Hal.h
    - 3.2.10 Linflexd_Lin_HwDrv.h
    - 3.2.11 Lin_ASRExt.h
    - 3.2.12 Linflexd_Lin_HwDrv_Autosar.h
    - 3.2.13 Linflexd_Lin_HwDrv_TrustedFunctions.h
    - 3.2.14 Lin_Types.h
    - 3.2.15 Lin_Hal_Types.h
    - 3.2.16 Linflexd_Lin_HwDrv_Types.h
  - 3.3 External Interfaces外部接口
    - 3.3.1 Lin_Init
    - 3.3.2 Lin_CheckWakeup
    - 3.3.3 Lin_GetStatus
    - 3.3.4 Lin_SendFrame
    - 3.3.5 Lin_GoToSleep
    - 3.3.6 Lin_GoToSleepInternal
    - 3.3.7 Lin_Wakeup
    - 3.3.8 Lin_WakeupInternal
    - 3.3.9 Lin_GetVersionInfo
    - 3.3.10 Linflexd_Lin_HwDrv_Init
    - 3.3.11 Linflexd_Lin_HwDrv_Deinit
    - 3.3.12 Linflexd_Lin_HwDrv_SendFrame
    - 3.3.13 Linflexd_Lin_HwDrv_AbortTransferData
    - 3.3.14 Linflexd_Lin_HwDrv_GetCurrentNodeState
    - 3.3.15 Linflexd_Lin_HwDrv_GetStatus
    - 3.3.16 Linflexd_Lin_HwDrv_GoToSleepMode
    - 3.3.17 Linflexd_Lin_HwDrv_GotoIdleState
    - 3.3.18 Linflexd_Lin_HwDrv_SendWakeupSignal
    - 3.3.19 Linflexd_Lin_HwDrv_TxRx_IRQHandler
    - 3.3.20 Linflexd_Lin_HwDrv_Error_IRQHandler
  - 3.4 Internal Functions 内部函数
    - 3.4.1 Lin_InitImplementation
    - 3.4.2 Lin_CommonCheckingChannel
    - 3.4.3 Lin_ChkParamFuncSendFrame
    - 3.4.4 Lin_Hal_CheckWakeup
    - 3.4.5 Lin_Hal_InitChannel
    - 3.4.6 Lin_Hal_SendFrame
    - 3.4.7 Lin_Hal_GoToSleep
    - 3.4.8 Lin_Hal_HardwareGetStatus
    - 3.4.9 Lin_Hal_GoToSleepInternal
    - 3.4.10 Lin_Hal_WakeUp
    - 3.4.11 Lin_Hal_WakeUpInternal
    - 3.4.12 Lin_Hal_Callback
    - 3.4.13 Lin_Hal_ErrorCallback
    - 3.4.14 Linflexd_Lin_HwDrv_StartTimeout
    - 3.4.15 Linflexd_Lin_HwDrv_TimeoutExpired
    - 3.4.16 Linflexd_Lin_HwDrv_StateTimeoutMode
    - 3.4.17 Linflexd_Lin_HwDrv_SetUpRegisterInInitMode
    - 3.4.18 Linflexd_Lin_HwDrv_SetUpRegisterInNormalMode
    - 3.4.19 Linflexd_Lin_HwDrv_GetTimeoutErrorStatus
    - 3.4.20 Linflexd_Lin_HwDrv_GetNoEventStatus
    - 3.4.21 Linflexd_Lin_HwDrv_ReceiveErrorsHandler
    - 3.4.22 Linflexd_Lin_HwDrv_ErrorsHandler
    - 3.4.23 Linflexd_Lin_HwDrv_CompleteTransfer
    - 3.4.24 Linflexd_Lin_HwDrv_CopyData
    - 3.4.25 Linflexd_Lin_HwDrv_CheckWakeup
  - 3.5 Gobal variants 全局变量
  - 3.6 Data Structure 类型定义
    - 3.6.1 struct Lin_ChannelConfigType
    - 3.6.2 struct Lin_ConfigType
    - 3.6.3 struct Lin_HwConfigType
    - 3.6.4 struct Linflexd_Lin_HwDrv_PduType
    - 3.6.5 struct Linflexd_Lin_HwDrv_StateStructType
    - 3.6.6 struct Linflexd_Lin_HwDrv_UserConfigType
    - 3.6.7 enum Lin_Hal_NodeType
    - 3.6.8 enum Linflexd_Lin_HwDrv_EventIdType
    - 3.6.9 enum Linflexd_Lin_HwDrv_NodeStateType
    - 3.6.10 enum Linflexd_Lin_HwDrv_TransferStatusType
    - 3.6.11 enum Linflexd_Lin_HwDrv_StatusType
    - 3.6.12 enum Linflexd_Lin_HwDrv_FrameCsModelType
    - 3.6.13 enum Linflexd_Lin_HwDrv_FrameResponseType

# 1 INTRODUCTION简介

## 1.1 Confidentiality 保密性

任何披露必须与负责的流程经理协调。

本文件过程说明仅限直接参与项目的人员查看。转让给其他方，尤其是Star Gather以外的合作伙伴，必须由项目负责人协调，并受开发合同中有关保密规定的约束。

## 1.2 Purpose of the document文档目的

目的是按照MCAL LIN Driver软件架构设计、设计准则、所分配的支持软件单元实施和验证的软件需求，开发MCAL LIN Driver软件详细设计。

## 1.3 Scope范围

此文档对MCAL LIN Driver软件有效。

## 1.4 References 参考文件

| Reference ID / 编号 | Document Name / 文档名称 | Version / 版本 | Date / 日期 | Author / 作者 | Status / 状态 |
|---|---|---|---|---|---|
| 1 | Automotive SPICE® Process Assessment Model | 2.5 | 2010-05-10 | VDA | Release |
| 2 | MCAL软件需求规范 | 1.0 | 2025-08-10 | 喻明睿 | 已发布 |
| 3 | C1 MCAL软件架构设计规范 | 1.0 | 2025-09-12 | 赵笃 | 已发布 |
| 4 | MCAL_LIN_DRV软件架构规范 | 1.0 | 2025-09-26 | 赵笃 | 已发布 |
| 5 | C1软件单元设计规范 | 1.0 | 2025-07-01 | 薛艳江 | 已发布 |
| 6 |  |  |  |  |  |
| 7 |  |  |  |  |  |
| 8 |  |  |  |  |  |
| 9 |  |  |  |  |  |
| 10 |  |  |  |  |  |

## 1.5 Abbreviations缩略语

| Abbreviation / 缩写 | Meaning/Explanation / 解释 |
|---|---|
| SW | Software |
| HW | Hardware |
| MCAL | Microcontroller Abstraction Layer |
| MCU | Micro Controller Unit |
| SWS | Software Specification |
| Hal | Hardware Abstraction Layer |
| HwDrv | Hardware Driver |
| LIN | Local Interconnect Network |
| PDU | Protocol Data Unit |
| SDU | Service Data Unit |
| PID | Protected Identifier |
| DL | Data length |
| ISR | Interrupt Service Routine |

# 2 Software Architecture软件架构

MCAL LIN Driver软件总体架构如下图所示：

![](reference.media/media/image2.emf)

其中Lin Interface和LINFLEXD为外部模块

- Lin Interface Layer: 向上层Lin User/ Lin Interface提供统一的独立于底层硬件的接口。

- Lin HAL Layer: 在Lin Interface Layer和Lin Flexd HW Driver Layer之间。屏蔽底层硬件差异，完成接口层函数的具体实现。

- LinFlexd HW Driver Layer：实现对底层LINFLEXD硬件设备的控制，包括初始化，数据收发等功能。

- LinFlexd ISR：负责LINFLEXD硬件设备的中断处理，并通过调用Lin HAL Layer/Lin Interface Layer回调函数通知上层软件。

# 3 Software DETAIL Design软件详细设计

## 3.1 Definition定义

MCAL LIN Driver模块属于通信驱动，对C1芯片上的LinFlexd硬件设备进行配置和控制。

## 3.2 Files

### 3.2.1 文件列表

| 组件 | 文件 |
|---|---|
| Lin Interface Layer | Lin.c |
| Lin Interface Layer | Lin_ASRExt.c |
| Lin Interface Layer | Lin.h |
| Lin Interface Layer | Lin_ASRExt.h |
| Lin Interface Layer | Lin_Types.h |
| Lin HAL Layer | Lin_Hal.c |
| Lin HAL Layer | Lin_Hal.h |
| Lin HAL Layer | Lin_Hal_Types.h |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv.c |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv_Autosar.c |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv.h |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv_Autosar.h |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv_TrustedFunctions.h |
| Lin HW Driver Layer | Linflexd_Lin_HwDrv_Types.h |
| LinFlexd ISR | Linflexd_Lin_HwDrv_Irq.c |

### 3.2.2 Lin.c

**描述：**

> 源文件，包括Lin接口层函数实现

**依赖关系：**

![](reference.media/media/image3.emf)

### 3.2.3 Lin_Hal.c

**描述：**

> 源文件，包括Lin硬件抽象层函数实现

**依赖关系：**

![](reference.media/media/image4.emf)

### 3.2.4 Linflexd_Lin_HwDrv.c

**描述：**

> 源文件，包括Lin硬件驱动层函数实现

**依赖关系：**

![](reference.media/media/image5.emf)

### 3.2.5 Lin_ASRExt.c

**描述：**

> 源文件，包括Lin接口层切换时钟模式函数实现

**依赖关系：**

![](reference.media/media/image6.emf)

### 3.2.6 Linflexd_Lin_HwDrv_Autosar.c

**描述：**

> 源文件，包括Lin硬件驱动层检查唤醒函数实现

**依赖关系：**

![](reference.media/media/image7.emf)

### 3.2.7 Linflexd_Lin_HwDrv_Irq.c

**描述：**

> 源文件，包括Lin硬件驱动层中断服务函数实现

**依赖关系：**

![](reference.media/media/image8.emf)

## 3.3 External Interfaces外部接口

### 3.3.1 Lin_Init

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数初始化LIN模块</td></tr>
<tr><td>函数原型</td><td colspan="4">void Lin_Init(const Lin_ConfigType * Config)</td></tr>
<tr><td>制约条件</td><td colspan="4">\-</td></tr>
<tr><td rowspan="2">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>I</td><td>Config</td><td>Lin_ConfigType *</td><td>指向LIN驱动配置的指针</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="4">\-</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">Lin.h</td></tr>
<tr><td>满足需求</td><td colspan="4">SWS_Lin_00006, SWS_Lin_00008, SWS_Lin_00084, SWS_Lin_00099, SWS_Lin_00105, SWS_Lin_00146, SWS_Lin_00150, SWS_Lin_00171, SWS_Lin_00190, GR_MCD_00031, GR_MCD_00046</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image9.emf)

### 3.3.2 Lin_CheckWakeup

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数用于上层核对LIN通道是否被唤醒</td></tr>
<tr><td>函数原型</td><td colspan="4">Std_ReturnType Lin_CheckWakeup(uint8 Channel)</td></tr>
<tr><td>制约条件</td><td colspan="4">LIN已经初始化</td></tr>
<tr><td rowspan="2">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>I</td><td>Channel</td><td>uint8</td><td>LIN通道Id</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="2">Std_ReturnType</td><td colspan="2">E_NOT_OK：LIN通道无效、驱动未初始化、不处于休眠状态<br><br>E_OK：通道被唤醒</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">Lin.h</td></tr>
<tr><td>满足需求</td><td colspan="4">SWS_Lin_00107, SWS_Lin_00251, SWS_Lin_00098, SWS_Lin_00160</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image10.emf)

### 3.3.3 Lin_GetStatus

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数获取LIN驱动状态</td></tr>
<tr><td>函数原型</td><td colspan="4"><code>Lin_StatusType Lin_GetStatus(uint8 Channel, uint8 ** Lin_SduPtr)</code></td></tr>
<tr><td>制约条件</td><td colspan="4">LIN已经初始化</td></tr>
<tr><td rowspan="3">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>I</td><td>Channel</td><td>uint8</td><td>LIN通道Id</td></tr>
<tr><td>I</td><td>Lin_SduPtr</td><td><code>uint8 **</code></td><td>指向接收SDU影子缓冲区的指针</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="2">Lin_StatusType</td><td colspan="2">LIN_NOT_OK：开发错误<br><br>LIN_TX_OK：发送成功<br><br>LIN_TX_BUSY：正在发送报文头或响应<br><br>LIN_TX_HEADER_ERROR：发送头错误<br><br>LIN_TX_ERROR：发送响应错误<br><br>LIN_RX_OK：接收成功<br><br>LIN_RX_BUSY：正在接收<br><br>LIN_RX_ERROR：接收错误<br><br>LIN_RX_NO_REPONSE：没有收到数据<br><br>LIN_OPERATIONAL：等待数据，准备发送下一报文头</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">Lin.h</td></tr>
<tr><td>满足需求</td><td colspan="4">SWS_Lin_00022, SWS_Lin_00024, SWS_Lin_00091, SWS_Lin_00092, SWS_Lin_00141, SWS_Lin_00143, SWS_Lin_00144, SWS_Lin_00168, SWS_Lin_00211, SWS_Lin_00233, SWS_Lin_00238, SWS_Lin_00255, SWS_Lin_00264, SWS_Lin_00289</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image11.emf)

### 3.3.4 Lin_SendFrame

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数发送一帧LIN报文</td></tr>
<tr><td>函数原型</td><td colspan="4">Std_ReturnType Lin_SendFrame(uint8 Channel, const Lin_PduType * PduInfoPtr)</td></tr>
<tr><td>制约条件</td><td colspan="4">LIN已经初始化</td></tr>
<tr><td rowspan="3">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>I</td><td>Channel</td><td>uint8</td><td>LIN通道Id</td></tr>
<tr><td>I</td><td>PduInfoPtr</td><td>Lin_PduType *</td><td>指向LIN报文PDU的指针，包括PID, Checksum, DL, SDU等</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="2">Std_ReturnType</td><td colspan="2">E_NOT_OK：LIN通道无效、驱动未初始化、处于休眠状态、PduInfoPtr为空、发送超时<br><br>E_OK：发送成功</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">Lin.h</td></tr>
<tr><td>满足需求</td><td colspan="4">SWS_Lin_00016, SWS_Lin_00017, SWS_Lin_00021, SWS_Lin_00025, SWS_Lin_00092, SWS_Lin_00191, SWS_Lin_00192, SWS_Lin_00195, SWS_Lin_00197, SWS_Lin_00198, SWS_Lin_00199, SWS_Lin_00287, GR_MCD_00031, GR_MCD_00033</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image12.emf)

## 3.4 Internal Functions 内部函数

### 3.4.1 Lin_InitImplementation

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数初始化LIN通道配置</td></tr>
<tr><td>函数原型</td><td colspan="4">static void Lin_InitImplementation(void)</td></tr>
<tr><td>制约条件</td><td colspan="4">\-</td></tr>
<tr><td rowspan="2">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>\-</td><td>\-</td><td>\-</td><td>\-</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="4">\-</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">\-</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image13.emf)

### 3.4.2 Lin_CommonCheckingChannel

<table border="1" cellspacing="0" cellpadding="4">
<tbody>
<tr><td>对应软件架构ID</td><td colspan="4">MCAL_LIN_DRV</td></tr>
<tr><td>函数说明</td><td colspan="4">该函数核对LIN通道的有效性</td></tr>
<tr><td>函数原型</td><td colspan="4">static Std_ReturnType Lin_CommonCheckingChannel(const uint8 Channel, const uint8 FunctionalId)</td></tr>
<tr><td>制约条件</td><td colspan="4">\-</td></tr>
<tr><td rowspan="3">输入/输出参数</td><td>I/O</td><td>参数名</td><td>数据类型</td><td>说明</td></tr>
<tr><td>I</td><td>Channel</td><td>uint8</td><td>LIN通道Id</td></tr>
<tr><td>I</td><td>FunctionalId</td><td>uint8</td><td>函数Id</td></tr>
<tr><td rowspan="2">返回值</td><td colspan="2">数据类型</td><td colspan="2">说明</td></tr>
<tr><td colspan="2">Std_ReturnType</td><td colspan="2">E_NOT_OK：通道无效<br><br>E_OK：通道有效</td></tr>
<tr><td>函数定义文件</td><td colspan="4">Lin.c</td></tr>
<tr><td>函数声明文件</td><td colspan="4">\-</td></tr>
</tbody>
</table>

**处理流程**

![](reference.media/media/image14.emf)

## 3.5 Gobal variants 全局变量

| 全局变量名称 | 全局变量类型 | 全局变量范围 | 全局变量描述 | 全局变量的存储RAM区 |
|---|---|---|---|---|
| Lin_apConfigPtr | Lin_ConfigType \* | Lin.c | 指向LIN全局配置的指针 | .mcal_bss |
| Lin_apChannelConfigPtr | Lin_ChannelConfigType \* | Lin.c | 指向LIN通道配置的指针 | .mcal_bss |
| Lin_au8LinDrvStatus | uint8 | Lin.c | 存储LIN驱动状态 | .mcal_data |
| Lin_au8LinChStatus | uint8 | Lin.c | 存储LIN通道状态 | .mcal_bss |
| Lin_Hal_au8HwMapping | uint8 | Lin_Hal.c | 存储逻辑通道与硬件实例映射关系 | .mcal_bss |
| Lin_Hal_apChannelsConfig | Lin_HwConfigType \* | Lin_Hal.c | 指向LIN硬件通道配置的指针 | .mcal_bss |
| Lin_Hal_au8TransmitHeaderCommand | uint8 | Lin_Hal.c | 存储LIN报文头命令类型 | .mcal_bss |
| Linflexd_Lin_HwDrv_apxBases | LINFLEXD_Type \* | Linflexd_Lin_HwDrv.c | 存储LIN实例及地址 | .mcal_const |
| Linflexd_Lin_HwDrv_au8SduBuffer | uint8 | Linflexd_Lin_HwDrv.c | 存储LIN实例接收数据的数组 | .mcal_bss |
| Linflexd_Lin_HwDrv_anPduInfo | Linflexd_Lin_HwDrv_PduType | Linflexd_Lin_HwDrv.c | 存储LIN slave协议数据单元 | .mcal_bss |
| Linflexd_Lin_HwDrv_axStateStructure | Linflexd_Lin_HwDrv_StateStructType | Linflexd_Lin_HwDrv.c | 存储LIN驱动运行状态 | .mcal_bss |
| Linflexd_Lin_HwDrv_apUserConfigs | Linflexd_Lin_HwDrv_UserConfigType \* | Linflexd_Lin_HwDrv.c | 指向LIN slave用户配置的指针 | .mcal_bss |
| Linflexd_Lin_HwDrv_apxStateStructureArray | Linflexd_Lin_HwDrv_StateStructType \* | Linflexd_Lin_HwDrv.c | 指向LIN驱动运行状态的指针 | .mcal_bss |

## 3.6 Data Structure 类型定义

### 3.6.1 struct Lin_ChannelConfigType

| Type | Name | Description |
|---|---|---|
| Uint8 | LinChannelID | Lin Channel ID |
| Lin_HwConfigType \* | ChannelConfigPtr | LIN Hardware configuration pointer |
| uint32 | ChannelCoreId | LIN Channel core id |
| boolean | AllocatedPartition | LIN Channel is allocated partition or not |

### 3.6.2 struct Lin_ConfigType

| Type | Name | Description |
|---|---|---|
| uint32 | PartitionCoreId | Partition core id is assigned for this configuration |
| Lin_ChannelConfigType \* | Lin_ChannelPtr | Constant pointer to an array containing the configurations for the available LIN channels |

满足需求：SWS_Lin_00013, SWS_Lin_00227

### 3.6.11 enum Linflexd_Lin_HwDrv_StatusType

| Name | Description |
|---|---|
| LINFLEXD_LIN_HWDRV_STATUS_SUCCESS | Successful operation |
| LINFLEXD_LIN_HWDRV_STATUS_ERROR | Failed operation |
| LINFLEXD_LIN_HWDRV_STATUS_BUSY | LIN hardware instance is in busy |
| LINFLEXD_LIN_HWDRV_STATUS_TIMEOUT | Timeout error |

满足需求：LINFLEXD_LIN_HWDRV_00033

### 3.6.12 enum Linflexd_Lin_HwDrv_FrameCsModelType

| Name | Description |
|---|---|
| LINFLEXD_LIN_HWDRV_ENHANCED_CS | Enhanced checksum model |
| LINFLEXD_LIN_HWDRV_CLASSIC_CS | Classic checksum model |

### 3.6.13 enum Linflexd_Lin_HwDrv_FrameResponseType

| Name | Description |
|---|---|
| LINFLEXD_LIN_HWDRV_FRAMERESPONSE_TX | Response is generated from this (master) node |
| LINFLEXD_LIN_HWDRV_FRAMERESPONSE_RX | Response is generated from a remote slave node |
| LINFLEXD_LIN_HWDRV_FRAMERESPONSE_IGNORE | Response is generated from one slave to another slave.<br><br>For the master the response will be anonymous, it does not have to receive the response |
