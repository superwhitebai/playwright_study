#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:38
# @Author  : 地核桃
# @file: workorder_page.py.py
# @desc:
# pages/workorder_page.py
import allure
from playwright.sync_api import Page
from playwright_study.pages.base_page import BasePage

class WorkorderPage(BasePage):
    # 工单系统按钮定位符（根据实际元素调整，此处为 class 定位）
    _workorder_btn = "text=工单系统"  # 你的元素定位：class="ant-image-img"
    # 可添加工单系统页面的其他元素（如页面标题，用于验证跳转成功）
    _workorder_title = "text=工单系统"  # 假设跳转后有此标题
    _workorde_my_work = "text=我的工作"

    def click_workorder_btn(self):
        """点击工单按钮，打开新页面并保存新页面对象"""
        with self.page.expect_popup() as popup_info:
            self.click(self._workorder_btn)
        self.new_page = popup_info.value  # 保存新页面对象到实例变量
        self.new_page.wait_for_load_state("networkidle")  # 等待新页面加载

    # 新增：点击新页面中的“我的工单”按钮
    def click_my_workorder_btn(self):
        """在新页面中点击“我的工单”"""
        if not hasattr(self, 'new_page'):
            raise Exception("未找到新页面，请先调用 click_workorder_btn() 打开新页面")
        self.new_page.click(self._workorde_my_work)  # 使用新页面对象操作
        self.new_page.wait_for_selector("text=待我处理")  # 等待跳转完成


    def is_workorder_page(self):
        """验证是否进入工单系统页面"""
        return self.get_text(self._workorder_title) == "工单系统"