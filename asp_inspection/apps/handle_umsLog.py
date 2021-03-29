#!/user/bin/env python
# -*- coding:utf-8 -*-

import os
from config.dev import umsLog_name


def path_name(path):
    """
    将路径中所有文件进行处理
    :param path: ums日志文件路径,日志文件命名格式ip_umslog
    :return:组装好的数据字典 {'ip':xxx,index_list:[{},{}...]}
    """
    result_list = []
    datanames = os.listdir(path)
    # 获取到所有umslog文件
    for log_name in datanames:
        data = {}
        # 获取到Ip
        ip = log_name.split("_")[0]

        data['ip'] = ip
        data['index_list'] = []
        file_path = path + "/" + log_name
        # 获取到每个日志文件的内容
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            # 将每组数据进行组装，按键值对形式存储起来
            content = file_obj.read()
            # print(content)
            iter_data = iter(content.split("\n"))
            for line in iter_data:
                # 获取到文本中所有的内容
                line = line.strip()
                if line.startswith('#'):
                    for line in iter_data:
                        d = {}
                        if 'aspnode_index' in line:
                            aspnode_index = line.split("=")[1]
                            d['aspnode_index'] = aspnode_index
                        elif 'aspnode_type' in line:
                            aspnode_type = line.split("=")[1].replace('"', "")
                            d['aspnode_type'] = aspnode_type
                        elif 'aspnode_result' in line:
                            d['aspnode_result'] = line.split("=")[1]
                        elif 'aspnode_desc' in line:
                            d['aspnode_desc'] = line[13:].replace('"', "")
                        # 根据aspnode_type对msg进行不同取值
                        elif 'aspnode_msg' in line and aspnode_type == "json":
                            aspnode_msg = line.split("=")[1].replace('"', "")
                            d['aspnode_msg'] = []
                            # 处理整条数据
                            str_list = aspnode_msg.split("},")

                            for list in str_list:
                                data_item = {}
                                str_a = list.split(",")
                                for item in str_a:
                                    item = item.replace("[{", "")
                                    item = item.replace("}]", "")
                                    item = item.replace("{", "")
                                    item = item.replace("}", "")
                                    item = item.split(":")
                                    name = item[0]
                                    value = item[1]
                                    data_item[name] = value
                                d['aspnode_msg'].append(data_item)

                        elif 'aspnode_msg' in line:
                            aspnode_msg = line.split("=")[1].replace('"', "")
                            d['aspnode_msg'] = aspnode_msg
                        data['index_list'].append(d)
                elif not line:
                    continue
                else:
                    break
            result_list.append(data)
    for item in result_list:
        # 对列表进行拆分再组合
        list_cuts = cut_list(item['index_list'], 5)
        a_data = data_assembly(list_cuts)
        item['index_list'] = a_data
    return result_list


def cut_list(index_lists, cut_len):
    """
    将列表拆分为指定长度的多个列表
    :param index_lists: 初始列表
    :param cut_len: 每个列表的长度
    :return: 一个二维数组 [[x,x],[x,x]]
    """
    res_data = []
    # 去空值
    lists = []
    for list_dex in index_lists:
        # print(list_dex)
        if bool(list_dex):
            lists.append(list_dex)
    # 切割
    if len(lists) > cut_len:
        for i in range(int(len(lists) / cut_len)):
            cut_a = lists[cut_len * i:cut_len * (i + 1)]
            res_data.append(cut_a)
        last_data = lists[int(len(lists) / cut_len) * cut_len:]
        if last_data:
            res_data.append(last_data)
    else:
        res_data.append(lists)
    return res_data


def data_assembly(lists):
    """
    将切分好的列表进行封装
    [{"a":"a"},{"b":"b"},{"c":"c"}]->[{"a":"a","b":"b","c":"c"}]
    :param lists: ums的中按序列切割的数据
    :return: index_list[]
    """
    result = []
    for list in lists:
        merge_dict = {}
        for i in list:
            merge_dict.update(i)
        result.append(merge_dict)
    return result


def handle_umslog(sheet_name):
    ums_path = umsLog_name + sheet_name
    # 判断路径是否存在，可能存在文件路径命名错误问题
    print(ums_path)
    print(os.path.exists(ums_path))
    if os.path.exists(ums_path):
        umsLog_data = path_name(ums_path)
        return umsLog_data
    else:
        print(">>>>请查看配置文件中sheet_name_list定义是否与umslog中子文件命名一致！！！")
