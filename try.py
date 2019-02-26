# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/20 23:02
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :studysuds.py
# Software  :PyCharm Community Edition
from suds.client import Client
from common.mysql import MysqlUtil
from faker import Faker


def getMcode(mobile):
    if type(mobile) == str and len(mobile) == 11:
        str1 = mobile[-2:]
        str2 = mobile[-3]
        sql = "select Fverify_code from sms_db_" + str1 + ".t_mvcode_info_" + str2 + \
              " where Fmobile_no=" + mobile + " GROUP BY Fsend_time DESC"
        print(sql)

        A = MysqlUtil()
        res = str(A.fetchone(sql))
        A.close_database()
    else:
        res = None
    return res


fake = Faker("zh_CN")
mobile = "17751810779"
print(mobile)

sendMCode_url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
client01 = Client(sendMCode_url)
t = {'mobile': mobile, 'tmpl_id': 1, 'client_ip': '47.107.168.87'}
client01.service.sendMCode(t)

code = getMcode(mobile)
print(mobile, code)


userRegister_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
client02 = Client(userRegister_url)
t = {"channel_id": "1", "ip": "129.45.6.7", "mobile": mobile, "pwd": "453173", "user_id": "abc1231",
     "verify_code": code}
result = client02.service.userRegister(t)
print(result)

