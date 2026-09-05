import allure
import pytest
import time
from page_objects.main_page import MainPage

@allure.feature("游客模式：B站视频播放模块")
class TestVideoPlay:
    @allure.story("游客搜索并播放视频")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.slow
    def test_guest_search_and_play(self, driver):
        """测试: 游客模式搜索视频 -> 进入播放页 -> 验证播放 -> 全屏操作"""
        main = MainPage(driver)

        with allure.step("Appium处理协议弹窗 + OpenCV图像检测处理年龄性别Compose弹窗"):
            main.skip_age_gender_guide()

        with allure.step("2. 首页点击搜索框进入搜索页"):
            search_page = main.enter_search_page()
            print("✅已经跳转至搜索页面")

        with allure.step("3. 输入关键词'自动化测试'并搜索"):
            search_page.search_video("自动化测试")

        with allure.step("4. 点击第一个搜索结果进入播放页"):
          player_page = search_page.click_first_video()

        with allure.step("5. 验证视频处于播放状态"):
            assert player_page.is_video_playing() is True

        with allure.step("6. 点击全屏按钮并验证"):
            player_page.toggle_full_screen()
