#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:41
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:

import sys, os
from pathlib import Path

# 确保项目根路径加入 sys.path
current_dir = Path(__file__).resolve().parent
project_root = current_dir  # 当前已是项目根目录（D:\GC_test\playwright_study）
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 文件：conftest.py
import pytest
from playwright.sync_api import sync_playwright
from utils.yaml_utils import config, project_root
from pages.login_page import LoginPage
from utils.logger_utils import get_logger
logger = get_logger("ui")

@pytest.fixture(scope="session")
def browser():
    """根据 config.yaml 启动指定浏览器"""
    browser_cfg = config.get("browser", {})
    browser_type = browser_cfg.get("type", "chromium")
    headless = browser_cfg.get("headless", False)
    slow_mo = browser_cfg.get("slow_mo", 0)

    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=headless, slow_mo=slow_mo)
        logger.info(f"启动浏览器：{browser_type}, headless={headless}, slow_mo={slow_mo}")
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def context(browser):
    """根据 storage_state 启动上下文"""
    storage_path = project_root / config["storage_state"]
    if storage_path.exists():
        ctx = browser.new_context(storage_state=str(storage_path))
        logger.info(f"使用登录态文件：{storage_path}")
    else:
        ctx = browser.new_context()
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    """每个用例一个新 Page"""
    p = context.new_page()
    yield p
    p.close()

@pytest.fixture(scope="function")
def login_page(page):
    """登录页面对象"""
    return LoginPage(page)
