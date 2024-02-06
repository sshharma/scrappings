import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from enr_news.helpers import extract_numericals

chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

keyword_name = 'Suicide'  # 'Kashmir'
url = 'https://www.enr.com/search?q=' + keyword_name

driver.get(url)
driver.maximize_window()
raw_records_no = driver.find_element(By.XPATH, "//h3[@class='search-results__title']").text
record_nos = extract_numericals(raw_records_no)
extract = []

number_of_pages = (record_nos // 10) + 1
for i in range(number_of_pages):
    records = driver.find_elements(By.XPATH, "//div[@class='record']")
    print(f"{len(records)} out of {record_nos}")
    time.sleep(2)
    for record_index, record_element in enumerate(records, start=1):
        current_record = {}
        # print(record_index, " : ", record_element)
        date_element = record_element.find_element(By.CLASS_NAME, 'date')
        title_element = record_element.find_element(By.TAG_NAME, 'a')
        current_record['title'] = title_element.text
        current_record['date_published'] = date_element.text
        current_record['web_link'] = title_element.get_attribute('href')

        extract.append(current_record)
        print(url + '&page=' + str(i + 2))
    driver.get(url + '&page=' + str(i + 2))

# === Data is extracted now from index page====================================
# === Now below code will iterate the extracted data and get articles ========
df = pd.DataFrame(extract)
print(df)

for index, row in df.iterrows():
    try:
        driver.close()
        driver = webdriver.Chrome(options=chrome_options)
        web_link = row['web_link']
        print(web_link)
        driver.get(web_link)
        try:
            main_element = driver.find_element(By.XPATH, "//article[@class='main-body page-article-show ']")
        except:
            main_element = driver.find_element(By.TAG_NAME, "div")
        try:
            author_element = main_element.find_element(By.CLASS_NAME, 'author')
            df.at[index, 'author'] = author_element.find_element(By.TAG_NAME, 'a').text
        except:
            df.at[index, 'author'] = 'no_value'

        # add code to read keywords
        key_data = ''
        try:
            keyword_element = main_element.find_element(By.CLASS_NAME, 'article-keywords')
            keywords = keyword_element.find_elements(By.TAG_NAME, 'a')
            for keyword_index, keyword in enumerate(keywords, start=1):
                key_data += str(keyword.text)
                if keyword_index < len(keywords):
                    key_data += ", "
        finally:
            print(f"Issue with keyword block")
        #     once I have access to enr.com, try 'join' method for this
        df.at[index, 'keywords'] = key_data

        try:
            article_element = main_element.find_element(By.CLASS_NAME, 'content')
            # paragraphs = article_element.find_elements(By.TAG_NAME, 'p')
            article = ''
            # for para_index, paragraph in enumerate(paragraphs, start=1):
            #     article += str(paragraph.text)
            paragraphs = article_element.find_elements(By.TAG_NAME, 'p')
            article = ' '.join([str(paragraph.text) for paragraph in paragraphs])
            df.at[index, 'article'] = article
        except:
            print(f"Couldn't find article for {row['web_link']}")
    except:
        print("There is some major issue with {row['web_link']}")

csv_path = 'D:/Applications/Idea-Projects/scrappings/outputs/ENR_' + keyword_name + str(time.time())+'.csv'
df.to_csv(csv_path, index=False)
