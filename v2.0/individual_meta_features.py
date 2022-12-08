from datetime import datetime
from individual_content_features import IndividualContentFeatures
from individual_user_features import IndividualUserFeatures
from tweets import Tweets


class IndividualMetaFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        # self._retweets = [twt.get_tweet_retweet_object() for twt in self._tweets_obj.get_retweeted_tweets().get_tweets_list()]

    #temporal features
    def tweet_month(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_month"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_month"
        else:
            self._features_id_name_dict[feature_id] = "tweet_month"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.month

    def tweet_week(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_week"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_week"
        else:
            self._features_id_name_dict[feature_id] = "tweet_week"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.date().isocalendar()[1]

    def tweet_day_of_month(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_day_of_month"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_day_of_month"
        else:
            self._features_id_name_dict[feature_id] = "tweet_day_of_month"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.day

    def tweet_weekday(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_weekday"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_weekday"
        else:
            self._features_id_name_dict[feature_id] = "tweet_weekday"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.date().isocalendar()[2]

    def tweet_hour(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_hour"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_hour"
        else:
            self._features_id_name_dict[feature_id] = "tweet_hour"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.hour

    def tweet_minute(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_minute"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_minute"
        else:
            self._features_id_name_dict[feature_id] = "tweet_minute"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.minute

    def tweet_second(self, retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_second"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_second"
        else:
            self._features_id_name_dict[feature_id] = "tweet_second"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dt_obj.second

    def tweet_is_in_certain_period(self, period_start="30-01-2000 10:30:00", period_end="30-12-2022 23:45:30", retweet_flag=False, quote_flag=False):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        period_start_dt_obj = datetime.strptime(period_start, "%d-%m-%Y %H:%M:%S")
        period_end_dt_obj = datetime.strptime(period_end, "%d-%m-%Y %H:%M:%S")
        if retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"tweet_is_in_{period_start}-{period_end}"
        elif quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + f"tweet_is_in_{period_start}-{period_end}"
        else:
            self._features_id_name_dict[feature_id] = f"tweet_is_in_{period_start}-{period_end}"

        for tweet in self._tweets_collection:
            if retweet_flag:
                dt_obj = tweet.get_tweet_retweet_object().get_tweet_creation_time()
            elif quote_flag:
                dt_obj = tweet.get_quote_status_object().get_tweet_creation_time()
            else:
                dt_obj = tweet.get_tweet_creation_time()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if (dt_obj >= period_start_dt_obj and dt_obj <= period_end_dt_obj) else False

    #Hashtag
    def any_hashtag(self):
        pass

    def hashtags_count(self):
        pass

    #Mentions
    def any_mention(self0):
        pass

    def mentions_count(self):
        pass

    #URLs
    def any_url(self):
        pass

    def urls_count(self):
        pass

    #Photos
    def any_photo(self):
        pass

    def photos_count(self):
        pass

    #Video
    def any_video(self):
        pass

    #Gif
    def any_gif(self):
        pass

    #Likes
    def likes_count(self):
        pass

    #Retweet
    def retweets_count(self):
        pass

    #Reply
    def is_this_a_reply(self):
        pass

    #Location
    def is_this_geotagged_with_point_coordinates(self):
        pass

    def mis_this_geotagged_with_polygone_coordinates(self0):
        pass

    #Retweet
    def is_this_a_retweet(self):
        feature_id = max(list(self._features_id_name_dict.keys()) ) + 1
        self._features_id_name_dict[feature_id] = is_this_a_retweet.__name__

        for tweet in self._tweets_collection:
            self._tweets_features[tweet][feature_id] = tweet.is_tweet_retweeted()

    def retweet_content_features(self):
        retweets = self._tweets_obj.get_retweeted_tweets()
        return IndividualContentFeatures(retweets, self._tweets_features, self._features_id_name_dict, retweet_flag=True, quote_flag=False)

    def retweet_user_features(self):
        retweets = self._tweets_obj.get_retweeted_tweets()
        return IndividualUserFeatures(retweets, self._tweets_features, self._features_id_name_dict, retweet_flag=True, quote_flag=False)

    def retweet_meta_features(self):
        retweets = self._tweets_obj.get_retweeted_tweets()
        return IndividualMetaFeatures(retweets, self._tweets_features, self._features_id_name_dict, retweet_flag=True, quote_flag=False)

    #Quote
    def is_this_a_quote(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = is_this_a_quote.__name__

        for tweet in self._tweets_collection:
            self._tweets_features[tweet][feature_id] = tweet.is_tweet_quoted()

    def quote_content_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualContentFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

    def quote_user_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualUserFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

    def quote_meta_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualMetaFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

