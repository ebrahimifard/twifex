from datetime import datetime
from individual_content_features import IndividualContentFeatures
from individual_user_features import IndividualUserFeatures
from tweets import Tweets
from tweet_text_analysis import TweetTextAnalysis


class IndividualMetaFeatures:
    def __init__(self, tweets, features, feature_id_to_name, retweet_flag=False, quote_flag=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()
        self._retweet_flag = retweet_flag
        self._quote_flag = quote_flag

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
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_hashtag"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_hashtag"
        else:
            self._features_id_name_dict[feature_id] = "any_hashtag"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_hashtags_obj = tweet.get_tweet_retweet_object().get_tweet_hashtags()
            elif self._quote_flag:
                twt_hashtags_obj = tweet.get_quote_status_object().get_tweet_hashtags()
            else:
                twt_hashtags_obj = tweet.get_tweet_hashtags()
            twt_hashtags = twt_hashtags_obj.get_tweet_hashtags()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_hashtags) > 0 else False

    def hashtags_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "hashtags_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "hashtags_count"
        else:
            self._features_id_name_dict[feature_id] = "hashtags_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_hashtags_obj = tweet.get_tweet_retweet_object().get_tweet_hashtags()
            elif self._quote_flag:
                twt_hashtags_obj = tweet.get_quote_status_object().get_tweet_hashtags()
            else:
                twt_hashtags_obj = tweet.get_tweet_hashtags()
            twt_hashtags = twt_hashtags_obj.get_tweet_hashtags()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(twt_hashtags)

    #Mentions
    def any_mention(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_mention"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_mention"
        else:
            self._features_id_name_dict[feature_id] = "any_mention"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_mentions_obj = tweet.get_tweet_retweet_object().get_tweet_mentions()
            elif self._quote_flag:
                twt_mentions_obj = tweet.get_quote_status_object().get_tweet_mentions()
            else:
                twt_mentions_obj = tweet.get_tweet_mentions()
            twt_mentions = twt_mentions_obj.get_tweet_mentions()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_mentions) > 0 else False

    def mentions_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "mentions_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "mentions_count"
        else:
            self._features_id_name_dict[feature_id] = "mentions_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_mentions_obj = tweet.get_tweet_retweet_object().get_tweet_mentions()
            elif self._quote_flag:
                twt_mentions_obj = tweet.get_quote_status_object().get_tweet_mentions()
            else:
                twt_mentions_obj = tweet.get_tweet_mentions()
            twt_mentions = twt_mentions_obj.get_tweet_mentions()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(twt_mentions)

    #URLs
    def any_url(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_url"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_url"
        else:
            self._features_id_name_dict[feature_id] = "any_url"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_urls_obj = tweet.get_tweet_retweet_object().get_tweet_urls()
            elif self._quote_flag:
                twt_urls_obj = tweet.get_quote_status_object().get_tweet_urls()
            else:
                twt_urls_obj = tweet.get_tweet_urls()
            twt_urls = twt_urls_obj.get_tweet_urls()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_urls) > 0 else False

    def urls_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "urls_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "urls_count"
        else:
            self._features_id_name_dict[feature_id] = "urls_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_urls_obj = tweet.get_tweet_retweet_object().get_tweet_urls()
            elif self._quote_flag:
                twt_urls_obj = tweet.get_quote_status_object().get_tweet_urls()
            else:
                twt_urls_obj = tweet.get_tweet_urls()
            twt_urls = twt_urls_obj.get_tweet_urls()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(twt_urls)

    #Photos
    def any_photo(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_photo"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_photo"
        else:
            self._features_id_name_dict[feature_id] = "any_photo"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_photos_obj = tweet.get_tweet_retweet_object().get_tweet_photos()
            elif self._quote_flag:
                twt_photos_obj = tweet.get_quote_status_object().get_tweet_photos()
            else:
                twt_photos_obj = tweet.get_tweet_photos()
            twt_photos = twt_photos_obj.get_tweet_photo_urls()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_photos) > 0 else False

    def photos_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "photos_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "photos_count"
        else:
            self._features_id_name_dict[feature_id] = "photos_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_photos_obj = tweet.get_tweet_retweet_object().get_tweet_photos()
            elif self._quote_flag:
                twt_photos_obj = tweet.get_quote_status_object().get_tweet_photos()
            else:
                twt_photos_obj = tweet.get_tweet_photos()
            twt_photos = twt_photos_obj.get_tweet_photo_urls()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(twt_photos)

    #Video
    def any_video(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_video"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_video"
        else:
            self._features_id_name_dict[feature_id] = "any_video"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_video_obj = tweet.get_tweet_retweet_object().get_tweet_video()
            elif self._quote_flag:
                twt_video_obj = tweet.get_quote_status_object().get_tweet_video()
            else:
                twt_video_obj = tweet.get_tweet_video()
            twt_video = twt_video_obj.get_tweet_video_url()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_video) > 0 else False

    #Gif
    def any_gif(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "any_gif"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "any_gif"
        else:
            self._features_id_name_dict[feature_id] = "any_gif"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_gif_obj = tweet.get_tweet_retweet_object().get_tweet_gif()
            elif self._quote_flag:
                twt_gif_obj = tweet.get_quote_status_object().get_tweet_gif()
            else:
                twt_gif_obj = tweet.get_tweet_gif()
            twt_gif = twt_gif_obj.get_tweet_gif_url()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if len(twt_gif) > 0 else False

    #Likes
    def likes_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "likes_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "likes_count"
        else:
            self._features_id_name_dict[feature_id] = "likes_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
            else:
                twt_obj = tweet
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_obj.get_tweet_likes_count()

    #Retweet
    def retweets_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "retweets_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "retweets_count"
        else:
            self._features_id_name_dict[feature_id] = "retweets_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
            else:
                twt_obj = tweet
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_obj.get_tweet_retweets_count()

    #Reply
    def is_this_a_reply(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "is_this_a_reply"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "is_this_a_reply"
        else:
            self._features_id_name_dict[feature_id] = "is_this_a_reply"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
            else:
                twt_obj = tweet
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_obj.is_tweet_a_reply()

    #Location
    def is_this_geotagged_with_point_coordinates(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "is_this_geotagged_with_point_coordinates"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "is_this_geotagged_with_point_coordinates"
        else:
            self._features_id_name_dict[feature_id] = "is_this_geotagged_with_point_coordinates"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_loc_obj = tweet.get_tweet_retweet_object().get_tweet_location()
            elif self._quote_flag:
                twt_loc_obj = tweet.get_quote_status_object().get_tweet_location()
            else:
                twt_loc_obj = tweet.get_tweet_location()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_loc_obj.is_tweet_coordinates_tagged()

    def is_this_geotagged_with_polygone_coordinates(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "is_this_geotagged_with_polygone_coordinates"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "is_this_geotagged_with_polygone_coordinates"
        else:
            self._features_id_name_dict[feature_id] = "is_this_geotagged_with_polygone_coordinates"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_loc_obj = tweet.get_tweet_retweet_object().get_tweet_location()
            elif self._quote_flag:
                twt_loc_obj = tweet.get_quote_status_object().get_tweet_location()
            else:
                twt_loc_obj = tweet.get_tweet_location()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_loc_obj.is_tweet_place_tagged()

    #Retweet
    def is_this_a_retweet(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "is_this_a_retweet"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "is_this_a_retweet"
        else:
            self._features_id_name_dict[feature_id] = "is_this_a_retweet"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
            else:
                twt_obj = tweet
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_obj.is_tweet_retweeted()

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
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "is_this_a_quote"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "is_this_a_quote"
        else:
            self._features_id_name_dict[feature_id] = "is_this_a_quote"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
            else:
                twt_obj = tweet
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_obj.is_tweet_quoted()

    def quote_content_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualContentFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

    def quote_user_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualUserFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

    def quote_meta_features(self):
        quotes = self._tweets_obj.get_quoted_tweets()
        return IndividualMetaFeatures(quotes, self._tweets_features, self._features_id_name_dict, retweet_flag=False, quote_flag=True)

