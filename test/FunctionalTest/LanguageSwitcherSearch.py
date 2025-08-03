import unittest
from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from sentence_transformers import SentenceTransformer, util

#====== URL AND WEBSITE ======
SITE_URL="https://react.dev/"
SITE_NAME="react.dev"
GIT_HUB_LINK="github.com"
SCRIPT_ARGUMENT="window.open(arguments[0]);"
FRENCH_URL="https://fr.react.dev/"

#====== SELECTORS ======
FULL_TRANSLATION_SELECTOR="ul.ms-6.my-3.list-disc"
TRANSLATION_BUTTON='[aria-label="Translations"]'

#====== TAGS AND ATTRIBUTES ======
TAG_LI="li"
TAG_A="a"
HERF_TAG="href"
LANG_ATTRIBUTE="lang"
HTML="html"
LANGUAGE_CODES = {
            "en": "en",
            "fr": "fr",  # French
            "ja": "ja",  # Japanese
            "ko": "ko",  # Korean
            "zh": "zh",  # Chinese
            "es": "es",  # Spanish
            "tr": "tr",  # Turkish
        }

#====== ERRORS ======
ERROR_404="404"
ERROR_NOT_FOUND="Not Found"

#====== DEFAULT ======
DEFAULT_SECTION_SELECTOR="main"
DEFAULT_MAX_CHAR=1500
SIMILARITY_THRESHOLD=0.4
PARAPHRASE_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
BODY_SELECTOR="body"

"""
    This class is to test the language switch functionality.
    It contains two main test :
    1. Test the nevigation buttons to the Translation page, and than if the links of each tranlated website is 
        correct.
    2. Test that chekc if the translation is correct. Meaning if the translation to French is similar 
        to the translation to English. 
"""
class  LanguageSwitcherTests(unittest.TestCase):

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
    def get_full_link(self):
        """
        Extract the URL of the translation pages that inside the "Full translation" part.
        Returns: A list that contains the url of the translation pages.

        """
        ul_all_lists = self.driver.find_elements(By.CSS_SELECTOR, FULL_TRANSLATION_SELECTOR)

        full_translations_ul = ul_all_lists[1]
        language_links = full_translations_ul.find_elements(By.TAG_NAME, TAG_LI)
        site_links = []
        for li in language_links:
            a_tag = li.find_elements(By.TAG_NAME, TAG_A)

            if a_tag:
                language_name = a_tag[0].text
                language_href = a_tag[0].get_attribute(HERF_TAG)
                # Only keep actual translation links (not github) case for each language there is 2 different links.
                if language_href and SITE_NAME in language_href and not GIT_HUB_LINK in language_href:
                    site_links.append((language_name, language_href))
        return site_links

    def check_the_open_translation_page(self, language_name, language_href, language_codes):
        """
        This helper function open a translation page link in a new tab. Then check the HTML lang
        and also if there is no 404 errors.
        Returns: str or None: Returns an error message if found, otherwise None.

        """
        #check if we are not in the Homepage.If we are then we stop this function and return None.
        if language_href.rstrip('/') == SITE_NAME:
            return None

        driver=self.driver

        #open the url in a new tab
        driver.execute_script(SCRIPT_ARGUMENT, language_href)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        #find the HTML lang attribute
        html_tag = driver.find_element(By.TAG_NAME, HTML)
        lang_attr = html_tag.get_attribute(LANG_ATTRIBUTE)

        #check if the HTML attribute is the same as the url meaning we got the right language.
        found = False
        for code in language_codes.values():
            if lang_attr and lang_attr.startswith(code):
                found = True
                break
        error=None
        if not found:
            error = f"{language_name} ({lang_attr})"

        # Check if the url did open.
        if ERROR_404 in driver.title or ERROR_NOT_FOUND in driver.page_source:
            error = f"{language_name} (404 page!)"

        #close the tab and switch back
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.2)

        return error

    def test_language_switcher(self):
        """
        This test is verified the correct functionality of the language switcher in on the React.dev homepage.
        We check the following conditions:
        - If the button exist.
        - Navigate to the language page -> to the "full translation" part in the page.
        - Navigate to all url inside this part.
        - Check there correctness (if they are open) and then check if the
          HTML `lang` attribute of each page matches the expected language code

        """
        driver=self.driver

        language_button=driver.find_element(By.CSS_SELECTOR,TRANSLATION_BUTTON)
        language_button.click()
        time.sleep(1)

        site_links=self.get_full_link()

        errors = []

        #Going throw each Url inside the full translation page and check it.
        for language_name,language_href in site_links:
            print(f"Testing {language_name} | {language_href}")
            error = self.check_the_open_translation_page(language_name, language_href, LANGUAGE_CODES)
            if error:
                errors.append(error)

        if errors:
            self.fail(f"Problems found for: {', '.join(errors)}")
        else:
            print("All language links opened correct language pages!")





    def get_clean_text(self,section=DEFAULT_SECTION_SELECTOR,max_chars=DEFAULT_MAX_CHAR):
        """
        Extracts and returns concatenated text content (up to max_chars) from a specific section of the page.
        If the section is not found, extracts from <body>.
        - Strips whitespace and ignores empty paragraphs.
        - Converts the result to lowercase.

        Args:
            section: Section to extract text from.
            max_chars: Maximum number of characters to extract.

        Returns: str: Cleaned and concatenated text from the page.

        """
        try:
            body_text= self.driver.find_element(By.CSS_SELECTOR, section)
        except:
            # Fallback to whole page if main section not found
            body_text = self.driver.find_element(By.TAG_NAME, BODY_SELECTOR)

        paragraphs = body_text.find_elements(By.TAG_NAME, "p")
        all_text = "".join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 0])
        return all_text[:max_chars].lower()

    def check_for_similarity(self,text1,text2):
        """
         Computes the semantic similarity between two pieces of text using a multilingual sentence transformer.
         The model used is 'paraphrase-multilingual-MiniLM-L12-v2', a lightweight transformer that produces
         vector embeddings for sentences in many languages.
        Args:
            text1: First text to compare.
            text2: second text to compare.

        Returns: the semantic similarity between text1 and text2.

        """
        model = SentenceTransformer(PARAPHRASE_MODEL)
        emb1 = model.encode(text1, convert_to_tensor=True)
        emb2 = model.encode(text2, convert_to_tensor=True)
        similarity = float(util.cos_sim(emb1, emb2))
        return similarity

    def test_translation_correctness(self):
        """
        This is the full test. We extract the 2 texts we want to compare and then check if they have similar semantic
        meaning.
        This ensures that the full translation is reasonably accurate and matches the English content semantically.

        """
        driver=self.driver

        #Extracting the English Text
        english_text = self.get_clean_text()

        #open the French tab
        driver.get(FRENCH_URL)
        time.sleep(2)
        french_text = self.get_clean_text()
        #check if similarity is less than 0.4
        if self.check_for_similarity(english_text, french_text)<SIMILARITY_THRESHOLD:
            self.fail("Full page translation does not match (low similarity).")
        else:
            print("Page translation similarity test PASSED!")





