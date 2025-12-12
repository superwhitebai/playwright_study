#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/9 20:12
# @Author  : 地核桃
# @file: test_error_assign.py
# @desc:

import allure
from playwright.sync_api import expect

from pages.workorder_page import WorkorderPage
from pages.login_page import LoginPage           # ⭐ 新增：登录页 PO
from utils.logger_utils import get_logger
from utils.yaml_utils import YamlUtils, config   # 已有
from utils.path_utils import get_project_root    # 如果你之前有这个工具

logger = get_logger("ui")

# 读取登录用例数据
project_root = get_project_root()
login_data_path = project_root / "data" / "login_data.yaml"
login_data = YamlUtils.read_yaml(login_data_path)

@allure.feature("工单系统模块")
class TestWorkorder:

    @allure.story("登录后进入工单系统并创建工单，校验 Toast 提示")
    def test_enter_workorder_after_login(self, page):
        """
        前置：已通过 test_login 保存过 storage_state
        步骤：
        1. 打开系统首页（此时应已自动登录到 应用面板）
        2. 点击首页【工单系统】按钮，打开新页面
        3. 刷新新页面两次
        4. 点击【我的工作】 -> 【我发起的】
        5. 点击【创建工单】，选择【技术 -> 0625二次】
        6. 点击第一个【确定】按钮
        7. 填写处理人和说明内容
        8. 点击第二个【确定】按钮
        9. 验证 Toast 提示：创建者不可以工单派给自己
        """
        logger.info("========【工单用例】登录后进入工单系统并创建工单 开始执行 ========")

        # 1. 先打开系统首页（如果 storage_state 生效会直接到 应用面板）
        base_url = config["env"][config["current_env"]]
        page.goto(base_url)
        logger.info(f"已打开系统首页：{base_url}，当前 URL={page.url}")

        # ⭐⭐ 关键兜底逻辑：如果还在登录页，就先登录一次
        if "login" in page.url:
            logger.info("检测到当前在登录页，说明未登录或登录态失效，开始执行登录流程……")
            case = login_data["success_case"]
            login_page = LoginPage(page)

            login_page.login_with_phone_code(
                phone=case["phone"],
                verify_code=case["verify_code"],
                need_send_code=True,
            )
            login_page.assert_login_success(expected=case["expected"])
            logger.info("登录成功，当前 URL=%s", page.url)

            # 可选：顺带再覆盖一次 storage_state，保证后面用例也是新账号
            page.context.storage_state(path=config["storage_state"])
            logger.info("已覆盖保存新的 storage_state：%s", config["storage_state"])

        # 2. 进工单系统
        workorder_page = WorkorderPage(page)
        logger.info("WorkorderPage 对象创建完成")

        workorder_page.click_workorder_btn()
        logger.info("已点击【工单系统】按钮，工单新页面已打开")

        # 3. 我的工作 -> 我发起的
        workorder_page.click_my_workorder_btn()
        logger.info("已点击【我的工作】按钮")

        workorder_page.click_my_initiated_btn()
        logger.info("已点击【我发起的】tab")

        # 4. 创建工单 & 选择问题类型
        workorder_page.click_create_workorder_btn()
        logger.info("已点击【创建工单】按钮")

        workorder_page.click_0625_secondary()
        logger.info("已选择问题类型：0625二次")

        # 5. 第一个【确定】
        workorder_page.click_confirm_button()
        logger.info("已点击第一个【确定】按钮，进入处理人表单")

        # 6. 填写处理人 + 说明
        description = "这是测试说明内容"
        workorder_page.fill_workorder_details(description=description)
        logger.info("工单详情填写完成，description=%s", description)

        # 7. 第二个【确定】
        workorder_page.click_second_confirm_btn()
        logger.info("已点击第二个【确定】按钮，工单提交流程结束")

        # 8. 校验 Toast
        logger.info("开始验证 Toast 提示：创建者不可以工单派给自己")

        if not workorder_page.new_page or workorder_page.new_page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="新工单页面已关闭",
                attachment_type=allure.attachment_type.PNG,
            )
            raise Exception("新工单页面已关闭，无法验证 Toast 提示")

        toast_locator = workorder_page.new_page.get_by_text(
            "创建者不可以工单派给自己",
            exact=True,
        )

        try:
            expect(toast_locator).to_be_visible(timeout=10000)
            logger.info("Toast 提示验证通过：创建者不可以工单派给自己")
        except Exception as e:
            allure.attach(
                workorder_page.new_page.screenshot(full_page=True),
                name="Toast 断言失败-页面截图",
                attachment_type=allure.attachment_type.PNG,
            )
            raise Exception("未找到预期的 Toast 提示：创建者不可以工单派给自己") from e

        logger.info("========【工单用例】登录后进入工单系统并创建工单 执行结束 ========")