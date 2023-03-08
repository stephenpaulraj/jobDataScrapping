import logging
import operator
import re
import time
from datetime import datetime as dsf
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
import test


requests_logger.setLevel(logging.WARN)

transport = AIOHTTPTransport(
        url='https://engaged-puma-42.hasura.app/v1/graphql',
        headers={'content-type': 'application/json',
                 'x-hasura-admin-secret': 'ahFsQwjyqg2UFjVGT3L786keKu7089kDC856PmO5486BV0sp5U3aHqL0FuB40Slw'}
    )

client = Client(transport=transport, fetch_schema_from_transport=True)

async def insert_job_additional_info(job_id, topic, sub_topic, content):

    # Execute single query
    query = gql(
        """
        mutation insert_job_additional($job_additional_info_content: String = "", $job_additional_info_sub_topic: String = "", $job_additional_info_topic: String = "", $job_basic_info_id: bigint = "") {
          insert_job_additional_details(objects: {job_additional_info_content: $job_additional_info_content, job_additional_info_sub_topic: $job_additional_info_sub_topic, job_additional_info_topic: $job_additional_info_topic, job_basic_info_id: $job_basic_info_id}) {
            returning {
              id
            }
          }
        }
        """
    )
    param = {"job_additional_info_content": content, "job_additional_info_sub_topic": sub_topic, "job_additional_info_topic": topic,
             "job_basic_info_id": job_id}

    result = await client.execute_async(query, variable_values=param)

async def insert_job_basic_info(job_t, e_id, salary, hour, loc, posted):

    # Execute single query
    query = gql(
        """
        mutation insert_job_basic_info($employer_id: bigint = "", $job_base_salary: String = "", $job_location: String = "", $job_posted_at: timestamp = "", $job_title: String = "", $job_work_hours: String = "") {
          insert_job_basic_information(objects: {employer_id: $employer_id, job_base_salary: $job_base_salary, job_location: $job_location, job_posted_at: $job_posted_at, job_title: $job_title, job_work_hours: $job_work_hours}) {
            returning {
              id
            }
          }
        }

        """
    )
    param = {"employer_id": e_id, "job_base_salary": salary, "job_location": loc,
             "job_posted_at": posted, "job_title": job_t, "job_work_hours": hour}

    result = client.execute(query, variable_values=param)


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
    remove_month = date[0].split(' ')
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
        print(l)
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

        await collect_job_info(soup, employer_id)


async def collect_job_info(soup, e_id):
    temp = []
    addi_details = []

    # finding main div for job info
    main_div = soup.find('div', {'typeof': 'JobPosting'})

    # job position name
    job_name_h1 = main_div.find('h1')
    job_name = job_name_h1.find('span', {'property': 'title'}).get_text().strip().title()

    # Date of job posted
    date_p_tag = main_div.find('p', {'class': 'date-business'})
    date_span = date_p_tag.find('span', {'class': 'date'}).get_text()
    date_trim = date_span.split('Posted on')
    date_conversion = date_trim[1].strip()
    date_1 = dsf.strptime(date_conversion, '%B %d, %Y')
    ss = str(date_1)
    new_date = dsf.strptime(ss, '%Y-%m-%d %H:%M:%S')
    sd = new_date.strftime('%d-%m-%Y')

    # Job posting summary
    job_posting_ul = main_div.find('ul', {'class': 'job-posting-brief'})
    job_posting_li = job_posting_ul.find_all('li')

    # Job location
    job_location_split = job_posting_li[0].get_text().split('Location')
    job_location = job_location_split[1].strip()
    temp.append(job_location)

    # Base salary
    base_salary = ''
    base_salary_span = job_posting_li[1].find('span', {'property': 'baseSalary'}).get_text()
    if base_salary_span.endswith(' hourly') or base_salary_span.endswith(
            ' annually (to be negotiated)') or base_salary_span.endswith(
            ' hourly (to be negotiated)') or base_salary_span.endswith(
            ' daily (to be negotiated)') or base_salary_span.endswith('commission per sale'):
        base_salary_split = re.split('HOUR|YEAR|DAY', base_salary_span)
        base_salary = base_salary_split[0] + '' + base_salary_split[1]
        # print(base_salary)
        temp.append(base_salary)
    # working hours
    work_hours_span = job_posting_li[1].find('span', {'property': 'workHours'}).get_text().strip()
    temp.append(work_hours_span)

    query = gql(
        """
        mutation insert_job_basic_info($employer_id: bigint = "", $job_base_salary: String = "", $job_location: String = "", $job_posted_at: timestamp = "", $job_title: String = "", $job_work_hours: String = "") {
          insert_job_basic_information(objects: {employer_id: $employer_id, job_base_salary: $job_base_salary, job_location: $job_location, job_posted_at: $job_posted_at, job_title: $job_title, job_work_hours: $job_work_hours}) {
            returning {
              id
            }
          }
        }

        """
    )
    param = {"employer_id": e_id, "job_base_salary": base_salary, "job_location": job_location,
             "job_posted_at": sd, "job_title": job_name, "job_work_hours": work_hours_span}

    result = await client.execute_async(query, variable_values=param)

    job_id = result['insert_job_basic_information']['returning'][0]['id']

    # Terms of employment - 4

    term_of_employment_span = job_posting_li[2].find_all('span')
    if term_of_employment_span[1].get_text() == 'Terms of employment':
        term_of_employment = term_of_employment_span[2].find('span').get_text()
        temp.append(term_of_employment)
    else:
        term_of_employment = "Not available"
        temp.append(term_of_employment)

    # Special commitments - 5
    special_commitments_span = job_posting_li[3].find_all('span')
    if special_commitments_span[1].get('property') == "specialCommitments":
        special_commitments = special_commitments_span[1].get_text().strip()
        temp.append(special_commitments)
    else:
        special_commitments = "Not available"
        temp.append(special_commitments)

    # Start date - 6
    start_date_span_1 = job_posting_li[4].find('span', {'class': 'fa-calendar'})
    start_date_span_2 = job_posting_li[3].find('span', {'class': 'fa-calendar'})
    if start_date_span_1 is not None:
        start_date_span = job_posting_li[4].find_all('span')
        start_date = start_date_span[2].get_text()
        temp.append(start_date)
    elif start_date_span_2 is not None:
        start_date_span = job_posting_li[3].find_all('span')
        start_date = start_date_span[2].get_text()
        temp.append(start_date)
    else:
        start_date = "Not available"
        temp.append(start_date)

    # Job benefits - 7
    job_benefit_span_1 = job_posting_li[5].find('span', {'class': 'fa-gift'})
    job_benefit_span_2 = job_posting_li[4].find('span', {'class': 'fa-gift'})
    if job_benefit_span_1 is not None:
        job_benefits_split = job_posting_li[5].get_text().split('Benefits:')
        job_benefits = job_benefits_split[1].strip()
        temp.append(job_benefits)
    elif job_benefit_span_2 is not None:
        job_benefits_split = job_posting_li[4].get_text().split('Benefits:')
        job_benefits = job_benefits_split[1].strip()
        temp.append(job_benefits)
    else:
        job_benefits = "Not available"
        temp.append(job_benefits)

    # Vacancies - 8
    vacancies_span_1 = job_posting_li[6].find('span', {'class': 'fa-user'})
    vacancies_span_2 = job_posting_li[5].find('span', {'class': 'fa-user'})
    vacancies_span_3 = job_posting_li[4].find('span', {'class': 'fa-user'})
    if vacancies_span_1 is not None:
        vacancy_span = job_posting_li[6].find_all('span')
        vacancy = vacancy_span[2].get_text().strip()
        temp.append(vacancy)
    elif vacancies_span_2 is not None:
        vacancy_span = job_posting_li[5].find_all('span')
        vacancy = vacancy_span[2].get_text().strip()
        temp.append(vacancy)
    elif vacancies_span_3 is not None:
        vacancy_span = job_posting_li[4].find_all('span')
        vacancy = vacancy_span[2].get_text().strip()
        temp.append(vacancy)
    else:
        vacancy = "Not available"
        temp.append(vacancy)

    #  job_type - 9
    if len(job_posting_li) >= 7:
        try:
            job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
            if job_type_span_1 is not None:
                job_type = job_posting_li[7].get_text().strip()
                temp.append(job_type)
        except IndexError:
            pass

    job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
    job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})

    if job_type_span_2 is not None:
        job_type = job_posting_li[6].get_text().strip()
        temp.append(job_type)
    elif job_type_span_3 is not None:
        job_type = job_posting_li[5].get_text().strip()
        temp.append(job_type)
    else:
        job_type = "Not available"
        temp.append(job_type)

    # Job type
    if len(job_posting_li) > 6:
        try:
            job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
            if job_type_span_1 is not None:
                job_type = job_posting_li[7].get_text().strip()
                temp.append(job_type)
        except IndexError:
            job_type = "Not available"
            temp.append(job_type)
    else:
        job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
        job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})

        if job_type_span_2 is not None:
            job_type = job_posting_li[6].get_text().strip()
            temp.append(job_type)
        elif job_type_span_3 is not None:
            job_type = job_posting_li[5].get_text().strip()
            temp.append(job_type)
        else:
            job_type = "Not available"
            temp.append(job_type)

        #=========================================================================
    # finding main div for job info

    comparison_chart = soup.find('div', {'class': 'comparisonchart'})
    all_divs = comparison_chart.find_all('div', {'property': True})
    all_divs.pop(0)

    for m in all_divs:
        details = []
        all_h3_tag = m.find('h3').get_text()
        all_h4_tag = m.find_all('h4')
        h4_array = []
        for k in all_h4_tag:
            h4 = k.get_text().strip()  # All sub topic
            h4_array.append(h4)
        all_ul_tag = m.find_all('ul')
        s = []
        for index, li_s in enumerate(all_ul_tag):
            all_list = li_s.find_all('li')
            for jj in all_list:
                temp_1 = []
                one_list = jj.get_text().strip()
                temp_1.append(all_h3_tag)
                temp_1.append(h4_array[index])
                temp_1.append(one_list)
                addi_details.append(temp_1)
    print('Information collected')

    query_1 = gql(
        """
        mutation insert_job_details($job_basic_info_id: bigint = "", $job_benefits: String = "", $job_type: String = "", $special_commitment: String = "", $start_date: String = "", $term_of_employment: String = "", $total_vacancies: String = "") {
          insert_job_details(objects: {job_basic_info_id: $job_basic_info_id, job_benefits: $job_benefits, job_type: $job_type, special_commitment: $special_commitment, start_date: $start_date, term_of_employment: $term_of_employment, total_vacancies: $total_vacancies}) {
            returning {
              id
            }
          }
        }

        """
    )
    param_1 = {"job_basic_info_id": job_id, "job_benefits": temp[6], "job_type": temp[8],
             "special_commitment": temp[4], "start_date": temp[5], "term_of_employment": temp[3], "total_vacancies": temp[7]}

    result_1 = await client.execute_async(query_1, variable_values=param_1)
    # ==========================================================================


    for one in addi_details:
        print('Adding to db')
        query_2 = gql(
            """
            mutation insert_job_additional($job_additional_info_content: String = "", $job_additional_info_sub_topic: String = "", $job_additional_info_topic: String = "", $job_basic_info_id: bigint = "") {
              insert_job_additional_details(objects: {job_additional_info_content: $job_additional_info_content, job_additional_info_sub_topic: $job_additional_info_sub_topic, job_additional_info_topic: $job_additional_info_topic, job_basic_info_id: $job_basic_info_id}) {
                returning {
                  id
                }
              }
            }
            """
        )
        param_2 = {"job_additional_info_content": one[2], "job_additional_info_sub_topic": one[1],
                 "job_additional_info_topic": one[0], "job_basic_info_id": job_id}

        result_2 = await client.execute_async(query_2, variable_values=param_2)

        print('done adding')
        print(result_2)


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


asyncio.run(collect_company_info())








