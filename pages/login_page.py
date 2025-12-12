#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:15
# @Author  : 地核桃
# @file: login_page.py.py
# @desc:
# pages/login_page.py
# pages/login_page.py
import os
from pathlib import Path
from typing import Optional
import logging
import time
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.yaml_utils import config, project_root
logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """登录页 Page Object，元素来自 locators/login_page.yaml"""

    def __init__(self, page: Page):
        # 关联到 locators/login_page.yaml
        super().__init__(page, locator_file="login_page.yaml")
        logger.info("LoginPage 初始化完成，已加载 locators/login_page.yaml")

    # ========== 原子操作（一步对应一个小操作） ==========

    @allure.step("打开登录页")
    def goto_login(self):
        logger.info("打开登录页：#/personal/index")
        # 根据你 config 里的 base_url 拼接，如：https://xxx/#/personal/index
        self.goto("#/personal/index")

    @allure.step("切换到手机/密码登录表单")
    def switch_to_password_login(self):
        logger.info("点击扫码登录按钮，切换到手机/密码登录表单")
        self.loc("scan_login_btn").click()

    @allure.step("输入手机号：{phone}")
    def input_phone(self, phone: str):
        logger.info("输入手机号：%s", phone)
        self.loc("phone_input").fill(phone)

    @allure.step("输入验证码：{code}")
    def input_verify_code(self, code: str):
        logger.info("输入验证码：%s", code)
        self.loc("code_input").fill(code)

    @allure.step("点击发送验证码按钮")
    def click_send_code(self):
        logger.info("点击发送验证码按钮")
        self.loc("send_code_btn").click()

    @allure.step("点击登录按钮")
    def click_login(self):
        logger.info("点击登录按钮")
        self.loc("login_btn").click()

    @allure.step("等待登录成功（出现【应用面板】文本）")
    def wait_for_login_success(self):
        logger.info("等待登录成功，检查【应用面板】文本是否出现")
        self.loc("app_panel_text").first.wait_for(state="visible")

    def is_login_success(self) -> bool:
        text = self.loc("app_panel_text").inner_text()
        logger.info("登录结果文本：%s", text)
        return text == "应用面板"

    # ========== 业务级组合动作（测试用例里主要调用这些） ==========

    @allure.step("使用手机号 + 验证码完成登录")
    def login_with_phone_code(self, phone: str, verify_code: str, need_send_code: bool = True):
        """
        一条龙登录流程：
        1. 打开登录页
        2. 切换到手机/密码登录表单
        3. 输入手机号
        4. (可选) 点击发送验证码
        5. 输入验证码
        6. 点击登录
        """
        logger.info("执行登录流程，phone=%s, verify_code=%s", phone, verify_code)

        self.goto_login()
        self.switch_to_password_login()
        self.input_phone(phone)

        if need_send_code:
            self.click_send_code()
            # 这里简单 sleep 一下，后面可以改成显式等待某个元素
            time.sleep(2)

        self.input_verify_code(verify_code)
        self.click_login()

    @allure.step("断言登录成功，期望文案：{expected}")
    def assert_login_success(self, expected: str = "应用面板"):
        self.wait_for_login_success()
        actual = self.loc("app_panel_text").inner_text()
        logger.info("断言登录成功：期望=%s，实际=%s", expected, actual)
        assert actual == expected, "登录失败：期望 %s，实际 %s" % (expected, actual)

    @allure.step("保存当前登录态到 storage_state：{path}")
    def save_storage_state(self, path: Optional[str] = None):
        # 统一：都保存到 项目根目录 / storage_state.json
        if path is None:
            path = project_root / config["storage_state"]
        else:
            # 如果传进来的是相对路径，也拼到 project_root 下
            path = (
                project_root / path
                if not os.path.isabs(path)
                else Path(path)
            )

        logger.info("保存 storage_state 到文件：%s", path)
        self.page.context.storage_state(path=str(path))