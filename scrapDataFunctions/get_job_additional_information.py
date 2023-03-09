def collect_job_additional_info(soup):
    addi_details = []
    comparison_chart = soup.find('div', {'class': 'comparisonchart'})
    all_divs = comparison_chart.find_all('div', {'property': True})
    all_main_h4 = comparison_chart.find_all('h4')
    all_divs.pop(0)
    dum = []

    # Overview - Collect info

    # Language
    if comparison_chart.find('p', {'property': 'qualification'}) is not None:
        h4 = all_main_h4[0].get_text().strip()
        one_list = comparison_chart.find('p', {'property': 'qualification'}).get_text()
        dum.append(h4)
        dum.append(one_list)
    else:
        pass

    # Education
    education_ul = comparison_chart.find('ul', {'property': 'educationRequirements qualification'})
    if education_ul is not None:
        h4 = all_main_h4[1].get_text().strip()
        one_list = education_ul.find('li').get_text().strip()
        dum.append(h4)
        dum.append(one_list)
    else:
        pass

    # Experience
    if comparison_chart.find('p', {'property': 'experienceRequirements qualification'}) is not None:
        h4 = all_main_h4[2].get_text().strip()
        one_list = comparison_chart.find('p', {'property': 'experienceRequirements qualification'}).get_text().strip()
        dum.append(h4)
        dum.append(one_list)
    else:
        pass



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
    return addi_details
