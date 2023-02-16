from tweet_text_analysis import TweetTextAnalysis


class TemporalSpatialMassUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    def temporal_spatial_tweets(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :return: an embedded dictionary that classifies a set of tweets into a hierarchical structure in which the
        key-value corresponds to a location (or a timestamp depending on the value of "order" parameter) and another
        dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be all tweets
        corresponding to the location and timestamp.
        """

        assert (order in ["spatial-temporal", "temporal-spatial"])
        assert (temporal_resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time " \
                                                                                                      "resolution " \
                                                                                                      "should be year,"\
                                                                                                      "month,week,day,"\
                                                                                                      "hour, minute, " \
                                                                                                      "or second"
        assert (isinstance(temporal_frequency, int) and temporal_frequency>0), "The temporal frequency has to be a " \
                                                                               "positive integer"
        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"

        tweet_set = {}
        if order == "spatial-temporal":
            spatial_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
            for location, tweets in spatial_tweets.items():
                tweet_set[location] = TemporalFeatures(TwifexUtility.collective_tweets_to_dictionary(tweets)).tweets_in_periods(resolution=temporal_resolution, frequency=temporal_frequency)
        elif order == "temporal-spatial":
            temporal_tweets = self.tweets_in_periods(resolution=temporal_resolution, frequency=temporal_frequency)
            for timestamp, tweets in temporal_tweets.items():
                tweet_set[timestamp] = PlaceFeatures(TwifexUtility.collective_tweets_to_dictionary(tweets)).tweets_with_location(spatial_resolution=spatial_resolution)
        return tweet_set

    def temporal_spatial_user_status_count(self, order='spatial-temporal', temporal_resolution='day',
                                           temporal_frequency=1, spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :return: a dictionary that represents user score across spatial units. The key-value pair in this dictionary
        corresponds to the spatial unit of analysis and statistical metrics of the user role of every account
        that has posted at least a tweet within each spatial unit.
        :return: an embedded dictionary that represents number of user's posts within a hierarchical structure in
        which the key-value corresponds to a location (or a timestamp depending on the value of "order" parameter)
        and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would
        be all the tweets posted by the user accounts corresponding to the location and timestamp.
        """

        assert (order in ["spatial-temporal", "temporal-spatial"]), "The order should be either spatial-temporal or " \
                                                                    "temporal-spatial"
        assert (temporal_resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time " \
                                                                                                      "resolution " \
                                                                                                      "should be year,"\
                                                                                                      "month,week,day,"\
                                                                                                      " hour, minute,"\
                                                                                                      "or second"
        assert (isinstance(temporal_frequency, int) and temporal_frequency > 0), "The temporal frequency has to be a " \
                                                                               "positive integer"
        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"


        total_likes = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution,
                                                           temporal_frequency=temporal_frequency,
                                                           spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            total_likes[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                total_likes[layer1][layer2] = []
                for tweet in tweets:
                    total_likes[layer1][layer2] = total_likes[layer1].get(layer2, []) + \
                                                 [float(tweet.get_twitter().get_statusses_count())]

                scores = total_likes[layer1][layer2]
                total_likes[layer1][layer2] = {}
                if len(scores) > 0:
                    total_likes[layer1][layer2]["average"] = np.nanmean(scores)
                    total_likes[layer1][layer2]["max"] = np.nanmax(scores)
                    total_likes[layer1][layer2]["min"] = np.nanmin(scores)
                    total_likes[layer1][layer2]["stdev"] = np.nanstd(scores)
                    total_likes[layer1][layer2]["median"] = np.nanmedian(scores)
                    total_likes[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    total_likes[layer1][layer2]["average"] = np.nan
                    total_likes[layer1][layer2]["max"] = np.nan
                    total_likes[layer1][layer2]["min"] = np.nan
                    total_likes[layer1][layer2]["stdev"] = np.nan
                    total_likes[layer1][layer2]["median"] = np.nan
                    total_likes[layer1][layer2]["sum"] = np.nan
                total_likes[layer1][layer2]["count"] = len(scores)

        return total_likes

    def temporal_spatial_user_analysis(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                       spatial_resolution='country', analysis_type='follower_count'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :param analysis_type: This field specifies the type of analysis on the tweet users. It can be "users_role",
        "users_reputation", "users_followers_count", "users_friends_count", "users_account_age", "total_likes_count",
        and "users_status_count".
        :return: an embedded dictionary that represents users reputation within a hierarchical structure in which the
        key-value corresponds to a location (or a timestamp depending on the value of "order" parameter) and another
        dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be all the
        user reputation corresponding to the location and timestamp.
        """

        assert (order in ["spatial-temporal", "temporal-spatial"]), "The order should be either spatial-temporal or " \
                                                                    "temporal-spatial"
        assert (temporal_resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time " \
                                                                                                      "resolution " \
                                                                                                      "should be year,"\
                                                                                                      "month,week,day,"\
                                                                                                      " hour, minute,"\
                                                                                                      "or second"
        assert (isinstance(temporal_frequency, int) and temporal_frequency > 0), "The temporal frequency has to be a " \
                                                                               "positive integer"
        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (analysis_type in ["users_role", "users_reputation", "users_followers_count", "users_friends_count",
                                  "users_account_age", "total_likes_count", "users_status_count"]), "The type of " \
                                                                                                    "analysis could be " \
                                                                                                    "user role, " \
                                                                                                    "user reputation, " \
                                                                                                    "users_followers_count, " \
                                                                                                    "users_friends_count, " \
                                                                                                    "users_account_age, " \
                                                                                                    "total_likes_count," \
                                                                                                    " and users_status_count"

        container = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution,
                                                           temporal_frequency=temporal_frequency,
                                                           spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            container[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                container[layer1][layer2] = []
                for tweet in tweets:

                    if analysis_type == "users_role":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                     [float(tweet.get_twitter().get_user_role())]
                    elif analysis_type == "users_reputation":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                          [float(tweet.get_twitter().get_user_reputation())]
                    elif analysis_type == "users_followers_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                     [float(tweet.get_twitter().get_followers_count())]
                    elif analysis_type == "users_friends_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                       [float(tweet.get_twitter().get_friends_count())]
                    elif analysis_type == "users_account_age":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_account_age())]
                    elif analysis_type == "total_likes_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_user_total_likes_count())]
                    elif analysis_type == "users_status_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_statusses_count())]

                # scores = container[layer1][layer2]
                # container[layer1][layer2] = {}

                container[layer1][layer2] = TwifexUtility.basic_statistics(container[layer1][layer2])
                # if len(scores) > 0:
                #     container[layer1][layer2]["average"] = np.nanmean(scores)
                #     container[layer1][layer2]["max"] = np.nanmax(scores)
                #     container[layer1][layer2]["min"] = np.nanmin(scores)
                #     container[layer1][layer2]["stdev"] = np.nanstd(scores)
                #     container[layer1][layer2]["median"] = np.nanmedian(scores)
                #     container[layer1][layer2]["sum"] = np.nansum(scores)
                # else:
                #     container[layer1][layer2]["average"] = np.nan
                #     container[layer1][layer2]["max"] = np.nan
                #     container[layer1][layer2]["min"] = np.nan
                #     container[layer1][layer2]["stdev"] = np.nan
                #     container[layer1][layer2]["median"] = np.nan
                #     container[layer1][layer2]["sum"] = np.nan
                # container[layer1][layer2]["count"] = len(scores)

        return container