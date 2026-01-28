import pytest
from tests.ui.pages.home_page import HomePage


@pytest.mark.smoke
def test_home_loads_and_modal_opens(driver, base_url):
    page = HomePage(driver, base_url).goto().wait_until_ready()

    assert page.row_count() > 0, "Expected at least 1 quake row to render"

    page.open_first_details()
    page.close_modal()
