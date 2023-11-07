# Tiktok scraping script

### Prerequisites: 
Python 3.10, Google Chrome

Install requirements with:

```pip install -r requirements.txt```

### Setup

1. Create a new profile in Chrome only for running this script. This keeps things separate from your normal browsing.
 It is not necessary to link it to a Google account.

2. Navigate to www.tiktok.com and log into an account. Again it is good to use a fresh one.

3. In chrome navigate to chrome://version/ and copy your Profile Path. If your on windows it should look something like:

```C:\Users\[Your_user_folder]\AppData\Local\Google\Chrome\User Data\Profile 1```

4. Open the script and paste your path into the CHROME_PROFILE variable on line 10.

## Running the script

To run the script use:

```python scrape_users.py keyword1 keyword2```

where keyword1 and 2 are keywords you wish to scrape TiKTok users for. You must provide at least 1 keyword, but you can add as many as you like. The script should take only a few seconds per keyword to run.

if you instead provide the optional flag "-v" to the script like:

```python scrape_users.py -v keyword1 keyword2```

you will scrape for to video links instead of user profiles.

Once completed you will see a csv file generated in the same directory as the script with the acquired data.



### Future Updates

- This script will be augmented by two additional scripts to scrape video and viewer data.
- Add batch scraping from file.
- Improve performance of the script
- Clean data in follower count output to be numerical format.