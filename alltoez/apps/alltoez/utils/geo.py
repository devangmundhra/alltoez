import math
import urllib, json

from django.conf import settings


def calc_bounding_box(lat, lon, radius, use_miles=True):
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

    lat = float(math.radians(lat))
    lon = float(math.radians(lon))
    radius = float(radius)

    R = use_miles and R_MILES or R_KM

    r = radius / R

    lat_T = math.asin( math.sin(lat) / math.cos(r) )
    delta_lon = math.asin( math.sin(r) / math.cos(lat) )

    lon_min = math.degrees(lon - delta_lon)
    lon_max = math.degrees(lon + delta_lon)

    lat_min = math.degrees(lat - r)
    lat_max = math.degrees(lat + r)

    return lat_min, lat_max, lon_min, lon_max


def rev_geocode_location_component(lat, lng, result_type=""):
    google_maps_api_key = getattr(settings, 'GOOGLE_MAPS_V3_APIKEY', None)
    qt_latlng = urllib.quote_plus("{},{}".format(lat, lng))
    geo = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}&result_type={2}".
                         format(qt_latlng,
                         google_maps_api_key, result_type))
    res = json.loads(geo.read())
    if res['status'] != 'OK':
        return ""
    # Example https://maps.googleapis.com/maps/api/geocodhttps://maps.googleapis.com/maps/api/geocode/json?latlng=37.7628848%2C-122.428514&key=AIzaSyDOtkrcR4QFGYTMdR71WkkUYsMQ735c_EU&result_type=neighborhood
    try:
        address = res['results'][0]['address_components'][0]['short_name']
        import pdb

        if result_type == 'political' and not address:
            pdb.set_trace()
        return address
    except ValueError:
        return ""


def geocode_location(location, full=False):
    key = getattr(settings, 'GOOGLE_MAPS_V3_APIKEY', None)
    location = urllib.quote_plus(location)
    if key:
        request = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&key=%s" % (location, key)
    else:
        request = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (location)

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