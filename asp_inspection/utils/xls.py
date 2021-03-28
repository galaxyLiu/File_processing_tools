#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlwt


class XlwtObj:
    """
    生成excel文件工具类
    """
    def __init__(self, file):
        self.file = file
        self.wbk = xlwt.Workbook()

    def get_sheet(self, name):
        try:
            sheet = self.sheet_by_name(name)
        except:
            sheet = self.wbk.add_sheet(name)
        return sheet

    def sheet_write_header(self, sheet, row, title):
        for i in range(len(title)):
            sheet.write(row, i, title[i])
            # 设置行宽
            first_col = sheet.col(i)  # xlwt中是行和列都是从0开始计算的
            first_col.width = 256 * 13
            # 设置行高
            sheet.row(i).height_mismatch = True
            sheet.row(i).height = 20 * 20  # 20是基数*20是行的高度

        self.wbk.save(self.file)

    def sheet_write(self, sheet, ncols, nrows, data):
        for i in range(len(data)):
            n = ncols + i
            for j in range(nrows):
                sheet.write(n, j, data[i][j])
        self.wbk.save(self.file)

    def sheet_new_write(self, sheet, datas):
        # i = 1
        i = 4
        for list in datas:
            j = 0
            # 内围循环列
            for data in list:
                sheet.write(i, j, list[data])
                j += 1
            i += 1
            # 设置行高
            sheet.row(i).height_mismatch = True
            sheet.row(i).height = 20 * 20  # 20是基数*20是行的高度
        # 最后将文件save保存
        self.wbk.save(self.file)
        print(u'\n录入成功！')

    def sheet_dict_write(self, sheet, row, datas):
        i = row
        keys = list(datas.keys())
        j = 0
        # 内围循环列
        for key in keys:
            sheet.write(i, j, datas[key])
            j += 1
        # 设置行高
        sheet.row(i).height_mismatch = True
        sheet.row(i).height = 20 * 20  # 20是基数*20是行的高度
        # 最后将文件save保存
        self.wbk.save(self.file)
        print(u'\n录入成功！')
