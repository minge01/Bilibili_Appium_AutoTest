import allure
import pytest
import time
from page_objects.main_page import MainPage

@allure.feature("游客模式：B站首页模块")
class TestHomeBrowse:
    @allure.story("游客首页浏览与分区切换")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_guest_browse_home_and_switch_tab(self, driver):
        """测试: 游客进入首页 -> 处理弹窗 -> 切换热门分区 -> 上滑浏览推荐流"""
        main = MainPage(driver)

        with allure.step("1. 处理年龄性别等前置弹窗"):
            main.skip_age_gender_guide()

        with allure.step("2. 等待首页搜索按钮可见，确认已真正进入首页"):
            # 搜索框 expand_search 是首页稳定存在的控件，用它判断"已离开弹窗页、首页加载完成"
            main.find(main._search_btn, timeout=8)
            print("✅已进入B站首页")

        with allure.step("3. 点击底部'热门'Tab 切换到热门分区"):
            main.switch_to_hot()
            # 点击后给列表加载留出时间
            time.sleep(1.5)

        with allure.step("4. 上滑浏览热门推荐流（连续滑动，验证页面可正常滚动）"):
            main.swipe_up()
            time.sleep(1)
            main.swipe_up()
            print("✅热门分区上滑浏览完成")

        with allure.step("5. 切回'首页'Tab 验证底部导航可往返"):
            main.find_and_click(main._home_tab)
            time.sleep(1)
            # 首页搜索框重新可见，代表导航切换成功
            main.find(main._search_btn, timeout=8)
            print("✅已切回首页")
