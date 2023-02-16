import numpy as np
import textstat
from scipy.stats import gmean, hmean, kurtosis, skew
from numpy import amin, amax, std, var, quantile, mean, ptp, median
from statistics import mode

from tweet_text_analysis import TweetTextAnalysis


class MassContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name, retweet_flag=False, quote_flag=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()
        self._retweet_flag = retweet_flag
        self._quote_flag = quote_flag

        #https://www.ibm.com/docs/en/spss-statistics/25.0.0?topic=summarize-statistics
        #https://www.ucd.ie/msc/t4media/Mean%20and%20Standard%20Deviation.pdf

        self._statistics = {"geometric_mean": lambda x: f"gmean({x})", "harmonic_mean": lambda x: f"hmean({x})",
                            "kurtosis": lambda x: f"kurtosis({x})", "maximum": lambda x: f"amax({x})",
                            "mean": lambda x: f"mean({x})", "median": lambda x: f"median({x})",
                            "minimum": lambda x: f"amin({x})", "range": lambda x: f"ptp({x})",
                            "skewness": lambda x: f"skew({x})", "standard_deviation": lambda x: f"std({x})",
                            "variance": lambda x: f"var({x})", "mode": lambda x: f"mode({x})",
                            "25% quantile": lambda x: f"quantile({x}, 0.25)",
                            "75% quantile": lambda x: f"quantile({x}, 0.75)", }

    def tweets_character_count_statistics(self):
        tweets_character_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            tweets_character_count_array.append(twt_text_length)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_character_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_character_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_character_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_character_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_word_count_statistics(self):
        tweets_words_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            tweets_words_count_array.append(twt_text_length)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_word_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_word_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_word_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_words_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_sentence_count_statistics(self):
        tweets_sentence_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="sentence")
            tweets_sentence_count_array.append(twt_text_length)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_sentence_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_sentence_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_sentence_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_sentence_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_syllables_count_statistics(self):
        tweets_syllables_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            tweets_syllables_count_array += [textstat.syllable_count(i, lang='en_US') for i in self._text_analysis.tweet_splitter(split_unit="word", input_text=twt_txt)]

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_syllables_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_syllables_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_syllables_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_syllables_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_word_length_statistics(self):
        tweets_word_length_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            tweets_word_length_array += [len(word) for word in self._text_analysis.tweet_splitter(split_unit="word", input_text=twt_txt)]

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_word_length_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_word_length_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_word_length_statistics_" + metric

            metric_function = self._statistics[metric](tweets_word_length_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_sentence_length_statistics(self):
        tweets_sentence_length_statistics = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            tweets_sentence_length_statistics += [len(self._text_analysis.tweet_splitter(split_unit="word", input_text=sentence)) for sentence in self._text_analysis.tweet_splitter(split_unit="sentence", input_text=twt_txt)]

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_sentence_length_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_sentence_length_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_sentence_length_statistics_" + metric

            metric_function = self._statistics[metric](tweets_sentence_length_statistics)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_character_count_statistics(self):
        tweets_lowercase_character_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_character_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            tweets_lowercase_character_count_array.append(twt_lowercase_character_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_character_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_character_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_character_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_character_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_uppercase_character_count_statistics(self):
        tweets_uppercase_character_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_character_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="character")
            tweets_uppercase_character_count_array.append(twt_uppercase_character_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_uppercase_character_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_uppercase_character_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_uppercase_character_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_uppercase_character_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_word_count_statistics(self):
        tweets_lowercase_word_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_word_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            tweets_lowercase_word_count_array.append(twt_lowercase_word_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_word_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_word_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_word_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_word_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_uppercase_word_count_statistics(self):
        tweets_uppercase_word_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_word_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="word")
            tweets_uppercase_word_count_array.append(twt_uppercase_word_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_uppercase_word_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_uppercase_word_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_uppercase_word_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_uppercase_word_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_sentence_count_statistics(self):
        tweets_lowercase_sentence_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentence_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            tweets_lowercase_sentence_count_array.append(twt_lowercase_sentence_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_sentence_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_sentence_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_sentence_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_sentence_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_uppercase_sentence_count_statistics(self):
        tweets_uppercase_sentence_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_sentence_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            tweets_uppercase_sentence_count_array.append(twt_uppercase_sentence_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_uppercase_sentence_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_uppercase_sentence_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_uppercase_sentence_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_uppercase_sentence_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweet_lowercase_to_uppercase_characters_fraction_statistics(self):
        tweets_lowercase_to_uppercase_characters_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_characters_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            twt_uppercase_characters_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="character")
            twt_lowercase_to_uppercase_characters_fraction = twt_lowercase_characters_count / twt_uppercase_characters_count if twt_uppercase_characters_count != 0 else None
            tweets_lowercase_to_uppercase_characters_fraction_array.append(twt_lowercase_to_uppercase_characters_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_characters_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_characters_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_characters_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_uppercase_characters_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweet_lowercase_to_uppercase_words_fraction_statistics(self):
        tweets_lowercase_to_uppercase_words_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_words_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            twt_uppercase_words_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="word")
            twt_lowercase_to_uppercase_words_fraction = twt_lowercase_words_count / twt_uppercase_words_count if twt_uppercase_words_count != 0 else None
            tweets_lowercase_to_uppercase_words_fraction_array.append(twt_lowercase_to_uppercase_words_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_words_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_words_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_words_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_uppercase_words_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweet_lowercase_to_uppercase_sentences_fraction_statistics(self):
        tweets_lowercase_to_uppercase_sentences_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentences_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            twt_uppercase_sentences_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            twt_lowercase_to_uppercase_sentences_fraction = twt_lowercase_sentences_count / twt_uppercase_sentences_count if twt_uppercase_sentences_count != 0 else None
            tweets_lowercase_to_uppercase_sentences_fraction_array.append(twt_lowercase_to_uppercase_sentences_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_sentences_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_sentences_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_sentences_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_uppercase_sentences_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_to_all_characters_fraction_statistics(self):
        tweets_lowercase_to_all_characters_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_characters_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            twt_lowercase_to_uppercase_sentences_fraction = twt_lowercase_characters_count / twt_characters_count if twt_characters_count != 0 else None
            tweets_lowercase_to_all_characters_fraction_array.append(twt_lowercase_to_uppercase_sentences_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_to_all_characters_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_to_all_characters_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_to_all_characters_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_all_characters_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_to_all_words_fraction_statistics(self):
        tweets_lowercase_to_all_words_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_words_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            twt_words_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            twt_lowercase_to_uppercase_words_fraction = twt_lowercase_words_count / twt_words_count if twt_words_count != 0 else None
            tweets_lowercase_to_all_words_fraction_array.append(twt_lowercase_to_uppercase_words_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_to_all_words_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_to_all_words_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_to_all_words_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_all_words_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_lowercase_to_all_sentences_fraction_statistics(self):
        tweets_lowercase_to_all_sentences_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentences_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            twt_sentences_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="sentence")
            twt_lowercase_to_uppercase_sentences_fraction = twt_lowercase_sentences_count / twt_sentences_count if twt_sentences_count != 0 else None
            tweets_lowercase_to_all_sentences_fraction_array.append(twt_lowercase_to_uppercase_sentences_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_lowercase_to_all_sentences_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_lowercase_to_all_sentences_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_lowercase_to_all_sentences_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_lowercase_to_all_sentences_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_exclamation_mark_count_statistics(self):
        tweets_exclamation_mark_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            exclamation_mark_count = self._text_analysis.exclamation_mark_count(input_text=twt_txt)
            tweets_exclamation_mark_count_array.append(exclamation_mark_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_exclamation_mark_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_exclamation_mark_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_exclamation_mark_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_exclamation_mark_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_question_mark_count_statistics(self):
        tweets_question_mark_count_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            question_mark_count = self._text_analysis.question_mark_count(input_text=twt_txt)
            tweets_question_mark_count_array.append(question_mark_count)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_question_mark_count_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_question_mark_count_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_question_mark_count_statistics_" + metric

            metric_function = self._statistics[metric](tweets_question_mark_count_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_exclamation_mark_to_all_characters_fraction_statistics(self):
        tweets_exclamation_mark_to_all_characters_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            exclamation_mark_count = self._text_analysis.exclamation_mark_count(input_text=twt_txt)
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            twt_exclamation_mark_to_all_characters_fraction = exclamation_mark_count / twt_characters_count if twt_characters_count != 0 else None
            tweets_exclamation_mark_to_all_characters_fraction_array.append(twt_exclamation_mark_to_all_characters_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_exclamation_mark_to_all_characters_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_exclamation_mark_to_all_characters_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_exclamation_mark_to_all_characters_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_exclamation_mark_to_all_characters_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_question_mark_to_all_characters_fraction_statistics(self):
        tweets_question_mark_to_all_characters_fraction_array = []
        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            question_mark_count = self._text_analysis.question_mark_count(input_text=twt_txt)
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            twt_question_mark_to_all_characters_fraction = question_mark_count / twt_characters_count if twt_characters_count != 0 else None
            tweets_question_mark_to_all_characters_fraction_array.append(twt_question_mark_to_all_characters_fraction)

        for metric in self._statistics:
            feature_id = max(list(self._features_id_name_dict.keys())) + 1
            if self._retweet_flag:
                self._features_id_name_dict[feature_id] = "retweet_" + "tweets_question_mark_to_all_characters_fraction_statistics_" + metric
            elif self._quote_flag:
                self._features_id_name_dict[feature_id] = "quote_" + "tweets_question_mark_to_all_characters_fraction_statistics_" + metric
            else:
                self._features_id_name_dict[feature_id] = "tweets_question_mark_to_all_characters_fraction_statistics_" + metric

            metric_function = self._statistics[metric](tweets_question_mark_to_all_characters_fraction_array)

            for tweet in self._tweets_collection:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = eval(metric_function)

    def tweets_abbreviation_count_statistics(self):
        pass

    def tweets_abbreviation_to_all_words_fraction_statistics(self):
        pass

    def tweets_vulgar_count_statistics(self):
        pass

    def tweets_vulgar_to_all_words_fraction_statistics(self):
        pass

    def tweets_pos_tags_count_statistics(self):
        pass

    def tweets_ner_tags_count_statistics(self):
        pass

    def tweets_pronouns_count_statistics(self):
        pass

    def tweets_first_singular_pronoun_count_statistics(self):
        pass

    def tweets_first_plural_pronoun_count_statistics(self):
        pass

    def tweets_second_singular_pronoun_count_statistics(self):
        pass

    def tweets_second_plural_pronoun_count_statistics(self):
        pass

    def tweets_third_singular_pronoun_count_statistics(self):
        pass

    def tweets_third_plural_pronoun_count_statistics(self):
        pass

    def tweets_flesch_reading_ease_readability_score_statistics(self):
        pass

    def tweets_flesch_kincaid_grade_readability_score_statistics(self):
        pass

    def tweets_gunning_fog_readability_score_statistics(self):
        pass

    def tweets_smog_index_readability_score_statistics(self):
        pass

    def tweets_automated_readability_index_readability_score_statistics(self):
        pass

    def tweets_coleman_liau_index_readability_score_statistics(self):
        pass

    def tweets_linsear_write_formula_readability_score_statistics(self):
        pass

    def tweets_dale_chall_readability_score_readability_score_statistics(self):
        pass

    def tweets_subjectivity_score_statistics(self):
        pass

    def tweets_polarity_score_statistics(self):
        pass

    def tweets_positivity_score_by_vader_statistics(self):
        pass

    def tweets_negativity_score_by_vader_statistics(self):
        pass

    def tweets_neutrality_score_by_vader_statistics(self):
        pass

    def tweets_compound_sentiment_score_by_vader_statistics(self):
        pass

    def tweets_nrc_emotions_score_statistics(self):
        pass

    def tweets_vad_sentiment_score_statistics(self):
        pass








    def tweets_language_fraction(self):
        pass

    def tweets_tf_idf(self):
        """
        This function measures tf-idf for every tweet in the dataset. Tf-idf is the result of elementwise product
         of tf and idf vector. Tf vector of a tweet shows the frequency of each tweet term in that tweet. Df vector
         of each tweet shows every token of a tweet occurs in how many of the tweets in the dataset. After making
         df vector for every tweet, we can build corresponding idf vector by calculating log(N/df_term) for every term
         where N is the total number of terms in each tweet.
        :return: a dictionary that maps every tweet_id to its tf-idf vector.
        """
        tweet_tokens = {}
        term_space = set()

        for tweet_id in tqdm(self.tweets):
            tokens = self.tweets[tweet_id].tweet_tokens()
            tweet_tokens[tweet_id] = tokens
            for token in tokens:
                term_space.add(token)

        tf = {}
        for tweet_id, tokens in tweet_tokens.items():
            tf[tweet_id] = {}
            for term in tokens:
                tf[tweet_id][term] = tf[tweet_id].get(term, 0) + 1

        df = {}
        for tweet_id, tokens in tf.items():
            # tmp = {p: 0 for p in tokens}
            df[tweet_id] = {}
            for token in set(tokens):
                for tweet_id2 in tf:
                    if token in tf[tweet_id2]:
                        df[tweet_id][token] = df[tweet_id].get(token, 0) + 1

        tf_idf = {}
        for tweet_id in tf:
            tf_idf[tweet_id] = {}
            for token in tf[tweet_id]:
                tf_idf[tweet_id][token] = tf[tweet_id][token] * np.log(len(df) / df[tweet_id][token])
        return tf_idf

    def tweets_pos_tf_idf(self):
        """
        This function measures tf-idf for tweet text part-of-speech (POS). Measuring pos_tf_idf is slightly different
        from ordinary tf-idf . In pos_tf_idf, instead of tweet texts, all the operations are performed on tweet text
        part-of-speech (POS).
        :return: a dictionary that maps every tweet_id to the tf-idf vector of its POS.
        """

        pos_dict = {}
        pos_space = set()

        for tweet_id in self.tweets:
            tokens = self.tweets[tweet_id].tweet_tokens(input_text=self.tweets[tweet_id].tweet_pos())
            pos_dict[tweet_id] = tokens
            for token in tokens:
                pos_space.add(token)

        tf = {}
        for tweet_id, tokens in pos_dict.items():
            # tmp = {p:0 for p in pos_space}
            tf[tweet_id] = {}
            for term in tokens:
                tf[tweet_id][term] = tf[tweet_id].get(term, 0) + 1

        df = {}
        for tweet_id, tokens in tf.items():
            df[tweet_id] = {}
            for token in tokens:
                for tweet_id2 in tf:
                    # tf_tweet_id2 = [w for w in tf[tweet_id2] if tf[tweet_id2][w]!=0]
                    # If we put tf instead of post_dict then df for every pos would be the same (becasue in tf all the pos are available)
                    if token in tf[tweet_id2]:
                        df[tweet_id][token] = df[tweet_id].get(token, 0) + 1

        tf_idf = {}
        for tweet_id in tf:
            tf_idf[tweet_id] = {}
            for token in tf[tweet_id]:
                tf_idf[tweet_id][token] = tf[tweet_id][token] * np.log(len(df) / df[tweet_id][token])
        return tf_idf

    def tf_idf_dimension_balancer(self, tf_idf):
        """
        This function equalise the dimension of tweets tf-idf vectors. To this end, it pulls all the tweets distinct tokens
        and makes a d dimensional (d:number of distinct tokens) space. In this space, all tf-idf vectors have the same
        dimension.
        :param tf_idf: a dictionary that maps every tweet_id to its corresponding tf-idf vector
        :return: a dictionary that maps every tweet_id to its corresponding tf-idf vector. All tweets have the same dimension.
        """
        tfidf = {}
        term_space = set()

        for tweet_id in tf_idf:
            for token in tf_idf[tweet_id]:
                term_space.add(token)

        for tweet_id in tf_idf:
            tfidf[tweet_id] = {}
            # temp = {p:0 for p in term_space}
            # for element in tfidf[tweet_id]:
            # vec = {}
            for term in term_space:
                tfidf[tweet_id][term] = tf_idf[tweet_id].get(term, 0)
                # temp[element] = tfidf[tweet_id][element]
            # tfidf[tweet_id] = vec
        return tfidf

    def tweets_ner_tf_idf(self):
        pass

    def tweets_emojis_histogram(self):
        """
        This function counts the frequency of different emojis in the dataset.
        :return: a sorted dictionary that shows the frequency of different emojis.
        """
        emojis_histogram = {}
        for tweet_id in self.tweets:
            emojis = self.tweets[tweet_id].get_emojis(count=False)
            if len(emojis) != 0:
                for emoji in emojis:
                    emojis_histogram[emoji["emoji"]] = emojis_histogram.get(emoji["emoji"], 0) + 1
        return {m[0]: m[1] for m in sorted(emojis_histogram.items(), key=lambda p: p[1], reverse=True)}

    def tweets_emoticons_histogram(self):
        """
        This function counts the frequency of different emoticons in the dataset.
        :return: a sorted dictionary that shows the frequency of different emoticons.
        """
        emoticons_histogram = {}
        for tweet_id in self.tweets:
            emoticons = self.tweets[tweet_id].get_emoticon(count=False)
            if len(emoticons) != 0:
                for emoticon in emoticons:
                    emoticons_histogram[emoticon] = emoticons_histogram.get(emoticon, 0) + 1
        return {m[0]: m[1] for m in sorted(emoticons_histogram.items(), key=lambda p: p[1], reverse=True)}

    def tweets_count(self):
        """
        This function count the number of tweets in the dataset.
        :return: an integer showing the number of tweets in the dataset.
        """
        return len(self.tweets)








#bag of words
#tf-idf
