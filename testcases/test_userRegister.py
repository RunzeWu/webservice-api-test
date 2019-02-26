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
        id = value["id"]
        param = eval(context.replace_new(value["data"]))
        mobile = param["mobile"]

        # 先发验证码
        if re.match(r"^1[356789]\d{9}$", mobile):
            self.MCodeParam["mobile"] = mobile
            print(mobile)
            MCode().sendMCode(self.MCodeParam)
            m_code = str(MCode().getMcode(mobile))

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

        try:
            sql = "select * FROM user_db.t_user_info WHERE Fuser_id = '" + param["user_id"]+"'"
            print(sql)
            result = self.mysql.fetchone(sql)
        except:
            result = None

        try:
            self.assertEqual(int(res.retCode), value["expect"])
            if str(res.retCode) == "0":
                try:
                    self.assertIsNot(result,None,"数据库中数据不存在数据！！")
                    self.excel.write_data(id + 1, 7, str(res.retCode))
                    self.excel.write_data(id + 1, 8, "PASS")
                except AssertionError as e:
                    self.excel.write_data(id + 1, 7, res.retCode)
                    self.excel.write_data(id + 1, 8, "Failed")
                    raise e
            else:
                try:
                    self.assertIs(result,None,"数据库中数据不存在数据！！")
                    self.excel.write_data(id + 1, 7, str(res.retCode))
                    self.excel.write_data(id + 1, 8, "PASS")
                except AssertionError as e:
                    self.excel.write_data(id + 1, 7, res.retCode)
                    self.excel.write_data(id + 1, 8, "Failed")
                    raise e

        except AssertionError as e:
            self.excel.write_data(id + 1, 7, res.retCode)
            self.excel.write_data(id + 1, 8, "Failed")
            raise e




