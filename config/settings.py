# 被测系统地址
BASE_URL = "http://127.0.0.1:5000"

# 等待时间（秒）
DEFAULT_TIMEOUT = 30000  # 30秒IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 10

# 失败截图
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = "screenshots"

# 报告目录
REPORT_DIR = "reports"

# 默认测试账号（可被 test_data.yaml 覆盖）
DEFAULT_USER = {
    "email": "test@example.com",
    "password": "test123"
}