import re
from datetime import datetime as dsf


def collect_job_basic_information(soup):
    job_temp = []
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

    return job_temp
