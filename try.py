#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/20 23:02
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :studysuds.py
# Software  :PyCharm Community Edition
from suds.client import Client
from common.mysql import MysqlUtil
import time
import suds


def getMcode(mobile):
    if type(mobile) == str and len(mobile) == 11:
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

sendMCode_url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
client=Client(sendMCode_url)
t={'mobile': 13251026000, 'tmpl_id': 1, 'client_ip': '47.107.168.87'}#用字典的方式传值
# try:
result=client.service.sendMCode(t)

code = int(getMcode("13251026000"))
# time.sleep(31)
print(code)
print(type(code))
# except suds.WebFault as e:
#     print(e)
#     print(type(e.fault))
# print(result)
# print(type(result))



userRegister_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
client=Client(userRegister_url)#Client里面直接放访问的URL，可以生成一个webservice对象

# print(client)#打印所webservice里面的所有接口方法名称，结果如下截图所示：
t={"channel_id":2,"ip":"129.45.6.7","mobile":13251026000 ,"pwd":None,"user_id" :"夜雨声烦","verify_code":str(code)}#用字典的方式传值
# data = {"ip":"129.45.6.7","mobile":"13251027555","pwd":"123456","channel_id":"2","user_id":"夜雨声烦","verify_code":""}
result=client.service.userRegister(t)
#client这个对象 ，调用service这个方法，然后再调用userRegister这个接口函数，函数里面传递刚刚我们准备
#好的得参数字典 t
print(result)#打印返回结果