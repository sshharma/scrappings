import csv
import json

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time

# Set the path to your ChromeDriver executable
chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website you want to scrape
url = 'https://www.autotempest.com/results?zip=30024&localization=country'
driver.get(url)
driver.maximize_window()
time.sleep(2)

def save_to_csv(in_scrapping_data, param):
    keys_stc = in_scrapping_data[0].keys()
    flattened_data = [[item[key_stc] for key_stc in keys_stc] for item in scrapping_data]
    with open(param, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(keys_stc)
        csv_writer.writerows(flattened_data)
# load_button = "//button[@class='more-results']"
#
# # ==============this part of the code will load entire webpage=======================
# # ===================================================================================
#
#
# # Function to check if the button is present on the page
# def is_button_present():
#     try:
#         button = driver.find_element(By.XPATH, load_button)
#         return True
#     except:
#         return False
#
#
# # Keep clicking on the button until it no longer appears
# while is_button_present():
#     try:
#         button = driver.find_element(By.XPATH, load_button)
#         button.click()
#         time.sleep(2)
#     except ElementNotInteractableException:
#         print('data loading buttons are not clickable anymore.')
#         break
#     except NoSuchElementException:
#         print('No More loading buttons found on the page')
#         break
#     except ElementClickInterceptedException:
#         print('got ElementClickInterceptedException on the page')
#         break
#     except:
#         print('got unknown issue on the page')
#         break

# ====================================================================================

print('--------------------')

root_xpath = "//section[@id='results']/section[@class='source-results separate results-loaded']"
result_types = driver.find_elements(By.XPATH, root_xpath)
result_type_count = len(result_types)
print(f"Total number of valid results : {result_type_count}")
scrapping_data = []

for result_index, result_element in enumerate(result_types, start=1):
    str_result_index = str(result_index)
    xpath_result = root_xpath + "[" + str_result_index + "]/section[@class='results-list']/div[@class='results-target']/ul"
    ul_elements = driver.find_elements(By.XPATH, xpath_result)
    num_ul_elements = len(ul_elements)
    print(f"Total number of unordered list in results({result_index}) are: {num_ul_elements}")

    for ul_index, ul_element in enumerate(ul_elements, start=1):
        str_ul_index = str(ul_index)
        print("Processing ul index: " + str_ul_index)
        xpath_ul = xpath_result + "[" + str_ul_index + "]/li"
        li_elements = driver.find_elements(By.XPATH, xpath_ul)
        num_li_elements = len(ul_elements)
        print(f"Total number of list index list in results({result_index} : {num_ul_elements}) are: {num_li_elements}")
        for li_index, li_element in enumerate(li_elements, start=1):
            str_li_index = str(li_index)
            current_car = {}
            xpath_li = xpath_ul + "[" + str_li_index + "]/section/div/div/"
            print("Processing li index: " + str_li_index)
            try:
                curr_car_element = driver.find_element(By.XPATH,
                                                       xpath_li + "/h2/span/a[@class='listing-link source-link']")
                current_car['Name'] = curr_car_element.text
                current_car['Dealer'] = driver.find_element(By.XPATH,
                                                            xpath_li + "/h2/span/a[@class='logo-link']/img").get_attribute(
                    'alt')
                current_car['Price'] = driver.find_element(By.XPATH,
                                                           xpath_li + "/div[@class='price-wrap']/div/div/div[@class='badge__labels']/div").text
                current_car['Mileage'] = driver.find_element(By.XPATH,
                                                             xpath_li + "/div[@class='info-wrap']/div[@class='info mileageDate']/span[@class='mileage']").text
                current_car['Listed'] = driver.find_element(By.XPATH,
                                                            xpath_li + "/div[@class='info-wrap']/div[@class='info mileageDate']/span[@class='date']").text
                current_car['City'] = driver.find_element(By.XPATH,
                                                          xpath_li + "/div[@class='info-wrap']/div[@class='info location has-distance']/span/span[@class='city']").text
                current_car['Listing_Link'] = curr_car_element.get_attribute('href')
                print(current_car)
                scrapping_data.append(current_car)

            except NoSuchElementException:
                print('Issue with ul index: ' + str_ul_index + " and li index: " + str_li_index)
                pass

    # print(scrapping_data)





save_to_csv(scrapping_data,"D:/Document/Kirti/temp_result.csv")

print("completed processing entire page. \nNow will start reading the data from direct link.")
# Extract keys from the first item in the list
time.sleep(5)


def fix_key(input_key):
    if input_key == '':
        input_key = 'unknown'
    return input_key


for entry in scrapping_data:
    try:
        # =========== for Private Auto Dealers =============================================
        if 'PrivateAuto' in entry['Dealer']:
            driver.get(entry['Listing_Link'])
            time.sleep(5)
            xpath_wfull = "//main/div/section[@class='w-full']/div[1]/div/div"
            wfull_items = driver.find_elements(By.XPATH, xpath_wfull)
            wfull_item_count = len(wfull_items)
            for wfull_index, wfull_element in enumerate(wfull_items, start=1):
                str_wfull_index = str(wfull_index)
                xpath_key = "div[2]/div[@class='name font-normal text-sm text-[#7E7E7E]']"
                xpath_value = "div[2]/div[@class='value font-bold text-base']"
                key = driver.find_element(By.XPATH, xpath_wfull + "[" + str_wfull_index + "]/" + xpath_key).text
                value = driver.find_element(By.XPATH, xpath_wfull + "[" + str_wfull_index + "]/" + xpath_value).text
                key = fix_key(key)
                entry[key] = value
                print(key + ":" + value)

            driver.find_element(By.XPATH, "//div[@class='font-semibold text-2xl md:text-3xl cursor-pointer'][1]").click()
            time.sleep(1)
            xpath_add_info_p = "//div[@class='mb-6']/div/div"
            add_info_items_p = driver.find_elements(By.XPATH, xpath_add_info_p)
            for add_info_p_index, add_info_p_element in enumerate(add_info_items_p, start=1):
                print(1)
                str_add_info_p_index = str(add_info_p_index)
                xpath_add_info = xpath_add_info_p + "[" + str_add_info_p_index + "]/div"
                add_info_items = driver.find_elements(By.XPATH, xpath_add_info)
                for add_info_index, add_info_element in enumerate(add_info_items, start=1):
                    str_add_info_index = str(add_info_index)
                    xpath_key = xpath_add_info + "[" + str_add_info_index + "]/p[1]"
                    xpath_value = xpath_add_info + "[" + str_add_info_index + "]/p[2]"
                    key = driver.find_element(By.XPATH, xpath_key).text
                    value = driver.find_element(By.XPATH, xpath_value).text
                    key = fix_key(key)
                    entry[key] = value
                    print(key + ":" + value)
        # =========== Private Auto Dealers ENDs Here=============================================
        # =========== Cars.com Dealer Starts here ===============================================
        elif 'Cars.com' in entry['Cars.com']:
            driver.get(entry['Listing_Link'])
            time.sleep(5)
            xpath_all_key = "//section[@class= 'sds-page-section basics-section']/dl/dt"
            xpath_all_value = "//section[@class= 'sds-page-section basics-section']/dl/dd"
            # all_elements = driver.find_elements(By.)
        # =========== Cars.com Dealer Ends here ================================================
        # =========== AutoTempest Dealer Starts from here =======================================
        elif 'AutoTempest' in entry['Dealer']:
            driver.get(entry['Listing_Link'])
            time.sleep(5)
            xpath_wfull = "//div[@data-content-id='summary']/table/tbody/tr"
            wfull_items = driver.find_elements(By.XPATH, xpath_wfull)
            for wfull_index, wfull_element in enumerate(wfull_items, start=1):
                str_wfull_index = str(wfull_index)
                key = driver.find_element(By.XPATH, xpath_wfull+"["+str_wfull_index+"]/td[1]").text
                value = driver.find_element(By.XPATH, xpath_wfull+"["+str_wfull_index+"]/td[2]").text
                key = fix_key(key)
                entry[key] = value
                print(key + ":" + value)
    # =========== AutoTempest Dealer Ends here =======================================

    except:
        print(f"Issue with link:{entry['Listing_Link']}")
        pass



# ====================================================================================================================
# =============This code will save the extracted data to csv =========================================================
# Specify the file path where you want to save the CSV file
try:
    save_to_csv(scrapping_data, "D:/Document/Kirti/final_result.csv")
except:
    json_file_path = "D:/Document/Kirti/final_result_json.json"
    # Serialize and save to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(scrapping_data, json_file, indent=2)
