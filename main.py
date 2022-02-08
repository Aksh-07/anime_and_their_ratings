from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from time import sleep

webdriver_url = "C:\chromedriver\chromedriver.exe"

service = Service(webdriver_url)
driver = webdriver.Chrome(service=service)
driver.get("https://next-episode.net/browse/?genre=41")

name_list = []
rating_list = []
summary_list = []
for i in range(7):
    list_items = driver.find_elements(By.CLASS_NAME, "list_item")
    for items in list_items:
        anime_name = items.find_elements(By.CSS_SELECTOR, ".headlinehref a")
        name = [items.text for items in anime_name]
        name_list.append(name)

        anime_ratings = items.find_elements(By.ID, "rating_result")
        rating = [items.get_attribute("innerHTML") for items in anime_ratings]
        rating_list.append(rating)

        summary = items.find_elements(By.CLASS_NAME, "summary")
        body = [items.get_attribute("innerHTML") for items in summary]
        summary_list.append(body)

    sleep(2)

    if i == 0:
        next_page = driver.find_element(By.XPATH, '//*[@id="paginationDiv"]/a[8]')
    elif i < 4:
        next_page = driver.find_element(By.XPATH, '//*[@id="paginationDiv"]/a[9]')
    else:
        next_page = driver.find_element(By.XPATH, '//*[@id="paginationDiv"]/a[10]')
    next_page.click()

data = pd.DataFrame(list(zip(name_list, rating_list, summary_list)), columns=["Name", "Rating", "Summary"])

