# page_objects/main_page.py

from appium.webdriver.common.mobileby import MobileBy
from base.base_page import BasePage
from page_objects.search_page import SearchPage
from utils.handle_popup import handle_popup
from utils.compose_popup_detect import handle_age_popup_full


class MainPage(BasePage):
    # 普通控件元素定位
    _search_btn = (MobileBy.ID, "tv.danmaku.bili:id/expand_search")  # 首页搜索框
    _home_tab = (MobileBy.XPATH, "//*[@text='首页']")
    _hot_tab = (MobileBy.XPATH, "//*[@text='热门']")

    # 年龄性别弹窗文本：仅用来Appium探测弹窗是否存在，不点击！
    _skip_age_gender_btn = (MobileBy.XPATH, '//*[@text="性别"]')

    # Compose右上角跳过按钮（Airtest模板定义）
    _compose_skip_btn = None

    def __init__(self, driver):
        super().__init__(driver)
        self._compose_skip_btn = self.get_template(
            "tpl1787648275794.png",
            record_pos=(0.442, -0.744),
            resolution=(900, 1600)
        )

    def enter_search_page(self):
        """首页点击搜索，进入搜索页面"""
        handle_popup(self.driver)
        # 增加等待首页搜索图标可见，确认已经完全离开弹窗页面
        self.find(self._search_btn, timeout=8)
        self.find_and_click(self._search_btn)
        return SearchPage(self.driver)

    def switch_to_hot(self):
        """切换热门分区"""
        handle_popup(self.driver)
        self.find_and_click(self._hot_tab)
        return self

    def skip_age_gender_guide(self):
        """
        前置弹窗处理
        1.handle_popup处理用户协议id控件弹窗
        2.adb+opencv多尺度模板匹配处理Compose年龄性别弹窗，无Airtest子进程
        """
        handle_popup(self.driver)
        # --------------------------
        # 调试：enable=False，完全跳过整套opencv截图匹配，几乎0耗时
        # 回归冷启动测试：enable=True开启弹窗检测
        # --------------------------
        # 👉开始处理年龄性别Compose弹窗(两步流程)
        handle_age_popup_full(driver=self.driver,enable=True)