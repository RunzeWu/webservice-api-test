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


# 需要faker模块，请pip install faker

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


def getuid(user_id):
    sql = "select Fuid FROM user_db.t_user_info where Fuser_id = '" + user_id + "'"
    A = MysqlUtil()
    res = str(A.fetchone(sql))
    A.close_database()
    return res


fake = Faker("zh_CN")
mobile = fake.phone_number()
print(mobile)

# 发验证码
sendMCode_url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
client01 = Client(sendMCode_url)
t = {'mobile': mobile, 'tmpl_id': 1, 'client_ip': '47.107.168.87'}
client01.service.sendMCode(t)

code = getMcode(mobile)
print(mobile, code)

# 注册
user_id = fake.name()

userRegister_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
client02 = Client(userRegister_url)
print(client02)
t = {"channel_id": "1", "ip": "129.45.6.7", "mobile": mobile, "pwd": "453173", "user_id": user_id,
     "verify_code": code}
result = client02.service.userRegister(t)
print(result)

# 实名认证
true_name = user_id
cre_id = fake.ssn()
uid = getuid(user_id)

print(true_name, cre_id, uid)
client03 = Client(userRegister_url)

t1 = {"uid": uid, "true_name": true_name, "cre_id": cre_id}

result = client03.service.verifyUserAuth(t1)
print(result)

# 绑定银行卡
cardid = str(fake.credit_card_number(card_type=None))
bankname = "招商银行"

t2 = {"uid": uid, "bank_name": "招商银行", "pay_pwd": "453173", "mobile": mobile, "cre_id": cre_id,
      "user_name": true_name, "cardid": "6212264301007974189x", "bank_type": 1001}
print(t2)

res = client03.service.bindBankCard(t2)
print(res)
