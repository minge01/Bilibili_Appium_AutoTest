import subprocess
import time
import cv2
import numpy as np
import os

DEVICE = "127.0.0.1:7555"
# 你的跳过按钮坐标
SKIP_X = 930
SKIP_Y = 85
# 弹窗按钮截图模板图片路径
TEMPLATE_IMG = r"images\skip_btn.png"

def adb_screenshot(save_path:str="screen.png"):
    """截取模拟器屏幕"""
    subprocess.run(["adb","-s",DEVICE,"shell","screencap","-p","/sdcard/screen.png"])
    subprocess.run(["adb","-s",DEVICE,"pull","/sdcard/screen.png",save_path])

def adb_tap(x:int,y:int):
    subprocess.run(["adb","-s",DEVICE,"shell","input","tap",str(x),str(y)])

def image_match(screen_path:str,template_path:str,threshold=0.8):
    """图像模板匹配，返回是否找到按钮"""
    screen = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    if screen is None or template is None:
        return False
    res = cv2.matchTemplate(screen,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return len(loc[0])>0

def safe_skip_age_popup(max_wait=5,interval=2):
    """安全版本：只有识别到弹窗才点击右上角，否则不点击任何地方"""
    start = time.time()
    print(f"等待年龄性别弹窗，最长 {max_wait}s")
    while time.time()-start < max_wait:
        adb_screenshot("screen_temp.png")
        found = image_match("screen_temp.png",TEMPLATE_IMG)
        if found:
            print("✅检测到弹窗，执行点击跳过")
            adb_tap(SKIP_X,SKIP_Y)
            time.sleep(1)
            return True
        time.sleep(interval)
    print("❌超时未检测到弹窗，不执行任何点击操作")
    return False
