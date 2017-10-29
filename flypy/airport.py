"""
Get information about airport

"""

import requests
USERNAME = "zuikng"
FA_KEY = "0cefa5ddec603e493bbee6ad558ff3df29be7b19"
FA_ENDPOINT = "https://flightxml.flightaware.com/json/FlightXML3/"


def airport_info(airport_code):
    """
    Get information about the airport from their three-letter code

    :param str airport_code: Three letter ICAO code
    :return:
    """

    r = requests.get("{}AirportBoards".format(FA_ENDPOINT), auth=(USERNAME,FA_KEY), params={
        "airport_code":airport_code,
        "type":"departures",
        "howMany": 100
    })

    return r

def get_flight_sched(airport_code, start, end):
    """

    :param airport_code:
    :param start:
    :param end:
    :return:
    """

    start = 1510416000

    r = requests.get("{}AirlineFlightSchedules".format(FA_ENDPOINT), auth=(USERNAME, FA_KEY), params={
        "origin": airport_code,
        "howMany": 100,
        "start_date": start,
        "end_date": start + 3600
    })

    return r