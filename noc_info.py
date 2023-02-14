from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.jobbank.gc.ca/jobsearch/jobposting/37626475?source=searchresults")
soup = BeautifulSoup(page.content, 'html.parser')

# finding main div for job info
main_div = soup.find('div', {'typeof': 'JobPosting'})

# job position name
job_name_h1 = main_div.find('h1')
job_name = job_name_h1.find('span', {'property': 'title'}).get_text()

# Date of job posted
date_p_tag = main_div.find('p', {'class': 'date-business'})
date_span = date_p_tag.find('span', {'class': 'date'}).get_text()
date_trim = date_span.split('Posted on')
date = date_trim[1].strip()

# Job posting summary
job_posting_ul = main_div.find('ul', {'class': 'job-posting-brief'})
job_posting_li = job_posting_ul.find_all('li')

# Job location
job_location_split = job_posting_li[0].get_text().split('Location')
job_location = job_location_split[1].strip()

# Base salary
base_salary_span = job_posting_li[1].find('span', {'property': 'baseSalary'}).get_text().split('HOUR')
base_salary = base_salary_span[0] + '' + base_salary_span[1]

# working hours
work_hours_span = job_posting_li[1].find('span', {'property': 'workHours'}).get_text().split('for')
work_hours = work_hours_span[1].strip()

# Terms of employment
term_of_employment_span = job_posting_li[2].find_all('span')
if term_of_employment_span[1].get_text() == 'Terms of employment':
    term_of_employment = term_of_employment_span[2].find('span').get_text()
else:
    term_of_employment = "Not available"

# Special commitments
special_commitments_span = job_posting_li[3].find_all('span')
if special_commitments_span[1].get('property') == "specialCommitments":
    special_commitments = special_commitments_span[1].get_text().strip()
else:
    special_commitments = "Not available"

# Start date
start_date_span_1 = job_posting_li[4].find('span', {'class': 'fa-calendar'})
start_date_span_2 = job_posting_li[3].find('span', {'class': 'fa-calendar'})
if start_date_span_1 is not None:
    start_date = job_posting_li[4].get_text().strip()
elif start_date_span_2 is not None:
    start_date_span = job_posting_li[3].find_all('span')
    start_date = start_date_span[2].get_text().strip()
else:
    start_date = "Not available"

# Job benefits
job_benefit_span_1 = job_posting_li[5].find('span', {'class': 'fa-gift'})
job_benefit_span_2 = job_posting_li[4].find('span', {'class': 'fa-gift'})
if job_benefit_span_1 is not None:
    job_benefits_split = job_posting_li[5].get_text().split('Benefits:')
    job_benefits = job_benefits_split[1].strip()
elif job_benefit_span_2 is not None:
    job_benefits_split = job_posting_li[4].get_text().split('Benefits:')
    job_benefits = job_benefits_split[1].strip()
else:
    job_benefits = "Not available"

# Vacancies
vacancies_span_1 = job_posting_li[6].find('span', {'class': 'fa-user'})
vacancies_span_2 = job_posting_li[5].find('span', {'class': 'fa-user'})
vacancies_span_3 = job_posting_li[4].find('span', {'class': 'fa-user'})
if vacancies_span_1 is not None:
    vacancy_span = job_posting_li[6].find_all('span')
    vacancy = vacancy_span[2].get_text().strip()
elif vacancies_span_2 is not None:
    vacancy_span = job_posting_li[5].find_all('span')
    vacancy = vacancy_span[2].get_text().strip()
elif vacancies_span_3 is not None:
    vacancy_span = job_posting_li[4].find_all('span')
    vacancy = vacancy_span[2].get_text().strip()
else:
    vacancy = "Not available"

# Job type
if job_posting_li[7].find('span', {'class': 'fa-university'}) or job_posting_li[6].find('span', {'class': 'fa-university'}) or job_posting_li[5].find('span', {'class': 'fa-university'}):
    job_type_span_1 = job_posting_li[7].find('span', {'class': 'fa-university'})
    job_type_span_2 = job_posting_li[6].find('span', {'class': 'fa-university'})
    job_type_span_3 = job_posting_li[5].find('span', {'class': 'fa-university'})
    if job_type_span_1 is not None:
        job_type = job_posting_li[7].get_text().strip()
    elif job_type_span_2 is not None:
        job_type = job_posting_li[6].get_text().strip()
    elif job_type_span_3 is not None:
        job_type = job_posting_li[5].get_text().strip()
    else:
        job_type = "Not available"



# extracting overview info
comparison_chart = soup.find('div', {'class': 'comparisonchart'})

# Language
if comparison_chart.find('p', {'property': 'qualification'}) is not None:
    language = comparison_chart.find('p', {'property': 'qualification'}).get_text()

# Education
education_ul = comparison_chart.find('ul', {'property': 'educationRequirements qualification'})
if education_ul is not None:
    education = education_ul.find('li').get_text().strip()

# Experience
if comparison_chart.find('p', {'property': 'experienceRequirements qualification'}) is not None:
    experience = comparison_chart.find('p', {'property': 'experienceRequirements qualification'}).get_text().strip()

# work site environment & work setting
work_setting_div = comparison_chart.find('div', {'property': ''})
if work_setting_div is not None:
    work_setting_env_h4 = work_setting_div.find_all('h4')
    if work_setting_env_h4[0].get_text() == "Work site environment":
        work_setting_ul = work_setting_div.find_all('ul', {'class': 'csvlist'})

        # work site environment
        work_site_li = work_setting_ul[0].find_all('li')
        for site in work_site_li:
            work_site_environment = site.get_text().strip()

        # work setting
        work_setting_li = work_setting_ul[1].find_all('li')
        for setting in work_setting_li:
            work_setting = setting.get_text().strip()

    elif work_setting_env_h4[0].get_text() == "Work setting":
        work_setting_ul = work_setting_div.find_all('ul', {'class': 'csvlist'})
        work_setting_li = work_setting_ul[0].find_all('li')
        for site in work_setting_li:
            work_setting = site.get_text().strip()

    else:
        work_site_environment = "No work site environment"
        work_setting = "No work setting"

# Responsibilities
if comparison_chart.find('div', {'property': 'responsibilities'}) is not None:
    responsibilities_div = comparison_chart.find('div', {'property': 'responsibilities'})
    responsibilities_h4 = responsibilities_div.find_all('h4')
    responsibilities_ul = responsibilities_div.find_all('ul')
    for res_li in responsibilities_ul:
        responisibilities_li = res_li.find_all('li')
        for r in responisibilities_li:
            responsibilities = r.get_text().strip()
else:
    responsibilities = "No responsibilities"

    # # responsibilities - tasks
    # if responsibilities_h4[0].get_text() == "Tasks":
    #     tasks_li = responsibilities_ul[0].find_all('li')
    #     for task in tasks_li:
    #         tasks = task.get_text().strip()
    # else:
    #     tasks = "No tasks"
    #
    # # responsibilities - supervision
    # if len(responsibilities_h4) > 1:
    #     if responsibilities_h4[1].get_text() == "Supervision":
    #         supervision_li = responsibilities_ul[1].find_all('li')
    #         for supervise in supervision_li:
    #             supervision = supervise.get_text().strip()
    # else:
    #     supervision = "No supervision"

# Credentials
skills_property_div = comparison_chart.find_all('div', {'property': 'skills'})
if len(skills_property_div) == 0:
    print("false")

else:
    if comparison_chart.find_all('div', {'property': 'skills'}) is not None:
        credentials_h4 = skills_property_div[0].find_all('h4')
        credentials_ul = skills_property_div[0].find_all('ul')
        if len(skills_property_div) > 1:
            if credentials_h4[0].get_text() == "Certificates, licences, memberships, and courses " and \
                    skills_property_div[1].find('h3').get_text() == "Additional information":
                credentials_li = credentials_ul[0].find_all('li')
                for certificate in credentials_li:
                    credentials = certificate.get_text().strip()
                add_info_ul = skills_property_div[1].find_all('ul')
                for a in add_info_ul:
                    add_info_li = a.find_all('li')
                    for b in add_info_li:
                        additional_information = b.get_text().strip()
            else:
                credentials = "No credentials"
                additional_information = "No additional information"
        elif len(skills_property_div) <= 1:
            if credentials_h4[0].get_text() == "Certificates, licences, memberships, and courses ":
                credentials_li = credentials_ul[0].find_all('li')
                for certificate in credentials_li:
                    credentials = certificate.get_text().strip()
            else:
                credentials = "No credentials"
            if skills_property_div[0].find('h3').get_text() == "Additional information":
                add_info_ul = skills_property_div[0].find_all('ul')
                for a in add_info_ul:
                    add_info_li = a.find_all('li')
                    for b in add_info_li:
                        additional_information = b.get_text().strip()
            else:
                additional_information = "No additional information"
        else:
            credentials = "No credentials"
            additional_information = "No additional information"

# Experience requirements
if comparison_chart.find('div', {'property': 'experienceRequirements'}) is not None:
    experience_div = comparison_chart.find('div', {'property': 'experienceRequirements'})
    experience_ul = experience_div.find_all('ul')
    for exp_li in experience_ul:
        experience_li = exp_li.find_all('li')
        for exp in experience_li:
            experience_and_specialization = exp.get_text().strip()

# Additional information
# if comparison_chart.find_all('div', {'property': 'skills'}) is not None:
#     skills_property_div = comparison_chart.find_all('div', {'property': 'skills'})
#     if skills_property_div[1].find('h3').get_text() == "Additional information":
#         add_info_ul = skills_property_div[1].find_all('ul')
#         for a in add_info_ul:
#             add_info_li = a.find_all('li')
#             for b in add_info_li:
#                 additional_information = b.get_text().strip()
#     else:
#         additional_information = "No additional information"

# Benefits
if comparison_chart.find('div', {'property': 'jobBenefits'}):
    benefits_div = comparison_chart.find('div', {'property': 'jobBenefits'})
    benefits_ul = benefits_div.find_all('ul')
    for c in benefits_ul:
        benefits_li = c.find_all('li')
        for d in benefits_li:
            benefits = d.get_text().strip()
else:
    benefits = "No job benefits"