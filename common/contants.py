#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/8 16:01
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : contants.py
# @Software : PyCharm Community Edition
import os
import time
# from common.config import ReadConfig

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根路径
# print(base_dir)
data_dir = os.path.join(base_dir, "data")  # datas文件夹路径

case_file = os.path.join(data_dir, "webservice-testdata.xlsx")  # user_test.xlsx文件路径
# receiver_file = os.path.join(data_dir, "receivers.xlsx")  # receivers.xlsx文件路径
# print(case_file)

conf_dir = os.path.join(base_dir, "conf")

test_env_conf = os.path.join(conf_dir, "test_env.conf")  # 测试环境配置文件路径
prod_env_conf = os.path.join(conf_dir, "prod_env.conf")  # 生产环境配置文件路径
global_conf = os.path.join(conf_dir, "global.conf")  # 测试配置文件路径

logs_dir = os.path.join(base_dir, "logs")
log_time = time.strftime('%Y-%m-%d')
logs_log = os.path.join(logs_dir, log_time + ".log")

testcases_dir = os.path.join(base_dir, "testcases")

reports_dir = os.path.join(base_dir, 'reports')  # reports文件夹路径
reports_html = os.path.join(reports_dir, 'api test_report.html')  # reports文件夹路径

# class FilePath:
#
#     def __init__(self):
#         self.dir_path = os.path.dirname(os.path.dirname(__file__))
#
#     def global_conf_path(self):
#         path = os.path.join(self.dir_path, "conf", "global.conf")
#         return path
#
#     def prod_conf_path(self):
#         path = os.path.join(self.dir_path, "conf", "prod_env.conf")
#         return path
#
#     def test_conf_path(self):
#         path = os.path.join(self.dir_path, "conf", "test_env.conf")
#         return path
#
#     def test_data_data(self):
#         path = os.path.join(self.dir_path, "datas", "user_test.xlsx")
#         return path
#
#     def receivers(self):
#         path = os.path.join(self.dir_path, "datas", "receivers.xlsx")
#         return path
#
#     def report_path(self):
#         # report_time = time.strftime("%Y-%m-%d-%H-%M-%S")
#         # report_name = report_time + " api test_report.html"
#         report_name = "api test_report.html"
#         path = os.path.join(self.dir_path, "reports", report_name)
#         # path = ReadConfig(self.conf_path()).get_value("report","file_path")+report_name
#         return path
#
#     def log_path(self):
#         log_time = time.strftime('%Y-%m-%d')
#         path = os.path.join(self.dir_path, "logs", log_time + ".log")
#         return path
