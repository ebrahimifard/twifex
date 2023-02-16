from tweet_text_analysis import TweetTextAnalysis


class TemporalSpatialMassContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    def temporal_spatial_tweets(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that classifies a set of tweets into a hierarchical structure in which the key-value corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be all tweets corresponding to the location and timestamp.
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

    def temporal_spatial_tweet_complexity(self, order='spatial-temporal', temporal_resolution='day',
                                          temporal_frequency=1, spatial_resolution='country', complexity_unit="word"):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param complexity_unit: the unit of analysis for measuring tweet complexity. It can be "word", "sentence", or "syllables".
        :return: an embedded dictionary that represents the tweet complexity across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the tweet complexity scores in all the tweets that are posted
        within every timeframe and spatial unit.
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
        assert (complexity_unit in ["word", "sentence",
                         "syllables"]), "The unit of analysis has to be word, sentence, or syllables"




        complexity = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            complexity[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                complexity[layer1][layer2] = []
                for tweet in tweets:
                    complexity[layer1][layer2] = complexity[layer1].get(layer2, []) + [float(tweet.text_complexity(complexity_unit=complexity_unit))]

                scores = complexity[layer1][layer2]
                complexity[layer1][layer2] = {}
                if len(scores) > 0:
                    complexity[layer1][layer2]["average"] = np.nanmean(scores)
                    complexity[layer1][layer2]["max"] = np.nanmax(scores)
                    complexity[layer1][layer2]["min"] = np.nanmin(scores)
                    complexity[layer1][layer2]["stdev"] = np.nanstd(scores)
                    complexity[layer1][layer2]["median"] = np.nanmedian(scores)
                    complexity[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    complexity[layer1][layer2]["average"] = np.nan
                    complexity[layer1][layer2]["max"] = np.nan
                    complexity[layer1][layer2]["min"] = np.nan
                    complexity[layer1][layer2]["stdev"] = np.nan
                    complexity[layer1][layer2]["median"] = np.nan
                    complexity[layer1][layer2]["sum"] = np.nan
                complexity[layer1][layer2]["count"] = len(scores)

        return complexity

    def temporal_spatial_tweet_readability(self, order='spatial-temporal', temporal_resolution='day',
                                           temporal_frequency=1, spatial_resolution='country',
                                           readability_metric="flesch_kincaid_grade"):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
        :return: an embedded dictionary that represents the tweet readability across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the tweet readability scores in all the tweets that are posted
        within every timeframe and spatial unit.
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
        assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        readability = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            readability[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                readability[layer1][layer2] = []
                for tweet in tweets:
                    readability[layer1][layer2] = readability[layer1].get(layer2, []) + [float(tweet.readability(readability_metric=readability_metric))]

                scores = readability[layer1][layer2]
                readability[layer1][layer2] = {}
                if len(scores) > 0:
                    readability[layer1][layer2]["average"] = np.nanmean(scores)
                    readability[layer1][layer2]["max"] = np.nanmax(scores)
                    readability[layer1][layer2]["min"] = np.nanmin(scores)
                    readability[layer1][layer2]["stdev"] = np.nanstd(scores)
                    readability[layer1][layer2]["median"] = np.nanmedian(scores)
                    readability[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    readability[layer1][layer2]["average"] = np.nan
                    readability[layer1][layer2]["max"] = np.nan
                    readability[layer1][layer2]["min"] = np.nan
                    readability[layer1][layer2]["stdev"] = np.nan
                    readability[layer1][layer2]["median"] = np.nan
                    readability[layer1][layer2]["sum"] = np.nan
                readability[layer1][layer2]["count"] = len(scores)

        return readability

    def temporal_spatial_tweet_length(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                      spatial_resolution='country', length_unit="word"):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param length_unit: the unit of analysis for measuring tweet length. It can be "character", "word", or "sentence".
        :return: an embedded dictionary that represents the tweet length across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the length in all the tweets that are posted
        within every timeframe and spatial unit.
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
        assert (length_unit in ["character", "word", "sentence"]), "The unit has to be character, word, or sentence"

        tweet_length = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            tweet_length[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                tweet_length[layer1][layer2] = []
                for tweet in tweets:
                    tweet_length[layer1][layer2] = tweet_length[layer1].get(layer2, []) + [float(tweet.text_length(length_unit=length_unit))]

                scores = tweet_length[layer1][layer2]
                tweet_length[layer1][layer2] = {}
                if len(scores) > 0:
                    tweet_length[layer1][layer2]["average"] = np.nanmean(scores)
                    tweet_length[layer1][layer2]["max"] = np.nanmax(scores)
                    tweet_length[layer1][layer2]["min"] = np.nanmin(scores)
                    tweet_length[layer1][layer2]["stdev"] = np.nanstd(scores)
                    tweet_length[layer1][layer2]["median"] = np.nanmedian(scores)
                    tweet_length[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    tweet_length[layer1][layer2]["average"] = np.nan
                    tweet_length[layer1][layer2]["max"] = np.nan
                    tweet_length[layer1][layer2]["min"] = np.nan
                    tweet_length[layer1][layer2]["stdev"] = np.nan
                    tweet_length[layer1][layer2]["median"] = np.nan
                    tweet_length[layer1][layer2]["sum"] = np.nan
                tweet_length[layer1][layer2]["count"] = len(scores)

        return tweet_length

    def temporal_spatial_tweet_count(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                     spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that represents the number of tweets across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the number of tweets that are posted
        within every timeframe and spatial unit.
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

        tweet_count = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            tweet_count[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                tweet_count[layer1][layer2] = len(tweets)
        return tweet_count

    def temporal_spatial_tweet_sentiment(self, order='spatial-temporal', temporal_resolution='day',
                                         temporal_frequency=1, spatial_resolution='country', sentiment_engine="vader"):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: an embedded dictionary that represents the tweets sentiment across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the sentiment scores in all the tweets that are posted
        within every timeframe and spatial unit.
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
        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"

        sentiments = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            sentiments[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                sentiments[layer1][layer2] = {}
                sentiment_results = []
                for tweet in tweets:
                    sentiment_results.append(tweet.sentiment_analysis(sentiment_engine))
                for result in sentiment_results:
                    for score in result:
                        sentiments[layer1][layer2][score] = sentiments[layer1][layer2].get(score, []) + [float(result[score])]

                for score in sentiments[layer1][layer2]:
                    scores = sentiments[layer1][layer2][score]
                    sentiments[layer1][layer2][score] = {}
                    sentiments[layer1][layer2][score]["average"] = np.nanmean(scores)
                    sentiments[layer1][layer2][score]["max"] = np.nanmax(scores)
                    sentiments[layer1][layer2][score]["min"] = np.nanmin(scores)
                    sentiments[layer1][layer2][score]["stdev"] = np.nanstd(scores)
                    sentiments[layer1][layer2][score]["median"] = np.nanmedian(scores)
                    sentiments[layer1][layer2][score]["sum"] = np.nansum(scores)
                    sentiments[layer1][layer2][score]["count"] = len(scores)
        return sentiments

    def temporal_spatial_tweet_likes_count(self, order='spatial-temporal', temporal_resolution='day',
                                           temporal_frequency=1, spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that represents the number of tweet likes across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the likes count in all the tweets that are posted
        within every timeframe and spatial unit.
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

        tweet_likes = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            tweet_likes[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                tweet_likes[layer1][layer2] = []
                for tweet in tweets:
                    tweet_likes[layer1][layer2] = tweet_likes[layer1].get(layer2, []) + [float(tweet.get_likes_count())]

                scores = tweet_likes[layer1][layer2]
                tweet_likes[layer1][layer2] = {}
                if len(scores) > 0:
                    tweet_likes[layer1][layer2]["average"] = np.nanmean(scores)
                    tweet_likes[layer1][layer2]["max"] = np.nanmax(scores)
                    tweet_likes[layer1][layer2]["min"] = np.nanmin(scores)
                    tweet_likes[layer1][layer2]["stdev"] = np.nanstd(scores)
                    tweet_likes[layer1][layer2]["median"] = np.nanmedian(scores)
                    tweet_likes[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    tweet_likes[layer1][layer2]["average"] = np.nan
                    tweet_likes[layer1][layer2]["max"] = np.nan
                    tweet_likes[layer1][layer2]["min"] = np.nan
                    tweet_likes[layer1][layer2]["stdev"] = np.nan
                    tweet_likes[layer1][layer2]["median"] = np.nan
                    tweet_likes[layer1][layer2]["sum"] = np.nan
                tweet_likes[layer1][layer2]["count"] = len(scores)

        return tweet_likes

    def temporal_spatial_tweet_retweet_count(self, order='spatial-temporal', temporal_resolution='day',
                                             temporal_frequency=1, spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that represents the number of retweets across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the retweets count in all the tweets that are posted
        within every timeframe and spatial unit.
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

        retweets = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            retweets[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                retweets[layer1][layer2] = []
                for tweet in tweets:
                    retweets[layer1][layer2] = retweets[layer1].get(layer2, []) + [float(tweet.get_retweet_count())]

                scores = retweets[layer1][layer2]
                retweets[layer1][layer2] = {}
                if len(scores) > 0:
                    retweets[layer1][layer2]["average"] = np.nanmean(scores)
                    retweets[layer1][layer2]["max"] = np.nanmax(scores)
                    retweets[layer1][layer2]["min"] = np.nanmin(scores)
                    retweets[layer1][layer2]["stdev"] = np.nanstd(scores)
                    retweets[layer1][layer2]["median"] = np.nanmedian(scores)
                    retweets[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    retweets[layer1][layer2]["average"] = np.nan
                    retweets[layer1][layer2]["max"] = np.nan
                    retweets[layer1][layer2]["min"] = np.nan
                    retweets[layer1][layer2]["stdev"] = np.nan
                    retweets[layer1][layer2]["median"] = np.nan
                    retweets[layer1][layer2]["sum"] = np.nan
                retweets[layer1][layer2]["count"] = len(scores)

        return retweets

    def temporal_spatial_tweet_language(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                        spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that represents the distribution of tweets language across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the distribution of languages in all the tweets that are posted
        within every timeframe and spatial unit.
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

        languages = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            languages[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                languages[layer1][layer2] = []
                for tweet in tweets:
                    languages[layer1][layer2] = languages[layer1].get(layer2, []) + [tweet.get_language()]
                scores = languages[layer1][layer2]
                lang_agg = {}
                for i in scores:
                    lang_agg[i] = lang_agg.get(i, 0) + 1

                languages[layer1][layer2] = lang_agg

        return languages

    def temporal_spatial_tweet_emojis(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                      spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: an embedded dictionary that represents the distribution of tweets emojis across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the distribution of emojis in all the tweets that are posted
        within every timeframe and spatial unit.
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

        tweet_emojis = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            tweet_emojis[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                tweet_emojis[layer1][layer2] = []
                for tweet in tweets:
                    emoji_list = []
                    for emj in tweet.get_emojis(count=False):
                        emoji_list += emj["emoji"]
                    tweet_emojis[layer1][layer2] = tweet_emojis[layer1].get(layer2, []) + emoji_list

                scores = tweet_emojis[layer1][layer2]
                emojis_agg = {}
                for i in scores:
                    emojis_agg[i] = emojis_agg.get(i, 0) + 1

                tweet_emojis[layer1][layer2] = emojis_agg

        return tweet_emojis

    def temporal_spatial_tweet_case_analysis(self, order='spatial-temporal', temporal_resolution='day',
                                             temporal_frequency=1, spatial_resolution='country',
                                             unit_of_analysis='character'):

        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal", then the first key would be a location and the second one is a timestamp. Otherwise and if the valuse of this parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param unit_of_analysis: the unit parameter can be word or character.
        :return: an embedded dictionary that represents the number of uppercase and lowercase characters or small and capital words (depending on the unit of analysis) across the temporal and spatial units regarding the selected display order. The key-value pair corresponds to a location (or a timestamp depending on the value of "order" parameter) and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be the statistical metrics of the number of uppercase and lowercase characters or small and capital words in all the tweets that are posted
        within every timeframe and spatial unit.
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
        assert (unit_of_analysis in ["character", "word"]), "unit can be character or word"

        tweet_case_analysis = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution, temporal_frequency=temporal_frequency, spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            tweet_case_analysis[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                tweet_case_analysis[layer1][layer2] = {}
                case_analysis_results = []
                for tweet in tweets:
                    case_analysis_results.append(tweet.case_analysis(frac=False, unit_of_analysis=unit_of_analysis))
                for result in case_analysis_results:
                    for score in result:
                        tweet_case_analysis[layer1][layer2][score] = tweet_case_analysis[layer1][layer2].get(score, []) + [float(result[score])]

                for score in tweet_case_analysis[layer1][layer2]:
                    scores = tweet_case_analysis[layer1][layer2][score]
                    tweet_case_analysis[layer1][layer2][score] = {}
                    tweet_case_analysis[layer1][layer2][score]["average"] = np.nanmean(scores)
                    tweet_case_analysis[layer1][layer2][score]["max"] = np.nanmax(scores)
                    tweet_case_analysis[layer1][layer2][score]["min"] = np.nanmin(scores)
                    tweet_case_analysis[layer1][layer2][score]["stdev"] = np.nanstd(scores)
                    tweet_case_analysis[layer1][layer2][score]["median"] = np.nanmedian(scores)
                    tweet_case_analysis[layer1][layer2][score]["sum"] = np.nansum(scores)
        return tweet_case_analysis
