#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from utils.es import ElasticObj
from common.handler_data import get_cmdb_data, get_ops_cmdb_data
from config import *



def cmdb_report_job():
    wb = xlrd.open_workbook(cmdb_file)
    esobj = ElasticObj(es_address)
    for name in wb.sheet_names():
        sheet = wb.sheet_by_name(name)
    for data in get_cmdb_data(sheet, sheet.number, sheet.name, app_index_prefix, doc_type):
        esobj.bulk_Data(data)


# def cmdb_report_job():
#     wb = xlrd.open_workbook('data/input/cmdb.xlsx')
#     esobj = ElasticObj(es_address)
#     for name in wb.sheet_names():
#         sheet = wb.sheet_by_name(name)
#         for index_prefix in index_prefixs:
#             if index_prefix.startswith("app"):
#                 for data in get_cmdb_data(sheet, sheet.number, sheet.name, index_prefix, doc_type):
#                     esobj.bulk_Data(data)
#             elif index_prefix.startswith("ops"):
#                 for data in get_ops_cmdb_data(sheet, sheet.number, sheet.name, index_prefix, doc_type):
#                     esobj.bulk_Data(data)
