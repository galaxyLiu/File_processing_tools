## 安全扫描报告工具 ScanProject

### 1. 简介

####         在卓望一级私有云项目中，通过绿盟安全扫描器对一级私有云所列的系统进行安全扫描。扫描方式为全量分多个批量进行，扫描完回自动生成报告，并上传到 ftp 服务器中，后台对报告进行自动化处理，并与 cmdb 数据核对，按几个需求进行自动化出多个维度的报告。

#### 环境
##### #env python3
##### elasticsearch
##### bs4
##### lxml
##### xlrd
##### xlwt

  ### 2. 报告输出

 ##### a. scan_data_job:  此任务是对网页报告进行爬虫处理，并录入到 es 集群中。

##### b. cmdb_data_job: 此任务是录入 cmdb 原始数据，作为es 查询原始数据使用。

##### c. cmdb_report_job: 此任务是录入 cmdb 原始数据，后面与扫描数据进行对接。

##### d. report_data_job: 次任务是爬虫扫描报告中的数据，并与任务cmdb_report_job进行对接。

##### e. app_report_job： 此任务是按业务维度输出业务excel 报告。

##### f. app_summary_job： 此任务是汇总输出扫描报告数据按业务维度输出总数量，高中低漏洞汇总数据。

##### g. pkg_report_job： 此任务需要放在服务端执行，执行输出打包 zip 数据，存放在 web 站点提供访问和下载。



## 

### 报告输出

#####  app_new_report_job() :报告处理方法

##### a. handle_scan_data() :此任务是对网页报告进行爬虫处理，并录入到 es 集群中。

##### b. handle_cmdb_data() :此任务是录入 cmdb 原始数据，作为es 查询原始数据使用。

##### c. app_report_new_job() :此任务是汇总输出扫描报告数据按业务维度输出报告，高中漏洞汇总数据



##### feichi_scan_report():个性化处理方法 

##### a. handle_feichi_scan_data()：此任务是对网页报告进行爬虫处理，并录入到 es 集群中。

##### b. handle_feichi_report() ：此任务是汇总输出扫描报告数据按业务维度输出报告，高中漏洞汇总数据





