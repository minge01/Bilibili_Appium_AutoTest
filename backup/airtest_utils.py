import time
import subprocess
import traceback
import os

# ===================== 模拟器设备号 =====================
DEVICE_SERIAL = "127.0.0.1:7555"
THRESHOLD = 0.72
AIRTEST_SCRIPT_PATH = "utils/airtest_mstpl_handler.py"
POPUP_TPL_PATH = "images/tpl1787648275794.png"


def airtest_img_click(img_template, threshold=0.72, retry=3, interval=1):
    for i in range(retry):
        try:
            from airtest.core.api import touch
            touch(img_template, threshold=threshold)
            print(f"图像点击成功, 重试轮次:{i}")
            return True
        except Exception:
            time.sleep(interval)
    print("图像点击重试全部失败！")
    return False


def try_popup_by_airtest(driver):
    """
    ✅【新版方案，不quit Appium，不重启APP】
    仅新开子进程尝试Airtest点击弹窗，找不到弹窗直接返回False，原有driver继续复用
    :return: True点击成功 / False弹窗未出现或者识别失败
    """
    print("👉尝试使用独立Airtest进程检测年龄性别弹窗")
    # Windows临时修复编码问题
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    cmd = [
        "python", AIRTEST_SCRIPT_PATH,
        "--device", DEVICE_SERIAL,
        "--tpl", POPUP_TPL_PATH,
        "--threshold", str(THRESHOLD)
    ]
    try:
        result = subprocess.run(
            cmd,
            timeout=8,
            capture_output=True,
            text=True,
            env=env
        )
        print("====Airtest子进程stdout====")
        print(result.stdout)
        if result.stderr:
            print("====stderr====")
            print(result.stderr)

        if result.returncode == 0:
            print("✅Airtest成功点击弹窗")
            time.sleep(0.8)
            return True
        else:
            print("ℹ️Airtest未找到弹窗(弹窗未弹出)，继续原有流程")
            return False

    except subprocess.TimeoutExpired:
        print("❌Airtest执行超时")
        return False
    except Exception as e:
        traceback.print_exc()
        return False
