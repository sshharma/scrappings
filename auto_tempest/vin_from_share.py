import re
import time

from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

chrome_path = 'D:/Applications/Chrome-Driver/latest/chromedriver.exe'

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website you want to scrape
url = 'https://www.autotempest.com/results?zip=30024&localization=country'
driver.get(url)
driver.maximize_window()
time.sleep(2)


load_button = "//button[@class='more-results']"

# ==============this part of the code will load entire webpage=======================
# ===================================================================================


# Function to check if the button is present on the page
def is_button_present():
    try:
        button = driver.find_element(By.XPATH, load_button)
        return True
    except:
        return False


# Keep clicking on the button until it no longer appears
while is_button_present():
    try:
        button = driver.find_element(By.XPATH, load_button)
        button.click()
        time.sleep(2)
    except ElementNotInteractableException:
        print('data loading buttons are not clickable anymore.')
        break
    except NoSuchElementException:
        print('No More loading buttons found on the page')
        break
    except ElementClickInterceptedException:
        print('got ElementClickInterceptedException on the page')
        break
    except:
        print('got unknown issue on the page')
        break

# ====================================================================================

print('--------------------')

# Define your XPath
xpath = "//div[@class='share-link inline-tool']"

# Find all elements that match the XPath
elements = driver.find_elements(By.XPATH, xpath)
print(f"Total elements found: {len(elements)}")
# Iterate through each element
for index, element in enumerate(elements, start=1):
    anchor_element = element.find_element(By.TAG_NAME, 'a')
    onclick_value = anchor_element.get_attribute('onclick')
    vin_pattern = re.compile(r"`([A-Z0-9]{17})`")
    matches = vin_pattern.findall(onclick_value)

    # Extracted VIN numbers
    print(f"Current value: {matches}")