from elasticsearch import Elasticsearch

from common.handler_new_data import get_new_xls_data, get_new_scan_data
from utils.xls import XlwtObj
from utils.scan import ScanObj
from common.handler_data import handle_cmdb_data_job1, scan_to_es_data
from common.handler_cmdb_new_data import handle_cmdb_new_data
from config import *
from utils.es import ElasticObj
from common.handler_data import get_cmdb_es_data
import xlrd
from common.handler_new_data import app_report_new_job
from common.handler_new_data import app_report_new_job_v1


# 将cmdb数据读取并存入es中
def handle_cmdb_data():
    esobj = ElasticObj(es_address)
    wb = xlrd.open_workbook(cmdb_file)
    for name in wb.sheet_names():
        sheet = wb.sheet_by_name(name)
        print("start perform %s sheet." % name)
        # for data in handle_cmdb_data_job1(sheet, sheet.number, sheet.name, index_prefix_leak_2019_fourth, doc_type):
        for data in handle_cmdb_new_data(sheet, sheet.number, sheet.name, index_prefix_leak_data, doc_type):
            cmdb_doc_data = get_cmdb_es_data(data, index_prefix_leak_data)
            esobj.es.bulk(cmdb_doc_data)
            print("存入成功。。。")


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
        print(poolname)
        if "feichi" in poolname:
            for scan_job in pool_pro_names[poolname]:
                if 'IPMI' in scan_job:
                    continue
                # print("scan_job",scan_job)
                task_url = subtask_url + poolname + scan_job + 'index.html'
                split_url = subtask_url + poolname + scan_job
                result = scan.get_ruixue_result(task_url, poolname, split_url)

                if result:
                    esobj.es.bulk(scan_to_es_data(index_prefix_leak_data, result))
                    # esobj.es.bulk(get_report_data(result, index_prefix_leak_07))  # 将数据存入es
                    print("job: %s --- 存入es成功" % scan_job)


def handle_scan_data():
    task = lm_task_name
    taskjob(task)


def app_new_report_job():
    # 此任务是对网页报告进行爬虫处理，并录入到 es 集群中。
    # handle_scan_data()
    # 此任务是录入 cmdb 原始数据，作为es 查询原始数据使用。
    # handle_cmdb_data()
    # 此任务是汇总输出扫描报告数据按业务维度输出报告，高中漏洞汇总数据
    app_report_new_job()
    # app_report_new_job_v1()
