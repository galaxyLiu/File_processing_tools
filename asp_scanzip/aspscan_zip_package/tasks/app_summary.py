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
        "size": 0,
        "aggs": {
            "group_by_appname": {
                "terms": {
                    "field": "appname.keyword",
                    "size": 500
                },
                "aggs": {
                    "sum_of_hight": {
                        "sum": {
                            "field": "hight"
                        }
                    },
                    "sum_of_center": {
                        "sum": {
                            "field": "center"
                        }
                    },
                    "sum_of_low": {
                        "sum": {
                            "field": "low"
                        }
                    },
                    "avg_of_risk": {
                        "avg": {
                            "field": "risk"
                        }
                    }
                }
            }

        }
    }
    res = es.search(index=index, body=body)
    data = res['aggregations']['group_by_appname']['buckets']
    return data


def get_data(d):
    data = []
    data.append(d['_source']['scan_ip'])
    data.append(d['_source']['hight'])
    data.append(d['_source']['center'])
    data.append(d['_source']['low'])
    data.append(d['_source']['risk'])
    return data


def handle_data(datas):
    result = []
    for d in datas:
        data = []
        data.append(d['key'])
        data.append(d['doc_count'])
        data.append(int(d['sum_of_hight']['value']))
        data.append(int(d['sum_of_center']['value']))
        data.append(int(d['sum_of_low']['value']))
        data.append(int(d['avg_of_risk']['value']))
        result.append(data)
    return result


def app_summary_job():
    data = get_es_data(app_index)
    result = handle_data(data)
    xlwtobj = XlwtObj(summary_file)
    name = 'summary_app'
    # if index.startswith("app"):
    #     xlwtobj = XlwtObj('data/output/summary_report/07/summary_app.xls')
    #     name = 'summary_app'
    # elif index.startswith("ops"):
    #     xlwtobj = XlwtObj('data/output/summary_report/07/summary_ops.xls')
    #     name = 'summary_ops'
    sheet = xlwtobj.get_sheet(name)
    xlwtobj.sheet_write_header(sheet, summary_title)
    xlwtobj.sheet_write(sheet, 1, len(summary_title), result)



