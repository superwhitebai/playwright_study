#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:38
# @Author  : 地核桃
# @file: workorder_page.py.py
# @desc:
# pages/workorder_page.py
from operator import index

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage

class WorkorderPage(BasePage):
    _confirm_button = 'xpath=/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]'

    # 2. 技术分类下的“0625二次”：避免硬编码层级，用包含关系
    _0625_secondary = (
        'div:has-text("技术") '  # 包含“技术”文本的父容器
        '.menu-item span:has-text("0625二次")'  # 子元素文本匹配
    )

    # 3. 说明内容输入框：模糊匹配placeholder（避免精确匹配失败）
    _description_textarea = (
        'textarea[class*="ant-input"]'  # class包含ant-input
        '[placeholder*="请输入"]'  # placeholder包含“请输入”
    )

    _handler_select_container = 'div.ant-select:has(span.ant-select-selection-placeholder:has-text("不指定时会由小组成员自己认领"))'
    _handler_input = f'{_handler_select_container} input.ant-select-selection-search-input'  # 依赖容器定位input
    _handler_options = f'{_handler_select_container} .ant-select-dropdown li'  # 下拉选项
    _handler_dropdown = "div.rc-select-dropdown:visible"

    # 4. 其他定位符规范化（统一前缀下划线，明确含义）
    _workorder_btn = "text=工单系统"  # 保持不变（文本定位稳定）
    _workorder_title = "text=工单系统"
    _my_work_btn = "text=我的工作"  # 原_workorde_my_work拼写错误，修正
    _my_initiated_tab = 'div[role="tab"]:has-text("我发起的")'  # 明确是tab
    _create_workorder_btn = "text=创建工单"  # 加下划线，符合私有属性规范
    _second_confirm_btn = (
        'div.ant-modal:has(text("处理人")) '  # 上下文：当前窗口显示处理人表单
        'div.ant-modal-footer button.ant-btn-primary:has-text("确定")'
    )

    def __init__(self, page: Page):
        super().__init__(page)
        self.new_page = None

    def click_workorder_btn(self):
        """点击工单按钮，打开新页面并保存新页面对象"""
        with self.page.expect_popup() as popup_info:
            self.click(self._workorder_btn)
        self.new_page = popup_info.value  # 保存新页面对象到实例变量
        self.new_page.wait_for_load_state("networkidle")  # 等待新页面加载

    # 新增：点击新页面中的“我的工单”按钮
    def click_my_workorder_btn(self):
        """点击“我的工作”按钮（修正版）"""
        self._check_new_page()
        with allure.step("点击新页面中的“我的工作”"):
            # 等待“我的工作”按钮可见（确保页面加载完成）
            my_work_locator = self.new_page.locator(self._my_work_btn)
            my_work_locator.wait_for(state="visible", timeout=15000)
            my_work_locator.click()


    def refresh_new_page_twice(self):
        self.new_page.wait_for_timeout(3000)
        self.new_page.reload(wait_until="networkidle")  # 刷新新页面

    def _check_new_page(self):
        """检查新页面是否已打开且未关闭"""
        if not self.new_page:  # 新页面未初始化（未打开）
            raise Exception("新页面未打开，请先调用 click_workorder_btn() 打开新页面")
        if self.new_page.is_closed():  # 新页面已被关闭
            raise Exception("新页面已关闭，无法执行操作")

    def click_my_initiated_btn(self):
        """点击“我发起的”标签（修正版）"""
        self._check_new_page()  # 仅检查新页面有效
        with allure.step("点击新页面中的“我发起的”"):
            # 等待“我发起的”标签可见
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
        """点击技术分类下的“0625二次”（修正版）"""
        self._check_new_page()  # 确保在新页面操作
        with allure.step("点击技术分类下的“0625二次”"):
            # 优化定位器：用后代选择器（空格），放宽层级限制
            # 先等待元素可见（超时10秒，应对加载延迟）
            locator = self._0625_secondary
            self.new_page.locator(locator).wait_for(state="visible", timeout=10000)
            # 在新页面中点击（关键：用self.new_page）
            self.new_page.locator(locator).click()


    def click_confirm_button(self):
        """点击第一个“确定”按钮（选择协同问题后），等待窗口显示“处理人”表单"""
        self._check_new_page()
        with allure.step("点击第一个确定按钮，等待窗口内容更新为处理人表单"):
            # 1. 点击第一个确定按钮（复用你的绝对XPath）
            confirm_locator = self.new_page.locator(self._confirm_button)
            confirm_locator.wait_for(state="visible", timeout=15000)  # 确保按钮存在
            confirm_locator.click(force=True)

            # 2. 关键：不等待按钮隐藏，而是等待窗口出现“处理人”字段（确认内容更新）
            try:
                self.new_page.wait_for_selector(
                    "text=处理人",  # 窗口内容更新的标志（必须是实际出现的文本）
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
            # 步骤1：通过提示文本找到输入框并点击展开下拉框
            input_locator = self.new_page.locator(self._handler_input)
            input_locator.wait_for(state="visible", timeout=15000)
            # 点击输入框激活（若无效则点击下拉箭头）
            input_locator.click(force=True)
            self.new_page.wait_for_timeout(800)

            for _ in range(2):
                self.new_page.keyboard.press("ArrowDown")
                self.new_page.wait_for_timeout(300)
            self.new_page.keyboard.press("Enter")

            desc_locator = self.new_page.locator(self._description_textarea)
            desc_locator.wait_for(state="visible", timeout=10000)

            # 强制激活输入框（解决可能的聚焦问题）
            desc_locator.click(force=True)
            self.new_page.wait_for_timeout(300)  # 等待光标聚焦

            # 清空并输入（避免默认值干扰）
            desc_locator.clear()
            desc_locator.type(description, delay=50)  # 放慢输入速度

            # 验证输入结果（可选）
            inputted_text = desc_locator.input_value()
            assert inputted_text == description, f"输入内容不匹配，实际输入：{inputted_text}"


    def is_workorder_page(self):
        """验证是否进入工单系统页面"""
        return self.get_text(self._workorder_title) == "工单系统"