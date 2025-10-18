#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:11
# @Author  : 地核桃
# @file: base_page.py
# @desc:
from playwright.sync_api import Page
from playwright_study.utils.yaml_utils import config


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = config["env"][config["current_env"]]  # 从配置获取基础URL

    # 封装通用操作
    def goto(self, path: str = ""):
        """访问页面（拼接基础URL）"""
        self.page.goto(f"{self.base_url}/{path}")

    def click(self, locator: str):
        """点击元素"""
        self.page.click(locator)

    def fill(self, locator: str, text: str):
        """输入文本"""
        self.page.fill(locator, text)

    def wait_for_selector(self, locator: str, timeout=30000):
        """等待元素出现"""
        self.page.wait_for_selector(locator, timeout=timeout)

    def get_text(self, locator: str):
        """获取元素文本"""
        return self.page.inner_text(locator)