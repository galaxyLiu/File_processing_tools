#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tasks.cmdb_data import cmdb_data_job
from tasks.app_report import app_report_job
from tasks.app_summary import app_summary_job
from tasks.cmdb_report import cmdb_report_job
from tasks.report_data import report_data_job
from tasks.scan_data import scan_data_job



def handel_app_report():
    scan_data_job()  # 此任务是对网页报告进行爬虫处理，并录入到 es 集群中。
    cmdb_data_job()  # 此任务是录入 cmdb 原始数据，作为es 查询原始数据使用。
    cmdb_report_job()  # 此任务是录入 cmdb 原始数据，后面与扫描数据进行对接
    report_data_job()  # 此次任务是爬虫扫描报告中的数据，并与任务cmdb_report_job进行对接。
    app_report_job()  # 此任务是按业务维度输出业务excel 报告。
    app_summary_job()  # 此任务是汇总输出扫描报告数据按业务维度输出总数量，高中低漏洞汇总数据


def main():
    #在此之前先进行先进行判断扫描文件是否上传成功，文件上传成功开始执行
    #研发平台展示，业务相关报告需求
    handel_app_report()



if __name__ == '__main__':
    main()
