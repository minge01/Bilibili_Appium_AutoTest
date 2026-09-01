from appium.webdriver.common.mobileby import MobileBy
from base.base_page import BasePage
from page_objects.player_page import PlayerPage


class SearchPage(BasePage):
    # ✅修正为正确ID search_src_text
    _search_input = (MobileBy.ID, "tv.danmaku.bili:id/search_src_text")
    # 右上角粉色搜索按钮
    _search_btn_top_right = (MobileBy.ID, "tv.danmaku.bili:id/action_search")
    # 第一条视频标题
    _first_video_title = (MobileBy.ID, "tv.danmaku.bili:id/title")

    def search_video(self, keyword):
        # 等待输入框可见，发送文字
        el = self.find(self._search_input)
        el.clear()
        el.send_keys(keyword)
        # 点击右上角搜索按钮
        self.find_and_click(self._search_btn_top_right)
        return self

    def click_first_video(self):
        self.find_and_click(self._first_video_title)
        # 【修复！】点击视频之后返回 PlayerPage 对象，不是返回self(SearchPage)
        return PlayerPage(self.driver)
