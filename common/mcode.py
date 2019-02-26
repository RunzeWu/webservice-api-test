# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/23 20:01
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :mcode.py
# Software  :PyCharm Community Edition
from suds.client import Client
from common.mysql import MysqlUtil
from common.config import ReadConfig


class MCode:
    def __init__(self):
        self.url = ReadConfig().get_value("env-api", "pre_url")+"sms-service-war-1.0/ws/smsFacade.ws?wsdl"
        self.client = Client(url=self.url)

    def sendMCode(self, params):
        '''
        :param mobile:
        :return: dict {retcode:"";retInfo:""}
        '''

        result = self.client.service.sendMCode(params)
        # print(result)
        return result

    def getMcode(self, mobile):
        if type(mobile) == str and len(mobile)==11:
            str1 = mobile[-2:]
            str2 = mobile[-3]
            sql = "select Fverify_code from sms_db_" + str1 + ".t_mvcode_info_" + str2 + \
                  " where Fmobile_no=" + mobile + " GROUP BY Fsend_time DESC"
            print(sql)

            A = MysqlUtil()
            res = A.fetchone(sql)
            A.close_database()
        else:
            res = None
        return res


if __name__ == '__main__':
    a = MCode()
    res = a.sendMCode("17751810770")
    # res = a.getMcode("17751810779")
    print(res)
