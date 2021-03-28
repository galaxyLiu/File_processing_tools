from elasticsearch import Elasticsearch
from config import *
from utils.xls import XlwtObj

es = Elasticsearch(es_address)
title = title1


def get_new_xls_data(result):  # 将es数据存入表格
    data = []
    for r in result:
        d = []
        d.append(r['scan_ip'])
        d.append(r['report_time'])
        d.append(r['vulnerability_name'])
        d.append(r['repair_method'])
        d.append(r['appname'])
        d.append(r['department_2'])
        d.append(r['device_classify'])
        d.append(r['mai_manufacturer'])
        d.append(r['device_name'])
        data.append(d)

    return data


def get_new_scan_data(index_scan, result):
    data = []
    for d in result:
        action = {
            "_index": index_scan,
            "_type": 'data',
            "_id": d['scan_ip'],
            "_source": {
                "scan_ip": d['scan_ip'],
                "report_time": d['report_time'],
                "vulnerability_name": d['vulnerability_name'],
                "repair_method": d['repair_method']
            }
        }
        data.append(action)
    return data


def getTotalCount_by_index(index):
    body = {
        "query": {
            "exists": {
                "field": "repair_method"
            }
        },
        "size": 0
    }
    res = es.search(index=index, body=body)
    return res['hits']['total']


def getdata_by_fromAndBody(start, index):
    body = {
        "from": start,
        "query": {
            "exists": {
                "field": "repair_method"
            }
        },
        "size": 3000
    }
    res = es.search(index=index, body=body)
    return res['hits']['hits']


def get_es_data(index_scan):
    start = 0
    total = getTotalCount_by_index(index_scan)
    datas = []
    while start < total:
        data = getdata_by_fromAndBody(start, index_scan)
        datas.extend(data)
        start += len(data)
    return datas


def get_data(d):
    result = []
    sourcedata = d['_source']
    vulnerability_name = sourcedata['vulnerability_name']
    repair_method = sourcedata['repair_method']
    for name, method in zip(vulnerability_name, repair_method):
        data = []
        data.append(d['_id'])
        data.append(sourcedata['report_time'])
        data.append(sourcedata['risk_grade'])
        data.append(name)
        data.append(method)
        data.append(sourcedata['is_exist'])
        data.append(sourcedata['appname'])
        data.append(sourcedata['department_2'])
        data.append(sourcedata['device_classify'])
        data.append(sourcedata['mai_manufacturer'])
        data.append(sourcedata['device_name'])
        data.append(sourcedata['poolname'])
        result.append(data)
    return result


# def out_to_excel(data, file):
#     print("开始执行。。。")
#     xlwtobj = XlwtObj(file)
#     sheet = xlwtobj.get_sheet('扫描报告')
#     xlwtobj.sheet_write_header(sheet, title_ruixue)
#     nrow = 1
#     for d in data:
#             result = get_data(d)
#             xlwtobj.sheet_write(sheet, nrow, len(title_ruixue), result)
#             nrow += len(result)
#             print("存入成功。。。")


def app_report_new_job_v1():
    app_datas = get_es_data(index_prefix_leak_data + "*")

    xlwtobj = XlwtObj(new_report_2019_fourth)
    hight_sheet = xlwtobj.get_sheet('高风险扫描报告')
    xlwtobj.sheet_write_header(hight_sheet, title_ruixue)

    middle_sheet = xlwtobj.get_sheet('中等风险扫描报告')
    xlwtobj.sheet_write_header(middle_sheet, title_ruixue)

    hight_nrow=1
    middle_nrow=1
    for data in app_datas:
        result = get_data(data)
        if data['_source']['risk_grade'] == "2":
            xlwtobj.sheet_write(hight_sheet, hight_nrow, len(title_ruixue), result)
            hight_nrow += len(result)
            print("hight 存入成功。。。")
        else:
            xlwtobj.sheet_write(middle_sheet, middle_nrow, len(title_ruixue), result)
            middle_nrow += len(result)
            print("middle 存入成功。。。")


def app_report_new_job():
    app_datas = get_es_data(index_prefix_leak_data + "*")

    xlwtobj = XlwtObj(new_report_2019_fourth)
    anquan_sheet = xlwtobj.get_sheet('安全设备')
    xlwtobj.sheet_write_header(anquan_sheet, title_ruixue)

    cunchu_sheet = xlwtobj.get_sheet('存储设备')
    xlwtobj.sheet_write_header(cunchu_sheet, title_ruixue)

    wangluo_sheet = xlwtobj.get_sheet('网络设备')
    xlwtobj.sheet_write_header(wangluo_sheet, title_ruixue)

    fuwuqi_sheet = xlwtobj.get_sheet('服务器')
    xlwtobj.sheet_write_header(fuwuqi_sheet, title_ruixue)

    no_cmdb_sheet = xlwtobj.get_sheet('cmdb未关联')
    xlwtobj.sheet_write_header(no_cmdb_sheet, title_ruixue)

    anquan_nrow=1
    cunchu_nrow=1
    wangluo_nrow=1
    fuwuqi_nrow=1
    no_cmdb_nrow=1
    for data in app_datas:
        result = get_data(data)
        if data['_source']['is_exist'] == 1:
            if data['_source']["device_classify"] == "安全设备":
                xlwtobj.sheet_write(anquan_sheet, anquan_nrow, len(title_ruixue), result)
                anquan_nrow += len(result)
                print("安全设备 存入成功。。。")
            elif data['_source']["device_classify"] == "存储设备":
                xlwtobj.sheet_write(cunchu_sheet, cunchu_nrow, len(title_ruixue), result)
                cunchu_nrow += len(result)
                print("存储设备 存入成功。。。")
            elif data['_source']["device_classify"] == "网络设备":
                xlwtobj.sheet_write(wangluo_sheet, wangluo_nrow, len(title_ruixue), result)
                wangluo_nrow += len(result)
                print("网络设备 存入成功。。。")
            elif data['_source']["device_classify"] == "服务器":
                xlwtobj.sheet_write(fuwuqi_sheet, fuwuqi_nrow, len(title_ruixue), result)
                fuwuqi_nrow += len(result)
                print("服务器 存入成功。。。")
        elif data['_source']['is_exist'] == 0:
            xlwtobj.sheet_write(no_cmdb_sheet, no_cmdb_nrow, len(title_ruixue), result)
            no_cmdb_nrow += len(result)
            print("no_cmdb 存入成功。。。")


