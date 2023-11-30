from time import sleep


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = 'https://www.tiktok.com'
# type chrome://version/ into address bar to locate your profile path and paste into line 10 bellow
# Best practice is to create a new profile for running the script
CHROME_PROFILE = r"C:\Users\OShaughnessyC\AppData\Local\Google\Chrome\User Data\Profile 1"
# make sure there is a 'r' before the path string above


def get_page_source(driver, search_url, scrolls=10):
    # request page from tiktok
    print(f"Scraping from: {search_url}")
    driver.get(search_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "app"))
    )

    # scroll page to account for pagination and get more results
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    if "Drag the slider to fit the puzzle" in driver.page_source:
        print("Warning: TikTok requested bot check - may not be able to gather results")
        driver = request_bot_check(driver)

    # pull page HTML
    page_source = driver.page_source
    return driver, page_source


def request_bot_check(driver):
    print("please login")
    while "Drag the slider to fit the puzzle" in driver.page_source:
        sleep(1)
    return driver