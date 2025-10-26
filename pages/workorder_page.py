#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:38
# @Author  : 地核桃
# @file: workorder_page.py.py
# @desc:
# pages/workorder_page.py
from operator import index

import allure
from playwright_study.pages.base_page import BasePage

class WorkorderPage(BasePage):
    # 工单系统按钮定位符（根据实际元素调整，此处为 class 定位）
    _workorder_btn = "text=工单系统"  # 你的元素定位：class="ant-image-img"
    # 可添加工单系统页面的其他元素（如页面标题，用于验证跳转成功）
    _workorder_title = "text=工单系统"  # 假设跳转后有此标题
    _workorde_my_work = "text=我的工作"
    _my_initiated_btn_ = 'div[role="tab"]:has-text("我发起的")'
    create_workorder_btn = "text=创建工单"
    locator = 'div:has-text("技术") .menu-item span:has-text("0625二次")'
    confirm_but = "xpath=/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]"
    _handler_input = (
        'div:has(> div:has-text("不指定时会由小组成员自己认领")) '  # 包含提示文本的容器
        'input.ant-select-selection-search-input'  # 容器内的输入框
    )
    _description_textarea = 'textarea[placeholder="请输入"][class="ant-input"]'




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

        # 新增：封装刷新新页面两次的方法

    def refresh_new_page_twice(self):
        self.new_page.reload(wait_until="networkidle")  # 刷新新页面
        self.new_page.wait_for_timeout(2000)  # 等待刷新完成
        # self.new_page.reload(wait_until="networkidle")  # 再次刷新新页面

    def _check_new_page(self):
        """检查新页面是否已打开且未关闭"""
        if not self.new_page:  # 新页面未初始化（未打开）
            raise Exception("新页面未打开，请先调用 click_workorder_btn() 打开新页面")
        if self.new_page.is_closed():  # 新页面已被关闭
            raise Exception("新页面已关闭，无法执行操作")

    def click_my_initiated_btn(self):
        """
        点击"我发起的"按钮的方法
        该方法会先检查是否已跳转到新页面，然后在新页面中定位并点击"我发起的"按钮。
        使用了allure框架记录测试步骤，并设置了元素可见的超时等待时间。
        """
        # 检查是否已跳转到新页面
        self._check_new_page()
        with allure.step("点击新页面中的“我发起的”按钮"):
            self.new_page.locator(self._my_initiated_btn_).wait_for(
                state="visible",
                timeout=10000
            )
            self.new_page.locator(self._my_initiated_btn_).click()

    def click_create_workorder_btn(self):
        """点击新页面中的“创建工单”按钮"""
        self._check_new_page()  # 确保新页面已打开
        with allure.step("点击新页面中的“创建工单”按钮"):
            # 关键：使用self.new_page定位，且调用locator方法
            self.new_page.locator(self.create_workorder_btn).click()

    def click_0625_secondary(self):
        """点击技术分类下的“0625二次”（修正版）"""
        self._check_new_page()  # 确保在新页面操作
        with allure.step("点击技术分类下的“0625二次”"):
            # 优化定位器：用后代选择器（空格），放宽层级限制
            # 先等待元素可见（超时10秒，应对加载延迟）
            locator = self.locator
            self.new_page.locator(locator).wait_for(state="visible", timeout=10000)
            # 在新页面中点击（关键：用self.new_page）
            self.new_page.locator(locator).click()

    def click_confirm_but(self):
        self._check_new_page()  # 确保在新页面操作
        with allure.step("点击弹窗中的“确定”按钮（XPath定位）"):
            # 直接使用带 "xpath=" 前缀的定位符
            self.new_page.locator(self.confirm_but).wait_for(
                state="visible",
                timeout=15000  # 超时15秒
            )
            self.new_page.locator(self.confirm_but).click()

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