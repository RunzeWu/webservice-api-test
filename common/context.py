# -*- coding:utf-8 _*-
import re
import random
from faker import Faker
from common.config import ReadConfig

config = ReadConfig()
fake = Faker("zh_CN")


class Context:  # 上下文，数据的准备和记录
    mobile = fake.phone_number()
    verify_code = ""
    uid = ""
    cre_id = fake.ssn()
    user_name = true_name = fake.name()
    user_id = true_name + str(random.randint(0, 10)) + " By夜雨声烦"
    cardid = "6212264301007"+ str(random.randint(100000,999999)) # 银行卡格式
    uid = ""




# s 是目标字符串
# d 是替换的内容
# 找到目标字符串里面的标识符KEY，去d里面拿到替换的值
# 替换到s 里面去，然后再返回
def replace(s):
    p = "\$\{(.*?)}"
    while re.search(p, s):
        m = re.search(p, s)
        # print(m)
        key = m.group(1)
        print(key)
        mobile = fake.phone_number()
        value = mobile
        # print(value)
        s = re.sub(p, value, s, count=1)
    return s


def replace_new(s):
    p = "\$\{(.*?)}"
    while re.search(p, s):
        m = re.search(p, s)
        key = m.group(1)
        if hasattr(Context, key):
            value = getattr(Context, key)  # 利用反射动态的获取属性
            s = re.sub(p, value, s, count=1)
            name = fake.name()
            if key == "mobile":
                setattr(Context, key, fake.phone_number())
            elif key == "true_name" or key == "user_name":
                setattr(Context, key, name)
            elif key == "user_id":
                setattr(Context, key, name + str(random.randint(0, 10)) + " By夜雨声烦")
            elif key == "cre_id":
                setattr(Context, key, fake.ssn())
            elif key == "cardid":
                setattr(Context, key,"6212264301007"+ str(random.randint(100000,999999)))
        else:
            return None  # 或者抛出一个异常，告知没有这个属性
    return s


if __name__ == '__main__':
    # s = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
    s1 = '{"uid":"${uid}","true_name":"${true_name}","user_id":"${user_id}","cre_id":"${cre_id}"}'
    s2 = '{"channel_id": "1", "ip": "129.45.6.7", "mobile": "${mobile}",' \
         ' "pwd": "453173", "user_id": "${user_id}", "verify_code": "${verify_code}"}'
    s3 = "{'uid': '${uid}', 'user_name': '${user_name}', 'cre_id': '${cre_id}', 'bank_type': 1001, " \
         "'mobile': '${mobile}', 'cardid': '${cardid}', 'pay_pwd': '453173', 'bank_name': '招商银行'}"

    s = replace_new(s3)
    print(s)
