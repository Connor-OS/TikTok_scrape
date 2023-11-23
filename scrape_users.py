import sys
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from utils import get_page_source, CHROME_PROFILE, BASE_URL


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


def scrape_video(driver, search_strings):
    videos = []
    for search_string in search_strings:
        search_url = f"{BASE_URL}/search?q={search_string}"
        driver, page_source = get_page_source(driver, search_url)
        soup = BeautifulSoup(page_source, 'html.parser')

        # extract user info
        videos_soup = soup.find_all("div", {"data-e2e": "search-card-desc"})
        videos_links = soup.find_all("div", {"data-e2e": "search_top-item"})
        print(f"Found {len(videos_soup)} results for {search_string}")
        for v, l in zip(videos_soup, videos_links):
            video = dict()
            # search term and username
            video["Keyword"] = search_string
            video["Username"] = v.find("a", {"data-e2e": "search-card-user-link"})['href'].strip("/@")
            # like count
            if likes := v.find("div", {"data-e2e": "search-card-like-container"}):
                pass
            else:
                continue
            likes = likes.get_text()
            likes = likes.split()[0]
            likes = eval(likes.replace('K', '*1e3').replace('M', '*1e6'))
            video["Likes"] = int(likes)
            # link
            video["URL"] = l.find("a")["href"]
            # description
            if description := v.find("p", {"data-e2e": "search-card-video-caption"}):
                video["Description"] = description.get_text()

            videos.append(video)

    videos_df = pd.DataFrame(videos)
    videos_df = videos_df.set_index("Keyword")
    videos_df = videos_df.sort_values(["Keyword", "Likes"], ascending=False)
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
        data = scrape_video(driver, sys.argv[2:])
    else:
        data = scrape_users(driver, sys.argv[1:])

    # write data to csv
    if data is not None:
        data.to_csv(f"user_data_{'_'.join(sys.argv[1:])}.csv")
    else:
        print("Unsuccessful scrape")
