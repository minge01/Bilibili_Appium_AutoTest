# PO 基类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import TIMEOUT
from utils.log_util import logger
from backup.airtest_utils import airtest_img_click
from airtest.core.cv import Template
import os
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    logger = logging.getLogger("BiliAutoTest")
    def find(self, locator, timeout=None):
        """显式等待查找元素，自带日志，等待元素可见
         timeout=None → 使用全局TIMEOUT(10)；探测场景手动传小数字，如timeout=2
        """
        use_timeout = timeout if timeout is not None else TIMEOUT
        try:
            el = WebDriverWait(self.driver, use_timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return el
        except Exception as e:
            logger.error(f"元素未找到(不可见/超时): {locator}, 错误: {e}")
            raise

    def find_and_click(self, locator, timeout=TIMEOUT):
        self.find(locator, timeout).click()

    def find_and_send(self, locator, text, timeout=TIMEOUT):
        el = self.find(locator, timeout)
        el.clear()
        el.send_keys(text)

    def swipe_up(self, duration=500):
        """向上滑动浏览视频
        使用 driver.swipe（W3C Actions 封装）替代已废弃的 TouchAction，
        两者行为等价：按下起点 -> 停留 duration(ms) -> 移动到终点 -> 释放。
        """
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        self.driver.swipe(
            start_x=int(width / 2),
            start_y=int(height * 0.8),
            end_x=int(width / 2),
            end_y=int(height * 0.2),
            duration=duration
        )

    def switch_to_webview(self, webview_name="WEBVIEW_tv.danmaku.bili"):
        """切换到WebView上下文（处理活动页/专题页）"""
        contexts = self.driver.contexts
        if webview_name in contexts:
            self.driver.switch_to.context(webview_name)
            logger.info(f"成功切换到上下文: {webview_name}")
        else:
            logger.warning(f"未找到上下文: {webview_name}")

    def switch_to_native(self):
        """切回原生"""
        self.driver.switch_to.context('NATIVE_APP')

# ===========新增图像点击封装方法============
    def img_click(self, template: Template, threshold=0.75, retry=3):
        """
        页面类直接调用，执行airtest图像点击
        """
        return airtest_img_click(template, threshold=threshold, retry=retry)

    def get_template(self, png_name: str, record_pos, resolution):
        """
        快速构造Template对象，自动去images文件夹找图片
        :param png_name: 图片文件名，例:"tpl1787648275794.png"
        :param record_pos: IDE生成的坐标元组
        :param resolution: IDE生成分辨率元组
        :return: Template
        """
        img_full_path = os.path.abspath(f"./images/{png_name}")
        return Template(img_full_path, record_pos=record_pos, resolution=resolution)



