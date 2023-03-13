import requests
from bs4 import BeautifulSoup
from colorama import Fore

from scrapDataFunctions import get_employer, get_job_detail_information


def collect_company_info(url_data):
    final_data = []
    employer_temp = []
    job_temp = []
    addi_details = []
    link = url_data
    for index, li in enumerate(link):
        print(Fore.GREEN + '-- Data Collecting ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')
        page = requests.get(li)
        soup = BeautifulSoup(page.content, 'html.parser')

        # ================================================================= #
        #          Employer  Information                                    #
        # ================================================================= #

        emp_data = get_employer.scrap_employer_data(soup, li)

        print(Fore.GREEN + '---- Employer Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Basic Information                                    #
        # ================================================================= #
        # try:
        #     job_basic_data = get_job_basic_information.collect_job_basic_information(soup)
        # except:
        #     print(Fore.RED + 'Some error on Getting Job Basic Data')
        #
        # print(Fore.GREEN + '---- Job Basic Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Details                                              #
        # ================================================================= #
        # try:
        #     job_detail_data = get_job_detail_information.collect_job_detail_info(soup)
        # except:
        #     print(Fore.RED + 'Some error on Getting Job Basic Data')
        #
        # print(Fore.GREEN + '---- Job Detail Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

        # ================================================================= #
        #          Job Additional Information                               #
        # ================================================================= #
        # try:
        #     job_additional_data = get_job_additional_information.collect_job_additional_info(soup)
        # except:
        #     print(Fore.RED + 'Some error on Getting Job Basic Data')
        #
        # print(Fore.GREEN + '---- Job Detail Data Collected for ' + str(index + 1) + ' / ' + str(len(link)) + ' URL')

    final_data.append(job_temp)
    final_data.append(employer_temp)
    final_data.append(addi_details)
    print(Fore.GREEN + '-- All Data collected Successfully')
    return final_data
