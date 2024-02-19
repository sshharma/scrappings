import csv
import json
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dateutil import parser
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

# Set the path to your ChromeDriver executable
chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website you want to scrape
base_url = 'https://www.autotempest.com/results?localization=country'
load_button_xpath = "//button[@class='more-results']"
SCRAPPED_DATA = []
# # ==============this part of the code will load entire webpage=======================
# # ===================================================================================


def click_load_more(driver):
    """
    Function to click on a 'load more' button until it is no longer interactable.
    :param driver: Selenium WebDriver object
    :param load_button_xpath: XPATH of the 'load more' button
    """

    # Function to check if the button is present and interactable on the page
    def is_button_present():
        try:
            button = driver.find_element(By.XPATH, load_button_xpath)
            return button.is_enabled() and button.is_displayed()
        except NoSuchElementException:
            return False

    # Keep clicking on the button until it no longer appears or is not interactable
    while is_button_present():
        try:
            button = driver.find_element(By.XPATH, load_button_xpath)
            button.click()
            time.sleep(2)
        except ElementNotInteractableException:
            print('Data loading buttons are not clickable anymore.')
            break
        except NoSuchElementException:
            print('No more loading buttons found on the page.')
            break
        except Exception as e:
            print(f'Got an unexpected exception: {str(e)}')
            break


def format_date(input_date):
    if input_date.lower() == 'today':
        return datetime.now().strftime('%b %d, %Y')
    elif input_date.lower() == 'yesterday':
        date = datetime.now() - timedelta(days=1)
        return date.strftime('%b %d, %Y')
    elif 'ago' in input_date:
        days_ago = int(input_date.split()[0])
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime('%b %d, %Y')
    else:
        return input_date


def get_backup_dealer(url):
    parsed_uri = urlparse(url)
    dealer = '{uri.netloc}'.format(uri=parsed_uri)
    return dealer


# ====================================================================================
# ====================================================================================
print('-----------------------------------------------')



min_miles = 0
max_miles = 1000000
gap_miles = 10

mile_ranges = [[i, i + gap_miles] for i in range(min_miles, max_miles, gap_miles)]


for min_mile, max_mile in mile_ranges:
    # print(f"Processing data for mile range: {mile_range}")
    url_mn_mile = '&minmiles=' + str(min_mile)
    url_mx_mile = '&maxmiles=' + str(max_mile)
    mile_url = base_url+url_mn_mile+url_mx_mile
    driver.get(mile_url)
    click_load_more(driver)

    result_list_items = driver.find_elements(By.CLASS_NAME, "result-wrap")
    print(f"result-list-items are :{len(result_list_items)}")
    for result_index, result_item in enumerate(result_list_items, start=1):
        current_car = {}
        try:
            try:
                name_item = result_item.find_element(By.XPATH, ".//span/a[@class='listing-link source-link']")
                current_car['Name'] = name_item.text
                car_url = name_item.get_attribute('href')
            except:
                current_car['Name'] = 'NA'
            xpath_dealer = ".//span/a[@class='logo-link']/img"
            try:
                current_car['Dealer'] = result_item.find_element(By.XPATH, xpath_dealer).get_attribute('alt')
            except:
                current_car['Dealer'] = get_backup_dealer(car_url)
            finally:
                current_car['Dealer']

            xpath_price = ".//div[@class='badge__label label--price']"
            try:
                current_car['Price'] = result_item.find_element(By.XPATH, xpath_price).text
            except:
                current_car['Price'] = 'NA'

            try:
                current_car['Mileage'] = result_item.find_element(By.CLASS_NAME, 'mileage').text
            except:
                current_car['Mileage'] = 'NA'

            try:
                raw_date = result_item.find_element(By.CLASS_NAME, 'date').text
                current_car['Listed'] = format_date(raw_date)
            except:
                current_car['Listed'] ='NA'

            try:
                current_car['City'] = result_item.find_element(By.CLASS_NAME, 'city').text
            except:
                current_car['City'] = 'NA'

            try:
                xpath_vin = ".//div[@class='inline-tools']/div[@class='tools']/div/a"
                vin_element = driver.find_element(By.XPATH, xpath_vin)
                onclick_value = vin_element.get_attribute('onclick')
                vin_pattern = re.compile(r"`([A-Z0-9]{17})`")
                current_car['VIN'] = vin_pattern.findall(onclick_value)
            except:
                current_car['VIN'] = 'NA'
            current_car['Link'] = name_item.get_attribute('href')
        except:
            print(f"Had issue with index:{result_index} and item:{result_item}")

        SCRAPPED_DATA.append(current_car.copy())
        current_car.clear()

print(len(SCRAPPED_DATA))
csv_path = 'AutoTempest_Extract' + str(time.time()) + '.csv'
df = pd.DataFrame(SCRAPPED_DATA)
df.to_csv(csv_path, index=False)