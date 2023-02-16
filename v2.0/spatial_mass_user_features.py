from tweet_text_analysis import TweetTextAnalysis


class SpatialMassUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    def spatial_user_role(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user score across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user role of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_roles = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            user_roles[location] = []
            for tweet in tweets:
                user_roles[location] = user_roles.get(location, []) + [float(tweet.get_twitter().get_user_role())]

            scores = user_roles[location]
            user_roles[location] = {}
            if len(scores) > 0:
                user_roles[location]["average"] = np.nanmean(scores)
                user_roles[location]["max"] = np.nanmax(scores)
                user_roles[location]["min"] = np.nanmin(scores)
                user_roles[location]["stdev"] = np.nanstd(scores)
                user_roles[location]["median"] = np.nanmedian(scores)
            else:
                user_roles[location]["average"] = np.nan
                user_roles[location]["max"] = np.nan
                user_roles[location]["min"] = np.nan
                user_roles[location]["stdev"] = np.nan
                user_roles[location]["median"] = np.nan
        return user_roles

    def spatial_user_reputation(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user reputation across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user reputation of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_reputation = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            user_reputation[location] = []
            for tweet in tweets:
                user_reputation[location] = user_reputation.get(location, []) + [float(tweet.get_twitter().get_user_reputation())]

            scores = user_reputation[location]
            user_reputation[location] = {}
            if len(scores) > 0:
                user_reputation[location]["average"] = np.nanmean(scores)
                user_reputation[location]["max"] = np.nanmax(scores)
                user_reputation[location]["min"] = np.nanmin(scores)
                user_reputation[location]["stdev"] = np.nanstd(scores)
                user_reputation[location]["median"] = np.nanmedian(scores)
            else:
                user_reputation[location]["average"] = np.nan
                user_reputation[location]["max"] = np.nan
                user_reputation[location]["min"] = np.nan
                user_reputation[location]["stdev"] = np.nan
                user_reputation[location]["median"] = np.nan
        return user_reputation

    def spatial_followers(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents followers count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the followers count of every account
        that has posted at least a tweet within each spatial unit.
        """

        followers_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            followers_count[location] = []
            for tweet in tweets:
                followers_count[location] = followers_count.get(location, []) + \
                                            [float(tweet.get_twitter().get_followers_count())]

            scores = followers_count[location]
            followers_count[location] = {}
            if len(scores) > 0:
                followers_count[location]["average"] = np.nanmean(scores)
                followers_count[location]["max"] = np.nanmax(scores)
                followers_count[location]["min"] = np.nanmin(scores)
                followers_count[location]["stdev"] = np.nanstd(scores)
                followers_count[location]["median"] = np.nanmedian(scores)
            else:
                followers_count[location]["average"] = np.nan
                followers_count[location]["max"] = np.nan
                followers_count[location]["min"] = np.nan
                followers_count[location]["stdev"] = np.nan
                followers_count[location]["median"] = np.nan
        return followers_count

    def spatial_friends(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents friends count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the friends count of every account
        that has posted at least a tweet within each spatial unit.
        """

        friends_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            friends_count[location] = []
            for tweet in tweets:
                friends_count[location] = friends_count.get(location, []) + [float(tweet.get_twitter().get_friends_count())]

            scores = friends_count[location]
            friends_count[location] = {}
            if len(scores) > 0:
                friends_count[location]["average"] = np.nanmean(scores)
                friends_count[location]["max"] = np.nanmax(scores)
                friends_count[location]["min"] = np.nanmin(scores)
                friends_count[location]["stdev"] = np.nanstd(scores)
                friends_count[location]["median"] = np.nanmedian(scores)
            else:
                friends_count[location]["average"] = np.nan
                friends_count[location]["max"] = np.nan
                friends_count[location]["min"] = np.nan
                friends_count[location]["stdev"] = np.nan
                friends_count[location]["median"] = np.nan
        return friends_count

    def spatial_account_age(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents account age across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the age of every account
        that has posted at least a tweet within each spatial unit.
        """

        account_age = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            account_age[location] = []
            for tweet in tweets:
                account_age[location] = account_age.get(location, []) + [float(tweet.get_twitter().get_account_age())]

            scores = account_age[location]
            account_age[location] = {}
            if len(scores) > 0:
                account_age[location]["average"] = np.nanmean(scores)
                account_age[location]["max"] = np.nanmax(scores)
                account_age[location]["min"] = np.nanmin(scores)
                account_age[location]["stdev"] = np.nanstd(scores)
                account_age[location]["median"] = np.nanmedian(scores)
            else:
                account_age[location]["average"] = np.nan
                account_age[location]["max"] = np.nan
                account_age[location]["min"] = np.nan
                account_age[location]["stdev"] = np.nan
                account_age[location]["median"] = np.nan
        return account_age

    def spatial_total_likes(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents total account likes across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the totall likes of every account
        that has posted at least a tweet within each spatial unit.
        """

        total_likes = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            total_likes[location] = []
            for tweet in tweets:
                total_likes[location] = total_likes.get(location, []) + [float(tweet.get_twitter().get_user_total_likes_count())]

            scores = total_likes[location]
            total_likes[location] = {}
            if len(scores) > 0:
                total_likes[location]["average"] = np.nanmean(scores)
                total_likes[location]["max"] = np.nanmax(scores)
                total_likes[location]["min"] = np.nanmin(scores)
                total_likes[location]["stdev"] = np.nanstd(scores)
                total_likes[location]["median"] = np.nanmedian(scores)
            else:
                total_likes[location]["average"] = np.nan
                total_likes[location]["max"] = np.nan
                total_likes[location]["min"] = np.nan
                total_likes[location]["stdev"] = np.nan
                total_likes[location]["median"] = np.nan
        return total_likes

    def spatial_status_count(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents status count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the status count of every account
        that has posted at least a tweet within each spatial unit.
        """

        status_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            status_count[location] = []
            for tweet in tweets:
                status_count[location] = status_count.get(location, []) + [float(tweet.get_twitter().get_statusses_count())]

            scores = status_count[location]
            status_count[location] = {}
            if len(scores) > 0:
                status_count[location]["average"] = np.nanmean(scores)
                status_count[location]["max"] = np.nanmax(scores)
                status_count[location]["min"] = np.nanmin(scores)
                status_count[location]["stdev"] = np.nanstd(scores)
                status_count[location]["median"] = np.nanmedian(scores)
            else:
                status_count[location]["average"] = np.nan
                status_count[location]["max"] = np.nan
                status_count[location]["min"] = np.nan
                status_count[location]["stdev"] = np.nan
                status_count[location]["median"] = np.nan
        return status_count