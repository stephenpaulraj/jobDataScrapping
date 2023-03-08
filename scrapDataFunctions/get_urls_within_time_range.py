import datetime

import pytz
import requests
from bs4 import BeautifulSoup


def canada_timezone():
    # Set the timezone to Eastern Time (Canada)
    canada_tz = pytz.timezone('America/Toronto')
    return canada_tz


def check_current_date(d):
    # Get the current local time
    current_time = datetime.datetime.now(canada_timezone())
    current_date = current_time.strftime("%d")
    c = int(current_date) - int(d)
    return c


def scrap_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Finding main all links div

    finding_main_div = soup.find('div', {'class': 'results-jobs'})
    links_article = finding_main_div.find_all('article')
    for url in links_article:
        links = url.find('a')
        if links is not None:
            href = links.get('href')
            full_url = "https://www.jobbank.gc.ca/" + href

    length = len(links_article)
    last = links_article[24]
    finding_date_sec = last.find('ul', {'class': 'list-unstyled'})
    finding_date_li = finding_date_sec.find('li', {'class': 'date'}).get_text()
    date = finding_date_li.split(',')
    remove_month = date[0].split(' ')
    last_element_month = remove_month[1].strip()
    return last_element_month


def collect_urls_list(d):
    default_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?page=1&sort=D&fsrc=16"
    count = 1
    urls_to_scrape = [default_url]
    while count < 1000:
        if scrap_data(default_url) == check_current_date(d):
            count += 1
            default_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?page=" + str(count) + "&sort=D&fsrc=16"
            urls_to_scrape.append(default_url)
        else:
            break

    return urls_to_scrape


def collect_main_urls_list(d):
    main_urls_to_collect_company_name = []
    url_lists = collect_urls_list(d)
    for url in url_lists:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Finding main all links div

        finding_main_div = soup.find('div', {'class': 'results-jobs'})
        links_article = finding_main_div.find_all('article')
        for url in links_article:
            temp = []
            links = url.find('a')
            if links is not None:
                href = links.get('href')
                full_url = "https://www.jobbank.gc.ca/" + href
                main_urls_to_collect_company_name.append(full_url)

    return main_urls_to_collect_company_name
