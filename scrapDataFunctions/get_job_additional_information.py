from scrapDataFunctions import hasura_calls
import asyncio

def collect_job_additional_info(soup, j_id):
    addi_details = []
    comparison_chart = soup.find('div', {'class': 'comparisonchart'})
    all_divs = comparison_chart.find_all('div', {'property': True})
    all_main_h4 = comparison_chart.find_all('h4')

    # Overview - Collect info
    if len(all_main_h4) > 0:
        overview_h4 = comparison_chart.find_all('h4')[:3]
        ss = []
        for j in overview_h4:
            temp = []
            sub_topic = j.get_text()
            overview_content = j.find_next().get_text().strip()
            temp.append('Overview')
            temp.append(sub_topic)
            temp.append(overview_content)
            addi_details.append(temp)

    # other additional details like responsibilities

    if len(all_divs) > 0:
        all_divs.pop(0)
        dum = []

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
                    # hasura call -- > addi_detail

        for a in addi_details:
            asyncio.run(hasura_calls.insert_job_additional_info(j_id, a))

    return addi_details
