import requests
from bs4 import BeautifulSoup
import datetime

URLS = [
'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest',
'https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest',
'https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest',
'https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest',
]
'''
Half Moon Bay, California
Huntington Beach, California
Providence, Rhode Island
Wrightsville Beach, North Carolina
'''

class Tides():
    
    def __init__(self):
        pass

def get_daylight_low_tides(URLS):
    for url in URLS:
        page = download_page(url)
        data = parse_page(page)

def download_page(url):
    res = requests.get(url)
    if res.ok:
        return res.content
    else:
        raise 

def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    # find table class = 'tide-day-tides' in div class = tide-header-today
    today_table = soup.find('div',{'class':'tide-header-today'}).find('table')
    # get all rows with 1st td = 'Low Tide'
    low_tide_data = []
    for row in today_table.findChildren('tr'):
        tds = row.findAll('td')
        if tds and tds[0].text == 'Low Tide':
            low_tide_data.append((tds[1].text, tds[2].text))
    # get sunrise/sunset times
    summary_p = soup.find('p', {'class':'tide-header-summary'}).text
    match = re.search(r'.*Sunrise is at\s*(1[0-2]|0?[1-9]:[0-5][0-9][ap][m]) and sunset is at\s*(1[0-2]|0?[1-9]:[0-5][0-9][ap][m]*)', summary_p)
    sunrise = match.group(1)
    sunset = match.group(2)

def get_


if __name__ == '__main__':
    print('hi')