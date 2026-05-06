import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.order_page import OrderPage
from config.settings import SCREENSHOT_DIR
import os
# from utils.data_cleaner import DataCleaner
from utils.logger import log  # 新增：导入日志

@pytest.fixture(scope="function")
def page():
    """提供 Playwright 页面对象，每个用例独立"""
    log.info("启动浏览器...")
    with sync_playwright() as p:
        # browser = p.chromium.launch(channel="chrome", headless=False)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        log.info("浏览器已启动，页面已创建")
        yield page
        log.info("关闭浏览器...")
        context.close()
        browser.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def shop_page(page):
    return ShopPage(page)

@pytest.fixture
def product_page(page):
    return ProductPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def order_page(page):
    return OrderPage(page)

@pytest.fixture
def logged_in_page(page, login_page):
    """已登录的页面 fixture，避免每个用例重复写登录"""
    log.info("使用 logged_in_page fixture，执行登录...")
    login_page.navigate_to_login()
    login_page.login("test@example.com", "test123")
    log.info("登录成功，返回已登录页面")
    return page

@pytest.fixture(scope="function", autouse=True)
def clean_before_test():
    """每个用例执行前的清理"""
    log.info("执行测试前清理...")
    # 这里可以清理测试数据，比如通过 API 删除测试用户创建的订单
    # 暂时用 pass，后续可以扩展
    pass

@pytest.fixture(scope="function")
def unique_email():
    """生成唯一邮箱，避免用例间数据冲突"""
    import time
    email = f"test_{int(time.time())}@example.com"
    log.info(f"生成唯一邮箱: {email}")
    return email

# 失败自动截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        log.error(f"测试失败: {item.name}")
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{item.name}_failed.png")
            page.screenshot(path=screenshot_path)
            log.error(f"失败截图已保存: {screenshot_path}")
            print(f"\n失败截图已保存: {screenshot_path}")

# 新增：自动记录每个测试用例的开始和结束（不需要手动调用）
@pytest.fixture(scope="function", autouse=True)
def log_test_boundary(request):
    """在每个测试用例执行前后自动记录日志"""
    log.info(f"========== 开始执行测试用例: {request.node.name} ==========")
    yield
    log.info(f"========== 测试用例执行结束: {request.node.name} ==========")

# 在文件最后添加这个
@pytest.fixture
def auth_api():
    """提供 API 测试客户端"""
    try:
        from apis.api_client import ApiClient
        return ApiClient()
    except ImportError as e:
        log.error(f"导入 ApiClient 失败: {e}")
        pytest.skip("API 客户端不可用")