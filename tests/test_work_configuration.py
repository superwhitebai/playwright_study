#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/11/17 19:23
# @Author  : 地核桃
# @file: test_work_configuration.py
# @desc:

import sys
import os

# 获取项目根目录（当前文件在tests目录下，需回退一级）
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
import time
import allure
from pages.workorder_page import WorkorderPage
from utils.logger_utils import get_logger
from pages.work_configuration import Work_Configuration
logger = get_logger("ui")
@allure.feature("工单系统模块配置")
class Testworkconfiguration:

    @allure.story("登录后进入工单系统")
    def test_enter_workorder_after_login(self, page, login_page):

        logger.info("========【工单用例】登录后进入工单系统 开始执行 ========")

        with allure.step("打开登录页并登录"):
            login_page.goto_login()
            logger.info("已打开登录页")
            # 如果 login_page 里已经封装了登录，这里可以顺便调一下并记录日志
            # login_page.login_xxx(...)
            logger.info("登录成功，准备进入工单系统")

        # 创建工单页面对象
        workorder_page = Work_Configuration(page)
        logger.info("Work_Configuration 对象创建完成")

        with allure.step("点击工单系统按钮（打开新页面）"):
            logger.info("点击【工单系统】按钮，等待新页面出现")
            workorder_page.click_workorder_title()

        with allure.step("刷新新页面"):
            logger.info("开始刷新新页面两次")
            workorder_page.refresh_new_page_twice()
            logger.info("新页面刷新完成")

        with allure.step("点击新页面中的【我的工单】"):
            workorder_page.click_my_initiated_btn()
            logger.info("已点击【我的工单】按钮")

        with allure.step("点击新页面中的【我发起的】"):
            workorder_page.click_my_configuration_btn()
            logger.info("已点击【我发起的】按钮，并检查是否出现待处理文本")

        with allure.step("点击新页面中的【我发起的】"):
            workorder_page.click_my_initiated_btnnn()
            logger.info("已点击【我发起的】按钮，并检查是否出现待处理文本")