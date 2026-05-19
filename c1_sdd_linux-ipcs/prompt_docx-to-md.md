# task-1
 - 1. 基于 @final_sdd.docx 转换成md_sdd_0519.md; 
 - 2. 要求：完整的转换，用对应的markdown标题等级等保持原始标题；章节不乱；插图保持原始文件；


# task-2
 - 1. 基于代码IPCS_49的 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd\IPCS_49\os\threadx\ipc-os-threadx.c",重新生成文档"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd\md_sdd_0519.md"的OSAL(THREADX) 函数实现 （todo）章节；先删除对应的内容，然后根据代码生成对应的函数、表格和流程图；流程图的生成要严格遵循cursorrules中的相关要求；生成流程图的步骤是先生成plantuml，然后生成svg到临时路径，最后插入指定svg到文档


# task-3
 - 1. 同步刚生成的 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd\md_sdd_0519.md"的OSAL(THREADX) 函数实现 （todo）章节到文档 @final_sdd.docx 。先删除对应章节的表格和流程图，然后用cursorrules中指定的方法和要求插入表格和svg图到指定位置；同时其他内容不变；插图的表格格式严格遵守cursorrules中指定的要求，保持单元格位置、合并、拆分严格与原始文档一致，并在word中用word风格的表格实现。

# task-4 名称更改
L1：RTOS 部署变体 / Linux 部署变体
L2 RTOS：×× 实现（FreeRTOS 实现等）
L2 Linux：UIO 实现、CDEV 实现、全内核实现

# task-5 勘误 修改 @md_sdd_0519.md文档中的错误实现
 - 1. 因为ipcs采用三层架构设计，shm、osal、hal三个层级之间具有固定不变的接口契约；为了满足hal、osal接口契约，Linux适配层分为user侧和kernel侧两个部分；其中user侧的接口契约完全满足hal、osal接口契约，user侧的具体代码实现是实现了对os和hw操作的代理实现，具体的OSAL和HW实现在kernel中，也就是Linux适配组件包括user侧的代理和kernel侧的实际实现。前边讲的这个设计是uio和cdev两个Linux部署变体的具体实现架构；
 - 2.Linux部署变体的全内核实现中，Linux适配组件包括具体的"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\os_kernel\ipc-os.c" 和 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu\hw\c1\ipc-hw.c",也就是不用user侧代理，与rtos部署形态一致；
  
  任务要求：1.根据aspice4，完善 @md_sdd_0519.md的设计，主要是章节# 2 架构符合性与软件单元划分，保证章节的功能单一，章节划分要合理，Linux的架构细分部分可以单例一章； 2. 根据1和2的架构设计，修正 @md_sdd_0519.md中对应的设计内容；

# task-6 转换 md格式sdd为docx格式
 - 1. 遵守cursorrules规则，将 @md_sdd_0519.md内容完全转换到 final_sdd.docx中

# task-7 ipcs详细设计章节完善，目标文件为 @md_sdd_0519.md