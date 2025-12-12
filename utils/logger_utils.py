#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/11/13 18:36
# @Author  : 地核桃
# @file: logger_utils.py.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2025/12/12
# @Author: 地核桃 + ai_Playwright助手
# @Desc: 项目通用日志封装

import logging
import logging.config
import yaml
from pathlib import Path

# ========== 自动加载 log.yaml 配置 ==========
project_root = Path(__file__).resolve().parents[1]
log_config_path = project_root / "config" / "log.yaml"

if log_config_path.exists():
    with open(log_config_path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    logging.config.dictConfig(config_data)
else:
    # 没找到配置文件则使用默认配置
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print(f"[logger_utils] ⚠️ 未找到日志配置文件：{log_config_path}")

# ========== 提供两种调用方式 ==========
def get_logger(name: str = "ui"):
    """返回指定名称的 logger 对象"""
    return logging.getLogger(name)

# ✅ 全局默认 logger（用于 from utils.logger_utils import logger）
logger = get_logger("ui")
