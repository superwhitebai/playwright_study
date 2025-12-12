import allure
from utils.logger_utils import logger
from utils.assert_utils import assert_visible
from pages.login_page import LoginPage
from pages.workorder_page import WorkorderPage
from utils.yaml_utils import config


@allure.feature("工单系统模块")  # 模块
class TestWorkorder:

    @allure.story("创建工单成功并验证 Toast 提示")  # 具体用例名称
    @allure.title("创建工单成功并验证 Toast 提示")
    def test_create_workorder_success(self, page):
        base_url = config["env"][config["current_env"]]

        with allure.step("打开系统首页"):  # 用例实现步骤
            page.goto(base_url)
            logger.info(f"打开系统首页：{base_url}")

        with allure.step("检测登录态并登录"):
            if "login" in page.url:
                login_page = LoginPage(page)
                login_page.login_with_phone_code("15258832127", "2127")
                login_page.assert_login_success("应用面板")
                page.context.storage_state(path=config["storage_state"])
                logger.info("已登录并保存 storage_state")

        with allure.step("进入工单系统"):
            workorder_page = WorkorderPage(page)
            workorder_page.click_workorder_btn()

        with allure.step("创建工单"):
            workorder_page.click_my_workorder_btn()
            workorder_page.click_my_initiated_btn()
            workorder_page.click_create_workorder_btn()
            workorder_page.click_0625_secondary()
            workorder_page.click_second_confirm_btn()
            workorder_page.fill_workorder_details("自动化测试工单")
            workorder_page.click_second_confirm_btn()

        with allure.step("验证工单创建成功 Toast 提示"):  # 断言
            toast = workorder_page.new_page.get_by_text("操作成功", exact=True)
            assert_visible(workorder_page.new_page, toast, "工单创建成功 Toast 提示")

