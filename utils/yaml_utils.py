#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:10
# @Author  : 地核桃
# @file: yaml_utils.py
# @desc:
import yaml


class YamlUtils:
    @staticmethod
    def read_yaml(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)


# 全局配置实例
config = YamlUtils.read_yaml("./config/config.yaml")
base_url = config["env"][config["current_env"]]  # 当前环境的基础URL