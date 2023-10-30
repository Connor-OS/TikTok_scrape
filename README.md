# Tiktok scraping script

### Prerequisites: 
Python 3.10, Google Chrome

Install requirements with:

```pip install -r requirements.txt```

### Setup

1. (Optional) Create a new profile in Chrome only for running this script. This keeps things separate from your normal browsing.
 It is not necessary to link it to a Google account.

2. Navigate to www.tiktok.com and log into an account. Again it is good to use a fresh one.

3. In chrome navigate to chrome://version/ and take a note of what is shown next to Profile Path. It should be something like:

```C:\Users\[Your_user_folder]\AppData\Local\Google\Chrome\User Data\Profile 1```

4. Open the script and edit lines 74 and 75 to contain the path to your chrome profile.

## Running the script

To run the script use:

```python scrape_users.py keyword1 keyword2```

where keyword1 and 2 are keywords you wish to scrape TiKTok for. You must provide at least 1 keyword, but you can add as many as you like. The script should take only a few seconds per keyword to run.

Once completed you will see a csv file generated in the same directory as the script with the acquired data.



### Future Updates

- Add batch scraping from file.
- Clean data in follower count output to be numerical format.
- This script will be augmented by two additional scripts to scrape video and viewer data.