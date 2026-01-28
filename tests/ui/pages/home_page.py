from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class HomePage:
    URL_PATH = "/"

    # Core UI
    TABLE = (By.CSS_SELECTOR, '[data-testid="quakes-table"]')
    ROWS = (By.CSS_SELECTOR, '[data-testid="quake-row"]')
    VIEW_DETAILS = (By.CSS_SELECTOR, '[data-testid="view-details"]')

    MODAL = (By.CSS_SELECTOR, '[data-testid="details-modal"]')
    CLOSE_MODAL = (By.CSS_SELECTOR, '[data-testid="close-modal"]')

    # States
    ALERT = (By.CSS_SELECTOR, '[role="alert"]')
    LOADING = (By.CSS_SELECTOR, '[data-testid="loading"]')
    EMPTY_STATE = (By.CSS_SELECTOR, '[data-testid="empty-state"]')

    # Filters
    MINMAG_INPUT = (By.CSS_SELECTOR, '[data-testid="minmag-input"]')
    REFRESH_BTN = (By.XPATH, "//button[contains(., 'Refresh')]")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 25)

    def goto(self):
        self.driver.get(self.base_url + self.URL_PATH)
        return self

    def wait_until_ready(self):
        """
        READY means the UI is in one of these final states:
        - table shown (results)
        - empty state shown (no results)
        - alert shown (error)
        Loading can appear in between and must disappear.
        """
        try:
            self.wait.until(
                lambda d: self._loading_present(d)
                or self._table_present(d)
                or self._empty_present(d)
                or self._alert_present(d)
            )
        except TimeoutException:
            raise AssertionError("Page did not enter loading/table/empty/alert state.")

        # If loading exists, wait until it disappears
        if self._loading_present(self.driver):
            self.wait.until(lambda d: not self._loading_present(d))

        # Error state wins
        if self._alert_present(self.driver):
            alert_text = self.driver.find_element(*self.ALERT).text.strip()
            raise AssertionError(f"UI shows an error state:\n{alert_text}")

        # Must end in either table or empty state
        if not self._table_present(self.driver) and not self._empty_present(self.driver):
            raise AssertionError("Page finished loading but neither table nor empty state appeared.")

        return self

    def _table_present(self, d) -> bool:
        return len(d.find_elements(*self.TABLE)) > 0

    def _empty_present(self, d) -> bool:
        return len(d.find_elements(*self.EMPTY_STATE)) > 0

    def _alert_present(self, d) -> bool:
        return len(d.find_elements(*self.ALERT)) > 0

    def _loading_present(self, d) -> bool:
        return len(d.find_elements(*self.LOADING)) > 0

    def row_count(self) -> int:
        if self._empty_present(self.driver):
            return 0
        self.wait.until(lambda d: len(d.find_elements(*self.ROWS)) > 0)
        return len(self.driver.find_elements(*self.ROWS))

    def get_visible_magnitudes(self):
        """
        Safe against React re-renders (stale elements).
        Returns [] if empty state is shown.
        """
        if self._empty_present(self.driver):
            return []

        for _ in range(3):
            try:
                self.wait.until(lambda d: len(d.find_elements(*self.ROWS)) > 0)

                mags = []
                rows = self.driver.find_elements(*self.ROWS)
                for row in rows:
                    mag_text = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
                    mags.append(float(mag_text))

                return mags
            except StaleElementReferenceException:
                continue

        raise AssertionError("Failed to read magnitudes due to repeated React re-renders.")

    def set_min_magnitude(self, value: float):
        el = self.wait.until(EC.element_to_be_clickable(self.MINMAG_INPUT))
        el.clear()
        el.send_keys(str(value))
        return self

    def refresh(self):
        self.wait.until(EC.element_to_be_clickable(self.REFRESH_BTN)).click()
        return self

    def open_first_details(self):
        self.wait.until(EC.element_to_be_clickable(self.VIEW_DETAILS)).click()
        self.wait.until(EC.visibility_of_element_located(self.MODAL))
        return self

    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_MODAL)).click()
        self.wait.until(EC.invisibility_of_element_located(self.MODAL))
        return self
