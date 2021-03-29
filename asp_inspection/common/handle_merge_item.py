#!/user/bin/env python
# -*- coding:utf-8 -*-


def hendle_merge_normal(data, item_data, ums_item, ip, poolname):
    """
    数据组装相同内容进行封装
    取出两个字典的值存入新字典中
    将空值暂设为空
    :param data:初始化的字典
    :param item_data: 巡检项的值
    :param ums_item: ums中的数据
    :param ip: ums文件中的主机ip
    :return:
    """
    data['poolname'] = poolname
    data['business_system'] = ''
    data['equipment_category'] = ''
    data['equipment_subclass'] = ''
    data['hostname'] = ''
    data['ip'] = ip
    data['check_subitem'] = item_data['check_subitem']
    # data['aspnode_index'] = item_data['aspnode_index']
    # data['aspnode_type'] = ums_item['aspnode_type']
    data['grouping_status'] = item_data['grouping_status']

    # 指标运算符 = 运算符+阈值operator+normal_threshold
    operator = str(item_data['operator'])
    normal_threshold = str(item_data['normal_threshold'])
    if "正则" in operator:
        lens = len(normal_threshold)
        normal_threshold = normal_threshold[1:lens - 1]

    if operator == "人工判断":
        data['operator'] = normal_threshold
    else:
        data['operator'] = operator + normal_threshold

    data['index_name'] = item_data['inspection_item']
    # 子项，指标名非Json格式取表，Json时取result_name
    data['child_item'] = item_data['child_item']

    data['priority_group'] = item_data['priority_group']

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
    exception_rule = handel_exception_rule(item_data)

    data['exception_rule'] = exception_rule + str(item_data['normal_threshold'])
    data['aspnode_msg'] = ums_item['aspnode_msg']
    data['aspnode_index'] = item_data['aspnode_index']
    return data


def hendle_merge_json(data, aspnode_index, item_data, ums_item, ip, poolname):
    """
    取出两个字典的值存入新字典中
    将空值暂设为空
    :param data: 定义的一个空字典
    :param aspnode_index: 序号，用于数据间的关联
    :param item_data: 巡检项的数据信息
    :param ums_item: ums日志数据信息
    :return: 合并后的marge_data
    """
    # item_data为一个标准的字典
    # 对ums_item进行处理，取出msg中内容，装入简单的dict中，再于item_data进行合并
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
        # result['result_desc'] = result_item[' result_desc']

        # 需要对system_data处理后进行合并
        item_data_change = {}
        item_data_change['poolname'] = poolname
        item_data_change['business_system'] = ''
        item_data_change['equipment_category'] = ''
        item_data_change['equipment_subclass'] = ''
        item_data_change['hostname'] = ''
        item_data_change['ip'] = ip
        item_data_change['check_subitem'] = item_data['check_subitem']
        item_data_change['grouping_status'] = item_data['grouping_status']
        item_data_change['inspection_item'] = item_data['inspection_item']
        # 指标运算符 = 运算符+阈值operator+normal_threshold
        operator = str(item_data['operator'])
        normal_threshold = str(item_data['normal_threshold'])
        if "正则" in operator:
            lens = len(normal_threshold)
            normal_threshold = normal_threshold[1:lens - 1]

        if operator == "人工判断":
            item_data_change['operator'] = "人工判断"
        else:
            item_data_change['operator'] = operator + normal_threshold

        # 巡检项，指标名非Json格式取表，Json时取result_name
        item_data_change['index_name'] = item_data['inspection_item']
        item_data_change['priority_group'] = item_data['priority_group']

        # 异常规则，运算符+阈值 运算符进行改变，改成相反的运算符
        exception_rule = handel_exception_rule(item_data)

        item_data_change['exception_rule'] = exception_rule + str(item_data['normal_threshold'])

        # 合并操作
        if result['aspnode_index'] == item_data['aspnode_index']:
            merge_dict = dict(result, **item_data_change)
            # 改变字典中的排位
            merge_dict_change = change_dict_index(merge_dict)
        merge_dict_list.append(merge_dict_change)
    return merge_dict_list


def handel_exception_rule(item_data):
    """
    异常规则，运算符+阈值 运算符进行改变，改成相反的运算符
    :param item_data: 系统巡检指标数据
    :return: 转换后的系统规则数据
    """
    exception_rule = item_data['operator']
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
    elif exception_rule == "正则":
        exception_rule = "不匹配"
    elif exception_rule == "人工判断":
        exception_rule = ""
    elif exception_rule == "正则表达式不匹配":
        exception_rule = "正则表达式匹配"
    else:
        exception_rule = exception_rule
    return exception_rule


def change_dict_index(marge_dict):
    data = {}
    data['poolname'] = marge_dict['poolname']
    data['business_system'] = marge_dict['business_system']
    data['equipment_category'] = marge_dict['equipment_category']
    data['equipment_subclass'] = marge_dict['equipment_subclass']
    data['hostname'] = marge_dict['hostname']
    data['ip'] = marge_dict['ip']
    data['check_subitem'] = marge_dict['check_subitem']
    data['grouping_status'] = marge_dict['grouping_status']
    data['operator'] = marge_dict['operator']
    data['inspection_item'] = marge_dict['inspection_item']
    data['child_item'] = marge_dict['result_name']
    data['priority_group'] = marge_dict['priority_group']
    data['aspnode_result'] = marge_dict['result_status']
    data['exception_rule'] = marge_dict['exception_rule']
    data['aspnode_msg'] = marge_dict['result_value']
    data['aspnode_index'] = marge_dict['aspnode_index']
    return data
