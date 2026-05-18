## C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md文档流程图重新生成、替换任务
 - 必须遵循的规则：
        "所有流程图任务，必须使用 PlantUML 活动图 V2 语法。
        必须包含 !pragma layout smetana。
        必须包含 skinparam conditionStyle insideDiamond 和 skinparam linetype ortho。
        所有的判断必须用 if (label) then (...) 格式，确保文字在菱形内。"
 - 步骤1：分析 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md文档，获取所有内部接口和外部接口函数，然后分析 @IPCS_49中的源码，根据源码中的函数体，在指定临时路径flow_umls下生成uml文件集，要求生成的uml流程图要严格遵循上述必遵循的规则，同时必须严格按照源码函数体生成，不可虚构，不可省略；
- 步骤2： 根据flow_umls下的uml文件，创建python脚本，调用java相关命令，生成对应的svg文件集，存储在临时路径flow_svgs下
- 步骤3： 插入对应的svg文件到  C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md

要求：只可以删改 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md的流程图，不可更改该文件其他内容；

## 修改 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md 章节3.2 Files
修改该文件中章节3.2 Files的头文件依赖图为 组件UML图，颜色为淡卡其色；不改变其他内容，只修改并替换该章节的插图，依赖图生成参考 C:\tangyapeng\docs\StarGather\c1_sdd\IPCS_49对应代码文件

## 替换原始文件ipcs_sdd.md 章节3.2 Files章节的svg插图到 C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx FILES章节，删除旧的，插入对应 原始文件ipcs_sdd.md 章节3.2 Files章节的svg插图， 不更改其他文件内容

## generate word format sdd
任务：以 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md为来源文件，以C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx为目标文件，提取来源文件对应的内容、图片、表格，插入、粘贴到目标文件中，生成最终的SDD文件
要求：除了目标文件的首页不变，其他所有章节的内容全部用来源文件对应的章节替换；来源文件的mermaid格式要转换为svg格式在插入到目标文件；要绝对保证粘贴后目标文件的章节格式、章节构成与来源文件一致；html格式的图表要严格按照原始格式的预览样式粘贴到目标文件对应位置，也就是保持为word的图表格式，但是与来源文件格式一致；

#修复 C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx执行章节内容任务
       - 任务目标1：修改该文件中章节3.2 Files的头文件依赖图为 组件UML图，颜色为淡卡其色；不改变其他内容，只修改并替换该章节的插图，依赖图生成参考 C:\tangyapeng\docs\StarGather\c1_sdd\IPCS_49对应代码文件；要求连接线上不允许添加文字；源文档中的插图有乱码及不应该存在的连接线注释、
       - 任务目标2：以 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md为来源文件，以C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx为目标文件，修改目标文件 4.3	3.3 EXTERNAL INTERFACES外部接口章节和4.4	3.4 INTERNAL FUNCTIONS 内部函数这两个章节中的每个函数描述部分，当前目标文件中的描述部分不可用；需要从对应的来源文件函数描述章节中，拷贝整个表格，并在目标文件粘贴为表格格式，而不是文本格式；该任务目标要求：必须对应正确的函数；必须粘贴完整的表格；必须粘贴为表格形式，而不是文本或者md格式；
       要求：任务1/2只需修改指定部分，不许增删改其他任何内容；

# 插图替换任务
1. 首先删除C:\tangyapeng\docs\StarGather\c1_sdd\files_32_umls所有puml文件中的 title行，不要标题；若puml文件中有中文，更改为对应的英文；
2. 以新的C:\tangyapeng\docs\StarGather\c1_sdd\files_32_umls作为来源，生成新的C:\tangyapeng\docs\StarGather\c1_sdd\files_32_svgs，替换该路径下原始的svgs
3. 将 C:\tangyapeng\docs\StarGather\c1_sdd\files_32_svgs根据对应位置，替换 C:\tangyapeng\docs\StarGather\c1_sdd\ipcs_sdd.md章节 Files；
4. 将 C:\tangyapeng\docs\StarGather\c1_sdd\files_32_svgs根据对应位置，替换 C:\tangyapeng\docs\StarGather\c1_sdd\final_sdd.docx章节 Files；
要求：只修改md和docx文档的指定插图，绝对不可修改其他内容