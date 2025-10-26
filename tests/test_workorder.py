#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:39
# @Author  : 地核桃
# @file: test_workorder.py.py
# @desc:

# tests/test_workorder.py
import allure
import pytest
from pages.workorder_page import WorkorderPage

@allure.feature("工单系统模块")
class TestWorkorder:
    @allure.story("登录后进入工单系统")  # 使用allure装饰器标记测试故事为"登录后进入工单系统"
    def test_enter_workorder_after_login(self, page, login_page):  # 定义测试方法，接收page和login_page参数
        login_page.goto_login()  # 执行登录操作
        workorder_page = WorkorderPage(page)  # 创建工单页面对象实例

        with allure.step("点击工单系统按钮（打开新页面）"):  # 使用allure标记测试步骤
            workorder_page.click_workorder_btn()  # 先打开新页面

        with allure.step("刷新新页面"):
            workorder_page.refresh_new_page_twice() # 刷新新页面两次

        with allure.step("点击新页面中的我的工单"):
            workorder_page.click_my_workorder_btn()  # 再点击新页面中的按钮

        with allure.step("点击新页面中的“我发起的”"):
            workorder_page.click_my_initiated_btn() # 验证新页面中是否出现待我处理文本

        with allure.step("点击创建工单"):
            workorder_page.click_create_workorder_btn() # 点击创建工单

        # 测试用例中调用该方法
        with allure.step("选择协同问题：0625二次"):
            workorder_page.click_0625_secondary()

        with allure.step("点击确定按钮"):
            workorder_page.click_confirm_but()

        with allure.step('点击接收人'):
            workorder_page.fill_workorder_details(
                receiver="地核桃",
                description="这是测试说明内容"
            )




        # 验证结果（示例）
        # assert workorder_page.new_page.locator("text=待我处理").is_visible()