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
#### 启动 Appium Server (appium)
#### 连接安卓设备/模拟器 (adb devices)
#### 运行测试并自动打开 Allure 报告（推荐）：python run_tests.py
#### 仅运行测试（不自动开报告）：pytest
#### 手动生成并打开 Allure 报告：allure serve reports/allure-results
#### 让 pytest 命令也自动打开报告：先设置环境变量 AUTO_OPEN_ALLURE=1 再运行 pytest