#!/bin/sh

#删除原来文件,创建空文件 [相关包和路径一定要看清楚]
#删除打包相关文件
cd /data/ftproot/scan_report/output_report
rm -rf app_report
mkdir app_report
rm -rf pkg_app_report
mkdir pkg_app_report
#此路径为打包文件占放路径
cd /vulnerability_test/zip_app_script/scan_project
rm -rf pkg_app_report
mkdir pkg_app_report
