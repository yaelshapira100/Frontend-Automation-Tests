import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#====== URL AND WEBSITE ======
SITE_URL = "https://react.dev"
#====== HEADERS & BREAKPOINTS & TAGS ======
HEADER_SELECTOR = "nav.z-40"
FOOTER_TAG = "footer"
LAYOUT_BREAKPOINTS = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "laptop", "width": 1200, "height": 800},
    {"name": "desktop", "width": 1920, "height": 1080}
]

#====== SCRIPTS ======
SCRIPT_NAME="return document.body.scrollWidth"
CLIENT_SCRIPT="return document.body.clientWidth"


class LayoutHomePageTest(unittest.TestCase):
    """
       Test suite to verify the layout and presence of key sections (header/footer) on the React.dev homepage
       across common device sizes (mobile, laptop, desktop).
       """

    def setUp(self):
        """
        Opens the Chrome browser and navigates to the homepage.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(SITE_URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """
        Closes the browser after each test.
        """
        self.driver.quit()


    def test_header(self):
        """
        Checks that the header navigation (nav.z-40) is present on the homepage.
        Fails if not found.
        """
        header_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, HEADER_SELECTOR)))
        self.assertIsNotNone(header_element, "Header element was not found!")

    def test_footer(self):
        """
        Checks that the footer is present on the homepage and prints its text.
        Fails if not found.
        """
        footer = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, FOOTER_TAG))
        )
        self.assertIsNotNone(footer)


    def test_layout_in_different_size(self):
        """
        Verifies that the homepage layout does not break or cause unwanted horizontal scrolling
        at common device sizes (mobile, laptop, desktop).
        For each breakpoint:
        - Resizes the window
        - Waits for rendering
        - Checks scrollWidth vs. clientWidth (no significant horizontal scroll)
        - Saves a screenshot for visual inspection
        """
        for point in LAYOUT_BREAKPOINTS:
            with self.subTest(LAYOUT_BREAKPOINTS=point["name"]):
                self.driver.set_window_size(point["width"], point["height"])
                time.sleep(1)

                scroll_width = self.driver.execute_script(SCRIPT_NAME)
                client_width = self.driver.execute_script(CLIENT_SCRIPT)
                self.assertTrue(
                    scroll_width - client_width < 50,
                    f"Layout breaks at {point['name']} – horizontal scroll detected!"
                )

                self.driver.save_screenshot(f"screenshot_{point['name']}.png")













