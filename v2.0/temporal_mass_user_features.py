from tweet_text_analysis import TweetTextAnalysis


class TemporalMassUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()


    def users_role_change(self, nodes):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :return: a dictionary that represents the change of the user role across the timespan of the dataset.
        The key-value pair in this dictionary corresponds to the timestamps and statistical metrics of the user roles
        in all the tweets that are posted within every timestamp.
        """

        user_roles = {}
        for time_frame, tweets in nodes.items():
            user_roles[time_frame] = []
            user_roles_results = []
            for tweet in tweets:
                user_roles_results.append(tweet.get_twitter().get_user_role())
            for result in user_roles_results:
                user_roles[time_frame] = user_roles.get(time_frame, []) + [float(result)]

            scores = user_roles[time_frame]
            user_roles[time_frame] = {}
            if len(scores) > 0:
                user_roles[time_frame]["average"] = np.nanmean(scores)
                user_roles[time_frame]["max"] = np.nanmax(scores)
                user_roles[time_frame]["min"] = np.nanmin(scores)
                user_roles[time_frame]["stdev"] = np.nanstd(scores)
                user_roles[time_frame]["median"] = np.nanmedian(scores)
            else:
                user_roles[time_frame]["average"] = np.nan
                user_roles[time_frame]["max"] = np.nan
                user_roles[time_frame]["min"] = np.nan
                user_roles[time_frame]["stdev"] = np.nan
                user_roles[time_frame]["median"] = np.nan
        return user_roles