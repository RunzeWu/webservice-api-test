#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/2/27 10:16
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_verifiedUserAuth.py
# @Software : PyCharm
import unittest
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
from common import db_select

logger = mylog.get_logger(logger_name="test_verifyUserAuth")


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


    def setUp(self):
        self.before_max_fpk_id = db_select.get_max_Fpk_id()

    @data(*testcases)
    def test_userRegister(self, value):
        userRegister_param = eval(context.replace_new(self.userRegister_data))
        register_mobile = userRegister_param["mobile"]

        # 发短信数据准备
        self.MCodeParam["mobile"] = register_mobile

        MCode().sendMCode(self.MCodeParam)

        # 注册数据准备

        user_id = userRegister_param["user_id"]
        userRegister_param["verify_code"] = MCode().getMcode(register_mobile)

        url = ReadConfig().get_value("env-api", "pre_url") + value["url"]
        client = Client(url)
        client.service.userRegister(userRegister_param)

        # 以上代码能跑通

        id = value["id"]
        title = value["title"]

        verifyuserauth_param = eval(context.replace_new(value["data"]))

        if title != "不注册直接认证(uid不存在)" and title != "uid为空":
            verifyuserauth_param["uid"] = db_select.getuid(user_id)

        true_name = getattr(Context, "true_name")

        if title != "用户姓名为空":
            verifyuserauth_param["true_name"] = true_name

        expect = str(value["expect"])

        logger.info(verifyuserauth_param)

        res = client.service.verifyUserAuth(verifyuserauth_param)
        logger.info(res)
        res.retCode = str(res.retCode)

        after_max_fpk_id = db_select.get_max_Fpk_id()

        try:
            self.assertEqual(expect, res.retCode)
            logger.info("判断校验码成功")
            if res.retCode == "0":
                try:
                    self.assertEqual(self.before_max_fpk_id, after_max_fpk_id - 1)
                    logger.info("验库成功")
                except AssertionError as e:
                    logger.error("验库失败")
                    self.excel.write_data(id + 1, 7, res.retCode)
                    self.excel.write_data(id + 1, 8, "Failed")
                    raise e
            else:
                try:
                    self.assertEqual(self.before_max_fpk_id, after_max_fpk_id)
                    logger.info("验库成功")
                except AssertionError as e:
                    self.excel.write_data(id + 1, 7, res.retCode)
                    self.excel.write_data(id + 1, 8, "Failed")
                    logger.error("验库失败")
                    raise e
            self.excel.write_data(id + 1, 7, res.retCode)
            self.excel.write_data(id + 1, 8, "Pass")
        except AssertionError as e:
            logger.error("校验码失败")
            self.excel.write_data(id + 1, 7, res.retCode)
            self.excel.write_data(id + 1, 8, "Failed")
            raise e
