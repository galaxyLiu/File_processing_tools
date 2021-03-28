#!/user/bin/env python
# -*- coding:utf-8 -*-

import xlrd

from config.dev import file_name
from apps.handle_umsLog import handle_umslog
from page_tasks.excel_baseline import merge_ums_baseline_data
from page_tasks.excel_traffic import merge_ums_traffic_data
from page_tasks.handle_system import handle_system_inspection_index
from page_tasks.handle_baseline import handle_baseline_indicators
from page_tasks.handle_traffic import handle_traffic_dimension_index
from page_tasks.excel_system import merge_ums_system_data


def handle_all_excelInfo():
    """
    逐个表处理，每张表的表头信息有差异
    1、处理ums日志信息
    2、处理各巡检指标信息
    3、将各巡检指标信息与日志信息做整合输出至excel中
    :return:
    """
    umslog_data = handle_umslog()
    with xlrd.open_workbook(file_name) as workbook:
        name_sheets = workbook.sheet_names()  # 获取Excel的sheet表列表，存储是sheet表名
        for index in name_sheets:  # for 循环读取每一个sheet表的内容
            if index == "系统巡检指标":
                system_data = handle_system_inspection_index(workbook, index)
                merge_ums_system_data(umslog_data, system_data)
            elif index == "基线巡检指标":
                baseline_data = handle_baseline_indicators(workbook, index)
                merge_ums_baseline_data(umslog_data, baseline_data)
            elif index == "交维巡检指标":
                traffic_data = handle_traffic_dimension_index(workbook, index)
                merge_ums_traffic_data(umslog_data, traffic_data)
