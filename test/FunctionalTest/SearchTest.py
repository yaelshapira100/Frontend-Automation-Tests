import unittest
from datetime import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

SITE_URL = "https://react.dev"
DARK_MODE_BTN_SELECTOR = "button[aria-label*='Dark']"
LIGHT_MODE_BTN_SELECTOR = "button[aria-label*='Light']"
SEARCH_BTN_SELECTOR = "button[aria-label*='Search']"
SEARCH_INPUT_SELECTOR = "input[type='search']"
SEARCH_RESULT_TITLE_SELECTOR = ".DocSearch-Hit-title"
SEARCH_RESULT_ITEM_SELECTOR = ".DocSearch-Hit"
RECENT_SEARCH_SELECTOR = 'li[id^="docsearch-recentSearches-item-"]'
FAVORITE_SEARCH_SELECTOR = 'li[id^="docsearch-favoriteSearches"]'
NO_RESULT_TITLE_SELECTOR = ".DocSearch-Title"
NO_RESULT_TEXT = "No results for"

QUERY="custom hook"
INVALID_QUERY="mvermlekrbm"
BODY_TAG="body"
BACKGROUND_COLOR_TAG="background-color"
class SearchTest(unittest.TestCase):

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

    


    def test_dark_mode_with_refresh(self):
        """
        Tests that dark mode toggle changes the theme, persists after refresh,
        and can be toggled back to light mode, which also persists.
        """
        dark_mode = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, DARK_MODE_BTN_SELECTOR))
        )

        #check for initial background color
        body = self.driver.find_element(By.TAG_NAME, BODY_TAG)
        initial_background = body.value_of_css_property(BACKGROUND_COLOR_TAG)

        # Toggle to dark mode
        dark_mode.click()
        self.wait.until(lambda d: body.value_of_css_property(BACKGROUND_COLOR_TAG) != initial_background)
        new_background = body.value_of_css_property(BACKGROUND_COLOR_TAG)
        self.assertNotEqual(initial_background, new_background, "Theme did not change!")

        # Refresh and check if dark mode persists
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, BODY_TAG)))
        body_after = self.driver.find_element(By.TAG_NAME, BODY_TAG)
        refreshed_background = body_after.value_of_css_property(BACKGROUND_COLOR_TAG)
        self.assertEqual(new_background, refreshed_background, "Dark mode did not persist after refresh!")

        #change background again
        light_mode = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, LIGHT_MODE_BTN_SELECTOR))
        )
        light_mode.click()

        self.wait.until(lambda d: body_after.value_of_css_property(BACKGROUND_COLOR_TAG) != new_background)
        light_background = body_after.value_of_css_property(BACKGROUND_COLOR_TAG)
        self.assertNotEqual(new_background, light_background, "Theme did not change back to light!")

        # Refresh and check if light mode persists
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME,BODY_TAG)))
        body_final = self.driver.find_element(By.TAG_NAME, BODY_TAG)
        refreshed_light = body_final.value_of_css_property(BACKGROUND_COLOR_TAG)
        self.assertEqual(light_background, refreshed_light, "Light mode did not persist after refresh!")



    def open_search(self):
        """
        Opens the search panel in a small window and verifies that it is visible.
        """
        self.driver.set_window_size(400, 800)
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_BTN_SELECTOR)))
        self.assertTrue(button.is_displayed(), "Search input is not visible.")
        button.click()


    def enter_search_query(self, query):
        """
        Types a search query into the search input field.
        """
        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_INPUT_SELECTOR)))
        input_box.send_keys(query)



    def click_first_result(self):
        """
        Clicks the first result in the search results and verifies navigation.
        """
        initial_url = self.driver.current_url
        result = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_RESULT_ITEM_SELECTOR)))
        self.first_result_text = result.text
        result.click()

        #check if we moved from one page to another
        self.wait.until(lambda d: d.current_url != initial_url)



    def check_for_recent_query(self,query):
        """
        Verifies that the search query appears in the recent searches list.
        """
        self.open_search()

        #check if there is at least one element
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, RECENT_SEARCH_SELECTOR))
        )

        #take all the elements inside the recent part
        recent_hits=recent_hits = self.driver.find_elements(By.CSS_SELECTOR, RECENT_SEARCH_SELECTOR)

        # check if the quert is in the recent hit elements meaning if it got saved into it.
        self.assertTrue(
            any(query.lower() in hit.text.lower() for hit in recent_hits),
            f"Query '{query}' was not found in Recent Searches."
        )


    def save_to_favorites(self,query):
        """
        Saves a recent search query to favorites.
        """

        self.open_search()
        #check in the history for the query
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, RECENT_SEARCH_SELECTOR))
        )
        recent_hits = self.driver.find_elements(By.CSS_SELECTOR, RECENT_SEARCH_SELECTOR)


        #going through all the result to find the right query and then press save.
        for hit in recent_hits:
            hit_text = hit.text.lower()
            if query.lower() in hit_text:

                save_button = hit.find_element(By.CSS_SELECTOR, 'button[title="Save this search"]')
                save_button.click()
                return

        #if the query wasn't found than print an error/
        self.fail(f"Query '{query}' was not found in Recent Searches – cannot save.")

    def remove_from_favorites(self,query):
        """
            Removes a saved search query from favorites.
        """
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, FAVORITE_SEARCH_SELECTOR))

        )
        recent_hits = self.driver.find_elements(By.CSS_SELECTOR, FAVORITE_SEARCH_SELECTOR)
        for hit in recent_hits:
            hit_text = hit.text.lower()
            if query.lower() in hit_text.lower():
                remove_button=hit.find_element(By.CSS_SELECTOR, 'button[title*="Remove this search"]')
                remove_button.click()
                return
        self.fail(f"Query '{query}' not found in Favorites – cannot remove.")

    def check_for_favorite_query_add_and_remove(self,query):
        """
            Adds and then removes a search query from favorites.
        """
        self.save_to_favorites(query)
        self.remove_from_favorites(query)


    def check_no_search_result(self):

        time.sleep(1)
        result=self.driver.find_element(By.CSS_SELECTOR, SEARCH_RESULT_ITEM_SELECTOR)
        if len(result)==0:
            print("No search result was found!")
        else :
            self.fail("Expected no result' but found {len(result)}.")



    def test_search_show_results(self):
        """
            Checks that searching for a valid query returns at least one result.
        """
        query=QUERY
        self.open_search()
        self.enter_search_query(query)
        results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, SEARCH_RESULT_TITLE_SELECTOR)))
        self.assertGreater(len(results), 0, f"No results found for query '{query}'")


    def test_nevigate_to_first_result(self):
        """
              Checks that clicking the first search result navigates away from the homepage.
        """
        query = QUERY
        self.open_search()
        self.enter_search_query(query)
        self.click_first_result()

        #check if we did jump to a different url page
        self.assertNotEqual(
            self.driver.current_url, SITE_URL,
            "Clicking result did not navigate to a new page."
        )

    def test_saved_query_to_recent(self):
        """
            Verifies that after searching and navigating, the query appears in recent searches.
        """
        query = QUERY
        self.open_search()
        self.enter_search_query(query)
        self.click_first_result()
        self.check_for_recent_query(query)

    def test_saved_query_to_favorite(self):
        """
            Tests that a query can be saved and then removed from favorites.
        """
        query = QUERY
        self.open_search()
        self.enter_search_query(query)
        self.click_first_result()
        self.check_for_favorite_query_add_and_remove(query)




    def test_for_a_wrong_result(self):
            """
               Checks that an invalid search query returns a 'No results for...' message.
            """
            self.open_search()
            self.enter_search_query(INVALID_QUERY)

            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, NO_RESULT_TITLE_SELECTOR),
                    NO_RESULT_TEXT
                )
            )

            #check for the component that holds the error info for the user.
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, NO_RESULT_TITLE_SELECTOR)
            self.assertTrue(
                any(NO_RESULT_TEXT in el.text for el in result_elements),
                "Expected 'No results for...' message was not found."
            )




if __name__ == "__main__":
    unittest.main()

