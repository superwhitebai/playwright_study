#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:15
# @Author  : 地核桃
# @file: login_page.py.py
# @desc:
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    #元素定位符
    _scan_login_btn = 'img#scanLogin.code-tips.pointer'#点击扫码登录按钮
    _phone_input = '#phoneInput' #手机号输入框
    _code_input = '#codeInput' #验证码输入框
    _send_code_btn = '#sendCodeBtn' #发送验证码按钮
    _login_btn = '#phoneLoginBtn' #登录按钮
    _app_panel_text = 'text=应用面板' #断言文本

    def __init__(self,page:Page):
        super().__init__(page)

    def goto_login(self):
        '''点击扫码登录按钮'''
        self.goto("#/personal/index")

    def switch_to_password_login(self):
        """切换到密码登录（点击扫码登录按钮后可能显示密码登录表单）"""
        self.click(self._scan_login_btn)

    def input_phone(self, phone: str):
        """输入手机号"""
        self.fill(self._phone_input, phone)

    def input_verify_code(self, code: str):
        """输入验证码"""
        self.fill(self._code_input, code)

    def click_send_code(self):
        """点击发送验证码"""
        self.click(self._send_code_btn)

    def click_login(self):
        """点击登录按钮"""
        self.click(self._login_btn)

    def wait_for_login_success(self):
        """等待登录成功（验证应用面板文本出现）"""
        self.wait_for_selector(self._app_panel_text)

    def is_login_success(self):
        """判断是否登录成功"""
        return self.get_text(self._app_panel_text) == "应用面板"