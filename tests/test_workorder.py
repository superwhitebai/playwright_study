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
        """测试登录后点击工单系统按钮并验证跳转成功"""
        # 1. 复用登录状态（通过 conftest.py 中的 context 加载 state.json）
        # 无需重复登录，直接访问登录后的首页（或应用面板页）
        login_page.goto_login()  # 此时已通过 storage_state 保持登录状态

        # 2. 初始化工单系统页面对象
        workorder_page = WorkorderPage(page)

        # 3. 点击工单系统按钮
        with allure.step("点击工单系统按钮"):
            workorder_page.click_workorder_btn()

        # 4. 验证跳转成功
        with allure.step("验证进入工单系统页面"):
            assert workorder_page.is_workorder_page(), "未成功进入工单系统页面"