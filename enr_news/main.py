import re
import time

from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

from enr_news.helpers import extract_numericals

chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

# Initialize the Chrome driver
driver = webdriver.Chrome()
keyword = 'Suicide'
# Navigate to the website you want to scrape
url = 'https://www.enr.com/search?q='+keyword
driver.get(url)
driver.maximize_window()

raw_records_no = driver.find_element(By.XPATH, "//h3[@class='search-results__title']").text
record_nos = extract_numericals(raw_records_no)

number_of_pages =(record_nos//10) + 1
for i in number_of_pages:
    records = driver.find_elements(By.XPATH, "//div[@class='record']")
    print(f"{len(records)} out of {record_nos}")
    time.sleep(80)