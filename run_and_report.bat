@echo off
echo "1. 运行测试用例，生成 Allure 结果数据..."
pytest  # 会自动根据 pytest.ini 配置生成 allure-results

echo "2. 生成 Allure HTML 报告..."
allure generate playwright_study/reports/allure-results -o playwright_study/reports/allure-report --clean

echo "3. 自动打开报告（浏览器）..."
allure open playwright_study/reports/allure-report