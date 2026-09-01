#utils, 工具类
# 日志封装
import logging
import os

# 基础配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
logger = logging.getLogger("BiliAutoTest")

# 设置日志级别
logger.setLevel(logging.INFO)

# 避免重复添加 handler
if not logger.handlers:
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
