#!/user/bin/env python
# -*- coding:utf-8 -*-

from apps.handle_index_data import FilterDict


def handle_result_byIndexName(ums_datas, item_datas):
    """
    根据item_datas中相同的巡检项取出序号，匹配umslog获取到结果状态，
    根据item_datas中的指标运算符确定umslog中的最终结果状态
    :param ums_datas: ums日志数据
    :param item_datas: 巡检指标数据
    :return:
    """
    new_list = filter_data(item_datas)
    filterObject = FilterDict(new_list)
    merge_index_datas = filterObject.run()
    # 获取到有相同巡检项的数据，根据指标项运算符调整umslog中的结果
    # 如果aspnode_index列表为1说明巡检项和序号一对一关系，列表长度大于一说明一对多关系
    for merge_index in merge_index_datas:
        len_index = len(merge_index['aspnode_index'])
        if len_index > 1:
            for ums_data in ums_datas:
                index_list = ums_data['index_list']
                item_operator = []
                aspnode_result = []
                for ums_item in index_list:
                    if int(ums_item['aspnode_index']) in merge_index['aspnode_index']:
                        # print("匹配到的序号：", ums_item['aspnode_index'])
                        # print(merge_index['item_operator'])
                        # print(ums_item['aspnode_result'])
                        # print(merge_index)
                        # print(ums_item)

                        item_operator.append(merge_index['item_operator'])
                        aspnode_result.append(ums_item['aspnode_result'])
                # print(item_operator)
                # print(aspnode_result)
                if aspnode_result:
                    if "与" in item_operator and '1' in aspnode_result:
                        # 所有的输出结果都改为1异常
                        for ums_item in index_list:
                            if int(ums_item['aspnode_index']) in merge_index['aspnode_index']:
                                ums_item['aspnode_result'] = '1'
                    elif "或" in item_operator and '0' in aspnode_result:
                        # 所有的输出结果都改为0正常
                        for ums_item in index_list:
                            if int(ums_item['aspnode_index']) in merge_index['aspnode_index']:
                                ums_item['aspnode_result'] = '0'
    return ums_datas


def filter_data(item_datas):
    # 循环列表拿到需要处理的值，巡检项、序号、运算符
    new_list = []
    for item_list in item_datas:
        dic = {}
        if item_list['aspnode_index']:
            dic['inspection_item'] = item_list['inspection_item']
            dic['item_operator'] = item_list['item_operator']
            dic['aspnode_index'] = int(item_list['aspnode_index'])
            new_list.append(dic)
    return new_list







