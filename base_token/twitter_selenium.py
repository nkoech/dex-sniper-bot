from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import logging

# Set up the logger
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)

def setup_driver():
    """Setup the Chrome driver with headless option."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
    return webdriver.Chrome(options=chrome_options)

def get_page_source(driver: webdriver.Chrome, url: str, timeout: int = 4) -> str:
    """Get the page source of the given URL."""
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.r-rjixqe')))
        return driver.page_source
    except TimeoutException:
        logging.error(f'Timeout while loading page {url} or locating element {"a.r-rjixqe"}')
        return None

def get_profile_followers(page_source):
    """Extract the profile followers from the page source."""
    soup = BeautifulSoup(page_source, 'lxml')
    try:
        return soup.find_all("a", {"class": "r-rjixqe"})[1].text
    except IndexError:
        return None

def main():
    driver = setup_driver()
    target_url = "https://twitter.com/DeadBearIncx"
    page_source = get_page_source(driver, target_url, 4)
    if page_source:
        profile_followers = get_profile_followers(page_source)
        print([{"profile_followers": profile_followers}])
    driver.quit()

if __name__ == "__main__":
    main()
    # Prompt: Write efficient and performant code to check if twitter account exists
