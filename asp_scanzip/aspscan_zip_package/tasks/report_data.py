#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.es import ElasticObj
from utils.scan import ScanObj
from common.handler_data import get_report_data
from config import *
from urllib.parse import unquote



def taskjob(task):
    esobj = ElasticObj(es_address)
    scan = ScanObj(base_url)
    subtask_url = base_url + task + "/"
    poolnames = scan.get_dirname(subtask_url)
    pool_pro_names = {}

    for poolname in poolnames:
        scan_jobs = scan.get_dirname(subtask_url + poolname)
        pool_pro_names[poolname] = scan_jobs

    for poolname in poolnames:
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
                doc = get_report_data(result, app_index_prefix)
                if doc:
                    esobj.es.bulk(doc)
                print("task successful -- %s", task_url)


def report_data_job():
    task = lm_task_name
    taskjob(task)
    # print("task: %s, subtask: %s is completed !" % (task))

    # subtasks = ['subtask1', 'subtask2', 'subtask3', 'subtask4', 'subtask5', 'subtask6', 'subtask7', 'subtask8',
    #             'subtask9', 'subtask10']
    # for subtask in subtasks:
    #     taskjob(task, subtask)
    #     print("task: %s, subtask: %s is completed !" % (task, subtask))
