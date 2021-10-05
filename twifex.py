#!/usr/bin/env python
# coding: utf-8

# In[71]:

############################################# Packages #############################################
import json
import copy
import requests
from pprint import pprint
from urlextract import URLExtract
import textstat
import os
import networkx as nx
import emoji
import re
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from hatesonar import Sonar
import pandas as pd
import datetime
from textblob import TextBlob
import community  # pip install python-louvain
from tqdm import tqdm

from nltk import PorterStemmer
# import nltk

import spacy
import en_core_web_sm

from dateutil.relativedelta import *
from bs4 import BeautifulSoup

import wordninja
from itertools import combinations


############################################# Packages #############################################


############################################# Notes and Comments #############################################
# ### Things that need to be fixed:
# - Exception handling
#     - For thise tweets that do not have media field in their entities
#     - For all the divisions (division by zero error)
#     - TO ALL the QUOTE TWEETS => EXCEPTION HANDLING IN CASE THERE IS NO QUOTE
#     - TO ALL the retweet TWEETS => EXCEPTION HANDLING IN CASE THERE IS NO retweet
#     - temporal network of tweets emergence
#     - adding different layers
#     - save in different formats
#     - creating dynamic network
#     - user profile face recognition
#     - user network
#     - Reply network
#     - change the community detection function signiture/ add the parameters / adding the directed version
#     - eigen vector centrality doesn't converge! think about it!
#     - components number is only implemented for undircedted graph! See, how much it influences the whole model
#     - In the user network you should take into account the difference between an account with only one single tweet and account with mu;ltiple tweet
#     - Adding botometer to User?
#     - Remove whatever that is related to hatesonar
#     - Add some dictionaries/models on state of the art of hate speech/offensive language/toxicity
#     - Add dictionaries/models related to sarcasm/humour/irony detection
#     - Add dictionaries/models related to patriotism detection
#     - Add dictionaries/models related to patriotism detection
#     - Add dictionaries/models related to patronizing and condescending language detection
#     - Add dictionaries/models related to aspect-based sentiment analysis
#     - Add dictionaries/models related to persuasive language detection
#     - Add dictionaries/models related to metaphor detection
# memotion (meme emotion)?
#       - the spatial units of analysis are place and country. How are they different? Explain what is "place"?
#       - Why don't we have resolution parameter for get account age function? and it only calculate the age in days?
#       - When we are returning some statistics on for example number of followers or totall likes, why don't we also return "sum" and "count"?

############################################# Notes and Comments #############################################


class TwixUtility:
    def __init__(self):
        pass

    @staticmethod
    def levenshtein_distance(self, text1, text2):
        """
        This function measures the levenshtein distance between two tweet texts given in the arguments.
        :param text1: the first tweet text.
        :param text2: the second tweet text.
        :return: an integer showing the leveneshtein distance between text1 and text2.
        """

        distance_mat = np.zeros((len(text1) + 1, len(text2) + 1))

        count = 0
        for i in range(len(text1) + 1):
            distance_mat[i][0] = count
            count += 1

        count = 0
        for i in range(len(text2) + 1):
            distance_mat[0][i] = count
            count += 1

        for text1_ind, text1_char in enumerate(text1):
            text1_ind = text1_ind + 1
            for text2_ind, text2_char in enumerate(text2):
                text2_ind = text2_ind + 1
                if text1_char == text2_char:
                    distance_mat[text1_ind][text2_ind] = distance_mat[text1_ind - 1][text2_ind - 1]
                else:
                    distance_mat[text1_ind][text2_ind] = np.min(
                        [distance_mat[text1_ind - 1][text2_ind - 1], distance_mat[text1_ind][text2_ind - 1],
                         distance_mat[text1_ind - 1][text2_ind]]) + 1

        x, y = distance_mat.shape[0] - 1, distance_mat.shape[1] - 1
        return distance_mat[x][y]


class Twix:
    def __init__(self):
        """
        This function builds a Twix object and load the necessary modules and dictionaries
        """
        address_book = {"nrc": "./resource/NRC.txt", "vad": "./resource/BRM-emot-submit.csv",
                        "vul": "./resource/vulgar.txt",
                        "abb": "./resource/abbr.txt", "emot": "./resource/emoticons.txt",
                        "stone_stopwords": "./resource/stopwords(Stone).txt",
                        "nltk_stopwords": "./resource/stopwords(nltk).txt",
                        "corenlp_stopwords": "./resource/stopwords(corenlp).txt",
                        "glascow_stopwords": "./resource/stopwords(glascow).txt"}

        stopwords_dic = {"stone": [word.strip() for word in open(address_book["stone_stopwords"]).readlines()],
                         "nltk": [word.strip() for word in open(address_book["nltk_stopwords"]).readlines()],
                         "corenlp": [word.strip() for word in open(address_book["corenlp_stopwords"]).readlines()],
                         "glascow": [word.strip() for word in open(address_book["glascow_stopwords"]).readlines()]}

        # Initialization of VADER sentiment analysis
        analyser = SentimentIntensityAnalyzer()

        # Initialization of sonar sentiment analysis
        # sonar = Sonar()

        # Initialization of SpaCy
        nlp = en_core_web_sm.load()

        # Initialization of NRC sentiment analysis
        nrc_raw = open(address_book["nrc"]).readlines()
        nrc_dic = {}
        for i in nrc_raw:
            tmp = i.strip().split("\t")
            lemma = tmp[0]
            sentiment = tmp[1]
            score = tmp[2]
            if lemma in nrc_dic.keys():
                nrc_dic[lemma][sentiment] = int(score)
            else:
                nrc_dic[lemma] = {sentiment: int(score)}

        # Initialization of VAD sentiment analysis
        # emotions = pd.DataFrame.from_csv(address_book["vad"]) # This is depreciated
        emotions = pd.read_csv(address_book["vad"])
        emotions = emotions[["Word", "V.Mean.Sum", "A.Mean.Sum", "D.Mean.Sum"]]
        emotions.columns = ["word", "valence", "arousal", "dominance"]
        emotions = emotions.T
        emotions.columns = emotions.loc["word"]
        emotions = emotions.drop(["word"], axis="index")
        vad_dic = pd.DataFrame.to_dict(emotions)

        # Initialization of Vulgar dictionary
        vulgar_words_list = [term.strip() for term in open(address_book["vul"]).readlines()]

        # Initialization of abbreviations dictionary
        abbreviation_list = [term.strip() for term in open(address_book["abb"]).readlines()]

        # Initialization of Emoticon dictionary
        emoticons_dict = [term.strip() for term in open(address_book["emot"]).readlines()]

        # self.params = {"vader": analyser, "nrc": nrc_dic, "sonar": sonar, "vad": vad_dic,
        #                "vulgar": vulgar_words_list, "abbr": abbreviation_list, "stopwords": stopwords_dic,
        #                "spacy": nlp, "emoticons": emoticons_dict}

        self.params = {"vader": analyser, "nrc": nrc_dic, "vad": vad_dic,
                       "vulgar": vulgar_words_list, "abbr": abbreviation_list, "stopwords": stopwords_dic,
                       "spacy": nlp, "emoticons": emoticons_dict}

    def single_tweet(self, path):
        """
        :param path: The path to a tweet json
        :return: A singleTweet object for the tweet json
        """
        return singleTweet(path, self.params)

    def collective_tweets(self, tweets):
        """
        :param tweets: a list of singleTweet objects
        :return: a collectiveTweet object which comprises the list of singleTweet objects
        """
        return collectiveTweets({tweet.get_id(): tweet for tweet in tweets})


class collectiveTweets:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def mass_based_features(self):
        """
        :return: a massBasedFeatures object which comprises the singleTweet objects
        """
        return massBasedFeatures(self.tweets)

    def topology_based_features(self):
        """
        :return: a topologyBasedFeatures object which comprises the singleTweet objects
        """
        return topologyBasedFeatures(self.tweets)  # Shouldn't this be topologyBasedFeatures?


############################################# mass features #############################################

class massBasedFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def time_dependent_features(self):
        """
        :return: an object of massTweetFeatures which comprises the singleTweet objects
        """
        return timeDependentMassFeatures(self.tweets)

    def time_independent_features(self):
        """
        :return: an object of massUserFeatures which comprises the singleTweet objects
        """
        return timeIndependentMassFeatures(self.tweets)


class timeIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def time_independent_location_dependent_mass_features(self):
        return timeIndependentLocationDependentMassFeatures(self.tweets)

    def time_independent_location_independent_mass_features(self):
        return timeIndependentLocationIndependentMassFeatures(self.tweets)


class timeDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def time_dependent_location_dependent_mass_features(self):
        return timeDependentLocationDependentMassFeatures(self.tweets)

    def time_dependent_location_independent_mass_features(self):
        return timeDependentLocationIndependentMassFeatures(self.tweets)


class timeDependentLocationDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationDependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationDependentUserMassFeatures(self.tweets)


class timeDependentLocationIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationIndependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationIndependentUserMassFeatures(self.tweets)


class timeIndependentLocationDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationDependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationDependentUserMassFeatures(self.tweets)


class timeIndependentLocationIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationIndependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationIndependentUserMassFeatures(self.tweets)


class temporalFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweets_period(self):
        """
        :return: a sorted list of tweets creation time
        """
        tweet_dates = []
        for tweet in self.tweets:
            tweet_dates.append(self.tweets[tweet].get_creation_time())
        return sorted(tweet_dates)

    def tweets_in_periods(self, resolution="year", frequency=1):
        """
        :param resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :return: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        """
        assert (resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time resolution " \
                                                                                             "should be year, month, " \
                                                                                             "week, day, hour, minute," \
                                                                                             " or second"

        sorted_tweet_times = self.tweets_period()
        time_frame = sorted_tweet_times[0]
        last = sorted_tweet_times[-1]
        temporal_tweets = {}

        if resolution == "year":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(years=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(years=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "month":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(months=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(months=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "week":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(weeks=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(weeks=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "day":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(days=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(days=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "hour":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(hours=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(hours=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "minute":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(minutes=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(minutes=frequency):
                        temporal_tweets[time_frame].append(tweet)

        elif resolution == "second":
            while (time_frame <= last):
                temporal_tweets[time_frame] = []
                time_frame += relativedelta(seconds=frequency)
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(seconds=frequency):
                        temporal_tweets[time_frame].append(tweet)

        return temporal_tweets


class placeFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweets_with_place(self):
        """
        This function filters out all tweets without geo location.
        :return: a dictionary that maps every geotagged tweet_id to its corresponding singleTweet object
        """
        return {p: q for p, q in self.tweets.items() if q.get_place() != None}

    def tweets_distinct_countries(self):
        """
        This function finds all countries that the tweets in the dataset are comming from.
        :return: return a list of distinct countries.
        """
        tweetsWithPlaces = self.tweets_with_place()
        places = set()
        for tweet_id, tweet in tweetsWithPlaces.items():
            place = tweet.get_place()
            places.add(place["country"])
        return list(places)

    def tweets_distinct_places(self, coordinates=True):
        """
        This function finds all places that the tweets in the dataset are comming from.
        :return: return a list of distinct places.
        """
        tweetsWithPlaces = self.tweets_with_place()
        places_coordinates = {}
        for tweet_id, tweet in tweetsWithPlaces.items():
            place = tweet.get_place()
            places_coordinates[place["full_name"]] = places_coordinates.get(place["full_name"], place["bounding_box"])
        if coordinates:
            return places_coordinates
        else:
            return list(places_coordinates.keys())

    def countries_with_tweets(self):
        """
        This function mapped all the geotagged tweets to their country of origin.
        :return: a dictionary that maps every country to the list of all tweets comming from that country.
        """
        tweetsWithPlaces = self.tweets_with_place()
        countries_dict = {}
        for tweet_id, tweet in tweetsWithPlaces.items():
            countries_dict[tweet.get_place()["country"]] = countries_dict.get(tweet.get_place()["country"], []) + [
                tweet]
        return countries_dict

    def places_with_tweets(self):
        """
        This function mapped all the geotagged tweets to their origin.
        :return: a dictionary that maps every place to the list of all tweets comming from that country.
        """
        tweetsWithPlaces = self.tweets_with_place()
        places_dict = {}
        for tweet_id, tweet in tweetsWithPlaces.items():
            places_dict[tweet.get_place()["full_name"]] = places_dict.get(tweet.get_place()["full_name"], []) + [tweet]
        return places_dict

    def test3(self):
        print("hi from test3")

class timeDependentLocationIndependentTweetMassFeatures(temporalFeatures):
    # def __init__(self, tweets):
    #     self.tweets = tweets
    #     self.nodes = self.tweets_period()
    def tweet_complexity_change(self, nodes, unit="word"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param unit: the unit of analysis for tweet complexity analysis. It can be "word", "sentence", or "syllables".
        :return: a dictionary that represents the change of the tweet complexity across the timespan of the dataset
        due to selected unit of analysis. The key-value pair in this dictionary corresponds to
        the timestamps and the statistical metrics of the tweet complexity scores in all the tweets that are posted
        within every timestamp.
        """

        assert (unit in ["word", "sentence",
                         "syllables"]), "The unit of analysis has to be word, sentence, or syllables"

        complexity = {}
        for time_frame, tweets in nodes.items():
            complexity[time_frame] = []
            complexity_results = []
            for tweet in tweets:
                complexity_results.append(tweet.text_complexity(unit=unit))
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

    def tweet_readability_change(self, nodes, metric="flesch_kincaid_grade"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score"
        :return: a dictionary that represents the change of the tweet readability across the timespan of the dataset
        due to selected readability metric. The key-value pair in this dictionary corresponds to the timestamps and
        the statistical metrics of the tweet readability scores in all the tweets that are posted within every timestamp.
        """

        assert (metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
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
                readability_results.append(tweet.readability(metric=metric))
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

    def tweet_length_change(self, nodes, unit="word"):
        """
        :param nodes: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        :param unit: the unit of analysis for measuring tweet length. It can be "character", "word", or "sentence".
        :return: a dictionary that represents the change of the tweet length across the timespan of the dataset
        due to selected unit of analysis. The key-value pair in this dictionary corresponds to the timestamps and
        the statistical metrics of the tweet length in all the tweets that are posted within every timestamp.
        """

        assert (unit in ["character", "word", "sentence"]), "The unit has to be character, word, or sentence"

        tweet_length = {}
        for time_frame, tweets in nodes.items():
            tweet_length[time_frame] = []
            tweet_length_results = []
            for tweet in tweets:
                tweet_length_results.append(tweet.text_length(unit=unit))
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


class timeDependentLocationIndependentUserMassFeatures(temporalFeatures):
    # def __init__(self, tweets):
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


class timeDependentLocationDependentTweetMassFeatures(temporalFeatures, placeFeatures):
    def test(self):
        print("test")


class timeDependentLocationDependentUserMassFeatures(temporalFeatures, placeFeatures):
    def test(self):
        print("test")


class timeIndependentLocationIndependentTweetMassFeatures:
    def __init__(self, tweets):
        self.tweets = tweets

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


class timeIndependentLocationIndependentUserMassFeatures:
    def __init__(self, tweets):
        self.tweets = tweets

    def users_followers_fraction(self, period=True, threshold=100):
        """
        This function finds the fraction of users whose followers number is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        followers number is equal to threshold, otherwise it counts the number of users whose
        followers number is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of followers.
        :return: a float number that shows the fraction of users whose followers number is equal or greater (depending on period)
        than threshold.
        """
        all_users = self.get_distinct_users()
        target = 0
        for user in all_users:
            if period:
                if user.get_followers_count() >= threshold:
                    target += 1
            else:
                if user.get_followers_count() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def users_friends_fraction(self, period=True, threshold=100):
        """
        This function finds the fraction of users whose friends (followee) number is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        friends number is equal to threshold, otherwise it counts the number of users whose
        friends number is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of friends.
        :return: a float number that shows the fraction of users whose friends number is equal or greater (depending on period)
        than threshold.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if period:
                if user.get_friends_count() >= threshold:
                    target += 1
            else:
                if user.get_friends_count() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def users_role_fraction(self, period=True, threshold=1):
        """
        This function finds the fraction of users whose role is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        role is equal to threshold, otherwise it counts the number of users whose
        role is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of the user role.
        :return: a float number that shows the fraction of users whose role is equal or greater (depending on period)
        than threshold.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if period:
                if user.get_user_role() >= threshold:
                    target += 1
            else:
                if user.get_user_role() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def verified_users_fraction(self):
        """
        This function finds the fraction of verified users in the dataset.
        :return: a float number showing the fraction of verified users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.get_user_verification_status() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_location_fraction(self):
        """
        This function finds the fraction of geolocated users in the dataset.
        :return: a float number showing the fraction of geolocated users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_location() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_photo_fraction(self):
        """
        This function finds the fraction of users with profile picture in the dataset.
        :return: a float number showing the fraction of users with profile picture.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_picture() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_url_fraction(self):
        """
        This function finds the fraction of users with profile url in the dataset.
        :return: a float number showing the fraction of users with profile url.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_url() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_description_fraction(self):
        """
        This function finds the fraction of users with profile description in the dataset.
        :return: a float number showing the fraction of users with profile description.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_description() == True:
                target += 1
        return target / self.distinct_users_count()

    def protected_users_fraction(self):
        """
        This function finds the fraction of protected users in the dataset.
        :return: a float number showing the fraction of protected users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_protected_profile() == True:
                target += 1
        return target / self.distinct_users_count()

    def top_twitters(self, threshold_mode=True, threshold=5, top_k_mode=False, top_k=10):
        """
        This function finds either the users whose tweets number is more than the threshold (threshold-mode), or
        top k users with highest tweets number (top_k-mode).
        :param threshold_mode: a boolean parameter that activates threshhold-mode.
        :param threshold: an integer showing the threshhold of the threshold-mode.
        :param top_k_mode: a boolean parameter that activates top_k-mode.
        :param top_k: an integer showing the top_k in top_k-mode.
        :return:
        """
        assert (threshold_mode != top_k_mode), "Only one of the threshold-mode and top_k-mode can be active at the " \
                                               "same time."
        users = {}
        for tweet_id in self.tweets:
            tweet_id = self.tweets[tweet_id].get_id()
            user_id = self.tweets[tweet_id].get_twitter().get_user_id()
            users[user_id] = users.get(user_id, []) + [tweet_id]
        top_users = {user: len(users[user]) for user in users}

        if threshold_mode and not top_k_mode:
            return {user: top_users[user] for user in top_users if top_users[user] > threshold}
        elif top_k_mode and not threshold_mode:
            return {m[0]: m[1] for m in sorted(top_users.items(), key=lambda p: p[1], reverse=True)[:top_k]}

    def users_tweet_count_histogram(self):
        """
        This function counts the frequency of users for distinct number of tweets.
        :return: a sorted dictionary that maps frequency of users to tweet number.
        """
        all_users = self.top_twitters(threshold_mode=False, threshold=50, top_k_mode=True,
                                      top_k=self.distinct_users_count())
        histogram = {}
        for user in all_users:
            histogram[all_users[user]] = histogram.get(all_users[user], 0) + 1
        return {m[0]: m[1] for m in sorted(histogram.items(), key=lambda p: p[0])}

    def distinct_users_count(self):
        """
        This function counts the number of all distinct users who posted at least one tweet in the dataset.
        :return: an integer showing the number of distinct users
        """
        users = set()
        for tweet_id in self.tweets:
            users.add(self.tweets[tweet_id].get_twitter().get_user_id())
        return len(users)

    def get_distinct_users(self, output="users_list"):
        """
        This function gives all distinct users who posted at least one tweet in the dataset.
        :param output: the output can be "users_list" or "users_id", or "users_tweet_dictionary".
        :return: a list of all distinct users_object or user_ids.
        """

        assert (output in ["users_list", "id",
                           "users_tweet_dictionary"]), "the output paramater can be users_list or id, or " \
                                                       "users_tweet_dictionary"

        users = set()
        users_object = []
        users_tweet_dict = {}
        for tweet_id in self.tweets:
            user_obj = self.tweets[tweet_id].get_twitter()
            user_id = user_obj.get_user_id()
            if user_id not in users:
                users.add(user_id)
                users_object.append(user_obj)
            users_tweet_dict[user_id] = users_tweet_dict.get(user_id, []) + [self.tweets[tweet_id]]
        if output == "users_list":
            return users_object
        elif output == "id":
            return list(users)
        elif output == "users_tweet_dictionary":
            return users_tweet_dict
    # def get_users_with_duplicated_tweets(self):
    #     user_tweet_dict = {p:q for p,q in self.get_distinct_users(output="users_tweet_dictionary").items() if len(q)>1}
    #     users_redundant_dict = {}
    #     for user_id, tweet_list in user_tweet_dict.items():
    #         users_redundant_dict[user_id] = {}
    #         for pair in combinations(tweet_list, 2):
    #             dist = TwixUtility.levenshtein_distance(pair[0], pair[1])
    #             if dist == 0:
    #                 users_redundant_dict[user_id][len(users_redundant_dict[user_id])+1] =


class timeIndependentLocationDependentTweetMassFeatures(placeFeatures):
    # def __init__(self, tweets):
    #     self.tweets = tweets
    def spatial_tweet_complexity(self, resolution='country', unit="word"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param unit: the unit of analysis for tweet complexity analysis. It can be "word", "sentence", or "syllables".
        :return: a dictionary that represents the tweet complexity across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet complexity scores in all the tweets that are posted
        within every spatial unit.
        """

        assert (resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (unit in ["word", "sentence",
                         "syllables"]), "The unit of analysis has to be word, sentence, or syllables"

        complexity = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                complexity[country] = []
                complexity_results = []
                for tweet in tweets:
                    complexity_results.append(tweet.text_complexity(unit=unit))
                for result in complexity_results:
                    complexity[country] = complexity.get(country, []) + [float(result)]

                scores = complexity[country]
                complexity[country] = {}
                if len(scores) > 0:
                    complexity[country]["average"] = np.nanmean(scores)
                    complexity[country]["max"] = np.nanmax(scores)
                    complexity[country]["min"] = np.nanmin(scores)
                    complexity[country]["stdev"] = np.nanstd(scores)
                    complexity[country]["median"] = np.nanmedian(scores)
                else:
                    complexity[country]["average"] = np.nan
                    complexity[country]["max"] = np.nan
                    complexity[country]["min"] = np.nan
                    complexity[country]["stdev"] = np.nan
                    complexity[country]["median"] = np.nan
            return complexity

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                complexity[place] = []
                complexity_results = []
                for tweet in tweets:
                    complexity_results.append(tweet.text_complexity(unit=unit))
                for result in complexity_results:
                    complexity[place] = complexity.get(place, []) + [float(result)]

                scores = complexity[place]
                complexity[place] = {}
                if len(scores) > 0:
                    complexity[place]["average"] = np.nanmean(scores)
                    complexity[place]["max"] = np.nanmax(scores)
                    complexity[place]["min"] = np.nanmin(scores)
                    complexity[place]["stdev"] = np.nanstd(scores)
                    complexity[place]["median"] = np.nanmedian(scores)
                else:
                    complexity[place]["average"] = np.nan
                    complexity[place]["max"] = np.nan
                    complexity[place]["min"] = np.nan
                    complexity[place]["stdev"] = np.nan
                    complexity[place]["median"] = np.nan
            return complexity

    def spatial_tweet_readability(self, resolution='country', metric="flesch_kincaid_grade"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
        :return: a dictionary that represents the tweet readability score across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet readability scores in all the tweets that are posted
        within every spatial unit.
        """

        assert (resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        readability = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                readability[country] = []
                readability_results = []
                for tweet in tweets:
                    readability_results.append(tweet.readability(metric=metric))
                for result in readability_results:
                    readability[country] = readability.get(country, []) + [float(result)]

                scores = readability[country]
                readability[country] = {}
                if len(scores) > 0:
                    readability[country]["average"] = np.nanmean(scores)
                    readability[country]["max"] = np.nanmax(scores)
                    readability[country]["min"] = np.nanmin(scores)
                    readability[country]["stdev"] = np.nanstd(scores)
                    readability[country]["median"] = np.nanmedian(scores)
                else:
                    readability[country]["average"] = np.nan
                    readability[country]["max"] = np.nan
                    readability[country]["min"] = np.nan
                    readability[country]["stdev"] = np.nan
                    readability[country]["median"] = np.nan
            return readability

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                readability[place] = []
                readability_results = []
                for tweet in tweets:
                    readability_results.append(tweet.readability(metric=metric))
                for result in readability_results:
                    readability[place] = readability.get(place, []) + [float(result)]

                scores = readability[place]
                readability[place] = {}
                if len(scores) > 0:
                    readability[place]["average"] = np.nanmean(scores)
                    readability[place]["max"] = np.nanmax(scores)
                    readability[place]["min"] = np.nanmin(scores)
                    readability[place]["stdev"] = np.nanstd(scores)
                    readability[place]["median"] = np.nanmedian(scores)
                else:
                    readability[place]["average"] = np.nan
                    readability[place]["max"] = np.nan
                    readability[place]["min"] = np.nan
                    readability[place]["stdev"] = np.nan
                    readability[place]["median"] = np.nan
            return readability

    def spatial_tweet_length(self, resolution='country', unit="word"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param unit: the unit of analysis for measuring tweet length. It can be "character", "word", or "sentence".
        :return: a dictionary that represents the tweet length across the spatial units. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the tweet length in all the tweets that are posted
        within every spatial unit.
        """

        assert (resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (unit in ["character", "word", "sentence"]), "The unit has to be character, word, or sentence"

        tweet_length = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                tweet_length[country] = []
                tweet_length_results = []
                for tweet in tweets:
                    tweet_length_results.append(tweet.text_length(unit=unit))
                for result in tweet_length_results:
                    tweet_length[country] = tweet_length.get(country, []) + [float(result)]

                scores = tweet_length[country]
                tweet_length[country] = {}
                if len(scores) > 0:
                    tweet_length[country]["average"] = np.nanmean(scores)
                    tweet_length[country]["max"] = np.nanmax(scores)
                    tweet_length[country]["min"] = np.nanmin(scores)
                    tweet_length[country]["stdev"] = np.nanstd(scores)
                    tweet_length[country]["median"] = np.nanmedian(scores)
                    tweet_length[country]["median"] = np.nanmedian(scores)
                else:
                    tweet_length[country]["average"] = np.nan
                    tweet_length[country]["max"] = np.nan
                    tweet_length[country]["min"] = np.nan
                    tweet_length[country]["stdev"] = np.nan
                    tweet_length[country]["median"] = np.nan
                    tweet_length[country]["median"] = np.nan
            return tweet_length

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                tweet_length[place] = []
                tweet_length_results = []
                for tweet in tweets:
                    tweet_length_results.append(tweet.text_length(unit=unit))
                for result in tweet_length_results:
                    tweet_length[place] = tweet_length.get(place, []) + [float(result)]

                scores = tweet_length[place]
                tweet_length[place] = {}
                if len(scores) > 0:
                    tweet_length[place]["average"] = np.nanmean(scores)
                    tweet_length[place]["max"] = np.nanmax(scores)
                    tweet_length[place]["min"] = np.nanmin(scores)
                    tweet_length[place]["stdev"] = np.nanstd(scores)
                    tweet_length[place]["median"] = np.nanmedian(scores)
                    tweet_length[place]["median"] = np.nanmedian(scores)
                else:
                    tweet_length[place]["average"] = np.nan
                    tweet_length[place]["max"] = np.nan
                    tweet_length[place]["min"] = np.nan
                    tweet_length[place]["stdev"] = np.nan
                    tweet_length[place]["median"] = np.nan
                    tweet_length[place]["median"] = np.nan
            return tweet_length

    def spatial_tweet_count(self, resolution='country'):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents the tweet count across the spatial units.
        The key-value pair in this dictionary corresponds to the spatial unit of analysis and
        the the number of the tweets that are posted within every spatial unit.
        """
        assert (resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"

        tweet_count = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                tweet_count[country] = len(tweets)
            return tweet_count
        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                tweet_count[place] = len(tweets)
            return tweet_count

    def spatial_sentiment(self, resolution='country', sentiment_engine="vader"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: a dictionary that represents the tweet sentiments across the spatial units regarding the selected sentiment engine. The key-value pair in this dictionary corresponds to
        the spatial unit of analysis and the statistical metrics of the sentiment scores in all the tweets that are posted within every spatial unit.
        """

        assert (resolution in ["country", "place"]), "The spatial unit of analysis has to be country or place"
        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"

        sentiments = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                sentiments[country] = {}
                sentiment_results = []
                for tweet in tweets:
                    sentiment_results.append(tweet.sentiment_analysis(sentiment_engine))
                for result in sentiment_results:
                    for score in result:
                        sentiments[country][score] = sentiments[country].get(score, []) + [float(result[score])]

                for score in sentiments[country]:
                    scores = sentiments[country][score]
                    sentiments[country][score] = {}
                    sentiments[country][score]["average"] = np.nanmean(scores)
                    sentiments[country][score]["max"] = np.nanmax(scores)
                    sentiments[country][score]["min"] = np.nanmin(scores)
                    sentiments[country][score]["stdev"] = np.nanstd(scores)
                    sentiments[country][score]["median"] = np.nanmedian(scores)
            return sentiments
        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                sentiments[place] = {}
                sentiment_results = []
                for tweet in tweets:
                    sentiment_results.append(tweet.sentiment_analysis(sentiment_engine))
                for result in sentiment_results:
                    for score in result:
                        sentiments[place][score] = sentiments[place].get(score, []) + [float(result[score])]

                for score in sentiments[place]:
                    scores = sentiments[place][score]
                    sentiments[place][score] = {}
                    sentiments[place][score]["average"] = np.nanmean(scores)
                    sentiments[place][score]["max"] = np.nanmax(scores)
                    sentiments[place][score]["min"] = np.nanmin(scores)
                    sentiments[country][score]["stdev"] = np.nanstd(scores)
                    sentiments[place][score]["median"] = np.nanmedian(scores)
            return sentiments

class timeIndependentLocationDependentUserMassFeatures(placeFeatures):

    def spatial_user_role(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user score across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user role of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_roles = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                user_roles[country] = []
                user_roles_results = []
                for tweet in tweets:
                    user_roles_results.append(tweet.get_twitter().get_user_role())
                for result in user_roles_results:
                    user_roles[country] = user_roles.get(country, []) + [float(result)]

                scores = user_roles[country]
                user_roles[country] = {}
                if len(scores) > 0:
                    user_roles[country]["average"] = np.nanmean(scores)
                    user_roles[country]["max"] = np.nanmax(scores)
                    user_roles[country]["min"] = np.nanmin(scores)
                    user_roles[country]["stdev"] = np.nanstd(scores)
                    user_roles[country]["median"] = np.nanmedian(scores)
                else:
                    user_roles[country]["average"] = np.nan
                    user_roles[country]["max"] = np.nan
                    user_roles[country]["min"] = np.nan
                    user_roles[country]["stdev"] = np.nan
                    user_roles[country]["median"] = np.nan
            return user_roles
        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                user_roles[place] = []
                user_roles_results = []
                for tweet in tweets:
                    user_roles_results.append(tweet.get_twitter().get_user_role())
                for result in user_roles_results:
                    user_roles[place] = user_roles.get(place, []) + [float(result)]

                scores = user_roles[place]
                user_roles[place] = {}
                if len(scores) > 0:
                    user_roles[place]["average"] = np.nanmean(scores)
                    user_roles[place]["max"] = np.nanmax(scores)
                    user_roles[place]["min"] = np.nanmin(scores)
                    user_roles[place]["stdev"] = np.nanstd(scores)
                    user_roles[place]["median"] = np.nanmedian(scores)
                else:
                    user_roles[place]["average"] = np.nan
                    user_roles[place]["max"] = np.nan
                    user_roles[place]["min"] = np.nan
                    user_roles[place]["stdev"] = np.nan
                    user_roles[place]["median"] = np.nan
            return user_roles

    def spatial_user_reputation(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user reputation across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user reputation of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_reputation = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                user_reputation[country] = []
                user_reputation_results = []
                for tweet in tweets:
                    user_reputation_results.append(tweet.get_twitter().get_user_reputation())
                for result in user_reputation_results:
                    user_reputation[country] = user_reputation.get(country, []) + [float(result)]

                scores = user_reputation[country]
                user_reputation[country] = {}
                if len(scores) > 0:
                    user_reputation[country]["average"] = np.nanmean(scores)
                    user_reputation[country]["max"] = np.nanmax(scores)
                    user_reputation[country]["min"] = np.nanmin(scores)
                    user_reputation[country]["stdev"] = np.nanstd(scores)
                    user_reputation[country]["median"] = np.nanmedian(scores)
                else:
                    user_reputation[country]["average"] = np.nan
                    user_reputation[country]["max"] = np.nan
                    user_reputation[country]["min"] = np.nan
                    user_reputation[country]["stdev"] = np.nan
                    user_reputation[country]["median"] = np.nan
            return user_reputation
        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                user_reputation[place] = []
                user_reputation_results = []
                for tweet in tweets:
                    user_reputation_results.append(tweet.get_twitter().get_user_reputation())
                for result in user_reputation_results:
                    user_reputation[place] = user_reputation.get(place, []) + [float(result)]

                scores = user_reputation[place]
                user_reputation[place] = {}
                if len(scores) > 0:
                    user_reputation[place]["average"] = np.nanmean(scores)
                    user_reputation[place]["max"] = np.nanmax(scores)
                    user_reputation[place]["min"] = np.nanmin(scores)
                    user_reputation[place]["stdev"] = np.nanstd(scores)
                    user_reputation[place]["median"] = np.nanmedian(scores)
                else:
                    user_reputation[place]["average"] = np.nan
                    user_reputation[place]["max"] = np.nan
                    user_reputation[place]["min"] = np.nan
                    user_reputation[place]["stdev"] = np.nan
                    user_reputation[place]["median"] = np.nan
            return user_reputation

    def spatial_followers(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents followers count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the followers count of every account
        that has posted at least a tweet within each spatial unit.
        """

        followers_count = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                followers_count[country] = []
                followers_count_results = []
                for tweet in tweets:
                    followers_count_results.append(tweet.get_twitter().get_followers_count())
                for result in followers_count_results:
                    followers_count[country] = followers_count.get(country, []) + [float(result)]

                scores = followers_count[country]
                followers_count[country] = {}
                if len(scores) > 0:
                    followers_count[country]["average"] = np.nanmean(scores)
                    followers_count[country]["max"] = np.nanmax(scores)
                    followers_count[country]["min"] = np.nanmin(scores)
                    followers_count[country]["stdev"] = np.nanstd(scores)
                    followers_count[country]["median"] = np.nanmedian(scores)
                else:
                    followers_count[country]["average"] = np.nan
                    followers_count[country]["max"] = np.nan
                    followers_count[country]["min"] = np.nan
                    followers_count[country]["stdev"] = np.nan
                    followers_count[country]["median"] = np.nan
            return followers_count

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                followers_count[place] = []
                followers_count_results = []
                for tweet in tweets:
                    followers_count_results.append(tweet.get_twitter().get_followers_count())
                for result in followers_count_results:
                    followers_count[place] = followers_count.get(place, []) + [float(result)]

                scores = followers_count[place]
                followers_count[place] = {}
                if len(scores) > 0:
                    followers_count[place]["average"] = np.nanmean(scores)
                    followers_count[place]["max"] = np.nanmax(scores)
                    followers_count[place]["min"] = np.nanmin(scores)
                    followers_count[place]["stdev"] = np.nanstd(scores)
                    followers_count[place]["median"] = np.nanmedian(scores)
                else:
                    followers_count[place]["average"] = np.nan
                    followers_count[place]["max"] = np.nan
                    followers_count[place]["min"] = np.nan
                    followers_count[place]["stdev"] = np.nan
                    followers_count[place]["median"] = np.nan
            return followers_count

    def spatial_friends(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents friends count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the friends count of every account
        that has posted at least a tweet within each spatial unit.
        """

        followers_count = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                followers_count[country] = []
                followers_count_results = []
                for tweet in tweets:
                    followers_count_results.append(tweet.get_twitter().get_friends_count())
                for result in followers_count_results:
                    followers_count[country] = followers_count.get(country, []) + [float(result)]

                scores = followers_count[country]
                followers_count[country] = {}
                if len(scores) > 0:
                    followers_count[country]["average"] = np.nanmean(scores)
                    followers_count[country]["max"] = np.nanmax(scores)
                    followers_count[country]["min"] = np.nanmin(scores)
                    followers_count[country]["stdev"] = np.nanstd(scores)
                    followers_count[country]["median"] = np.nanmedian(scores)
                else:
                    followers_count[country]["average"] = np.nan
                    followers_count[country]["max"] = np.nan
                    followers_count[country]["min"] = np.nan
                    followers_count[country]["stdev"] = np.nan
                    followers_count[country]["median"] = np.nan
            return followers_count

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                followers_count[place] = []
                followers_count_results = []
                for tweet in tweets:
                    followers_count_results.append(tweet.get_twitter().get_friends_count())
                for result in followers_count_results:
                    followers_count[place] = followers_count.get(place, []) + [float(result)]

                scores = followers_count[place]
                followers_count[place] = {}
                if len(scores) > 0:
                    followers_count[place]["average"] = np.nanmean(scores)
                    followers_count[place]["max"] = np.nanmax(scores)
                    followers_count[place]["min"] = np.nanmin(scores)
                    followers_count[place]["stdev"] = np.nanstd(scores)
                    followers_count[place]["median"] = np.nanmedian(scores)
                else:
                    followers_count[place]["average"] = np.nan
                    followers_count[place]["max"] = np.nan
                    followers_count[place]["min"] = np.nan
                    followers_count[place]["stdev"] = np.nan
                    followers_count[place]["median"] = np.nan
            return followers_count

    def spatial_account_age(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents account age across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the age of every account
        that has posted at least a tweet within each spatial unit.
        """

        account_age = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                account_age[country] = []
                account_age_results = []
                for tweet in tweets:
                    account_age_results.append(tweet.get_twitter().get_account_age())
                for result in account_age_results:
                    account_age[country] = account_age.get(country, []) + [float(result)]

                scores = account_age[country]
                account_age[country] = {}
                if len(scores) > 0:
                    account_age[country]["average"] = np.nanmean(scores)
                    account_age[country]["max"] = np.nanmax(scores)
                    account_age[country]["min"] = np.nanmin(scores)
                    account_age[country]["stdev"] = np.nanstd(scores)
                    account_age[country]["median"] = np.nanmedian(scores)
                else:
                    account_age[country]["average"] = np.nan
                    account_age[country]["max"] = np.nan
                    account_age[country]["min"] = np.nan
                    account_age[country]["stdev"] = np.nan
                    account_age[country]["median"] = np.nan
            return account_age

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                account_age[place] = []
                account_age_results = []
                for tweet in tweets:
                    account_age_results.append(tweet.get_twitter().get_account_age())
                for result in account_age_results:
                    account_age[place] = account_age.get(place, []) + [float(result)]

                scores = account_age[place]
                account_age[place] = {}
                if len(scores) > 0:
                    account_age[place]["average"] = np.nanmean(scores)
                    account_age[place]["max"] = np.nanmax(scores)
                    account_age[place]["min"] = np.nanmin(scores)
                    account_age[place]["stdev"] = np.nanstd(scores)
                    account_age[place]["median"] = np.nanmedian(scores)
                else:
                    account_age[place]["average"] = np.nan
                    account_age[place]["max"] = np.nan
                    account_age[place]["min"] = np.nan
                    account_age[place]["stdev"] = np.nan
                    account_age[place]["median"] = np.nan
            return account_age

    def spatial_total_likes(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents total account likes across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the totall likes of every account
        that has posted at least a tweet within each spatial unit.
        """

        total_likes = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                total_likes[country] = []
                total_likes_results = []
                for tweet in tweets:
                    total_likes_results.append(tweet.get_twitter().get_user_total_likes_count())
                for result in total_likes_results:
                    total_likes[country] = total_likes.get(country, []) + [float(result)]

                scores = total_likes[country]
                total_likes[country] = {}
                if len(scores) > 0:
                    total_likes[country]["average"] = np.nanmean(scores)
                    total_likes[country]["max"] = np.nanmax(scores)
                    total_likes[country]["min"] = np.nanmin(scores)
                    total_likes[country]["stdev"] = np.nanstd(scores)
                    total_likes[country]["median"] = np.nanmedian(scores)
                else:
                    total_likes[country]["average"] = np.nan
                    total_likes[country]["max"] = np.nan
                    total_likes[country]["min"] = np.nan
                    total_likes[country]["stdev"] = np.nan
                    total_likes[country]["median"] = np.nan
            return total_likes

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                total_likes[place] = []
                total_likes_results = []
                for tweet in tweets:
                    total_likes_results.append(tweet.get_twitter().get_user_total_likes_count())
                for result in total_likes_results:
                    total_likes[place] = total_likes.get(place, []) + [float(result)]

                scores = total_likes[place]
                total_likes[place] = {}
                if len(scores) > 0:
                    total_likes[place]["average"] = np.nanmean(scores)
                    total_likes[place]["max"] = np.nanmax(scores)
                    total_likes[place]["min"] = np.nanmin(scores)
                    total_likes[place]["stdev"] = np.nanstd(scores)
                    total_likes[place]["median"] = np.nanmedian(scores)
                else:
                    total_likes[place]["average"] = np.nan
                    total_likes[place]["max"] = np.nan
                    total_likes[place]["min"] = np.nan
                    total_likes[place]["stdev"] = np.nan
                    total_likes[place]["median"] = np.nan
            return total_likes

    def spatial_status_count(self, resolution="country"):
        """
        :param resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents status count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the status count of every account
        that has posted at least a tweet within each spatial unit.
        """

        status_count = {}
        if resolution == "country":
            tweets_with_countries = self.countries_with_tweets()
            for country, tweets in tweets_with_countries.items():
                status_count[country] = []
                status_count_results = []
                for tweet in tweets:
                    status_count_results.append(tweet.get_twitter().get_statusses_count())
                for result in status_count_results:
                    status_count[country] = status_count.get(country, []) + [float(result)]

                scores = status_count[country]
                status_count[country] = {}
                if len(scores) > 0:
                    status_count[country]["average"] = np.nanmean(scores)
                    status_count[country]["max"] = np.nanmax(scores)
                    status_count[country]["min"] = np.nanmin(scores)
                    status_count[country]["stdev"] = np.nanstd(scores)
                    status_count[country]["median"] = np.nanmedian(scores)
                else:
                    status_count[country]["average"] = np.nan
                    status_count[country]["max"] = np.nan
                    status_count[country]["min"] = np.nan
                    status_count[country]["stdev"] = np.nan
                    status_count[country]["median"] = np.nan
            return status_count

        elif resolution == "place":
            tweets_with_places = self.places_with_tweets()
            for place, tweets in tweets_with_places.items():
                status_count[place] = []
                status_count_results = []
                for tweet in tweets:
                    status_count_results.append(tweet.get_twitter().get_statusses_count())
                for result in status_count_results:
                    status_count[place] = status_count.get(place, []) + [float(result)]

                scores = status_count[place]
                status_count[place] = {}
                if len(scores) > 0:
                    status_count[place]["average"] = np.nanmean(scores)
                    status_count[place]["max"] = np.nanmax(scores)
                    status_count[place]["min"] = np.nanmin(scores)
                    status_count[place]["stdev"] = np.nanstd(scores)
                    status_count[place]["median"] = np.nanmedian(scores)
                else:
                    status_count[place]["average"] = np.nan
                    status_count[place]["max"] = np.nan
                    status_count[place]["min"] = np.nan
                    status_count[place]["stdev"] = np.nan
                    status_count[place]["median"] = np.nan
            return status_count

############################################# mass features #############################################


############################################# network features #############################################
class topologyBasedFeatures:
    def __init__(self, tweets):
        """
        This is a constructor for tweetNetwork class
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object.
        """
        self.tweets = tweets

    def time_dependent_features(self):
        """
        :return: an object of networkTweetFeatures which comprises the singleTweet objects
        """
        return timeDependentNetworkFeatures(self.tweets)

    def time_independent_features(self):
        """
        :return: an object of networkUserFeatures which comprises the singleTweet objects
        """
        return timeIndependentNetworkFeatures(self.tweets)


class timeDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def time_dependent_location_dependent_network_features(self):
        return timeDependentLocationDependentNetworkFeatures(self.tweets)

    def time_dependent_location_independent_network_features(self):
        return timeDependentLocationIndependentNetworkFeatures(self.tweets)


class timeIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def time_independent_location_dependent_network_features(self):
        return timeIndependentLocationDependentNetworkFeatures(self.tweets)

    def time_independent_location_independent_network_features(self):
        return timeIndependentLocationIndependentNetworkFeatures(self.tweets)


class timeDependentLocationDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationDependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationDependentUserNetworkFeatures(self.tweets)


class timeDependentLocationIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationIndependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the singleTweet objects
        """
        return timeDependentLocationIndependentUserNetworkFeatures(self.tweets)


class timeIndependentLocationDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationDependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationDependentUserNetworkFeatures(self.tweets)


class timeIndependentLocationIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationIndependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the singleTweet objects
        """
        return timeIndependentLocationIndependentUserNetworkFeatures(self.tweets)


# class timeDependentLocationDependentTweetNetworkFeatures:

# class timeDependentLocationDependentUserNetworkFeatures:

# class timeDependentLocationIndependentTweetNetworkFeatures:

# class timeDependentLocationIndependentUserNetworkFeatures:

# class timeIndependentLocationDependentTweetNetworkFeatures:

# class timeIndependentLocationDependentUserNetworkFeatures:

# class timeIndependentLocationIndependentTweetNetworkFeatures:

# class timeIndependentLocationIndependentUserNetworkFeatures:

############################################# network features #############################################

#### => 8 classes based on 4 above classes


class tweetTopologyFeatures:
    def __init__(self, tweets):
        """
        This is a constructor for tweetNetwork class
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object.
        """
        self.tweets = tweets

    def retweet_network(self):
        """
        This function creates the network of retweets from the dataset.
        :return: a retweetNetwork object.
        """
        return retweetNetwork(self.tweets)

    def quote_network(self):
        """
        This function creates the network of quotes from the dataset.
        :return: a quoteNetwork object.
        """
        return quoteNetwork(self.tweets)

    def reply_network(self):  # not yet deployed
        """
        This function creates the network of replies from the dataset.
        :return: a replyNetwork object.
        """
        return replyNetwork(self.tweets)
    # def retweet_quote_network(self):
    #     """
    #     This function creates the network of retweet-quote from the dataset.
    #     :return: a retweetQuoteNetwork object.
    #     """
    #     return retweetQuoteNetwork(self.tweets)
    # def retweet_reply_network(self):  # Not yet deplyed
    #     """
    #     This function creates the network of retweet-reply from the dataset.
    #     :return: a retweetReplyNetwork object.
    #     """
    #     return retweetReplyNetwork(self.tweets)
    # def quote_reply_network(self):  # not yet deployed
    #     """
    #     This function creates the network of quote-reply from the dataset.
    #     :return: a quoteReplyNetwork object.
    #     """
    #     return quoteReplyNetwork(self.tweets)
    # def retweet_quote_reply_network(self):  # not yet deployed
    #     """
    #     This function creates the network of retweet_quote_reply from the dataset.
    #     :return: a retweetQuoteReplyNetwork object.
    #     """
    #     return retweetQuoteReplyNetwork(self.tweets)


class userTopologyFeatures:
    def __init__(self, tweets):
        """
        This is a constructor for tweetNetwork class
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object.
        """
        self.tweets = tweets

    def user_retweet_network(self):
        """
        This function creates the user_retweet_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has retweeted user A.
        :return: a userRetweetNetwork object.
        """
        return userRetweetNetwork(self.tweets)

    def user_quote_network(self):
        """
        This function creates the user_quote_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has quoted user A.
        :return: a userQuoteNetwork object.
        """
        return userQuoteNetwork(self.tweets)

    def user_reply_network(self):  # not yet deployed
        """
        This function creates the user_reply_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has replied to user A.
        :return: a userReplyNetwork object.
        """
        return userReplyNetwork(self.tweets)
    # def user_retweet_quote_network(self):
    #     """
    #     This function creates user_retweet_quote_network from the dataset. In this directed network, nodes
    #     represent users. Also a link from user A to B shows user B has either retweeted or quoted user A.
    #     :return: a userRetweetQuoteNetwork object.
    #     """
    #     return userRetweetQuoteNetwork(self.tweets)
    # def user_retweet_reply_network(self):  # Not yet deplyed
    #     """
    #     This function creates user_retweet_reply_network from the dataset. In this directed network, nodes
    #     represent users. Also a link from user A to B shows user B has either retweeted or replied to user A.
    #     :return: a userRetweetReplyNetwork object.
    #     """
    #     return userRetweetReplyNetwork(self.tweets)
    # def user_quote_reply_network(self):  # not yet deployed
    #     """
    #     This function creates user_quote_reply_network from the dataset. In this directed network, nodes
    #     represent users. Also a link from user A to B shows user B has either quoted or replied to user A.
    #     :return: a userQuoteReplyNetwork object.
    #     """
    #     return userQuoteReplyNetwork(self.tweets)
    # def user_retweet_quote_reply_network(self):  # not yet deployed
    #     """
    #     This function creates user_retweet_quote_reply_network from the dataset. In this directed network, nodes
    #     represent users. Also a link from user A to B shows user B has either quoted, retweeted or replied to user A.
    #     :return: a userRetweetQuoteReplyNetwork object.
    #     """
    #     return userRetweetQuoteReplyNetwork(self.tweets)


class network():
    def __init__(self, tweets):
        """
        This is a constructor of a network class.
        :param tweets: a dictionary that maps every tweet_id to its corresponding singleTweet object.
        """
        self.network = nx.DiGraph()
        self.tweets = tweets

    def building_network(self):
        pass

    def components_number(self):
        """
        This function calculates the number of connected components in the desired network.
        :return: an integer that shows the number of connected components.
        """
        return nx.number_connected_components(self.network.to_undirected())

    def centrality_measures(self, metric="degree"):
        """
        This function measures network centrality based on the chosen metric.
        :param metric: metric can be "degree", "closeness", "betweenness", "eigenvector", "katz", and "pagerank". Please
        note that for degree centrality it measures both in-degree and out-degree centrality.
        :return: This function does not return anything, instead it add the relevant attribute to the caller network object.
        To get the network, use get_network() function.
        """

        assert (metric in ["degree", "closeness", "betweenness", "eigenvector", "katz",
                           "pagerank"]), "The metric has to be" \
                                         " degree, closeness, betweenness, " \
                                         "eigenvector, katz, or pagerank."
        if metric == "degree":
            degree_centrality = nx.centrality.degree_centrality(self.network)
            for node_id in degree_centrality:
                self.network.node[node_id]["degree_centrality"] = degree_centrality[node_id]
            in_degree_centrality = nx.centrality.in_degree_centrality(self.network)
            for node_id in in_degree_centrality:
                self.network.node[node_id]["in_degree_centrality"] = in_degree_centrality[node_id]
            out_degree_centrality = nx.centrality.out_degree_centrality(self.network)
            for node_id in out_degree_centrality:
                self.network.node[node_id]["out_degree_centrality"] = out_degree_centrality[node_id]
        elif metric == "closeness":
            closeness_centrality = nx.centrality.closeness_centrality(self.network)
            for node_id in closeness_centrality:
                self.network.node[node_id]["closeness_centrality"] = closeness_centrality[node_id]
        elif metric == "betweenness":
            betweenness_centrality = nx.centrality.betweenness_centrality(self.network)
            for node_id in betweenness_centrality:
                self.network.node[node_id]["betweenness_centrality"] = betweenness_centrality[node_id]
        elif metric == "eigenvector":
            eigenvector_centrality = nx.centrality.eigenvector_centrality_numpy(self.network)
            for node_id in eigenvector_centrality:
                self.network.node[node_id]["eigenvector_centrality"] = eigenvector_centrality[node_id]
        elif metric == "katz":
            katz_centrality = nx.centrality.katz_centrality_numpy(self.network)
            for node_id in katz_centrality:
                self.network.node[node_id]["katz_centrality"] = katz_centrality[node_id]
        elif metric == "pagerank":
            pagerank_centrality = nx.pagerank_numpy(self.network)
            for node_id in pagerank_centrality:
                self.network.node[node_id]["pagerank_centrality"] = pagerank_centrality[node_id]

    def community_detection(self):
        """
        This function identified communities in the network using Louvain algorithm. PLease note that, it uses the undirected
        version of the network.
        :return: This function does not return anything, instead it add the relevant attribute to the caller network object.
        To get the network, use get_network() function.
        """
        partition = community.best_partition(self.network.to_undirected())
        for node_id in partition:
            self.network.node[node_id]["community"] = partition[node_id]

    def word_count_layer(self):
        pass

    def character_count_layer(self):
        pass

    def sentence_count_layer(self):
        pass

    def word_complexity_layer(self):
        pass

    def sentence_complexity_layer(self):
        pass

    def syllables_complexity_layer(self):
        pass

    def sentiment_layer(self):
        pass

    def readability_layer(self):
        pass

    def get_network(self):
        return self.network


class retweetNetwork(network):  # node should change to nodes in order to call a particular node
    def building_network(self):
        """
        This function builds the retweet network.
        :return: This function does not return the network. It updates the class properties. To get the network, use
        get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.add_edge(tweet.get_retweeted().get_id(), tweet.get_id(), kind="retweet")
            elif trf == False:
                self.network.add_node(tweet.get_id())

    def word_count_layer(self):
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()]["word_count"] = tweet.get_retweeted().text_length()
                self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
            elif trf == False:
                self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()

    def character_count_layer(self):
        """
        This function add the number of characters in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()][
                    "character_count"] = tweet.get_retweeted().text_length(unit="character")
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="character")
            elif trf == False:
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="character")

    def sentence_count_layer(self):
        """
        This function add the number of sentences in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.nodes[tweet.get_retweeted().get_id()][
                    "character_count"] = tweet.get_retweeted().text_length(unit="sentence")
                self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(unit="sentence")
            elif trf == False:
                self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(unit="sentence")

    def word_complexity_layer(self):
        """
        This function add the word complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()][
                    "word_complexity"] = tweet.get_retweeted().text_complexity()
                self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
            elif trf == False:
                self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()

    def sentence_complexity_layer(self):
        """
        This function add the sentence complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()][
                    "sentence_complexity"] = tweet.get_retweeted().text_complexity(unit="sentence")
                self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(unit="sentence")
            elif trf == False:
                self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(unit="sentence")

    def syllables_complexity_layer(self):
        """
        This function add the syllables complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()][
                    "syllables_complexity"] = tweet.get_retweeted().text_complexity(unit="syllables")
                self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(unit="syllables")
            elif trf == False:
                self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(unit="syllables")

    def sentiment_layer(self, sentiment_engine="vader"):
        """
        This function add the sentiment of each tweet as a property to every node.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"

        subscores_labels = {"textblob": ["subjectivity", "polarity"],
                            "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
                            "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
                                    "sadness_score", "surprise_score", "trust_score"],
                            "hate_speech": ["hate_speech", "offensive_language", "neither"],
                            "vad": ["valence_score", "arousal_score", "dominance_score"]}
        for tweet_id, tweet in self.tweets.items():
            for i in subscores_labels[sentiment_engine]:
                trf = tweet.is_retweeted()
                if trf == True:
                    self.network.node[tweet.get_retweeted().get_id()][i] = \
                        tweet.get_retweeted().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
                    self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
                        i]
                elif trf == False:
                    self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
                        i]

    def readability_layer(self, metric="flesch_kincaid_grade"):
        """
        This function add the readability of each tweet as a property to every node.
        :param metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
        :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        assert (metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        # for tweet_id, tweet in self.tweets.items():
        for tweet_id in tqdm(self.tweets):
            tweet = self.tweets[tweet_id]
            trf = tweet.is_retweeted()
            if trf == True:
                self.network.node[tweet.get_retweeted().get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.get_retweeted().text_preprocessing()}\")')
                self.network.node[tweet.get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.text_preprocessing()}\")')
            elif trf == False:
                self.network.node[tweet.get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.text_preprocessing()}\")')


class quoteNetwork(network):
    def building_network(self):
        """
        This function builds the quote network.
        :return: This function does not return the network. It updates the class properties. To get the network, use
        get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.add_edge(tweet.get_quote().get_id(), tweet.get_id(), kind="quote")
            elif tqf == False:
                self.network.add_node(tweet.get_id())

    def word_count_layer(self):
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()]["word_count"] = tweet.get_quote().text_length()
                self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
            elif tqf == False:
                self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()

    def character_count_layer(self):
        """
        This function add the number of characters in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
                    unit="character")
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="character")
            elif tqf == False:
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="character")

    def sentence_count_layer(self):
        """
        This function add the number of sentences in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
                    unit="sentence")
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="sentence")
            elif tqf == False:
                self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(unit="sentence")

    def word_complexity_layer(self):
        """
        This function add the word complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()]["word_complexity"] = tweet.get_quote().text_complexity()
                self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
            elif tqf == False:
                self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()

    def sentence_complexity_layer(self):
        """
        This function add the sentence complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()][
                    "sentence_complexity"] = tweet.get_quote().text_complexity(unit="sentence")
                self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(unit="sentence")
            elif tqf == False:
                self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(unit="sentence")

    def syllables_complexity_layer(self):
        """
        This function add the syllables complexity of each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()][
                    "syllables_complexity"] = tweet.get_quote().text_complexity(unit="syllables")
                self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(unit="syllables")
            elif tqf == False:
                self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(unit="syllables")

    def sentiment_layer(self, sentiment_engine="vader"):
        """
        This function add the sentiment of each tweet as a property to every node.
        :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
        "vad".
        :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "The sentiment_engine has to be" \
                                              "textblob, vader, nrc," \
                                              "hate_speech or vad"

        subscores_labels = {"textblob": ["subjectivity", "polarity"],
                            "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
                            "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
                                    "sadness_score", "surprise_score", "trust_score"],
                            "hate_speech": ["hate_speech", "offensive_language", "neither"],
                            "vad": ["valence_score", "arousal_score", "dominance_score"]}
        for tweet_id, tweet in self.tweets.items():
            for i in subscores_labels[sentiment_engine]:
                tqf = tweet.is_quoted()
                if tqf == True:
                    self.network.node[tweet.get_quote().get_id()][i] = \
                        tweet.get_quote().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
                    self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
                        i]
                elif tqf == False:
                    self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
                        i]

    def readability_layer(self, metric="flesch_kincaid_grade"):
        """
        This function add the readability of each tweet as a property to every node.
        :param metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
        :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        assert (metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score", ]), "The metric " \
                                                               "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                               "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                               "or dale_chall_readability_score."

        for tweet_id, tweet in self.tweets.items():
            tqf = tweet.is_quoted()
            if tqf == True:
                self.network.node[tweet.get_quote().get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.get_quote().text_preprocessing()}\")')
                self.network.node[tweet.get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.text_preprocessing()}\")')
            elif tqf == False:
                self.network.node[tweet.get_id()]["readability"] = eval(
                    f'textstat.{metric}(\"{tweet.text_preprocessing()}\")')


class user:
    def __init__(self, user_object):
        """
        This is the constructor of user class.
        :param user_object: the user object which is embedded in tweet object.
        """
        self.user = user_object

    def get_user_id(self):
        """
        This function gives the user unique id.
        :return: an integer showing the user unique id.
        """
        return self.user["id"]

    def get_user_name(self):
        """
        The name of the user, as they’ve defined it. Not necessarily a person’s name. Typically capped at 50 characters,
         but subject to change.
        :return: a string showing the user defined name.
        """
        return self.user["name"]

    def get_screen_name(self):
        """
        The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject
         to change. Typically a maximum of 15 characters long, but some historical accounts may exist with longer names.
        :return: a string showing the screen name of the user.
        """
        return self.user["screen_name"]

    def get_friends_count(self):
        """
        The number of users this account is following (AKA their “followings”)
        :return: an integer showing the number of account holder's friends (followings).
        """
        return self.user["friends_count"]

    def get_followers_count(self):
        """
        The number of followers this account has.
        :return: an integer showing the number of account holder's followers.
        """
        return self.user["followers_count"]

    def get_user_role(self):  # Think about division by zero prioblem
        """
        user role measures the ratio of followers to followees of a user. A user with a high follower to followee ratio is a
        broadcaster. Conversely, a user with a low follower to followee ratio is a receiver.
        :return: a float number shoing the ratio of followers to friends.
        """
        try:
            return (self.get_followers_count()) / (self.get_friends_count())
        except ZeroDivisionError:
            print("This user does not have any friend")
            return np.nan

    def get_user_reputation(self):
        """
        this function measures the relative importance of a user on Twitter. The reputation is defined as the ratio
        between the number of friends and the number of followers as: (followers #) / (followers # + friends #).
        :return: a float number showing the ratio (followers #) / (followers # + friends #).
        """

        try:
            return (self.get_followers_count()) / (self.get_followers_count() + self.get_friends_count())
        except ZeroDivisionError:
            print("This user has neither friend or follower")
            return np.nan

    def get_account_birthday(self, output="object"):
        """
        It showsthe  date and time that the user account was created on Twitter.
        :param output: it can be either "object" or "string". By choosing the object, the datetime object will be returned
        and by selecting string, the string version of datetime object will be returned.
        :return: a string ot datetime object depending on the output parameter.
        """

        assert (output in ["object", "string"]), "the output has to be object or string"

        if output == "object":
            return datetime.datetime.strptime(self.user["created_at"], "%a %b %d %H:%M:%S %z %Y")
        elif output == "string":
            return self.user["created_at"]

    def get_account_age(self):
        """
        This function calculates the age of the account until today with the resolution of day.
        :return: the account age with the resolutiion of day.
        """
        today = datetime.datetime.now()
        account_creation_time = self.get_account_birthday()
        return (today.date() - account_creation_time.date()).days

    def get_user_total_likes_count(self):
        """
        The number of Tweets this user has liked in the account’s lifetime.
        :return: an integer show the number of Tweets that this account has liked in the account’s lifetime.
        """
        return self.user["favourites_count"]

    def get_statusses_count(self):
        """
        The number of Tweets (including retweets) issued by the user in the account's lifetime
        :return: an integer  showing the number of Tweets issued by the user.
        """
        return self.user["statuses_count"]

    def get_average_follow_speed(self):
        """
        this function calculates the average speed of this account in following other Twitter accounts.
        :return: a float number showing the average follow speed in this account.
        """
        return self.get_followers_count() / self.get_account_age()

    def get_being_followed_speed(self):
        """
        this function calculates the average speed of being followed by other accounts.
        :return: a float number showing the average speed of being followed by other accounts.
        """
        return self.get_friends_count() / self.get_account_age()

    def get_average_like_speed(self):
        """
        this function calculates the average speed of this account in liking tweets.
        :return: a float number showing the average like speed in this account.
        """
        return self.get_user_total_likes_count() / self.get_account_age()

    def get_average_status_speed(self):
        """
        this function calculates the average speed of this account in posting tweets.
        :return: a float number showing the average tweet speed in this account.
        """
        return self.get_statusses_count() / self.get_account_age()

    def get_user_verification_status(self):
        """
        this function shows the verification status of this account.
        :return: a boolean showing the verification status of this account.
        """
        return self.user["verified"]

    def user_has_profile_location(self):
        """
        this function shows the user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable.
        :return: a string showing the user-defined location for this account.
        """
        return True if self.user["location"] != None else False

    def user_has_profile_picture(self):
        """
        this function shows the user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable.
        :return: a string showing the user-defined location for this account.
        """
        return True if self.user["profile_image_url_https"] != None else False

    def get_user_profile_picture(self, saving_address):
        """
        this function download the user profile picture.
        :param saving_address: the address to save the photo.
        :return: a photo
        """
        """
        this function download the user profile picture.
        :return: a string showing the user-defined location for this account.
        """
        url = self.user["profile_image_url_https"]
        local_filename = url.split('/')[-1]
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(saving_address + local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        elif response.status_code == 404:
            print("the photo in the specified address is not found")
        else:
            return ("the error code: ", response.status_code)

    def user_has_profile_url(self):  # need to add url in class attributes
        """
        this function shows a URL provided by the user in association with their profile.
        :return: a string showing the url provided by the user.
        """
        return True if self.user["url"] != None else False

    def user_has_profile_description(self):
        """
        this function shows the user-defined string describing their account.
        :return: a string showing the user defined profile description.
        """
        return True if self.user["description"] != None else False

    def user_protected_profile(self):
        """
        this function shows the protection status of the account. When true, indicates that this user has chosen to
        protect his/her tweets.
        :return: a boolean showing the protection status of the account.
        """
        return True if self.user["protected"] == True else False

    # Your username cannot be longer than 15 characters.
    # A username can only contain alphanumeric characters (letters A-Z, numbers 0-9) with the exception of underscores
    # https://www.techwalla.com/articles/what-characters-are-allowed-in-a-twitter-name
    # https://help.twitter.com/en/managing-your-account/twitter-username-rules

    # FIND A WAY TO CAPTURE THE PERMUTATION OF UPPERCASE, LOWERCASE, AND NUMBERS AND UNDERSCORE IN USER SCREENNAME
    def user_profile_screen_name_analysis(self):
        """
        This function analyses the length , the number of digits, letters and underscores in the screen name. These are
        the only valid characters in the screen names.
        :return: a dictionary that shows the number of characters, digits, letters and underscores in the screen name.
        """
        return {"digit_count": len([i for i in self.get_screen_name() if i in [str(dig) for dig in range(0, 10)]]),
                "letter_count": len([i for i in self.get_screen_name() if i.isalpha()]),
                "underscore_count": len([i for i in self.get_screen_name() if i == "_"]),
                "screen_name_length": len(self.get_screen_name())
                }


class singleTweet:
    def __init__(self, tweet_path, param):
        """
        This is the constructor of singleTweet.
        :param tweet_path: an individual tweet path.
        :param param: a dictionary of necessary objects and modules.
        """
        self.tweet = json.load(open(tweet_path))
        self.parameters = param
        self.text = ""

    def get_entities(self):
        """
        This function extracts the full tweet entities including hashtags, mentions, urls, photos, videos, gifs, and symbols
         from a tweet object.
        :return: a dictionary containing all the entities.
        """
        if not self.is_retweeted():
            if self.tweet["truncated"]:
                tweet_entities = self.tweet["extended_tweet"]["entities"]
                if "extended_entities" in self.tweet["extended_tweet"].keys():
                    tweet_entities["media"] = self.tweet["extended_tweet"]["extended_entities"]["media"]
            else:
                tweet_entities = self.tweet["entities"]
                if "extended_entities" in self.tweet.keys():
                    tweet_entities["media"] = self.tweet["extended_entities"]["media"]
        elif self.is_retweeted():
            if self.tweet["retweeted_status"]["truncated"]:
                tweet_entities = self.tweet["retweeted_status"]["extended_tweet"]["entities"]
                if "extended_entities" in self.tweet["retweeted_status"]["extended_tweet"].keys():
                    tweet_entities["media"] = self.tweet["retweeted_status"]["extended_tweet"]["extended_entities"][
                        "media"]
            else:
                tweet_entities = self.tweet["retweeted_status"]["entities"]
                if "extended_entities" in self.tweet["retweeted_status"].keys():
                    tweet_entities["media"] = self.tweet["retweeted_status"]["extended_entities"]["media"]
        return tweet_entities

    def get_tweet(self):
        """
        :return: the tweet as a json file
        """
        return self.tweet

    def get_url(self):
        """
        this function builds the tweet url.
        :return: a string of tweet url.
        """
        return "https://twitter.com/" + self.get_twitter().get_screen_name() + "/status/" + str(self.get_id())

    def get_twitter(self):
        """
        :return: the user object embedded in the tweet object.
        """
        return user(self.tweet["user"])

    def get_creation_time(self, output="object"):
        """
        It shows the creation time and date of a tweet.
        :param output: it can be either "object", "original_string", or "improved_string". By choosing the original_string
        the created_at field of tweet object is returned. By choosing object, a datetime object of the tweet creation time
        including year, month, day, hour, minute and second is returned. "improved_string" returns the string version of
        the datetime object.
        :return: a string or datetime object of the tweet creation time.
        """

        assert (output in ["object", "original_string",
                           "improved_string"]), "the output has to be object or original_string, or" \
                                                "improved_string"

        if output == "object":
            return datetime.datetime.strptime(datetime.datetime.strftime(
                datetime.datetime.strptime(self.tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S"),
                "%Y %m %d %H %M %S")
        elif output == "original_string":
            return self.tweet["created_at"]
        elif output == "improved_string":
            return datetime.datetime.strftime(
                datetime.datetime.strptime(self.tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S")

    def get_source(self):
        """
        :return: a string showing th utility used to post the Tweet.
        """
        return self.tweet["source"]

    def get_likes_count(self):
        """
        :return: an integer which indicates approximately how many times this Tweet has been liked by Twitter users
        """
        return self.tweet["favorite_count"]

    def get_retweet_count(self):
        """
        :return: an integer which indicates how many times this tweet has been retweeted.
        """
        return self.tweet["retweet_count"]

    def get_language(self):
        """
        :return: a string showing the language of the tweet.
        """
        return self.tweet["lang"]

    def get_place(self):
        """
        When present, indicates that the tweet is associated (but not necessarily originating from) a Place.
        :return: a place object.
        """
        return self.tweet["place"]

    def get_coordinates(self):
        """
        Represents the geographic location of this Tweet as reported by the user or client application.
        :return: a coordinate object
        """
        return self.tweet["coordinates"]

    def get_tweet_urls(self):
        """
        :return: a list of urls in this tweet.
        """
        return self.get_entities()["urls"]

    def get_hashtags(self):
        """
        :return: a list of hashtags in this tweet.
        """
        entities = self.get_entities()
        if "hashtags" in entities:
            return entities["hashtags"]
        else:
            return []

    def get_mentions(self):
        """
        :return: a list of mentions in this tweet.
        """
        entities = self.get_entities()
        if "hashtags" in entities:
            return entities["user_mentions"]
        else:
            return []

    def get_symbols(self):
        """
        :return: a list of symbols in this tweet.
        """
        entities = self.get_entities()
        if "hashtags" in entities:
            return entities["symbols"]
        else:
            return []

    def get_media(self):
        """
        :return: it returns the photo(s), video, and animated-gif attached to this tweet as a list.
        """
        entities = self.get_entities()
        if "media" in entities:
            return entities["media"]
        else:
            return []

    def get_photo(self):
        """
        :return: it returns the photo(s) attached to this tweet as a list.
        """
        media = self.get_media()
        photos = []
        for medium in media:
            if medium["type"] == "photo":
                photos.append(medium)
        return photos

    def get_video(self):
        """
        :return: it returns the video attached to this tweet in a list.
        """
        media = self.get_media()
        videos = []
        for medium in media:
            if medium["type"] == "video":
                videos.append(medium)
        return videos

    def get_gif(self):
        """
        :return: it returns the animated-gif attached to this tweet as a list.
        """
        media = self.get_media()
        gifs = []
        for medium in media:
            if medium["type"] == "animated_gif":
                gifs.append(medium)
        return gifs

    def get_text(self):  ## Maybe you need to check this function for retweet and quote class
        """
        :return: a string showing the full text of this tweet
        """
        if self.text != "":
            return self.text
        else:
            if not self.is_retweeted():
                if self.tweet["truncated"]:
                    tweet_text = self.tweet["extended_tweet"]["full_text"]
                else:
                    if "full_text" in self.tweet:
                        tweet_text = self.tweet["full_text"]
                    else:
                        tweet_text = self.tweet["text"]
            elif self.is_retweeted():
                if self.tweet["retweeted_status"]["truncated"]:
                    tweet_text = self.tweet["retweeted_status"]["extended_tweet"]["full_text"]
                else:
                    tweet_text = self.tweet["retweeted_status"]["text"]
            return tweet_text

    def get_id(self):
        """
        :return: an integer showing the unique id of this tweet.
        """
        return self.tweet["id"]

    def is_retweeted(self):
        """
        :return: a boolean shows whether this tweet is retweeted or not.
        """
        return True if "retweeted_status" in self.tweet.keys() else False

    def is_quoted(self):
        """
        :return: a boolean showing whether this is a quoted tweet or not..
        """
        return True if "quoted_status" in self.tweet.keys() else False

    def get_quote(self):
        """
        :return: it returns the quoted part of the this tweet..
        """
        return quoteClass(self.tweet["quoted_status"], self.parameters) if self.is_quoted() else None

    def get_retweeted(self):
        """
        :return: it returns the retweeted part of this tweet.
        """
        return retweetedClass(self.tweet["retweeted_status"], self.parameters) if self.is_retweeted() else None

    def tweet_source_status(self):
        """
        :return: a boolean that shows whether this tweet is posted by an official source or not.
        """
        official_clients = ["Twitter for iPhone", "Twitter for Android", "Twitter Web Client", "Twitter for iPad",
                            "Mobile Web (M5)", "TweetDeck", "Facebook", "Twitter for Windows", "Mobile Web (M2)",
                            "Twitter for Windows Phone", "Mobile Web", "Google", "Twitter for BlackBerry",
                            "Twitter for Android Tablets", "Twitter for Mac", "iOS", "Twitter for BlackBerry®"]
        soup = BeautifulSoup(self.get_source(), "html.parser")
        client = soup.text
        return True if client in official_clients else False

    def tweet_stemming(self, input_text=None, inplace=False):
        """
        This function performs the stemming operation using Porter algorithm.
        :param input_text: if this parameter is None, then stemming is applied on the text field of the caller object, otherwise
        and in case of a string as an input for this parameter, the stemming is applied on the input text.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after stemming.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently and
        returns the whole object, in contrast when it is equal to False the function only returns the text field after
        the stemming without changing the text field.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        stemmed = PorterStemmer().stem(text)
        if inplace:
            self.text = stemmed
            return self
        else:
            return stemmed

    def hashtag_splitter(self, input_text=None, inplace=False):
        """
        This function slices up hashtags as in most of the times, hashtags are made up of concatanation of meaningful words.
        :param input_text: if this parameter is None, then slicing is applied on the hashtags of the caller object, otherwise
        and in case of a string as an input for this parameter, the slicing is applied on the input text.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after slicing up the hashtags.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
        by splitting the hashtags and returning the whole object, in contrast when it is equal to False the function only
        returns the text field after slicing up the hashtags without changing the text field.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        hashtags = self.get_hashtags()

        if len(hashtags) > 0:
            for hashtag in hashtags:
                hashtag_text = hashtag["text"]
                if text.isupper():
                    pat = r'[A-Z0-9]+[a-z0-9]*'
                    replacement = " ".join(re.findall(pat, hashtag_text))
                    text = text.replace(hashtag_text, replacement)
                else:
                    replacement = " ".join(wordninja.split(hashtag_text))
                    text = text.replace(hashtag_text, replacement)

        if inplace:
            self.text = text
            return self
        else:
            return text

    def mention_replacement(self, input_text=None, inplace=False):
        """
        This function replaces Twitter account mentions by the accounts' screen name.
        :param input_text: if this parameter is None, then the replacement is applied on the mention of the caller object,
        otherwise and in case of a string as an input for this parameter, the replacement is applied on the input text.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after replacing the mentions.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
        by replacing the mentions with the accounts screen names and returning the whole object, in contrast when it is equal
        to False the function only returns the text field after replacing the mentions without changing the text field.
        """
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        mentions = self.get_mentions()
        for mention in mentions:
            text = text.replace(mention["screen_name"], mention["name"])

        if inplace:
            self.text = text
            return self
        else:
            return text

    def url_removal(self, input_text=None, inplace=False):
        """
        This function removes the urls from the tweet text.
        :param input_text: if this parameter is None, then the urls are removed from the caller object text, otherwise
        and in case of a string as an input for this parameter, the urls are removed from the input text.
        :param inplace: if inplace is True, the url removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the urls.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
        by removing the urls and returning the whole object, in contrast when it is equal to False the function only
        returns the text field after url removal.
        """
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        extractor = URLExtract()
        urls = extractor.find_urls(text)
        for url in urls:
            text = text.replace(url, "")
        if inplace:
            self.text = text
            return self
        else:
            return text

    def hashtags_removal(self, input_text=None, mode=2, inplace=False):
        """
        This function removes hashtags from tweet text according to different modes.
        :param input_text: if this parameter is None, then the hashtag removal is applied on the caller object,
        otherwise and in case of a string as an input for this parameter, the hashtag removal is applied to the input text.
        :param mode: there are three modes for hashtags removal. In mode 1, the text remains intact, in Mode 2, only the
        hashtag characters (#) are removed, and in mode 3, the whole hashtags consisting the hashtag character and the terms
        after the hashtags are removed.
        :param inplace: if inplace is True, the hashtag removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the hashtags.
        :return: when the implace parameter is equal to True, the function removes the hashtags permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         hashtags from the text.
        """

        assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if mode == 1:
            pass
        elif mode == 2:
            text = text.replace("#", "")
        elif mode == 3:
            for h in self.get_hashtags():
                text = text.replace("#" + h["text"], "")
        if inplace:
            self.text = text
            return self
        else:
            return text

    def mentions_removal(self, input_text=None, mode=2, inplace=False):
        """
        This function removes mentions from tweet text according to different modes.
        :param input_text: if this parameter is None, then the mention removal is applied on the caller object,
        otherwise and in case of a string as an input for this parameter, the mention removal is applied to the input text.
        :param mode: there are three modes for mention removal. In mode 1, the text remains intact, in Mode 2, only the
        mention characters (@) are removed, and in mode 3, the whole mention consisting the mention character and the terms
        after the mentions are removed.
        :param inplace: if inplace is True, the mention removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the mention.
        :return: when the implace parameter is equal to True, the function removes the mentions permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         mentions from the text.
        """

        assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if mode == 1:
            pass
        elif mode == 2:
            text = text.replace("@", "")
        elif mode == 3:
            for m in self.get_mentions():
                text = text.replace("@" + m["screen_name"], "")
        if inplace:
            self.text = text
            return self
        else:
            return text

    def control_characters_removal(self, input_text=None, inplace=False):
        """
        This functions removes common control characters carriage return (\r), line feed (\n), horizontal tab (\t).
        :param input_text: if this parameter is None, then the control characters are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the control characters are removed from the input text.
        :param inplace: if inplace is True, the control characters removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the control characters.
        :return: when the implace parameter is equal to True, the function removes the control characters permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         control characters from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        pattern = re.compile(r'[\r\t\n]')
        text = pattern.sub(" ", text)
        if inplace:
            self.text = text
            return self
        else:
            return text

    def stopwords_removal(self, input_text=None, stopword_corpus="stone", inplace=False):
        """
        This function removes stopwords from the tweet according to chosen stopword corpus.
        :param input_text: if this parameter is None, then the stopwords are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the stopwords are removed from the input text.
        :param stopword_corpus: The stopword corpus can be "stone", "nltk", "corenlp", or "glascow". Almost every text mining
         framework uses one of these corpuses for removing the stopwords.
        :param inplace: if inplace is True, the stopwords removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the stopwords.
        :return: when the implace parameter is equal to True, the function removes the stopwords permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
        stopwords from the text.
        """

        assert (stopword_corpus in ["stone", "nltk", "corenlp",
                                    "glascow"]), "stopword_orpus can be stone, nltk, corenlp, and glascow"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(text)
        if stopword_corpus == "stone":
            processed_text = " ".join(
                [word for word in words if word.lower() not in self.parameters["stopwords"]["stone"]])
        elif stopword_corpus == "nltk":
            processed_text = " ".join(
                [word for word in words if word.lower() not in self.parameters["stopwords"]["nltk"]])
        elif stopword_corpus == "corenlp":
            processed_text = " ".join(
                [word for word in words if word.lower() not in self.parameters["stopwords"]["corenlp"]])
        elif stopword_corpus == "glascow":
            processed_text = " ".join(
                [word for word in words if word.lower() not in self.parameters["stopwords"]["glascow"]])

        if inplace:
            self.text = processed_text
            return self
        else:
            return processed_text

    def whitespace_removal(self, input_text=None, inplace=False):
        """
        This functions removes whitespaces from the text.
        :param input_text: if this parameter is None, then the whitespaces are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the whitespaces are removed from the input text.
        :param inplace: if inplace is True, the whitespace removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the whitespaces.
        :return: when the implace parameter is equal to True, the function removes the whitespaces permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         whitespaces from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        text = text.strip()
        while (text.count("  ") > 0):
            text = text.replace("  ", " ")
        if inplace:
            self.text = text
            return self
        else:
            return text

    def punctuation_removal(self, input_text=None, inplace=False):
        """
        This functions removes punctuation characters from the text.
        :param input_text: if this parameter is None, then the punctuations are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the punctuations are removed from the input text.
        :param inplace: if inplace is True, the punctuations removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the punctuations.
        :return: when the implace parameter is equal to True, the function removes the punctuations permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         punctuations from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        punctuation_free = textstat.remove_punctuation(text).replace(".", "").replace("\"", "").replace("“",
                                                                                                        "").replace("”",
                                                                                                                    "").strip()
        if inplace:
            self.text = punctuation_free
            return self
        else:
            return punctuation_free

    def text_preprocessing(self, input_text=None, url=True, case=True, punctuation=True, hashtag=2, mention=2,
                           whitespace=True, control_characters=True, stop="stone", hashtag_split=True,
                           mention_replacement=True):
        """
        This function preprocess the tweet text.
        :param input_text: if this parameter is None, then preprocessing is performed on the caller object text field,
        otherwise and in case of a string as an input for this parameter, the preprocessing is applied on the input text.
        :param url: by setting this boolean parameter True, the tweet urls are removed.
        :param case: setting this boolean parameter True, turns the tweet text to lower case.
        :param punctuation: by setting this boolean parameter True, the tweet punctuations are removed.
        :param hashtag: this integer parameter represents the hashtag removal mode. There are three modes for
        hashtags removal. In mode 1, the text remains intact, in Mode 2, only the hashtag characters (#) are removed,
        and in mode 3, the whole hashtags consisting the hashtag character and the terms after the hashtags are removed.
        :param mention: this integer parameter represents the mention removal mode. There are three modes for
        mention removal. In mode 1, the text remains intact, in Mode 2, only the mention characters (@) are removed,
        and in mode 3, the whole mention consisting the hashtag character and the terms after the hashtags are removed.
        :param whitespace: by setting this boolean parameter True, the tweet whitespaces are removed.
        :param control_characters: by setting this boolean parameter True, the common control characters (carriage return(\r),
        line feed(\n), and horizontal tab(\t)) are removed.
        :param stop: this string parameter represents the stopwords corpus for stopword removal. The stopword corpus can
        be "stone", "nltk", "corenlp", or "glascow". Almost every text mining framework uses one of these corpuses for
        removing the stopwords. In order to seactivates stopwords removal, this parameter has to be set to False.
        :param hashtag_split: by setting this parameter to True, the hashtags are splitted and replaced in the text.
        :param mention_replacement: by setting this parameter to True, the mentions are replaced by their corresponding screen names.
        :return: when the implace parameter is equal to True, the function applies the preprocessing permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after preprocessing.
        """

        assert (url in [True, False]), "url parameter can be True or False"
        assert (case in [True, False]), "case parameter can be True or False"
        assert (punctuation in [True, False]), "punctuation parameter can be True or False"
        assert (hashtag in [1, 2, 3]), "hashtag parameter can be 1, 2, 3"
        assert (mention in [1, 2, 3]), "mention parameter can be 1, 2, 3"
        assert (whitespace in [True, False]), "whitespace parameter can be True or False"
        assert (control_characters in [True, False]), "control_characters parameter can be True or False"
        assert (stop in ["stone", "nltk", "corenlp", "glascow",
                         False]), "stop parameter can be stone, nltk, corenlp, glascow, or False"
        assert (hashtag_split in [True, False]), "hashtag_split parameter can be True or False"
        assert (mention_replacement in [True, False]), "mention_replacement parameter can be True or False"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if control_characters == True:
            text = self.control_characters_removal(input_text=text)

        if url == True:
            text = self.url_removal(input_text=text)

        if mention_replacement == True:
            text = self.mention_replacement(input_text=text)

        if hashtag == 1:
            pass
        elif hashtag == 2:
            text = self.hashtags_removal(input_text=text, mode=2)
        elif hashtag == 3:
            text = self.hashtags_removal(input_text=text, mode=3)

        if hashtag_split == True:
            text = self.hashtag_splitter(input_text=text)

        if mention == 1:
            pass
        elif mention == 2:
            text = self.mentions_removal(input_text=text)
        elif mention == 3:
            text = self.mentions_removal(input_text=text)

        if case == True:
            text = text.lower()

        if stop != False:
            text = self.stopwords_removal(input_text=text, stopword_corpus=stop)

        if punctuation == True:
            text = self.punctuation_removal(input_text=text)

        if whitespace == True:
            text = self.whitespace_removal(input_text=text)

        #         if contraction == True

        return text

    def tweet_pos(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding Part-of-Speech (POS) tag.
        :param input_text: if this parameter is None, then the Part-of-Speech (POS) tagging is performed on the caller object text field,
        otherwise and in case of a string as an input for this parameter, the Part-of-Speech tagging is performed on the input text.
        :return: this function returns the POS tagged version of the tweet.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        text = self.text_preprocessing(input_text=text)
        pos_text = ""
        spacy_text = self.parameters["spacy"](text)
        for token in spacy_text:
            pos_text = pos_text + " " + token.pos_
        return pos_text.strip()

    def tweet_ner(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding Named-Entity-Recognition (NER) tag.
        :param input_text: if this parameter is None, then the Named-Entity-Recognition (NER) tagging is performed on the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        NER tagging is performed on the input text.
        :return: this function returns the Named-Entity-Recognition (NER) tagged version of the tweet.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        text = self.text_preprocessing(input_text=text)

        ner_text = ""
        spacy_text = self.parameters["spacy"](text)
        for token in spacy_text.ents:
            ner_text = ner_text + " " + token.label_

        return ner_text.strip()

    def tweet_lemmatization(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding lemma.
        :param input_text: if this parameter is None, then the lemmatization is performed on the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        lemmatization is performed on the input text.
        :return: this function returns the lemmatized version of the tweet.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        text = self.text_preprocessing(input_text=text)

        tweet_lemmas = ""
        spacy_text = self.parameters["spacy"](text)
        for token in spacy_text:
            tweet_lemmas = tweet_lemmas + " " + token.lemma_

        return tweet_lemmas.strip()

    def tweet_tokens(self, preprocessing=True, lemmatization=True, input_text=None):
        """
        This function tokenises the tweet text field. If any customized preprocessing is required, the preprocessing can
        be set to False and text_preprocessing function with arbitrary settings is called and feed to input_text parameter.
        :param preprocessing: if this parameter is set to True, the default preprocessing is perfomed on tweet text.
        :param lemmatization: if this parameter is set to True, the lemmatization is performed on the tweet text.
        :param input_text: if this parameter is None, then the tokenisation is performed on the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        tokenisation is performed on the input text.
        :return: a list of tokens.
        """

        assert (preprocessing in [True, False]), "preprocessing is a boolean parameter, so it can be True or False"
        assert (lemmatization in [True, False]), "lemmatization is a boolean parameter, so it can be True or False"

        if input_text == None:
            if preprocessing and lemmatization:
                return self.tweet_splitter(self.tweet_lemmatization(self.text_preprocessing(self.get_text())))
            elif preprocessing and lemmatization == False:
                return self.tweet_splitter(self.text_preprocessing(self.get_text()))
            elif preprocessing == False and lemmatization:
                return self.tweet_splitter(self.tweet_lemmatization(self.get_text()))
            elif preprocessing == False and lemmatization == False:
                return self.tweet_splitter(self.get_text())
        else:
            if preprocessing and lemmatization:
                return self.tweet_splitter(self.tweet_lemmatization(self.text_preprocessing(input_text=input_text)))
            elif preprocessing and lemmatization == False:
                return self.tweet_splitter(self.text_preprocessing(input_text=input_text))
            elif preprocessing == False and lemmatization:
                return self.tweet_splitter(self.tweet_lemmatization(input_text=input_text))
            elif preprocessing == False and lemmatization == False:
                return self.tweet_splitter(input_text=input_text)

    def get_emojis(self, count=True, emoji_list=True, input_text=None):
        """
        This function collects the emojis from tweet text.
        :param count: if this is set to True, the function counts the number of emojis in the tweet.
        :param emoji_list: if this is set to True, the function collects the emojis in the tweet.
        :param input_text: if this parameter is None, then the emojis are extracted from the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        emojis are extracted from the input text.
        :return: if both parameters are set to True, then the function returns a dictionary containing the list of emojis and
        their number. if only count is set to True, the number of emojis is returned and if emoji_list is set to True, the
        list of emojis is returned.
        """
        assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
        assert (emoji_list in [True, False]), "emoji_list is a boolean parameter, so it can be True or False"
        assert (count or emoji_list), "at least one of the count and emoji_list parameters " \
                                      "has to be set to True"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        emojis = emoji.emoji_lis(text)
        if emoji_list == True and count == True:
            return {"emoji_count": len(emojis), "emoji_list": emojis}
        elif emoji_list == True and count == False:
            return emojis
        elif emoji_list == False and count == True:
            return len(emojis)

            # Emoticon analysos <= doesn't work properly

    def get_emoticon(self, count=True, emoticon_list=True, input_text=None):
        """
        This function collects the emoticons from tweet text.
        :param count: if this is set to True, the function counts the number of emoticons in the tweet.
        :param emoji_list: if this is set to True, the function collects the emoticons in the tweet.
        :param input_text: if this parameter is None, then the emoticons are extracted from the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        emoticons are extracted from the input text.
        :return: if both parameters are set to True, then the function returns a dictionary containing the list of emoticons and
        their number. if only count is set to True, the number of emoticons is returned and if emoticons_list is set to True, the
        list of emoticons is returned.
        """
        assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
        assert (emoticon_list in [True, False]), "emoticon_list is a boolean parameter, so it can be True or False"
        assert (count or emoticon_list), "at least one of the count and emoticon_list parameters " \
                                         "has to be set to True"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(text)
        emoticons = [word for word in words if word in self.parameters["emoticons"]]

        if emoticon_list == True and count == True:
            return {"emoticons_count": len(emoticons), "emoticon_list": emoticons}
        elif emoticon_list == True and count == False:
            return emoticons
        elif emoticon_list == False and count == True:
            return len(emoticons)

    def tweet_splitter(self, input_text=None, unit="word"):
        """
        this function splits the tweet text field according to chosen splitting unit.
        :param input_text: if this parameter is None, then the caller object text field is splitted, otherwise
        and in case of a string as an input for this parameter, the input text is splitted up.
        :param unit: the splitting unit can be "word", or "sentence".
        :return: a list containing the splitting units.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if unit == "word":
            return re.findall(r'\S+', text)
        elif unit == "sentence":
            return [i for i in re.split(r'[.?!]+', text) if i != '']

    def text_length(self, input_text=None, unit="word"):
        """
        this function measures the length of the tweet based on the selected length unit.
        :param input_text: if this parameter is None, then the length of caller object text field is measured, otherwise
        and in case of a string as an input for this parameter, the length of input text is measured.
        :param unit: the length unit can be "character", "word", or "sentence".
        :return: an integer showing the length of the tweet text field.
        """

        assert (unit in ["character", "word", "sentence"]), "the unit can be character, word, or sentence"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if unit == "character":
            return len(text)
        elif unit == "word":
            return len(self.tweet_splitter(unit="word", input_text=text))
        elif unit == "sentence":
            return len(self.tweet_splitter(unit="sentence", input_text=text))

    def text_complexity(self, input_text=None, unit="word"):
        """
        this function measures the complexity of a tweet text based on the selected complexity unit.
        :param input_text: if this parameter is None, then the complexity of caller object text field is measured, otherwise
        and in case of a string as an input for this parameter, the complexity of input text is measured.
        :param unit: the length unit can be "word", "sentence", or "syllables".
        :return: an float showing the complexity of the tweet text.
        """

        assert (unit in ["word", "sentence", "syllables"]), "unit parameter can be word, sentence, or syllables"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if unit == "word":
            return np.average([len(word) for word in self.tweet_splitter(unit="word", input_text=text)])
        elif unit == "sentence":
            return np.average([len(self.tweet_splitter(unit="word", input_text=sentence)) for sentence in
                               self.tweet_splitter(unit="sentence", input_text=text)])
        elif unit == "syllables":
            return np.average(
                [textstat.syllable_count(i, lang='en_US') for i in self.tweet_splitter(unit="word", input_text=text)])

    def text_pronoun_count(self, input_text=None, pronoun="third_singular"):
        """
        This function counts the number of pronouns in the tweet text according to selected pronoun for counting.
        :param input_text: if this parameter is None, then the number of chosen pronoun in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of chosen pronoun in the
        input_text is counted.
        :param pronoun: the pronoun can be "first_singular", "first_plural", "second_singular", "second_plural", "third_singular", or
        "third_plural".
        :return: an integer showing the number of chosen pronoun in the tweet text.
        """

        assert (pronoun in ["first_singular", "first_plural", "second_singular", "second_plural", "third_singular",
                            "third_plural"]), "the pronoun parameter can be first_singular, first_plural, second_singular, second_plural, " \
                                              "third_singular, or third_plural"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = [i.lower() for i in self.tweet_splitter(unit="word", input_text=text)]
        if pronoun == "first_singular":
            return words.count("i") + words.count("my") + words.count("mine") + words.count("me") + words.count(
                "myself") + words.count("i'm") + words.count("i've") + words.count("i'd") + words.count("i'll")
        elif pronoun == "first_plural":
            return words.count("we") + words.count("our") + words.count("ours") + words.count("us") + words.count(
                "ourselves") + words.count("we're") + words.count("we've") + words.count("we'd") + words.count("we'll")
        elif pronoun == "second_singular":
            return words.count("you") + words.count("your") + words.count("yours") + words.count(
                "yourself") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
                "you'll")
        elif pronoun == "second_plural":
            return words.count("you") + words.count("your") + words.count("yours") + words.count(
                "yourselves") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
                "you'll")
        elif pronoun == "third_singular":
            return words.count("he") + words.count("she") + words.count("it") + words.count("his") + words.count(
                "her") + words.count("its") + words.count("him") + words.count("hers") + words.count(
                "he's") + words.count("she's") + words.count("it's") + words.count("he'll") + words.count(
                "she'll") + words.count("it'll") + + words.count("he'd") + words.count("she'd") + words.count("it'd")
        elif pronoun == "third_plural":
            return words.count("they") + words.count("them") + words.count("their") + words.count(
                "theirs") + words.count("themselves") + words.count("they're") + words.count("they've") + words.count(
                "they'd") + words.count("they'll")

    def case_analysis(self, count=True, frac=True, unit="character",
                      input_text=None):  #### THINK ABOUT DIVISION BY ZERO ERROR ####
        """
        This function analyses the count and fraction of upper and lower letters or capital and small words in the tweet text
        depending on the selected unit of analysis.
        :param count: if this is set to True, the function count the number of upper and lower letters or capital and small words
        in the tweet text.
        :param frac: if this is set to True, the function measures the fraction of  upper and lower letters or capital and small words
        in the tweet text.
        :param unit: the unit parameter can be word or character.
        :param input_text: if this parameter is None, then the case analysis is performed on the caller object text field
        , otherwise and in case of a string as an input for this parameter, the case analysis is performed on the input_text.
        :return: it returns a dictionary which its content depends on the parameters value. If the unit of analysis is
        set to character, depending on the value of count and frac parameters, the dictionary contains
        either the number of lowercase and uppercase characters, or ratio of lowercase and uppercase characters to all characters,
        or both. If the unit of analysis is set to word, then depending on the value of count and frac parameters,
        the dictionary contains either the number of capital and small words, or ratio of capital and small words to
        all words, or both.
        """

        assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
        assert (frac in [True, False]), "frac is a boolean parameter, so it can be True or False"
        assert (unit in ["character", "word"]), "unit can be character or word"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if unit == "character":
            uppercase_character_count = sum(1 for i in text if i.isupper())
            lowercase_character_count = sum(1 for i in text if i.islower())
            character_count = self.text_length(unit="character", input_text=text)
            if count == True and frac == True:  ######### THINK ABOUT DIVISION BY ZERO ERROR ###
                try:
                    return {"uppercase_character_count": uppercase_character_count,
                            "lowercase_character_count": lowercase_character_count,
                            "uppercase_to_lowercase": uppercase_character_count / lowercase_character_count,
                            "lowercase_to_all_characters": lowercase_character_count / character_count,
                            "uppercase_to_all_characters": uppercase_character_count / character_count}
                except ZeroDivisionError:
                    if character_count == 0:
                        print(
                            "the number of characters is zero, consequently the number of lowercase character is zero")
                    elif lowercase_character_count == 0:
                        print("the number of lowercase characters is zero")

            elif count == True and frac == False:
                return {"uppercase_character_count": uppercase_character_count,
                        "lowercase_character_count": lowercase_character_count}
            elif count == False and frac == True:
                try:
                    return {"uppercase_to_lowercase": uppercase_character_count / lowercase_character_count,
                            "lowercase_to_all_characters": lowercase_character_count / character_count,
                            "uppercase_to_all_characters": uppercase_character_count / character_count}
                except ZeroDivisionError:
                    if character_count == 0:
                        print(
                            "the number of characters is zero, consequently the number of lowercase characters is zero")
                    elif lowercase_character_count == 0:
                        print("the number of lowercase characters is zero")

        elif unit == "word":
            words = self.tweet_splitter(unit="word", input_text=text)
            capital_words_count = len([b for b in words if b.isupper()])
            small_words_count = len([b for b in words if b.islower()])
            words_count = len(words)
            if count == True and frac == True:
                try:
                    return {"capital_words_count": capital_words_count, "small_words_count": small_words_count,
                            "capital_to_small": capital_words_count / small_words_count,
                            "capital_to_all_words": capital_words_count / words_count,
                            "small_to_all_words": small_words_count / words_count}
                except ZeroDivisionError:
                    if words_count == 0:
                        print("the number of words is zero, consequently the number of snall words is zero")
                    elif small_words_count == 0:
                        print("the number of small words is zero")

            elif count == True and frac == False:
                return {"capital_words_count": capital_words_count, "small_words_count": small_words_count}
            elif count == False and frac == True:
                try:
                    return {"capital_to_small": capital_words_count / small_words_count,
                            "capital_to_all_words": capital_words_count / words_count,
                            "small_to_all_words": small_words_count / words_count}
                except ZeroDivisionError:
                    if words_count == 0:
                        print("the number of words is zero, consequently the number of snall words is zero")
                    elif small_words_count == 0:
                        print("the number of small words is zero")

    def exclamation_mark_count(self, input_text=None):
        """
        This function counts the number of exclamation mark in  the tweet text field.
        :param input_text: if this parameter is None, then the number of exclamation mark in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of exclamation mark in the
         input_text is counted.
        :return: an integer showing the number of exclamation mark in the tweet text.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        return text.count("!")

    def question_mark_count(self, input_text=None):
        """
        This function counts the number of question marks in the tweet text field.
        :param input_text: if this parameter is None, then the number of question marks in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of question marks in the
         input_text is counted.
        :return: an integer showing the number of question marks in the tweet text.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text
        return text.count("?")

    def abbreviations(self, input_text=None):
        """
        This function finds the abbreviations used in tweet text.
        :param input_text: if this parameter is None, then the function finds the abbreviations used in the caller object text field
        , otherwise and in case of a string as an input for this parameter, the function finds the abbreviations in the
        input_text.
        :return: a list of abbreviations used in the tweet text.
        """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(unit="word", input_text=text)
        return [i for i in words if i in self.parameters["abbr"]]

    def vulgar_words(self, input_text=None):
        """
         This function finds the vulgar terms used in tweet text.
         :param input_text: if this parameter is None, then the function finds the vulgar terms used in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function finds the vulgar terms in the
         input_text.
         :return: a list of vulgar terms used in the tweet text.
         """
        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(unit="word", input_text=text)
        return [i for i in words if i in self.parameters["vulgar"]]

    def sentiment_analysis(self, sentiment_engine="vader", input_text=None):
        """
        This function performs sentiment analysis over tweet text field using various sentiment analysis engines
        :param sentiment_engine: sentiment_engine can be "textblob", "vader", "nrc", "hate_speech", or "vad".
        :param input_text: if this parameter is None, then the function measure the sentiment of the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function measures the sentiment of the
         input_text.
        :return: it returns a dictionary containing various sentiment scores depending on the chosen sentiment_engine. If
        it is textblob, the sentiment scores are polarity and subjectivity. If it vader, the scores are positivity, negativity,
        neutrality, and composite score. If the sentiment_engine is nrc, then the sentiment scores are anger, disgust, sadness,
        anticipation, fear, surprise, joy, and trust. If the hate_speech engine is chosen, the scores  woud be hate_speech,
        offensive language, and neither. And finally, if the sentiment engine is vad, the scores would be valence, arousal,
        and dominance.
        """

        assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
                                     "vad"]), "the sentiment_engine has to be" \
                                              "textblob, vader, nrc, hate_speech, or vad"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if sentiment_engine == "textblob":
            return {"subjectivity": TextBlob(text).sentiment.subjectivity,
                    "polarity": TextBlob(text).sentiment.polarity}
        elif sentiment_engine == "vader":
            return {"positivity_score": self.parameters["vader"].polarity_scores(text)["pos"],
                    "negativity_score": self.parameters["vader"].polarity_scores(text)["neg"],
                    "neutrality_score": self.parameters["vader"].polarity_scores(text)["neu"],
                    "composite_score": self.parameters["vader"].polarity_scores(text)["compound"]}
        elif sentiment_engine == "nrc":
            nrc_text_list = self.tweet_splitter(unit="word", input_text=text)
            anger_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    anger_score += self.parameters["nrc"][term]["anger"]
            anticipation_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    anticipation_score += self.parameters["nrc"][term]["anticipation"]
            disgust_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    disgust_score += self.parameters["nrc"][term]["disgust"]
            fear_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    fear_score += self.parameters["nrc"][term]["fear"]
            joy_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    joy_score += self.parameters["nrc"][term]["joy"]
            sadness_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    sadness_score += self.parameters["nrc"][term]["sadness"]
            surprise_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    surprise_score += self.parameters["nrc"][term]["surprise"]
            trust_score = 0
            for term in nrc_text_list:
                if term in self.parameters["nrc"]:
                    trust_score += self.parameters["nrc"][term]["trust"]
            return {"anger_score": anger_score, "anticipation_score": anticipation_score,
                    "disgust_score": disgust_score, "fear_score": fear_score, "joy_score": joy_score,
                    "sadness_score": sadness_score, "surprise_score": surprise_score, "trust_score": trust_score}
        elif sentiment_engine == "hate_speech":
            sonar2 = self.parameters["sonar"].ping(text)
            return {"hate_speech": sonar2["classes"][0]["confidence"],
                    "offensive_language": sonar2["classes"][1]["confidence"],
                    "neither": sonar2["classes"][2]["confidence"]}
        elif sentiment_engine == "vad":
            word_list = self.tweet_splitter(unit="word", input_text=text)

            valence_score = 0
            for term in word_list:
                if term in self.parameters["vad"]:
                    valence_score += self.parameters["vad"][term]["valence"]

            arousal_score = 0
            for term in word_list:
                if term in self.parameters["vad"]:
                    arousal_score += self.parameters["vad"][term]["arousal"]

            dominance_score = 0
            for term in word_list:
                if term in self.parameters["vad"]:
                    dominance_score += self.parameters["vad"][term]["dominance"]

            return {"valence_score": valence_score, "arousal_score": arousal_score, "dominance_score": dominance_score}

    def readability(self, metric="flesch_kincaid_grade", input_text=None):
        """
        This function measures the readability of the tweet text according to the chosen readbility metric.
        :param metric: the readability metrics can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score"
        :param input_text: if this parameter is None, then the function measures the readability of the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function measures the readability of the
         input_text.
        :return:
        """

        assert (metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score"]), "The metric " \
                                                             "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                             "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                             "or dale_chall_readability_score."

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        if metric == "flesch_reading_ease":
            return textstat.flesch_reading_ease(text)
        elif metric == "flesch_kincaid_grade":
            return textstat.flesch_kincaid_grade(text)
        elif metric == "gunning_fog":
            return textstat.gunning_fog(text)
        elif metric == "smog_index":
            return textstat.smog_index(text)
        elif metric == "automated_readability_index":
            return textstat.automated_readability_index(text)
        elif metric == "coleman_liau_index":
            return textstat.coleman_liau_index(text)
        elif metric == "linsear_write_formula":
            return textstat.linsear_write_formula(text)
        elif metric == "dale_chall_readability_score":
            return textstat.dale_chall_readability_score(text)

    def long_words_count(self, threshold=6, input_text=None):
        """
        This function counts the number of words that are longer than a particular threshold.
        :param threshold: an integer showing the threshhold of long words.
        :param input_text: if this parameter is None, then the function counts the long words in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function counts the number of long words in the
         input_text.
        :return: an integer number showing the number of words which are longer than a particular threshhold.
        """

        assert (isinstance(threshold, int) and threshold > 0), "threshhold has to be a positive integer"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(unit="word", input_text=text)
        return len([i for i in words if len(i) > threshold])

    def multiple_syllables_count(self, threshold=2, input_text=None):
        """
        This function counts the number of words that their syllables number is more than a particular threshold.
        :param threshold: an integer showing the threshhold of syllables.
        :param input_text: if this parameter is None, then the function counts the number of syllables in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function counts the number of syllables in the
         input_text.
        :return: an integer number showing the number of wordsthat that their syllables number is higher than a particular threshold.
        """

        assert (isinstance(threshold, int) and threshold > 0), "threshhold has to be a positive integer"

        if input_text == None:
            text = self.get_text()
        else:
            text = input_text

        words = self.tweet_splitter(unit="word", input_text=text)
        return len([i for i in words if textstat.syllable_count(i, lang='en_US') > threshold])

    def get_tweet_photos(self, saving_address):
        photos = self.get_photo()
        for photo in photos:
            url = photo["media_url"]
            local_filename = url.split('/')[-1]
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(saving_address + local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                print("the photo in the specified address is not found")
            else:
                return ("the error code: ", response.status_code)

    def get_tweet_videos(self, saving_address):
        videos = self.get_video()  # So far, there is only possibility of uploading one single video in every tweet
        for video in videos:
            urls = video["video_info"]["variants"]
            for variant in urls:
                if variant['content_type'] == 'video/mp4':
                    url = variant["url"]
                    break
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                local_filename = url.split('/')[-1]
                reg = re.search(r'^.*\?', local_filename)
                file_name = local_filename[reg.start():reg.end()].replace("?", "")
                with open(saving_address + file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                print("the video in the specified address is not found")
            else:
                return ("the error code: ", response.status_code)

    def get_tweet_gifs(self, saving_address):
        gifs = self.get_gif()  # So far, there is only possibility of uploading one single gif in every tweet
        for gif in gifs:
            url = gif["video_info"]["variants"][0]["url"]
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = url.split('/')[-1]
                # reg = re.search(r'^.*\?', local_filename)
                # file_name = local_filename[reg.start():reg.end()].replace("?","")
                with open(saving_address + file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                print("the gif in the specified address is not found")
            else:
                return ("the error code: ", response.status_code)


class retweetedClass(singleTweet):
    def __init__(self, twt, para):
        """
        This is the constructor for the retweetedClass.
        :param twt: a tweet object.
        :param para: a dictionary of necessary objects and modules.
        """
        self.tweet = twt
        self.parameters = para

    def get_entities(self):
        """
        This function extracts the full retweet entities including hashtags, mentions, urls, photos, videos, gifs, and symbols
         from a tweet object.
        :return: a dictionary containing all the entities.
        """
        if self.tweet["truncated"]:
            tweet_entities = self.tweet["extended_tweet"]["entities"]
            if "extended_entities" in self.tweet["extended_tweet"].keys():
                tweet_entities["media"] = self.tweet["extended_tweet"]["extended_entities"]["media"]
        else:
            tweet_entities = self.tweet["entities"]
            if "extended_entities" in self.tweet.keys():
                tweet_entities["media"] = self.tweet["extended_entities"]["media"]
        return tweet_entities

    def get_text(self):  ## Maybe you need to check this function for retweet and quote class
        """
        :return: a string showing the full text of this retweet
        """
        if self.tweet["truncated"]:
            tweet_text = self.tweet["extended_tweet"]["full_text"]
        else:
            if "full_text" in self.tweet:
                tweet_text = self.tweet["full_text"]
            else:
                tweet_text = self.tweet["text"]
        return tweet_text


class quoteClass(singleTweet):
    def __init__(self, twt, para):
        """
        This is the constructor for the quoteClass.
        :param twt: a tweet object.
        :param para: a dictionary of necessary objects and modules.
        """
        self.tweet = twt
        self.parameters = para

    def get_entities(self):
        """
        This function extracts the full quote entities including hashtags, mentions, urls, photos, videos, gifs, and symbols
         from a tweet object.
        :return: a dictionary containing all the entities.
        """
        if self.tweet["truncated"]:
            tweet_entities = self.tweet["extended_tweet"]["entities"]
            if "extended_entities" in self.tweet["extended_tweet"].keys():
                tweet_entities["media"] = self.tweet["extended_tweet"]["extended_entities"]["media"]
        else:
            tweet_entities = self.tweet["entities"]
            if "extended_entities" in self.tweet.keys():
                tweet_entities["media"] = self.tweet["extended_entities"]["media"]
        return tweet_entities

    def get_text(self):  ## Maybe you need to check this function for retweet and quote class
        """
        :return: a string showing the full text of this retweet
        """
        if self.tweet["truncated"]:
            tweet_text = self.tweet["extended_tweet"]["full_text"]
        else:
            if "full_text" in self.tweet:
                tweet_text = self.tweet["full_text"]
            else:
                tweet_text = self.tweet["text"]
        return tweet_text

        # return self.tweet["extended_tweet"]["full_text"] if self.tweet["truncated"] else self.tweet["text"]

