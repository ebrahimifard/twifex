
class PlaceFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def geotagged_tweets(self):
        """
        This function filters out all tweets without geo location.
        :return: a dictionary that maps every geotagged tweet_id to its corresponding SingleTweet object
        """
        return {p: q for p, q in self.tweets.items() if q.get_place() != None}

    def tweets_distinct_countries(self):
        """
        This function finds all countries that the tweets in the dataset are comming from.
        :return: return a list of distinct countries.
        """
        tweetsWithPlaces = self.geotagged_tweets()
        places = set()
        for tweet_id, tweet in tweetsWithPlaces.items():
            place = tweet.get_place()
            places.add(place["country"])
        return list(places)

    def tweets_distinct_places(self, coordinates=True):
        """
        This function finds all places that the tweets in the dataset are comming from.
        :return: return a list of distinct places.
        """
        tweetsWithPlaces = self.geotagged_tweets()
        places_coordinates = {}
        for tweet_id, tweet in tweetsWithPlaces.items():
            place = tweet.get_place()
            places_coordinates[place["full_name"]] = places_coordinates.get(place["full_name"], place["bounding_box"])
        if coordinates:
            return places_coordinates
        else:
            return list(places_coordinates.keys())

    def tweets_with_location(self, spatial_resolution='country'):
        """
        This function mapped all the geotagged tweets to their locations based on the spatial resolution specified in the function argument.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that maps every location to the list of all tweets coming from that location.
        """
        if spatial_resolution == 'country':
            res = "country"
        elif spatial_resolution == 'place':
            res = "full_name"

        tweetsWithPlaces = self.geotagged_tweets()
        location_dict = {}
        for tweet_id, tweet in tweetsWithPlaces.items():
            location_dict[tweet.get_place()[res]] = location_dict.get(tweet.get_place()[res], []) + [
                tweet]
        return location_dict

    # def countries_with_tweets(self):
    #     """
    #     This function mapped all the geotagged tweets to their country of origin.
    #     :return: a dictionary that maps every country to the list of all tweets comming from that country.
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
    #     :return: a dictionary that maps every place to the list of all tweets comming from that country.
    #     """
    #     tweetsWithPlaces = self.geotagged_tweets()
    #     places_dict = {}
    #     for tweet_id, tweet in tweetsWithPlaces.items():
    #         places_dict[tweet.get_place()["full_name"]] = places_dict.get(tweet.get_place()["full_name"], []) + [tweet]
    #     return places_dict