# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/6 16:52
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :mylog.py
# Software  :PyCharm Community Edition
import logging
import logging.handlers
from common.config import ReadConfig
from common import contants

config = ReadConfig()


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel('DEBUG') # 直接设置为最低
    # 定义输出格式
    fmt = config.get_value("log", "formatter")
    formate = logging.Formatter(fmt)

    file_handler = logging.handlers.RotatingFileHandler(contants.logs_log, maxBytes=20 * 1024 * 1024, backupCount=10, encoding="utf-8")
    level = config.get_value('log', 'file_handler')
    file_handler.setLevel(level)
    file_handler.setFormatter(formate)

    console_handler = logging.StreamHandler()
    level = config.get_value('log', 'console_handler')
    console_handler.setLevel(level)
    console_handler.setFormatter(formate)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    logger = get_logger(logger_name="invest")
    logger.info("****************")
    logger.debug("----------------")
    logger.warning("+++++++++++++++")
    logger.error("////////////////")
    logger.critical("/*-/*-/-*/*-*/")
