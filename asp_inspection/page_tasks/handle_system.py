#!/user/bin/env python
# -*- coding:utf-8 -*-

from utils.merge_cell import merge_cell, list_dic


def handle_system_inspection_index(workbook, index):
    apply_dic = []
    sheet_info = workbook.sheet_by_name(index)  # 根据表名获取表中的所有内容，sheet_info也是列表，列表中的值是每个单元格里值
    first_line = sheet_info.row_values(0)  # 获取首行，我这里的首行是表头，用表头作为字典的key，每一行数据对应表头的value，每一行组成一个字典
    # 将表头名称转换成标准对接格式的key，first_line类型为List
    first_line_list = []
    first_title = ""
    # print(first_line)
    for title in first_line:
        if title == '检查分组':
            first_title = "check_subitem"
        elif title == '序号':
            first_title = "aspnode_index"
        elif title == '优先级分组':
            first_title = "priority_group"
        elif title == '指标名':
            first_title = "index_name"
        elif title == '运算符':
            first_title = "operator"
        elif title == '正常阈值':
            first_title = "normal_threshold"
        elif title == '大类':
            first_title = "equipment_category"
        elif title == '是否执行':
            first_title = "grouping_status"
        else:
            first_title = ""
        first_line_list.append(first_title)

    values_merge_cell = merge_cell(sheet_info)  # 这里是调用处理合并单元格的函数
    for i in range(1, sheet_info.nrows):  # 开始为组成字典准备数据
        other_line = sheet_info.row_values(i)
        for key in values_merge_cell.keys():
            if key[0] == i:
                other_line[key[1]] = values_merge_cell[key]
        # dic = list_dic(first_line, other_line)  # 调用组合字典的函数，传入key和value，字典生成
        dic = list_dic(first_line_list, other_line)  # 调用组合字典的函数，传入key和value，字典生成
        apply_dic.append(dic)

    # 去空值、合并log数据、输出至excel
    apply_dic_len = len(apply_dic)
    for i in range(apply_dic_len):
        apply_dic[i].pop('')
    return apply_dic
