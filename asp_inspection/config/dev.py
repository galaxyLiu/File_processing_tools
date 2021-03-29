#!/user/bin/env python
# -*- coding:utf-8 -*-

# sheet页名称，注sheet名称与umslog文件名称对应
# 在linux服务器可能出现中文编码不一致问题，建议不使用中文
sheet_name_list = ["系统", "基线", "交维", "全量"]
# 巡检指标汇总文件
file_name = r'data\UMS自动化项目进度跟踪.xlsx'
# umslog文件
umsLog_name = r'data\umslog'+'\\'
# 巡检文件生成路径
excel_name = r'data\output'+'\\'


# 文件头部文件获取字段
header_inspection_index = ['资源池', '业务系统', '设备大类', '设备小类', '主机名', 'IP', '检查分组', '检查分组状态',
                           '指标运算符', '巡检项', '子项', '优先级分组', '结果状态', '异常规则', '巡检值','序号（便于核查，可删除）']
