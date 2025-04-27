import requests
import time
from bs4 import BeautifulSoup
import tempfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as se


from jsonify import Question

usr = 0
chrome_driver = '/Users/quinnedgar/chromedriver-mac-arm64/chromedriver'
url = 'https://canvas.oregonstate.edu/courses/1999561/quizzes/3035252/take'

options = Options()
options.add_argument(f"user-data-dir=selenium-sessions/selenium-profile") #tempfile.mkdtemp()
options.add_argument('--headless')

service = Service(executable_path=chrome_driver)

def create_driver():
    return webdriver.Chrome(service=service, options=options)
    

driver = None

try:
    st = time.time()
    print("Attempting to authenticate login...")
    driver = create_driver()
    driver.get("https://canvas.oregonstate.edu/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'DashboardCard_Container'))
    )

    driver.get(url)
    print("Authentication Verified")
    end = time.time()
    print(f'Auth Time: {end-st}')

    
except se.SessionNotCreatedException as e:
    if '--user-data-dir' in e:
        print('User directory busy')
    else: raise
    

except se.TimeoutException:
    print("\nAuthentication failed, please sign in\n")

    if '--headless' in options.arguments:
        options.arguments.remove('--headless')

    if driver:
        driver.quit()
    
    driver = create_driver()

    driver.get("https://canvas.oregonstate.edu/")
    input("Press Enter AFTER you are fully logged in...")

    driver.get(url)
    
try: 
    search_boxes = WebDriverWait(driver, 100).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text'))
    )

    open('scraped.json', 'w')
    for bx in search_boxes:
        ob = Question(bx.text)
        ob.jsonify()

finally:
    print('JSON Written')
    driver.quit()

