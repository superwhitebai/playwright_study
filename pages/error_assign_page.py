#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/9 20:13
# @Author  : 地核桃
# @file: error_assign_page.py
# @desc:
# pages/workorder_page.py
import allure
from playwright.sync_api import Page, expect
from typing import Optional
from pages.base_page import BasePage
from utils.logger_utils import get_logger
import re

logger = get_logger("ui")

class WorkorderPage(BasePage):
    """
    工单系统页面，不再依赖 YAML 定位，全部用元素定位（get_by_xxx）重写
    """

    def __init__(self, page: Page):
        super().__init__(page)   # 不再传 locator_file
        self.new_page: Optional[Page] = None   # 工单系统的新窗口

    # ========= 通用内部方法 =========

    def _check_new_page(self):
        """检查新页面是否已打开且未关闭"""
        if self.new_page is None:
            raise Exception("工单新页面未打开，请先调用 click_workorder_btn()")
        if self.new_page.is_closed():
            raise Exception("工单新页面已关闭，无法继续操作")

    # ========= 顶层入口：从应用面板进入工单系统 =========

    @allure.step("点击应用面板中的【工单系统】按钮，打开工单新页面")
    def click_workorder_btn(self):
        """
        在应用面板首页，点击【工单系统】，等待新窗口打开
        """
        with self.page.expect_popup() as popup_info:
            # 文本“工单系统”在应用面板左侧或卡片上，一般 text 定位就够了
            self.page.get_by_text("工单系统", exact=True).click()
        self.new_page = popup_info.value
        self.new_page.wait_for_load_state("networkidle")
        logger.info("工单系统新页面已打开，URL=%s", self.new_page.url)

    # ========= 工单首页：左侧菜单 / Tab =========


    @allure.step("等待工单首页加载完成（直到【我的工作】可见）")
    def wait_for_workorder_home_ready(self, timeout: int = 30000):
        """
        页面自动刷新没关系，我们只关心：左侧出现【我的工作】
        """
        self._check_new_page()

        # 等一轮网络空闲（可能中间有自动刷新）
        self.new_page.wait_for_load_state("networkidle")

        my_work = self.new_page.get_by_text("我的工作")
        expect(my_work).to_be_visible(timeout=timeout)

    @allure.step("点击工单页面左侧【我的工作】")
    def click_my_workorder_btn(self):
        """
        左侧菜单点击【我的工作】
        """
        self._check_new_page()
        self.wait_for_workorder_home_ready()

        my_work = self.new_page.get_by_text("我的工作")
        expect(my_work).to_be_visible(timeout=15000)
        my_work.click()

    @allure.step("点击工单页面中的【我发起】tab")
    def click_my_initiated_btn(self):
        """
        顶部或中间 Tab：只要包含“我发起”字样即可
        """
        self._check_new_page()

        tab = self.new_page.get_by_text("我发起")
        expect(tab).to_be_visible(timeout=15000)
        tab.click()

    # ========= 创建工单入口 =========

    @allure.step("点击【创建工单】按钮")
    def click_create_workorder_btn(self):
        """
        在“我发起”列表页面点击【创建工单】
        这里用模糊匹配，兼容“+ 创建工单”等情况
        """
        self._check_new_page()

        # 先等一轮列表区域加载
        self.new_page.wait_for_load_state("networkidle")

        # 优先用 role=button + name 包含“创建工单”
        btn = self.new_page.get_by_role("button", name=re.compile("创建工单"))
        try:
            expect(btn).to_be_visible(timeout=10000)
            btn.click()
            return
        except Exception:
            # 如果 role 匹配不到，再退回纯文本匹配
            logger.warning("通过 role=button 未找到【创建工单】，退回 get_by_text 匹配")
            fallback = self.new_page.get_by_text("创建工单")
            expect(fallback).to_be_visible(timeout=10000)
            fallback.click()

    # ========= 问题类型选择 =========

    @allure.step("选择问题类型【技术 -> 0625二次】")
    def click_0625_secondary(self):
        """
        选择左侧“技术”分类下的“0625二次”，你之前这段 CSS 是有效的，这里沿用
        """
        self._check_new_page()

        locator = self.new_page.locator(
            'div:has-text("技术") .menu-item span:has-text("0625二次")'
        )
        locator.wait_for(state="visible", timeout=10000)
        locator.click()

    # ========= 第一个确定：问题类型弹窗 =========

    @allure.step("点击问题类型弹窗中的【确定】按钮")
    def click_confirm_button(self):
        """
        你原来用的是绝对 XPath，这里先沿用；如果后续 DOM 波动再调
        """
        self._check_new_page()

        confirm_btn = self.new_page.locator(
            'xpath=/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]'
        )
        confirm_btn.wait_for(state="visible", timeout=15000)
        confirm_btn.click()

    # ========= 填写处理人 + 描述 =========

    @allure.step("填写处理人和工单说明")
    def fill_workorder_details(self, description: str):
        """
        保留你原来的逻辑：
        1. 点击处理人下拉框（通过提示文案“ 不指定时会由小组成员自己认领 ”）
        2. 键盘下移两次，回车选择处理人
        3. 在说明文本框输入 description
        """
        self._check_new_page()

        # 处理人下拉框容器
        handler_container = self.new_page.locator(
            'div.ant-select:has(span.ant-select-selection-placeholder:has-text("不指定时会由小组成员自己认领"))'
        )
        handler_container.wait_for(state="visible", timeout=15000)
        handler_container.click(force=True)
        self.new_page.wait_for_timeout(800)

        # 下移两次选人
        for _ in range(4):
            self.new_page.keyboard.press("ArrowDown")
            self.new_page.wait_for_timeout(300)
        self.new_page.keyboard.press("Enter")

        # 填写说明 textarea
        desc_locator = self.new_page.locator(
            'textarea[class*="ant-input"][placeholder*="请输入"]'
        )
        desc_locator.wait_for(state="visible", timeout=10000)
        desc_locator.click(force=True)
        self.new_page.wait_for_timeout(300)
        desc_locator.fill("")         # 先清空
        desc_locator.type(description, delay=50)

        # 校验内容是否输入成功
        inputted = desc_locator.input_value()
        assert inputted == description, f"输入内容不匹配，实际：{inputted}"

    # ========= 第二个确定：处理人弹窗 =========

    @allure.step("点击处理人弹窗中的【确 定】按钮")
    def click_second_confirm_btn(self):
        """
        使用你调试出来的定位：get_by_role("button", name="确 定")
        注意中间有空格
        """
        self._check_new_page()

        btn = self.new_page.get_by_role("button", name="确 定")
        btn.wait_for(state="visible", timeout=10000)
        btn.click()