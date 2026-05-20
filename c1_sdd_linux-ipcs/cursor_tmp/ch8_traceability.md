# 8 双向追溯与一致性 (Bidirectional Traceability and Consistency)

## 8.1 追溯性策略与声明 (Traceability Statement)

本章节旨在建立并证明本模块的软件详细设计与上游（软件需求、软件架构）以及下游（物理源代码）之间的双向追溯关系，以满足 ASPICE 规范中 SWE.3.BP4 的核心要求。

本追溯矩阵确保了各层级设计的一致性（Consistency）与完整性：上游 `ipcs-architecture.pdf` §2.4 需求分配表中的架构组件均在本文档软件单元与 `ipcs/` 源码中落实；函数级设计见第 4–6 章。过程类需求（安全、构建、测试流程等）由项目 SWE 工作产品承担，不在 SDD 软件单元表中展开实现。

需求—组件映射真源：`ipcs-architecture.pdf` §2.4 REQUIREMENTS ALLOCATION（V1.0，2026-04-16）。组件—单元映射真源：本文档 §2.1–§2.2。

## 8.2 需求-架构-设计-代码 双向追溯矩阵 (Bidirectional Traceability Matrix)

下表按架构文档 §2.4 逐条展开：同一需求 ID 若分配多个架构组件，则分多行；「本详细设计单元 ID」与「物理源代码实体」来自 §2.2 与 §2.1。

| 软件需求 ID (SWE.1) | 需求简述 | 架构组件 ID (SWE.2) | 本详细设计单元 ID (SWE.3 Unit) | 物理源代码实体 (Code) | 设计章节 | 追溯关系及设计覆盖说明 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| IPCS_001 | 同核或异核上应用间点对点双向通信 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 端到端路径：Drv_Ipcs_Conf_Cmp 配置对称布局；Drv_Ipcs_Core_Cmp 实例/通道； Drv_Ipcs_Queue_Cmp 队列与 BD； Drv_Ipcs_Osal_Cmp/Drv_Ipcs_Hal_Cmp 地址与通知 |
| IPCS_001 | 同核或异核上应用间点对点双向通信 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 端到端路径：Drv_Ipcs_Conf_Cmp 配置对称布局；Drv_Ipcs_Core_Cmp 实例/通道； Drv_Ipcs_Queue_Cmp 队列与 BD； Drv_Ipcs_Osal_Cmp/Drv_Ipcs_Hal_Cmp 地址与通知 |
| IPCS_001 | 同核或异核上应用间点对点双向通信 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 端到端路径：Drv_Ipcs_Conf_Cmp 配置对称布局；Drv_Ipcs_Core_Cmp 实例/通道； Drv_Ipcs_Queue_Cmp 队列与 BD； Drv_Ipcs_Osal_Cmp/Drv_Ipcs_Hal_Cmp 地址与通知 |
| IPCS_001 | 同核或异核上应用间点对点双向通信 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 端到端路径：Drv_Ipcs_Conf_Cmp 配置对称布局；Drv_Ipcs_Core_Cmp 实例/通道； Drv_Ipcs_Queue_Cmp 队列与 BD； Drv_Ipcs_Osal_Cmp/Drv_Ipcs_Hal_Cmp 地址与通知 |
| IPCS_001 | 同核或异核上应用间点对点双向通信 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 端到端路径：Drv_Ipcs_Conf_Cmp 配置对称布局；Drv_Ipcs_Core_Cmp 实例/通道； Drv_Ipcs_Queue_Cmp 队列与 BD； Drv_Ipcs_Osal_Cmp/Drv_Ipcs_Hal_Cmp 地址与通知 |
| IPCS_002 | 部署于 AutoSAR OS 时满足 ASIL-D | 过程类 | —（过程类；非运行时软件单元） | — | — | 安全目标分解、安全机制与证据在独立安全工作中产品化；架构上 Drv_Ipcs_Osal_Cmp 承担 AutoSAR 集成与 OS 交互边界 |
| IPCS_002 | 部署于 AutoSAR OS 时满足 ASIL-D | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 安全目标分解、安全机制与证据在独立安全工作中产品化；架构上 Drv_Ipcs_Osal_Cmp 承担 AutoSAR 集成与 OS 交互边界 |
| IPCS_003 | 内核与硬件平台、字节序无关 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 可移植逻辑在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp； 平台相关集中在 Drv_Ipcs_Hal_Cmp；字节序通过可移植类型与显式转换策略在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp 收敛 |
| IPCS_003 | 内核与硬件平台、字节序无关 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 可移植逻辑在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp； 平台相关集中在 Drv_Ipcs_Hal_Cmp；字节序通过可移植类型与显式转换策略在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp 收敛 |
| IPCS_003 | 内核与硬件平台、字节序无关 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 可移植逻辑在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp； 平台相关集中在 Drv_Ipcs_Hal_Cmp；字节序通过可移植类型与显式转换策略在 Drv_Ipcs_Core_Cmp/Drv_Ipcs_Queue_Cmp 收敛 |
| IPCS_005 | 作为复杂驱动在 AutoSAR OS 下运行 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 与 AutoSAR CDD/OS 接口封装、调度与错误钩子对齐；Drv_Ipcs_Conf_Cmp 配置由集成方提供 |
| IPCS_006 | 作为驱动在 ThreadX 下运行 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | ThreadX 变体 OSAL：任务/中断/同步原语映射 |
| IPCS_009 | platform / os / phy / transport | 过程类 | —（过程类；非运行时软件单元） | — | — | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_009 | platform / os / phy / transport | Drv_Ipcs_Linux_Adapt_Cmp | SWU_IPCS_LINUX_OS_UIO、SWU_IPCS_LINUX_OS_CDEV、SWU_IPCS_LINUX_OS_KERN、SWU_IPCS_LINUX_UIO_KO、SWU_IPCS_LINUX_CDEV_KO | `ipcs/mpu/os_uio/ipc-os.c`；`ipcs/mpu/os_cdev/ipc-os.c`；`ipcs/mpu/os_kernel/ipc-os.c`；`ipcs/mpu/os_kernel/ipc-uio.c`；`ipcs/mpu/os_kernel/ipc-cdev.c` | §6.3、§6.4、§6.5、§6.6、§6.7 | 目录与依赖方向约束架构分层；删除一层仅当上层不依赖该抽象时成立，需在集成配置中关闭对 |
| IPCS_010 | 传输层设计支持基准与吞吐量估计 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 在传输路径保留可观测计数/时间戳或钩子，供基准测试构建使用；不与生产最小集强制绑定 |
| IPCS_010 | 传输层设计支持基准与吞吐量估计 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 在传输路径保留可观测计数/时间戳或钩子，供基准测试构建使用；不与生产最小集强制绑定 |
| IPCS_011 | 可在 Windows 主机上构建 | 过程类 | —（过程类；非运行时软件单元） | — | — | 构建系统、工具链与主机桩实现；不属 Drv_Ipcs_Core_Cmp～ Drv_Ipcs_Linux_Adapt_Cmp 运行时职责 |
| IPCS_012 | 主机单元测试、 组件易于模型替换 | 过程类 | —（过程类；非运行时软件单元） | — | — | 通过 OSAL/HWAL 接口注入替身；测试工程与 mock 属 SWE.3/SWE.5 支持 |
| IPCS_012 | 主机单元测试、 组件易于模型替换 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 通过 OSAL/HWAL 接口注入替身；测试工程与 mock 属 SWE.3/SWE.5 支持 |
| IPCS_012 | 主机单元测试、 组件易于模型替换 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 通过 OSAL/HWAL 接口注入替身；测试工程与 mock 属 SWE.3/SWE.5 支持 |
| IPCS_012 | 主机单元测试、 组件易于模型替换 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 通过 OSAL/HWAL 接口注入替身；测试工程与 mock 属 SWE.3/SWE.5 支持 |
| IPCS_012 | 主机单元测试、 组件易于模型替换 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 通过 OSAL/HWAL 接口注入替身；测试工程与 mock 属 SWE.3/SWE.5 支持 |
| IPCS_013 | 信息安全与功能安全验证需模糊测试 | 过程类 | —（过程类；非运行时软件单元） | — | — | SWE.5 /安全验证计划中的测试手段；架构上保持接口边界清晰以便 fuzz 目标收敛 |
| IPCS_014 | SHM 驱动支持多通信通道（数据流） | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 多 channel 模型与共享内存布局 |
| IPCS_014 | SHM 驱动支持多通信通道（数据流） | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 多 channel 模型与共享内存布局 |
| IPCS_014 | SHM 驱动支持多通信通道（数据流） | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 多 channel 模型与共享内存布局 |
| IPCS_015 | 通道/流内消息顺序保持 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 单通道队列语义与发送/接收顺序约定 |
| IPCS_015 | 通道/流内消息顺序保持 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 单通道队列语义与发送/接收顺序约定 |
| IPCS_016 | 每通道支持多个缓冲池 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | pool 配置与 Drv_Ipcs_Queue_Cmp 多队列管理 |
| IPCS_016 | 每通道支持多个缓冲池 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | pool 配置与 Drv_Ipcs_Queue_Cmp 多队列管理 |
| IPCS_016 | 每通道支持多个缓冲池 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | pool 配置与 Drv_Ipcs_Queue_Cmp 多队列管理 |
| IPCS_017 | 全核多传输并行、高效核利用 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 多 instance；Drv_Ipcs_Osal_Cmp 每核执行模型与中断亲和 |
| IPCS_017 | 全核多传输并行、高效核利用 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 多 instance；Drv_Ipcs_Osal_Cmp 每核执行模型与中断亲和 |
| IPCS_017 | 全核多传输并行、高效核利用 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 多 instance；Drv_Ipcs_Osal_Cmp 每核执行模型与中断亲和 |
| IPCS_018 | 零拷贝 API 与实现 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 指针/BD 描述已有缓冲区，避免驱动内额外拷贝 |
| IPCS_018 | 零拷贝 API 与实现 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 指针/BD 描述已有缓冲区，避免驱动内额外拷贝 |
| IPCS_019 | 异步（基于通知）接收 API | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 回调由 Drv_Ipcs_Osal_Cmp 异步上下文触发； Drv_Ipcs_Core_Cmp 分发 |
| IPCS_019 | 异步（基于通知）接收 API | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 回调由 Drv_Ipcs_Osal_Cmp 异步上下文触发； Drv_Ipcs_Core_Cmp 分发 |
| IPCS_020 | 两通信端间不受干扰（内存保护） | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 共享内存分区与访问权限由布局 （Drv_Ipcs_Conf_Cmp）与 SoC/OS 内存保护共同保证；Drv_Ipcs_Core_Cmp 遵守边界 |
| IPCS_020 | 两通信端间不受干扰（内存保护） | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 共享内存分区与访问权限由布局 （Drv_Ipcs_Conf_Cmp）与 SoC/OS 内存保护共同保证；Drv_Ipcs_Core_Cmp 遵守边界 |
| IPCS_021 | 非托管通道，应用独占通道内存 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | unmanaged 模型与 ipcsShmUnmanaged* 路径 |
| IPCS_021 | 非托管通道，应用独占通道内存 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | unmanaged 模型与 ipcsShmUnmanaged* 路径 |
| IPCS_022 | 虚拟中断不投递陈旧数据 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 序列号/队列状态与通知路径协调，避免在无效状态下回调 |
| IPCS_022 | 虚拟中断不投递陈旧数据 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 序列号/队列状态与通知路径协调，避免在无效状态下回调 |
| IPCS_022 | 虚拟中断不投递陈旧数据 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 序列号/队列状态与通知路径协调，避免在无效状态下回调 |
| IPCS_022 | 虚拟中断不投递陈旧数据 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 序列号/队列状态与通知路径协调，避免在无效状态下回调 |
| IPCS_023 | 丢失中断不导致数据丢失 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 依赖共享内存中的提交顺序与对端可见性；接收方可通过轮询或计数补偿（与 IPCS_039 协同） |
| IPCS_023 | 丢失中断不导致数据丢失 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 依赖共享内存中的提交顺序与对端可见性；接收方可通过轮询或计数补偿（与 IPCS_039 协同） |
| IPCS_024 | 与 AUTOSAR 4.4 或更高版本兼容 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 接口与配置模型对齐 R4.4+ 集成约定 |
| IPCS_024 | 与 AUTOSAR 4.4 或更高版本兼容 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 接口与配置模型对齐 R4.4+ 集成约定 |
| IPCS_025 | 池中缓冲区数量与大小可配置 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 集成配置数据；Drv_Ipcs_Core_Cmp/ Drv_Ipcs_Queue_Cmp 消费 |
| IPCS_028 | 支持核间中断作为收发通知 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | Drv_Ipcs_Hal_Cmp 平台实现； Drv_Ipcs_Osal_Cmp 挂接 Linux/RTOS 中断模型 |
| IPCS_028 | 支持核间中断作为收发通知 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | Drv_Ipcs_Hal_Cmp 平台实现； Drv_Ipcs_Osal_Cmp 挂接 Linux/RTOS 中断模型 |
| IPCS_029 | 软件组件使用静态内存分配 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 实现约束：无堆或受限堆；池与队列静态维度由 Drv_Ipcs_Conf_Cmp 定义 |
| IPCS_029 | 软件组件使用静态内存分配 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 实现约束：无堆或受限堆；池与队列静态维度由 Drv_Ipcs_Conf_Cmp 定义 |
| IPCS_029 | 软件组件使用静态内存分配 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 实现约束：无堆或受限堆；池与队列静态维度由 Drv_Ipcs_Conf_Cmp 定义 |
| IPCS_030 | 设备端源码符合编码规范 | 过程类 | —（过程类；非运行时软件单元） | — | — | 编码标准与静态分析门禁 |
| IPCS_031 | 多对内核（多实例）通信 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 多 instance 与独立 SHM/IRQ 配置 |
| IPCS_031 | 多对内核（多实例）通信 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 多 instance 与独立 SHM/IRQ 配置 |
| IPCS_034 | 校验应用传入的公共 API 参数 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 各公共 API 入口参数与范围检查 |
| IPCS_035 | 校验通道类型与所请求操作是否匹配 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | managed/unmanaged API 与 channel 类型一致性 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Core_Cmp | SWU_IPCS_CORE_SHM、SWU_IPCS_CORE_UTIL | `ipcs/ipcs_cores/ipc-shm.c` / `ipc-shm.h`；`ipcs/ipcs_cores/ipc-util.c` / `ipc-util.h` | §4 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Queue_Cmp | SWU_IPCS_CORE_QUEUE | `ipcs/ipcs_cores/ipc-queue.c` / `ipc-queue.h` | §4 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Conf_Cmp | SWU_IPCS_CORE_TYPES | `ipcs/ipcs_cores/ipc-types.h`；工程 `ipcf_Ip_Cfg*.h` | §4.6 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_036 | 低延迟、小体积、可按需裁剪 HW/OS/传输 | Drv_Ipcs_Linux_Adapt_Cmp | SWU_IPCS_LINUX_OS_UIO、SWU_IPCS_LINUX_OS_CDEV、SWU_IPCS_LINUX_OS_KERN、SWU_IPCS_LINUX_UIO_KO、SWU_IPCS_LINUX_CDEV_KO | `ipcs/mpu/os_uio/ipc-os.c`；`ipcs/mpu/os_cdev/ipc-os.c`；`ipcs/mpu/os_kernel/ipc-os.c`；`ipcs/mpu/os_kernel/ipc-uio.c`；`ipcs/mpu/os_kernel/ipc-cdev.c` | §6.3、§6.4、§6.5、§6.6、§6.7 | 可选编译与目录级特性开关；Linux 路径 Drv_Ipcs_Linux_Adapt_Cmp 按需链接 |
| IPCS_038 | 按辰至汽车质量流程开发为生产级软件 | 过程类 | —（过程类；非运行时软件单元） | — | — | 项目管理、配置管理、问题解决与发布流程；架构文档为 SWE.2 工作产品之一 |
| IPCS_039 | 支持轮询方式 （IRQ_NONE） | Drv_Ipcs_Osal_Cmp | SWU_IPCS_OSAL_AUTOSAR、SWU_IPCS_OSAL_FREERTOS、SWU_IPCS_OSAL_THREADX、SWU_IPCS_LINUX_OS_KERN | `ipcs/mcu/os/autosar/ipc-os-autosar.c`；`ipcs/mcu/os/freertos/ipc-os-freertos.c`；`ipcs/mcu/os/threadx/ipc-os-threadx.c`；`ipcs/mpu/os_kernel/ipc-os.c` | §5.3、§5.4、§5.5、§6.3 | Drv_Ipcs_Osal_Cmp ipcsShmPollChannels / 轮询桥接；Drv_Ipcs_Hal_Cmp 在无硬件 IRQ 路径下的空操作或最小支持 |
| IPCS_039 | 支持轮询方式 （IRQ_NONE） | Drv_Ipcs_Hal_Cmp | SWU_IPCS_HAL_MCU、SWU_IPCS_HAL_LINUX | `ipcs/mcu/hw/ipc-hw.c`；`ipcs/mpu/hw/c1/ipc-hw.c` | §5.6、§6.8 | Drv_Ipcs_Osal_Cmp ipcsShmPollChannels / 轮询桥接；Drv_Ipcs_Hal_Cmp 在无硬件 IRQ 路径下的空操作或最小支持 |

## 8.3 软件单元与源码索引（与 §2 一致）

| SW-Unit-ID | 源码文件 | 详细设计章节 |
| :--- | :--- | :--- |
| SWU_IPCS_CORE_SHM | ipcs/ipcs_cores/ipc-shm.c | §4.2–§4.4 |
| SWU_IPCS_CORE_QUEUE | ipcs/ipcs_cores/ipc-queue.c | §4.2、§4.4 |
| SWU_IPCS_CORE_UTIL | ipcs/ipcs_cores/ipc-util.c | §4.2、§4.4 |
| SWU_IPCS_CORE_TYPES | ipcs/ipcs_cores/ipc-types.h | §4.6 |
| SWU_IPCS_OSAL_AUTOSAR | ipcs/mcu/os/autosar/ipc-os-autosar.c | §5.3 |
| SWU_IPCS_OSAL_FREERTOS | ipcs/mcu/os/freertos/ipc-os-freertos.c | §5.4 |
| SWU_IPCS_OSAL_THREADX | ipcs/mcu/os/threadx/ipc-os-threadx.c | §5.5 |
| SWU_IPCS_HAL_MCU | ipcs/mcu/hw/ipc-hw.c | §5.6 |
| SWU_IPCS_LINUX_OS_KERN | ipcs/mpu/os_kernel/ipc-os.c | §6.3 |
| SWU_IPCS_LINUX_OS_UIO | ipcs/mpu/os_uio/ipc-os.c | §6.4 |
| SWU_IPCS_LINUX_UIO_KO | ipcs/mpu/os_kernel/ipc-uio.c | §6.5 |
| SWU_IPCS_LINUX_OS_CDEV | ipcs/mpu/os_cdev/ipc-os.c | §6.6 |
| SWU_IPCS_LINUX_CDEV_KO | ipcs/mpu/os_kernel/ipc-cdev.c | §6.7 |
| SWU_IPCS_HAL_LINUX | ipcs/mpu/hw/c1/ipc-hw.c | §6.8 |

对外应用 API（`ipcs-shm.h` 非 static）：`ipcsShmInit`、`ipcsShmFree`、`ipcsShmAcquireBuf`、`ipcsShmReleaseBuf`、`ipcsShmTx`、`ipcsShmUnmanagedAcquire`、`ipcsShmUnmanagedTx`、`ipcsShmIsRemoteReady`、`ipcsShmPollChannels` — 设计见 §4.3，与 §3.3 一致。
