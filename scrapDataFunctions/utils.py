import time
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def selenium_data(url):
    DRIVER_PATH = '/chromeDriver/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(url)
    xpathArgs = '//*[@id="applynowbutton"]'

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpathArgs))
    )
    button = driver.find_element(By.ID, "applynowbutton")
    button.click()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    button_triggered_div = soup.find('div', {'class': 'howtoapply'})
    if button_triggered_div.find_all('p') is not None:
        finding_mail_address = button_triggered_div.find_all('p')
        if finding_mail_address[0].find('a') is not None:
            mail_address = finding_mail_address[0].find('a').get_text()
            driver.close()
            return mail_address
        else:
            return "noemail@gmail.com"
    else:
        return "noemail@gmail.com"


def convert_into_latitude_longitude(url):
    geolocator = Nominatim(user_agent="geoapiExercises")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # job location
    job_location_ul_tag = soup.find('ul', {'class': 'job-posting-brief'})
    job_location_li_tags = job_location_ul_tag.find_all('li')

    # job location address
    job_location_address = job_location_li_tags[0].find('span', {'property': 'addressLocality'}).get_text()

    # job location province
    job_location_province = job_location_li_tags[0].find('span', {'property': 'addressRegion'}).get_text()

    concatednated_location = job_location_address +", "+ job_location_province
    location = geolocator.geocode(concatednated_location)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude