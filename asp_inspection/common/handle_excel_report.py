#!/user/bin/env python
# -*- coding:utf-8 -*-

import xlwt,time

from config.dev import header_inspection_index
from utils.xls import XlwtObj


def handle_excel_data(datas, header_title, excel_name,sheet):
    """
    按规范生成excel表
    :param datas: 合并后的ums及巡检数据
    :param header_title: 文件头部名称
    :param excel_name: 文件名称，系统、交维、基线各文件名称
    :return:
    """
    excel_name = excel_name+"%s巡检报表.xls" %sheet
    xlwtobj = XlwtObj(excel_name)

    # 文字居中样式
    center_alignment = xlwt.Alignment()  # Create Alignment
    center_alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    center_alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED

    center_style = xlwt.XFStyle()  # Create Style
    center_style.alignment = center_alignment

    # 文字右对齐样式
    right_alignment = xlwt.Alignment()  # Create Alignment
    right_alignment.horz = xlwt.Alignment.HORZ_RIGHT
    right_alignment.vert = xlwt.Alignment.VERT_CENTER

    right_style = xlwt.XFStyle()  # Create Style
    right_style.alignment = right_alignment

    # 设置背景样式
    blue_pattern = xlwt.Pattern()  # Create the Pattern
    blue_pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    blue_pattern.pattern_fore_colour = 7

    color_style = xlwt.XFStyle()  # Create Style
    color_style.alignment = center_alignment
    color_style.pattern = blue_pattern

    allInfo_sheet = xlwtobj.get_sheet('全量')
    # 表头合并单元格测试
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    allInfo_sheet.write_merge(0, 0, 0, 14, header_title, center_style)
    allInfo_sheet.write_merge(1, 1, 0, 14, current_time, right_style)
    allInfo_sheet.write_merge(2, 2, 0, 14, '巡检全量信息', color_style)
    xlwtobj.sheet_write_header(allInfo_sheet, 3, header_inspection_index)
    xlwtobj.sheet_new_write(allInfo_sheet, datas)

    exception_sheet = xlwtobj.get_sheet('异常')
    exception_sheet.write_merge(0, 0, 0, 14, '巡检异常项', center_style)
    xlwtobj.sheet_write_header(exception_sheet, 1, header_inspection_index)

    artificial_sheet = xlwtobj.get_sheet('人工判断')
    artificial_sheet.write_merge(0, 0, 0, 14, '巡检人工确认项', center_style)
    xlwtobj.sheet_write_header(artificial_sheet, 1, header_inspection_index)

    no_result_sheet = xlwtobj.get_sheet('无结果')
    no_result_sheet.write_merge(0, 0, 0, 14, '巡检无结果项', center_style)
    xlwtobj.sheet_write_header(no_result_sheet, 1, header_inspection_index)

    exception_row = 1
    artificial_row = 1
    no_result_row = 1
    for data in datas:

        aspnode_result = data['aspnode_result']
        aspnode_msg = data['aspnode_msg']

        if aspnode_result == "异常":
            exception_row += 1
            xlwtobj.sheet_dict_write(exception_sheet, exception_row, data)
            print("异常 存入成功。。。")
        elif aspnode_result == "人工判断":
            artificial_row += 1
            xlwtobj.sheet_dict_write(artificial_sheet, artificial_row, data)
            print("人工判断 存入成功。。。")
        elif aspnode_msg == "":
            no_result_row += 1
            xlwtobj.sheet_dict_write(no_result_sheet, no_result_row, data)
            print("无结果 存入成功。。。")
