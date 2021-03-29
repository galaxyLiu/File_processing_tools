#!/user/bin/env python
# -*- coding:utf-8 -*-

from common.handle_merge_excel import merge_ums_excel_data
from common.handle_excel_report import handle_excel_data
from config.dev import excel_name


def merge_ums_item_data(ums_datas, item_datas, sheet):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_datas: 处理后的ums日志数据
    :param item_datas: 处理后的对应页的巡检数据
    :return:
    """
    print("=========处理%s巡检===========" % (sheet))
    data_merge_list = merge_ums_excel_data(ums_datas, item_datas)
    header_title = "%s巡检报表" % (sheet)
    handle_excel_data(data_merge_list, header_title, excel_name,sheet)
