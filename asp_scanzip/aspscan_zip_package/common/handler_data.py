#!/usr/bin/env python
# -*- coding: utf-8 -*-


POOLNAME = {
    '信息港资源池': 'xxg',
    '哈尔滨资源池': 'hachi',
    '呼和浩特资源池': 'huchi',
    '业支域非池化': 'feichihua',
    '南方基地': 'nanji',
    '深圳池外': 'szcw'
}


def get_xls_data(result):
    data = []
    for r in result:
        d = []
        d.append(r['report_time'])
        d.append(r['scan_ip'])
        d.append(r['poolname'])
        d.append(r['os'])
        d.append(r['hostname'])
        d.append(r['network'])
        d.append(r['vlan'])
        d.append(r['hight'])
        d.append(r['center'])
        d.append(r['low'])
        d.append(r['total'])
        d.append(r['risk'])
        data.append(d)
    return data


def get_scan_data(index, result):
    data = []
    for d in result:
        action = {
            "_index": index,
            "_type": 'data',
            "_id": d['scan_ip'],
            "_source": {
                "scan_ip": d['scan_ip'],
                "hostname": d['hostname'],
                "os": d['os'],
                "hight": int(d['hight']),
                "center": int(d['center']),
                "low": int(d['low']),
                "total": int(d['total']),
                "risk": float(d['risk']),
                "scan_id": d['scan_id'],
                "task": d['task'],
                # "subtask": d['subtask'],
                "report_time": d['report_time'],
                "report_utctime": d['report_utctime'],
                "vlan": d['vlan'],
                "network": d['network'],
                "poolname": d['poolname']
            }
        }
        data.append(action)
    return data


def get_cmdb_data(sheet, id, name, index_prefix, doc_type):
    data = []
    for rownum in range(1, sheet.nrows):
        rowdata = sheet.row_values(rownum)
        if not rowdata[0].strip():
            print("index %s row %s is null." % (id, rownum))
            continue
        poolname = POOLNAME.get(rowdata[22].strip(), '正在核实业务系统')
        appname = str(rowdata[12]).strip()
        action = {
            "_index": index_prefix + poolname,
            "_type": doc_type,
            "_id": str(rowdata[20]).strip(),
            "_source": {
                "gm_ip": str(rowdata[20]).strip(),
                "appname": appname if appname else '正在核实业务系统',
                "poolalias": str(rowdata[22]).strip(),
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


def get_cmdb_data_v1(sheet, id, name, index_prefix, doc_type):
    data = []
    for rownum in range(1, sheet.nrows):
        rowdata = sheet.row_values(rownum)
        if not rowdata[0].strip():
            print("index %s row %s is null." % (id, rownum))
            continue
        action = []
        if id == 0 or id == 1 or id == 3:
            poolname = POOLNAME.get(rowdata[6].strip(), '正在核实业务系统')
            appname = str(rowdata[11]).strip()
            action = {
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_id": str(rowdata[0]).strip(),
                "_source": {
                    "gm_ip": str(rowdata[0]).strip(),
                    "ipmi_ip": str(rowdata[3]).strip(),
                    "appname": appname if appname else '正在核实业务系统',
                    "poolalias": str(rowdata[6]).strip(),
                    "poolname": poolname,
                    "sheetname": name,
                    "nrow": rownum + 1,
                    "sheetindex": id
                }
            }
        if id == 2:
            poolname = POOLNAME.get(rowdata[3].strip(), '正在核实业务系统')
            appname = str(rowdata[8]).strip()
            action = {
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_id": str(rowdata[0]).strip(),
                "_source": {
                    "gm_ip": str(rowdata[0]).strip(),
                    "appname": appname if appname else '正在核实业务系统',
                    "poolalias": str(rowdata[3]).strip(),
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


def get_ops_cmdb_data(sheet, id, name, index_prefix, doc_type):
    data = []
    for rownum in range(1, sheet.nrows):
        rowdata = sheet.row_values(rownum)
        if not rowdata[0].strip():
            print("index %s row %s is null." % (id, rownum))
            continue
        if not str(rowdata[3]).strip():
            continue
        if id == 0 or id == 1 or id == 3:
            poolname = POOLNAME.get(rowdata[6].strip(), 'unknown')
            appname = str(rowdata[11]).strip()
            action = {
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_id": str(rowdata[3]).strip(),
                "_source": {
                    "gm_ip": str(rowdata[0]).strip(),
                    "ipmi_ip": str(rowdata[3]).strip(),
                    "appname": appname if appname else 'unknown',
                    "poolalias": str(rowdata[6]).strip(),
                    "poolname": poolname,
                    "sheetname": name,
                    "nrow": rownum + 1,
                    "sheetindex": id
                }
            }
        else:
            continue
        data.append(action)
        if len(data) == 2000:
            yield data
            data = []
    yield data


def get_report_data(result, index_prefix):
    doc = []
    for r in result:
        doc.append({"update": {"_index": index_prefix + r['poolname'], "_type": "data", "_id": r['scan_ip']}})
        doc.append({"doc": r})
    return doc


def get_cmdb_es_data(result, index_prefix):
    doc = []
    for r in result:
        doc.append({"update": {"_index": index_prefix + r['_source']['poolname'], "_type": "data", "_id": r['_id']}})
        r['_source']['is_exist'] = 1
        doc.append({"doc": r['_source']})
    return doc


def get_index_data(result):
    doc = []
    for r in result:
        doc.append({"index": {"_index": "report_data_%s" % r['poolname'], "_type": "data", "_id": r['scan_ip']}})
        doc.append(r)
    return doc


def scan_to_es_data(index, result):
    doc = []
    for r in result:
        doc.append({"index": {"_index": index + r['poolname'], "_type": "data", "_id": r['scan_ip']}})
        doc.append(r)
    return doc

def scan_qm_es_data(index, r):
    doc = []
    doc.append({"index": {"_index": index + r['poolname'], "_type": "data", "_id": r['scan_ip']}})
    doc.append(r)
    return doc

# 处理cmdb数据，将需要的cmdb字段的数据存入es中
def handle_cmdb_data_job1(sheet, id, name, index_prefix, doc_type):
    data = []
    for rownum in range(1, sheet.nrows):
        rowdata = sheet.row_values(rownum)
        if not rowdata[0].strip():
            print("index %s row %s is null." % (id, rownum))
            continue
        action = []
        if id == 0 or id == 3:  # 1/4表格
            poolname = POOLNAME.get(rowdata[6].strip(), 'unknown')
            appname = str(rowdata[11]).strip()
            action = {
                "_id": str(rowdata[0]).strip(),
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_source": {
                    "appname": appname if appname else 'unknown',
                    "department_2": str(rowdata[10]).strip(),  # 所属部门
                    "device_classify": str(rowdata[17]).strip(),  # 设备分类
                    "mai_manufacturer": str(rowdata[33]).strip(),  # 维保厂家
                    "device_name": str(rowdata[44]).strip(),  # 设备名称
                    "gm_ip": str(rowdata[0]).strip(),
                    "poolname": poolname,
                    "sheetname": name,
                    "nrow": rownum + 1,
                    "sheetindex": id
                }
            }
        if id == 1:  # 2表格
            poolname = POOLNAME.get(rowdata[6].strip(), 'unknown')
            appname = str(rowdata[11]).strip()
            action = {
                "_id": str(rowdata[0]).strip(),
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_source": {
                    "appname": appname if appname else 'unknown',
                    "department_2": str(rowdata[10]).strip(),  # 所属部门
                    "device_classify": str(rowdata[14]).strip(),  # 设备分类
                    "mai_manufacturer": str(rowdata[37]).strip(),  # 维保厂家
                    "device_name": str(rowdata[47]).strip(),  # 设备名称
                    "gm_ip": str(rowdata[0]).strip(),
                    "poolname": poolname,
                    "sheetname": name,
                    "nrow": rownum + 1,
                    "sheetindex": id
                }
            }
        if id == 2:  # 3表格
            poolname = POOLNAME.get(rowdata[3].strip(), 'unknown')
            appname = str(rowdata[8]).strip()
            action = {
                "_id": str(rowdata[0]).strip(),
                "_index": index_prefix + poolname,
                "_type": doc_type,
                "_source": {
                    "appname": appname if appname else 'unknown',
                    "department_2": str(rowdata[7]).strip(),  # 所属部门
                    "device_classify": str(rowdata[11]).strip(),  # 设备分类
                    "mai_manufacturer": str(rowdata[34]).strip(),  # 维保厂家
                    "device_name": str(rowdata[44]).strip(),  # 设备名称
                    "gm_ip": str(rowdata[0]).strip(),
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


def get_name_method(list_data):
    data = []
    for i in range(len(list_data)):
        if i % 2 == 1:
            data.append(list_data[i])
            yield data
            data = []
        else:
            data.append(list_data[i])


def get_port_name(list_data):
    data = []
    for i in range(len(list_data)):
        if i % 4 == 1:
            data.append(list_data[i])
            yield data
            data = []
        if i % 3 == 1:
            data.append(list_data[i])
            yield data
            data = []
        if i % 2 == 1:
            data.append(list_data[i])
            yield data
            data = []
        else:
            data.append(list_data[i])