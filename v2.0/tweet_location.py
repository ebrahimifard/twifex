from polygon_coordinates import PolygonCoordinates
from point_coordinates import PointCoordinates


class TweetLocation:
    def __init__(self, place, coordinates):

        assert (isinstance(place, dict) or place is None), "The place has to be a dict or None"
        assert (isinstance(coordinates, dict) or coordinates is None), "The coordinates has to be a dict or None"

        self._is_place_tagged = False if place is None else True
        self._is_coordinates_tagged = False if coordinates is None else True
        self._is_geotagged = True if (self._is_place_tagged is True or self._is_coordinates_tagged is True) else False
        self._id = None if place is None else place["id"]

        self._name = None if place is None else place["name"]
        self._full_name = None if place is None else place["full_name"]
        self._place_type = None if place is None else place["place_type"]
        self._city = self._full_name if self._place_type == "city" else None
        self._poi = self._full_name if self._place_type == "poi" else None
        self._country = None if place is None else place["country"]
        self._country_code = None if place is None else place["country_code"]

        self._url = None if place is None else place["url"]

        self._polygon_coordinates = None if place is None else PolygonCoordinates(place["bounding_box"])
        self._point_coordinates = None if coordinates is None else PointCoordinates(coordinates)

    def is_tweet_place_tagged(self):
        return self._is_place_tagged

    def is_tweet_coordinates_tagged(self):
        return self._is_coordinates_tagged

    def is_tweet_geotagged(self):
        return self._is_geotagged

    def get_tweet_location_id(self):
        return self._id

    def get_tweet_location_name(self):
        return self._name

    def get_tweet_location_full_name(self):
        return self._full_name

    def get_tweet_location_type(self):
        return self._place_type

    def get_tweet_location_city(self):
        return self._city

    # poi : point of interest
    def get_tweet_location_poi(self):
        return self._poi

    def get_tweet_location_country(self):
        return self._country

    def get_tweet_location_country_code(self):
        return self._country_code

    def get_tweet_location_polygon_coordinates(self):
        return self._polygon_coordinates

    def get_tweet_location_point_coordinates(self):
        return self._point_coordinates
