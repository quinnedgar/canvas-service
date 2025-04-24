import requests
from bs4 import BeautifulSoup
import openAI
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

usr = 1
chrome_driver = '/Users/quinnedgar/chromedriver-mac-arm64/chromedriver'
url = 'https://canvas.oregonstate.edu/courses/1999561/quizzes/3035252/take'

options = Options()
options.add_argument(f"user-data-dir=/Users/quinnedgar/selenium-profile") 

service = Service(executable_path=chrome_driver)


if not usr:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://canvas.oregonstate.edu/")
    input("Press Enter AFTER you are fully logged in...")

    driver.quit()
    exit()

else:
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(2)



try: 
    search_boxes = WebDriverWait(driver, 1000).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text'))
    )

    for i in search_boxes:
        print(i.text + '\n')

finally:
    time.sleep(10)
    driver.quit()


