#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/9/4 09:52
# @Author  : 地核桃
# @file: playwright_study.py
# @desc:
import time

# conftest.py（pytest Fixture 配置）
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser():
    """启动浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False 可见浏览器窗口
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """创建新页面"""
    page = browser.new_page()
    yield page
    page.close()


# test_login.py（测试用例）
def test_login_success(page):
    """成功登录测试"""
    # 步骤1：打开登录页
    page.goto("https://sso.dev.igancao.cn/#/personal/index")
    # 步骤2：点击扫码登录按钮
    page.click("img#scanLogin.code-tips.pointer")

    # 步骤3：输入用户名和密码
    page.fill("#phoneInput", "13221010902")
    page.fill("#codeInput", "0902")
    time.sleep(3)

    # 步骤4：点击发送短信按钮
    page.click("#sendCodeBtn")
    time.sleep(3)
    # 步骤5：点击登录按钮
    page.click('#phoneLoginBtn')

    # 步骤4：断言登录成功（检查欢迎文本）
    assert page.inner_text('text=应用面板') == '应用面板'



def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 非无头模式，方便观察登录过程
        context = browser.new_context()  # 创建一个上下文（隔离的浏览器环境）
        page = context.new_page()

        # 执行登录操作（替换为你的实际登录步骤）
        page.goto("你的登录页面URL")
        page.fill("#phoneInput", "你的手机号")
        page.click("#sendCodeBtn")
        # （如果需要手动输入验证码，这里可以加个延迟，手动输入后再继续）
        page.wait_for_timeout(10000)  # 等待10秒，手动输入验证码
        page.fill("#codeInput", "验证码")  # 或自动填充
        page.click("#phoneLoginBtn")

        # 等待登录完成（比如等待“应用面板”出现，确认登录成功）
        page.locator("text=应用面板").wait_for()

        # 保存登录状态到文件（关键步骤）
        context.storage_state(path="login_state.json")

        browser.close()

if __name__ == "__main__":
    save_login_state()  # 运行一次，生成login_state.json