import logging
import operator
import time
from functools import reduce
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import pytz
import datetime
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from json.decoder import JSONDecodeError
from geopy.geocoders import Nominatim
wb = Workbook()
import json
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger


requests_logger.setLevel(logging.WARN)


def canada_timezone():
    # Set the timezone to Eastern Time (Canada)
    canada_tz = pytz.timezone('America/Toronto')
    return canada_tz


def scrap_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Finding main all links div

    finding_main_div = soup.find('div', {'class': 'results-jobs'})
    links_article = finding_main_div.find_all('article')
    for url in links_article:
        links = url.find('a')
        if links is not None:
            href = links.get('href')
            full_url = "https://www.jobbank.gc.ca/" + href

    length = len(links_article)
    last = links_article[24]
    finding_date_sec = last.find('ul', {'class': 'list-unstyled'})
    finding_date_li = finding_date_sec.find('li', {'class': 'date'}).get_text()
    date = finding_date_li.split(',')
    remove_month = date[0].split('February')
    last_element_month = remove_month[1].strip()
    return last_element_month


def check_current_date():
    # Get the current local time
    current_time = datetime.datetime.now(canada_timezone())
    current_date = current_time.strftime("%d")
    c = int(current_date)-1
    return current_date


def collect_urls_list():
    default_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?page=1&sort=D&fsrc=16"
    count = 1
    urls_to_scrape = []
    urls_to_scrape.append(default_url)
    while count < 1000:
        if scrap_data(default_url) == check_current_date():
            count += 1
            default_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?page=" + str(count) + "&sort=D&fsrc=16"
            urls_to_scrape.append(default_url)
        else:
            break

    return urls_to_scrape


def collect_main_urls_list():
    main_urls_to_collect_company_name = []
    url_lists = collect_urls_list()
    for url in url_lists:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Finding main all links div

        finding_main_div = soup.find('div', {'class': 'results-jobs'})
        links_article = finding_main_div.find_all('article')
        for url in links_article:
            temp = []
            links = url.find('a')
            if links is not None:
                href = links.get('href')
                full_url = "https://www.jobbank.gc.ca/" + href
                main_urls_to_collect_company_name.append(full_url)

    return main_urls_to_collect_company_name


temp = []


async def collect_company_info():

    count = 0
    link = collect_main_urls_list()
    for l in link:
        employer_employer_details = []
        page = requests.get(l)
        soup = BeautifulSoup(page.content, 'html.parser')
        employer_name_main_div = soup.find('div', {'vocab': 'http://schema.org/'})
        employer_name_p_tag = employer_name_main_div.find('p', {'class': 'date-business'})
        employer_name_span = employer_name_p_tag.find('span', {'property': 'name'})
        emp_name = ""
        emp_url = ""
        if employer_name_span.find('strong') is not None:
            emp_name = employer_name_span.get_text().strip()
            employer_employer_details.append(emp_name)
            emp_url = "Not available"

        else:
            emp = employer_name_span.find('a')
            emp_url = emp.get('href')
            emp_name = employer_name_span.get_text().strip()
            employer_employer_details.append(emp_name)
            employer_employer_details.append(emp_url)

        # job posting details

        job_posting_region_div = soup.find('div', {'class': 'job-posting-details-jmi-content'})
        job_region_a_tag = job_posting_region_div.find_all('a')

        # noc number
        noc_no = job_region_a_tag[0].find('span', {'class': 'noc-no'}).get_text()
        noc = noc_no.split('NOC ')
        with open('noc.json', 'r') as file:
            data = json.load(file)
            #ssss = '95105'
            ddd = data['data']['noc']
            noc_id = ''
            for d in ddd:
                if noc[1] == d['noc_code']:
                    noc_id = d['id']
        # noc = "10010"
        # try:
        #
        #     load_dotenv()
        #     url: str = os.environ["SUPABASE_URL"]
        #     key: str = os.environ["SUPABASE_KEY"]
        #     supabase: Client = create_client(url, key)
        #     noc_data = supabase.table("noc").select().eq("noc_code", noc[1]).execute()
        #
        #     #print(noc_data)
        #     # if len(noc_data.data>0):
        #     #     employer_employer_details.append(noc[1])
        # except JSONDecodeError as e:
        #     print(e)


        # job posting region name
        job_region = job_region_a_tag[1].find('span', {'class': 'noc-location'}).get_text().strip()
        job = job_region.split(' Region')
        employer_employer_details.append(job[0])

        # job median wage
        median_wage = job_posting_region_div.find('dd').get_text().strip()
        wage = median_wage.split(' $/hour')
        employer_employer_details.append(wage[0])

        # job location
        job_location_ul_tag = soup.find('ul', {'class': 'job-posting-brief'})
        job_location_li_tags = job_location_ul_tag.find_all('li')

        # job location address
        job_location_address = job_location_li_tags[0].find('span', {'property': 'addressLocality'}).get_text()
        employer_employer_details.append(job_location_address)

        # job location province
        job_location_province = job_location_li_tags[0].find('span', {'property': 'addressRegion'}).get_text()
        employer_employer_details.append(job_location_province)
        count += 1

        temp.append(employer_employer_details)

        email = selenium_data(l)

        latitude, longitude = convert_into_latitude_longitude(l)



        # try:
        #
        #     load_dotenv()
        #     url: str = os.environ["SUPABASE_URL"]
        #     key: str = os.environ["SUPABASE_KEY"]
        #     supabase: Client = create_client(url, key)
        #     supabase.table("employers").insert({"employer_name": emp_name, "employer_url": emp_url, "employer_noc_id": noc_id, "employer_region": job[0], "employer_address": job_location_address, "employer_province": job_location_province, "employer_email_address": email, "latitude": latitude, "longitude": longitude}).execute()
        # except JSONDecodeError as e:
        #     print(e)

        transport = AIOHTTPTransport(
            url='https://engaged-puma-42.hasura.app/v1/graphql',
            headers={'content-type': 'application/json',
                     'x-hasura-admin-secret': 'ahFsQwjyqg2UFjVGT3L786keKu7089kDC856PmO5486BV0sp5U3aHqL0FuB40Slw'}
        )

        client = Client(transport=transport, fetch_schema_from_transport=True)
        # Execute single query
        query = gql(
            """
            mutation insertEmployerInfo($employer_name: String = "", $employer_noc_id: bigint = "", $employer_province: String = "", $employer_region: String = "", $employer_url: String = "", $employer_email_address: String = "", $latitude: float8 = "", $longitude: float8 = "", $employer_address: String = "") {
            insert_employers(objects: {employer_name: $employer_name, employer_noc_id: $employer_noc_id, employer_province: $employer_province, employer_region: $employer_region, employer_url: $employer_url, employer_email_address: $employer_email_address, latitude: $latitude, longitude: $longitude, employer_address: $employer_address}) {
            returning {
                  id
                }
              }
            }
            """
        )
        param = {"employer_name": emp_name, "employer_noc_id": noc_id, "employer_province": job_location_province, "employer_region": job[0], "employer_url": emp_url, "employer_email_address": email, "latitude": latitude, "longitude": longitude, "employer_address": job_location_address}

        result = await client.execute_async(query, variable_values=param)

        employer_id = result['insert_employers']['returning'][0]['id']

        # collect_job_info(l, employer_id)


def collect_job_info():
    print('sss')

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


#collect_company_info()

# noc = "10010"
# try:
#
#     load_dotenv()
#     url: str = os.environ["SUPABASE_URL"]
#     key: str = os.environ["SUPABASE_KEY"]
#     supabase: Client = create_client(url, key)
#     noc_data = supabase.table("noc").select().eq("noc_code", noc).execute()
#
#     print(noc_data.data)
#     print("hello")
#     # if len(noc_data.data>0):
#     #     employer_employer_details.append(noc[1])
# except JSONDecodeError as e:
#     print(e)
# noc = "10010"
# load_dotenv()
# url: str = os.environ["SUPABASE_URL"]
# key: str = os.environ["SUPABASE_KEY"]
# supabase: Client = create_client(url, key)
# noc_data = supabase.table("noc").select().eq("noc_code", noc).execute()
#
# print(noc_data.data)
# print("hello")
#

# asyncio.run(collect_company_info())

collect_job_info()







