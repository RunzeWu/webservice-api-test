# -*- coding:utf-8 _*-
import re
import random
from faker import Faker
from common.config import ReadConfig

config = ReadConfig()
fake = Faker("zh_CN")


class Context:  # 上下文，数据的准备和记录
    # admin_user = config.get_value('data', 'admin_user')
    # admin_pwd = config.get_value('data', 'admin_pwd')
    # loan_member_id = config.get_value('data','loan_member_id')
    # normal_user = config.get_value('data', 'normal_user')
    # normal_pwd = config.get_value('data', 'normal_pwd')
    # normal_member_id = config.get_value('data', 'normal_member_id')
    mobile = fake.phone_number()
    verify_code = ""
    user_id = fake.name() + str(random.randint(0, 10)) + " By夜雨声烦"

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
    p="\$\{(.*?)}"
    while re.search(p, s):
        m = re.search(p, s)
        key = m.group(1)
        # print(key)
        if hasattr(Context, key):
            value = getattr(Context, key)  # 利用反射动态的获取属性
            s = re.sub(p, value, s, count=1)
            if key == "mobile":
                setattr(Context, key, fake.phone_number())
            if key == "user_id":
                setattr(Context, key, fake.name() + str(random.randint(0, 10)) + " By夜雨声烦")
        else:
            return None  # 或者抛出一个异常，告知没有这个属性
    return s


if __name__ == '__main__':

    # s = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
    s1 = '{"ip":"129.45.6.7","mobile":"${mobile}","pwd":"123456","channel_id":"2","user_id":"${user_id}","verify_code":"${verify_code}"}'

    # data = {"admin_user": "15873171553", "admin_pwd": "123456"}
    #
    # s = replace(s, data)
    # print(s)
    for i in range(8):
        s = replace_new(s1)
        print(s)
