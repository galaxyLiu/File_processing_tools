# 离线巡检报告工具

### 1、简介

##### 在卓望一级私有云项目中，通过ums平台对自动化脚本进行运行输出系统巡检、基线巡检、交维巡检输出日志与巡检指标进行对接。按巡检各维度输出报告。

### 2、数据处理说明

##### a、handle_all_excelInfo： 程序入口

##### b、handle_umslog：处理ums日志数据处理

##### c、handle_system_inspection_index：系统巡检指标数据处理

##### d、handle_baseline_indicators：基线巡检指标数据处理

##### e、handle_traffic_dimension_index：交维巡检指标数据处理

##### f、merge_ums_excel_data：系统巡检与ums日志文件合并

##### g、handle_excel_data：excel报告输出

### 3、文件夹说明

##### 需创建两个文件夹

##### a、input：umslog文件及巡检指标存放位置

##### b、output：生成文件存放位置

### 4、传入文件要求
##### umslog文件按约定规范以 ip_umslog命名，文件内容每个索引开头以 # 分隔换行
##### 巡检指标文件，系统巡检指标、基线巡检指标、交维巡检指标分三页合并在一个文件中，并分别以此命名。
##### 文件头部不得随意修改，修改文件头部信息及时同步以免数据不准确。

