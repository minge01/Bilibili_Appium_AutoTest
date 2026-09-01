# config, 配置文件
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "outputs", "logs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "outputs", "screenshots")

# B站安卓包名与Activity
BILI_PACKAGE = "tv.danmaku.bili"
BILI_ACTIVITY = ".MainActivityV2"

TIMEOUT = 10  # 全局显式等待时间

# compose弹窗配置
# COMPOSE_POPUP_UDID = "127.0.0.1:7555"
# COMPOSE_DOT_X, COMPOSE_DOT_Y = 1007,193 # Compose性别选择页面右上角三个点坐标
# COMPOSE_THRESHOLD_BODY = 0.70
# COMPOSE_THRESHOLD_ICON = 0.65
# POPUP_BODY_TPL_PATH = "./images/age_popup_body.png" # 性别选择页面弹窗主体模板
# THREE_DOT_TPL_PATH = "./images/three_dot.png" # 性别选择页面三个点模板
# SKIP_SELECT_TPL_PATH = "./images/tpl_skip_select.png" # 性别选择页面“暂不选择”跳过按钮模板

