#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, os
from elasticsearch import Elasticsearch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = '/data/ftproot/scan_project/pool_scan_tasks'
report_dir = '/data/ftproot/scan_report/output_report'
reports = ['ops_report', 'app_report']
indexs = ['app_reportv2_data_07_*', 'ops_reportv2_data_07_*']


def get_cmd_result(cmd):
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = [d for d in res.stdout.read().strip().split(b'\n') if d.split()]
    error = res.stderr.read()
    if error:
        print("error: ", error)
    return data


def execue_cmd(cmd):
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.stderr.read().split():
        print(b"error: ", res.stderr.read())
        print(cmd)
    return res.stdout.read(), res.stderr.read()


def get_ip_dirname():
    cmd = "find %s -type d -name host" % data_dir
    data = get_cmd_result(cmd)
    result = {}
    for d in data:
        dir = d.decode()
        cmd = "cd '%s' && ls|grep html" % dir
        iphtmls = get_cmd_result(cmd)
        for iphtml in iphtmls:
            iphtml = iphtml.decode()
            ip = iphtml.rstrip('.html')
            result[ip] = dir + "/" + iphtml
    return result


def copy_hostreport():
    es = Elasticsearch(["10.12.70.42"])
    result = get_ip_dirname()
    with open('ErrorResult.log', "w") as f:
        for ip in result:
            body = {
                "size": 500,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": ip,
                                    "fields": ["_id"]
                                }
                            }, {
                                "exists": {
                                    "field": "hight"
                                }
                            }
                        ]
                    }
                }
            }
            data = []
            for index in indexs:
                if index.startswith("app"):
                    pkg_dir = 'pkg_app_report'
                elif index.startswith("ops"):
                    pkg_dir = 'pkg_ops_report'
                res = es.search(index=index, body=body)
                if res['hits']['hits']:
                    data.append((pkg_dir, res['hits']['hits']))
            if not data:
                f.write("扫描报告中的IP:%s 在CMDB信息中找不到!\n" % ip)
            for pkg_dir, res in data:
                for r in res:
                    dirpath = "./%s/%s" % (pkg_dir, r['_source']['appname'].replace('/', '_'))
                    if not os.path.exists(dirpath):
                        os.mkdir(dirpath)
                        cmd = "\cp -r resources/host '%s/'" % dirpath
                        print(cmd)
                        execue_cmd(cmd)
                    cmd = "\cp '%s' '%s/host/'" % (result[ip], dirpath)
                    execue_cmd(cmd)
    print("copy_hostreport compled")


def copy_appreport():
    with open(BASE_DIR + '/aspscan.log', 'a+') as f:
        for report in reports:
            base_appdir = "%s/%s" % (report_dir, report)
            cmd = 'ls %s' % base_appdir
            result = get_cmd_result(cmd)
            for r in result:
                if report == 'ops_report':
                    appdir = 'pkg_ops_report/' + r.decode().rstrip('.xls')
                if report == 'app_report':
                    appdir = 'pkg_app_report/' + r.decode().rstrip('.xls')
                if not os.path.exists(appdir) and not os.path.isfile(appdir):
                    f.write(r.decode() + ' 不存在')
                    continue
                cmd = "\cp '%s/%s' '%s'" % (base_appdir, r.decode(), appdir)
                execue_cmd(cmd)
            print("copy %s compled" % (report))


def zip_report():
    with open(BASE_DIR + '/aspscan.log', 'w') as f:
        for report in reports:
            src_dir = '/opt/aspire/script/scan_project/pkg_%s' % report
            dest_dir = '%s/pkg_%s' % (report_dir, report)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            os.chdir(src_dir)
            cmd = 'ls'
            result = get_cmd_result(cmd)
            for r in result:
                appname = r.decode()
                cmd = "zip -qr '%s/%s.zip' '%s'" % (dest_dir, appname, appname)
                f.write(cmd + "\n")
                execue_cmd(cmd)
            print("zip %s compled" % report)


def main():
    copy_hostreport()
    copy_appreport()
    zip_report()


if __name__ == '__main__':
    print("Starting Perform...")
    main()
    print("completed over!")
