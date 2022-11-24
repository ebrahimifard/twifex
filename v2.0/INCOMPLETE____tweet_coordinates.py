# UNECESSARY FILE=> HAS TO BE DELETED

# from point_coordinates import PointCoordinates
# from polygon_coordinates import PolygonCoordinates
#
#
# class TweetCoordinates:
#     def __init__(self, coordinates):
#         self._is_coordinates_available = False if coordinates is None else True
#         self._coordinates_type = coordinates["type"] if self._is_coordinates_available else None
#         self._polygon_coordinates = PolygonCoordinates(coordinates) if self._coordinates_type == "Polygon" else None
#         self._point_coordinates = PointCoordinates(coordinates) if self._coordinates_type == "Point" else None
#
#     def get_tweet_polygon_coordinates(self):
#         return self._polygon_coordinates
#
#     def get_tweet_point_coordinates(self):
#         return self._point_coordinates
