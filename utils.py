from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

BASE_URL = 'https://www.tiktok.com'
# type chrome://version/ into address bar to locate your profile path and paste into line 10 bellow
# Best practice is to create a new profile for running the script
CHROME_PROFILE = r"C:\Users\OShaughnessyC\AppData\Local\Google\Chrome\User Data\Profile 2"
# make sure there is a 'r' before the path string above


def get_page_source(driver, search_url):
    # request page from tiktok
    print(f"Scraping from: {search_url}")
    driver.get(search_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "app"))
    )

    if "top-login-button" in driver.page_source:
        driver = request_user_login(driver)

    if "Drag the slider to fit the puzzle" in driver.page_source:
        print("Warning: TikTok requested bot check - can't gather results")

    # scroll page to account for pagination and get more results
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    if "Drag the slider to fit the puzzle" in driver.page_source:
        print("Warning: TikTok requested bot check - may not be able to gather results")

    # pull page HTML
    page_source = driver.page_source
    return driver, page_source


def request_user_login(driver):
    print("please login")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="profile-icon"]'))
    )
    return driver