#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/24 21:26
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :test_userRegister.py
# Software  :PyCharm Community Edition
import unittest
import re
import time
import faker
from suds.client import Client
from libext.ddt import ddt, data
from common import mylog
from common.mcode import MCode
from common.do_testcase_excel import DoExcel
from common import contants
from common import context
from common.mysql import MysqlUtil
from common.config import ReadConfig

logger = mylog.get_logger(logger_name="test_userRegister")
# print(testcases)


@ddt
class TestUserRegister(unittest.TestCase):
    excel = DoExcel(contants.case_file, "userRegister")
    testcases = excel.read_data()
    logger.info("读取userRegister所有测试用例成功")

    @classmethod
    def setUpClass(cls):
        cls.mysql = MysqlUtil()

        cls.MCodeParam = {'mobile': '${mobile}', 'tmpl_id': 1, 'client_ip': '47.107.168.87'}

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()

    def setUp(self):
        # fake = faker.Faker("zh_CN")
        pass
        # print(self.user_id)


    def tearDown(self):
        pass

    @data(*testcases)
    def test_userRegister(self, value):
        # print(value["data"], type(value["data"]))

        param = eval(context.replace_new(value["data"]))
        mobile = param["mobile"]


        # 先发验证码
        if re.match(r"^1[356789]\d{9}$", mobile):
            self.MCodeParam["mobile"] = mobile
            print(mobile)
            MCode().sendMCode(self.MCodeParam)
            m_code = str(MCode().getMcode(mobile))
            if value["title"] == "验证码不正确":
                m_code = m_code.join("4")
            elif value["title"] == "验证码为空":
                m_code = ""
            print(mobile)
            print(m_code)
        else:
            m_code = ""

        param["verify_code"] = m_code

        if value["title"] == "验证码超时":
            time.sleep(30)

        client = Client(ReadConfig().get_value("env-api", "pre_url")+value["url"])

        res = client.service.userRegister(param)
        print(res)



