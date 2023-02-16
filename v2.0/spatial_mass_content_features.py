from tweet_text_analysis import TweetTextAnalysis


class SpatialMassContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    def spatial_tweet_complexity(self, spatial_resolution='country', complexity_unit="word"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param complexity_unit: the unit of analysis for measuring tweet complexity. It can be "word", "sentence", or "syllables".
        :return: a dictionary that represents the tweet complexity across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet complexity scores in all the tweets that are posted
        within every spatial unit.
        """

        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (complexity_unit in ["word", "sentence",
                         "syllables"]), "The unit of analysis has to be word, sentence, or syllables"

        complexity = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            complexity[location] = []
            for tweet in tweets:
                complexity[location] = complexity.get(location, []) + [float(tweet.text_complexity(complexity_unit=complexity_unit))]

            scores = complexity[location]
            complexity[location] = {}
            if len(scores) > 0:
                complexity[location]["average"] = np.nanmean(scores)
                complexity[location]["max"] = np.nanmax(scores)
                complexity[location]["min"] = np.nanmin(scores)
                complexity[location]["stdev"] = np.nanstd(scores)
                complexity[location]["median"] = np.nanmedian(scores)
            else:
                complexity[location]["average"] = np.nan
                complexity[location]["max"] = np.nan
                complexity[location]["min"] = np.nan
                complexity[location]["stdev"] = np.nan
                complexity[location]["median"] = np.nan
        return complexity

    def spatial_tweet_readability(self, spatial_resolution='country', readability_metric="flesch_kincaid_grade"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
        :return: a dictionary that represents the tweet readability score across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet readability scores in all the tweets that are posted
        within every spatial unit.
        """

        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        readability = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            readability[location] = []
            for tweet in tweets:
                readability[location] = readability.get(location, []) + [float(tweet.readability(readability_metric=readability_metric))]

            scores = readability[location]
            readability[location] = {}
            if len(scores) > 0:
                readability[location]["average"] = np.nanmean(scores)
                readability[location]["max"] = np.nanmax(scores)
                readability[location]["min"] = np.nanmin(scores)
                readability[location]["stdev"] = np.nanstd(scores)
                readability[location]["median"] = np.nanmedian(scores)
            else:
                readability[location]["average"] = np.nan
                readability[location]["max"] = np.nan
                readability[location]["min"] = np.nan
                readability[location]["stdev"] = np.nan
                readability[location]["median"] = np.nan
        return readability

    def spatial_tweet_length(self, spatial_resolution='country', length_unit="word"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param length_unit: the unit of analysis for measuring tweet length. It can be "character", "word", or "sentence".
        :return: a dictionary that represents the tweet length across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet length in all the tweets that are posted
        within every spatial unit.
        """

        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (length_unit in ["character", "word", "sentence"]), "The unit has to be character, word, or sentence"

        tweet_length = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            tweet_length[location] = []
            for tweet in tweets:
                tweet_length[location] = tweet_length.get(location, []) + [float(tweet.text_length(length_unit=length_unit))]

            scores = tweet_length[location]
            tweet_length[location] = {}
            if len(scores) > 0:
                tweet_length[location]["average"] = np.nanmean(scores)
                tweet_length[location]["max"] = np.nanmax(scores)
                tweet_length[location]["min"] = np.nanmin(scores)
                tweet_length[location]["stdev"] = np.nanstd(scores)
                tweet_length[location]["median"] = np.nanmedian(scores)
            else:
                tweet_length[location]["average"] = np.nan
                tweet_length[location]["max"] = np.nan
                tweet_length[location]["min"] = np.nan
                tweet_length[location]["stdev"] = np.nan
                tweet_length[location]["median"] = np.nan
        return tweet_length

    def spatial_tweet_count(self, spatial_resolution='country'):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents the tweet count across the spatial units.
        The key-value pair in this dictionary corresponds to the spatial unit of analysis and
        the the number of the tweets that are posted within every spatial unit.
        """
        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"

        tweet_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)

        for location, tweets in geotagged_tweets.items():
            tweet_count[location] = len(tweets)
        return tweet_count

    def spatial_sentiment(self, spatial_resolution='country', sentiment_engine="vader"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: a dictionary that represents the tweet sentiments across the spatial units regarding the selected sentiment engine. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the sentiment scores in all the tweets that are posted within every spatial unit.
        """

        assert (spatial_resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"

        sentiments = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            sentiments[location] = {}
            sentiment_results = []
            for tweet in tweets:
                sentiment_results.append(tweet.sentiment_analysis(sentiment_engine))
            for result in sentiment_results:
                for score in result:
                    sentiments[location][score] = sentiments[location].get(score, []) + [float(result[score])]

            for score in sentiments[location]:
                scores = sentiments[location][score]
                sentiments[location][score] = {}
                sentiments[location][score]["average"] = np.nanmean(scores)
                sentiments[location][score]["max"] = np.nanmax(scores)
                sentiments[location][score]["min"] = np.nanmin(scores)
                sentiments[location][score]["stdev"] = np.nanstd(scores)
                sentiments[location][score]["median"] = np.nanmedian(scores)
        return sentiments