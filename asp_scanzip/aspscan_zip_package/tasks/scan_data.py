#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.es import ElasticObj
from utils.scan import ScanObj
from utils.xls import XlwtObj
from common.handler_data import get_xls_data, get_scan_data
from config import *
from urllib.parse import unquote


def taskjob(task, xls_outfile):
    esobj = ElasticObj(es_address)
    xlwtobj = XlwtObj(xls_outfile)
    scan = ScanObj(base_url)
    # subtask_url = base_url + task + "/" + subtask + "/"
    subtask_url = base_url + task + "/"
    poolnames = scan.get_dirname(subtask_url)
    pool_pro_names = {}

    for poolname in poolnames:
        scan_jobs = scan.get_dirname(subtask_url + poolname)
        pool_pro_names[poolname] = scan_jobs
    for poolname in poolnames:
        ncols = 1
        if pool_pro_names[poolname]:
            sheet = xlwtobj.get_sheet(poolname.strip("/"))
            xlwtobj.sheet_write_header(sheet, scan_title)
        for scan_job in pool_pro_names[poolname]:
            final_name = scan.get_dirname(subtask_url + poolname + scan_job)
            final_name = unquote(final_name[0], encoding="utf8")
            if final_name == "无存活主机/":
                continue
            else:
                task_url = subtask_url + poolname + scan_job + 'index.html'
                scan_job = unquote(scan_job, encoding="utf8")
                scan_id = scan_job.split('_')[0]
                result = scan.get_result(task_url, scan_id, task, poolname)
                xlwtobj.sheet_write(sheet, ncols, len(scan_title), get_xls_data(result))  # 将cmdb数据写入excel表中
                ncols = ncols + len(result)
                index = scan_index_prefix + poolname.strip("/")
                esobj.bulk_Index_Data(index, get_scan_data(index, result))  # 以index的形式存入es中，会覆盖以前的数据


def scan_data_job():
    task = lm_task_name
    xls_outfile = scan_report_xsl
    taskjob(task, xls_outfile)
