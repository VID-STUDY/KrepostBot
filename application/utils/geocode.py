from math import radians, cos, sin, asin, sqrt
from yandex_geocoder import Client
from typing import Optional, AnyStr
import requests
import settings

def distance_between_two_points(first_coordinates: tuple, second_coordinates: tuple) -> tuple:
    """
    Calculate the great circle distance between two pints
    on the Earth (specified in decimal degrees)
    :param first_coordinates: Coordinates (latitude, longitude) of first point
    :param second_coordinates: Coordinates (latitude, longitude) of second point
    :return: distance
    """
    firstLat = first_coordinates[0]
    firstLong = first_coordinates[1]
    secondLat = second_coordinates[0]
    secondLong = second_coordinates[1]
    longWay = requests.get('https://api.routing.yandex.net/v2/route?waypoints=55.734494627139355,37.68191922355621|55.733441295701056,37.59027350593535&apikey=424e9981-9ff1-44c3-ba6e-60c7669b25f3')
    print(longWay)
    lat1, lon1 = first_coordinates
    lat2, lon2 = second_coordinates
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversina formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of Earth in kilometers is 6731
    km = 6371 * c
    # If distance in kilometres, round the value
    if km >= 1:
        return round(km, 1), 'км'
    else:
        # If distance is smaller than 1, return metres value
        metres = km * 1000
        return round(metres), 'м'


def get_address_by_coordinates(coordinates: tuple) -> Optional[AnyStr]:
    """
    Return address string value by coordinates
    :param coordinates: Coordinates (latitude, longitude)
    :return: string value
    """
    client = Client('4d16304f-12ba-4134-ac9b-f0da5028a1f4')
    latitude = coordinates[0]
    longitude = coordinates[1]
    location = client.address(longitude, latitude)
    return location

