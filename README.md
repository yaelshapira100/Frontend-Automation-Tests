# Name: Yael Shapira
# Frontend-Automation-Tests
This project includes automated tests for the react.dev website, covering both UI and functional scenarios using Selenium and Python’s unittest. Includes user flows such as language switching, navigation, and content checks. Easily extendable for future features.

# Personal Note 

Although I started this project with only basic familiarity with React and HTML, I devoted time to learning how to
analyze and interact with web pages. I leveraged various online resources—including tutorials via Youtube, documentation
and developer communities—to quickly upskill myself and gain a practical understanding of web page structure a
and browser automation in short time.

Additionally, this was my first time ever writing full automated tests (beyond short code snippets).
Learning how to structure comprehensive test cases, select the right tools, and build a maintainable suite was both a
challenge and a valuable learning experience. I took special care to write my tests in a clear and organized way.

# About Me 

- I have no formal background in computer science and began programming about a year and a half ago,
  through self-study and university courses.
- I am a fast and motivated learner, naturally curious, and dedicated to solving new challenges.
- I love learning new technologies and diving into new topics on my own initiative.

# What’s Included 

Main tests I implemented:
1. Theme Toggle Test: Checks dark mode and light mode functionality, including persistence after page refresh.

2. Search Functionality Tests:
      * Checks that the search bar works, returns results, and navigates to the correct page from a query.
      * Verifies that recent searches and favorites are managed correctly (add/remove).
      * Handles both valid and invalid queries, with appropriate user feedback.

3. Layout and Responsiveness Test: Ensures the page layout does not break across multiple viewport sizes
   (mobile, laptop, desktop).and also Tests for Header and Footer.

4. Accessibility Test:
    * Validates keyboard navigation (TAB/SHIFT+TAB) reaches all interactive elements (can open a new window tab
     and close it, can go back and fourth inside a page).
    * Ensures all focused elements have a visible outline for accessibility.

5. Translation Test:
    * Language Navigation Test: Checks that all language switcher links (for translated versions of the site) open the
     correct localized page, and that the HTML lang attribute matches the expected language code.
    * Translation Quality Test: Uses a multilingual language model (paraphrase-multilingual-MiniLM-L12-v2, known from
     academic courses work I used) to semantically compare the English and French homepages.
     The test automatically translates the French text to English and computes the semantic similarity,
     helping to validate the translation quality beyond simple word-matching.


# What's next? 

1. Accessibility for Users with Disabilities:
    * Tests for screen reader support (ARIA roles/labels).
    * Checks for proper color contrast for visually impaired users.
    * Validates keyboard-only navigation for all main flows.
    * Tests for audio/video alternatives (subtitles, transcripts) for hearing-impaired use


3. Backend/API Tests:
    * Verifying correct data is fetched and displayed.
    * Testing error handling for API/network failures.

5. Visual Errors Tests:
    * Automatically detect unexpected changes in layout or styling.







