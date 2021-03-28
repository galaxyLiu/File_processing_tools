#!/user/bin/env python
# -*- coding:utf-8 -*-

from common.handle_merge_item import hendle_merge_normal, hendle_merge_json


def merge_ums_excel_data(ums_datas, system_data):
    """
    合并数据，将数据存入excel表中，存入表中需要的数据格式
    :param ums_data: 处理后的ums日志数据
    :param system_data: 处理后的巡检数据
    :return: List[dict]
    """
    data_list = []
    for ums_data in ums_datas:
        index_list = ums_data['index_list']
        ip = ums_data['ip']
        for system_item in system_data:
            data = {}
            for ums_item in index_list:
                if system_item['aspnode_index'] == int(ums_item['aspnode_index']) and ums_item['aspnode_type'] == 'normal':
                    print("匹配到的序号：",system_item['aspnode_index'])
                    data = hendle_merge_normal(data, system_item, ums_item, ip,poolname='')
                elif system_item['aspnode_index'] == int(ums_item['aspnode_index']) and ums_item['aspnode_type'] == 'json':
                    aspnode_index = system_item['aspnode_index']
                    print("匹配到的序号：",aspnode_index)
                    data = hendle_merge_json(data, aspnode_index, system_item, ums_item, ip , poolname='')
                else:
                    pass
                    # print("未匹配到的序号：", system_item['aspnode_index'])

            if data:
                data_list.append(data)
    # print("data_list", data_list)
    data_merge_list = []
    for item in data_list:
        if isinstance(item, list):
            for i in item:
                data_merge_list.append(i)
        else:
            data_merge_list.append(item)
    return data_merge_list