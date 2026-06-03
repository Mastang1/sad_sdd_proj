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
 - 2. 保证文档格式使用原始final_sdd.docx的标题格式；
 - 3. 保证所有svg图，表格，文本都拷贝正确，表格拷贝遵循cursorrules规则；


# task-7 ipcs详细设计章节完善，目标文件为 @md_sdd_0519.md
 - 1. 实现 7	LINUX 部署变体详细设计，添加所有函数的设计，函数信息来自 "C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\ipcs\mpu", 函数信息格式参考 章节6；
 - 2. 函数信息的表格格式按照cursorrules要求开发；
 - 3. 函数序列图的生成按照cursorrules的要求，先生成plantuml，然后在执行的路径生成svg，最后插入到指定文档位置；
 - 4. 要求内核侧的Linux驱动开发，要按照驱动开发的章节要求和格式编写，不必与RTOS设计相同；
 - 5. 完善详细设计，加入各个部署实现的关键场景流程图，必须与代码一致；
 - 6. 章节 4	分层架构与部署变体设计中缺少必要的静态图，根据cursorrules，添加对应的静态图

 # task-7 补充修改 目标文件为 @md_sdd_0519.md
  - 1. 修改 6.7 Linux 关键场景流程章节和 RTOS关键场景流程章节；首先，场景流程动态设计部分不能用流程图，必须用uml序列图，展示不同的软件单元ID之间的动态流程；
  - 2. 先删除这两个章节的流程，分析代码，先列出需要的跨单元的流程场景，然后分别为这些跨单元的流程画出基于uml的序列图，图中加入必要注释；序列图元与图中的序列图颜色一致；每个章节的序列图要尽量涵盖跨单元的流程；核心流程必须有对应的图；


# task-8 目标：@md_sdd_0519.md 章节8修改
 - 1. 删除当前章节8，根据格式从"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\format_refer\chapter-trace-temple.md"粘贴模板到md文档；
 - 2. 分别参考 @ipcs-architecture.pdf的 "2.4 REQUIREMENTS ALLOCATION 需求分配"章节，获取 需求-组件 追溯映射、参考当前 @md_sdd_0519.md的单元设计章节，获取组件-单元的映射；完成章节8的内容编写；
 - 要求：格式符合标题和内容；内容符合指定文档信息，不虚构；


# task-9: @md_sdd_0519.md 完善
 - 1. 总体任务，参考章节 4.1和4.2，修改章节5.1 5.2及章节6.1 6.2
 - 2.要求：标题以章节4.1 4.2为模板
 - 3. 要求：文件的依赖关系图采用组件uml图实现，颜色与章节4系统；生成依赖源码的#include信息；要求先生成plantuml，然后转为svg并插入到文档对应位置
 - 4. 要求：生成后核对对应源码文件夹的文件名称、数量是否与文档一致；核对是否符合所有要求；


# task-10: @md_sdd_0519.md 完善
 - 1. 总体任务，@md_sdd_0519.md文档中的"4.7 Dynamic Detailed Design 动态详细设计"章节的5个流程图缺失，重新生成uml序列图，然后转为svg格式，最后插入到对应位置；注意：序列图的生成、插入流程遵循rules中对应的约束；
 - 2. 要求：只可修改指定的操作，不要自行修改其他位置

# task-11: @md_sdd_0519.md 完善
 - 1. 总体任务，@md_sdd_0519.md的章节6的表格中，有多余的"`"符号，主要做表格单元格 函数定义文件 和 函数声明文件之后，需要分析并删除 " `"符合；
 - 2. 要求：只可修改指定的操作，不要自行修改其他位置


# task-12: 源码修改 和 @md_sdd_0519.md对应符号的同步更新
 - 0.任务0：修改源码中enum ipc_s32g3xx_processor_idx为 enum ipc_c1_processor_idx
 - 1. 任务1： 修改源码中所有的结构体类型,把ipc前缀改为ipcs，然后添加后缀_TYPE,最后修改类型名称为大写，例如把 ipc_mscm_regs改为 IPCS_MSCM_REGS_TYPE;
 - 2. 任务2：修改源码中所有enmu类型名称，把ipc前缀改为ipcs，然后添加后缀_E,最后修改类型名称为大写，例如把 ipc_c1_processor_idx 改为IPCS_C1_PROCESSOR_IDX_E；
 - 3.任务3：根据代码更新 @md_sdd_0519.md,更新代码中对应的struct 、 enum类型名称的修改，这些集中在标题为 全局变量 和 类型定义 章节
 - 2. 要求：只可修改指定的操作，不要自行修改其他位置；


# task-13: 源码修改 和 @md_sdd_0519.md 生成 @final_sdd.docx 标题格式修改
 - 1. 在原有的更新 @final_sdd.docx的功能基础上，进行如下标题文字格式修改：
     - 一级标题：修改为微软雅黑、粗体、4号子，注意包含修改标题号
     - 二级标题：修改为微软雅黑、粗体、斜体、小4号子，注意包含修改标题号
     - 三级标题：修改为微软雅黑、粗体、小4号子，注意包含修改标题号
     - 要求：只可以修改标题，不可修改其他任何内容；执行成功后把该功能加入到生成脚本中

# task-14: 根据源码修改 @md_sdd_0519.md 
 - 1. 遍历 @md_sdd_0519.md中章节4、章节5、章节6 共计三个章节中的svg流程图slug对应的plantuml文件，根据内容等信息，在源码中找到对应的函数，然后执行分析，根据分析信息需要重新生成的文件判断条件如下：1.1：若流程图中只有笼统的描述语言，而非代码逻辑，证明该图不可用，需要重新生成；1.2：流程图节点中有endif、...符合、多余的%号等不符合实际函数的字符及语句，证明该图不可用需要重新生成；1.3：若某个plantuml从上到下流程叠加节点超过20个，证明需要修改，改为两列方案；
 - 2. 根据1中提取到的需要更新的插图slug，开始基于对应的函数源码执行plantuml生成、转为svg，并插入到对应的 @md_sdd_0519.md位置的操作；重新生成必须遵循的约束规则：2.1：生成的plantuml必须不能包含纯描述语句，节点中必须是来自代码函数的表达式；2.2：代码中复杂的表达式可以合并在一个节点中，节点中多个表达式要换行；2.3：连续多个赋值语句必须放在一个流程图节点中，并必须换行；2.4：当从上到下节点长度达到20个后，下个节点要放到左侧或者右侧，禁止流程图布局为面条形状；
 - 要求：先执行1，然后根据1的列表，执行任务2；只可执行1中判断需要修改的插图，不许修改 @md_sdd_0519.md中其他地方任意的文本；执行任务2完成后，必须将所有生成的plantuml和源码给到LLM，重新校验是否符合2.1-2.4的要求，不符合重新执行生成，并再次校验，直到最终完全符合要求；

# task-15: 根据源码修改 @final_sdd.docx
 - 1. final_sdd.docx文件中的svg数量太多，导致编写后不能保存，现在需要批量转换指定的svg为emf格式的图片，存储在cursor_tmp下的flow_emf路径下，然后用指定的emf文件，替换docx中的svg；
 - 2. 要求：只可以替换执行的流程图svg，保持当前的缩放尺寸(所以要先记录每个svg的宽高和位置)；不许修改其他任何地方
 - 3. 规则：必须使用 inkscape命令，现有的"C:\tangyapeng\docs\StarGather\sad_sdd_proj\c1_sdd_linux-ipcs\cursor_tmp\flow_emf"实测在word中打不开