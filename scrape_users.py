import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

from utils import get_page_source, CHROME_PROFILE, BASE_URL
from scrape_video import scrape_video


def scrape_users(driver, search_strings):
    users = []
    for search_string in search_strings:
        print(f"Searching for: {search_string}, may take a few seconds...")
        search_url = f"{BASE_URL}/search/user?q={search_string}"
        driver, page_source = get_page_source(driver, search_url)
        soup = BeautifulSoup(page_source, 'html.parser')
        # extract user info
        users_soup = soup.find_all("a", {"data-e2e": "search-user-info-container"})
        print(f"Found {len(users_soup)} results for {search_string}")
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

    if len(users) == 0:
        return

    users_df = pd.DataFrame(users)
    users_df = users_df.set_index("Keyword")
    users_df = users_df.sort_values(["Keyword", "Followers"], ascending=False)
    return users_df


def scrape_videos(driver, search_strings):
    users = []
    for search_string in search_strings:
        print(f"Searching for: {search_string}, may take a few seconds...")
        search_url = f"{BASE_URL}/search/user?q={search_string}"
        driver, page_source = get_page_source(driver, search_url,1)
        soup = BeautifulSoup(page_source, 'html.parser')
        # extract user info
        users_soup = soup.find_all("a", {"data-e2e": "search-user-info-container"})
        for u in users_soup:
            users.append(u['href'].strip("/@"))

    videos_df = scrape_video(driver, users[:10], 1)
    videos_df = videos_df.sort_values("Views", ascending=False)
    videos_df = videos_df.set_index("URL")
    return videos_df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide keywords to scrape:"
              "for example: python scrape_users.py keyword1 keyword2")
    print(f"Using chrome profile: {CHROME_PROFILE}")

    print(f"Found these keywords from your input: {' '.join(sys.argv[1:])}")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_list = CHROME_PROFILE.split(os.sep)
    user_data_dir = os.sep.join(chrome_list[:-1])
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={chrome_list[-1]}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if sys.argv[1] == "-v":
        data = scrape_videos(driver, sys.argv[2:])
    else:
        data = scrape_users(driver, sys.argv[1:])

    # write data to csv
    if data is not None:
        data.to_csv(f"user_data_{'_'.join(sys.argv[1:])}.csv")
    else:
        print("Unsuccessful scrape")
