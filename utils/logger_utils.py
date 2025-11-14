#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/11/13 18:36
# @Author  : 地核桃
# @file: logger_utils.py.py
# @desc:

import os
import logging
import logging.config
import yaml

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_CONFIG_PATH = os.path.join(ROOT_DIR, "config", "log.yaml")

LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str = "ui") -> logging.Logger:
    """
    返回一个按 log.yaml 配置好的 logger
    """
    with open(LOG_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 如果 handler 里有相对路径 filename，自动加上 ROOT_DIR
    for handler in config.get("handlers", {}).values():
        filename = handler.get("filename")
        if filename and not os.path.isabs(filename):
            handler["filename"] = os.path.join(ROOT_DIR, filename)

    logging.config.dictConfig(config)
    return logging.getLogger(name)