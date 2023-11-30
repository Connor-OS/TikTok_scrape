import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

from utils import get_page_source, CHROME_PROFILE, BASE_URL


def scrape_video(driver, search_strings, scrolls=10):
    videos = []
    for search_string in search_strings:
        search_url = f"{BASE_URL}/@{search_string}"
        driver, page_source = get_page_source(driver, search_url, scrolls)
        soup = BeautifulSoup(page_source, 'html.parser')

        # extract user info
        videos_soup = soup.find_all("div", {"data-e2e": "user-post-item"})
        videos_desc = soup.find_all("div", {"data-e2e": "user-post-item-desc"})
        print(f"Found {len(videos_soup)} results for {search_string}")
        for v, d in zip(videos_soup, videos_desc):
            video = dict()
            # search term and username
            video["Keyword"] = search_string
            # like count
            if views := v.find("strong", {"data-e2e": "video-views"}):
                pass
            else:
                continue
            views = views.get_text()
            views = eval(views.replace('K', '*1e3').replace('M', '*1e6'))
            video["Views"] = int(views)
            # link
            video["URL"] = v.find("a")["href"]
            # description
            video["Description"] = d.get_text()

            videos.append(video)

    videos_df = pd.DataFrame(videos)
    videos_df = videos_df.set_index("Keyword")
    videos_df = videos_df.sort_values(["Keyword", "Views"], ascending=False)
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

    data = scrape_video(driver, sys.argv[1:])


    # write data to csv
    if data is not None:
        data.to_csv(f"user_video_data_{'_'.join(sys.argv[1:])}.csv")
    else:
        print("Unsuccessful scrape")
