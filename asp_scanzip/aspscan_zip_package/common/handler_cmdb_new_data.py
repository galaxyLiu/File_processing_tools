#! /usr/bin/env python
# -*- coding:utf-8 -*-

POOLNAME = {
    '信息港资源池': 'xxg',
    '哈尔滨资源池': 'hachi',
    '呼和浩特资源池': 'huchi',
    '业支域非池化': 'feichihua',
    '南方基地': 'nanji',
    '深圳池外':'szcw'
}


# 处理cmdb数据，将需要的cmdb字段的数据存入es中
def handle_cmdb_new_data(sheet, id, name, index_prefix, doc_type):
    data = []
    for rownum in range(1, sheet.nrows):
        rowdata = sheet.row_values(rownum)
        if not rowdata[0].strip():
            print("index %s row %s is null." % (id, rownum))
            continue
        poolname = POOLNAME.get(rowdata[22].strip(), '正在核实业务系统')
        appname = str(rowdata[12]).strip()
        action = {
            "_id": str(rowdata[20]).strip(),
            "_index": index_prefix + poolname,
            "_type": doc_type,
            "_source": {
                "appname": appname if appname else '正在核实业务系统',
                "department_2": str(rowdata[5]).strip(),  # 所属部门
                "device_classify": str(rowdata[11]).strip(),  # 设备分类
                "mai_manufacturer": str(rowdata[32]).strip(),  # 维保厂家
                "device_name": str(rowdata[2]).strip(),  # 设备名称
                "gm_ip": str(rowdata[20]).strip(),
                "poolname": poolname,
                "sheetname": name,
                "nrow": rownum + 1,
                "sheetindex": id
            }
        }
        data.append(action)
        if len(data) == 2000:
            yield data
            data = []
    yield data
