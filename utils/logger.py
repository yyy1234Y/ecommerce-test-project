import logging
import sys
import allure

def setup_logger(name="ecommerce_test", level=logging.INFO):
    """设置并返回一个logger实例"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class AllureLogger:
    """同时输出到控制台和 Allure 报告的日志类"""
    def __init__(self, name="ecommerce_test"):
        self.logger = setup_logger(name)

    def info(self, msg: str):
        self.logger.info(msg)
        allure.attach(msg, "INFO", attachment_type=allure.attachment_type.TEXT)

    def error(self, msg: str):
        self.logger.error(msg)
        allure.attach(msg, "ERROR", attachment_type=allure.attachment_type.TEXT)

    def debug(self, msg: str):
        self.logger.debug(msg)
        allure.attach(msg, "DEBUG", attachment_type=allure.attachment_type.TEXT)

    def warning(self, msg: str):
        self.logger.warning(msg)
        allure.attach(msg, "WARNING", attachment_type=allure.attachment_type.TEXT)

# 全局日志实例，方便导入使用
log = AllureLogger()