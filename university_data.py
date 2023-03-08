from bs4 import BeautifulSoup
import requests

university_url = []
page = requests.get("https://www.kanan.co/study-in-canada/universities/")
soup = BeautifulSoup(page.content, 'html.parser')

univ_table = soup.find('table', {'class': 'table-auto'})
univ_tbody = univ_table.find('tbody')
univ_tr = univ_tbody.find_all('tr')
for a in univ_tr:
    univ_td = a.find_all('td')
    univ_a_tag = univ_td[1].find('a')
    if univ_a_tag is not None:
        href = univ_a_tag.get('href')
        finalUrl = 'https://www.kanan.co/' + href
        university_url.append(finalUrl)

print(len(university_url))