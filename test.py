from bs4 import BeautifulSoup
import requests
import json
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger


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




async def job_additional_information(soup_1, j_id):
    print('true')
    soup = soup_1


    # finding main div for job info
    main_div = soup.find('div', {'typeof': 'JobPosting'})

    comparison_chart = soup.find('div', {'class': 'comparisonchart'})
    all_main_h4 = comparison_chart.find_all('h4')
    all_divs = comparison_chart.find_all('div', {'property': True})
    all_divs.pop(0)
    print(all_divs)


    for m in all_divs:
        details = []
        all_h3_tag = m.find('h3').get_text()
        all_h4_tag = m.find_all('h4')
        h4_array = []
        for k in all_h4_tag:
            h4 = k.get_text().strip() # All sub topic
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

    addi(j_id)

def addi(j_id):
    for c in addi_details:
        asyncio.run(insert_job_additional_info(j_id, c[0], c[1], c[2]))
