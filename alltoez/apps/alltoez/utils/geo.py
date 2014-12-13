from django.conf import settings
from math import *

import urllib, json

def calc_bounding_box(lat, lon, radius, use_miles = True):
    """ retval -> lat_min, lat_max, lon_min, lon_max
        Calculates the max and min lat and lon for an area.
        It approximates a search area of radius r by using a box
        For further details:
        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates (section 3.3)
        For testing output
        http://www.getlatlon.com/
    """

    # d = distance
    # R = Radius of sphere (6378.1 km or 3,963.1676 miles)
    # r = d/R angular radius of query circle

    R_MILES = 3963.1676
    R_KM    = 6378.1

    lat = float(radians(lat))
    lon = float(radians(lon))
    radius = float(radius)

    R = use_miles and R_MILES or R_KM

    r = radius / R

    lat_T = asin( sin(lat) / cos(r) )
    delta_lon = asin( sin(r) / cos(lat) )

    lon_min = degrees(lon - delta_lon)
    lon_max = degrees(lon + delta_lon)

    lat_min = degrees(lat - r)
    lat_max = degrees(lat + r)

    return lat_min, lat_max, lon_min, lon_max

def geocode_location(location, full=False):
    key = settings.GOOGLE_MAPS_API_KEY
    location = urllib.quote_plus(location)
    request = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (location)

    data = urllib.urlopen(request).read()
    dlist = json.loads(data)
    if dlist['status'] == "OK":
        if full:
            result = {
                'lng': float(dlist['results'][0]['geometry']['location']['lng']),
                'lat': float(dlist['results'][0]['geometry']['location']['lat']),
                'region': _get_location_address_parameter(dlist, ['administrative_area_level_1', 'administrative_area_level_2']),
                'country': _get_location_address_parameter(dlist, ['country']),
                'city': _get_location_address_parameter(dlist, ['postal_town']),
            }
            return result
        else:
            lng = float(dlist['results'][0]['geometry']['location']['lng'])
            lat = float(dlist['results'][0]['geometry']['location']['lat'])
            return (lat, lng)
    else:
        if full:
            return {}
        return (0, 0)

def _get_location_address_parameter(dlist, types):
    address_components = dlist['results'][0]['address_components']
    for component in address_components:
        for t in types:
            if t in component['types']:
                return component['long_name']
    return None