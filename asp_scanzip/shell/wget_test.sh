#!/bin/sh

#用于下载文件
echo "从10.12.70.42的nginx中下载文件"
wget --http-user=admin  --http-passwd=xsZjMbbcgSMHy39x3kpkP+YcFMQyYSRn6L67dSWntBM= -nd -r -l1 --no-parent -A .zip -P /vulnerability/zip_app_script/pkg_app_report/report  http://10.12.70.42:5050/scan_report/output_report/pkg_app_report/
cd /vulnerability/zip_app_script/pkg_app_report

#判断下载文件是否为空
file_num=$(ls /vulnerability/zip_app_script/pkg_app_report/report | wc -l)
echo $file_num

if [ $file_num -eq 0 ];then
	echo "文件不存在,程序不执行"
	cd /vulnerability/zip_app_script/pkg_app_report
	rm -rf report
	exit
else
	echo "文件存在，开始执行文件"
	#改名称，以时间命名文件夹
	PKG_FILR=$(date "+%Y%m%d")
	mv  report  $PKG_FILR

	#再把以时间命名的文件压缩包移至指定路径
	cp -r /vulnerability/zip_app_script/pkg_app_report/$PKG_FILR /vulnerability/upload/pkg_app_report

fi
