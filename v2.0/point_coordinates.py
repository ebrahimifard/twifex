
class PointCoordinates:
    def __init__(self, point):

        assert isinstance(point, dict), "The point has to be a dict"

        self._is_point_coordinates_available = False if point is None \
            else [True if point["type"] == "Point" else False]
        if self._is_point_coordinates_available:
            self._longitude = point["coordinates"][0]
            self._latitude = point["coordinates"][1]
        else:
            self._longitude = None
            self._latitude = None

    def is_point_coordinates_available(self):
        return self._is_point_coordinates_available

    def get_longitude(self):
        return self._longitude

    def get_latitude(self):
        return self._latitude

    def __eq__(self, other):
        if self.get_longitude() == other.get_longitude() and self.get_latitude() == other.get_latitude():
            return True
        else:
            return False
