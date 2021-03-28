#!/user/bin/env python
# -*- coding:utf-8 -*-
from common.handle_merge_excel import merge_ums_excel_data
from common.handle_excel_report import handle_excel_data
from config.dev import traffic_excel_name


def merge_ums_traffic_data(ums_data, traffic_data):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_data:ums数据
    :param traffic_data:交维数据
    :return:
    """
    print("=========处理交维巡检===========")
    data_marge_list = merge_ums_excel_data(ums_data,traffic_data)
    # print(data_marge_list)
    header_title = "交维巡检报表"
    handle_excel_data(data_marge_list, header_title, traffic_excel_name)
