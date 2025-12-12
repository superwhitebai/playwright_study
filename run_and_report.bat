@echo off
echo ========== 开始执行 UI 自动化测试 ==========
pytest -vs --alluredir=reports/
echo ========== 生成 Allure 报告 ==========
allure serve reports/
pause
