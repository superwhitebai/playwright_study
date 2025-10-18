#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:38
# @Author  : 地核桃
# @file: workorder_page.py.py
# @desc:
# pages/workorder_page.py
from playwright.sync_api import Page
from playwright_study.pages.base_page import BasePage

class WorkorderPage(BasePage):
    # 工单系统按钮定位符（根据实际元素调整，此处为 class 定位）
    _workorder_btn = ".ant-image-img"  # 你的元素定位：class="ant-image-img"
    # 可添加工单系统页面的其他元素（如页面标题，用于验证跳转成功）
    _workorder_title = "text=工单系统"  # 假设跳转后有此标题

    def __init__(self, page: Page):
        super().__init__(page)

    def click_workorder_btn(self):
        """点击工单系统按钮"""
        self.click(self._workorder_btn)
        # 等待页面跳转完成（根据实际情况调整等待条件）
        self.wait_for_selector(self._workorder_title)

    def is_workorder_page(self):
        """验证是否进入工单系统页面"""
        return self.get_text(self._workorder_title) == "工单系统"