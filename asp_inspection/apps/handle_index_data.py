#!/user/bin/env python
# -*- coding:utf-8 -*-


class FilterDict():
    def __init__(self, initial_list):
        self.initial_list = initial_list

    def run(self):
        filter_set = self.filter_inspection_item()
        # print("------", self.integration_method(filter_set))
        return self.integration_method(filter_set)

    # 按inspection_item字段分类
    def filter_inspection_item(self):
        inspection_item_set = set()
        for i in self.initial_list:
            inspection_item_set.add(i["inspection_item"])
        # print("相同的巡检项：", inspection_item_set)
        return inspection_item_set

    # 整合
    def integration_method(self, filter_set):
        newList = []
        for name in filter_set:
            aspnode_index = []
            for dict in self.initial_list:
                index = dict["aspnode_index"]
                inspection_item = dict["inspection_item"]
                item_operator = dict["item_operator"]
                if dict["inspection_item"] == name:
                    aspnode_index.append(index)
                    newDict = {"aspnode_index": list(set(aspnode_index)),
                               "inspection_item": inspection_item,
                               "item_operator": item_operator}
            newList.append(newDict)
        return newList