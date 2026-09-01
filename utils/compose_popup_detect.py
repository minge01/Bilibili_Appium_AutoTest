import cv2
import subprocess
import time

from utils.handle_popup import handle_popup
from utils.log_util import logger
import config.settings

# --------【Compose年龄性别页面配置，换模拟器/改分辨率，只修改下面这一块】--------
UDID = "127.0.0.1:7555" # MUMU模拟器唯一标识
# 弹窗主体特征图：截年龄性别弹窗中间大片区域（判断弹窗是否出现）
POPUP_BODY_TPL_PATH = "./images/age_popup_body.png"
# 右上角三点小图标模板
THREE_DOT_TPL_PATH = "./images/three_dot.png"
# 暂不选择模板
SKIP_SELECT_TPL_PATH = "./images/tpl_skip_select.png"
# 三点兜底坐标【⚠️修改模拟器分辨率必须同步更新该坐标，同时重新截图全部png模板】
DOT_X, DOT_Y = 1007, 193
# 匹配阈值
THRESHOLD_BODY = 0.70   #弹窗主体，适当放宽
THRESHOLD_ICON = 0.65   #三点图标，放宽一点
# --------------------------配置区结束，下面不要改动常量------------------------

def get_screen_cv_mat():
    """adb截图，返回opencv图像矩阵"""
    try:
        out = subprocess.run(
            ["adb","-s",UDID,"exec-out","screencap","-p"],
            capture_output=True, timeout=5
        )
        import numpy as np
        arr = np.frombuffer(out.stdout, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logger.error(f"adb截图失败 {str(e)}")
        return None

def match_template(screen_img, template_path, threshold):
    """模板匹配，命中返回中心点(x,y)；不命中返回None"""
    tpl = cv2.imread(template_path,cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        logger.warning(f"模板文件不存在 {template_path}")
        return None
    # 如果传入的 screen_img 是彩色图，也将其转为灰度图
    if len(screen_img.shape) == 3: # 彩色图的shape是(高度, 宽度, 通道数3) len(...)：计算元组中元素的个数。
        screen_img = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(screen_img, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        h,w = tpl.shape[:2]
        cx = max_loc[0] + w//2
        cy = max_loc[1] + h//2
        return (cx, cy)
    return None


def handle_age_popup_full(driver=None,enable:bool=True):
    if not enable: # not反义的意思，如果enable为False，则负负得正执行if内代码
        print("ℹ️调试模式，跳过年龄性别弹窗视觉检测")
        return

    # 如果传入driver，再次兜底检查ANR崩溃弹窗
    if driver is not None: # 如果传入driver非空，再次兜底检查ANR崩溃弹窗
        handle_popup(driver)

    print("👉开始处理年龄性别Compose弹窗(两步流程)")
    screen = get_screen_cv_mat()
    if screen is None:
        logger.warning("获取屏幕截图失败，跳过compose弹窗检测")
        return

    # ==========最重要第一步：检测弹窗主体是否存在==========
    popup_pos = match_template(screen, POPUP_BODY_TPL_PATH, THRESHOLD_BODY)
    if popup_pos is None:
        print("ℹ️屏幕没有检测到年龄性别弹窗主体，直接跳过，不执行任何点击")
        return

    print("✅检测到年龄性别Compose弹窗存在，开始处理")
    #弹窗确实存在，才继续往下执行

    #1、优先匹配三点图标
    three_dot_pos = match_template(screen, THREE_DOT_TPL_PATH, THRESHOLD_ICON)
    if three_dot_pos is not None:
        print(f"✅图像识别命中三点图标 pos={three_dot_pos}")
        subprocess.run(["adb","-s",UDID,"shell","input","tap",str(three_dot_pos[0]),str(three_dot_pos[1])],timeout=3)
    else:
        #⚠️只有确认弹窗存在，才走兜底adb坐标点击！！
        print(f"⚠️三点图标识别失败，弹窗已确认存在，执行兜底坐标点击({DOT_X},{DOT_Y})")
        subprocess.run(["adb","-s",UDID,"shell","input","tap",str(DOT_X),str(DOT_Y)],timeout=3)

    time.sleep(1.6) #等待下拉菜单展开

    #2、点击暂不选择
    screen2 = get_screen_cv_mat()
    skip_pos = match_template(screen2, SKIP_SELECT_TPL_PATH, THRESHOLD_ICON)
    if skip_pos is not None:
        print(f"✅识别暂不选择，执行点击 pos={skip_pos}")
        subprocess.run(["adb","-s",UDID,"shell","input","tap",str(skip_pos[0]),str(skip_pos[1])],timeout=3)
    else:
        print("⚠️未识别【暂不选择】模板，有可能菜单未展开")
    time.sleep(2.0)

    #3、校验：再次截图确认弹窗已经消失
    screen3 = get_screen_cv_mat()
    check_popup = match_template(screen3, POPUP_BODY_TPL_PATH, THRESHOLD_BODY)
    if check_popup is None:
        print("✅校验：年龄性别弹窗已经消失")
    else:
        logger.warning("⚠️警告：弹窗处理完毕，弹窗主体依旧存在！流程可能卡住")
