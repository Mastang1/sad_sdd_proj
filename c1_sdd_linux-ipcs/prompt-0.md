#Task

## task1：格式化 @ipc-shm 文件夹的代码
 - 1. 修改 @ipc-shm 中所有代码，修改函数命名规则为驼峰命名法，并把函数名称前缀ipc_改为ipcs,例如：ipc_shm_rx更改为ipcsShmRx;
 - 2. 接头体定义名称格式修改：将所有结构体格式改为大写命名方式，并添加后缀_TYPE, 同时把前缀ipc_改为IPCS_;例如 struct ipc_unmanaged_channel 改为： struct IPCS_UNMANAGED_CHANNEL_TYPE
 - 3. 替换所有ipcf字符串为对应大小写的ipcs

## task2：变体代码对比分析
 - 1.简单背景说明： @ipc-shm 和 @IPCS_49 这两个folders包含了IPC核间共享内存驱动的多RTOS和Linux的不同实现，但是采用了shm层、os 适配层、hw 适配层桑层划分，每层之间使用固定的API实现了解耦；问题：现在分析C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\IPCS_49\common和C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\ipc-shm.c及C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\ipc-queue.c，也就是分析两个driver的shm层这个组件在实现上有什么不同；区分的必要性是什么、为什么这么做而不统一？形成分析报告到工作区的ana.md
 - 2. 1中的shm层，是否可以统一为一个对两种变体都适用的模块？除了错误类型，int sint32这种无关紧要的修改，难点在哪里？是否可以实现不用条件编译宏来实现一个统一的shm层？如果必须要条件编译，列举哪部分需要。总体要求：尽量搞一个不用条件编译宏的统一的shm层
 - 3. cfg部分统一用现有rtos部分的配置；catch flush部分用#ifdef方式判断是否为Linux来处理；内存拷贝函数，用统一的rtos中自定义的实现；Autosar 文件头版本互检也用宏判断；返回错误类型及返回值类型统一为sint32为int；Linux日志部分删除不用；基于以上的处理，还有哪些影响统一shm层的部分？

---
## task3: 
 - 背景描述：
  1. 当前工作区核心是一个名为IPCS的 基于共享内存的核间通信 Linux驱动源码，具体源代码路径在 C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm；
  2.在架构设计规范文档中，将该驱动分为三个层级，参考"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipcs-architecture.pdf",每个层级有固定的API契约；三个层级为：ipcs_shm(具体的共享内存管理逻辑和对外API)、ipcs_os(提供OS软中断接口共享内存数据发送中断，并在软中间线程中进行数据的处理序列)、ipcs_hw(提供必要的中断控制、内存access等API封装)；
  3. 为了满足架构设计规范的契约，实现了三种不同的实现、部署方案:
   a. 基于uio子系统实现user-kernl访问的方案。在user侧通过"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_uio"实现满足架构设计的ipcs_os/ipcs_hw接口契约，因为user侧的ipcs_hw接口不能直接访问硬件，所以统一在"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_uio"封装，不再依赖"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\hw"实现，具体的hardware的访问在内核模块中实现，user侧通过uio进行访问；内核侧的对应实现在"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_kernel"中的"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_kernel\ipc-uio.c"中，基于平台设备实现设备匹配，基于UIO实现user中断接收，通过cdev实现初始化配置；
   b.基于cdev 设备模型的user-kernel访问方案。具体实现参考代码：内核侧实现——"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_kernel\ipc-cdev.c",user 侧实现"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_cdev";
   c. 全内核实现方案。参考源码："C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipc-shm\os_kernel\ipc-os.c";
   
- 任务1：基于上述"a. 基于uio子系统实现user-kernl访问的方案。",实现详细设计规范，写入到根路径的ipcs_uio_adapt_SDD.md;
  1. 要求a的实现综合组件名为Linux 适配组件，架构分层为ipcs_uio_user_glue（具体LLM可以改一个更规范的名称）和在内核侧的 ipcs_uio_driver;
  2. 要求在详细设计中加入：Linux 适配组件的分层架构视图，设计说明信息；组件的对外接口设计，user-kernel的接口设计；要求该部分设计参考"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipcs-architecture.pdf"的格式实现；符合aspice规范要求；
  3. 要求在详细设计中加入：user侧的代码的静态设计设计，及对外接口、内部函数的详细实现；参考"C:\tangyapeng\docs\StarGather\c1_sdd_linux-ipcs\ipcs_sdd.md"的章节3.3、/3.4;特别强调：每个函数的详细契约信息必须画出表格，参考 3.3.1 ipcsShmInit 章节的格式，必须保持表格格式完全一致，这个要求实现后必须核对，格式一致才可以通过；
  4. 要求为每个函数设计的小章节的表格后加入设计流程图，流程图用mermaid格式实现，参考 3.3.1 ipcsShmInit 章节实现


 - 1. 完成IPCS Driver SDD 分层部署章节编写，细化不同部署变体和实现方式的接口和单元边界描述；
 - 2. 完成LINUX侧UIO、CDEV两种适配层实现的接口详细设计。详细描述通用的OSAL、HAL接口为契约、具体的接口协议实现；
 - 3. 完成Linux适配层的几个设计单元的类型定义、全局变量章节编写；
 - 4. 全文档格式修改、完善；
  
  其他：mpecan-lin自动测试用例失败问题解决结论，和同事一起调试复现用例失败的调用栈现象为log打印接口递归调用，导致栈溢出，同事修改log打印接口为异步实现后，回归测试通过；
