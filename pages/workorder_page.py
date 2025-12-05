#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:38
# @Author  : 地核桃
# @file: workorder_page.py.py
# @desc:根据登录态-创建工单

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage

class WorkorderPage(BasePage):



    _confirm_button = 'xpath=/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]'
    _0625_secondary = (
        'div:has-text("技术") '  
        '.menu-item span:has-text("0625二次")'
    )
    _description_textarea = (
        'textarea[class*="ant-input"]'  
        '[placeholder*="请输入"]'
    )
    _handler_select_container = 'div.ant-select:has(span.ant-select-selection-placeholder:has-text("不指定时会由小组成员自己认领"))'
    _handler_input = f'{_handler_select_container} input.ant-select-selection-search-input'
    _handler_options = f'{_handler_select_container} .ant-select-dropdown li'  # 下拉选项
    _handler_dropdown = "div.rc-select-dropdown:visible"
    _workorder_btn = "text=工单系统"  # 保持不变（文本定位稳定）
    _workorder_title = "text=工单系统"
    _my_work_btn = "text=我的工作"
    _my_initiated_tab = 'div[role="tab"]:has-text("我发起的")'
    _create_workorder_btn = "text=创建工单"
    _second_confirm_btn = (
        'div.ant-modal:has(text("处理人")) ' 
        'div.ant-modal-footer button.ant-btn-primary:has-text("确定")'
    )


    def __init__(self, page: Page):
        super().__init__(page)
        self.new_page = None

    def click_workorder_btn(self):
        """点击工单按钮，打开新页面并保存新页面对象"""
        with self.page.expect_popup() as popup_info:
            self.click(self._workorder_btn)
        self.new_page = popup_info.value
        self.new_page.wait_for_load_state("networkidle")

    # 新增：点击新页面中的“我的工单”按钮
    def click_my_workorder_btn(self):
        """点击“我的工作”按钮"""
        self._check_new_page()
        with allure.step("点击新页面中的“我的工作”"):
            my_work_locator = self.new_page.locator(self._my_work_btn)
            my_work_locator.wait_for(state="visible", timeout=15000)
            my_work_locator.click()


    def refresh_new_page_twice(self):
        self.new_page.wait_for_timeout(3000)
        self.new_page.reload(wait_until="networkidle")  #(刷新页面)

    def _check_new_page(self):
        """检查新页面是否已打开且未关闭"""
        if not self.new_page:  # 新页面未初始化（未打开）
            raise Exception("新页面未打开，请先调用 click_workorder_btn() 打开新页面")
        if self.new_page.is_closed():  # 新页面已被关闭
            raise Exception("新页面已关闭，无法执行操作")

    def click_my_initiated_btn(self):
        """点击“我发起的”标签"""
        self._check_new_page()
        with allure.step("点击新页面中的“我发起的”"):
            # 等待“我发起的”标签
            initiated_locator = self.new_page.locator(self._my_initiated_tab)
            initiated_locator.wait_for(state="visible", timeout=15000)
            initiated_locator.click()

    def click_create_workorder_btn(self):
        """点击新页面中的“创建工单”按钮"""
        self._check_new_page()  # 确保新页面已打开
        with allure.step("点击新页面中的“创建工单”按钮"):
            # 关键：使用self.new_page定位，且调用locator方法
            self.new_page.locator(self._create_workorder_btn).click()

    def click_0625_secondary(self):
        """点击技术分类下的“0625二次”"""
        self._check_new_page()
        with allure.step("点击技术分类下的“0625二次”"):
            locator = self._0625_secondary
            self.new_page.locator(locator).wait_for(state="visible", timeout=10000)
            self.new_page.locator(locator).click()


    def click_confirm_button(self):
        self._check_new_page()
        with allure.step("点击第一个确定按钮，等待窗口内容更新为处理人表单"):
            # 绝对XPath）
            confirm_locator = self.new_page.locator(self._confirm_button)
            confirm_locator.wait_for(state="visible", timeout=15000)  # 确保按钮存在
            confirm_locator.click(force=True)
            try:
                self.new_page.wait_for_selector(
                    "text=处理人",
                    state="visible",
                    timeout=15000
                )
            except TimeoutError:
                allure.attach(
                    self.new_page.screenshot(full_page=True),
                    name="点击确定后未显示处理人表单",
                    attachment_type=allure.attachment_type.PNG
                )
                raise Exception("点击第一个确定后，窗口未切换到处理人表单（未找到“处理人”文本）")

    def fill_workorder_details(self, description):
        self._check_new_page()
        with allure.step("通过提示文本定位处理人输入框"):
            input_locator = self.new_page.locator(self._handler_input)
            input_locator.wait_for(state="visible", timeout=15000)
            input_locator.click(force=True)
            self.new_page.wait_for_timeout(800)

            for _ in range(2):
                self.new_page.keyboard.press("ArrowDown")
                self.new_page.wait_for_timeout(300)
            self.new_page.keyboard.press("Enter")

            desc_locator = self.new_page.locator(self._description_textarea)
            desc_locator.wait_for(state="visible", timeout=10000)

            desc_locator.click(force=True)
            self.new_page.wait_for_timeout(300)  # 等待光标聚焦

            desc_locator.clear()
            desc_locator.type(description, delay=50)  # 放慢输入速度

            inputted_text = desc_locator.input_value()
            assert inputted_text == description, f"输入内容不匹配，实际输入：{inputted_text}"


    def is_workorder_page(self):
        """验证是否进入工单系统页面"""
        return self.get_text(self._workorder_title) == "工单系统"