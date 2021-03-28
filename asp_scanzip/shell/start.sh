#!/bin/sh

#判断供安全员方提供上传文件的路径是否存在文件，存在则执行，不存在则退出
#a、删除上次索引数据，删除上次生成的包
#b、将各资源池传过来的包，解压并移动到运行路径
#c、执行文件解析代码
#d、将生成的业务zip包从10.200.11.169移动到192.168.70.245


#路径对应自己的路径
#判断文件是否存在，文件存在则往下执行

file_num=$(ls /home/zabbix/security_report/app_monthly_report | wc -l)
echo $file_num

if [ $file_num -eq 0 ];then
	echo "文件不存在,程序不执行"
	exit
else
	echo "文件存在，开始执行文件"
	#a、删除上次索引数据，删除上次生成的包
	curl http://10.12.70.42:9200 
	if [[ $? -eq 0 ]];then
		echo "es启动成功。。。" 
		#将原来索引数据删除
		#月度索引
		curl -XPOST '10.12.70.42:9200/scan_data_index_*/_delete_by_query?refresh&slices=5&pretty' -H 'Content-Type: application/json' -d'{"query": {"match_all": {}}}'
		curl -XPOST '10.12.70.42:9200/cmdb_data_index_*/_delete_by_query?refresh&slices=5&pretty' -H 'Content-Type: application/json' -d'{"query": {"match_all": {}}}'
		curl -XPOST '10.12.70.42:9200/app_report_data_index_*/_delete_by_query?refresh&slices=5&pretty' -H 'Content-Type: application/json' -d'{"query": {"match_all": {}}}'
		#瑞雪漏洞报告索引，不需要则不启用
		#curl -XPOST '10.12.70.42:9200/security_scan1_cmdb2_*/_delete_by_query' -H 'Content-Type: application/json'  -d'{"query": {"match_all": {}}}'
		echo "上月es存入索引数据已删除成功。。。" 
	else
		echo "es未启动，请先启动es！！！！" 
		exit 0
	fi 
	
	#删除资源池安全报告包相关文件,删除运行路径的报告
	cd /data/ftproot/scan_project/pool_scan_tasks
	rm -rf lvmeng
	mkdir lvmeng
	echo "删除上月报告数据成功。。。" 

	#b、将各资源池传过来的包，解压并移动到运行路径，上传路径的报告需在此步解压完后删除
	#文件解压后解压到  /data/ftproot/scan_project/pool_scan_tasks 此为运行环境
	cd /vulnerability_test/zip_app_script
	python3 get_zip_files.py

	#c、执行文件解析代码
	#进入扫描文件脚本文件夹
	cd /vulnerability_test/zip_app_script/aspscan_zip_package
	#执行扫描报告输出任务
	python3 run.py
	echo "安全报告输出任务完成。。。" 

	#获取上一个脚本任务执行情况
	if [[ $? -eq 0 ]];then
		#进入打包执行目录，执行打包任务
		cd /vulnerability_test/zip_app_script/scan_project
		python3 pkg_report.py 
	else
		echo "扫描报告输出任务执行有误，请排查！！！！" 
		exit 0
	fi

	#d、将生成的业务zip包从10.200.11.169移动到192.168.70.245
	#此步骤不适用scp命令执行，文件传到nginx路径下去，在192.168.70.245使用wget方式获取文件
fi
