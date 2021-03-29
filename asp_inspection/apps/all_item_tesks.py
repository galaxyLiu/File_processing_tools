#!/user/bin/env python
# -*- coding:utf-8 -*-

import xlrd

from config.dev import file_name, sheet_name_list
from apps.handle_umsLog import handle_umslog
from page_tasks.handle_system import handle_inspection_index
from page_tasks.excel_system import merge_ums_item_data


def handle_all_excelInfo():
    """
    逐个表处理，每张表的表头信息有差异
    1、处理ums日志信息
    2、处理各巡检指标信息
    3、将各巡检指标信息与日志信息做整合输出至excel中
    :return:
    """
    with xlrd.open_workbook(file_name) as workbook:
        name_sheets = workbook.sheet_names()  # 获取Excel的sheet表列表，存储是sheet表名
        for index in name_sheets:  # for 循环读取每一个sheet表的内容
            if index in sheet_name_list:
                print(index)
                # 获取到每个index，去获取对应的数据,获取每页数据执行一致，调用一个方法，不一致再方法中再分别获取
                # 每页的数据获取是可以适配的，umslog的数据获取参数传递
                inspection_data = handle_inspection_index(workbook, index)
                umslog_data = handle_umslog(index)
                merge_ums_item_data(umslog_data, inspection_data, index)
            else:
                print(">>>>请查看配置文件中sheet_name_list定义是否与巡检指标中文件一致！！！")
