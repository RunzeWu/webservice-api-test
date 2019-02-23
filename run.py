#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/23 20:01
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :run.py
# Software  :PyCharm Community Edition
import unittest
from libext import HTMLTestRunnerNew
from common import contants

# 自动查找testcases目录下，以test开头的.py文件里面的测试类
discover = unittest.defaultTestLoader.discover(contants.testcases_dir, pattern="test_*.py", top_level_dir=None)

with open(contants.reports_html, "wb+") as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title="webservice接口测试报告",
                                              description="description",tester="夜雨声烦")
    runner.run(discover)