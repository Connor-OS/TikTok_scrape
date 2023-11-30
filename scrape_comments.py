import sys
import os

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from utils import get_page_source, CHROME_PROFILE, BASE_URL


def scrape_comments(driver, search_strings):
    comments = []
    for search_string in search_strings:
        search_url = f"{BASE_URL}/@{search_string}"
        driver, page_source = get_page_source(driver, search_url)
        soup = BeautifulSoup(page_source, 'html.parser')

        # extract user info
        comment_soup = soup.find_all("a", {"data-e2e": "comment-avatar-1"})
        comment_desc = soup.find_all("p", {"data-e2e": "comment-level-1"})
        print(f"Found {len(comment_soup)} results for {search_string}")
        for c, d in zip(comment_soup, comment_desc):
            comment = dict()
            # search term and username
            comment["Keyword"] = search_string
            # user
            comment["Commenter"] = c["href"]
            # description
            comment["Description"] = d.find("span").get_text()
            comments.append(comment)

    videos_df = pd.DataFrame(comments)
    videos_df = videos_df.set_index("Keyword")
    # videos_df = videos_df.sort_values(["Keyword"], ascending=False)
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

    data = scrape_comments(driver, sys.argv[1:])


    # write data to csv
    if data is not None:
        data.to_csv(f"comment_data.csv")
    else:
        print("Unsuccessful scrape")
