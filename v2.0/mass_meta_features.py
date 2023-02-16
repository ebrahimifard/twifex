from tweet_text_analysis import TweetTextAnalysis


class MassMetaFeatures:
    def __init__(self, tweets, features, feature_id_to_name, temporal=False, spatial=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

        self._temporal = temporal
        self._spatial = spatial



    # def tweets_clients_fraction
    def official_source_fraction(self):
        """
        This function finds the fraction of tweets posted from official sources in the dataset.
        :return: a float number showing the fraction of tweets posted from official sources.
        """
        target = 0
        for tweet_id, tweet in self.tweets.items():
            if tweet.tweet_source_status():
                target += 1
        return target / len(self.tweets)

    def tweets_replies_fraction(self):
        pass

    def tweets_mention_histogram(self):
        """
        This function counts the frequency of mentioning different users in the dataset.
        :return: a sorted dictionary that shows the frequency of mapping different users.
        """
        mention_histogram = {}
        for tweet_id in self.tweets:
            mentions = self.tweets[tweet_id].get_mentions()
            if len(mentions) != 0:
                for mention in mentions:
                    mention_histogram[mention["screen_name"]] = mention_histogram.get(mention["screen_name"], 0) + 1
        return {m[0]: m[1] for m in sorted(mention_histogram.items(), key=lambda p: p[1], reverse=True)}

    def tweets_hashtag_histogram(self):
        """
        This function counts the frequency of different hashtags in the dataset.
        :return: a sorted dictionary that shows the frequency of different hashtags.
        """
        hashtag_histogram = {}
        for tweet_id in self.tweets:
            hashtags = self.tweets[tweet_id].get_hashtags()
            if len(hashtags) != 0:
                for hashtag in hashtags:
                    hashtag_histogram[hashtag["text"]] = hashtag_histogram.get(hashtag["text"], 0) + 1
        return {m[0]: m[1] for m in sorted(hashtag_histogram.items(), key=lambda p: p[1], reverse=True)}

    def tweets_retweeted_status_histogram(self):
        """
        This function counts how many of the tweets in the dataset are retweets.
        :return: a dictionary that shows the number of retweets(True) and non-retweets(False).
        """
        retweet = {True: 0, False: 0}
        for tweet_id in self.tweets:
            if self.tweets[tweet_id].is_retweeted():
                retweet[True] += 1
            else:
                retweet[False] += 1
        return retweet

    def tweets_quoted_status_histogram(self):
        """
        This function counts how many of the tweets in the dataset are quoted.
        :return: a dictionary that shows the number of quoted-tweets(True) and non-quoted tweets(False).
        """
        quoted = {True: 0, False: 0}
        for tweet_id in self.tweets:
            if self.tweets[tweet_id].is_quoted():
                quoted[True] += 1
            else:
                quoted[False] += 1
        return quoted

    def tweets_photo_histogram(self):
        """
        This function counts the frequency of photos in the dataset.
        :return: a sorted dictionary that shows the frequency of mapping different users.
        """
        photos_histogram = {}
        for tweet_id in self.tweets:
            photos = self.tweets[tweet_id].get_photo()
            photos_histogram[len(photos)] = photos_histogram.get(len(photos), 0) + 1
        return photos_histogram

    def tweets_video_histogram(self):
        """
        This function counts the frequency of videos in the dataset.
        :return: a sorted dictionary that shows the frequency of mapping different users.
        """
        videos_histogram = {}
        for tweet_id in self.tweets:
            videos = self.tweets[tweet_id].get_video()
            videos_histogram[len(videos)] = videos_histogram.get(len(videos), 0) + 1
        return videos_histogram

    def tweets_gif_histogram(self):
        """
        This function counts the frequency of gifs in the dataset.
        :return: a sorted dictionary that shows the frequency of mapping different users.
        """
        gifs_histogram = {}
        for tweet_id in self.tweets:
            gifs = self.tweets[tweet_id].get_gif()
            gifs_histogram[len(gifs)] = gifs_histogram.get(len(gifs), 0) + 1
        return gifs_histogram

    def tweets_symbols_histogram(self):
        """
        This function counts the frequency of symbols in the dataset.
        :return: a sorted dictionary that shows the frequency of mapping different users.
        """
        symbols_histogram = {}
        for tweet_id in self.tweets:
            symbols = self.tweets[tweet_id].get_gif()
            symbols_histogram[len(symbols)] = symbols_histogram.get(len(symbols), 0) + 1
        return symbols_histogram
