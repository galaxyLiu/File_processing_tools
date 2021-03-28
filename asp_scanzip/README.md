## 安全扫描报告工具 ScanProject

### 1、简介

#### 在卓望一级私有云项目中，通过绿盟安全扫描器对一级私有云所列的系统进行安全扫描。扫描方式为全量分多个批量进行，扫描完回自动生成报告，并上传到 ftp 服务器中，后台对报告进行自动化处理，并与 cmdb 数据核对，按几个需求进行自动化出多个维度的报告。

### 2. 报告输出

##### a. scan_data_job:  此任务是对网页报告进行爬虫处理，并录入到 es 集群中。

##### b. cmdb_data_job: 此任务是录入 cmdb 原始数据，作为es 查询原始数据使用。

##### c. cmdb_report_job: 此任务是录入 cmdb 原始数据，后面与扫描数据进行对接。

##### d. report_data_job: 次任务是爬虫扫描报告中的数据，并与任务cmdb_report_job进行对接。

##### e. app_report_job： 此任务是按业务维度输出业务excel 报告。

##### f. app_summary_job： 此任务是汇总输出扫描报告数据按业务维度输出总数量，高中低漏洞汇总数据。

##### g. pkg_report_job： 此任务需要放在服务端执行，执行输出打包 zip 数据，存放在 web 站点提供访问和下载。



### 3、脚本说明

##### start.sh 主程序运行脚本，用于设置定时任务，启动月度安全报告执行，数据存入es，执行文件打包程序将文件传入指定服务器。

##### 判断供安全员方提供上传文件的路径是否存在文件，存在则执行，不存在则退出

##### a、通过清除索引数据命令，删除上次索引数据，删除上次生成的包

##### b、get_zip_files.py  将各资源池传过来的包，解压并移动到运行路径

##### c、aspscan_zip_package/run.py 执行文件解析代码

##### d、scan_project/pkg_report.py 将生成的业务zip包从程序运行服务器移动到指定对接服务器

##### e、最后执行删除生成zip文件的命令



### 4、文件夹说明

##### scan_project 用于执行打包文件的文件层配置

##### pkg_app_report 用于生成zip文件前文件组装中间层

##### 将按业务维度输出业务excel 报告，根据业务维度索引中的ip与原报告中ip进行比对，获取到原报告

##### resources为html中的样式封装，将获取到的ip.html文件与样式封装，变成所需要的可直接查看的文件。



### 5、脚本使用文件配置说明

##### a、aspscan_zip_package/dev.py文件进行索引及文件路径的配置

##### b、get_zip_files.py 文件头部配置解压源文件和解压目的文件的地址

##### c、pkg_report.py 配置文件说明

##### //nginx数据

##### data_dir = '/data/ftproot/scan_project/pool_scan_tasks'

##### //app_report生成的按业务名命名的包

##### report_dir = '/data/ftproot/scan_report/output_report'

##### report = 'app_report'

##### //存入es中app业务的索引

##### index = 'app_report_data_index_*'

