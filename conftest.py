#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:41
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:


import pytest


import sys
from pathlib import Path

# 获取 conftest.py 所在的目录（即 playwrigh_study 目录）
current_dir = Path(__file__).resolve().parent  # 绝对路径，如 D:\GC_test\playwright_study
print(f"当前 conftest.py 所在目录：{current_dir}")  # 打印确认

# 将项目根目录（playwright_study）添加到 Python 搜索路径
sys.path.append(str(current_dir))
print(f"添加到 sys.path 的路径：{current_dir}")  # 打印确认
print(f"当前 sys.path 列表：{sys.path}")  # 查看是否包含目标路径

# 之后再导入 utils
from utils.yaml_utils import config  # 第12行的导入语句


# conftest.py 中已有的 context 夹具（确保正确加载状态）
@pytest.fixture(scope="module")
def context(browser):
    # 加载保存的登录状态
    context = browser.new_context(storage_state=config["storage_state"])
    yield context
    context.close()