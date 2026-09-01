# pytest 前后置（驱动生命周期、截图钩子）
# 亮点:使用 pytest 的 fixture 实现用例前后置，自动清理弹窗，并使用 allure 报告展示截图。
# conftest.py 放在【项目根目录】和utils、base同级
import pytest
import allure
import os

from base.base_driver import init_driver, quit_driver
from config.settings import SCREENSHOT_DIR
from utils.handle_popup import handle_popup
from utils.log_util import logger


@pytest.fixture(scope="module")
def driver():
    """全局驱动 fixture，整个测试会话只初始化一次"""
    dr = init_driver()
    yield dr
    quit_driver(dr)  # 使用封装好的安全退出


@pytest.fixture(autouse=True)
def intercept_popups(driver):
    """每个用例前后自动弹窗清理，自动生效不需要调用"""
    handle_popup(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败自动截图，附加allure报告"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        # 关键修复：driver对象存在 并且 session_id 不为空，代表会话还存活，才执行截图
        if driver and hasattr(driver, "session_id") and driver.session_id:
            # 确保截图文件夹存在
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            filename = os.path.join(SCREENSHOT_DIR, f"{item.name}_fail.png")
            try:
                driver.save_screenshot(filename)
                with open(filename, "rb") as f:
                    allure.attach(f.read(), "失败截图", allure.attachment_type.PNG)
                logger.error(f"用例失败，截图已保存 {filename}")
            except Exception as e:
                logger.warning(f"会话已失效，无法截取失败截图：{str(e)}")
        else:
            logger.warning("driver会话已经销毁，跳过失败截图")


import subprocess
def pytest_sessionfinish(session, exitstatus):
    """可选增强：测试结束后自动打开 Allure 报告。

    默认不生效；设置环境变量 AUTO_OPEN_ALLURE=1 后，直接运行 `pytest`
    也会在浏览器自动打开报告（不阻塞 pytest 退出）。
    例如（PowerShell）:  $env:AUTO_OPEN_ALLURE=1; pytest
    例如（Git Bash）:    AUTO_OPEN_ALLURE=1 pytest
    """
    if os.environ.get("AUTO_OPEN_ALLURE") != "1":
        return
    results_dir = os.path.join("reports", "allure-results")
    if not (os.path.isdir(results_dir) and os.listdir(results_dir)):
        return
    root = os.path.dirname(os.path.abspath(__file__))
    if os.name == "nt":
        # start 在新窗口启动，pytest 退出后报告服务仍独立运行
        subprocess.Popen(
            'start "" allure serve {}'.format(results_dir),
            shell=True,
            cwd=root,
        )
    else:
        subprocess.Popen("allure serve {}".format(results_dir), shell=True, cwd=root)
