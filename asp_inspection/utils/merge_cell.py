#!/user/bin/env python
# -*- coding:utf-8 -*-


def merge_cell(sheet_info):
    '''
    #handle Merge transverse cells and handle Merge Vertical Cells, assign empty cells,
    :param rlow:row, include row exclusive of row_range
    :param rhigh:row_range
    :param clow:col, include col exclusive of col_range
    :param chigh:col_range
    :param sheet_info:object of sheet
    :return:dic contain all of empty cells value
    '''
    merge = {}
    merge_cells = sheet_info.merged_cells
    for (rlow, rhigh, clow, chigh) in merge_cells:
        # 合并单元格中的值
        value_mg_cell = sheet_info.cell_value(rlow, clow)
        if rhigh - rlow == 1:
            # Merge transverse cells
            for n in range(chigh - clow - 1):
                merge[(rlow, clow + n + 1)] = value_mg_cell
        elif chigh - clow == 1:
            # Merge Vertical Cells
            for n in range(rhigh - rlow - 1):
                merge[(rlow + n + 1, clow)] = value_mg_cell
    return merge


def list_dic(list1, list2):
    '''
    two lists merge a dict,a list as key,other list as value
    :param list1:key
    :param list2:value
    :return:dict
    '''
    dic = dict(map(lambda x, y: [x, y], list1, list2))
    return dic