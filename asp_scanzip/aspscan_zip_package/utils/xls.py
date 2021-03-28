#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlwt


class XlwtObj:
    def __init__(self, file):
        self.file = file
        self.wbk = xlwt.Workbook()

    def get_sheet(self, name):
        try:
            sheet = self.sheet_by_name(name)
        except:
            sheet = self.wbk.add_sheet(name)
        return sheet

    def sheet_write_header(self, sheet, title):
        for i in range(len(title)):
            sheet.write(0, i, title[i])
        self.wbk.save(self.file)

    def sheet_write(self, sheet, ncols, nrows, data):
        for i in range(len(data)):
            n = ncols + i
            for j in range(nrows):
                sheet.write(n, j, data[i][j])
        self.wbk.save(self.file)
