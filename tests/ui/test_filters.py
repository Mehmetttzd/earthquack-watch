import pytest
from tests.ui.pages.home_page import HomePage


@pytest.mark.regression
def test_min_magnitude_filter_enforced(driver, base_url):
    page = HomePage(driver, base_url).goto().wait_until_ready()

    target = 6.0
    page.set_min_magnitude(target).refresh().wait_until_ready()

    mags = page.get_visible_magnitudes()

    # If no results, that's valid: filter may be strict for current real-time data
    if len(mags) == 0:
        return

    assert all(m >= target for m in mags), f"Found magnitudes below {target}: {mags}"
