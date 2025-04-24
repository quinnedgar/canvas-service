from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import pickle
import time

usr = 1
chrome_driver = '/Users/quinnedgar/chromedriver-mac-arm64/chromedriver'
url = 'https://canvas.oregonstate.edu/courses/1999561/quizzes/3035252/take'

options = Options()
service = Service(executable_path=chrome_driver)
driver = webdriver.Chrome(service=service, options=options)


if not usr:
    driver.get("https://canvas.oregonstate.edu/login/ldap")

    WebDriverWait(driver, 1000).until(
        EC.url_contains("canvas.oregonstate.edu")
    )

    cookies = driver.get_cookies()
    with open("/Users/quinnedgar/cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)

else:
    driver.get("https://canvas.oregonstate.edu")

    with open("/Users/quinnedgar/cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
    for c in cookies:
        driver.add_cookie(c)



try: 
    search_boxes = WebDriverWait(driver, 1000).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text'))
    )

    for i in search_boxes:
        print(i.text)


finally:
    time.sleep(10)
    driver.quit()

'''
fl = open('/Users/quinnedgar/canvas.txt', 'w')
fl.write(driver.page_source)
'''
