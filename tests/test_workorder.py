#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:39
# @Author  : 地核桃
# @file: test_workorder.py.py
# @desc:


import allure
from playwright.sync_api import expect
from pages.workorder_page import WorkorderPage
from utils.logger_utils import get_logger   # ✅ 1. 引入日志工具

logger = get_logger("ui")
@allure.feature("工单系统模块")
class TestWorkorder:

    @allure.story("登录后进入工单系统")
    def test_enter_workorder_after_login(self, page, login_page):

        logger.info("========【工单用例】登录后进入工单系统 开始执行 ========")

        with allure.step("打开登录页并登录"):
            login_page.goto_login()
            logger.info("已打开登录页")
            # 如果 login_page 里已经封装了登录，这里可以顺便调一下并记录日志
            # login_page.login_xxx(...)
            logger.info("登录成功，准备进入工单系统")

        # 创建工单页面对象
        workorder_page = WorkorderPage(page)
        logger.info("WorkorderPage 对象创建完成")

        with allure.step("点击工单系统按钮（打开新页面）"):
            logger.info("点击【工单系统】按钮，等待新页面出现")
            workorder_page.click_workorder_btn()

        with allure.step("刷新新页面"):
            logger.info("开始刷新新页面两次")
            workorder_page.refresh_new_page_twice()
            logger.info("新页面刷新完成")

        with allure.step("点击新页面中的【我的工单】"):
            workorder_page.click_my_workorder_btn()
            logger.info("已点击【我的工单】按钮")

        with allure.step("点击新页面中的【我发起的】"):
            workorder_page.click_my_initiated_btn()
            logger.info("已点击【我发起的】按钮，并检查是否出现待处理文本")

        with allure.step("点击【创建工单】按钮"):
            workorder_page.click_create_workorder_btn()
            logger.info("已点击【创建工单】按钮，进入工单创建页面")

        with allure.step("选择问题 0625 二类"):
            workorder_page.click_0625_secondary()
            logger.info("已选择问题类型：0625二类")

        with allure.step("点击第一个页面【确认】按钮"):
            workorder_page.click_confirm_button()
            logger.info("已点击第一步确认按钮")

        with allure.step("填写接收人和说明内容"):
            description = "这是测试说明内容"
            workorder_page.fill_workorder_details(description=description)
            logger.info("工单详情填写完成，description=%s", description)

        with allure.step("点击第二个页面【确认】按钮"):
            workorder_page.click_confirm_button()
            logger.info("已点击第二步确认按钮，工单提交流程结束")

            # workorder_page.page.pause()

        with allure.step("验证Toast提示"):
            logger.info("开始验证Toast提示：创建者不可以工单派给自己")

            # 1. 检查新页面状态
            if not workorder_page.new_page or workorder_page.new_page.is_closed():
                allure.attach(
                    workorder_page.page.screenshot(full_page=True),
                    name="新工单页面已关闭",
                    attachment_type=allure.attachment_type.PNG
                )
                raise Exception("新工单页面已关闭，无法验证Toast")

            # 2. 用新页面定位Toast（核心修正）
            toast_locator = workorder_page.new_page.get_by_text(
                "创建者不可以工单派给自己",
                exact=True  # 完全匹配文本
            )

            # 3. 修正断言：移除message参数，用try-except自定义错误
            try:
                # 等待10秒，直到Toast可见（自动重试）
                expect(toast_locator).to_be_visible(timeout=10000)
            except Exception as e:
                # 断言失败时，添加新页面截图到Allure报告
                allure.attach(
                    workorder_page.new_page.screenshot(full_page=True),
                    name="Toast断言失败-页面截图",
                    attachment_type=allure.attachment_type.PNG
                )
                # 抛出自定义错误信息
                raise Exception("未找到预期的Toast提示：创建者不可以工单派给自己") from e

        logger.info("========【工单用例】登录后进入工单系统 执行结束 ========")

        # 验证结果
        # assert workorder_page.new_page.locator("text=待我处理").is_visible()