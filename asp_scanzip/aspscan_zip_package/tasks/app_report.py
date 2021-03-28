#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elasticsearch import Elasticsearch
from utils.xls import XlwtObj
from config import *




def get_es_data(index):
    es = Elasticsearch([es_address])
    body = {
        "query": {
            "exists": {
                "field": "hight"
            }
        },
        "size": 8000

    }
    res = es.search(index=index, body=body)
    data = res['hits']['hits']
    return data


def get_data(d):
    data = []
    data.append(d['_source']['scan_ip'])
    data.append(d['_source']['hight'])
    data.append(d['_source']['center'])
    data.append(d['_source']['low'])
    data.append(d['_source']['risk'])
    return data


def handle_data(index, datas):
    result = {}
    for d in datas:
        data = get_data(d)
        appname = d['_source']['appname']
        if appname not in result:
            result[appname] = [data]
        else:
            result[appname].append(data)
    for appname in result:
        appname_str=appname.strip()
        appname_str = appname_str.replace('\n', '')
        xlwtobj = XlwtObj('/data/ftproot/scan_report/output_report/app_report/%s.xls' % appname_str)
        # if index.startswith("ops"):
        #     xlwtobj = XlwtObj('data/output/ops_report/07/%s.xls' % appname)
        # elif index.startswith("app"):
        #     xlwtobj = XlwtObj('data/output/app_report/07/%s.xls' % appname)

        sheet = xlwtobj.get_sheet(appname.split(':')[0])
        xlwtobj.sheet_write_header(sheet, title_app_report)
        xlwtobj.sheet_write(sheet, 1, len(title_app_report), result[appname])


def app_report_job():
    # ops_datas = get_es_data(ops_index)
    app_datas = get_es_data(app_index)
    # handle_data(ops_index, ops_datas)
    handle_data(app_index, app_datas)
