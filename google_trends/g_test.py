
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


def load_page(url, driver):
    for i in range(3):
        try:
            driver.get(url)
            print(f"URL requested", end='\r')
            # continue with the next steps
            break
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
    driver.find_element(By.LINK_TEXT, 'Sign in').click()
    sleep(2)
    # driver.find_element(By.XPATH, "//input[@aria-label='Email or phone']").send_keys(username)
    # driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button/span").click()
    # sleep(20)
    # driver.find_element(By.XPATH, "//input[@jsname='YPqjbf' and  @name='Passwd']").send_keys(password)
    # driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button/span").click()
    sleep(300)
    return driver

driver = initialize()
driver = login(driver)
