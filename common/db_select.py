#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/1 13:48
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : db_select.py
# @Software : PyCharm
from common import mysql


def getuid(user_id):
    A = mysql.MysqlUtil()
    sql = "select Fuid FROM user_db.t_user_info where Fuser_id = '" + user_id + "'"
    res = str(A.fetchone(sql))
    A.close_database()
    return res


def get_max_Fpk_id():
    A = mysql.MysqlUtil()
    sql = "select MAX(Fpk_id) AS max_id FROM user_db.t_user_auth_info"
    res = A.fetchone(sql)
    A.close_database()
    return res
