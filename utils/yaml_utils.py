#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:10
# @Author  : 地核桃
# @file: yaml_utils.py
# @desc:
# playwright_study/utils/yaml_utils.py
import yaml
from pathlib import Path

# utils/yaml_utils.py
import yaml
from pathlib import Path


class YamlUtils:
    @staticmethod
    def read_yaml(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)


# ====== 加载全局 config.yaml ======
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
config_file_path = project_root / "config" / "config.yaml"

config = YamlUtils.read_yaml(config_file_path)
base_url = config["env"][config["current_env"]]
