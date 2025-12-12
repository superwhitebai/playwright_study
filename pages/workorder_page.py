# 文件：pages/workorder_page.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/12
# @Author  : 地核桃（优化融合 by ai_Playwright助手）
# @Desc: 根据登录态创建工单

import allure
import re
from typing import Optional
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger_utils import logger


class WorkorderPage(BasePage):
    """工单系统页面操作封装"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.new_page: Optional[Page] = None

    # ========= 通用内部方法 =========

    def _check_new_page(self):
        """校验工单新窗口是否已打开"""
        if self.new_page is None:
            logger.error("工单新页面未打开，请先执行 click_workorder_btn()")
            raise Exception("工单新页面未打开")
        if self.new_page.is_closed():
            logger.error("工单新页面已关闭，无法继续操作")
            raise Exception("工单新页面已关闭")

    # ========= 顶层入口 =========

    @allure.step("点击应用面板中的【工单系统】按钮，打开工单新页面")
    def click_workorder_btn(self):
        with self.page.expect_popup() as popup_info:
            self.page.get_by_text("工单系统", exact=True).click()
        self.new_page = popup_info.value
        self.new_page.wait_for_load_state("networkidle")
        logger.info(f"✅ 工单系统新页面已打开，URL={self.new_page.url}")

    # ========= 页面加载校验 =========

    @allure.step("等待工单首页加载完成（直到【我的工作】可见）")
    def wait_for_workorder_home_ready(self, timeout: int = 30000):
        self._check_new_page()
        self.new_page.wait_for_load_state("networkidle")
        expect(self.new_page.get_by_text("我的工作")).to_be_visible(timeout=timeout)
        logger.info("✅ 工单首页加载完成")

    @allure.step("点击左侧【我的工作】菜单")
    def click_my_workorder_btn(self):
        self._check_new_page()
        self.wait_for_workorder_home_ready()
        my_work = self.new_page.get_by_text("我的工作")
        expect(my_work).to_be_visible(timeout=15000)
        my_work.click()
        logger.info("✅ 已点击【我的工作】")

    @allure.step("点击顶部【我发起的】Tab")
    def click_my_initiated_btn(self):
        self._check_new_page()
        tab = self.new_page.get_by_text("我发起")
        expect(tab).to_be_visible(timeout=15000)
        tab.click()
        logger.info("✅ 已切换到【我发起的】Tab")

    # ========= 创建工单 =========

    @allure.step("点击【创建工单】按钮")
    def click_create_workorder_btn(self):
        self._check_new_page()
        self.new_page.wait_for_load_state("networkidle")

        btn = self.new_page.get_by_role("button", name=re.compile("创建工单"))
        try:
            expect(btn).to_be_visible(timeout=10000)
            btn.click()
            logger.info("✅ 点击【创建工单】按钮成功")
        except Exception:
            logger.warning("通过 role=button 未找到【创建工单】，退回 get_by_text 匹配")
            fallback = self.new_page.get_by_text("创建工单")
            expect(fallback).to_be_visible(timeout=10000)
            fallback.click()

    @allure.step("选择问题类型【技术 -> 0625二次】")
    def click_0625_secondary(self):
        self._check_new_page()
        locator = self.new_page.locator(
            'div:has-text("技术") .menu-item span:has-text("0625二次")'
        )
        locator.wait_for(state="visible", timeout=10000)
        locator.click()
        logger.info("✅ 已选择问题类型：技术 -> 0625二次")

    @allure.step("点击第二个【确 定】按钮")
    def click_second_confirm_btn(self):
        self._check_new_page()
        btn = self.new_page.get_by_role("button", name="确 定")
        expect(btn).to_be_visible(timeout=10000)
        btn.click()
        logger.info("✅ 点击第二个确定按钮成功")

    # ========= 填写工单详情 =========

    @allure.step("填写处理人和工单说明")  # 使用allure.step装饰器标记测试步骤，步骤名称为"填写处理人和工单说明"
    @allure.step("填写工单详情：处理人 + 说明")
    def fill_workorder_details(self, description: str):
        self._check_new_page()

        try:
            with allure.step("选择工单处理人"):
                handler = self.new_page.locator(
                    'div.ant-select:has(span.ant-select-selection-placeholder:has-text("不指定时会由小组成员自己认领"))'
                )
                handler.wait_for(state="visible", timeout=15000)
                handler.click(force=True)
                logger.info("✅ 已点击处理人下拉框")

                # 循环按键选择成员
                for i in range(2):
                    self.new_page.keyboard.press("ArrowDown")
                    logger.info(f"⬇️ 第 {i+1} 次按下方向键 ↓")
                    self.new_page.wait_for_timeout(300)

                self.new_page.keyboard.press("Enter")
                logger.info("✅ 已按下 Enter 键确认选择处理人")

            with allure.step("填写工单说明内容"):
                desc = self.new_page.locator(
                    'textarea[class*="ant-input"][placeholder*="请输入"]'
                )
                desc.wait_for(state="visible", timeout=10000)
                desc.fill("")
                desc.type(description, delay=50)
                expect(desc).to_have_value(description)
                logger.info(f"✅ 已填写工单说明：{description}")

            allure.attach(
                self.new_page.screenshot(full_page=False),
                name="工单详情填写完成",
                attachment_type=allure.attachment_type.PNG,
            )

        except Exception as e:
            allure.attach(
                self.new_page.screenshot(full_page=True),
                name="工单详情填写失败截图",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.error(f"❌ 填写工单详情失败：{e}")
            raise
