#!/user/bin/env python
# -*- coding:utf-8 -*-
from apps.handle_ums_result import handle_result_byIndexName
from common.handle_merge_item import hendle_merge_normal, hendle_merge_json


def merge_ums_excel_data(ums_datas, item_datas):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_datas: 处理后的ums日志数据
    :param item_datas: 处理后的对应页的巡检数据
    :return: List[dict]
    """
    # 在此之前处理好结果状态aspnode_result
    # 结果状态对巡检指标的检查分组与指标运算符一对多的情况做适配,修改umglog的输出状态
    ums_datas = handle_result_byIndexName(ums_datas, item_datas)

    data_list = []
    for ums_data in ums_datas:
        index_list = ums_data['index_list']
        ip = ums_data['ip']
        for item_data in item_datas:
            data = {}
            for ums_item in index_list:
                if item_data['aspnode_index'] == int(ums_item['aspnode_index']) and ums_item['aspnode_type'] == 'normal':
                    print("匹配到的序号：", item_data['aspnode_index'])
                    data = hendle_merge_normal(data, item_data, ums_item, ip,poolname='')
                elif item_data['aspnode_index'] == int(ums_item['aspnode_index']) and ums_item['aspnode_type'] == 'json':
                    aspnode_index = item_data['aspnode_index']
                    print("匹配到的序号：", aspnode_index)
                    data = hendle_merge_json(data, aspnode_index, item_data, ums_item, ip , poolname='')
                else:
                    pass
                    # print("未匹配到的序号：", item_data['aspnode_index'])
            if data:
                data_list.append(data)
    data_merge_list = []
    for item in data_list:
        if isinstance(item, list):
            for i in item:
                data_merge_list.append(i)
        else:
            data_merge_list.append(item)
    return data_merge_list