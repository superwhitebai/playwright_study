#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:25
# @Author  : 地核桃
# @file: test_login.py.py
# @desc:
import sys
import os

# 获取项目根目录（当前文件在tests目录下，需回退一级）
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)


import pytest
import time
import allure
from utils.yaml_utils import YamlUtils, config
from utils.path_utils import get_project_root
from utils.logger_utils import get_logger

# 获取项目根目录
project_root = get_project_root()
# 拼接测试数据文件的绝对路径
login_data_path = project_root / "data" / "login_data.yaml"
# 读取测试数据
login_data = YamlUtils.read_yaml(login_data_path)
logger = get_logger("ui")

@allure.feature("登录模块")
class TestLogin:

    @allure.story("成功登录")
    @pytest.mark.parametrize("case", [login_data["success_case"]])
    def test_login_success(self, login_page, case):
        logger.info("【登录用例】开始执行，用例数据：%s", case)

        with allure.step("打开登录页"):
            login_page.goto_login()
            logger.info("打开登录页成功")

        with allure.step("输入账号密码"):
            login_page.switch_to_password_login()
            login_page.input_phone(case["phone"])
            login_page.input_verify_code(case["verify_code"])
            logger.info("账号密码输入完成")

        with allure.step("发送验证码"):
            login_page.click_send_code()
            logger.info("点击发送验证码按钮")

            time.sleep(3)
            login_page.click_login()
            logger.info("点击登录按钮")

        with allure.step("验证登录成功"):
            login_page.wait_for_login_success()
            assert login_page.is_login_success(), f"预期结果：{case['expected']}"
            logger.info("登录成功断言通过")

        # 登录成功后保存状态（仅首次运行时需要，后续可注释）
        login_page.page.context.storage_state(path=config["storage_state"])

    # @allure.story("失败登录")
    # @pytest.mark.parametrize("case", login_data["fail_cases"])
    # def test_login_fail(self, login_page, case):
    #     """测试失败登录场景（如验证码错误、手机号为空）"""
    #     login_page.goto_login()
    #     login_page.switch_to_password_login()
    #     login_page.input_phone(case["phone"])
    #     login_page.input_verify_code(case["verify_code"])
    #     login_page.click_send_code()
    #     time.sleep(3)
    #     login_page.click_login()
    #
    #     # 断言失败提示（需根据实际页面调整定位符）
    #     error_msg = login_page.get_text("div.error提示的定位符")
    #     assert error_msg == case["expected"], f"预期错误：{case['expected']}"
