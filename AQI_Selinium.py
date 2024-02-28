from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime

driver = webdriver.Chrome()

driver.get("https://www.timeanddate.com/")

driver.find_element(by=By.XPATH, value="//*[@class='site-nav-bar__button site-nav-bar__button--search']").click()
driver.find_element(by=By.XPATH, value="//*[@class='site-nav-bar__search']").send_keys('somajiguda')
driver.find_element(by=By.XPATH, value="//*[@class='site-nav-bar__button site-nav-bar__button--search']").click()

driver.find_element(by=By.XPATH, value="//a[@href='/worldclock/@10524278']").click()

element = driver.find_element(by=By.XPATH, value="//a[@href='/weather/@10524278']")
actions = ActionChains(driver)
actions.move_to_element(element).perform()
sub = driver.find_element(by=By.XPATH, value="//a[@href='/weather/@10524278/historic']")
actions.click(sub).perform()


def scrape_weather_data(driver, date_link, date):
    ActionChains(driver).move_to_element(date_link).click().perform()
    time.sleep(2)

    column_names = ['Time', 'Temperature', 'Weather', 'Wind Speed', 'Humidity', 'Pressure', 'Date']
    table = driver.find_element(By.ID, "wt-his")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    data_list = []

    for row in rows[1:-1]:
        columns = row.find_elements(By.TAG_NAME, "td")
        time_data = row.find_element(By.TAG_NAME, "th").text[0:5]
        data_list.append([time_data] + [column.text for i, column in enumerate(columns[1:-1]) if i != 3] + [date])

    return pd.DataFrame(data_list, columns=column_names)


date_links_div = driver.find_element(by=By.XPATH, value="//div[@class='row pdflexi']/div[@class='weatherLinks']")

date_link = date_links_div.find_elements(by=By.TAG_NAME, value="a")[1]

data = []

date_string = date_link.text
date_year = 2023 if "Dec" in date_string else 2024
date_object = datetime.strptime(f"{date_year} {date_string}", "%Y %d %b")
date = date_object.strftime("%Y-%m-%d")
weather_data = scrape_weather_data(driver, date_link, date)
data.append(weather_data)

result_df = pd.concat(data, ignore_index=True)

result_df['Temperature'] = result_df['Temperature'].str.extract('(\d+)').astype(float)
result_df['Wind Speed'] = result_df['Wind Speed'].str.extract('(\d+)').astype(float)
result_df['Humidity'] = result_df['Humidity'].str.extract('(\d+)').astype(float)
result_df['Pressure'] = result_df['Pressure'].str.extract('(\d+)').astype(float)

try:
    existing_data = pd.read_csv('AQI_Weather.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame()

final_data = pd.concat([existing_data, result_df], ignore_index=True)

final_data.to_csv('AQI_Weather.csv', index=False)

driver.quit()