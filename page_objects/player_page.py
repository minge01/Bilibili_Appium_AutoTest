# 播放页（含原生与WebView交互）
import subprocess
import time
from appium.webdriver.common.appiumby import AppiumBy
from base.base_page import BasePage

class PlayerPage(BasePage):
    _video_player = (AppiumBy.ID, "tv.danmaku.bili:id/reveal_placeholder") # 播放器控件

    def is_video_playing(self):
        """验证视频是否在播放页"""
        return self.find(self._video_player).is_displayed()

    def toggle_full_screen(self):
        """
        B站新版Compose播放器，全屏按钮无法被uiautomator抓取，使用adb坐标点击
        1080*1920模拟器，右下角全屏按钮坐标 x=960 y=1740
        """
        # 先点击视频画面，唤出播放器控制栏（非常关键！不点击不会显示全屏图标）
        subprocess.run(["adb", "-s", "127.0.0.1:7555", "shell", "input", "tap", "540", "380"],timeout=3)
        time.sleep(1.2)
        # 点击右下角全屏按钮（换模拟器记得更新坐标）
        subprocess.run(["adb", "-s", "127.0.0.1:7555", "shell", "input", "tap", "1007", "610"],timeout=3)
        time.sleep(1)
        return self