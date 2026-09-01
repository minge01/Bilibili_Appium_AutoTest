import subprocess
import time
import traceback
from appium import webdriver
from appium.options.android import UiAutomator2Options

# ===================== 【配置区 自己修改这里】 =====================
DEVICE_SERIAL = "127.0.0.1:7555"   # adb devices查到的模拟器/设备号
APP_PACKAGE = "com.xxx.xxx"
APP_ACTIVITY = ".MainActivity"
POPUP_TPL_PATH = "images/tpl1787648275794.png"    # 弹窗关闭按钮截图模板
THRESHOLD = 0.72
AIRTEST_SCRIPT_PATH = "airtest_mstpl_handler.py"
APPIUM_SERVER_URL = "http://127.0.0.1:4723"
# =================================================================

def create_appium_driver() -> webdriver.Remote:
    """新建Appium会话"""
    options = UiAutomator2Options()
    options.set_capability("deviceName", DEVICE_SERIAL)
    options.set_capability("udid", DEVICE_SERIAL)
    options.set_capability("platformName", "Android")
    options.set_capability("appPackage", APP_PACKAGE)
    options.set_capability("appActivity", APP_ACTIVITY)
    options.set_capability("noReset", True)
    options.set_capability("automationName", "UiAutomator2")
    driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
    return driver


def run_airtest_popup_subprocess():
    """独立子进程运行Airtest，彻底隔离Appium会话，无uiautomator冲突"""
    cmd = [
        "python", AIRTEST_SCRIPT_PATH,
        "--device", DEVICE_SERIAL,
        "--tpl", POPUP_TPL_PATH,
        "--threshold", str(THRESHOLD)
    ]
    try:
        result = subprocess.run(cmd, timeout=20, capture_output=True, text=True)
        print("==== Airtest子进程输出 ====")
        print(result.stdout)
        if result.stderr:
            print("Airtest stderr:", result.stderr)
        if result.returncode == 0:
            print("✅弹窗处理成功")
            return True
        else:
            print("❌弹窗未找到或点击失败")
            return False
    except subprocess.TimeoutExpired:
        print("❌Airtest弹窗脚本超时")
        return False
    except Exception as e:
        print(f"❌运行airtest子进程异常: {e}")
        traceback.print_exc()
        return False


def main():
    driver = None
    try:
        print("=== 启动Appium会话 ===")
        driver = create_appium_driver()
        time.sleep(2)

        # ----------------你的Appium业务代码写在这里----------------
        # driver.find_element(...).click()

        print("准备处理弹窗，关闭Appium会话释放uiautomator")
        driver.quit()
        driver = None
        time.sleep(1.5)

        # 调用MSTPL多尺度匹配弹窗脚本
        popup_ok = run_airtest_popup_subprocess()
        if not popup_ok:
            print("弹窗识别失败，可自行添加重试逻辑")

        time.sleep(1)

        # 重启全新Appium会话继续业务
        print("=== 重启全新Appium会话，继续后续业务 ===")
        driver = create_appium_driver()

        # ----------------后续Appium业务代码写在这里----------------

    except Exception as e:
        print(f"主流程异常: {e}")
        traceback.print_exc()
    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass


if __name__ == "__main__":
    main()
