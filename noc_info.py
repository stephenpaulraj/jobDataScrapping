from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests



page = requests.get("https://www.jobbank.gc.ca/jobsearch/jobposting/37607604?source=searchresults")
soup = BeautifulSoup(page.content, 'html.parser')

# finding main div for job info
main_div = soup.find('div', {'typeof': 'JobPosting'})

# extracting basic job info
basic_info_ul = main_div.find('ul', {'class': 'job-posting-brief'})
li_of_basic_info = basic_info_ul.find_all('li')
dd = (len(li_of_basic_info))
for l in li_of_basic_info:
    s = l.find_all('span')
    # if s[0] == '<span aria-hidden="true" class="fas fa-map-marker-alt"></span>':
    #     print('true')
    print(s[0])




    # if info[0] == '<span aria-hidden="true" class="fas fa-map-marker-alt"></span>':
    #     print('true')

# extracting overview info
comparison_chart = soup.find('div', {'class': 'comparisonchart'})

# Language
if comparison_chart.find('p', {'property': 'qualification'}) is not None:
    language = comparison_chart.find('p', {'property': 'qualification'}).get_text()

#
if comparison_chart.find('ul', {'property': 'educationRequirements'}) is not None:
    language = comparison_chart.find('p', {'property': 'qualification'}).get_text()
    print(language)

