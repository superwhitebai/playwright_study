#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/11/17 19:26
# @Author  : 地核桃
# @file: work_configuration.py
# @desc:
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class Work_Configuration(BasePage):
    _workorder_btn = "text=工单系统"

    _workorder_title = "text=工单实体配置管理tab"
    _workorder_btnn = "text=工单实体配置管理"
    _workorder_add_btn = "div.base-tool-right button:has-text('工单实体配置')"
    _workorder_add_btnn = "div:has-text('问题分类') + div .ant-select-selection-search-input"



    def __init__(self, page: Page):
        super().__init__(page)
        self.new_page = None

    def click_workorder_title(self):
        """点击工单配置，打开新页面并保存新页面对象"""
        with self.page.expect_popup() as popup_info:
            self.click(self._workorder_btn)
        self.new_page = popup_info.value
        self.new_page.wait_for_load_state("networkidle")

    def click_word_workorder_btn(self):
        """点击“工单配置”tab"""
        self._check_new_page()
        with allure.step("点击新页面中的“我的工作”"):
            my_work_locator = self.new_page.locator(self._workorder_title)
            my_work_locator.wait_for(state="visible", timeout=15000)
            my_work_locator.click()

    def refresh_new_page_twice(self):
        self.new_page.wait_for_timeout(3000)
        self.new_page.reload(wait_until="networkidle")


    def click_my_initiated_btn(self):
        """点击“工单配置”按钮"""
        self._check_new_page()
        with allure.step("点击“工单配置”按钮"):
            # 等待“我发起的”标签
            initiated_locator = self.new_page.locator(self._workorder_btnn)
            initiated_locator.wait_for(state="visible", timeout=15000)
            initiated_locator.click()

    def click_my_configuration_btn(self):
        """点击“我发起的”标签"""
        self._check_new_page()
        with allure.step("点击新页面中的“我发起的”"):
            # 等待“我发起的”标签
            initiated_locator = self.new_page.locator(self._workorder_add_btn)
            initiated_locator.wait_for(state="visible", timeout=15000)
            initiated_locator.click()

    def click_my_initiated_btnnn(self):
        """点击“工单配置”按钮"""
        self._check_new_page()
        with allure.step("点击“工单配置”按钮"):
            # 等待“我发起的”标签
            initiated_locator = self.new_page.locator(self._workorder_add_btnn)
            initiated_locator.wait_for(state="visible", timeout=15000)
            initiated_locator.click()


    def _check_new_page(self):
        """检查新页面是否已打开且未关闭"""
        if not self.new_page:  # 新页面未初始化（未打开）
            raise Exception("新页面未打开，请先调用 click_workorder_btn() 打开新页面")
        if self.new_page.is_closed():  # 新页面已被关闭
            raise Exception("新页面已关闭，无法执行操作")
