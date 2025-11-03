#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/27 22:47
# @Author  : 地核桃
# @file: work.py
# @desc:
import allure

from pages.base_page import BasePage


class WorkorderPage(BasePage):
    # 1. 移除绝对XPath，改用相对定位
    # 原confirm_but和_confirm_button重复，合并为一个
    _confirm_button = (
        'div.ant-modal:visible '  # 可见弹窗（上下文限定）
        'div.ant-modal-footer '   # 弹窗底部（区域限定）
        'button.ant-btn-primary:has-text("确定")'  # 主按钮+文本（特征匹配）
    )

    # 2. 技术分类下的“0625二次”：避免硬编码层级，用包含关系
    _tech_0625_secondary = (
        'div:has-text("技术") '  # 包含“技术”文本的父容器
        '.menu-item span:has-text("0625二次")'  # 子元素文本匹配
    )

    # 3. 说明内容输入框：模糊匹配placeholder（避免精确匹配失败）
    _description_textarea = (
        'textarea[class*="ant-input"]'  # class包含ant-input
        '[placeholder*="请输入"]'      # placeholder包含“请输入”
    )

    # 4. 其他定位符规范化（统一前缀下划线，明确含义）
    _workorder_btn = "text=工单系统"  # 保持不变（文本定位稳定）
    _workorder_title = "text=工单系统"
    _my_work_btn = "text=我的工作"  # 原_workorde_my_work拼写错误，修正
    _my_initiated_tab = 'div[role="tab"]:has-text("我发起的")'  # 明确是tab
    _create_workorder_btn = "text=创建工单"  # 加下划线，符合私有属性规范

    def click_workorder_btn(self):
        """点击工单按钮，打开新页面并验证"""
        with self.page.expect_popup() as popup_info:
            self.click(self._workorder_btn)
        self.new_page = popup_info.value
        # 等待页面完全加载（替代固定延迟）
        self.new_page.wait_for_load_state("load")  # 比networkidle更通用
        # 验证新页面正确性（关键！避免切换到错误页面）
        assert self.new_page.locator(self._workorder_title).is_visible(), "未进入工单系统页面"

    def refresh_new_page_twice(self):
        """刷新页面（移除冗余注释，用内置等待）"""
        self.new_page.reload(wait_until="load")  # 等待刷新完成
        # 若需第二次刷新，取消注释（但通常一次足够）
        # self.new_page.reload(wait_until="load")

    def fill_workorder_details(self, description):
        self._check_new_page()
        with allure.step("选择处理人并输入说明"):
            # 处理人选择：动态适配选项位置（避免硬编码3次箭头）
            input_locator = self.new_page.locator(self._handler_input)
            input_locator.wait_for(state="visible", timeout=15000)
            input_locator.click(force=True)
            # 等待下拉框展开（用元素可见替代固定延迟）
            self.new_page.locator('div.ant-select-dropdown:visible').wait_for()

            # 动态获取“地核桃”选项的索引（替代硬编码3次）
            options = self.new_page.locator('div.ant-select-dropdown:visible .ant-select-item').all()
            target_index = None
            for i, option in enumerate(options):
                if "地核桃" in option.text_content():
                    target_index = i
                    break
            if target_index is None:
                raise Exception("未找到“地核桃”选项")
            # 按对应次数的下箭头
            for _ in range(target_index):
                self.new_page.keyboard.press("ArrowDown")
                self.new_page.wait_for_timeout(200)  # 短延迟确保聚焦
            self.new_page.keyboard.press("Enter")

            # 说明内容输入（强化等待）
            desc_locator = self.new_page.locator(self._description_textarea)
            desc_locator.wait_for(state="visible", timeout=15000)
            desc_locator.click(force=True)
            desc_locator.clear()
            desc_locator.type(description, delay=50)
            # 验证输入成功（增加容错，允许空白字符差异）
            assert description.strip() in desc_locator.input_value().strip(), "说明内容输入失败"