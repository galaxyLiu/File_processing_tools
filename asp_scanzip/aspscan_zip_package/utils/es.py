#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import time
from os import walk
# import CSVOP
# from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticObj:
    def __init__(self, ip="127.0.0.1",timeout=100):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        # 无用户名密码状态
        self.es = Elasticsearch([ip])
        # 用户名密码状态
        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)

    def create_index(self, index_name="ott", index_type="ott_type"):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "date": {
                            "type": "text",
                            "index": True
                        },
                        "keyword": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "source": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "link": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print("res")

    def update_by_query(self, index, dock_type, doc):
        body = {
            "doc": doc
        }
        self.es.update_by_query(index=index, body=body, doc_type=dock_type)

    def IndexData(self):
        es = Elasticsearch()
        csvdir = 'D:/work/ElasticSearch/exportExcels'
        filenamelist = []
        for (dirpath, dirnames, filenames) in walk(csvdir):
            filenamelist.extend(filenames)
            break
        total = 0
        for file in filenamelist:
            csvfile = csvdir + '/' + file
            self.Index_Data_FromCSV(csvfile, es)
            total += 1
            print(total)
            time.sleep(10)

    # def Index_Data_FromCSV(self, csvfile):
    #     '''
    #     从CSV文件中读取数据，并存储到es中
    #     :param csvfile: csv文件，包括完整路径
    #     :return:
    #     '''
    #     list = CSVOP.ReadCSV(csvfile)
    #     index = 0
    #     doc = {}
    #     for item in list:
    #         if index > 1:  # 第一行是标题
    #             doc['title'] = item[0]
    #             doc['link'] = item[1]
    #             doc['date'] = item[2]
    #             doc['source'] = item[3]
    #             doc['keyword'] = item[4]
    #             res = self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)
    #             print(res['created'])
    #         index += 1
    #         print
    #         index



    def bulk_Data(self, data):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        # success, _ = bulk(self.es, data, index=index, raise_on_error=True)
        success, _ = bulk(self.es, data, raise_on_error=True)
        print('Performed %d actions .' % success)

    def bulk_Index_Data(self, index, data):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        # success, _ = bulk(self.es, data, index=index, raise_on_error=True)
        success, _ = bulk(self.es, data, index=index, raise_on_error=True)
        print('Performed %d actions .' % success)




