from point_coordinates import PointCoordinates


class PolygonCoordinates:
    def __init__(self, coordinates):

        assert isinstance(coordinates, dict), "The point has to be a dict"

        self._is_polygon_coordinates_available = False if coordinates is None \
            else [True if coordinates["type"] == "Polygon" else False]
        self._coordinates = [PointCoordinates({"coordinates": i, "type": "Point"})
                             for i in coordinates["coordinates"][0]] if self._is_polygon_coordinates_available else None

    def is_polygon_coordinates_available(self):
        return self._is_polygon_coordinates_available

    def get_coordinates(self):
        return self._coordinates

    def __eq__(self, other):
        flag = False
        for i in self.get_coordinates():
            for j in other.get_coordinates():
                if i.get_longitude() == j.get_longitude() and i.get_latitude() == j.get_latitude():
                    flag = True
                    break
                else:
                    flag = False
        return flag

