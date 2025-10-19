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

    def scroll_by_distance(self, x: int = 0, y: int = 500, delay: int = 500):
        """
        按指定距离滑动（x: 水平方向，y: 垂直方向，正数向下/右，负数向上/左）
        :param x: 水平滑动距离（像素）
        :param y: 垂直滑动距离（像素）
        :param delay: 滑动动画时长（毫秒）
        """
        self.page.mouse.wheel(dx=x, dy=y)
        # 等待滑动完成（可选）
        self.page.wait_for_timeout(delay)

    def scroll_to_bottom(self, delay: int = 500):
        """滑动到页面底部"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(delay)

    def scroll_to_top(self, delay: int = 500):
        """滑动到页面顶部"""
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(delay)