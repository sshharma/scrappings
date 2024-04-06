import sys
import urllib.parse
import requests
import json
from time import sleep
# sys.path.append('../Scraper')
# sys.path.append('../Scraper/general_utilities')
# sys.path.append('../Scraper/scrape_utilities')

from pandas import json_normalize
from tqdm import tqdm

import os.path
import pandas as pd
from random import random
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)


def initialize():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    # options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.set_capability("loggingPrefs", {"performance": "ALL"})
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    # options.add_argument("--disable-images")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # # or alternatively we can set direct preference:
    # options.add_experimental_option(
    #     "prefs", {"profile.managed_default_content_settings.images": 2}
    # )
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(.5)

    return driver


def load_page(url, driver, k):
    for i in range(3):
        try:
            driver.get(url)
            print(f"URL requested", end='\r')
            # if page is loaded successfully
            if driver.title == f"{k} - Explore - Google Trends":
                print(f"Page loaded successfully!!", end='\r')
                break               # continue with the next steps
        except TimeoutException as e:
            print("Page load Timeout Occurred. Refreshing !!!", end='\r')
            driver.refresh()
        except Exception as e:
            print("Page load Timeout Occurred. Refreshing !!!", end='\r')
            driver.refresh()
    return driver


def login(driver, user=None):
    username = os.environ.get('google_email')
    password = os.environ.get('google_password')

    # url = "https://authn.edx.org/login"
    url = 'https://trends.google.com/'

    driver = load_page(url, driver)
    # driver.get(url)
    sleep(1 + random() * 2)
    username_box = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="emailOrUsername"]')))
    for character in username:
        username_box.send_keys(character)
        sleep(0.1 + random() / 8)
    sleep(2 + random() * 2)
    username_box.send_keys(Keys.ENTER)

    sleep(3+random()*3)
    password_box = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="password"]')))
    sleep(1+random()*2)
    for character in password:
        password_box.send_keys(character)
        sleep(0.1 + random() / 8)
    password_box.send_keys(Keys.ENTER)

    sleep(random()*5)
    print("Logged in")
    return

def clickable(xpath, wait=20, driver=None):
    try:
        element = WebDriverWait(driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        # Example XPATH = "//div[@class='list-group list-group-flush flex-fill']"
    except:
        element = None
    return element


def catch(func, *args, handle=lambda e : str(e)[0:100], **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle(e)


def proper_scrape(element, xpath, attr=None, handle = lambda e: None):
    if xpath == 'noxpath':
        value = attr
    else:
        try:
            el = element.find_element(By.XPATH, xpath)
            if attr == 'text':
                value = getattr(el, attr)
            elif '___' in attr:
                value = attr.replace('___', '')
            else:
                value = type(el).get_attribute(el, attr)
        except Exception as e:
                value = handle(e)
    return value

# def get_table():
#     load_page(url, driver)
#
#     headers = {
#         'Accept': 'application/json, text/plain, */*',
#         'Sec-Fetch-Site': 'same-site',
#         # 'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Sec-Fetch-Mode': 'cors',
#         'Host': 'api.arkhamintelligence.com',
#         'Origin': 'https://platform.arkhamintelligence.com',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
#         'Referer': 'https://platform.arkhamintelligence.com/',
#         'Connection': 'keep-alive',
#         'Sec-Fetch-Dest': 'empty',
#         'X-Timestamp': '1710861549',
#         # 'X-Payload': '48984fdd6c6118bf48a4d77497929aef1c4cd2784f2f253aee9b03fa3b786a70',
#     }
#
#     params = {
#         # 'sortKey': 'time',
#         'sortDir': 'desc',
#         'limit': '16',
#         'offset': '16',
#         'flow': 'all',
#         'base': 'grayscale',
#         'usdGte': '0.1',
#     }
#
#     response = requests.get('https://api.arkhamintelligence.com/transfers', params=params, headers=headers)
#     response.json()
#
#     df = pd.json_normalize(response.json())
#     print(df)
#
#     return df

def log_filter(log_): # only keeps XHR responses downloaded from the server
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
        and 'https://api.arkhamintelligence.com/transfers' in log_["params"]['response']['url']
        )


def get_keywords():
    f = '~/Dropbox (GSU Dropbox)/My PyCharm Projects/6- Google Trends/guide/keywords.csv'
    k = pd.read_csv(f)
    return k

# guide is the database of urls we want to scrape
def make_guide():
    k = get_keywords()
    keywords = k.loc[pd.notna(k['keyword list']), 'keyword list'].unique()
    keywords = [urllib.parse.quote(k) for k in keywords]
    geo = k.loc[pd.notna(k['geo list']), 'geo list'].unique()
    geo = [urllib.parse.quote(g) for g in geo]
    from_date = '2017-01-01'
    to_date = '2020-01-01'

    urls = [{'url':f'https://trends.google.com/trends/explore?date={from_date}%20{to_date}&geo={g}&q={k}&hl=en', 'keyword': k, 'geo': g} for k in keywords for g in geo]
    guide = pd.DataFrame(urls)
    path = './12_GoogleTrends/guide.csv'
    guide.to_csv(path, index=False)
    return guide


def log_filter(log_):
    return (
        # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
            and "XHR" in log_["params"]["type"]
    )


# def getdf(j):
#     ''' just a helper function that extracts a DF from a JSON'''
#     j = j['body']
#     j = j.replace(")]}\',\n", "")
#     jj = json.loads(j.strip())
#     df = pd.DataFrame(jj['default']['timelineData'])
#     return df
def scrape_gtrends(url,k):
    '''scrapes the data for one url and saves as a CSV'''
    load_page(url, driver,k)
    sleep(3)  # wait for the requests to take place
    print(url)
    clickable(xpath='trends-widget', wait=10) # make sure the target element is clickable (i.e., fully loaded)

    # detect errors and return None
    bads = ['Please try again in a bit.']
    for b in bads:
        if b in driver.page_source:
            print(b)
            return None


    # extract the JSON requests from the browser logs
    logs_raw = driver.get_log("performance")

    #### Cleaning & Filtering JSONs & concatenating them into a single DataFrame called "dfs"
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    logs_filt = [l for l in filter(log_filter, logs) if 'multiline' in str(l)]
    print(f'{len(logs_filt)} logs found')
    jsons = []
    for log in logs_filt:
        try:
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            print(f"Caught {resp_url}")
            j = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})

            j = j['body']
            j = j.replace(")]}\',\n", "")
            jj = json.loads(j.strip())
            jj = jj['default']['timelineData']
            jsons.extend([jj])
            # print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
        except Exception as e:
            # print(e)
            pass
    dfs = pd.concat([pd.DataFrame(j) for j in jsons])

    return dfs

def getGTrends():
    path = './12_GoogleTrends/guide.csv'
    guide = pd.read_csv(path)
    print(f'read guide: {len(guide)} rows')

    out = './12_GoogleTrends/results2.csv'

    if os.path.exists(out):
        '''if some progress is already made in a previous run, read the results'''
        dfs = pd.read_csv(out)
        # Do not repeat the stuff that are already completed in a previous run
        # remove complete ones from guide
        dfs['status'] = 'ok'
        G = guide.merge(dfs[['keyword', 'geo', 'status']], on=['keyword', 'geo'], how='left')
        guide = G[pd.isna(G.status)]
        print(f'cleaned guide: {len(guide)} rows')
    else:
        dfs = pd.DataFrame()


    # Loop over cleaned guide and scrape one by one
    for i in tqdm(guide.index):
        try:
            sleep(5 + random())
            url = guide.loc[i, 'url']
            k = guide.loc[i, 'keyword']
            g = guide.loc[i, 'geo']
            df = scrape_gtrends(url, k)
            if not isinstance(df, pd.DataFrame):
                print('not a dataframe .. sleeping for a minute')
                driver.close()
                driver = initialize()
                sleep(10)
            df['keyword'] = k
            df['geo'] = g
            dfs = pd.concat([dfs,df])
            sleep(5)
            dfs.to_csv(out, index=False)
        except Exception as e:
            print(str(e)[0:100])
    dfs.to_csv(out, index=False)
    return


if __name__ == '__main__':
    if 'driver' not in globals():
        driver = initialize()
    getGTrends()