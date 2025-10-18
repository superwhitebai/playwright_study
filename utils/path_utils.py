#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 22:11
# @Author  : 地核桃
# @file: path_utils.py.py
# @desc:
# utils/path_utils.py
from pathlib import Path

def get_project_root():
    """获取项目根目录（playwright_study 目录）"""
    # 以当前文件（path_utils.py）为基准向上导航
    current_file = Path(__file__).resolve()
    # 根据实际目录结构调整 parent 次数（例如：utils → playwright_study 需 1 次 parent）
    return current_file.parent.parent