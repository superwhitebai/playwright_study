#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:24
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:
import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from utils.yaml_utils import config


@pytest.fixture(scope="session")  # 会话级：所有用例共享一个浏览器
def browser():
    with sync_playwright() as p:
        # 从配置获取浏览器类型和参数
        browser_type = config["browser"]["type"]
        browser = getattr(p, browser_type).launch(
            headless=config["browser"]["headless"],
            slow_mo=config["browser"]["slow_mo"]
        )
        yield browser
        browser.close()

@pytest.fixture(scope="module")  # 模块级：每个模块共享一个上下文
def context(browser):
    # 加载登录状态（如果存在），否则新建上下文
    try:
        context = browser.new_context(storage_state=config["storage_state"])
    except:
        context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")  # 用例级：每个用例一个页面
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def login_page(page):
    """登录页面对象夹具"""
    return LoginPage(page)

def login_page_yy(page):
    """登录页面对象夹具"""
    return LoginPage(page)