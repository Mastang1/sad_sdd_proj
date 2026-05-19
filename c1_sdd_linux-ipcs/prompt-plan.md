# plan-0
 - 约定：
        L1：RTOS 部署变体 / Linux 部署变体
        L2 RTOS：×× 实现（FreeRTOS 实现等）
        L2 Linux：UIO 实现、CDEV 实现、全内核实现

 - 情况说明：
    1. 参考代码 @ipcs 和架构设计文档  @ipcs-architecture.pdf ,在架构设计中，未对Linux适配组件进行更细的划分，但是在具体的详细设计代码中，该OS适配层根据实际的实现分为user-kernel两个部分或者全内核实现，user-kernel不分中，为了保持架构设计中统一的hal和osal接口，在user层添加了glue 代码，保证在user构建库中有hal和osal的接口代理，并通过UIO或者cdev与kernel driver通信，实际实现在kernel中实现，如真实操作hardware的实现是在kernel的driver实现的；
    2. rtos中osal部署变体采用三个实际的rtos，使用统一的osal 接口实现；
    3. 目前SDD文档状态 @md_sdd_0519.md

 - 问题：
    1. @md_sdd_0519.md 文档结构如何修改，形成一个提纲，保证符合当前情况；
    2. 是否添加 依赖说明章节，包括外部硬件资源依赖和软件组件依赖如 RTOS api以及Linux kernel组件等；
    3. 情况说明 序号1中的问题，在提纲中必须解决；
    4. 要求：修改后的sdd提纲要覆盖aspice 4的规范要求


任务：目标操作文件 @md_sdd_0519.md
1. 评估文档每一句话，以产品级文档的要求，删除不符合要求的词句；
2. 章节2 3，十分乱，章节2，划分组件到单元ID 划分即可；章节3 核心细化rtos部署变体、Linux部署变体，以及内部分层剖析设计；
3. 修改前核对10遍，保证这两个章节 2. 3. 符合代码，符合补充信息，文档结构合理，设计符合文档阅读顺序
补充： - 1. 因为ipcs采用三层架构设计，shm、osal、hal三个层级之间具有固定不变的接口契约；为了满足hal、osal接口契约，Linux适配层分为user侧和kernel侧两个部分；其中user侧的接口契约完全满足hal、osal接口契约，user侧的具体代码实现是实现了对os和hw操作的代理实现，具体的OSAL和HW实现在kernel中，也就是Linux适配组件包括user侧的代理和kernel侧的实际实现。前边讲的这个设计是uio和cdev两个Linux部署变体的具体实现架构；
 - 2.Linux部署变体的全内核实现中，Linux适配组件包括具体的"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\os_kernel\ipc-os.c" 和 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\hw\c1\ipc-hw.c",也就是不用user侧代理，与rtos部署形态一致；



任务：目标操作文件 @md_sdd_0519.md
#role： aspice专家、Linux/mcu 驱动专家、架构师
任务：分析章节 2 章节3，基于源码 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs"及 一下补充信息，完善它们
补充： - 1. 因为ipcs采用三层架构设计，shm、osal、hal三个层级之间具有固定不变的接口契约；为了满足hal、osal接口契约，Linux适配层分为user侧和kernel侧两个部分；其中user侧的接口契约完全满足hal、osal接口契约，user侧的具体代码实现是实现了对os和hw操作的代理实现，具体的OSAL和HW实现在kernel中，也就是Linux适配组件包括user侧的代理和kernel侧的实际实现。前边讲的这个设计是uio和cdev两个Linux部署变体的具体实现架构；
 - 2.Linux部署变体的全内核实现中，Linux适配组件包括具体的"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\os_kernel\ipc-os.c" 和 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\hw\c1\ipc-hw.c",也就是不用user侧代理，与rtos部署形态一致；