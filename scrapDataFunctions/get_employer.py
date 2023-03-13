import asyncio
import json
from scrapDataFunctions import utils
from scrapDataFunctions import hasura_calls
import io
import colorama
from colorama import Fore
from scrapDataFunctions import get_job_basic_information, get_job_detail_information, get_job_additional_information

def scrap_employer_data(url, link):

    employer_name_main_div = url.find('div', {'vocab': 'http://schema.org/'})
    employer_name_p_tag = employer_name_main_div.find('p', {'class': 'date-business'})
    employer_name_span = employer_name_p_tag.find('span', {'property': 'name'})
    emp_name = ""
    emp_url = ""
    if employer_name_span.find('strong') is not None:
        emp_name = employer_name_span.get_text().strip()
        emp_url = "Not available"

    else:
        emp = employer_name_span.find('a')
        emp_url = emp.get('href')
        emp_name = employer_name_span.get_text().strip()

    # job posting details

    job_posting_region_div = url.find('div', {'class': 'job-posting-details-jmi-content'})
    job_region_a_tag = job_posting_region_div.find_all('a')

    # noc number
    noc_no = job_region_a_tag[0].find('span', {'class': 'noc-no'}).get_text()
    noc = noc_no.split('NOC ')
    with io.open('noc_folder/noc.json', 'r') as file:
        data = json.load(file)
        # ssss = '95105'
        ddd = data['data']['noc']
        noc_id = ''
        for d in ddd:
            if noc[1] == d['noc_code']:
                noc_id = d['id']

    # job posting region name
    if job_region_a_tag[1].find('span', {'class': 'noc-location'}):
        job_region_data = job_region_a_tag[1].find('span', {'class': 'noc-location'}).get_text().strip()
        job = job_region_data.split(' Region')
        job_region = job[0]
    else:
        job_region = '0'


    # job median wage
    if job_posting_region_div.find('dd'):
        median_wage = job_posting_region_div.find('dd').get_text().strip()
        wage_split = median_wage.split(' $/hour')
        wage = wage_split[0]
    else:
        wage = '0'

    # job location
    job_location_ul_tag = url.find('ul', {'class': 'job-posting-brief'})
    job_location_li_tags = job_location_ul_tag.find_all('li')

    # job location address
    if job_location_li_tags[0].find('span', {'property': 'addressLocality'}):
        job_location_address = job_location_li_tags[0].find('span', {'property': 'addressLocality'}).get_text()
    else:
        job_location_address = '0'

    # job location province
    if job_location_li_tags[0].find('span', {'property': 'addressRegion'}):
        job_location_province = job_location_li_tags[0].find('span', {'property': 'addressRegion'}).get_text()
    else:
        job_location_province = '0'

    email = utils.selenium_data(link)

    latitude, longitude = utils.convert_into_latitude_longitude(link)
    print(Fore.CYAN + '---- Calling GQl... ')
    employer_id = asyncio.run(hasura_calls.insert_employer_info(emp_name, noc_id, job_location_province,
                                                    job_region, emp_url, email, latitude, longitude,
                                                    job_location_address))

    print(Fore.YELLOW + '---- Employer Data Inserted... ' + str(employer_id))
    print(Fore.CYAN + '---- Calling GQl... ')
    job_id = get_job_basic_information.collect_job_basic_information(url, employer_id)

    print(Fore.YELLOW + '---- Job Basic Information  Inserted... ' + str(job_id))
    print(Fore.CYAN + '---- Calling GQl... ')
    job_details_id = get_job_detail_information.collect_job_detail_info(url, job_id)

    print(Fore.YELLOW + '---- Job Detail Information  Inserted... ' + str(job_details_id))
    print(Fore.CYAN + '---- Calling GQl... ')

    get_job_additional_information.collect_job_additional_info(url, job_id)
    print(Fore.YELLOW + '---- Job Additonal Detail Information  Inserted... ')





    return employer_id
