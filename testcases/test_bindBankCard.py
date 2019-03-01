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
        self.userRegister_data["mobile"] = self.mobile

        self.client01 = Client(
            ReadConfig().get_value("env-api", "pre_url") + "sms-service-war-1.0/ws/smsFacade.ws?wsdl")
        self.client01.service.sendMCode(self.MCode_data)

        self.userRegister_data["verify_code"] = MCode().getMcode(self.mobile)
        url = ReadConfig().get_value("env-api", "pre_url") + "finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
        self.client = Client(url)
        self.client.service.userRegister(self.userRegister_data)

        self.verifyUserAuth_data["uid"] = self.uid = db_select.getuid(self.userRegister_data["user_id"])
        self.true_name = self.verifyUserAuth_data["true_name"]

    def tearDown(self):
        pass

    @data(*testcases)
    def test_bindBankCard(self, value):
        url = ReadConfig().get_value("env-api", "pre_url") + value["url"]
        client = Client(url)
        # print(self.userRegister_data)
        # client.service.userRegister(self.userRegister_data)
        # print(self.verifyUserAuth_data)
        client.service.verifyUserAuth(self.verifyUserAuth_data)
        # 以上代码跑通
        # 以下对绑定银行卡设计用例

        data = eval(context.replace_new(value["data"]))

        data["uid"] = self.uid
        data["cre_id"] = self.verifyUserAuth_data["cre_id"]
        if value["title"] != "持卡人姓名为空":
            data['user_name'] = self.verifyUserAuth_data["true_name"]
        else:
            data['user_name'] = None

        if value["title"] == "证件id为空":
            data["cre_id"] = None
        if value["title"] == "uid为空":
            data["uid"] = None
        if value["title"] == "uid不存在":
            data["uid"] = "99999999"
        if value["title"] != "银行卡卡号格式不正确" and value["title"] != "银行卡卡号为空":
            data["cardid"] = "6212264301007974189"
        if value["title"] != "手机号码为空" and value["title"] != "手机号码格式不正确":
            data["mobile"] = self.mobile

        print(data)

        res = self.client.service.bindBankCard(data)
        print(res)
        actual = str(res.retCode)
        expect = str(value["expect"])
        id = value["id"]

        try:
            '''
            该接口有问题，所以数据校验没做
            如果做，比对id等字段 表：user_db_xx.t_bind_card_x
            按uid后三位分库分表，倒数2位代表user_db库，倒数第三位代表表的位置
            '''
            self.assertEqual(expect, actual)
            logger.info("状态码校验成功")
            self.excel.write_data(id + 1, 7, actual)
            self.excel.write_data(id + 1, 8, "PASS")
        except AssertionError as e:
            logger.error("数据校验失败")
            self.excel.write_data(id + 1, 7, actual)
            self.excel.write_data(id + 1, 8, "Failed")
            raise e







