#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/28 22:20
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :test_bindBankCard.py
# Software  :PyCharm Community Edition
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

logger = mylog.get_logger(logger_name="test_bindBankCard")

@ddt
class TestBindBankCard(unittest.TestCase):
    excel = DoExcel(contants.case_file, "bindBankCard")
    testcases = excel.read_data()
    logger.info("读取bindBankCard所有测试用例成功")

    @classmethod
    def setUpClass(cls):
        cls.mysql = MysqlUtil()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()

    def setUp(self):
        self.MCode_data = eval(
            context.replace_new('{"mobile": "${mobile}", "tmpl_id": 1, "client_ip": "47.107.168.87"}'))
        self.mobile = self.MCode_data["mobile"]
        self.userRegister_data = eval(context.replace_new('{"channel_id": "1", "ip": "129.45.6.7",'
                                                          ' "mobile": "${mobile}", "pwd": "453173", '
                                                          '"user_id": "${user_id}", "verify_code": "${verify_code}"}'))

        self.verifyUserAuth_data = eval(context.replace_new('{"uid": "${uid}", "true_name": "${true_name}",'
                                                            ' "cre_id": "${cre_id}"}'))
        self.userRegister_data["mobile"] = mobile

        self.client01 = Client(
            ReadConfig().get_value("env-api", "pre_url") + "sms-service-war-1.0/ws/smsFacade.ws?wsdl")
        self.client01.service.sendMCode(self.MCode_data)

        self.userRegister_data["verify_code"] = MCode().getMcode(mobile)
        url = ReadConfig().get_value("env-api", "pre_url") + "finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
        client = Client(url)
        client.service.userRegister(self.userRegister_data)

        self.verifyUserAuth_data["uid"] = self.uid = db_select.getuid(self.userRegister_data["user_id"])
        self.true_name = self.verifyUserAuth_data["true_name"]

    def tearDown(self):
        pass

    @data(*testcases)
    def test_bindBankCard(self, value):
        url = ReadConfig().get_value("env-api", "pre_url") + value["url"]
        client = Client(url)
        # client.service.userRegister(self.userRegister_data)
        print(self.verifyUserAuth_data)
        res = client.service.verifyUserAuth(self.verifyUserAuth_data)
        # 以上代码跑通
        # 以下对绑定银行卡设计用例

        data = eval(context.replace_new(value["data"]))

        user_name = self.userRegister_data["true_name"]
        mobile = self.mobile
        # cardid =





