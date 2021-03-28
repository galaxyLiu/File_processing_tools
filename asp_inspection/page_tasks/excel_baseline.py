#!/user/bin/env python
# -*- coding:utf-8 -*-
from common.handle_merge_excel import merge_ums_excel_data
from common.handle_excel_report import handle_excel_data
from config.dev import baseline_excel_name


def merge_ums_baseline_data(ums_data, baseline_data):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_data: ums日志文件数据
    :param baseline_data: 基线报告数据
    :return:
    """
    print("=========处理基线巡检===========")
    data_merge_list = merge_ums_excel_data(ums_data,baseline_data)
    # print("===",data_marge_list)
    header_title = "基线巡检报表"
    handle_excel_data(data_merge_list, header_title,baseline_excel_name)

