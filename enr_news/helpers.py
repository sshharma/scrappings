import re


def extract_numericals(inValue):
    match = re.search(r'\((\d+)\)', inValue)
    match_2 = re.search(r'\(([\d,]+)\)', inValue)
    if match:
        numerical_value = int(match.group(1))
        print("Numerical Value:", numerical_value)

    elif match_2:
        numerical_value_str = match_2.group(1)
        # Remove commas and convert to integer
        numerical_value = int(numerical_value_str.replace(',', ''))
        print("Numerical Value:", numerical_value)
    else:
        print("No numerical value found in the given text.")
    return numerical_value






# for index, row in df.iterrows():
#     try:
#         driver.close()
#         driver = webdriver.Chrome(options=chrome_options)
#         web_link = row['web_link']
#         print(web_link)
#         driver.get(web_link)
#         try:
#             main_element = driver.find_element(By.XPATH, "//article[@class='main-body page-article-show ']")
#         except:
#             main_element = driver.find_element(By.XPATH, "//div[@class= 'body gsd-paywall article-body']")
#         try:
#             author_element = main_element.find_element(By.CLASS_NAME, 'author')
#             df.at[index, 'author'] = author_element.find_element(By.TAG_NAME, 'a').text
#         except:
#             df.at[index, 'author'] = 'no_value'
#
#         # add code to read keywords
#         key_data = ''
#         try:
#             keyword_element = main_element.find_element(By.CLASS_NAME, 'article-keywords')
#             keywords = keyword_element.find_elements(By.TAG_NAME, 'a')
#             for keyword_index, keyword in enumerate(keywords, start=1):
#                 key_data += str(keyword.text)
#                 if keyword_index < len(keywords):
#                     key_data += ", "
#         finally:
#             print(f"Issue with keyword block")
#         #     once I have access to enr.com, try 'join' method for this
#         df.at[index, 'keywords'] = key_data
#
#         try:
#             article_element = main_element.find_element(By.CLASS_NAME, 'content')
#             # paragraphs = article_element.find_elements(By.TAG_NAME, 'p')
#             article = ''
#             # for para_index, paragraph in enumerate(paragraphs, start=1):
#             #     article += str(paragraph.text)
#             paragraphs = article_element.find_elements(By.TAG_NAME, 'p')
#             article = ' '.join([str(paragraph.text) for paragraph in paragraphs])
#             df.at[index, 'article'] = article
#         except:
#             article_element = main_element.find_elements(By.TAG_NAME, 'font')
#             print(f"Couldn't find article for {row['web_link']}")
#             article = ' '.join([str(paragraph.text) for paragraph in article_element])
#             df.at[index, 'article'] = article
#         finally:
#             article_element = main_element.find_elements(By.TAG_NAME, 'div')
#
#     except:
#         print("There is some major issue with {row['web_link']}")

