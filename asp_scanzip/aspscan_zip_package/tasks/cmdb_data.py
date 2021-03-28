#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from utils.es import ElasticObj
from common.handler_data import get_cmdb_data
from config import *


def cmdb_data_job():
    wb = xlrd.open_workbook(cmdb_file)
    index_prefix = cmdb_index
    esobj = ElasticObj(es_address)
    for name in wb.sheet_names():
        sheet = wb.sheet_by_name(name)
        print("start perform %s sheet." % name)
        for data in get_cmdb_data(sheet, sheet.number, sheet.name, index_prefix, doc_type):
            esobj.bulk_Data(data)
