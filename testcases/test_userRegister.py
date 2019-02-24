#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/24 21:26
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :test_userRegister.py
# Software  :PyCharm Community Edition
import unittest
import suds
from libext.ddt import ddt,data
from common import mylog
from common.mcode import MCode
from common.do_testcase_excel import DoExcel
from common import contants
from common import context

logger = mylog.get_logger(logger_name="test_userRegister")
# print(testcases)


@ddt
class TestUserRegister(unittest.TestCase):
    excel = DoExcel(contants.case_file, "userRegister")
    testcases = excel.read_data()
    logger.info("读取userRegister所有测试用例成功")

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass
        # fake = Faker("zh_CN")
        # self.number=fake.phone_number()

    def tearDown(self):
        pass

    @data(*testcases)
    def test_userRegister(self, testcase):
        pass

