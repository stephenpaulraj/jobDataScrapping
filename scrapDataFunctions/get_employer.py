import json
from scrapDataFunctions import utils
from scrapDataFunctions import hasura_calls
import io


def scrap_employer_data(url, link):
    employer_temp = []
    employer_employer_details = []

    employer_name_main_div = url.find('div', {'vocab': 'http://schema.org/'})
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
        job_region = job_region_a_tag[1].find('span', {'class': 'noc-location'}).get_text().strip()
        job = job_region.split(' Region')
        employer_employer_details.append(job[0])

        # job median wage
        median_wage = job_posting_region_div.find('dd').get_text().strip()
        wage = median_wage.split(' $/hour')
        employer_employer_details.append(wage[0])

        # job location
        job_location_ul_tag = url.find('ul', {'class': 'job-posting-brief'})
        job_location_li_tags = job_location_ul_tag.find_all('li')

        # job location address
        job_location_address = job_location_li_tags[0].find('span', {'property': 'addressLocality'}).get_text()
        employer_employer_details.append(job_location_address)

        # job location province
        job_location_province = job_location_li_tags[0].find('span', {'property': 'addressRegion'}).get_text()
        employer_employer_details.append(job_location_province)

        employer_temp.append(employer_employer_details)

        email = utils.selenium_data(link)

        latitude, longitude = utils.convert_into_latitude_longitude(link)

        employer_employer_details.append(email)
        employer_employer_details.append(latitude)
        employer_employer_details.append(longitude)

        print('Inserting Employer Data...')

        employer_id = hasura_calls.insert_employer_info(emp_name, noc_id, job_location_province,
                                                        job[0], emp_url, email, latitude, longitude,
                                                        job_location_address)

        print(emp_name, noc_id, job_location_province,
              job[0], emp_url, email, latitude, longitude,
              job_location_address)
    return employer_id
