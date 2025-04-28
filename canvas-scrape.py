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

from question import Question

usr = 0
chrome_driver = '/Users/quinnedgar/chromedriver-mac-arm64/chromedriver'
url = 'https://canvas.oregonstate.edu/courses/1999561/quizzes/3035252/take'

options = Options()
options.add_argument(f"user-data-dir=user-sessions/user-0") #tempfile.mkdtemp()
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
    if '--user-data-dir' in str(e):
        print('User directory busy')
    else: raise
    

except se.TimeoutException:
    print("\nAuthentication failed, please sign in\n")
    current_time = time.time()

    if '--headless' in options.arguments:
        options.arguments.remove('--headless')

    if driver:
        driver.quit()

    attempts = 0
    dr = create_driver()
    dr.get("https://canvas.oregonstate.edu/")

    while True:
        if (time.time() - current_time > 90): 
            print('Timeout, Exiting...')
            break

        try:
            WebDriverWait(dr, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ic-DashboardCard__header_hero"))
            )
            print('Auth Success')
            break

        except se.TimeoutException:
            attempts += 1
            print(f'Attempt No. - {attempts}')
        
        except Exception as e:
            print(f'Err: {e}')
            break

finally:
    if driver: driver.quit()



try:
    dr = create_driver()
    dr.get(url)
    search_boxes = WebDriverWait(dr, 100).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text'))
    )

    open('scraped.json', 'w')
    for bx in search_boxes:
        ob = Question(bx.text)
        ob.jsonify()

finally:
    print('JSON Written')
    dr.quit()
