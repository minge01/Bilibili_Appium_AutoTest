@echo off
title BiliBili Appium 冒烟测试集
rem ============================================
rem  BiliBili Appium 冒烟测试集一键启动
rem  用例: [1/2] 首页浏览 test_home
rem        [2/2] 视频播放 test_video
rem  运行结束自动打开 Allure 报告
rem ============================================

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [错误] 未找到虚拟环境 .venv，请先在项目根目录执行:
    echo     python -m venv .venv
    echo     .venv\Scripts\activate
    echo     pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   冒烟测试集开始...
echo   [1/2] 首页浏览 test_home
echo   [2/2] 视频播放 test_video
echo   标记: smoke  新用例记得加 @pytest.mark.smoke
echo ============================================================
echo.

".venv\Scripts\python.exe" run_tests.py -m smoke

echo.
echo 测试与报告流程已结束，按任意键关闭窗口...
pause >nul
