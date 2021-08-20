import requests
from bs4 import BeautifulSoup
import re
import time

class TidesError(Exception):
    pass

class DownloadError(TidesError):
    pass

class TideTimeParseError(TidesError):
    pass

class Tides():
    
    def __init__(self):
        pass

    def get_daylight_low_tides(self, url):
        '''
        get low tide info for list of urls 
        '''
        out = []
        page = self.download_page(url)
        tide_data,sunrise,sunset = self.parse_page(page)
        for tide_timestamp,data in tide_data:
            if sunrise < tide_timestamp and tide_timestamp < sunset:
                out.append(data)
            else:
                print('Data point was not a during sun up hours.')
        return out

    def download_page(self, url):
        '''
        download page
        '''
        res = requests.get(url)
        if res.ok:
            return res.content
        else:
            raise DownloadError(f"Unable to get {url}")

    def parse_page(self, page):
        '''
        parse page for tides and sunset times
        '''
        soup = BeautifulSoup(page, 'html.parser')
        tides = self.parse_tides_data(soup)
        sunrise,sunset = self.parse_sun_times(soup)
        return (tides, sunrise, sunset)

    def parse_tides_data(self, soup):
        '''
        getting tides datapoints
        '''
        # find table in div class = tide-header-today
        today_table = soup.find('div',{'class':'tide-header-today'}).find('table')
        # get all rows with 1st td = 'Low Tide'
        low_tide_data = []
        for row in today_table.findChildren('tr'):
            tds = row.findAll('td')
            if tds and tds[0].text == 'Low Tide':
                #TODO: issues parsing 00:XXam. need to look rework this
                try:
                    tide_str = tds[1].text.split('(')[0].strip()
                    time_obj = time.strptime(tide_str,"%I:%M %p")
                except ValueError as e:
                    raise TideTimeParseError(f"unable to parse time: {tide_str}")
                low_tide_data.append((time_obj, (tds[1].text, tds[2].text)))
        return low_tide_data

    def parse_sun_times(self, soup):
        '''
        getting sunrise/sunset times
        '''
        summary_p = soup.find('p', {'class':'tide-header-summary'}).text
        match = re.search(r'.*Sunrise is at\s*(1[0-2]|0?[1-9]:[0-5][0-9][ap][m]) and sunset is at\s*(1[0-2]|0?[1-9]:[0-5][0-9][ap][m]*)', summary_p)
        sunrise = match.group(1)
        sunset = match.group(2)
        sunrise = time.strptime(sunrise,"%I:%M%p")
        sunset = time.strptime(sunset,"%I:%M%p")
        return sunrise,sunset

if __name__ == '__main__':
    urls = [
        (
            'Half Moon Bay, California',
            'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest'),
        (
            'Huntington Beach, California',
            'https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest'),
        (
            'Providence, Rhode Island', 
            'https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest'),
        (
            'Wrightsville Beach, North Carolina', 
            'https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest')
        ]
    
    tides = Tides()
    for location, url in urls:
        print(location)
        try:
            out = tides.get_daylight_low_tides(url)
        except TideTimeParseError as e:
            print(f"skipping: {e}")
            continue
        print(out)