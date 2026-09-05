### 项目说明
#### 项目名称： Bilibili App 自动化测试框架 (Appium + PO + Pytest)
#### 项目描述： 针对B站安卓端核心业务流程设计的自动化测试脚手架，覆盖游客模式浏览、搜索、播放等核心链路。
#### 技术栈： Python, Appium, UiAutomator2, Pytest, Allure, PO设计模式

### 核心职责/亮点：
#### 采用 Page-Object 设计模式，将页面元素与业务逻辑深度解耦，提升代码复用率与可维护性。
#### 设计黑名单弹窗拦截机制，动态处理青少年模式、权限授权、登录诱导弹窗，极大提升脚本稳定性。
#### 采用 Session 复用方案，通过 noReset 配置结合人工扫码一次，规避 Appium 反自动化检测与风控验证码，实现登录态持久化。
#### 结合 Pytest Hook 机制实现 用例失败自动截图 并注入 Allure 报告；封装 WebView 上下文切换，支持混合页面测试。

### 如何启动项目
#### 准备环境（首次）
#### 创建并激活虚拟环境：python -m venv .venv → .venv\Scripts\activate
#### 安装依赖：pip install -r requirements.txt
#### 启动 Appium Server (appium)
#### 连接安卓设备/模拟器 (adb devices)
#### 运行测试并自动打开 Allure 报告（推荐，需在 .venv 激活状态下）：python run_tests.py
#### 一键冒烟测试集（首页浏览 + 视频播放，Windows 双击即可）：run_smoke.bat
#### 只跑冒烟标记的用例：python run_tests.py -m smoke
#### 只跑回归标记的用例：python run_tests.py -m regression
#### 跳过耗时用例（依赖网络/视频加载的）：python run_tests.py -m "not slow"
#### 组合筛选（回归集里排除慢用例）：python run_tests.py -m "regression and not slow"
#### 查看所有可用标记：pytest --markers
#### 用例上打标记：@pytest.mark.smoke / @pytest.mark.regression / @pytest.mark.slow（可叠加，新标记需先在 pytest.ini 的 markers 中注册）
#### 仅运行测试（不自动开报告）：pytest
#### 手动生成并打开 Allure 报告：allure serve reports/allure-results
#### 让 pytest 命令也自动打开报告：先设置环境变量 AUTO_OPEN_ALLURE=1 再运行 pytest