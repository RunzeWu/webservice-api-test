#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/23 21:12
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :test_sendMCode.py
# Software  :PyCharm Community Edition
import unittest
import suds
from libext.ddt import ddt,data
from common import mylog
from common.mcode import MCode
from common.do_testcase_excel import DoExcel
from common import contants
from common import context

logger = mylog.get_logger(logger_name="test_sendMCode")
# print(testcases)


@ddt
class TestSendMcode(unittest.TestCase):
    excel = DoExcel(contants.case_file, "sendMCode")
    testcases = excel.read_data()
    logger.info("读取sendMCode所有测试用例成功")

    @classmethod
    def setUpClass(cls):
        cls.mcode = MCode()


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
    def test_sendMCode(self, testcase):
        id = testcase["id"]
        # title = testcase["title"]
        param = testcase["data"]
        expect = testcase["expect"]

        param = eval(context.replace(param))
        try:
            res = MCode().sendMCode(param)
            logger.info("请求发送成功")
            retCode = res.retCode
        except suds.WebFault as e:
            logger.error("系统错误")
            fault = e.fault
            print(e.fault)
            faultstring = str(fault["faultstring"])
            # print(faultstring)
            self.assertEqual(faultstring, expect,"系统报错信息不一致")
            self.excel.write_data(id + 1, 7, faultstring)
            self.excel.write_data(id + 1, 8, "PASS")
            res=None

        if res is not None:
            try:
                # logger.info(type(expect),type(retCode))
                self.assertEqual(expect, eval(retCode))
                # self.assertRaises()
                self.excel.write_data(id + 1, 7, retCode)
                self.excel.write_data(id + 1, 8, "PASS")
            except AssertionError as e:
                logger.error("*****断言失败*****")
                self.excel.write_data(id + 1, 7, retCode)
                self.excel.write_data(id + 1, 8, "Failed")
                raise e
        else:
            pass


if __name__ == '__main__':
    unittest.main()