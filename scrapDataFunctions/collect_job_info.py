import re
from datetime import datetime as dsf

import requests
from bs4 import BeautifulSoup
import json
from scrapDataFunctions import utils
from scrapDataFunctions import get_employer
from scrapDataFunctions import get_job_basic_information
from scrapDataFunctions import get_job_detail_information
from scrapDataFunctions import get_job_additional_information


def collect_company_info(url_data):
    final_data = []
    employer_temp = []
    job_temp = []
    addi_details = []
    count = 0
    link = url_data
    for index, li in enumerate(link):
        print('-- Data Collecting ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')
        page = requests.get(li)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            emp_data = get_employer.scrap_employer_data(soup, li)
            print(emp_data)
        except:
            print('Error on Getting Employer data')

        print('---- Employer Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Basic Information                                    #
        # ================================================================= #
        try:
            job_basic_data = get_job_basic_information.collect_job_basic_information(soup)
            print(job_basic_data)
        except:
            print('Some error on Getting Job Basic Data')

        print('---- Job Basic Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Details                                              #
        # ================================================================= #
        try:
            job_detail_data = get_job_detail_information.collect_job_detail_info(soup)
            print(job_detail_data)
        except:
            print('Some error on Getting Job Basic Data')

        print('---- Job Detail Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Additional Information                               #
        # ================================================================= #
        try:
            job_additional_data = get_job_additional_information.collect_job_additional_info(soup)
            print(job_additional_data)
        except:
            print('Some error on Getting Job Basic Data')

        print('---- Job Detail Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')



    final_data.append(job_temp)
    final_data.append(employer_temp)
    final_data.append(addi_details)
    print('-- All Data collected Successfully')
    return final_data
