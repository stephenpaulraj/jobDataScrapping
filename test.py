from bs4 import BeautifulSoup
import requests
import json
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger


def job_additional_information():
    url = 'https://www.jobbank.gc.ca//jobsearch/jobposting/37788517;jsessionid=E2DDA58242EC9C9C7F8E098871B25FAC.jobsearch77?source=searchresults'

    url_reponse = requests.get(url)

    soup = BeautifulSoup(url_reponse.content, 'html.parser')

    comparison_chart = soup.find('div', {'class': 'comparisonchart'})





    print(comparison_chart)



job_additional_information()


