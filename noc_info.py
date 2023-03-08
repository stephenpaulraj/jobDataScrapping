import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import main
from datetime import datetime

url_list = main.collect_main_urls_list()
url = url_list[:1]




# for u in url:
# print(u)
page = requests.get('https://www.jobbank.gc.ca//jobsearch/jobposting/37788517;jsessionid=E2DDA58242EC9C9C7F8E098871B25FAC.jobsearch77?source=searchresults')
soup = BeautifulSoup(page.content, 'html.parser')

temp = []

# finding main div for job info
main_div = soup.find('div', {'typeof': 'JobPosting'})

# # job position name
# job_name_h1 = main_div.find('h1')
# job_name = job_name_h1.find('span', {'property': 'title'}).get_text().strip().title()
#
# # Date of job posted
# date_p_tag = main_div.find('p', {'class': 'date-business'})
# date_span = date_p_tag.find('span', {'class': 'date'}).get_text()
# date_trim = date_span.split('Posted on')
# date_conversion = date_trim[1].strip()
# date_1 = datetime.strptime(date_conversion, '%B %d, %Y')
# ss = str(date_1)
# new_date = datetime.strptime(ss, '%Y-%m-%d %H:%M:%S')
# sd = new_date.strftime('%d-%m-%Y')
#
# Job posting summary
# job_posting_ul = main_div.find('ul', {'class': 'job-posting-brief'})
# job_posting_li = job_posting_ul.find_all('li')
#
# # Job location
# job_location_split = job_posting_li[0].get_text().split('Location')
# job_location = job_location_split[1].strip()
# temp.append(job_location)
#
# # Base salary
# base_salary = ''
# base_salary_span = job_posting_li[1].find('span', {'property': 'baseSalary'}).get_text()
# if base_salary_span.endswith(' hourly') or base_salary_span.endswith(' annually (to be negotiated)') or base_salary_span.endswith(' hourly (to be negotiated)') or base_salary_span.endswith(' daily (to be negotiated)') or base_salary_span.endswith('commission per sale'):
#     base_salary_split = re.split('HOUR|YEAR|DAY', base_salary_span)
#     base_salary = base_salary_split[0]+''+base_salary_split[1]
#     temp.append(base_salary)
# # working hours
# work_hours_span = job_posting_li[1].find('span', {'property': 'workHours'}).get_text().strip()
# temp.append(work_hours_span)
#
# # Terms of employment
#
# term_of_employment_span = job_posting_li[2].find_all('span')
# if term_of_employment_span[1].get_text() == 'Terms of employment':
#     term_of_employment = term_of_employment_span[2].find('span').get_text()
#     temp.append(term_of_employment)
# else:
#     term_of_employment = "Not available"
#     temp.append(term_of_employment)
#
# # Special commitments
# special_commitments_span = job_posting_li[3].find_all('span')
# if special_commitments_span[1].get('property') == "specialCommitments":
#     special_commitments = special_commitments_span[1].get_text().strip()
#     temp.append(special_commitments)
# else:
#     special_commitments = "Not available"
#     temp.append(special_commitments)
#
# # Start date
# start_date_span_1 = job_posting_li[4].find('span', {'class': 'fa-calendar'})
# start_date_span_2 = job_posting_li[3].find('span', {'class': 'fa-calendar'})
# if start_date_span_1 is not None:
#     start_date_span = job_posting_li[4].find_all('span')
#     start_date = start_date_span[2].get_text()
#     temp.append(start_date)
# elif start_date_span_2 is not None:
#     start_date_span = job_posting_li[3].find_all('span')
#     start_date = start_date_span[2].get_text()
#     temp.append(start_date)
# else:
#     start_date = "Not available"
#     temp.append(start_date)
#
# # Job benefits
# job_benefit_span_1 = job_posting_li[5].find('span', {'class': 'fa-gift'})
# job_benefit_span_2 = job_posting_li[4].find('span', {'class': 'fa-gift'})
# if job_benefit_span_1 is not None:
#     job_benefits_split = job_posting_li[5].get_text().split('Benefits:')
#     job_benefits = job_benefits_split[1].strip()
#     temp.append(job_benefits)
# elif job_benefit_span_2 is not None:
#     job_benefits_split = job_posting_li[4].get_text().split('Benefits:')
#     job_benefits = job_benefits_split[1].strip()
#     temp.append(job_benefits)
# else:
#     job_benefits = "Not available"
#     temp.append(job_benefits)
#
# # Vacancies
# vacancies_span_1 = job_posting_li[6].find('span', {'class': 'fa-user'})
# vacancies_span_2 = job_posting_li[5].find('span', {'class': 'fa-user'})
# vacancies_span_3 = job_posting_li[4].find('span', {'class': 'fa-user'})
# if vacancies_span_1 is not None:
#     vacancy_span = job_posting_li[6].find_all('span')
#     vacancy = vacancy_span[2].get_text().strip()
#     temp.append(vacancy)
# elif vacancies_span_2 is not None:
#     vacancy_span = job_posting_li[5].find_all('span')
#     vacancy = vacancy_span[2].get_text().strip()
#     temp.append(vacancy)
# elif vacancies_span_3 is not None:
#     vacancy_span = job_posting_li[4].find_all('span')
#     vacancy = vacancy_span[2].get_text().strip()
#     temp.append(vacancy)
# else:
#     vacancy = "Not available"
#     temp.append(vacancy)
#
# if len(job_posting_li) >= 7:
#     try:
#         job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
#         if job_type_span_1 is not None:
#             job_type = job_posting_li[7].get_text().strip()
#             temp.append(job_type)
#     except IndexError:
#         pass
#
# job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
# job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})
#
# if job_type_span_2 is not None:
#     job_type = job_posting_li[6].get_text().strip()
#     temp.append(job_type)
# elif job_type_span_3 is not None:
#     job_type = job_posting_li[5].get_text().strip()
#     temp.append(job_type)
# else:
#     job_type = "Not available"
#     temp.append(job_type)
#
# # Job type
# if len(job_posting_li) > 6:
#     try:
#         job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
#         if job_type_span_1 is not None:
#             job_type = job_posting_li[7].get_text().strip()
#             print(job_type)
#             temp.append(job_type)
#     except IndexError:
#         job_type = "Not available"
#         print(job_type)
#         temp.append(job_type)
# else:
#     job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
#     job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})
#
#     if job_type_span_2 is not None:
#         job_type = job_posting_li[6].get_text().strip()
#         print(job_type)
#         temp.append(job_type)
#     elif job_type_span_3 is not None:
#         job_type = job_posting_li[5].get_text().strip()
#         print(job_type)
#         temp.append(job_type)
#     else:
#         job_type = "Not available"
#         print(job_type)
#         temp.append(job_type)
# print(temp)
#
# # extracting overview info
# comparison_chart = soup.find('div', {'class': 'comparisonchart'})
#
# # Language
# if comparison_chart.find('p', {'property': 'qualification'}) is not None:
#     language = comparison_chart.find('p', {'property': 'qualification'}).get_text()
# else:
#     language = '0'
#
# # Education
# education_ul = comparison_chart.find('ul', {'property': 'educationRequirements qualification'})
# if education_ul is not None:
#     education = education_ul.find('li').get_text().strip()
# else:
#     education = '0'
#
# # Experience
# if comparison_chart.find('p', {'property': 'experienceRequirements qualification'}) is not None:
#     experience = comparison_chart.find('p', {'property': 'experienceRequirements qualification'}).get_text().strip()
# else:
#     experience = '0'
#
# # work site environment & work setting
# work_setting_div = comparison_chart.find('div', {'property': ''})
# if work_setting_div is not None:
#     if len(work_setting_div.find_all('ul')) > 1:
#         work_h4 = work_setting_div.find_all('h4')
#         work_ul = work_setting_div.find_all('ul')
#         for work, work_li in zip(work_h4, work_ul):
#             work_h4_tag = work.get_text().strip()
#             works = work_li.get_text().strip()
#     elif len(work_setting_div.find_all('ul')) == 1:
#         work_h4_tag = work_setting_div.find('h4').get_text().strip()
#         works = work_setting_div.find('ul').get_text().strip()
#     else:
#         work_h4_tag = '0'
#         works = '0'
# else:
#     work_h4_tag = '0'
#     works = '0'
#
# # Responsibilities
# if comparison_chart.find('div', {'property': 'responsibilities'}) is not None:
#     responsibilities_div = comparison_chart.find('div', {'property': 'responsibilities'})
#     heading = responsibilities_div.find('h3').get_text()
#     if len(responsibilities_div.find_all('ul')) > 1:
#         responsibilities_h4 = responsibilities_div.find_all('h4')
#         responsibilities_ul = responsibilities_div.find_all('ul')
#         for res_h4, res_li in zip(responsibilities_h4, responsibilities_ul):
#             responsibilities_h4 = responsibilities_div.find('h4').get_text().strip()
#             responsibilities_li = res_li.find('li').get_text().strip()
#     elif len(responsibilities_div.find_all('ul')) == 1:
#         responsibilities_h4 = responsibilities_div.find('h4').get_text().strip()
#         responsibilities_li = responsibilities_div.find('ul').get_text().strip()
# else:
#     responsibilities_h4 = "0"
#     responsibilities_li = '0'
#
# # Credentials
# skills_property_div = comparison_chart.find_all('div', {'property': 'skills'})
# if len(skills_property_div) == 0:
#     credentials = "no credentials"
#     additional_information = "no addi"
# else:
#     if comparison_chart.find_all('div', {'property': 'skills'}) is not None:
#         credentials_h4 = skills_property_div[0].find_all('h4')
#         credentials_ul = skills_property_div[0].find_all('ul')
#         if len(skills_property_div) > 1:
#             if credentials_h4[0].get_text() == "Certificates, licences, memberships, and courses " and \
#                     skills_property_div[1].find('h3').get_text() == "Additional information":
#                 credentials_li = credentials_ul[0].find_all('li')
#                 for certificate in credentials_li:
#                     credentials = certificate.get_text().strip()
#                 add_info_ul = skills_property_div[1].find_all('ul')
#                 for a in add_info_ul:
#                     add_info_li = a.find_all('li')
#                     for b in add_info_li:
#                         additional_information = b.get_text().strip()
#             else:
#                 credentials = "No credentials"
#                 additional_information = "No additional information"
#         elif len(skills_property_div) <= 1:
#             try:
#                 if credentials_h4[0].get_text() == "Certificates, licences, memberships, and courses ":
#                     credentials_li = credentials_ul[0].find_all('li')
#                     for certificate in credentials_li:
#                         credentials = certificate.get_text().strip()
#                 else:
#                     credentials = "No credentials"
#                 if skills_property_div[0].find('h3').get_text() == "Additional information":
#                     add_info_ul = skills_property_div[0].find_all('ul')
#                     for a in add_info_ul:
#                         add_info_li = a.find_all('li')
#                         for b in add_info_li:
#                             additional_information = b.get_text().strip()
#             except IndexError:
#                 credentials = "No credentials"
#                 additional_information = "No additional information"
#
# # Experience requirements
# if comparison_chart.find('div', {'property': 'experienceRequirements'}) is not None:
#     experience_div = comparison_chart.find('div', {'property': 'experienceRequirements'})
#     experience_ul = experience_div.find_all('ul')
#     for exp_li in experience_ul:
#         experience_li = exp_li.find_all('li')
#         for exp in experience_li:
#             experience_and_specialization = exp.get_text().strip()
#
# # Additional information
# # if comparison_chart.find_all('div', {'property': 'skills'}) is not None:
# #     skills_property_div = comparison_chart.find_all('div', {'property': 'skills'})
# #     if skills_property_div[1].find('h3').get_text() == "Additional information":
# #         add_info_ul = skills_property_div[1].find_all('ul')
# #         for a in add_info_ul:
# #             add_info_li = a.find_all('li')
# #             for b in add_info_li:
# #                 additional_information = b.get_text().strip()
# #     else:
# #         additional_information = "No additional information"
#
# # Benefits
# if comparison_chart.find('div', {'property': 'jobBenefits'}):
#     benefits_div = comparison_chart.find('div', {'property': 'jobBenefits'})
#     benefits_ul = benefits_div.find_all('ul')
#     for c in benefits_ul:
#         benefits_li = c.find_all('li')
#         for d in benefits_li:
#             benefits = d.get_text().strip()
# else:
#     benefits = "No job benefits"
#
#
# # ===========================================================================================
#
comparison_chart = soup.find('div', {'class': 'comparisonchart'})
all_main_h4 = comparison_chart.find_all('h4')
all_divs = comparison_chart.find_all('div')
temp = []


# Language
if comparison_chart.find('p', {'property': 'qualification'}) is not None:
    h4 = all_main_h4[0].get_text().strip()
    one_list = comparison_chart.find('p', {'property': 'qualification'}).get_text()
    temp.append(h4)
    temp.append(one_list)
else:
    pass

# Education
education_ul = comparison_chart.find('ul', {'property': 'educationRequirements qualification'})
if education_ul is not None:
    h4 = all_main_h4[1].get_text().strip()
    one_list = education_ul.find('li').get_text().strip()
    temp.append(h4)
    temp.append(one_list)
else:
    pass

# Experience
if comparison_chart.find('p', {'property': 'experienceRequirements qualification'}) is not None:
    h4 = all_main_h4[2].get_text().strip()
    one_list = comparison_chart.find('p', {'property': 'experienceRequirements qualification'}).get_text().strip()
    temp.append(h4)
    temp.append(one_list)
else:
    pass
s = []
if comparison_chart.find('div', {'property': ''}):
    work_div = comparison_chart.find('div', {'property': ''})
    h4_tag = work_div.find_all('h4')
    ul_tag = work_div.find_all('ul')
    for i in h4_tag:
        h4 = i.get_text()
    for j in ul_tag:
        content_li = j.find_all('li')
        for k in content_li:
            content = k.get_text().strip()
else:
    h3 = 'Work setting'
    h4 = '0'
    content = '0'

if comparison_chart.find('div', {'property': 'responsibilities'}):
    responsibilities_div = comparison_chart.find('div', {'property': 'responsibilities'})
    res_h3 = responsibilities_div.find('h3').get_text()
    res_h4_tag = responsibilities_div.find_all('h4')
    res_ul_tag = responsibilities_div.find_all('ul')
    for l in res_h4_tag:
        res_h4 = l.get_text()
    for m in res_ul_tag:
        res_li = m.find_all('li')
        for n in res_li:
            res_content = n.get_text().strip()
else:
    res_h3 = 'Responsibilities'
    res_h4 = '0'
    res_content = '0'

skills_div = comparison_chart.find_all('div', {'property': 'skills'})
if len(skills_div) > 1:
    h3_tag_1 = skills_div[0].find('h3').get_text()
    h3_tag_2 = skills_div[1].find('h3').get_text()
    if h3_tag_1 == 'Credentials' and h3_tag_2 == 'Additional information':
        cred_h4_tag = skills_div[0].find_all('h4')
        cred_ul_tag = skills_div[0].find_all('ul')
        addi_h4_tag = skills_div[1].find_all('h4')
        addi_ul_tag = skills_div[1].find_all('ul')
        for p in cred_h4_tag:
            cred_h4 = p.get_text()
        for q in cred_ul_tag:
            cred_li = q.find_all('li')
            for r in cred_li:
                cred_content = r.get_text()
        for s in addi_h4_tag:
            addi_h4 = s.get_text()
        for t in addi_ul_tag:
            addi_li = t.find_all('li')
            for v in addi_li:
                addi_content = v.get_text()

else:
    h3_tag = skills_div.find('h3').get_text()
    if h3_tag == 'Credentials':
        cred_h4_tag = skills_div[0].finda_all('h4')
        cred_ul_tag = skills_div[0].find_all('ul')
        for p in cred_h4_tag:
            cred_h4 = p.get_text()
        for q in cred_ul_tag:
            cred_li = q.find_all('li')
            for r in cred_li:
                cred_content = r.get_text()

    elif h3_tag == 'Additional information':
        addi_h4_tag = skills_div[0].finda_all('h4')
        addi_ul_tag = skills_div[0].find_all('ul')
        for s in addi_h4_tag:
            addi_h4 = s.get_text()
        for t in addi_ul_tag:
            addi_li = t.find_all('li')
            for v in addi_li:
                addi_content = v.get_text()
    else:
        cred_h4 = '0'
        cred_content = '0'
        addi_h4 = '0'
        addi_content = '0'

if comparison_chart.find('div', {'property': 'experienceRequirements'}):
    experience_specialization_div = comparison_chart.find('div', {'property': 'experienceRequirements'})
    exp_h3 = experience_specialization_div.find('h3').get_text()
    exp_h4_tag = experience_specialization_div.find_all('h4')
    exp_ul_tag = experience_specialization_div.find_all('ul')
    for a in exp_h4_tag:
        exp_h4 = a.get_text()
    for b in exp_ul_tag:
        exp_li = b.find_all('li')
        for c in exp_li:
            exp_content = c.get_text().strip()
else:
    exp_h3 = 'experience and specialization'
    exp_h4 = '0'
    exp_content = '0'

if comparison_chart.find('div', {'property': 'jobBenefits'}):
    benefits_div = comparison_chart.find('div', {'property': 'jobBenefits'})
    benefits_h3 = benefits_div.find('h3').get_text()
    benefits_h4_tag = benefits_div.find_all('h4')
    benefits_ul_tag = benefits_div.find_all('ul')
    for d in benefits_h4_tag:
        benefits_h4 = d.get_text().strip()
    for e in benefits_ul_tag:
        benefits_li = e.find_all('li')
        for f in benefits_li:
            benefits_content = f.get_text().strip()
else:
    benefits_h3 = 'Benefits'
    benefits_h4 = '0'
    benefits_content = '0'



for m in all_divs:
    details = []
    all_h3_tag = m.find_all('h3')
    for h in all_h3_tag:
        h3 = h.get_text().strip()
        temp.append(h3)
    all_h4_tag = m.find_all('h4')
    for k in all_h4_tag:
        h4 = k.get_text().strip()
        temp.append(h4)
    all_ul_tag = m.find_all('ul')
    for li_s in all_ul_tag:
        all_list = li_s.find_all('li')
        for jj in all_list:
            one_list = jj.get_text().strip()
            temp.append(one_list)

    # temp.append(details)


