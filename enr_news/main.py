import time
import pandas as pd
from numpy.core import records
from selenium import webdriver
from selenium.webdriver.common.by import By

from enr_news.extract_artical_newspaper3K import extract_articles
from enr_news.helpers import extract_numericals

chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

keyword_name = 'Kashmir'  # 'Suicide'  # 'The'  'Kashmir'
url = 'https://www.enr.com/search?q=' + keyword_name

driver.get(url)
driver.maximize_window()
raw_records_no = driver.find_element(By.XPATH, "//h3[@class='search-results__title']").text
print(raw_records_no)
record_nos = extract_numericals(raw_records_no)
extract = []

number_of_pages = (record_nos // 10)
if record_nos % 10 > 0:
    number_of_pages += 1

print(f"Total number of pages for record:{record_nos} should be: {number_of_pages}")

for i in range(number_of_pages):
    try:
        records = driver.find_elements(By.XPATH, "//div[@class='record']")
        # print(f"{len(records)} out of {record_nos}")
        # time.sleep(2)
        for record_index, record_element in enumerate(records, start=1):
            current_record = {}
            # print(record_index, " : ", record_element)
            try:
                date_element = record_element.find_element(By.CLASS_NAME, 'date')
                title_element = record_element.find_element(By.TAG_NAME, 'a')
                current_record['title'] = title_element.text
                current_record['date_published'] = date_element.text
                current_record['web_link'] = title_element.get_attribute('href')

                extract.append(current_record)
                # print(url + '&page=' + str(i + 2))
            except:
                print(f"Issue with page:{i+1} and record {record_index}")
                continue
            finally:
                continue
        driver.close()
        if i < number_of_pages-1:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url + '&page=' + str(i + 2))
    except:
        print(f"Issue with page number:{i+1} ")
# === Data is extracted now from index page====================================
df = pd.DataFrame(extract)

df = extract_articles(df)
# print(df)

csv_path = 'D:/Applications/Idea-Projects/scrappings/outputs/ENR_' + keyword_name + str(time.time()) + '.csv'
df.to_csv(csv_path, index=False)
