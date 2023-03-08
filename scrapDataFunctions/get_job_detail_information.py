def collect_job_detail_info(soup):
    job_temp = []
    main_div = soup.find('div', {'typeof': 'JobPosting'})
    job_posting_ul = main_div.find('ul', {'class': 'job-posting-brief'})
    job_posting_li = job_posting_ul.find_all('li')
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

    return job_temp
