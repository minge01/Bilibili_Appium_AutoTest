#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键运行 Appium 测试，并在结束后自动打开 Allure 报告。

用法:
    python run_tests.py                 # 运行全部用例，执行完自动打开报告
    python run_tests.py -k test_search  # 只运行匹配的用例（参数会透传给 pytest）
    python run_tests.py test_cases/test_video.py  # 指定某个测试文件
    python run_tests.py -m smoke        # 只跑冒烟用例（核心链路）
    python run_tests.py -m regression   # 只跑回归用例
    python run_tests.py -m "not slow"   # 跳过慢用例（耗时短，适合调试）

说明:
    - 用例结果目录由 pytest.ini 的 --alluredir 决定 (reports/allure-results)。
    - pytest 退出后自动调用 `allure serve`：生成报告 + 启动本地服务 + 自动打开浏览器。
    - 报告服务会持续运行，按 Ctrl+C 关闭即可。
"""
import os
import sys
import shutil
import subprocess

# 项目根目录（本文件所在目录）
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# 使用相对路径，避免 Windows 下 allure(Java) 对中文绝对路径的编码问题
ALLURE_REL = "reports/allure-results"


def check_interpreter():
    """校验当前解释器是否具备运行条件（pytest + appium 已安装）。

    项目依赖已统一安装在虚拟环境 .venv 中；系统 Python（含 py 启动器
    默认指向的解释器）并未安装这些依赖。若误用会抛出 ModuleNotFoundError，
    这里提前拦截并给出明确的运行指引。
    """
    try:
        import appium  # noqa: F401
        import pytest  # noqa: F401
        return True
    except ModuleNotFoundError as e:
        print("\n[错误] 当前 Python 环境缺少依赖: {}".format(e.name))
        print("       本项目依赖安装在虚拟环境 .venv 中，请改用 .venv 的解释器运行：\n")
        print("       方法一（推荐，先激活虚拟环境再运行）:")
        print("           .venv\\Scripts\\activate")
        print("           python run_tests.py\n")
        print("       方法二（不激活，直接指定解释器）:")
        print("           .venv\\Scripts\\python.exe run_tests.py\n")
        print("       注意：不要用 py 启动器（py 指向系统 Python，未安装项目依赖）。")
        return False


def find_allure():
    """返回可用于命令的 allure 路径字符串；找不到返回 None。

    查找优先级：
        1. PATH 中的 allure / allure.bat
        2. 环境变量 ALLURE_HOME 指向的安装目录
        3. 常见安装路径（本项目机器示例，可按需修改或改用 ALLURE_HOME）
    """
    # 1) PATH 中直接可用
    if shutil.which("allure") or shutil.which("allure.bat"):
        return "allure"
    # 2) ALLURE_HOME 环境变量
    home = os.environ.get("ALLURE_HOME")
    if home:
        for cand in (os.path.join(home, "bin", "allure.bat"),
                     os.path.join(home, "bin", "allure")):
            if os.path.isfile(cand):
                return cand
    # 3) 常见安装路径兜底（路径含中文也没关系，这里只用绝对路径调用）
    for cand in (
        r"E:\ruanjian\Learn\KaiFaRuanJian\allure-2.45.0\bin\allure.bat",
    ):
        if os.path.isfile(cand):
            return cand
    return None


def main():
    # 统一以项目根为工作目录，保证相对路径正确
    os.chdir(ROOT_DIR)

    # 0) 解释器自检：依赖已迁入 .venv，用系统 Python / py 运行会缺包
    if not check_interpreter():
        return 2

    import pytest  # 自检通过后再导入（系统 Python 缺少 pytest 时避免顶层崩溃）

    # 1) 运行 pytest，命令行参数原样透传
    pytest_args = sys.argv[1:]
    print("\n===== 开始执行 pytest =====")
    exit_code = pytest.main(pytest_args)

    # 2) 没有结果文件就不开报告
    if not (os.path.isdir(ALLURE_REL) and os.listdir(ALLURE_REL)):
        print("\n[警告] 未发现 Allure 结果文件，跳过打开报告。")
        print("         结果目录: " + os.path.join(ROOT_DIR, ALLURE_REL))
        return exit_code

    allure = find_allure()
    if not allure:
        print("\n[警告] 未找到 allure 命令，请先安装 Allure Commandline 并加入 PATH。")
        print("         报告结果目录: " + os.path.join(ROOT_DIR, ALLURE_REL))
        return exit_code

    # 3) allure serve: 生成报告 + 启动本地服务 + 自动打开浏览器
    #    使用 shell=True 以便 Windows 上能正确调用 allure.bat
    print("\n===== 生成并打开 Allure 报告 =====")
    cmd = "{} serve {}".format(allure, ALLURE_REL)
    try:
        subprocess.run(cmd, shell=True, cwd=ROOT_DIR, check=False)
    except KeyboardInterrupt:
        print("\n[信息] 已关闭 Allure 报告服务。")
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        try:
            input("\n[错误] 运行异常，按回车退出...")
        except Exception:
            pass
        sys.exit(1)
