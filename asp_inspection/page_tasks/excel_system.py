#!/user/bin/env python
# -*- coding:utf-8 -*-

from common.handle_merge_excel import merge_ums_excel_data
from common.handle_excel_report import handle_excel_data
from config.dev import system_excel_name


def merge_ums_system_data(ums_datas, system_data):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_data: 处理后的ums日志数据
    :param system_data: 处理后的系统巡检数据
    :return:
    """
    print("=========处理系统巡检===========")
    data_merge_list = merge_ums_excel_data(ums_datas, system_data)
    # print("====", data_merge_list)
    header_title = "系统巡检报表"
    handle_excel_data(data_merge_list, header_title, system_excel_name)
