# -*- coding: utf-8 -*-
"""Normalize md_sdd_0519.md headings from chapter 3 onward (English + 中文)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"

# Exact line replacements (order: longer keys first where nested)
REPLACEMENTS: list[tuple[str, str]] = [
    # TOC (CONTENTS) — chapters 3–7 only
    ("- 3 分层架构与部署变体设计", "- 3 LAYERED ARCHITECTURE AND DEPLOYMENT VARIANTS 分层架构与部署变体设计"),
    ("  - 3.1 三层架构与接口契约", "  - 3.1 SHM / OSAL / HAL Interface Contract 三层接口契约"),
    ("  - 3.2 RTOS 部署变体", "  - 3.2 RTOS Deployment Variant RTOS 部署变体"),
    ("  - 3.3 Linux 部署变体", "  - 3.3 Linux Deployment Variants Linux 部署变体"),
    ("  - 3.3.1 UIO 实现", "  - 3.3.1 UIO Implementation UIO 实现"),
    ("  - 3.3.2 CDEV 实现", "  - 3.3.2 CDEV Implementation CDEV 实现"),
    ("  - 3.3.3 全内核实现", "  - 3.3.3 In-Kernel Implementation 全内核实现"),
    ("  - 3.4 OSAL/HAL 实现位置对照", "  - 3.4 OSAL/HAL Implementation Mapping OSAL/HAL 实现对照"),
    ("- 4 公共详细设计（跨部署变体共享）", "- 4 COMMON DETAILED DESIGN 公共详细设计"),
    ("  - 4.1 Definition定义", "  - 4.1 Definition 定义"),
    ("  - 4.2 Files", "  - 4.2 Files 文件"),
    ("  - 4.3 External Interfaces外部接口", "  - 4.3 External Interfaces 外部接口"),
    ("  - 4.4 Internal Functions 内部函数", "  - 4.4 Internal Functions 内部函数"),
    ("  - 4.5 Global variants 全局变量", "  - 4.5 Global Variables 全局变量"),
    ("  - 4.6 Data Structure 类型定义", "  - 4.6 Data Types 类型定义"),
    ("  - 4.7 Dynamic Detailed Design 动态详细设计", "  - 4.7 Dynamic Detailed Design 动态详细设计"),
    ("- 5 RTOS 部署变体详细设计", "- 5 RTOS DEPLOYMENT VARIANT DETAILED DESIGN RTOS 部署变体详细设计"),
    ("  - 5.1 Definition定义", "  - 5.1 Definition 定义"),
    ("  - 5.2 Files", "  - 5.2 Files 文件"),
    ("  - 5.3 SWU_IPCS_OSAL_AUTOSAR 软件单元设计", "  - 5.3 SWU_IPCS_OSAL_AUTOSAR Software Unit Design 软件单元设计"),
    ("  - 5.4 SWU_IPCS_OSAL_FREERTOS 软件单元设计", "  - 5.4 SWU_IPCS_OSAL_FREERTOS Software Unit Design 软件单元设计"),
    ("  - 5.5 SWU_IPCS_OSAL_THREADX 软件单元设计", "  - 5.5 SWU_IPCS_OSAL_THREADX Software Unit Design 软件单元设计"),
    ("  - 5.6 SWU_IPCS_HAL_MCU 软件单元设计", "  - 5.6 SWU_IPCS_HAL_MCU Software Unit Design 软件单元设计"),
    ("  - 5.7 Global variants 全局变量", "  - 5.7 Global Variables 全局变量"),
    ("  - 5.8 Data Structure 类型定义", "  - 5.8 Data Types 类型定义"),
    ("  - 5.9 RTOS 动态详细设计", "  - 5.9 RTOS Dynamic Detailed Design RTOS 动态详细设计"),
    ("- 6 Linux 部署变体详细设计", "- 6 LINUX DEPLOYMENT VARIANT DETAILED DESIGN Linux 部署变体详细设计"),
    ("  - 6.1 Definition定义", "  - 6.1 Definition 定义"),
    ("  - 6.2 Files", "  - 6.2 Files 文件"),
    ("  - 6.3 SWU_IPCS_LINUX_OS_KERN 软件单元设计", "  - 6.3 SWU_IPCS_LINUX_OS_KERN Software Unit Design 软件单元设计"),
    ("  - 6.4 SWU_IPCS_LINUX_OS_UIO 软件单元设计", "  - 6.4 SWU_IPCS_LINUX_OS_UIO Software Unit Design 软件单元设计"),
    ("  - 6.5 SWU_IPCS_LINUX_UIO_KO 软件单元设计", "  - 6.5 SWU_IPCS_LINUX_UIO_KO Software Unit Design 软件单元设计"),
    ("  - 6.6 SWU_IPCS_LINUX_OS_CDEV 软件单元设计", "  - 6.6 SWU_IPCS_LINUX_OS_CDEV Software Unit Design 软件单元设计"),
    ("  - 6.7 SWU_IPCS_LINUX_CDEV_KO 软件单元设计", "  - 6.7 SWU_IPCS_LINUX_CDEV_KO Software Unit Design 软件单元设计"),
    ("  - 6.8 Linux HAL 函数设计", "  - 6.8 SWU_IPCS_HAL_LINUX Software Unit Design 软件单元设计"),
    ("  - 6.9 Linux 关键场景流程", "  - 6.9 Linux Key Scenario Flows Linux 关键场景流程"),
    ("  - 6.10 Global variants 全局变量", "  - 6.10 Global Variables 全局变量"),
    ("  - 6.11 Data Structure 类型定义", "  - 6.11 Data Types 类型定义"),
    ("- 7 双向追溯与一致性 (Bidirectional Traceability and Consistency)", "- 7 BIDIRECTIONAL TRACEABILITY AND CONSISTENCY 双向追溯与一致性"),
    # Chapter 3
    ("# 3 分层架构与部署变体设计", "# 3 LAYERED ARCHITECTURE AND DEPLOYMENT VARIANTS 分层架构与部署变体设计"),
    ("## 3.1 SHM / OSAL / HAL 三层接口契约", "## 3.1 SHM / OSAL / HAL Interface Contract 三层接口契约"),
    ("## 3.2 RTOS 部署变体", "## 3.2 RTOS Deployment Variant RTOS 部署变体"),
    ("## 3.3 Linux 部署变体", "## 3.3 Linux Deployment Variants Linux 部署变体"),
    ("### 3.3.1.1 User–Kernel 适配接口（IF_LinuxAdapt_UIO）", "### 3.3.1.1 User-Kernel Adaptation Interface (IF_LinuxAdapt_UIO) User-Kernel 适配接口"),
    ("### 3.3.1 UIO 实现", "### 3.3.1 UIO Implementation UIO 实现"),
    ("### 3.3.2.1 User–Kernel 适配接口（IF_LinuxAdapt_CDEV）", "### 3.3.2.1 User-Kernel Adaptation Interface (IF_LinuxAdapt_CDEV) User-Kernel 适配接口"),
    ("### 3.3.2 CDEV 实现", "### 3.3.2 CDEV Implementation CDEV 实现"),
    ("### 3.3.3 全内核实现", "### 3.3.3 In-Kernel Implementation 全内核实现"),
    ("## 3.4 OSAL/HAL 实现位置对照", "## 3.4 OSAL/HAL Implementation Mapping OSAL/HAL 实现对照"),
    # Chapter 4
    ("# 4 公共详细设计（跨部署变体共享）", "# 4 COMMON DETAILED DESIGN 公共详细设计"),
    ("## 4.1 Definition定义", "## 4.1 Definition 定义"),
    ("## 4.2 Files", "## 4.2 Files 文件"),
    ("### 4.2.1 文件列表", "### 4.2.1 File List 文件列表"),
    ("## 4.3 External Interfaces外部接口", "## 4.3 External Interfaces 外部接口"),
    ("## 4.5 Global variants 全局变量", "## 4.5 Global Variables 全局变量"),
    ("## 4.6 Data Structure 类型定义", "## 4.6 Data Types 类型定义"),
    ("### 4.7.1 初始化流程（CORE-S01）", "### 4.7.1 Initialization Sequence (CORE-S01) 初始化流程"),
    ("### 4.7.2 Managed 发送流程（CORE-S02）", "### 4.7.2 Managed Transmit Sequence (CORE-S02) Managed 发送流程"),
    ("### 4.7.3 Managed 接收与释放流程（CORE-S03）", "### 4.7.3 Managed Receive and Release Sequence (CORE-S03) Managed 接收与释放流程"),
    ("### 4.7.4 Unmanaged 发送与接收流程（CORE-S04）", "### 4.7.4 Unmanaged Sequence (CORE-S04) Unmanaged 收发流程"),
    ("### 4.7.5 中断与轮询流程（CORE-S05）", "### 4.7.5 Interrupt and Polling Sequence (CORE-S05) 中断与轮询流程"),
    # Chapter 5
    ("# 5 RTOS 部署变体详细设计", "# 5 RTOS DEPLOYMENT VARIANT DETAILED DESIGN RTOS 部署变体详细设计"),
    ("## 5.1 Definition定义", "## 5.1 Definition 定义"),
    ("## 5.2 Files", "## 5.2 Files 文件"),
    ("### 5.2.1 文件列表", "### 5.2.1 File List 文件列表"),
    ("## 5.3 SWU_IPCS_OSAL_AUTOSAR 软件单元设计", "## 5.3 SWU_IPCS_OSAL_AUTOSAR Software Unit Design 软件单元设计"),
    ("## 5.4 SWU_IPCS_OSAL_FREERTOS 软件单元设计", "## 5.4 SWU_IPCS_OSAL_FREERTOS Software Unit Design 软件单元设计"),
    ("## 5.5 SWU_IPCS_OSAL_THREADX 软件单元设计", "## 5.5 SWU_IPCS_OSAL_THREADX Software Unit Design 软件单元设计"),
    ("## 5.6 SWU_IPCS_HAL_MCU 软件单元设计", "## 5.6 SWU_IPCS_HAL_MCU Software Unit Design 软件单元设计"),
    ("## 5.7 Global variants 全局变量", "## 5.7 Global Variables 全局变量"),
    ("## 5.8 Data Structure 类型定义", "## 5.8 Data Types 类型定义"),
    ("## 5.9 RTOS 动态详细设计", "## 5.9 RTOS Dynamic Detailed Design RTOS 动态详细设计"),
    # Chapter 6
    ("# 6 Linux 部署变体详细设计", "# 6 LINUX DEPLOYMENT VARIANT DETAILED DESIGN Linux 部署变体详细设计"),
    ("## 6.1 Definition定义", "## 6.1 Definition 定义"),
    ("## 6.2 Files", "## 6.2 Files 文件"),
    ("### 6.2.1 文件列表", "### 6.2.1 File List 文件列表"),
    ("### 6.2.2 ipc-os.c（UIO 用户侧）", "### 6.2.2 ipc-os.c (UIO User Proxy) UIO 用户侧代理"),
    ("### 6.2.3 ipc-os.h（UIO 用户侧）", "### 6.2.3 ipc-os.h (UIO User Proxy) UIO 用户侧头文件"),
    ("### 6.2.4 ipc-os.c（CDEV 用户侧）", "### 6.2.4 ipc-os.c (CDEV User Proxy) CDEV 用户侧代理"),
    ("### 6.2.5 ipc-os.h（CDEV 用户侧）", "### 6.2.5 ipc-os.h (CDEV User Proxy) CDEV 用户侧头文件"),
    ("### 6.2.6 ipc-os.c（全内核 OSAL）", "### 6.2.6 ipc-os.c (In-Kernel OSAL) 全内核 OSAL"),
    ("### 6.2.7 ipc-os.h（全内核 OSAL）", "### 6.2.7 ipc-os.h (In-Kernel OSAL) 全内核 OSAL 头文件"),
    ("## 6.3 SWU_IPCS_LINUX_OS_KERN 软件单元设计", "## 6.3 SWU_IPCS_LINUX_OS_KERN Software Unit Design 软件单元设计"),
    ("## 6.4 SWU_IPCS_LINUX_OS_UIO 软件单元设计", "## 6.4 SWU_IPCS_LINUX_OS_UIO Software Unit Design 软件单元设计"),
    ("## 6.5 SWU_IPCS_LINUX_UIO_KO 软件单元设计", "## 6.5 SWU_IPCS_LINUX_UIO_KO Software Unit Design 软件单元设计"),
    ("## 6.6 SWU_IPCS_LINUX_OS_CDEV 软件单元设计", "## 6.6 SWU_IPCS_LINUX_OS_CDEV Software Unit Design 软件单元设计"),
    ("## 6.7 SWU_IPCS_LINUX_CDEV_KO 软件单元设计", "## 6.7 SWU_IPCS_LINUX_CDEV_KO Software Unit Design 软件单元设计"),
    ("## 6.8 Linux HAL 函数设计", "## 6.8 SWU_IPCS_HAL_LINUX Software Unit Design 软件单元设计"),
    ("## 6.9 Linux 关键场景流程", "## 6.9 Linux Key Scenario Flows Linux 关键场景流程"),
    ("### 6.9.1 UIO 初始化（LIN-S01）", "### 6.9.1 UIO Initialization (LIN-S01) UIO 初始化"),
    ("### 6.9.2 CDEV 初始化（LIN-S02）", "### 6.9.2 CDEV Initialization (LIN-S02) CDEV 初始化"),
    ("### 6.9.3 全内核初始化（LIN-S03）", "### 6.9.3 In-Kernel Initialization (LIN-S03) 全内核初始化"),
    ("### 6.9.4 UIO 发送通知（LIN-S04）", "### 6.9.4 UIO Transmit Notify (LIN-S04) UIO 发送通知"),
    ("### 6.9.5 CDEV 发送通知（LIN-S05）", "### 6.9.5 CDEV Transmit Notify (LIN-S05) CDEV 发送通知"),
    ("### 6.9.6 UIO 接收唤醒（LIN-S06）", "### 6.9.6 UIO Receive Wakeup (LIN-S06) UIO 接收唤醒"),
    ("### 6.9.7 CDEV 接收唤醒（LIN-S07）", "### 6.9.7 CDEV Receive Wakeup (LIN-S07) CDEV 接收唤醒"),
    ("### 6.9.8 全内核接收（LIN-S08）", "### 6.9.8 In-Kernel Receive (LIN-S08) 全内核接收"),
    ("## 6.10 Global variants 全局变量", "## 6.10 Global Variables 全局变量"),
    ("## 6.11 Data Structure 类型定义", "## 6.11 Data Types 类型定义"),
    # Chapter 7
    ("# 7 双向追溯与一致性 (Bidirectional Traceability and Consistency)", "# 7 BIDIRECTIONAL TRACEABILITY AND CONSISTENCY 双向追溯与一致性"),
    ("## 7.1 追溯性策略与声明 (Traceability Statement)", "## 7.1 Traceability Statement 追溯性策略与声明"),
    ("## 7.2 需求-架构-设计-代码 双向追溯矩阵 (Bidirectional Traceability Matrix)", "## 7.2 Bidirectional Traceability Matrix 双向追溯矩阵"),
]

# Sort by length descending to avoid partial replacements
REPLACEMENTS.sort(key=lambda x: len(x[0]), reverse=True)


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
            print(f"  [{n}x] {old!r} -> {new!r}")
    MD.write_text(text, encoding="utf-8")
    print(f"done: {count} replacements in {MD}")


if __name__ == "__main__":
    main()
