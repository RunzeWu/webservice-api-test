#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/2/27 10:16
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_verifiedUserAuth.py
# @Software : PyCharm
import unittest
import re
from suds.client import Client
from libext.ddt import ddt, data
from common import mylog
from common.mcode import MCode
from common.do_testcase_excel import DoExcel
from common import contants
from common import context
from common.context import Context
from common.mysql import MysqlUtil
from common.config import ReadConfig

logger = mylog.get_logger(logger_name="test_verifyUserAuth")


# print(testcases)


@ddt
class TestUserRegister(unittest.TestCase):
    excel = DoExcel(contants.case_file, "verifyUserAuth")
    testcases = excel.read_data()
    logger.info("读取verifyUserAuth所有测试用例成功")

    @classmethod
    def setUpClass(cls):
        cls.mysql = MysqlUtil()

        cls.MCodeParam = {'mobile': '${mobile}', 'tmpl_id': 1, 'client_ip': '47.107.168.87'}
        cls.userRegister_data = '{"channel_id": "1", "ip": "129.45.6.7", "mobile": "${mobile}", ' \
                                '"pwd": "453173", "user_id": "${user_id}", "verify_code": "${verify_code}"}'


    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()

    def getuid(self, user_id):
        sql = "select Fuid FROM user_db.t_user_info where Fuser_id = '" + user_id + "'"
        A = MysqlUtil()
        res = str(A.fetchone(sql))
        A.close_database()
        return res

    @data(*testcases)
    def test_userRegister(self, value):
        print(type(context.replace_new(self.userRegister_data)))
        userRegister_param = eval(context.replace_new(self.userRegister_data))
        register_mobile = userRegister_param["mobile"]

        # 发短信数据准备
        self.MCodeParam["mobile"] = register_mobile

        MCode().sendMCode(self.MCodeParam)


        # 注册数据准备

        user_id = userRegister_param["user_id"]
        userRegister_param["verify_code"] = MCode().getMcode(register_mobile)

        url = ReadConfig().get_value("env-api", "pre_url")+value["url"]
        client = Client(url)
        res = client.service.userRegister(userRegister_param)
        print(userRegister_param, res)

        # 以上代码能跑通

        uid = self.getuid(user_id)

        id = value["id"]
        title = value["title"]
        verifyUserAuth_param = eval(context.replace_new(value["data"]))
        verifyUserAuth_param["uid"] = uid
        true_name = getattr(Context, "true_name")
        verifyUserAuth_param["true_name"] = true_name

        expect = value["expect"]

        print(verifyUserAuth_param)

        res = client.service.verifyUserAuth(verifyUserAuth_param)
        print(res)

        # 注册

        # 实名验证
