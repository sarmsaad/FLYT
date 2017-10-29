"""
Barbarian way to get data about flights

"""
from bs4 import BeautifulSoup
import requests

import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
                  '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

dictConfig(logging_config)

l = logging.getLogger()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36",
}


def parse_sched(page):
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find("table", class_="prettyTable").find_all("tr")
    flights = list(table)
    items = [[cell.get_text().strip() for cell in r.find_all("td")] for r in flights]
    return items[2:]


def iter_sched(airport_code, page_limit=10):
    items = []
    for i in range(page_limit):
        l.debug("Requesting %s page %s", airport_code, i)
        page = page_req(airport_code, i * 20)
        items += parse_sched(page)
    return items


def page_req(airport_code, offset=0):
    r = requests.get(
        "https://flightaware.com/live/airport/K{}/scheduled?;offset={};order=filed_departuretime;sort=ASC".format(
            airport_code, offset), headers=HEADERS)
    if r.status_code == 200:
        return r.text
    else:
        raise Exception("Request failed")


def parse_time(time_str):
    """
    Parse the time string from the time table
    """
    hour = time_str[4:6]
    minute = time_str[7:9]
    part = time_str[9:11]

    if part == "PM":
        hour = int(hour) + 12
    return int(hour), int(minute)


def get_flights(airport, start_time):
    """
    Get the number of flights within the time period

    :param str airport: Three-letter airport code
    :param datetime.datetime start_time: Start time
    :param datetime.datetime end_time: End time
    :return: number of flight of each airline
    :rtype: dict
    """

    scheds = iter_sched(airport, page_limit=2)
    r = []
    for s in scheds:
        hour, minute = parse_time(s[3])
        if hour == start_time.hour or (minute < start_time.minute and hour <= start_time.hour):
            r.append(s)
        elif hour == start_time.hour + 1 and minute > start_time.minute:
            break
    return r


def count_airline(flights):
    aircode = [x[0][:3] for x in flights]
    return {e: aircode.count(e) for e in set(aircode)}


if __name__ == '__main__':
    pass
