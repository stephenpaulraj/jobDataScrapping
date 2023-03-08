import re
from datetime import datetime as dsf

import requests
from bs4 import BeautifulSoup
import json
from scrapDataFunctions import utils


def collect_company_info(url_data):

    final_data = []
    employer_temp = []
    job_temp = []
    addi_details = []
    count = 0
    link = url_data
    for index, li in enumerate(link):
        print('-- Data Collecting ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')
        employer_employer_details = []
        page = requests.get(li)
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
        job_location_ul_tag = soup.find('ul', {'class': 'job-posting-brief'})
        job_location_li_tags = job_location_ul_tag.find_all('li')

        # job location address
        job_location_address = job_location_li_tags[0].find('span', {'property': 'addressLocality'}).get_text()
        employer_employer_details.append(job_location_address)

        # job location province
        job_location_province = job_location_li_tags[0].find('span', {'property': 'addressRegion'}).get_text()
        employer_employer_details.append(job_location_province)
        count += 1

        employer_temp.append(employer_employer_details)

        email = utils.selenium_data(li)

        latitude, longitude = utils.convert_into_latitude_longitude(li)

        print('---- Employer Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Basic Information                                    #
        # ================================================================= #

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
        job_temp.append(job_location)

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
            job_temp.append(base_salary)
        # working hours
        work_hours_span = job_posting_li[1].find('span', {'property': 'workHours'}).get_text().strip()
        job_temp.append(work_hours_span)

        print('---- Job Basic Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

    # ================================================================= #
    #          Job Details                                              #
    # ================================================================= #

        term_of_employment_span = job_posting_li[2].find_all('span')
        if term_of_employment_span[1].get_text() == 'Terms of employment':
            term_of_employment = term_of_employment_span[2].find('span').get_text()
            job_temp.append(term_of_employment)
        else:
            term_of_employment = "Not available"
            job_temp.append(term_of_employment)

        # Special commitments - 5
        special_commitments_span = job_posting_li[3].find_all('span')
        if special_commitments_span[1].get('property') == "specialCommitments":
            special_commitments = special_commitments_span[1].get_text().strip()
            job_temp.append(special_commitments)
        else:
            special_commitments = "Not available"
            job_temp.append(special_commitments)

        # Start date - 6
        start_date_span_1 = job_posting_li[4].find('span', {'class': 'fa-calendar'})
        start_date_span_2 = job_posting_li[3].find('span', {'class': 'fa-calendar'})
        if start_date_span_1 is not None:
            start_date_span = job_posting_li[4].find_all('span')
            start_date = start_date_span[2].get_text()
            job_temp.append(start_date)
        elif start_date_span_2 is not None:
            start_date_span = job_posting_li[3].find_all('span')
            start_date = start_date_span[2].get_text()
            job_temp.append(start_date)
        else:
            start_date = "Not available"
            job_temp.append(start_date)

        # Job benefits - 7
        job_benefit_span_1 = job_posting_li[5].find('span', {'class': 'fa-gift'})
        job_benefit_span_2 = job_posting_li[4].find('span', {'class': 'fa-gift'})
        if job_benefit_span_1 is not None:
            job_benefits_split = job_posting_li[5].get_text().split('Benefits:')
            job_benefits = job_benefits_split[1].strip()
            job_temp.append(job_benefits)
        elif job_benefit_span_2 is not None:
            job_benefits_split = job_posting_li[4].get_text().split('Benefits:')
            job_benefits = job_benefits_split[1].strip()
            job_temp.append(job_benefits)
        else:
            job_benefits = "Not available"
            job_temp.append(job_benefits)

        # Vacancies - 8
        vacancies_span_1 = job_posting_li[6].find('span', {'class': 'fa-user'})
        vacancies_span_2 = job_posting_li[5].find('span', {'class': 'fa-user'})
        vacancies_span_3 = job_posting_li[4].find('span', {'class': 'fa-user'})
        if vacancies_span_1 is not None:
            vacancy_span = job_posting_li[6].find_all('span')
            vacancy = vacancy_span[2].get_text().strip()
            job_temp.append(vacancy)
        elif vacancies_span_2 is not None:
            vacancy_span = job_posting_li[5].find_all('span')
            vacancy = vacancy_span[2].get_text().strip()
            job_temp.append(vacancy)
        elif vacancies_span_3 is not None:
            vacancy_span = job_posting_li[4].find_all('span')
            vacancy = vacancy_span[2].get_text().strip()
            job_temp.append(vacancy)
        else:
            vacancy = "Not available"
            job_temp.append(vacancy)

        #  job_type - 9
        if len(job_posting_li) >= 7:
            try:
                job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
                if job_type_span_1 is not None:
                    job_type = job_posting_li[7].get_text().strip()
                    job_temp.append(job_type)
            except IndexError:
                pass

        job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
        job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})

        if job_type_span_2 is not None:
            job_type = job_posting_li[6].get_text().strip()
            job_temp.append(job_type)
        elif job_type_span_3 is not None:
            job_type = job_posting_li[5].get_text().strip()
            job_temp.append(job_type)
        else:
            job_type = "Not available"
            job_temp.append(job_type)

        # Job type
        if len(job_posting_li) > 6:
            try:
                job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
                if job_type_span_1 is not None:
                    job_type = job_posting_li[7].get_text().strip()
                    job_temp.append(job_type)
            except IndexError:
                job_type = "Not available"
                job_temp.append(job_type)
        else:
            job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
            job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})

            if job_type_span_2 is not None:
                job_type = job_posting_li[6].get_text().strip()
                job_temp.append(job_type)
            elif job_type_span_3 is not None:
                job_type = job_posting_li[5].get_text().strip()
                job_temp.append(job_type)
            else:
                job_type = "Not available"
                job_temp.append(job_type)


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
        print('---- Job Detail Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

    final_data.append(job_temp)
    final_data.append(employer_temp)
    final_data.append(addi_details)
    print('-- All Data collected Successfully')
    return final_data
