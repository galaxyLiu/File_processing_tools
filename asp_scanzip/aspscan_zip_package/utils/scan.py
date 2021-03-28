#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, datetime
from bs4 import BeautifulSoup
from common.handler_data import get_name_method


class ScanObj:
    def __init__(self, url):
        self.base_url = url
        self.auth = ('admin', 'xsZjMbbcgSMHy39x3kpkP+YcFMQyYSRn6L67dSWntBM=')

    def get_data(self, url):
        try:
            resp = requests.get(url, auth=self.auth)
        except Exception as e:
            print("请求异常: %s" % str(e))
            return ''
        return resp.content

    def get_dirname(self, url):
        data = self.get_data(url)
        soup = BeautifulSoup(data, 'lxml')
        soup_as = soup.find_all("a")
        names = []
        for item in soup_as:
            value = item['href']
            if value.startswith(".."):
                continue
            names.append(value)
        return names

    def get_result(self, url, scan_id, task, poolname):
        result = []
        print(scan_id)
        print(url)
        soup = BeautifulSoup(self.get_data(url), 'lxml')
        report_content_1_1_body = soup.find_all("div", attrs={"class": "report_content"})[0]
        report_content_1_1_table = report_content_1_1_body.find_all("table", attrs={"class": "report_table plumb"})[2]
        td = report_content_1_1_table.find_all('td')[0]

        time = td.text.split('结束：')[1]
        if time:
            report_time = td.text.split('结束：')[1]
            print(report_time)
            date_time = datetime.datetime.strptime(report_time, '%Y-%m-%d %H:%M:%S')

        report_content_3_1_body = soup.find_all("div", attrs={"class": "report_content"})[2]
        report_content_3_1_table = report_content_3_1_body.find_all("table", attrs={"class": "report_table"})[0]
        trs = report_content_3_1_table.find_all("tbody")[0].find_all('tr')
        try:
            for tr in trs:
                data = {}
                tds = tr.find_all("td")
                data['scan_ip'] = tds[0].find_all("a")[0].string if tds[0].find_all('a') else tds[0].text
                data['hostname'] = tds[1].string if tds[1].string else ''
                data['os'] = tds[2].string
                data['hight'] = int(tds[3].string)
                data['center'] = int(tds[4].string)
                data['low'] = int(tds[5].string)
                data['total'] = int(tds[6].string)
                data['risk'] = float(tds[7].string)
                data['scan_id'] = scan_id
                data['task'] = task
                # data['subtask'] = subtask
                data['report_time'] = report_time.strip()
                data['report_utctime'] = int(date_time.timestamp())
                data['vlan'] = 'null'
                data['network'] = 'null'
                data['poolname'] = poolname.strip('/')
                if data['hight'] == 0 and data['center'] == 0:
                    continue
                result.append(data)
        except Exception as e:
            print("request error url: ", url)
            print("error:", str(e))
        return result

    def get_data_by_scanip(self, scan_url, poolname, scan_ip, risk_grade):
        data = {}
        data['scan_ip'] = scan_ip
        data['is_exist'] = 0
        data['poolname'] = poolname
        data['risk_grade'] = risk_grade
        data['device_classify'] = ""
        data['device_name'] = ""
        data['appname'] = ""
        data['department_2'] = ""
        data['mai_manufacturer'] = ""
        print("scan_ip:", scan_ip)
        print("scan_url:", scan_url)  # 去掉index.heml的url
        soup_scan = BeautifulSoup(self.get_data(scan_url), 'lxml')

        report_content_1_1_body = soup_scan.find_all("div", attrs={"class": "report_content"})[0]
        # print(report_content_1_1_body)
        report_content_1_1_table = report_content_1_1_body.find_all("table", attrs={"class": "report_table"})[1]
        # tr = report_content_1_1_table.find_all("tr", attrs={"class": "odd"})[2]
        if (len(report_content_1_1_table.find_all("tbody")[0].find_all('tr'))) == 5:
            tr = report_content_1_1_table.find_all("tbody")[0].find_all("tr")[4]
        else:
            tr = report_content_1_1_table.find_all("tbody")[0].find_all("tr")[5]
        # print(tr)
        # exit(1)
        td = tr.find_all('td')[0]
        # report_time_1 = td.text
        # report_time = report_time_1.strip()
        data['report_time'] = td.text.strip()  # 扫描时间
        # print("report_time", td.text.strip())

        report_content_2_body = soup_scan.find_all("div", attrs={"class": "report_content"})[1]
        report_content_2_table = report_content_2_body.find_all("table", attrs={"class": "report_table"})[1]
        # print(report_content_2_table)

        report_content_2_2_trs = report_content_2_table.find_all("tr", recursive=False)

        names = []
        methods = []
        data['vulnerability_name'] = []
        data['repair_method'] = []
        # data['vulnerability_grade'] = []

        if len(report_content_2_2_trs) % 2 != 0:
            print('数据异常!')
            exit(1)

        for name_node, method_node in get_name_method(report_content_2_2_trs):
            if 'vuln_low' in name_node.find_all('img')[1]['src']:
                continue

            name = name_node.find_all("span")[0].string
            names.append(name)

            report_content_2_2_table = method_node.find_all("table", attrs={"class": "report_table plumb"})[0]
            report_content_2_2_2_tr = report_content_2_2_table.find_all("tr")[1]
            method = report_content_2_2_2_tr.find_all("td")[0].text.replace(" ", "")
            methods.append(method)
        # print("name", name)
        iter_dict = zip(names, methods)
        for name, method in iter_dict:
            data['vulnerability_name'].append(name)
            data['repair_method'].append(method)
        return data

    def get_ruixue_result(self, url, poolname, split_url):
        # print("poolname:", poolname)
        result = []
        risk_grade = ""
        soup = BeautifulSoup(self.get_data(url), 'lxml')

        report_content_3_1_body = soup.find_all("div", attrs={"class": "report_content"})[2]
        report_content_3_1_table = report_content_3_1_body.find_all("table", attrs={"class": "report_table"})[0]
        trs = report_content_3_1_table.find_all("tbody")[0].find_all('tr')

        # try:
        for tr in trs:
            tds = tr.find_all("td")
            if '危险' not in tds[0].find_all("img")[0]['title']:
                continue

            if tds[0].find_all("img")[0]['title'] == "非常危险":
                risk_grade = "2"
            elif tds[0].find_all("img")[0]['title'] == "比较危险":
                risk_grade = "1"

            scan_ip = tds[0].find_all("a")[0].string if tds[0].find_all('a') else tds[0].text  # 得到页面单个Ip
            scan_url = split_url + "host/" + scan_ip + ".html"  # 每个ip的单个报告
            data = self.get_data_by_scanip(scan_url, poolname.strip('/'), scan_ip, risk_grade)
            result.append(data)

        return result
