import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_BASE_URL = "http://localhost:5173"


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=DEFAULT_BASE_URL)


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    """
    Chrome via Selenium Manager (no manual driver installs).
    Headless in CI by default; local can be headed.
    """
    headless = os.getenv("HEADLESS", "0") == "1"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")

    # Stability flags (especially for CI)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # we use explicit waits only

    yield drv

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Save screenshot on test failure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("artifacts/screenshots", exist_ok=True)
            filename = f"artifacts/screenshots/{item.name}.png"
            drv.save_screenshot(filename)
