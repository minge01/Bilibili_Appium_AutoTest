# 通用弹窗拦截器
from appium.webdriver.common.appiumby import AppiumBy
from utils.log_util import logger
import time

# 弹窗黑名单（跳过广告、青少年模式、权限弹窗、登录弹窗）
BLACK_LIST = [
    (AppiumBy.ID, "tv.danmaku.bili:id/close"),          # 跳过广告/关闭弹窗
    (AppiumBy.ID, "tv.danmaku.bili:id/btn_cancel"),     # 取消按钮
    (AppiumBy.ID, "tv.danmaku.bili:id/iv_close"),       # 青少年模式关闭
    (AppiumBy.ID, "tv.danmaku.bili:id/agree"),       # 同意用户协议按钮
    (AppiumBy.XPATH, "//*[@text='我知道了']"),           # 系统弹窗确认
    (AppiumBy.XPATH, "//*[@text='稍后']"),              # 权限弹窗拒绝
    (AppiumBy.XPATH, "//*[@text='取消']")               # 登录弹窗取消
]
# 新增 文本黑名单，用来捕获系统ANR弹窗
TEXT_BLACK_LIST = [
    "关闭应用"
]

def handle_popup(driver):
    """黑名单机制：遍历黑名单，存在则点击关闭
    新增防御：校验driver会话是否存活；会话销毁直接return，不发起appium请求，避免socket卡死
    """
    if not hasattr(driver, "session_id") or driver.session_id is None:
        logger.debug("driver会话已经销毁，跳过弹窗处理")
        return

    # --------第一步：处理B站APP自身弹窗（原有逻辑）--------
    for locator in BLACK_LIST:
        try:
            els = driver.find_elements(*locator)
            if els:
                els[0].click()
                logger.info(f"拦截并关闭弹窗: {locator}")
                time.sleep(0.8)
        except Exception as e:
            logger.debug(f"弹窗元素不存在 {locator}, {str(e)}")
            continue

    # --------第二步：处理安卓系统ANR【哔哩哔哩没有响应】弹窗--------
    for txt in TEXT_BLACK_LIST:
        try:
            xpath_expr = f'//*[@text="{txt}"]'
            els = driver.find_elements(AppiumBy.XPATH, xpath_expr)
            if els:
                els[0].click()
                logger.warning(f"🚨捕获ANR系统弹窗，点击：{txt}")
                time.sleep(1.5)
                # 点击关闭应用后进程被杀，重新激活B站APP
                driver.activate_app("tv.danmaku.bili")
                logger.info("🔁ANR触发，重新启动哔哩哔哩，等待初始化……")
                time.sleep(5)   # 给冷启动充足加载时间
        except Exception as e:
            logger.debug(f"ANR弹窗未出现 {txt}, err:{str(e)}")
            continue
