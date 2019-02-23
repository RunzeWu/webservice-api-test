#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/20 13:08
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :mysql.py
# Software  :PyCharm Community Edition
import pymysql
from common.config import ReadConfig


class MysqlUtil:

    def __init__(self, return_dict=False):

        # 数据库参数修改请到配置文件下
        self.database = pymysql.connect(
            host=ReadConfig().get_value("mysql-conf", "host"),  # 如果是服务器，则输公网ip
            user=ReadConfig().get_value("mysql-conf", "user"),  # 当时设置的数据超级管理员账户
            passwd=ReadConfig().get_value("mysql-conf", "password"),  # 当时设置的管理员密码
            port=ReadConfig().get_int("mysql-conf", "port"),  # MySQL数据的端口为3306，注意:切记这里不要写引号''
            # database=ReadConfig().get_value("mysql-conf", "database")  # 当时
        )
        if return_dict:
            self.cursor = self.database.cursor(pymysql.cursors.DictCursor)  # 指定每行数据以字典的形式返回
        else:
            self.cursor = self.database.cursor()  # 获取一个游标 — 也就是开辟一个缓冲区，用于存放sql语句执行的结果

    def close_database(self):
        self.cursor.close()
        self.database.close()

    def fetchone(self, sql):
        # 执行SQL
        self.cursor.execute(sql)
        # 获取结果
        result = self.cursor.fetchone()
        return result[0]  # 返回结果

    def fetch_all(self, sql):
        # 执行SQL
        self.cursor.execute(sql)
        # 获取结果
        results = self.cursor.fetchall()  # 返回列表 [(),()]
        return results


if __name__ == '__main__':
    A = MysqlUtil()
    sql = "select Fverify_code from sms_db_79.t_mvcode_info_7 where Fmobile_no='17751810779' GROUP BY Fsend_time DESC;"
    res = A.fetchone(sql)
    print(type(res))
    print(res)