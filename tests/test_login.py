# 文件：tests/test_login.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/12
# @Author: 地核桃（优化 by ai_Playwright助手）
# @Desc: 登录模块测试用例

import allure
import pytest
from utils.yaml_utils import YamlUtils, project_root
from utils.logger_utils import logger
from pages.login_page import LoginPage


@allure.feature("登录模块")
class TestLogin:
    """登录模块测试集合"""

    @pytest.fixture(autouse=True)
    def setup_class(self, login_page):
        """
        类级前置：
        - 读取测试数据
        - 提供 login_page 实例
        """
        self.login_page = login_page
        self.login_data = YamlUtils.read_yaml(project_root / "data" / "login_data.yaml")
        logger.info("===== 登录模块初始化完成 =====")

    # ==============================================================
    @allure.story("正确手机号验证码登录成功")
    @allure.title("正确手机号+验证码登录成功")
    @pytest.mark.parametrize("case", YamlUtils.read_yaml(project_root / "data" / "login_data.yaml"))
    @pytest.mark.run(order=1)
    def test_login_success(self, case):
        """验证：正确手机号+验证码登录成功"""

        title = case["title"]
        data = case["data"]
        asserts = case["asserts"]

        with allure.step(f"执行用例：{title}"):
            logger.info(f"执行登录用例：{title}，数据：{data}")

        with allure.step("执行登录流程"):
            self.login_page.login_with_phone_code(
                phone=data["phone"],
                verify_code=data["verify_code"],
                need_send_code=True
            )

        with allure.step("验证登录成功"):
            self.login_page.assert_login_success(expected=asserts["expect_text"])
            logger.info("✅ 登录成功断言通过")
