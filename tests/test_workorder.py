#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:39
# @Author  : 地核桃
# @file: test_workorder.py.py
# @desc:

# tests/test_workorder.py
import allure
import pytest
from playwright_study.pages.workorder_page import WorkorderPage

@allure.feature("工单系统模块")
class TestWorkorder:
    @allure.story("登录后进入工单系统")
    def test_enter_workorder_after_login(self, page, login_page):
        login_page.goto_login()
        workorder_page = WorkorderPage(page)

        with allure.step("点击工单系统按钮（打开新页面）"):
            workorder_page.click_workorder_btn()  # 先打开新页面

        with allure.step("点击新页面中的我的工单"):
            workorder_page.click_my_workorder_btn()  # 再点击新页面中的按钮

        # 验证结果（示例）
        assert workorder_page.new_page.locator("text=待我处理").is_visible()