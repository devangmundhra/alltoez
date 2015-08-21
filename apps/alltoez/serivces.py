from django.contrib.gis.geos import Polygon


class EventSearchServices(object):
    zoom = 0
    bounds = None
    latitude = None
    longitude = None

    def __init__(self, zoom=8, bounds=None):
        self.zoom = zoom
        self.bounds = self._bounds(bounds)
        self.latitude = self._latitude()
        self.longitude = self._longitude()

    def _latitude(self):
        return  self.bounds.centroid.x if self.bounds else None

    def _longitude(self):
        return  self.bounds.centroid.y if self.bounds else None

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
        except (IndexError, AttributeError):
            return None

    def get_events_within_bounds(self, queryset):
        queryset = queryset.filter(venue__point__within=self.bounds).\
                distance(self.bounds.centroid, field_name='venue__point')
        return queryset
