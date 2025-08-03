import unittest
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#====== URL AND WEBSITE ======
SITE_URL="https://react.dev/"
YOUTUBE_TAB="youtube.com"
#====== TAGS AND ATTRIBUTES ======
BODY_TAG="body"
HERF_TAB="href"
OUTLINE_PROPERTY="outline"
MAX_TABS=60

class AccessibilityTest(unittest.TestCase):
    """
     Test suite to verify keyboard accessibility and visible focus on the React.dev homepage.

     This test checks that TAB navigation can reach all interactive elements,
     that each focused element has a visible outline, and that a YouTube video
     link is reachable and functional via keyboard only.
     """

    def setUp(self):
        """
        This function open the Chrome Browser and then open the React.dev Homepage.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(SITE_URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """
        This function is responsible to close the browser after each test.
        """
        self.driver.quit()

    def test_tab_accessibility(self):
        """
        Main accessibility test:
        1. Navigates the homepage using TAB up to MAX_TABS times.
        2. For each element focused, checks that a visible outline is present.
        3. When a YouTube link is focused, presses ENTER to follow the link.
        4. Asserts that the YouTube link opens correctly in a new tab or window.
        5. Navigates backward through focus order with Shift+TAB, ensuring no errors.
        """
        driver = self.driver
        driver.get(SITE_URL)
        time.sleep(1)

        body = driver.find_element(By.TAG_NAME, BODY_TAG)

        video_found=False
        video_index=-1
        max_tabs = MAX_TABS
        focused_elements = []

        #Moving inside the main page until we reach max_tabs
        for i in range(max_tabs):
            body.send_keys(Keys.TAB)
            time.sleep(0.1)
            focused = driver.switch_to.active_element
            href = focused.get_attribute(HERF_TAB) or ""
            text = focused.text.strip()


            #Check for visible focused
            outline = focused.value_of_css_property(OUTLINE_PROPERTY)
            self.assertTrue(
                ("solid" in outline or "rgb" in outline or "1px" in outline) and not outline == "none",
                "Focused element has no visible focus outline!"
            )

            focused_elements.append(focused)

            #if the current focused is a YouTube link -> We press Enter and check if the link is ok
            if YOUTUBE_TAB in href:
                focused.send_keys(Keys.ENTER)
                video_found = True
                video_index = i
                break

        #Check if we did reach a YouTube link
        self.assertTrue(video_found, "Did not reach the YouTube link with TAB navigation.")


        time.sleep(2)

        #check if the new tab opened after pressing ENTER;
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            self.assertTrue("youtube.com" in driver.current_url, "New tab is not a YouTube video!")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        else:
            # If no new tab, check if the current URL is the YouTube link
            self.assertTrue("youtube.com" in driver.current_url, "Did not navigate to YouTube video!")


        # Backward navigation: Go back through the focus order using Shift+TAB until the start
        for j in range(video_index, 0, -1):
            body.send_keys(Keys.SHIFT + Keys.TAB)
            time.sleep(0.1)
            focused = driver.switch_to.active_element
            text = focused.text.strip()
