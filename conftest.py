#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:41
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:
import pytest

from playwright_study.utils.yaml_utils import config


# conftest.py 中已有的 context 夹具（确保正确加载状态）
@pytest.fixture(scope="module")
def context(browser):
    # 加载保存的登录状态
    context = browser.new_context(storage_state=config["storage_state"])
    yield context
    context.close()