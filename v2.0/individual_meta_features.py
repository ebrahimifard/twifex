from datetime import datetime


class IndividualMetaFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_collection = tweets
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name

    #temporal features
    def tweet_month(self):
        feature_id = max(list(self._features_id_name_dict.keys()) ) + 1
        self._features_id_name_dict[feature_id] = tweet_month.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.month

    def tweet_week(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_week.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.date().isocalendar()[1]

    def tweet_day_of_month(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_day_of_month.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.day

    def tweet_weekday(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_weekday.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.date().isocalendar()[2]

    def tweet_hour(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_hour.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.hour

    def tweet_minute(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_minute.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.minute

    def tweet_second(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_second.__name__

        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = dt_obj.second

    def tweet_is_in_certain_period(self, period_start="30-01-2000 10:30:00", period_end="30-12-2022 23:45:30"):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_is_in_certain_period.__name__

        period_start_dt_obj = datetime.strptime(period_start, "%d-%m-%Y %H:%M:%S")
        period_end_dt_obj = datetime.strptime(period_end, "%d-%m-%Y %H:%M:%S")
        for tweet in self._tweets_collection:
            dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet][feature_id] = True if (dt_obj >= period_start_dt_obj and dt_obj <= period_end_dt_obj) else False

    #Hashtag
    def meta_any_hashtag(self):
        pass

    def meta_hashtags_count(self):
        pass

    #Mentions
    def meta_any_mention(self0):
        pass

    def meta_mentions_count(self):
        pass

    #URLs
    def meta_any_url(self):
        pass

    def meta_urls_count(self):
        pass

    #Photos
    def meta_any_photo(self):
        pass

    def meta_photos_count(self):
        pass

    #Video
    def meta_any_video(self):
        pass

    #Gif
    def meta_any_gif(self):
        pass

    #Likes
    def meta_likes_count(self):
        pass

    #Retweet
    def meta_retweets_count(self):
        pass

    #Reply
    def meta_is_this_a_reply(self):
        pass

    #Location
    def meta_is_this_geotagged_with_point_coordinates(self):
        pass

    def meta_is_this_geotagged_with_polygone_coordinates(self0):
        pass




    #Retweet
    def meta_is_this_a_retweet(self):
        pass

    #Quote
    def meta_is_this_a_quote(self):
        pass