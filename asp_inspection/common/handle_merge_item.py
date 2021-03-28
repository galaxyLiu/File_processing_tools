#!/user/bin/env python
# -*- coding:utf-8 -*-


def hendle_merge_normal(data, system_item, ums_item, ip, poolname):
    """
    数据组装相同内容进行封装
    取出两个字典的值存入新字典中
    将空值暂设为空
    :param data:
    :param system_item:
    :param ums_item:
    :param ip:
    :return:
    """
    data['poolname'] = poolname
    data['business_system'] = ''
    data['equipment_category'] = system_item['equipment_category']
    data['check_subitem'] = system_item['check_subitem']
    data['hostname'] = ''
    data['ip'] = ip
    # data['aspnode_index'] = system_item['aspnode_index']
    data['aspnode_type'] = ums_item['aspnode_type']
    data['grouping_status'] = system_item['grouping_status']
    # 指标运算符 = 运算符+阈值operator+normal_threshold
    data['operator'] = str(system_item['operator']) + str(system_item['normal_threshold'])
    # 巡检项，指标名非Json格式取表，Json时取result_name
    data['index_name'] = system_item['index_name']
    data['aspnode_desc'] = ums_item['aspnode_desc']
    data['priority_group'] = system_item['priority_group']
    # 结果状态
    aspnode_result = ums_item['aspnode_result']
    if aspnode_result == "0":
        aspnode_result = "正常"
    elif aspnode_result == "1":
        aspnode_result = "异常"
    elif aspnode_result == "2":
        aspnode_result = "人工判断"
    elif ums_item['aspnode_msg'] == "":
        aspnode_result = "无结果"
    data['aspnode_result'] = aspnode_result
    # 异常规则，运算符+阈值 运算符进行改变，改成相反的运算符
    exception_rule = handel_exception_rule(system_item)

    data['exception_rule'] = exception_rule + str(system_item['normal_threshold'])
    data['aspnode_msg'] = ums_item['aspnode_msg']

    return data


def hendle_merge_json(data, aspnode_index, system_item, ums_item, ip, poolname):
    """
    取出两个字典的值存入新字典中
    将空值暂设为空
    :param data: 定义的一个空字典
    :param aspnode_index: 序号，用于数据间的关联
    :param system_item: 系统数据信息
    :param ums_item: ums日志数据信息
    :return: 合并后的marge_data
    """
    # system_item为一个标准的字典
    # 对ums_item进行处理，取出msg中内容，装入简单的dict中，再于system_item进行合并
    aspnode_msg = ums_item['aspnode_msg']
    merge_dict_list = []
    for result_item in aspnode_msg:
        result = {}
        result['aspnode_index'] = aspnode_index
        result['aspnode_type'] = 'json'
        result['result_name'] = result_item[' result_name']
        # 结果状态
        aspnode_result = result_item[' result_status']
        if aspnode_result == "0":
            aspnode_result = "正常"
        elif aspnode_result == "1":
            aspnode_result = "异常"
        elif aspnode_result == "2":
            aspnode_result = "人工判断"
        elif ums_item['aspnode_msg'] == "":
            aspnode_result = "无结果"
        result['result_status'] = aspnode_result
        result['result_value'] = result_item[' result_value']
        result['result_desc'] = result_item[' result_desc']

        # 需要对system_data处理后进行合并
        system_item_change = {}
        system_item_change['poolname'] = poolname
        system_item_change['business_system'] = ''
        system_item_change['equipment_category'] = system_item['equipment_category']
        system_item_change['check_subitem'] = system_item['check_subitem']
        system_item_change['hostname'] = ''
        system_item_change['ip'] = ip
        system_item_change['grouping_status'] = system_item['grouping_status']
        # 指标运算符 = 运算符+阈值operator+normal_threshold
        system_item_change['operator'] = str(system_item['operator']) + str(system_item['normal_threshold'])
        # 巡检项，指标名非Json格式取表，Json时取result_name
        system_item_change['index_name'] = system_item['index_name']
        system_item_change['priority_group'] = system_item['priority_group']

        # 异常规则，运算符+阈值 运算符进行改变，改成相反的运算符
        exception_rule = handel_exception_rule(system_item)

        system_item_change['exception_rule'] = exception_rule + str(system_item['normal_threshold'])

        # 合并操作
        if result['aspnode_index'] == system_item['aspnode_index']:
            merge_dict = dict(result, **system_item_change)
            # 改变字典中的排位
            merge_dict_change = change_dict_index(merge_dict)
        merge_dict_list.append(merge_dict_change)
    return merge_dict_list


def handel_exception_rule(system_item):
    """
    异常规则，运算符+阈值 运算符进行改变，改成相反的运算符
    :param system_item: 系统巡检指标数据
    :return: 转换后的系统规则数据
    """
    exception_rule = system_item['operator']
    if exception_rule == "=":
        exception_rule = "!="
    elif exception_rule == "<=":
        exception_rule = ">"
    elif exception_rule == "<":
        exception_rule = ">="
    elif exception_rule == ">=":
        exception_rule = "<"
    elif exception_rule == ">":
        exception_rule = "<="
    elif exception_rule == "!=":
        exception_rule = "=="
    elif exception_rule == "包含":
        exception_rule = "不包含"
    else:
        exception_rule = exception_rule
    return exception_rule


def change_dict_index(marge_dict):
    data = {}
    data['poolname'] = marge_dict['poolname']
    data['business_system'] = marge_dict['business_system']
    data['equipment_category'] = marge_dict['equipment_category']
    data['check_subitem'] = marge_dict['check_subitem']
    data['hostname'] = marge_dict['hostname']
    data['ip'] = marge_dict['ip']
    data['aspnode_type'] = marge_dict['aspnode_type']
    data['grouping_status'] = marge_dict['grouping_status']
    data['operator'] = marge_dict['operator']
    data['index_name'] = marge_dict['result_name']
    data['aspnode_desc'] = marge_dict['result_desc']
    data['priority_group'] = marge_dict['priority_group']
    data['aspnode_result'] = marge_dict['result_status']
    data['exception_rule'] = marge_dict['exception_rule']
    data['aspnode_msg'] = marge_dict['result_value']
    return data
