from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis.measure import D


class EventSearchServices(object):
    zoom = 0
    bounds = None
    latitude = None
    longitude = None

    def __init__(self, zoom=8, bounds=None, circle=None):
        self.zoom = zoom
        self.bounds = self._bounds(bounds)
        self.circle_center, self.radius_mi = self._circle(circle)
        self.latitude = self._latitude()
        self.longitude = self._longitude()
        self.radius_mi = self.radius_mi if self.radius_mi else 0

    def _longitude(self):
        if self.circle_center:
            return self.circle_center.x
        if self.bounds:
            return self.bounds.centroid.x
        return None

    def _latitude(self):
        if self.circle_center:
            return self.circle_center.y
        if self.bounds:
            return self.bounds.centroid.y
        return None

    def _circle(self, circle):
        try:
            circle_list = circle.split(',')
            # Sent latidude,longitude,radius
            return Point(float(circle_list[1]), float(circle_list[0])), float(circle_list[2])
        except (IndexError, AttributeError, ValueError):
            return None, 0

    def _bounds(self, bounds):
        try:
            bounds_list = bounds.split(',')
            sw = (bounds_list[0], bounds_list[1])
            ne = (bounds_list[2], bounds_list[3])
            xmin = sw[1]
            ymin = sw[0]
            xmax = ne[1]
            ymax = ne[0]
            bbox = (xmin, ymin, xmax, ymax)
            return Polygon.from_bbox(bbox)
        except (IndexError, AttributeError, ValueError):
            return None

    def get_events_within_bounds(self, queryset):
        if not self.bounds:
            return queryset
        queryset = queryset.filter(venue__point__within=self.bounds).\
                distance(self.bounds.centroid, field_name='venue__point')
        return queryset

    def get_events_near_center(self, queryset):
        if not self.circle_center:
            return queryset
        queryset = queryset.filter(venue__point__distance_lte=(self.circle_center, D(mi=self.radius_mi))).\
            distance(self.circle_center, field_name='venue__point')
        return queryset