
class SpatialTweets:
    def __init__(self, tweets):
        self._tweets = tweets
        # self._geotagged_tweets = self._geotagged_tweets(tweets)

    # @staticmethod
    # def _geotagged_tweets(tweets):
    #     """
    #     This function filters out all tweets without geo location.
    #     :return: a dictionary that maps every geotagged tweet_id to its corresponding SingleTweet object
    #     """
    #     return [p for p in tweets if p.get_tweet_location().is_geotagged()]

    def get_geotagged_tweets(self):
        """
        This function filters out all geotagged tweets (i.e., tweets without place or coordinates fields).
        :return: list of all geotagged tweets
        """
        geotagged_tweets = [tweet for tweet in self._tweets if tweet.get_tweet_location().is_tweet_geotagged()]
        return geotagged_tweets

    def get_place_tagged_tweets(self):
        """
        This function filters out all place-tagged tweets (i.e., tweets without place field).
        :return: list of all place-tagged tweets
        """
        place_tagged_tweets = [tweet for tweet in self._tweets if tweet.get_tweet_location().is_tweet_place_tagged()]
        return place_tagged_tweets

    def get_coordinates_tagged_tweets(self):
        """
        This function filters out all coordinates-tagged tweets (i.e., tweets without coordinates field).
        :return: list of all coordinates-tagged tweets
        """
        coordinates_tagged_tweets = [tweet for tweet in self._tweets if tweet.get_tweet_location().is_tweet_coordinates_tagged()]
        return coordinates_tagged_tweets

    def get_tweets_distinct_locations(self, spatial_unit="country"):
        assert (spatial_unit in ["country", "city", "poi", "polygon_coordinates", "point_coordinates", ]), \
            "The spatial unit has to be country, city, poi, polygon_coordinates, point_coordinates"

        if spatial_unit in ["country", "city", "poi", "polygon_coordinates"]:
            geotagged_tweets = self.get_place_tagged_tweets()
        elif spatial_unit == "point_coordinates":
            geotagged_tweets = self.get_coordinates_tagged_tweets()

        locations = []
        for tweet in geotagged_tweets:
            locations.append(eval(f"tweet.get_tweet_location().get_tweet_location_{spatial_unit}()"))
        return list(set(locations))

        # if spatial_unit == "country":
        #     for tweet in self._geotagged_tweets:
        #         locations.append(tweet.get_tweet_location().get_tweet_location_country())
        # elif spatial_unit == "city":
        #     for tweet in self._geotagged_tweets:
        #         if tweet.get_tweet_location().get_tweet_location_type() == "city":
        #             locations.append(tweet.get_tweet_location().get_tweet_location_full_name())
        # elif spatial_unit == "polygon_coordinates":
        #     for tweet in self._geotagged_tweets:
        #         locations.append(tweet.get_tweet_location().get_tweet_polygon_coordinates())
        # elif spatial_unit == "point_coordinates":
        #     for tweet in self._geotagged_tweets:
        #         locations.append(tweet.get_tweet_location().get_tweet_point_coordinates())
        #
        # return list(set(locations))

    # def tweets_distinct_countries(self):
    #     """
    #     This function finds all countries that the tweets in the dataset are coming from.
    #     :return: return a list of distinct countries.
    #     """
    #     countries = []
    #     for tweet in self._geotagged_tweets:
    #         countries.append(tweet.get_tweet_location().get_tweet_location_country())
    #
    #     return list(set(countries))
    #
    # def tweets_distinct_cities(self):
    #     """
    #     This function finds all cities that the tweets in the dataset are coming from.
    #     :return: return a list of distinct cities.
    #     """
    #     cities = []
    #     for tweet in self._geotagged_tweets:
    #         if tweet.get_tweet_location().get_tweet_location_type() == "city":
    #             cities.append(tweet.get_tweet_location().get_tweet_location_full_name())
    #
    #     return list(set(cities))
    #
    # def tweets_distinct_polygon_coordinates(self):
    #     polygon_coordinates = []
    #     for tweet in self._geotagged_tweets:
    #         polygon_coordinates.append(tweet.get_tweet_location().get_tweet_polygon_coordinates())
    #
    #     return list(set(polygon_coordinates))
    #
    # def tweets_distinct_point_coordinates(self):
    #     point_coordinates = []
    #     for tweet in self._geotagged_tweets:
    #         point_coordinates.append(tweet.get_tweet_location().get_tweet_point_coordinates())
    #
    #     return list(set(point_coordinates))

    def get_tweets_with_location(self, spatial_unit='country'):
        """
        This function mapped all the geotagged tweets to their locations based on the spatial resolution specified in
        the function argument.
        :param spatial_unit: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that maps every location to the list of all tweets coming from that location.
        """

        assert (spatial_unit in ["country", "city", "poi", "polygon_coordinates", "point_coordinates", ]), \
            "The spatial unit should be country, city, poi, polygon_coordinates, point_coordinates"

        if spatial_unit in ["country", "city", "poi", "polygon_coordinates"]:
            geotagged_tweets = self.get_place_tagged_tweets()
        elif spatial_unit == "point_coordinates":
            geotagged_tweets = self.get_coordinates_tagged_tweets()

        tweets_with_locations = {}
        for tweet in geotagged_tweets:
            loc = eval(f"tweet.get_tweet_location().get_tweet_location_{spatial_unit}()")
            tweets_with_locations[loc] = tweets_with_locations.get(loc, []) + [tweet]
        return tweets_with_locations

    # def countries_with_tweets(self):
    #     """
    #     This function mapped all the geotagged tweets to their country of origin.
    #     :return: a dictionary that maps every country to the list of all tweets coming from that country.
    #     """
    #     tweetsWithPlaces = self.geotagged_tweets()
    #     countries_dict = {}
    #     for tweet_id, tweet in tweetsWithPlaces.items():
    #         countries_dict[tweet.get_place()["country"]] = countries_dict.get(tweet.get_place()["country"], []) + [
    #             tweet]
    #     return countries_dict
    #
    # def places_with_tweets(self):
    #     """
    #     This function mapped all the geotagged tweets to their origin.
    #     :return: a dictionary that maps every place to the list of all tweets coming from that country.
    #     """
    #     tweetsWithPlaces = self.geotagged_tweets()
    #     places_dict = {}
    #     for tweet_id, tweet in tweetsWithPlaces.items():
    #         places_dict[tweet.get_place()["full_name"]] = places_dict.get(tweet.get_place()["full_name"], []) +
    #         [tweet]
    #     return places_dict
