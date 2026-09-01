# base,基础封装层（驱动初始化、BasePage）
# 驱动管理（复用登录态核心配置）
from airtest.core.api import auto_setup
from appium import webdriver
from config.settings import BILI_PACKAGE, BILI_ACTIVITY
from appium.options.android import UiAutomator2Options

def init_driver():
    desired_caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "udid": "127.0.0.1:7555",
        "appPackage": BILI_PACKAGE,
        "appActivity": BILI_ACTIVITY,
        "noReset": False,                     # 先改成False，每次重启APP，避免残留坏状态
        "newCommandTimeout": 60,
        "uiautomator2ServerReadTimeout": 30000,
        "skipServerInstallation": False,      # 强制关闭，让appium重新推送安装uiautomator2‑server
        "skipDeviceInitialization": True
    }
    options = UiAutomator2Options().load_capabilities(desired_caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    # 手动强制拉起B站，防止noReset=True状态下APP没启动，停留在桌面。noReset=True时会二次重启APP，需要注释掉
    # driver.start_activity(app_package="tv.danmaku.bili", app_activity=".MainActivityV2")
    return driver

def quit_driver(driver):
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
