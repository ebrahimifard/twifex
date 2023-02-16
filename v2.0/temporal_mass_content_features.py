from tweet_text_analysis import TweetTextAnalysis


class TemporalMassContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()


    def tweet_complexity_change(self, nodes, complexity_unit="word"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param complexity_unit: the unit of analysis for measuring tweet complexity. It can be "word", "sentence", or "syllables".
        :return: a dictionary that represents the change of the tweet complexity across the timespan of the dataset
        due to selected unit of analysis. The key-value pair in this dictionary corresponds to
        the timestamps and the statistical metrics of the tweet complexity scores in all the tweets that are posted
        within every timestamp.
        """

        assert (complexity_unit in ["word", "sentence",
                         "syllables"]), "The unit of analysis has to be word, sentence, or syllables"

        complexity = {}
        for time_frame, tweets in nodes.items():
            complexity[time_frame] = []
            complexity_results = []
            for tweet in tweets:
                complexity_results.append(tweet.text_complexity(complexity_unit=complexity_unit))
            for result in complexity_results:
                complexity[time_frame] = complexity.get(time_frame, []) + [float(result)]

            scores = complexity[time_frame]
            complexity[time_frame] = {}
            if len(scores) > 0:
                complexity[time_frame]["average"] = np.nanmean(scores)
                complexity[time_frame]["max"] = np.nanmax(scores)
                complexity[time_frame]["min"] = np.nanmin(scores)
                complexity[time_frame]["stdev"] = np.nanstd(scores)
                complexity[time_frame]["median"] = np.nanmedian(scores)
            else:
                complexity[time_frame]["average"] = np.nan
                complexity[time_frame]["max"] = np.nan
                complexity[time_frame]["min"] = np.nan
                complexity[time_frame]["stdev"] = np.nan
                complexity[time_frame]["median"] = np.nan
        return complexity

    def tweet_readability_change(self, nodes, readability_metric="flesch_kincaid_grade"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score"
        :return: a dictionary that represents the change of the tweet readability across the timespan of the dataset
        due to selected readability metric. The key-value pair in this dictionary corresponds to the timestamps and
        the statistical metrics of the tweet readability scores in all the tweets that are posted within every timestamp.
        """

        assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        readability = {}
        for time_frame, tweets in nodes.items():
            readability[time_frame] = []
            readability_results = []
            for tweet in tweets:
                readability_results.append(tweet.readability(readability_metric=readability_metric))
            for result in readability_results:
                readability[time_frame] = readability.get(time_frame, []) + [float(result)]

            scores = readability[time_frame]
            readability[time_frame] = {}
            if len(scores) > 0:
                readability[time_frame]["average"] = np.nanmean(scores)
                readability[time_frame]["max"] = np.nanmax(scores)
                readability[time_frame]["min"] = np.nanmin(scores)
                readability[time_frame]["stdev"] = np.nanstd(scores)
                readability[time_frame]["median"] = np.nanmedian(scores)
            else:
                readability[time_frame]["average"] = np.nan
                readability[time_frame]["max"] = np.nan
                readability[time_frame]["min"] = np.nan
                readability[time_frame]["stdev"] = np.nan
                readability[time_frame]["median"] = np.nan
        return readability

    def tweet_length_change(self, nodes, length_unit="word"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param length_unit: the unit of analysis for measuring tweet length. It can be "character", "word", or "sentence".
        :return: a dictionary that represents the change of the tweet length across the timespan of the dataset
        due to selected unit of analysis. The key-value pair in this dictionary corresponds to the timestamps and
        the statistical metrics of the tweet length in all the tweets that are posted within every timestamp.
        """

        assert (length_unit in ["character", "word", "sentence"]), "The unit has to be character, word, or sentence"

        tweet_length = {}
        for time_frame, tweets in nodes.items():
            tweet_length[time_frame] = []
            tweet_length_results = []
            for tweet in tweets:
                tweet_length_results.append(tweet.text_length(length_unit=length_unit))
            for result in tweet_length_results:
                tweet_length[time_frame] = tweet_length.get(time_frame, []) + [float(result)]

            scores = tweet_length[time_frame]
            tweet_length[time_frame] = {}
            if len(scores) > 0:
                tweet_length[time_frame]["average"] = np.nanmean(scores)
                tweet_length[time_frame]["max"] = np.nanmax(scores)
                tweet_length[time_frame]["min"] = np.nanmin(scores)
                tweet_length[time_frame]["stdev"] = np.nanstd(scores)
                tweet_length[time_frame]["median"] = np.nanmedian(scores)
                tweet_length[time_frame]["median"] = np.nanmedian(scores)
            else:
                tweet_length[time_frame]["average"] = np.nan
                tweet_length[time_frame]["max"] = np.nan
                tweet_length[time_frame]["min"] = np.nan
                tweet_length[time_frame]["stdev"] = np.nan
                tweet_length[time_frame]["median"] = np.nan
                tweet_length[time_frame]["median"] = np.nan
        return tweet_length

    def tweet_count_change(self, nodes):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :return: a dictionary that represents the change of the tweet count across the timespan of the dataset.
        The key-value pair in this dictionary corresponds to the timestamps and
        the number of tweets that are posted within every timestamp.
        """

        tweet_count = {}
        for time_frame, tweets in nodes.items():
            tweet_count[time_frame] = len(tweets)
        return tweet_count

    def sentiment_change(self, nodes, sentiment_engine="vader"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: a dictionary that represents the change of the sentiment across the timespan of the dataset
        due to selected sentiment engine. The key-value pair in this dictionary corresponds to
        the timestamps and the statistical metrics of the sentiment scores in all the tweets that are posted
        within every timestamp.
        """

        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"
        sentiments = {}
        for time_frame, tweets in nodes.items():
            sentiments[time_frame] = {}
            sentiment_results = []
            for tweet in tweets:
                sentiment_results.append(tweet.sentiment_analysis(sentiment_engine))
            for result in sentiment_results:
                for score in result:
                    sentiments[time_frame][score] = sentiments[time_frame].get(score, []) + [float(result[score])]

            for score in sentiments[time_frame]:
                scores = sentiments[time_frame][score]
                sentiments[time_frame][score] = {}
                sentiments[time_frame][score]["average"] = np.nanmean(scores)
                sentiments[time_frame][score]["max"] = np.nanmax(scores)
                sentiments[time_frame][score]["min"] = np.nanmin(scores)
                sentiments[time_frame][score]["stdev"] = np.nanstd(scores)
                sentiments[time_frame][score]["median"] = np.nanmedian(scores)
        return sentiments