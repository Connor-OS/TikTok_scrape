import sys
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = 'https://www.tiktok.com'
# type chrome://version/ into address bar to locate your profile path and paste into line 10 bellow
# Best practice is to create a new profile for running the script
CHROME_PROFILE = r"C:\Users\user_folder\AppData\Local\Google\Chrome\User Data\Profile 2"
# make sure there is a 'r' before the path string above

def scrape_users(driver, search_strings):
    users = []
    for search_string in search_strings:
        print(f"Searching for: {search_string}, may take a few seconds...")
        # request page from tiktok
        search_url = f"{BASE_URL}/search/user?q={search_string}"
        driver.get(search_url)
        sleep(5)  # wait for page to load up 5s seems to be long enough

        # scroll page to account for pagination and get more results
        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.5)
        # pull page HTML
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # extract user info
        users_soup = soup.find_all("a", {"data-e2e": "search-user-info-container"})
        for u in users_soup:
            user = dict()
            # search term and username
            user["Keyword"] = search_string
            user["Username"] = u['href'].strip("/@")
            # follow count
            if followers := u.find("strong", {"data-e2e": "search-follow-count"}):
                pass
            elif followers := u.find("span", {"data-e2e": "search-follow-count"}):
                pass
            else:
                continue
            followers = followers.get_text()
            followers = followers.split()[0]
            followers = eval(followers.replace('K', '*1e3').replace('M', '*1e6'))
            user["Followers"] = int(followers)
            # link
            user["Page"] = f"{BASE_URL}{u['href']}"
            # nickname
            if nickname := u.find("p", {"data-e2e": "search-user-nickname"}):
                user["Nickname"] = nickname.get_text()
            # description
            if description := u.find("p", {"data-e2e": "search-user-desc"}):
                user["Description"] = description.get_text()

            users.append(user)
        print(f"found {len(users)} results for {search_string}")

    users_df = pd.DataFrame(users)
    users_df = users_df.set_index("Keyword")
    users_df = users_df.sort_values(["Keyword", "Followers"], ascending=False)
    return users_df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("provide keywords to scrape:"
              "for example: python scrape_users.py keyword1 keyword2")

    print(f"found these keywords from your input: {' '.join(sys.argv[1:])}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_list = CHROME_PROFILE.split(os.sep)
    user_data_dir = os.sep.join(chrome_list[:-1])
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"profile-directory={chrome_list[-1]}")
    driver = webdriver.Chrome(options=options)

    users = scrape_users(driver, sys.argv[1:])
    users.to_csv(f"user_data_{'_'.join(sys.argv[1:])}.csv")
