from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime

# convert the date from 'Aug 12, 2021' to 'August 2021'

def date_formater(date):
    d = datetime.datetime.strptime(date, '%b. %d, %Y')
    return d.strftime('%B %Y')


# create a function to right click until the date is found in the calendar

def press_right_arrow_until_date_is_found(date):
    # get the text of the initial calendar
    current_calendar = driver.find_element(By.CLASS_NAME, "uitk-calendar").text
    # while the date does not appear in the calendar view press right arrow until it does
    while(date_formater(date) not in current_calendar):
        right_arrow = driver.find_elements(By.XPATH, 
            "//button[@data-stid='date-picker-paging']")[1]
        right_arrow.click()
        current_calendar = driver.find_element(By.CLASS_NAME, "uitk-calendar").text


# function to select the dates using xpath with the unique attribute. Ex: aria-label="Aug 12, 2021"

def select_date(start_date_calendar, end_date_calendar):
    # press right until the start date is found
    press_right_arrow_until_date_is_found(start_date_calendar)
    # click on the date that matches the xpath with the aria-label
    driver.find_element(By.XPATH, 
        "//button[@aria-label='{}']".format(start_date_calendar)).click()
    time.sleep(1)

    # press right until the end date is found
    press_right_arrow_until_date_is_found(end_date_calendar)
    # click on the date that matches the xpath with the aria-label
    driver.find_element(By.XPATH,  
        "//button[@aria-label='{}']".format(end_date_calendar)).click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[@data-stid='apply-date-picker']").click()

    time.sleep(2)



# get the website
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
url = 'https://www.expedia.ca/'
driver.get(url)

# input destination
driver.find_element(By.CSS_SELECTOR, '.uitk-fake-input').click()
dest = driver.find_element(By.ID, 'location-field-destination')
dest.send_keys('Hong Kong')
dest.send_keys(Keys.ENTER)
time.sleep(2)

select = driver.find_elements(By.XPATH, "//li[@class='uitk-typeahead-result-item has-subtext']")
for city in select:
    if'Hong Kong' in city.text:
        city.click()
        break

time.sleep(1)


# input check-in and check-out date
start_date = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#d1-btn")))
end_date = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#d2-btn")), 5)
start_date.click()

time.sleep(1)

#date selection
select_date('Mar. 30, 2023', 'Apr. 4, 2023')

time.sleep(1)

search = driver.find_element(By.XPATH,"//button[@data-testid='submit-button']")
search.click()

time.sleep(10)

driver.close()