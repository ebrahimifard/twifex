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


# import Network
# import location
# import TemporalFeatures

############################################# Packages #############################################


############################################# Notes and Comments #############################################

### There is an assumptioin here: The tweet json are collected in the extended mode with maximum inbformation

### In the paper talk about four different kind of objects (f1:tweet f2:tweet-retweet f3:tweet-quote f4:tweet-retweet-quote)
### Handling f1,f2,is okay, but how about f3 and f4? think about it! and incorporate it!

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
#       - Having a consistency between the class methods and names. Sme methods have to be available across different classes with the same name
#       - Summarising all those if and else where you calcualte statitical metrics for an array => maybe defining a function?
#       - add a function to check if two tweets are posted by the same account?
#       - replace "stdev" with "stddev"
#       - Try to use np.nan instead of None thoroughout the code
#       - VERY IMPORTANT ====> IN network bulidng functions, make sure about double counting!!!! $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#       - In url networks, it should be possible to make the network based on the main website domain not the detailed one
#       - Why not all user networks are multigraph??
#       - When you are making tweet_level networks, add an attribute to the nodes that displays their type (whether they are tweet, retweet, retweeted_quote, or quote)
#       - Make sure you use the correct variables/dictionaries in every network making method (for instance, in tweet_level_retweet_quote_reply network make sure all the dictionaries are retweet_quote_reply)



############################################# Notes and Comments #############################################
class TwifexUtility:
    def __init__(self):
        pass

    @staticmethod
    def levenshtein_distance(text1, text2):
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

    @staticmethod
    def basic_statistics(num_list):
        dict_container = {}
        if len(num_list) > 0:
            dict_container["average"] = np.nanmean(num_list)
            dict_container["max"] = np.nanmax(num_list)
            dict_container["min"] = np.nanmin(num_list)
            dict_container["stdev"] = np.nanstd(num_list)
            dict_container["median"] = np.nanmedian(num_list)
            dict_container["sum"] = np.nansum(num_list)
        else:
            dict_container["average"] = np.nan
            dict_container["max"] = np.nan
            dict_container["min"] = np.nan
            dict_container["stdev"] = np.nan
            dict_container["median"] = np.nan
            dict_container["sum"] = np.nan
        dict_container["count"] = len(num_list)

        return dict_container

    @staticmethod
    def tweets_retweets_retweetedquotes_quotes(tweets_dict):
        tweets_quotes_retweets = {}
        for tweet_id, tweet in tweets_dict.items():
            tweets_quotes_retweets[tweet_id] = {}
            tweets_quotes_retweets[tweet_id]["type"] = "twt"
            tweets_quotes_retweets[tweet_id]["object"] = tweet
            if tweet.is_retweeted():
                retweeted_tweet = tweet.get_retweeted()
                tweets_quotes_retweets[retweeted_tweet.get_id()] = {}
                tweets_quotes_retweets[retweeted_tweet.get_id()]["type"] = "rt"
                tweets_quotes_retweets[retweeted_tweet.get_id()]["object"] = retweeted_tweet

                if retweeted_tweet.is_quoted():
                    quoted_tweet = tweet.get_retweeted().get_quote()
                    tweets_quotes_retweets[quoted_tweet.get_id()] = {}
                    tweets_quotes_retweets[quoted_tweet.get_id()]["type"] = "rt_qt"
                    tweets_quotes_retweets[quoted_tweet.get_id()]["object"] = quoted_tweet

            if tweet.is_quote_available():
                quoted_tweet = tweet.get_quote()
                tweets_quotes_retweets[quoted_tweet.get_id()] = {}
                tweets_quotes_retweets[quoted_tweet.get_id()]["type"] = "qt"
                tweets_quotes_retweets[quoted_tweet.get_id()]["object"] = quoted_tweet

        return tweets_quotes_retweets

    @staticmethod
    def collective_tweets_to_dictionary(tweets_list):
        return {tweet.get_id(): tweet for tweet in tweets_list}


class Twifex:
    def __init__(self):
        """
        This function builds a Twifex object and load the necessary modules and dictionaries
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
        :return: A SingleTweet object for the tweet json
        """

        # s = SingleTweet(param=self.params)
        # s.tweet_loader(tweet_path=path)
        # print("hi")

        return SingleTweet(param=self.params).tweet_loader(tweet_path=path)

    def collective_tweets(self, tweets):
        """
        :param tweets: a list of SingleTweet objects
        :return: a collectiveTweet object which comprises the list of SingleTweet objects
        """
        return CollectiveTweets({tweet.get_id(): tweet for tweet in tweets})


class CollectiveTweets:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def mass_based_features(self):
        """
        :return: a MassBasedFeatures object which comprises the SingleTweet objects
        """
        return MassBasedFeatures(self.tweets)

    def topology_based_features(self):
        """
        :return: a topologyBasedFeatures object which comprises the SingleTweet objects
        """
        return TopologyBasedFeatures(self.tweets)  # Shouldn't this be topologyBasedFeatures?





############################################# mass features #############################################


class MassBasedFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def time_dependent_features(self):
        """
        :return: an object of massTweetFeatures which comprises the SingleTweet objects
        """
        return TimeDependentMassFeatures(self.tweets)

    def time_independent_features(self):
        """
        :return: an object of massUserFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentMassFeatures(self.tweets)


class TimeIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def time_independent_location_dependent_mass_features(self):
        return TimeIndependentLocationDependentMassFeatures(self.tweets)

    def time_independent_location_independent_mass_features(self):
        return TimeIndependentLocationIndependentMassFeatures(self.tweets)


class TimeDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def time_dependent_location_dependent_mass_features(self):
        return TimeDependentLocationDependentMassFeatures(self.tweets)

    def time_dependent_location_independent_mass_features(self):
        return TimeDependentLocationIndependentMassFeatures(self.tweets)


class TimeDependentLocationDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationDependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationDependentUserMassFeatures(self.tweets)


class TimeDependentLocationIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationIndependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationIndependentUserMassFeatures(self.tweets)


class TimeIndependentLocationDependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationDependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationDependentUserMassFeatures(self.tweets)


class TimeIndependentLocationIndependentMassFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationIndependentTweetMassFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserMassFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationIndependentUserMassFeatures(self.tweets)

# #TRANSFERRED
# class TemporalFeatures:
#     def __init__(self, tweets):
#         """
#         :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
#         """
#         self.tweets = tweets
#
#     def tweets_period(self):
#         """
#         :return: a sorted list of tweets creation time
#         """
#         tweet_dates = []
#         for tweet in self.tweets:
#             tweet_dates.append(self.tweets[tweet].get_creation_time())
#         return sorted(tweet_dates)
#
#     def tweets_in_periods(self, resolution="year", frequency=1):
#         """
#         :param resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
#         "hour", "minute" and "second".
#         :param frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
#         it means tweets are categorised by the time-frame of two weeks.
#         :return: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
#         the timestamps and all the tweets that are posted within every timestamp.
#         """
#         assert (resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time resolution " \
#                                                                                              "should be year, month, " \
#                                                                                              "week, day, hour, minute," \
#                                                                                              " or second"
#
#         sorted_tweet_times = self.tweets_period()
#         time_frame = sorted_tweet_times[0]
#         last = sorted_tweet_times[-1]
#         temporal_tweets = {}
#
#         if resolution == "year":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(years=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(years=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "month":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(months=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(months=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "week":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(weeks=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(weeks=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "day":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(days=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(days=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "hour":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(hours=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(hours=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "minute":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(minutes=frequency)
#             print(len(self.tweets))
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if time_frame <= tweet_time < time_frame + relativedelta(minutes=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         elif resolution == "second":
#             while (time_frame <= last):
#                 temporal_tweets[time_frame] = []
#                 time_frame += relativedelta(seconds=frequency)
#             for tweet_id, tweet in self.tweets.items():
#                 tweet_time = tweet.get_creation_time()
#                 for time_frame in temporal_tweets:
#                     if tweet_time >= time_frame and tweet_time < time_frame + relativedelta(seconds=frequency):
#                         temporal_tweets[time_frame].append(tweet)
#
#         return temporal_tweets

# #TRANSFERRED
# class PlaceFeatures:
#     def __init__(self, tweets):
#         """
#         :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
#         """
#         self.tweets = tweets
#
#     def geotagged_tweets(self):
#         """
#         This function filters out all tweets without geo location.
#         :return: a dictionary that maps every geotagged tweet_id to its corresponding SingleTweet object
#         """
#         return {p: q for p, q in self.tweets.items() if q.get_place() != None}
#
#     def tweets_distinct_countries(self):
#         """
#         This function finds all countries that the tweets in the dataset are comming from.
#         :return: return a list of distinct countries.
#         """
#         tweetsWithPlaces = self.geotagged_tweets()
#         places = set()
#         for tweet_id, tweet in tweetsWithPlaces.items():
#             place = tweet.get_place()
#             places.add(place["country"])
#         return list(places)
#
#     def tweets_distinct_places(self, coordinates=True):
#         """
#         This function finds all places that the tweets in the dataset are comming from.
#         :return: return a list of distinct places.
#         """
#         tweetsWithPlaces = self.geotagged_tweets()
#         places_coordinates = {}
#         for tweet_id, tweet in tweetsWithPlaces.items():
#             place = tweet.get_place()
#             places_coordinates[place["full_name"]] = places_coordinates.get(place["full_name"], place["bounding_box"])
#         if coordinates:
#             return places_coordinates
#         else:
#             return list(places_coordinates.keys())
#
#     def tweets_with_location(self, spatial_resolution='country'):
#         """
#         This function mapped all the geotagged tweets to their locations based on the spatial resolution specified in the function argument.
#         :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
#         :return: a dictionary that maps every location to the list of all tweets coming from that location.
#         """
#         if spatial_resolution == 'country':
#             res = "country"
#         elif spatial_resolution == 'place':
#             res = "full_name"
#
#         tweetsWithPlaces = self.geotagged_tweets()
#         location_dict = {}
#         for tweet_id, tweet in tweetsWithPlaces.items():
#             location_dict[tweet.get_place()[res]] = location_dict.get(tweet.get_place()[res], []) + [
#                 tweet]
#         return location_dict
#
#     # def countries_with_tweets(self):
#     #     """
#     #     This function mapped all the geotagged tweets to their country of origin.
#     #     :return: a dictionary that maps every country to the list of all tweets comming from that country.
#     #     """
#     #     tweetsWithPlaces = self.geotagged_tweets()
#     #     countries_dict = {}
#     #     for tweet_id, tweet in tweetsWithPlaces.items():
#     #         countries_dict[tweet.get_place()["country"]] = countries_dict.get(tweet.get_place()["country"], []) + [
#     #             tweet]
#     #     return countries_dict
#     #
#     # def places_with_tweets(self):
#     #     """
#     #     This function mapped all the geotagged tweets to their origin.
#     #     :return: a dictionary that maps every place to the list of all tweets comming from that country.
#     #     """
#     #     tweetsWithPlaces = self.geotagged_tweets()
#     #     places_dict = {}
#     #     for tweet_id, tweet in tweetsWithPlaces.items():
#     #         places_dict[tweet.get_place()["full_name"]] = places_dict.get(tweet.get_place()["full_name"], []) + [tweet]
#     #     return places_dict


class TimeDependentLocationIndependentTweetMassFeatures(TemporalFeatures):
    # def __init__(self, tweets):
    #     self.tweets = tweets
    #     self.nodes = self.tweets_period()
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


class TimeDependentLocationIndependentUserMassFeatures(TemporalFeatures):
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


class TimeDependentLocationDependentTweetMassFeatures(TemporalFeatures, PlaceFeatures):

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


class TimeDependentLocationDependentUserMassFeatures(TemporalFeatures, PlaceFeatures):
    # def test(self):
    #     print("test")
    def temporal_spatial_tweets(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :return: an embedded dictionary that classifies a set of tweets into a hierarchical structure in which the
        key-value corresponds to a location (or a timestamp depending on the value of "order" parameter) and another
        dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be all tweets
        corresponding to the location and timestamp.
        """

        assert (order in ["spatial-temporal", "temporal-spatial"])
        assert (temporal_resolution in ["year", "month", "week", "day", "hour", "minute", "second"]), "The time " \
                                                                                                      "resolution " \
                                                                                                      "should be year,"\
                                                                                                      "month,week,day,"\
                                                                                                      "hour, minute, " \
                                                                                                      "or second"
        assert (isinstance(temporal_frequency, int) and temporal_frequency>0), "The temporal frequency has to be a " \
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

    def temporal_spatial_user_status_count(self, order='spatial-temporal', temporal_resolution='day',
                                           temporal_frequency=1, spatial_resolution='country'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :return: a dictionary that represents user score across spatial units. The key-value pair in this dictionary
        corresponds to the spatial unit of analysis and statistical metrics of the user role of every account
        that has posted at least a tweet within each spatial unit.
        :return: an embedded dictionary that represents number of user's posts within a hierarchical structure in
        which the key-value corresponds to a location (or a timestamp depending on the value of "order" parameter)
        and another dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would
        be all the tweets posted by the user accounts corresponding to the location and timestamp.
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


        total_likes = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution,
                                                           temporal_frequency=temporal_frequency,
                                                           spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            total_likes[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                total_likes[layer1][layer2] = []
                for tweet in tweets:
                    total_likes[layer1][layer2] = total_likes[layer1].get(layer2, []) + \
                                                 [float(tweet.get_twitter().get_statusses_count())]

                scores = total_likes[layer1][layer2]
                total_likes[layer1][layer2] = {}
                if len(scores) > 0:
                    total_likes[layer1][layer2]["average"] = np.nanmean(scores)
                    total_likes[layer1][layer2]["max"] = np.nanmax(scores)
                    total_likes[layer1][layer2]["min"] = np.nanmin(scores)
                    total_likes[layer1][layer2]["stdev"] = np.nanstd(scores)
                    total_likes[layer1][layer2]["median"] = np.nanmedian(scores)
                    total_likes[layer1][layer2]["sum"] = np.nansum(scores)
                else:
                    total_likes[layer1][layer2]["average"] = np.nan
                    total_likes[layer1][layer2]["max"] = np.nan
                    total_likes[layer1][layer2]["min"] = np.nan
                    total_likes[layer1][layer2]["stdev"] = np.nan
                    total_likes[layer1][layer2]["median"] = np.nan
                    total_likes[layer1][layer2]["sum"] = np.nan
                total_likes[layer1][layer2]["count"] = len(scores)

        return total_likes

    def temporal_spatial_user_analysis(self, order='spatial-temporal', temporal_resolution='day', temporal_frequency=1,
                                       spatial_resolution='country', analysis_type='follower_count'):
        """
        :param order: the hierarchical structure of temporal-spatial embedded dictionary. If it is "spatial-temporal",
        then the first key would be a location and the second one is a timestamp. Otherwise and if the values of this
        parameter is equal to "temporal-spatial", then the first key would be a timestamp and the second one is a
        location.
        :param temporal_resolution: the time resolution of tweets categories. It can be "year", "month", "week", "day",
        "hour", "minute" and "second".
        :param temporal_frequency: the time frequency of tweets categories. For instance, if resolution="week" and
        frequency=2, it means tweets are categorised by the time-frame of two weeks.
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or
        place.
        :param analysis_type: This field specifies the type of analysis on the tweet users. It can be "users_role",
        "users_reputation", "users_followers_count", "users_friends_count", "users_account_age", "total_likes_count",
        and "users_status_count".
        :return: an embedded dictionary that represents users reputation within a hierarchical structure in which the
        key-value corresponds to a location (or a timestamp depending on the value of "order" parameter) and another
        dictionary. In this second dictionary, the key is a timestamp (or a location) and the value would be all the
        user reputation corresponding to the location and timestamp.
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
        assert (analysis_type in ["users_role", "users_reputation", "users_followers_count", "users_friends_count",
                                  "users_account_age", "total_likes_count", "users_status_count"]), "The type of " \
                                                                                                    "analysis could be " \
                                                                                                    "user role, " \
                                                                                                    "user reputation, " \
                                                                                                    "users_followers_count, " \
                                                                                                    "users_friends_count, " \
                                                                                                    "users_account_age, " \
                                                                                                    "total_likes_count," \
                                                                                                    " and users_status_count"

        container = {}
        hierarchical_tweets = self.temporal_spatial_tweets(order=order, temporal_resolution=temporal_resolution,
                                                           temporal_frequency=temporal_frequency,
                                                           spatial_resolution=spatial_resolution)
        for layer1, embedded_dictionary in hierarchical_tweets.items():
            container[layer1] = {}
            for layer2, tweets in embedded_dictionary.items():
                container[layer1][layer2] = []
                for tweet in tweets:

                    if analysis_type == "users_role":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                     [float(tweet.get_twitter().get_user_role())]
                    elif analysis_type == "users_reputation":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                          [float(tweet.get_twitter().get_user_reputation())]
                    elif analysis_type == "users_followers_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                     [float(tweet.get_twitter().get_followers_count())]
                    elif analysis_type == "users_friends_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                       [float(tweet.get_twitter().get_friends_count())]
                    elif analysis_type == "users_account_age":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_account_age())]
                    elif analysis_type == "total_likes_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_user_total_likes_count())]
                    elif analysis_type == "users_status_count":
                        container[layer1][layer2] = container[layer1].get(layer2, []) + \
                                                      [float(tweet.get_twitter().get_statusses_count())]

                # scores = container[layer1][layer2]
                # container[layer1][layer2] = {}

                container[layer1][layer2] = TwifexUtility.basic_statistics(container[layer1][layer2])
                # if len(scores) > 0:
                #     container[layer1][layer2]["average"] = np.nanmean(scores)
                #     container[layer1][layer2]["max"] = np.nanmax(scores)
                #     container[layer1][layer2]["min"] = np.nanmin(scores)
                #     container[layer1][layer2]["stdev"] = np.nanstd(scores)
                #     container[layer1][layer2]["median"] = np.nanmedian(scores)
                #     container[layer1][layer2]["sum"] = np.nansum(scores)
                # else:
                #     container[layer1][layer2]["average"] = np.nan
                #     container[layer1][layer2]["max"] = np.nan
                #     container[layer1][layer2]["min"] = np.nan
                #     container[layer1][layer2]["stdev"] = np.nan
                #     container[layer1][layer2]["median"] = np.nan
                #     container[layer1][layer2]["sum"] = np.nan
                # container[layer1][layer2]["count"] = len(scores)

        return container


class TimeIndependentLocationIndependentTweetMassFeatures:
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


class TimeIndependentLocationIndependentUserMassFeatures:
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
    #             dist = TwifexUtility.levenshtein_distance(pair[0], pair[1])
    #             if dist == 0:
    #                 users_redundant_dict[user_id][len(users_redundant_dict[user_id])+1] =


class TimeIndependentLocationDependentTweetMassFeatures(PlaceFeatures):

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


class TimeIndependentLocationDependentUserMassFeatures(PlaceFeatures):

    def spatial_user_role(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user score across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user role of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_roles = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            user_roles[location] = []
            for tweet in tweets:
                user_roles[location] = user_roles.get(location, []) + [float(tweet.get_twitter().get_user_role())]

            scores = user_roles[location]
            user_roles[location] = {}
            if len(scores) > 0:
                user_roles[location]["average"] = np.nanmean(scores)
                user_roles[location]["max"] = np.nanmax(scores)
                user_roles[location]["min"] = np.nanmin(scores)
                user_roles[location]["stdev"] = np.nanstd(scores)
                user_roles[location]["median"] = np.nanmedian(scores)
            else:
                user_roles[location]["average"] = np.nan
                user_roles[location]["max"] = np.nan
                user_roles[location]["min"] = np.nan
                user_roles[location]["stdev"] = np.nan
                user_roles[location]["median"] = np.nan
        return user_roles

    def spatial_user_reputation(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents user reputation across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the user reputation of every account
        that has posted at least a tweet within each spatial unit.
        """

        user_reputation = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            user_reputation[location] = []
            for tweet in tweets:
                user_reputation[location] = user_reputation.get(location, []) + [float(tweet.get_twitter().get_user_reputation())]

            scores = user_reputation[location]
            user_reputation[location] = {}
            if len(scores) > 0:
                user_reputation[location]["average"] = np.nanmean(scores)
                user_reputation[location]["max"] = np.nanmax(scores)
                user_reputation[location]["min"] = np.nanmin(scores)
                user_reputation[location]["stdev"] = np.nanstd(scores)
                user_reputation[location]["median"] = np.nanmedian(scores)
            else:
                user_reputation[location]["average"] = np.nan
                user_reputation[location]["max"] = np.nan
                user_reputation[location]["min"] = np.nan
                user_reputation[location]["stdev"] = np.nan
                user_reputation[location]["median"] = np.nan
        return user_reputation

    def spatial_followers(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents followers count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the followers count of every account
        that has posted at least a tweet within each spatial unit.
        """

        followers_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            followers_count[location] = []
            for tweet in tweets:
                followers_count[location] = followers_count.get(location, []) + \
                                            [float(tweet.get_twitter().get_followers_count())]

            scores = followers_count[location]
            followers_count[location] = {}
            if len(scores) > 0:
                followers_count[location]["average"] = np.nanmean(scores)
                followers_count[location]["max"] = np.nanmax(scores)
                followers_count[location]["min"] = np.nanmin(scores)
                followers_count[location]["stdev"] = np.nanstd(scores)
                followers_count[location]["median"] = np.nanmedian(scores)
            else:
                followers_count[location]["average"] = np.nan
                followers_count[location]["max"] = np.nan
                followers_count[location]["min"] = np.nan
                followers_count[location]["stdev"] = np.nan
                followers_count[location]["median"] = np.nan
        return followers_count

    def spatial_friends(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents friends count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the friends count of every account
        that has posted at least a tweet within each spatial unit.
        """

        friends_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            friends_count[location] = []
            for tweet in tweets:
                friends_count[location] = friends_count.get(location, []) + [float(tweet.get_twitter().get_friends_count())]

            scores = friends_count[location]
            friends_count[location] = {}
            if len(scores) > 0:
                friends_count[location]["average"] = np.nanmean(scores)
                friends_count[location]["max"] = np.nanmax(scores)
                friends_count[location]["min"] = np.nanmin(scores)
                friends_count[location]["stdev"] = np.nanstd(scores)
                friends_count[location]["median"] = np.nanmedian(scores)
            else:
                friends_count[location]["average"] = np.nan
                friends_count[location]["max"] = np.nan
                friends_count[location]["min"] = np.nan
                friends_count[location]["stdev"] = np.nan
                friends_count[location]["median"] = np.nan
        return friends_count

    def spatial_account_age(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents account age across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the age of every account
        that has posted at least a tweet within each spatial unit.
        """

        account_age = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            account_age[location] = []
            for tweet in tweets:
                account_age[location] = account_age.get(location, []) + [float(tweet.get_twitter().get_account_age())]

            scores = account_age[location]
            account_age[location] = {}
            if len(scores) > 0:
                account_age[location]["average"] = np.nanmean(scores)
                account_age[location]["max"] = np.nanmax(scores)
                account_age[location]["min"] = np.nanmin(scores)
                account_age[location]["stdev"] = np.nanstd(scores)
                account_age[location]["median"] = np.nanmedian(scores)
            else:
                account_age[location]["average"] = np.nan
                account_age[location]["max"] = np.nan
                account_age[location]["min"] = np.nan
                account_age[location]["stdev"] = np.nan
                account_age[location]["median"] = np.nan
        return account_age

    def spatial_total_likes(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents total account likes across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the totall likes of every account
        that has posted at least a tweet within each spatial unit.
        """

        total_likes = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            total_likes[location] = []
            for tweet in tweets:
                total_likes[location] = total_likes.get(location, []) + [float(tweet.get_twitter().get_user_total_likes_count())]

            scores = total_likes[location]
            total_likes[location] = {}
            if len(scores) > 0:
                total_likes[location]["average"] = np.nanmean(scores)
                total_likes[location]["max"] = np.nanmax(scores)
                total_likes[location]["min"] = np.nanmin(scores)
                total_likes[location]["stdev"] = np.nanstd(scores)
                total_likes[location]["median"] = np.nanmedian(scores)
            else:
                total_likes[location]["average"] = np.nan
                total_likes[location]["max"] = np.nan
                total_likes[location]["min"] = np.nan
                total_likes[location]["stdev"] = np.nan
                total_likes[location]["median"] = np.nan
        return total_likes

    def spatial_status_count(self, spatial_resolution="country"):
        """
        :param spatial_resolution: The spatial unit of analysis which according to Twitter can be either country or place.
        :return: a dictionary that represents status count across spatial units. The key-value pair in this dictionary corresponds to the spatial unit of analysis and statistical metrics of the status count of every account
        that has posted at least a tweet within each spatial unit.
        """

        status_count = {}
        geotagged_tweets = self.tweets_with_location(spatial_resolution=spatial_resolution)
        for location, tweets in geotagged_tweets.items():
            status_count[location] = []
            for tweet in tweets:
                status_count[location] = status_count.get(location, []) + [float(tweet.get_twitter().get_statusses_count())]

            scores = status_count[location]
            status_count[location] = {}
            if len(scores) > 0:
                status_count[location]["average"] = np.nanmean(scores)
                status_count[location]["max"] = np.nanmax(scores)
                status_count[location]["min"] = np.nanmin(scores)
                status_count[location]["stdev"] = np.nanstd(scores)
                status_count[location]["median"] = np.nanmedian(scores)
            else:
                status_count[location]["average"] = np.nan
                status_count[location]["max"] = np.nan
                status_count[location]["min"] = np.nan
                status_count[location]["stdev"] = np.nan
                status_count[location]["median"] = np.nan
        return status_count

############################################# mass features #############################################


############################################# network features #############################################
class TopologyBasedFeatures:
    def __init__(self, tweets):
        """
        This is a constructor for tweetNetwork class
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
        """
        self.tweets = tweets

    def time_dependent_features(self):
        """
        :return: an object of networkTweetFeatures which comprises the SingleTweet objects
        """
        return TimeDependentNetworkFeatures(self.tweets)

    def time_independent_features(self):
        """
        :return: an object of networkUserFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentNetworkFeatures(self.tweets)


class TimeDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def time_dependent_location_dependent_network_features(self):
        return TimeDependentLocationDependentNetworkFeatures(self.tweets)

    def time_dependent_location_independent_network_features(self):
        return TimeDependentLocationIndependentNetworkFeatures(self.tweets)


class TimeIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def time_independent_location_dependent_network_features(self):
        return TimeIndependentLocationDependentNetworkFeatures(self.tweets)

    def time_independent_location_independent_network_features(self):
        return TimeIndependentLocationIndependentNetworkFeatures(self.tweets)


class TimeDependentLocationDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationDependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationDependentUserNetworkFeatures(self.tweets)


class TimeDependentLocationIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetMassFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationIndependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeDependentLocationIndependentUserNetworkFeatures(self.tweets)


class TimeIndependentLocationDependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationDependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationDependentUserNetworkFeatures(self.tweets)


class TimeIndependentLocationIndependentNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets

    def tweet_features(self):
        """
        :return: an object of timeDependentTweetNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationIndependentTweetNetworkFeatures(self.tweets)

    def user_features(self):
        """
        :return: an object of timeDependentUserNetworkFeatures which comprises the SingleTweet objects
        """
        return TimeIndependentLocationIndependentUserNetworkFeatures(self.tweets)



#TRANSFERRED
# class Network:
#     def __init__(self, tweets):
#         """
#         This is a constructor of a network class.
#         :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
#         """
#         # self.network = nx.DiGraph()
#         self.tweets = tweets
#         # self.network = nx.DiGraph()
#
#         ### The network here should be DiGraph and not MultiGraph becasue it is not possible to have multiple edges for retweet, quote, and reply networks.
#         self.tweet_level_retweet_network = nx.DiGraph()
#         self.tweet_level_quote_network = nx.DiGraph()
#         self.tweet_level_reply_network = nx.DiGraph()
#         self.tweet_level_quote_reply_network = nx.DiGraph()
#         self.tweet_level_retweet_reply_network = nx.DiGraph()
#         self.tweet_level_retweet_quote_network = nx.DiGraph()
#         self.tweet_level_retweet_quote_reply_network = nx.DiGraph()
#
#         self.tweet_level_cooccurrence_hashtag_network = nx.Graph()
#         self.tweet_level_cooccurrence_mention_network = nx.Graph()
#         self.tweet_level_cooccurrence_url_network = nx.Graph()
#
#         self.tweet_hashtag_bipartite_network = nx.DiGraph()
#         self.tweet_mention_bipartite_network = nx.DiGraph()
#         self.tweet_url_bipartite_network = nx.DiGraph()
#
#
#
#         ### But here we need to have a multi graph becasue a user can retweet/quote/reply to the other user at the same time
#         self.user_level_retweet_network = nx.DiGraph()
#         self.user_level_quote_network = nx.DiGraph()
#         self.user_level_reply_network = nx.DiGraph()
#         self.user_level_quote_reply_network = nx.MultiDiGraph()
#         self.user_level_retweet_reply_network = nx.MultiDiGraph()
#         self.user_level_retweet_quote_network = nx.MultiDiGraph()
#         self.user_level_retweet_quote_reply_network = nx.MultiDiGraph()
#
#         self.user_level_cooccurrence_hashtag_network = nx.Graph()
#         self.user_level_cooccurrence_mention_network = nx.Graph()
#         self.user_level_cooccurrence_url_network = nx.Graph()
#
#         self.user_hashtag_bipartite_network = nx.DiGraph()
#         self.user_mention_bipartite_network = nx.DiGraph()
#         self.user_url_bipartite_network = nx.DiGraph()
#
#
#
#         self.network_repository = []
#
#         self.quote_reply_key_keepers = {}
#         self.retweet_reply_key_keepers = {}
#         self.retweet_quote_key_keepers = {}
#         self.retweet_quote_reply_key_keepers = {}
#
#
#         self.tweets_quotes_retweets = TwifexUtility.tweets_retweets_retweetedquotes_quotes(tweets)
        # for tweet_id, tweet in self.tweets.items():
        #     self.tweets_quotes_retweets[tweet_id] = {}
        #     self.tweets_quotes_retweets[tweet_id]["type"] = "twt"
        #     self.tweets_quotes_retweets[tweet_id]["object"] = tweet
        #     if tweet.is_retweeted():
        #         retweeted_tweet = tweet.get_retweeted()
        #         self.tweets_quotes_retweets[retweeted_tweet.get_id()] = {}
        #         self.tweets_quotes_retweets[retweeted_tweet.get_id()]["type"] = "rt"
        #         self.tweets_quotes_retweets[retweeted_tweet.get_id()]["object"] = retweeted_tweet
        #
        #         if retweeted_tweet.is_quoted():
        #             quoted_tweet = tweet.get_retweeted().get_quote()
        #             self.tweets_quotes_retweets[quoted_tweet.get_id()] = {}
        #             self.tweets_quotes_retweets[quoted_tweet.get_id()]["type"] = "rt_qt"
        #             self.tweets_quotes_retweets[quoted_tweet.get_id()]["object"] = quoted_tweet
        #
        #     if tweet.is_quote_available():
        #         quoted_tweet = tweet.get_quote()
        #         self.tweets_quotes_retweets[quoted_tweet.get_id()] = {}
        #         self.tweets_quotes_retweets[quoted_tweet.get_id()]["type"] = "qt"
        #         self.tweets_quotes_retweets[quoted_tweet.get_id()]["object"] = quoted_tweet

    # ### Tweet-level network
    # # retweet/quote/reply networks
    # def tweet_level_retweet_network_building(self):
    #     self.network_repository.append("tweet_level_retweet_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #
    #         if retweet_condition:
    #             self.tweet_level_retweet_network.add_edge(tweet.get_id(),
    #                                                       tweet.get_retweeted().get_id(), kind="retweet")
    #         else:
    #             self.tweet_level_retweet_network.add_node(tweet.get_id())
    #
    # def tweet_level_quote_network_building(self):
    #     self.network_repository.append("tweet_level_quote_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         quote_condition = tweet.is_quote_available()
    #
    #         if quote_condition:
    #             self.tweet_level_quote_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 self.tweet_level_quote_network.add_edge(tweet.get_quote().get_id(),
    #                                                         tweet.get_quote().get_quote_status_id(), kind="quote")
    #         else:
    #             self.tweet_level_quote_network.add_node(tweet.get_id())
    #
    # def tweet_level_reply_network_building(self):
    #     self.network_repository.append("tweet_level_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         if reply_condition:
    #             self.tweet_level_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #         else:
    #             self.tweet_level_reply_network.add_node(tweet.get_id())
    #
    # # quote-reply/retweet-reply/retweet-quote networks
    # def tweet_level_quote_reply_network_building(self):
    #     self.network_repository.append("tweet_level_quote_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         quote_condition = tweet.is_quote_available()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         if quote_condition is True and reply_condition is True:
    #             self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="quote")
    #             inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_quote().is_quoted()
    #             if inner_reply_condition_level_one:
    #                 self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
    #                                                               tweet.get_quote().get_reply_to_id(), kind="reply")
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
    #                                                               tweet.get_quote().get_quote_status_id(), kind="quote")
    #
    #         elif quote_condition is True and reply_condition is False:
    #             self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             inner_reply_condition = tweet.get_quote().is_this_a_reply()
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_reply_condition:
    #                 self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
    #                                                               tweet.get_quote().get_reply_to_id(), kind="reply")
    #             if inner_quote_condition:
    #                 self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
    #                                                               tweet.get_quote().get_quote_status_id(), kind="quote")
    #         elif quote_condition is False and reply_condition is True:
    #             self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #         elif quote_condition is False and reply_condition is False:
    #             self.tweet_level_quote_reply_network.add_node(tweet.get_id())
    #
    # def tweet_level_retweet_reply_network_building(self):
    #     self.network_repository.append("tweet_level_retweet_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         if retweet_condition is True and reply_condition is True:  #######This condition seems impossible to happen
    #             self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
    #             self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #             inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
    #             if inner_reply_condition:
    #                 self.tweet_level_retweet_reply_network.add_edge(tweet.get_retweeted().get_id(),
    #                                                                 tweet.get_retweeted().get_reply_to_id(), kind="reply")
    #         elif retweet_condition is True and reply_condition is False:
    #             self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
    #             inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
    #             if inner_reply_condition:
    #                 self.tweet_level_retweet_reply_network.add_edge(tweet.get_retweeted().get_id(),
    #                                                                 tweet.get_retweeted().get_reply_to_id(), kind="reply")
    #         elif retweet_condition is False and reply_condition is True:
    #             self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #         elif retweet_condition is False and reply_condition is False:
    #             self.tweet_level_retweet_reply_network.add_node(tweet.get_id())
    #
    # def tweet_level_retweet_quote_network_building(self):
    #     self.network_repository.append("tweet_level_retweet_quote_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         quote_condition = tweet.is_quote_available()
    #
    #         ####### if retweet_condition is True and quote_condition is True: #This condition seems impossible to happen
    #         if retweet_condition is True and quote_condition is False:
    #             self.tweet_level_retweet_quote_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_retweet_quote_network.add_edge(tweet.get_retweeted().get_id(),
    #                                                                 tweet.get_retweeted().get_quote().get_id(), kind="quote")
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 if inner_quote_condition_level_two:
    #                     self.tweet_level_retweet_quote_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
    #                                      tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
    #         elif retweet_condition is False and quote_condition is True:
    #             self.tweet_level_retweet_quote_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 self.tweet_level_retweet_quote_network.add_edge(tweet.get_quote().get_id(),
    #                                                                 tweet.get_quote().get_quote_status_id(), kind="quote")
    #         elif retweet_condition is False and quote_condition is False:
    #             self.tweet_level_retweet_quote_network.add_node(tweet.get_id())
    #
    # # retweet-quote-reply network
    # def tweet_level_retweet_quote_reply_network_building(self):
    #     self.network_repository.append("tweet_level_retweet_quote_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         quote_condition = tweet.is_quote_available()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #
    #         # The first two conditions never occur
    #         # if retweet_condition is True and quote_condition is True and reply_condition is True:
    #         # elif retweet_condition is True and quote_condition is True and reply_condition is False:
    #         if retweet_condition is True and quote_condition is False and reply_condition is True:  #######This condition seems impossible to happen
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #             inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #             if inner_reply_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_reply_to_id(),
    #                                  kind="reply")
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(),
    #                                  kind="quote")
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
    #                 if inner_quote_condition_level_two:
    #                     self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
    #                                      tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
    #                 if inner_reply_condition_level_two:
    #                     self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
    #                                      tweet.get_retweeted().get_quote().get_reply_to_id(), kind="reply")
    #
    #         elif retweet_condition is True and quote_condition is False and reply_condition is False:
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
    #             inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #             if inner_reply_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_reply_to_id(), kind="reply")
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(), kind="quote")
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
    #                 if inner_quote_condition_level_two:
    #                     self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
    #                                      tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
    #                 if inner_reply_condition_level_two:
    #                     self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
    #                                      tweet.get_retweeted().get_quote().get_reply_to_id(), kind="reply")
    #
    #         elif retweet_condition is False and quote_condition is True and reply_condition is True:
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #             inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_quote().is_quoted()
    #             if inner_reply_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_reply_to_id(), kind="reply")
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_quote_status_id(), kind="quote")
    #
    #         elif retweet_condition is False and quote_condition is True and reply_condition is False:
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
    #             inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_quote().is_quoted()
    #             if inner_reply_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_reply_to_id(), kind="reply")
    #             if inner_quote_condition_level_one:
    #                 self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_quote_status_id(), kind="quote")
    #
    #         elif retweet_condition is False and quote_condition is False and reply_condition is True:
    #             self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
    #         elif retweet_condition is False and quote_condition is False and reply_condition is False:
    #             self.tweet_level_retweet_quote_reply_network.add_node(tweet.get_id())
    #
    #         # # if retweet_condition is True and quote_condition is True: #This condition seems impossible to happen
    #         # if retweet_condition is True and quote_condition is False:
    #         #     network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind=network_type)
    #         #     inner_quote_condition = tweet.get_retweeted().is_quoted()
    #         #     if inner_quote_condition:
    #         #         network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(), kind=network_type)
    #         # elif retweet_condition is False and quote_condition is True:
    #         #     network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind=network_type)
    #         # elif retweet_condition is False and quote_condition is False:
    #         #     network.add_node(tweet.get_id())
    #
    # # hashtag/mention/url networks
    # def tweet_level_cooccurrence_hashtag_network_building(self):
    #     self.network_repository.append("tweet_level_cooccurrence_hashtag_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         tweet1_id = tweet1.get_id()
    #         tweet1_hashtags = tweet1.get_hashtags()
    #
    #         j = i + 1
    #
    #         self.tweet_level_cooccurrence_hashtag_network.add_node(tweet1_id)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             tweet1_rt_id = tweet1_rt.get_id()
    #
    #             for ht in tweet1_hashtags:
    #                 if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
    #                     edge_label = "-" + ht
    #                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id]["hashtags"] += edge_label
    #                 else:
    #                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, hashtags=ht)
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                 tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                 for ht1 in tweet1_hashtags:
    #                     for ht2 in tweet1_rt_qt_hashtags:
    #                         if ht1 == ht2:
    #                             if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + ht1
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id][
    #                                     "hashtags"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
    #                                                                           hashtags=ht1)
    #
    #                 for ht1 in tweet1_hashtags:
    #                     for ht2 in tweet1_rt_qt_hashtags:
    #                         if ht1 == ht2:
    #                             if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + ht1
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
    #                                     "hashtags"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
    #                                                                           hashtags=ht1)
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             tweet1_qt_id = tweet1_qt.get_id()
    #             tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #             for ht1 in tweet1_hashtags:
    #                 for ht2 in tweet1_qt_hashtags:
    #                     if ht1 == ht2:
    #                         if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                             self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
    #                             edge_label = "-" + ht1
    #                             self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id][
    #                                 "hashtags"] += edge_label
    #                         else:
    #                             self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
    #                                                                       hashtags=ht1)
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             tweet2_id = tweet2.get_id()
    #             tweet2_hashtags = tweet2.get_hashtags()
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #
    #                 if tweet1_id != tweet2_rt_id:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet2_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                         tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                         if tweet1_id != tweet2_rt_qt_id:
    #                             for ht1 in tweet1_hashtags:
    #                                 for ht2 in tweet2_rt_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                             self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "hashtags"] += edge_label
    #                                         else:
    #                                             self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_rt_qt_id,
    #                                                                                       weight=1,
    #                                                                                       hashtags=ht1)
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1_id != tweet2_qt_id:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet2_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_qt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 if tweet1_rt_id != tweet2_rt_id:
    #                     for ht1 in tweet1_rt_hashtags:
    #                         for ht2 in tweet2_rt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_id:
    #                         for ht1 in tweet1_rt_qt_hashtags:
    #                             for ht2 in tweet2_rt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
    #                                                                                   weight=1, hashtags=ht1)
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_id != tweet2_rt_qt_id:
    #                         for ht1 in tweet1_rt_hashtags:
    #                             for ht2 in tweet2_rt_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1, hashtags=ht1)
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_qt_id:
    #                         for ht1 in tweet1_rt_qt_hashtags:
    #                             for ht2 in tweet2_rt_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1, hashtags=ht1)
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1_qt_id != tweet2_qt_id:
    #                     for ht1 in tweet1_qt_hashtags:
    #                         for ht2 in tweet2_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1_rt_id != tweet2_qt_id:
    #                     for ht1 in tweet1_rt_hashtags:
    #                         for ht2 in tweet2_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt_id != tweet2_qt_id:
    #                         for ht1 in tweet1_rt_qt_hashtags:
    #                             for ht2 in tweet2_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
    #                                                                                   weight=1, hashtags=ht1)
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_hashtags = tweet2_rt.get_hashtags()
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 if tweet1_qt_id != tweet2_rt_id:
    #                     for ht1 in tweet1_qt_hashtags:
    #                         for ht2 in tweet2_rt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_qt_id != tweet2_rt_qt_id:
    #                         for ht1 in tweet1_qt_hashtags:
    #                             for ht2 in tweet2_rt_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1,
    #                                                                                   hashtags=ht1)
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 if tweet1_rt_id != tweet2_id:
    #                     for ht1 in tweet1_rt_hashtags:
    #                         for ht2 in tweet2_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet2_id != tweet1_rt_qt_id:
    #                         for ht1 in tweet1_rt_qt_hashtags:
    #                             for ht2 in tweet2_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "hashtags"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_id,
    #                                                                                   weight=1,
    #                                                                                   hashtags=ht1)
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 if tweet1_qt_id != tweet2_id:
    #                     for ht1 in tweet1_qt_hashtags:
    #                         for ht2 in tweet2_hashtags:
    #                             if ht1 == ht2:
    #                                 if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_id][
    #                                         "hashtags"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
    #                                                                               hashtags=ht1)
    #
    #             if tweet1_id != tweet2_id:
    #                 for ht1 in tweet1_hashtags:
    #                     for ht2 in tweet2_hashtags:
    #                         if ht1 == ht2:
    #                             if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id]["weight"] += 1
    #                                 edge_label = "-" + ht1
    #                                 self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id][
    #                                     "hashtags"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_id, weight=1,
    #                                                                           hashtags=ht1)
    #             j += 1
    #
    # def tweet_level_cooccurrence_mention_network_building(self):
    #     self.network_repository.append("tweet_level_cooccurrence_mention_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         tweet1_id = tweet1.get_id()
    #         tweet1_mentions = tweet1.get_mentions()
    #
    #         j = i + 1
    #
    #         self.tweet_level_cooccurrence_mention_network.add_node(tweet1_id)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             tweet1_rt_id = tweet1_rt.get_id()
    #
    #             for mt in tweet1_mentions:
    #                 if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
    #                     edge_label = "-" + mt
    #                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id]["mentions"] += edge_label
    #                 else:
    #                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, mentions=mt)
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                 tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                 for mt1 in tweet1_mentions:
    #                     for mt2 in tweet1_rt_qt_mentions:
    #                         if mt1 == mt2:
    #                             if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + mt1
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id][
    #                                     "mentions"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
    #                                                                           mentions=mt1)
    #
    #                 for mt1 in tweet1_mentions:
    #                     for mt2 in tweet1_rt_qt_mentions:
    #                         if mt1 == mt2:
    #                             if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + mt1
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
    #                                     "mentions"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
    #                                                                           mentions=mt1)
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             tweet1_qt_id = tweet1_qt.get_id()
    #             tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #             for mt1 in tweet1_mentions:
    #                 for mt2 in tweet1_qt_mentions:
    #                     if mt1 == mt2:
    #                         if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                             self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
    #                             edge_label = "-" + mt1
    #                             self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id][
    #                                 "mentions"] += edge_label
    #                         else:
    #                             self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
    #                                                                       mentions=mt1)
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             tweet2_id = tweet2.get_id()
    #             tweet2_mentions = tweet2.get_mentions()
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #
    #                 if tweet1_id != tweet2_rt_id:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet2_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                         tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                         if tweet1_id != tweet2_rt_qt_id:
    #                             for mt1 in tweet1_mentions:
    #                                 for mt2 in tweet2_rt_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                             self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "mentions"] += edge_label
    #                                         else:
    #                                             self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_rt_qt_id,
    #                                                                                       weight=1,
    #                                                                                       mentions=mt1)
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1_id != tweet2_qt_id:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet2_qt_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_qt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 if tweet1_rt_id != tweet2_rt_id:
    #                     for mt1 in tweet1_rt_mentions:
    #                         for mt2 in tweet2_rt_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_id:
    #                         for mt1 in tweet1_rt_qt_mentions:
    #                             for mt2 in tweet2_rt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
    #                                                                                   weight=1, mentions=mt1)
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_id != tweet2_rt_qt_id:
    #                         for mt1 in tweet1_rt_mentions:
    #                             for mt2 in tweet2_rt_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1, mentions=mt1)
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_qt_id:
    #                         for mt1 in tweet1_rt_qt_mentions:
    #                             for mt2 in tweet2_rt_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1, mentions=mt1)
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1_qt_id != tweet2_qt_id:
    #                     for mt1 in tweet1_qt_mentions:
    #                         for mt2 in tweet2_qt_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1_rt_id != tweet2_qt_id:
    #                     for mt1 in tweet1_rt_mentions:
    #                         for mt2 in tweet2_qt_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt_id != tweet2_qt_id:
    #                         for mt1 in tweet1_rt_qt_mentions:
    #                             for mt2 in tweet2_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
    #                                                                                   weight=1, mentions=mt1)
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_mentions = tweet2_rt.get_mentions()
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 if tweet1_qt_id != tweet2_rt_id:
    #                     for mt1 in tweet1_qt_mentions:
    #                         for mt2 in tweet2_rt_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_qt_id != tweet2_rt_qt_id:
    #                         for mt1 in tweet1_qt_mentions:
    #                             for mt2 in tweet2_rt_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
    #                                                                                   weight=1,
    #                                                                                   mentions=mt1)
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 if tweet1_rt_id != tweet2_id:
    #                     for mt1 in tweet1_rt_mentions:
    #                         for mt2 in tweet2_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet2_id != tweet1_rt_qt_id:
    #                         for mt1 in tweet1_rt_qt_mentions:
    #                             for mt2 in tweet2_mentions:
    #                                 if mt1 == mt2:
    #                                     if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "mentions"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_id,
    #                                                                                   weight=1,
    #                                                                                   mentions=mt1)
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 if tweet1_qt_id != tweet2_id:
    #                     for mt1 in tweet1_qt_mentions:
    #                         for mt2 in tweet2_mentions:
    #                             if mt1 == mt2:
    #                                 if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_id][
    #                                         "mentions"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
    #                                                                               mentions=mt1)
    #
    #             if tweet1_id != tweet2_id:
    #                 for mt1 in tweet1_mentions:
    #                     for mt2 in tweet2_mentions:
    #                         if mt1 == mt2:
    #                             if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id]["weight"] += 1
    #                                 edge_label = "-" + mt1
    #                                 self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id][
    #                                     "mentions"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_id, weight=1,
    #                                                                           mentions=mt1)
    #             j += 1
    #
    # def tweet_level_cooccurrence_url_network_building(self):
    #     self.network_repository.append("tweet_level_cooccurrence_url_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         tweet1_id = tweet1.get_id()
    #         tweet1_urls = tweet1.get_tweet_urls(return_format="expanded_url")
    #
    #         j = i + 1
    #
    #         self.tweet_level_cooccurrence_url_network.add_node(tweet1_id)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             tweet1_rt_id = tweet1_rt.get_id()
    #
    #             for ut in tweet1_urls:
    #                 if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
    #                     edge_label = "-" + ut
    #                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id]["urls"] += edge_label
    #                 else:
    #                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, urls=ut)
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                 tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 for ut1 in tweet1_urls:
    #                     for ut2 in tweet1_rt_qt_urls:
    #                         if ut1 == ut2:
    #                             if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + ut1
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id][
    #                                     "urls"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
    #                                                                       urls=ut1)
    #
    #                 for ut1 in tweet1_urls:
    #                     for ut2 in tweet1_rt_qt_urls:
    #                         if ut1 == ut2:
    #                             if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
    #                                 edge_label = "-" + ut1
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
    #                                     "urls"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
    #                                                                       urls=ut1)
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             tweet1_qt_id = tweet1_qt.get_id()
    #             tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #             for ut1 in tweet1_urls:
    #                 for ut2 in tweet1_qt_urls:
    #                     if ut1 == ut2:
    #                         if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                             self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
    #                             edge_label = "-" + ut1
    #                             self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id][
    #                                 "urls"] += edge_label
    #                         else:
    #                             self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
    #                                                                   urls=ut1)
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             tweet2_id = tweet2.get_id()
    #             tweet2_urls = tweet2.get_tweet_urls(return_format="expanded_url")
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #
    #                 if tweet1_id != tweet2_rt_id:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet2_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                         tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                         if tweet1_id != tweet2_rt_qt_id:
    #                             for ut1 in tweet1_urls:
    #                                 for ut2 in tweet2_rt_qt_urls:
    #                                     if ut1 == ut2:
    #                                         if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                             self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_qt_id][
    #                                                 "urls"] += edge_label
    #                                         else:
    #                                             self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_rt_qt_id,
    #                                                                                   weight=1,
    #                                                                                   urls=ut1)
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_id != tweet2_qt_id:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet2_qt_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt_id != tweet2_rt_id:
    #                     for ut1 in tweet1_rt_urls:
    #                         for ut2 in tweet2_rt_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_id:
    #                         for ut1 in tweet1_rt_qt_urls:
    #                             for ut2 in tweet2_rt_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
    #                                                                               weight=1, urls=ut1)
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_id != tweet2_rt_qt_id:
    #                         for ut1 in tweet1_rt_urls:
    #                             for ut2 in tweet2_rt_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
    #                                                                               weight=1, urls=ut1)
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt_id != tweet2_rt_qt_id:
    #                         for ut1 in tweet1_rt_qt_urls:
    #                             for ut2 in tweet2_rt_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
    #                                                                               weight=1, urls=ut1)
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt_id != tweet2_qt_id:
    #                     for ut1 in tweet1_qt_urls:
    #                         for ut2 in tweet2_qt_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_id()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 tweet2_qt_id = tweet2_qt.get_id()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt_id != tweet2_qt_id:
    #                     for ut1 in tweet1_rt_urls:
    #                         for ut2 in tweet2_qt_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt_id != tweet2_qt_id:
    #                         for ut1 in tweet1_rt_qt_urls:
    #                             for ut2 in tweet2_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
    #                                                                               weight=1, urls=ut1)
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 tweet2_rt_id = tweet2_rt.get_id()
    #                 tweet2_rt_urls = tweet2_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt_id != tweet2_rt_id:
    #                     for ut1 in tweet1_qt_urls:
    #                         for ut2 in tweet2_rt_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
    #                                                                           urls=ut1)
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     tweet2_rt_qt_id = tweet2_rt_qt.get_id()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_qt_id != tweet2_rt_qt_id:
    #                         for ut1 in tweet1_qt_urls:
    #                             for ut2 in tweet2_rt_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
    #                                                                               weight=1,
    #                                                                               urls=ut1)
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt_id != tweet2_id:
    #                     for ut1 in tweet1_rt_urls:
    #                         for ut2 in tweet2_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
    #                                                                           urls=ut1)
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     tweet1_rt_qt_id = tweet1_rt_qt.get_id()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet2_id != tweet1_rt_qt_id:
    #                         for ut1 in tweet1_rt_qt_urls:
    #                             for ut2 in tweet2_urls:
    #                                 if ut1 == ut2:
    #                                     if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_id][
    #                                             "urls"] += edge_label
    #                                     else:
    #                                         self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_id,
    #                                                                               weight=1,
    #                                                                               urls=ut1)
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 tweet1_qt_id = tweet1_qt.get_id()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt_id != tweet2_id:
    #                     for ut1 in tweet1_qt_urls:
    #                         for ut2 in tweet2_urls:
    #                             if ut1 == ut2:
    #                                 if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id][
    #                                         "urls"] += edge_label
    #                                 else:
    #                                     self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
    #                                                                           urls=ut1)
    #
    #             if tweet1_id != tweet2_id:
    #                 for ut1 in tweet1_urls:
    #                     for ut2 in tweet2_urls:
    #                         if ut1 == ut2:
    #                             if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id]["weight"] += 1
    #                                 edge_label = "-" + ut1
    #                                 self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id][
    #                                     "urls"] += edge_label
    #                             else:
    #                                 self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_id, weight=1,
    #                                                                       urls=ut1)
    #             j += 1
    #
    # # bipartite version of tweet-level hashtag/mention/url networks
    # def tweet_hashtag_bipartite_network_building(self):
    #     self.network_repository.append("tweet_hashtag_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_id()
    #         hashtag_list = tweet.get_hashtags()
    #
    #         for hashtag in hashtag_list:
    #             if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
    #                 self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                 self.tweet_hashtag_bipartite_network.edges[source, hashtag][
    #                     "shared_author"] += tweet.get_twitter().get_screen_name()
    #             else:
    #                 self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                     shared_author=tweet.get_twitter().get_screen_name())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_id()
    #             hashtag_list = tweet.get_hashtags()
    #             for hashtag in hashtag_list:
    #
    #                 if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
    #                     self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                     self.tweet_hashtag_bipartite_network.edges[source, hashtag][
    #                         "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                         shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_id()
    #                 hashtag_list = tweet.get_retweeted().get_quote().get_hashtags()
    #                 for hashtag in hashtag_list:
    #
    #                     if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
    #                         self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                         self.tweet_hashtag_bipartite_network.edges[source, hashtag][
    #                             "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                     else:
    #                         self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                             shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_id()
    #             hashtag_list = tweet.get_quote().get_hashtags()
    #             for hashtag in hashtag_list:
    #
    #                 if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
    #                     self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                     self.tweet_hashtag_bipartite_network.edges[source, hashtag][
    #                         "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                         shared_author=tweet.get_quote().get_twitter().get_screen_name())
    #
    # def tweet_mention_bipartite_network_building(self):
    #     self.network_repository.append("tweet_mention_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_id()
    #         mention_list = tweet.get_mentions()
    #
    #         for mention in mention_list:
    #             if self.tweet_mention_bipartite_network.has_edge(source, mention):
    #                 self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                 self.tweet_mention_bipartite_network.edges[source, mention]["shared_author"] += tweet.get_twitter().get_screen_name()
    #             else:
    #                 self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                    shared_author=tweet.get_twitter().get_screen_name())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_id()
    #             mention_list = tweet.get_mentions()
    #             for mention in mention_list:
    #
    #                 if self.tweet_mention_bipartite_network.has_edge(source, mention):
    #                     self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                     self.tweet_mention_bipartite_network.edges[source, mention][
    #                         "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                        shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_id()
    #                 mention_list = tweet.get_retweeted().get_quote().get_mentions()
    #                 for mention in mention_list:
    #
    #                     if self.tweet_mention_bipartite_network.has_edge(source, mention):
    #                         self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                         self.tweet_mention_bipartite_network.edges[source, mention][
    #                             "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                     else:
    #                         self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                            shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_id()
    #             mention_list = tweet.get_quote().get_mentions()
    #             for mention in mention_list:
    #
    #                 if self.tweet_mention_bipartite_network.has_edge(source, mention):
    #                     self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                     self.tweet_mention_bipartite_network.edges[source, mention][
    #                         "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                        shared_author=tweet.get_quote().get_twitter().get_screen_name())
    #
    # def tweet_url_bipartite_network_building(self):
    #     self.network_repository.append("tweet_url_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_id()
    #         url_list = tweet.get_tweet_urls(return_format="expanded_url")
    #
    #         for url in url_list:
    #             if self.tweet_url_bipartite_network.has_edge(source, url):
    #                 self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
    #                 self.tweet_url_bipartite_network.edges[source, url]["shared_author"] += tweet.get_twitter().get_screen_name()
    #             else:
    #                 self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                 shared_author=tweet.get_twitter().get_screen_name())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_id()
    #             url_list = tweet.get_tweet_urls(return_format="expanded_url")
    #             for url in url_list:
    #
    #                 if self.tweet_url_bipartite_network.has_edge(source, url):
    #                     self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
    #                     self.tweet_url_bipartite_network.edges[source, url][
    #                         "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                     shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_id()
    #                 url_list = tweet.get_retweeted().get_quote().get_tweet_urls(return_format="expanded_url")
    #                 for url in url_list:
    #
    #                     if self.tweet_url_bipartite_network.has_edge(source, url):
    #                         self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
    #                         self.tweet_url_bipartite_network.edges[source, url][
    #                             "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                     else:
    #                         self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                         shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_id()
    #             url_list = tweet.get_quote().get_tweet_urls(return_format="expanded_url")
    #             for url in url_list:
    #
    #                 if self.tweet_url_bipartite_network.has_edge(source, url):
    #                     self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
    #                     self.tweet_url_bipartite_network.edges[source, url][
    #                         "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
    #                 else:
    #                     self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                     shared_author=tweet.get_quote().get_twitter().get_screen_name())
    # ####################################################################
    #
    # ### User-level network
    # # retweet/quote/reply networks
    # def user_level_retweet_network_building(self):
    #     self.network_repository.append("user_level_retweet_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         source = tweet.get_twitter().get_screen_name()
    #         if retweet_condition:
    #             destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #             if self.user_level_retweet_network.has_edge(source, destination):
    #                 self.user_level_retweet_network.edges[source, destination]["weight"] += 1
    #             else:
    #                 self.user_level_retweet_network.add_edge(source, destination, kind="retweet", weight=1)
    #         else:
    #             self.user_level_retweet_network.add_node(source)
    #
    # def user_level_quote_network_building(self):
    #     self.network_repository.append("user_level_quote_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         quote_condition = tweet.is_quote_available()
    #
    #         source = tweet.get_twitter().get_screen_name()
    #         if quote_condition:
    #             destination = tweet.get_quote().get_twitter().get_screen_name()
    #             if self.user_level_quote_network.has_edge(source, destination):
    #                 self.user_level_quote_network.edges[source, destination]["weight"] += 1
    #             else:
    #                 self.user_level_quote_network.add_edge(source, destination, kind="quote", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = tweet.get_quote().get_twitter().get_screen_name()
    #                 inner_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if self.user_level_quote_network.has_edge(inner_source, inner_destination):
    #                     self.user_level_quote_network.edges[inner_source, inner_destination]["weight"] += 1
    #                 else:
    #                     self.user_level_quote_network.add_edge(inner_source, inner_destination, kind="quote", weight=1)
    #         else:
    #             self.user_level_quote_network.add_node(source)
    #
    # def user_level_reply_network_building(self):
    #     self.network_repository.append("user_level_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         source = tweet.get_twitter().get_screen_name()
    #         if reply_condition:
    #             destination = tweet.get_in_reply_to_screen_name()
    #             if self.user_level_reply_network.has_edge(source, destination):
    #                 self.user_level_reply_network.edges[source, destination]["weight"] += 1
    #             else:
    #                 self.user_level_reply_network.add_edge(source, destination, kind="reply", weight=1)
    #         else:
    #             self.user_level_reply_network.add_node(source)
    #
    # # quote-reply/retweet-reply/retweet-quote networks
    # def user_level_quote_reply_network_building(self):
    #     self.network_repository.append("user_level_quote_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         quote_condition = tweet.is_quote_available()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         key_code = 0
    #         source = tweet.get_twitter().get_screen_name()
    #
    #         if quote_condition is True and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             quote_destination = tweet.get_quote().get_twitter().get_screen_name()
    #
    #             # key_code = 0
    #             if (source, quote_destination, "quote") in self.quote_reply_key_keepers.keys():
    #                 self.user_level_quote_reply_network.edges[source, quote_destination, self.quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")]]["weight"] += 1
    #             else:
    #                 self.quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
    #                 key_code += 1
    #                 self.user_level_quote_reply_network.add_edge(source, quote_destination, key=self.quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")], kind="quote", weight=1)
    #
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.quote_reply_key_keepers.keys():
    #                 self.user_level_quote_reply_network.edges[
    #                     source, reply_destination, self.quote_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_quote_reply_network.add_edge(source, reply_destination, key=self.quote_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = tweet.get_quote().get_twitter().get_screen_name()
    #                 inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (
    #                         inner_source, inner_quote_destination, "quote") in self.quote_reply_key_keepers.keys():
    #                     self.user_level_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #                 inner_reply_condition = tweet.get_quote().is_this_a_reply()
    #                 if inner_reply_condition:
    #                     inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.quote_reply_key_keepers.keys():
    #                         self.user_level_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, network_type)]][
    #                             "weight"] += 1
    #                     else:
    #                         self.quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #
    #         elif quote_condition is True and reply_condition is False:
    #             # source = tweet.get_twitter().get_screen_name()
    #             quote_destination = tweet.get_quote().get_twitter().get_screen_name()
    #
    #             # key_code = 0
    #             if (source, quote_destination, "quote") in self.quote_reply_key_keepers.keys():
    #                 self.user_level_quote_reply_network.edges[source, quote_destination, self.quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")]]["weight"] += 1
    #             else:
    #                 self.quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
    #                 key_code += 1
    #                 self.user_level_quote_reply_network.add_edge(source, quote_destination, key=self.quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")], kind="quote", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = tweet.get_quote().get_twitter().get_screen_name()
    #                 inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (inner_source, inner_quote_destination, "quote") in self.quote_reply_key_keepers.keys():
    #                     self.user_level_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #                 inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
    #                 if inner_reply_destination:
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.quote_reply_key_keepers.keys():
    #                         self.user_level_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, "reply")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #
    #         elif quote_condition is False and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.quote_reply_key_keepers.keys():
    #                 self.user_level_quote_reply_network.edges[
    #                     source, reply_destination, self.quote_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_quote_reply_network.add_edge(source, reply_destination, key=self.quote_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #         elif quote_condition is False and reply_condition is False:
    #             self.user_level_quote_reply_network.add_node(source)
    #
    # def user_level_retweet_reply_network_building(self):
    #     self.network_repository.append("user_level_retweet_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         key_code = 0
    #         source = tweet.get_twitter().get_screen_name()
    #
    #         if retweet_condition is True and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #
    #             if (source, retweet_destination, "retweet") in self.retweet_reply_key_keepers.keys():
    #                 self.user_level_retweet_reply_network.edges[source, retweet_destination, self.retweet_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")]]["weight"] += 1
    #             else:
    #                 self.retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_reply_network.add_edge(source, retweet_destination, key=self.retweet_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")], kind="retweet", weight=1)
    #
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.retweet_reply_key_keepers.keys():
    #                 self.user_level_retweet_reply_network.edges[
    #                     source, reply_destination, self.retweet_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_reply_network.add_edge(source, reply_destination, key=self.retweet_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #             inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
    #             if inner_reply_condition:
    #                 inner_source = retweet_destination
    #                 inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()
    #
    #                 if (
    #                         inner_source, inner_reply_destination,
    #                         "reply") in self.retweet_reply_key_keepers.keys():
    #                     self.user_level_retweet_reply_network.edges[
    #                         inner_source, inner_reply_destination, self.retweet_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_reply_key_keepers[
    #                         (inner_source, inner_reply_destination, "reply")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                            key=self.retweet_reply_key_keepers[
    #                                                (inner_source, inner_reply_destination, "reply")],
    #                                            kind="reply", weight=1)
    #
    #         elif retweet_condition is True and reply_condition is False:
    #             # source = tweet.get_twitter().get_screen_name()
    #             retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #
    #             if (source, retweet_destination, "retweet") in self.retweet_reply_key_keepers.keys():
    #                 self.user_level_retweet_reply_network.edges[source, retweet_destination, self.retweet_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")]]["weight"] += 1
    #             else:
    #                 self.retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_reply_network.add_edge(source, retweet_destination, key=self.retweet_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")], kind="retweet", weight=1)
    #
    #             inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
    #             if inner_reply_condition:
    #                 inner_source = retweet_destination
    #                 inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()
    #
    #                 if (
    #                         inner_source, inner_reply_destination,
    #                         "reply") in self.retweet_reply_key_keepers.keys():
    #                     self.user_level_retweet_reply_network.edges[
    #                         inner_source, inner_reply_destination, self.retweet_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_reply_key_keepers[
    #                         (inner_source, inner_reply_destination, "reply")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                            key=self.retweet_reply_key_keepers[
    #                                                (inner_source, inner_reply_destination, "reply")],
    #                                            kind="reply", weight=1)
    #
    #         elif retweet_condition is False and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.retweet_reply_key_keepers.keys():
    #                 self.user_level_retweet_reply_network.edges[
    #                     source, reply_destination, self.retweet_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_reply_network.add_edge(source, reply_destination, key=self.retweet_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #         elif retweet_condition is False and reply_condition is False:
    #             self.user_level_retweet_reply_network.add_node(source)
    #
    # def user_level_retweet_quote_network_building(self):
    #     self.network_repository.append("user_level_retweet_quote_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         quote_condition = tweet.is_quote_available()
    #
    #         key_code = 0
    #         source = tweet.get_twitter().get_screen_name()
    #         # if retweet_condition is True and quote_condition is True: #Not possible
    #         if retweet_condition is True and quote_condition is False:
    #             # source = tweet.get_twitter().get_screen_name()
    #             retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #
    #             if (source, retweet_destination, "retweet") in self.retweet_quote_key_keepers.keys():
    #                 self.user_level_retweet_quote_network.edges[source, retweet_destination, self.retweet_quote_key_keepers[
    #                     (source, retweet_destination, "retweet")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_key_keepers[(source, retweet_destination, "retweet")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_network.add_edge(source, retweet_destination, key=self.retweet_quote_key_keepers[
    #                     (source, retweet_destination, "retweet")], kind="retweet", weight=1)
    #
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #             if inner_quote_condition_level_one:
    #                 inner_source = retweet_destination
    #                 inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 # inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (inner_source, inner_quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
    #                     self.user_level_retweet_quote_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 if inner_quote_condition_level_two:
    #                     inner_source_level_two = inner_quote_destination
    #                     inner_quote_destination_level_two = tweet.get_quote().get_inner_quote_screen_name()
    #                     if (inner_source_level_two, inner_quote_destination_level_two,
    #                         "quote") in self.retweet_quote_key_keepers.keys():
    #                         self.user_level_retweet_quote_network.edges[
    #                             inner_source_level_two, inner_quote_destination_level_two,
    #                             self.retweet_quote_key_keepers[
    #                                 (inner_source_level_two, inner_quote_destination_level_two, "quote")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_key_keepers[
    #                             (inner_source_level_two, inner_quote_destination_level_two, "quote")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_network.add_edge(inner_source_level_two, inner_quote_destination_level_two,
    #                                                key=self.retweet_quote_key_keepers[
    #                                                    (inner_source_level_two, inner_quote_destination_level_two,
    #                                                     "quote")],
    #                                                kind="quote", weight=1)
    #
    #         elif retweet_condition is False and quote_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             quote_destination = tweet.get_quote().get_twitter().get_screen_name()
    #
    #             # key_code = 0
    #             if (source, quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
    #                 self.user_level_retweet_quote_network.edges[source, quote_destination, self.retweet_quote_key_keepers[
    #                     (source, quote_destination, "quote")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_key_keepers[(source, quote_destination, "quote")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_network.add_edge(source, quote_destination, key=self.retweet_quote_key_keepers[
    #                     (source, quote_destination, "quote")], kind="quote", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = quote_destination
    #                 inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (inner_source, inner_quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
    #                     self.user_level_retweet_quote_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #
    #         elif retweet_condition is False and quote_condition is False:
    #             self.user_level_retweet_quote_network.add_node(source)
    #
    # # retweet-quote-reply network
    # def user_level_retweet_quote_reply_network_building(self):
    #     self.network_repository.append("user_level_retweet_quote_reply_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         retweet_condition = tweet.is_retweeted()
    #         quote_condition = tweet.is_quote_available()
    #         reply_condition = tweet.is_this_a_reply()
    #
    #         key_code = 0
    #         source = tweet.get_twitter().get_screen_name()
    #
    #         if retweet_condition is True and quote_condition is False and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #
    #             if (source, retweet_destination, "retweet") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[source, retweet_destination, self.retweet_quote_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, retweet_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")], kind="retweet", weight=1)
    #
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[
    #                     source, reply_destination, self.retweet_quote_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #             inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #
    #             if inner_reply_condition_level_one:
    #                 inner_source = retweet_destination
    #                 inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()
    #
    #                 if (
    #                         inner_source, inner_reply_destination,
    #                         "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_reply_destination, "reply")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_reply_destination, "reply")],
    #                                            kind="reply", weight=1)
    #             if inner_quote_condition_level_one:
    #                 inner_source = retweet_destination
    #                 inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 if (
    #                         inner_source, inner_quote_destination,
    #                         "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
    #
    #                 if inner_reply_condition_level_two:
    #                     inner_source = inner_quote_destination
    #                     inner_reply_destination = tweet.get_retweeted().get_quote().get_in_reply_to_screen_name()
    #
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, "reply")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #                 if inner_quote_condition_level_two:
    #                     inner_source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                     inner_quote_destination = inner_quote_destination
    #                     if (
    #                             inner_source, inner_quote_destination,
    #                             "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                                 (source, inner_quote_destination, "quote")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_quote_destination, "quote")],
    #                                                kind="quote", weight=1)
    #         elif retweet_condition is True and quote_condition is False and reply_condition is False:
    #             # source = tweet.get_twitter().get_screen_name()
    #             retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()
    #
    #             if (source, retweet_destination, "retweet") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[source, retweet_destination, self.retweet_quote_reply_key_keepers[
    #                     (source, retweet_destination, "retweet")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, retweet_destination,
    #                                        key=self.retweet_quote_reply_key_keepers[
    #                                            (source, retweet_destination, "retweet")], kind="retweet",
    #                                        weight=1)
    #
    #             inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
    #             inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
    #
    #             if inner_reply_condition_level_one:
    #                 inner_source = retweet_destination
    #                 inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()
    #
    #                 if (
    #                         inner_source, inner_reply_destination,
    #                         "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_reply_destination, "reply")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_reply_destination, "reply")],
    #                                            kind="reply", weight=1)
    #             if inner_quote_condition_level_one:
    #                 inner_source = retweet_destination
    #                 inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 if (
    #                         inner_source, inner_quote_destination,
    #                         "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #
    #                 inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
    #                 inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
    #
    #                 if inner_reply_condition_level_two:
    #                     inner_source = inner_quote_destination
    #                     inner_reply_destination = tweet.get_retweeted().get_quote().get_in_reply_to_screen_name()
    #
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, "reply")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #                 if inner_quote_condition_level_two:
    #                     inner_source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                     inner_quote_destination = inner_quote_destination
    #                     if (
    #                             inner_source, inner_quote_destination,
    #                             "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                                 (source, inner_quote_destination, "quote")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_quote_destination, "quote")],
    #                                                kind="quote", weight=1)
    #         elif retweet_condition is False and quote_condition is True and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             quote_destination = tweet.get_quote().get_twitter().get_screen_name()
    #
    #             # key_code = 0
    #             if (source, quote_destination, "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[source, quote_destination, self.retweet_quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, quote_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")], kind="quote", weight=1)
    #
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[
    #                     source, reply_destination, self.retweet_quote_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = quote_destination
    #                 inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (
    #                         inner_source, inner_quote_destination,
    #                         "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #                 inner_reply_condition = tweet.get_quote().is_this_a_reply()
    #                 if inner_reply_condition:
    #                     inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, "reply")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #         elif retweet_condition is False and quote_condition is True and reply_condition is False:
    #             # source = tweet.get_twitter().get_screen_name()
    #             quote_destination = tweet.get_quote().get_twitter().get_screen_name()
    #
    #             # key_code = 0
    #             if (source, quote_destination, "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[source, quote_destination, self.retweet_quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")]]["weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, quote_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, quote_destination, "quote")], kind="quote", weight=1)
    #
    #             inner_quote_condition = tweet.get_quote().is_quoted()
    #             if inner_quote_condition:
    #                 inner_source = quote_destination
    #                 inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
    #                 if (
    #                         inner_source, inner_quote_destination,
    #                         "quote") in self.retweet_quote_reply_key_keepers.keys():
    #                     self.user_level_retweet_quote_reply_network.edges[
    #                         inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_quote_destination, "quote")]][
    #                         "weight"] += 1
    #                 else:
    #                     self.retweet_quote_reply_key_keepers[
    #                         (inner_source, inner_quote_destination, "quote")] = key_code
    #                     key_code += 1
    #                     self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
    #                                            key=self.retweet_quote_reply_key_keepers[
    #                                                (inner_source, inner_quote_destination, "quote")],
    #                                            kind="quote", weight=1)
    #                 inner_reply_condition = tweet.get_quote().is_this_a_reply()
    #                 if inner_reply_condition:
    #                     inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
    #                     if (
    #                             inner_source, inner_reply_destination,
    #                             "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                         self.user_level_retweet_quote_reply_network.edges[
    #                             inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
    #                                 (inner_source, inner_reply_destination, "reply")]][
    #                             "weight"] += 1
    #                     else:
    #                         self.retweet_quote_reply_key_keepers[
    #                             (inner_source, inner_reply_destination, "reply")] = key_code
    #                         key_code += 1
    #                         self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
    #                                                key=self.retweet_quote_reply_key_keepers[
    #                                                    (inner_source, inner_reply_destination, "reply")],
    #                                                kind="reply", weight=1)
    #         elif retweet_condition is False and quote_condition is False and reply_condition is True:
    #             # source = tweet.get_twitter().get_screen_name()
    #             reply_destination = tweet.get_in_reply_to_screen_name()
    #             if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
    #                 self.user_level_retweet_quote_reply_network.edges[
    #                     source, reply_destination, self.retweet_quote_reply_key_keepers[
    #                         (source, reply_destination, "reply")]][
    #                     "weight"] += 1
    #             else:
    #                 self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
    #                 key_code += 1
    #                 self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
    #                     (source, reply_destination, "reply")], kind="reply", weight=1)
    #         elif retweet_condition is False and quote_condition is False and reply_condition is False:
    #             self.user_level_retweet_quote_reply_network.add_node(source)
    #
    # # user-level co-occurence hashtag/mention/url networks
    # def user_level_cooccurrence_hashtag_network_building(self):  # Thinking of pruning hashtags      #also adding tweet_ids as a feature instead of deleting them (convert them to a a string)
    #     self.network_repository.append("user_level_cooccurrence_hashtag_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         user1 = tweet1.get_twitter().get_screen_name()
    #         tweet1_hashtags = tweet1.get_hashtags()
    #
    #         j = i + 1
    #
    #         self.user_level_cooccurrence_hashtag_network.add_node(user1)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #
    #             if (user1, user1_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                 if (tweet1.get_id(), tweet1_rt.get_id()) not in \
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt][
    #                             "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"]:
    #                     for ht in tweet1_hashtags:
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + ht
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["hashtags"] += edge_label
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #             else:
    #                 for ht in tweet1_hashtags:
    #                     if (user1, user1_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + ht
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["hashtags"] += edge_label
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #                     else:
    #                         self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt, weight=1, hashtags=ht,
    #                                                                  tweets=[(tweet1.get_id(), tweet1_rt.get_id())])
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                 tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                     if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"]:
    #                         for ht1 in tweet1_hashtags:
    #                             for ht2 in tweet1_rt_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
    #                                         "hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet1_rt_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
    #                                         "hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt_qt, weight=1,
    #                                                                              hashtags=ht1,
    #                                                                              tweets=[(tweet1.get_id(),
    #                                                                                       tweet1_rt_qt.get_id())])
    #
    #                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                     if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"]:
    #                         for ht1 in tweet1_hashtags:
    #                             for ht2 in tweet1_rt_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
    #                                         "hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet1_rt_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
    #                                         "hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user1_rt_qt, weight=1,
    #                                                                              hashtags=ht1, tweets=[
    #                                             (tweet1_rt.get_id(), tweet1_rt_qt.get_id())])
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #             tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #             if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                 if (tweet1.get_id(), tweet1_qt.get_id()) not in \
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
    #                             "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"]:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet1_qt_hashtags:
    #                             if ht1 == ht2:
    #                                 # if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + ht1
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["hashtags"] += edge_label
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #             else:
    #                 for ht1 in tweet1_hashtags:
    #                     for ht2 in tweet1_qt_hashtags:
    #                         if ht1 == ht2:
    #                             if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + ht1
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["hashtags"] += edge_label
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #                             else:
    #                                 self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_qt, weight=1, hashtags=ht1,
    #                                                                          tweets=[
    #                                                                              (tweet1.get_id(), tweet1_qt.get_id())])
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             user2 = tweet2.get_twitter().get_screen_name()
    #             tweet2_hashtags = tweet2.get_hashtags()
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #
    #                 if tweet1.get_id() != tweet2_rt.get_id():
    #                     if (user1, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"]:
    #                             for ht1 in tweet1_hashtags:
    #                                 for ht2 in tweet2_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_hashtags:
    #                             for ht2 in tweet2_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_rt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1.get_id(), tweet2_rt.get_id())])
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                         tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                         if tweet1.get_id() != tweet2_rt_qt.get_id():
    #                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                 if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt]["tweets"] and (
    #                                         tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt]["tweets"]:
    #                                     for ht1 in tweet1_hashtags:
    #                                         for ht2 in tweet2_rt_qt_hashtags:
    #                                             if ht1 == ht2:
    #                                                 # if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + ht1
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "hashtags"] += edge_label
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "tweets"] += [(tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                             else:
    #                                 for ht1 in tweet1_hashtags:
    #                                     for ht2 in tweet2_rt_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + ht1
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "hashtags"] += edge_label
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
    #                                                     "tweets"] += [
    #                                                     (tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_rt_qt,
    #                                                                                          weight=1,
    #                                                                                          hashtags=ht1, tweets=[
    #                                                         (tweet1.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1.get_id() != tweet2_qt.get_id():
    #                     if (user1, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"]:
    #                             for ht1 in tweet1_hashtags:
    #                                 for ht2 in tweet2_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_hashtags:
    #                             for ht2 in tweet2_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_qt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 if tweet1_rt.get_id() != tweet2_rt.get_id():
    #                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"]:
    #                             for ht1 in tweet1_rt_hashtags:
    #                                 for ht2 in tweet2_rt_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_rt_hashtags:
    #                             for ht2 in tweet2_rt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_rt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2_rt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
    #                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
    #                                     tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt]["tweets"]:
    #                                 for ht1 in tweet1_rt_qt_hashtags:
    #                                     for ht2 in tweet2_rt_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                         else:
    #                             for ht1 in tweet1_rt_qt_hashtags:
    #                                 for ht2 in tweet2_rt_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_rt,
    #                                                                                      weight=1,
    #                                                                                      hashtags=ht1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt]["tweets"]:
    #                                 for ht1 in tweet1_rt_hashtags:
    #                                     for ht2 in tweet2_rt_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for ht1 in tweet1_rt_hashtags:
    #                                 for ht2 in tweet2_rt_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_rt_qt,
    #                                                                                      weight=1,
    #                                                                                      hashtags=ht1, tweets=[
    #                                                     (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
    #                                 for ht1 in tweet1_rt_qt_hashtags:
    #                                     for ht2 in tweet2_rt_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                 for ht1 in tweet1_rt_qt_hashtags:
    #                                     for ht2 in tweet2_rt_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + ht1
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "hashtags"] += edge_label
    #                                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_rt_qt,
    #                                                                                          weight=1, hashtags=ht1,
    #                                                                                          tweets=[
    #                                                                                              (tweet1_rt_qt.get_id(),
    #                                                                                               tweet2_rt_qt.get_id())])
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1_qt.get_id() != tweet2_qt.get_id():
    #                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"]:
    #                             for ht1 in tweet1_qt_hashtags:
    #                                 for ht2 in tweet2_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         # if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_qt_hashtags:
    #                             for ht2 in tweet2_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_qt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2_qt.get_id())])
    #                                 # else:
    #                                 #     self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_qt, weight=1, hashtags=ht1, tweets=[(tweet1_qt.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_hashtags = tweet2_qt.get_hashtags()
    #
    #                 if tweet1_rt.get_id() != tweet2_qt.get_id():
    #                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"]:
    #                             for ht1 in tweet1_rt_hashtags:
    #                                 for ht2 in tweet2_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_rt_hashtags:
    #                             for ht2 in tweet2_qt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_qt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2_qt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
    #                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
    #                                     tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt]["tweets"]:
    #                                 for ht1 in tweet1_rt_qt_hashtags:
    #                                     for ht2 in tweet2_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                         else:
    #                             for ht1 in tweet1_rt_qt_hashtags:
    #                                 for ht2 in tweet2_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_qt,
    #                                                                                      weight=1,
    #                                                                                      hashtags=ht1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_hashtags = tweet2_rt.get_hashtags()
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 if tweet1_qt.get_id() != tweet2_rt.get_id():
    #                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"]:
    #                             for ht1 in tweet1_qt_hashtags:
    #                                 for ht2 in tweet2_rt_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ht1 in tweet1_qt_hashtags:
    #                             for ht2 in tweet2_rt_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_rt, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2_rt.get_id())])
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()
    #
    #                     if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt]["tweets"]:
    #                                 for ht1 in tweet1_qt_hashtags:
    #                                     for ht2 in tweet2_rt_qt_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for ht1 in tweet1_qt_hashtags:
    #                                 for ht2 in tweet2_rt_qt_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_rt_qt,
    #                                                                                      weight=1,
    #                                                                                      hashtags=ht1, tweets=[
    #                                                     (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_hashtags = tweet1_rt.get_hashtags()
    #
    #                 if tweet1_rt.get_id() != tweet2.get_id():
    #                     if (user1_rt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"]:
    #                             for ht1 in tweet1_rt_hashtags:
    #                                 for ht2 in tweet2_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for ht1 in tweet1_rt_hashtags:
    #                             for ht2 in tweet2_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_rt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2.get_id():
    #                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] and (
    #                                     tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"]:
    #                                 for ht1 in tweet1_rt_qt_hashtags:
    #                                     for ht2 in tweet2_hashtags:
    #                                         if ht1 == ht2:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                         else:
    #                             for ht1 in tweet1_rt_qt_hashtags:
    #                                 for ht2 in tweet2_hashtags:
    #                                     if ht1 == ht2:
    #                                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + ht1
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
    #                                                 "hashtags"] += edge_label
    #                                             self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2, weight=1,
    #                                                                                      hashtags=ht1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2.get_id())])
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_hashtags = tweet1_qt.get_hashtags()
    #
    #                 if tweet1_qt.get_id() != tweet2.get_id():
    #                     if (user1_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"]:
    #                             for ht1 in tweet1_qt_hashtags:
    #                                 for ht2 in tweet2_hashtags:
    #                                     if ht1 == ht2:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for ht1 in tweet1_qt_hashtags:
    #                             for ht2 in tweet2_hashtags:
    #                                 if ht1 == ht2:
    #                                     if (user1_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + ht1
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
    #                                             "hashtags"] += edge_label
    #                                         self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2, weight=1,
    #                                                                                  hashtags=ht1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2.get_id())])
    #
    #             if tweet1.get_id() != tweet2.get_id():
    #                 if (user1, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                     if (tweet1.get_id(), tweet2.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1, user2][
    #                                 "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"]:
    #                         for ht1 in tweet1_hashtags:
    #                             for ht2 in tweet2_hashtags:
    #                                 if ht1 == ht2:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                 else:
    #                     for ht1 in tweet1_hashtags:
    #                         for ht2 in tweet2_hashtags:
    #                             if ht1 == ht2:
    #                                 if (user1, user2) in self.user_level_cooccurrence_hashtag_network.edges:
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + ht1
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["hashtags"] += edge_label
    #                                     self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2, weight=1, hashtags=ht1,
    #                                                                              tweets=[
    #                                                                                  (
    #                                                                                  tweet1.get_id(), tweet2.get_id())])
    #             j += 1
    #
    #     for edge in self.user_level_cooccurrence_hashtag_network.edges:
    #         del self.user_level_cooccurrence_hashtag_network.edges[edge]["tweets"]
    #
    # def user_level_cooccurrence_mention_network_building(self):
    #     self.network_repository.append("user_level_cooccurrence_mention_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         user1 = tweet1.get_twitter().get_screen_name()
    #         tweet1_mentions = tweet1.get_mentions()
    #
    #         j = i + 1
    #
    #         self.user_level_cooccurrence_mention_network.add_node(user1)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #
    #             if (user1, user1_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                 if (tweet1.get_id(), tweet1_rt.get_id()) not in \
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt][
    #                             "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"]:
    #                     for mt in tweet1_mentions:
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + mt
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["mentions"] += edge_label
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #             else:
    #                 for mt in tweet1_mentions:
    #                     if (user1, user1_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + mt
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["mentions"] += edge_label
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #                     else:
    #                         self.user_level_cooccurrence_mention_network.add_edge(user1, user1_rt, weight=1, mentions=mt,
    #                                                                  tweets=[(tweet1.get_id(), tweet1_rt.get_id())])
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                 tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                     if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"]:
    #                         for mt1 in tweet1_mentions:
    #                             for mt2 in tweet1_rt_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
    #                                         "mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet1_rt_qt_mentions:
    #                             if mt1 == mt2:
    #                                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
    #                                         "mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_mention_network.add_edge(user1, user1_rt_qt, weight=1,
    #                                                                              mentions=mt1,
    #                                                                              tweets=[(tweet1.get_id(),
    #                                                                                       tweet1_rt_qt.get_id())])
    #
    #                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                     if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"]:
    #                         for mt1 in tweet1_mentions:
    #                             for mt2 in tweet1_rt_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
    #                                         "mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet1_rt_qt_mentions:
    #                             if mt1 == mt2:
    #                                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
    #                                         "mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user1_rt_qt, weight=1,
    #                                                                              mentions=mt1, tweets=[
    #                                             (tweet1_rt.get_id(), tweet1_rt_qt.get_id())])
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #             tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #             if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                 if (tweet1.get_id(), tweet1_qt.get_id()) not in \
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_qt][
    #                             "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"]:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet1_qt_mentions:
    #                             if mt1 == mt2:
    #                                 # if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + mt1
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["mentions"] += edge_label
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #             else:
    #                 for mt1 in tweet1_mentions:
    #                     for mt2 in tweet1_qt_mentions:
    #                         if mt1 == mt2:
    #                             if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + mt1
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["mentions"] += edge_label
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #                             else:
    #                                 self.user_level_cooccurrence_mention_network.add_edge(user1, user1_qt, weight=1, mentions=mt1,
    #                                                                          tweets=[
    #                                                                              (tweet1.get_id(), tweet1_qt.get_id())])
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             user2 = tweet2.get_twitter().get_screen_name()
    #             tweet2_mentions = tweet2.get_mentions()
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #
    #                 if tweet1.get_id() != tweet2_rt.get_id():
    #                     if (user1, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"]:
    #                             for mt1 in tweet1_mentions:
    #                                 for mt2 in tweet2_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_mentions:
    #                             for mt2 in tweet2_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1, user2_rt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1.get_id(), tweet2_rt.get_id())])
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                         tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                         if tweet1.get_id() != tweet2_rt_qt.get_id():
    #                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                 if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt]["tweets"] and (
    #                                         tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt]["tweets"]:
    #                                     for mt1 in tweet1_mentions:
    #                                         for mt2 in tweet2_rt_qt_mentions:
    #                                             if mt1 == mt2:
    #                                                 # if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + mt1
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "mentions"] += edge_label
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "tweets"] += [(tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                             else:
    #                                 for mt1 in tweet1_mentions:
    #                                     for mt2 in tweet2_rt_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + mt1
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "mentions"] += edge_label
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
    #                                                     "tweets"] += [
    #                                                     (tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_mention_network.add_edge(user1, user2_rt_qt,
    #                                                                                          weight=1,
    #                                                                                          mentions=mt1, tweets=[
    #                                                         (tweet1.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1.get_id() != tweet2_qt.get_id():
    #                     if (user1, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"]:
    #                             for mt1 in tweet1_mentions:
    #                                 for mt2 in tweet2_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_mentions:
    #                             for mt2 in tweet2_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1, user2_qt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 if tweet1_rt.get_id() != tweet2_rt.get_id():
    #                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"]:
    #                             for mt1 in tweet1_rt_mentions:
    #                                 for mt2 in tweet2_rt_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_rt_mentions:
    #                             for mt2 in tweet2_rt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_rt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2_rt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
    #                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
    #                                     tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt]["tweets"]:
    #                                 for mt1 in tweet1_rt_qt_mentions:
    #                                     for mt2 in tweet2_rt_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                         else:
    #                             for mt1 in tweet1_rt_qt_mentions:
    #                                 for mt2 in tweet2_rt_mentions:
    #                                     if mt1 == mt2:
    #                                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_rt,
    #                                                                                      weight=1,
    #                                                                                      mentions=mt1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt]["tweets"]:
    #                                 for mt1 in tweet1_rt_mentions:
    #                                     for mt2 in tweet2_rt_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for mt1 in tweet1_rt_mentions:
    #                                 for mt2 in tweet2_rt_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_rt_qt,
    #                                                                                      weight=1,
    #                                                                                      mentions=mt1, tweets=[
    #                                                     (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
    #                                 for mt1 in tweet1_rt_qt_mentions:
    #                                     for mt2 in tweet2_rt_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                 for mt1 in tweet1_rt_qt_mentions:
    #                                     for mt2 in tweet2_rt_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + mt1
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "mentions"] += edge_label
    #                                                 self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_rt_qt,
    #                                                                                          weight=1, mentions=mt1,
    #                                                                                          tweets=[
    #                                                                                              (tweet1_rt_qt.get_id(),
    #                                                                                               tweet2_rt_qt.get_id())])
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1_qt.get_id() != tweet2_qt.get_id():
    #                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"]:
    #                             for mt1 in tweet1_qt_mentions:
    #                                 for mt2 in tweet2_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         # if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_qt_mentions:
    #                             for mt2 in tweet2_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_qt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_mentions = tweet2_qt.get_mentions()
    #
    #                 if tweet1_rt.get_id() != tweet2_qt.get_id():
    #                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"]:
    #                             for mt1 in tweet1_rt_mentions:
    #                                 for mt2 in tweet2_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_rt_mentions:
    #                             for mt2 in tweet2_qt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_qt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2_qt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
    #                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
    #                                     tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt]["tweets"]:
    #                                 for mt1 in tweet1_rt_qt_mentions:
    #                                     for mt2 in tweet2_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                         else:
    #                             for mt1 in tweet1_rt_qt_mentions:
    #                                 for mt2 in tweet2_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_qt,
    #                                                                                      weight=1,
    #                                                                                      mentions=mt1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2_qt.get_id())])
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_mentions = tweet2_rt.get_mentions()
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 if tweet1_qt.get_id() != tweet2_rt.get_id():
    #                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"]:
    #                             for mt1 in tweet1_qt_mentions:
    #                                 for mt2 in tweet2_rt_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for mt1 in tweet1_qt_mentions:
    #                             for mt2 in tweet2_rt_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_rt, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2_rt.get_id())])
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()
    #
    #                     if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt]["tweets"]:
    #                                 for mt1 in tweet1_qt_mentions:
    #                                     for mt2 in tweet2_rt_qt_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for mt1 in tweet1_qt_mentions:
    #                                 for mt2 in tweet2_rt_qt_mentions:
    #                                     if mt1 == mt2:
    #                                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_rt_qt,
    #                                                                                      weight=1,
    #                                                                                      mentions=mt1, tweets=[
    #                                                     (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_mentions = tweet1_rt.get_mentions()
    #
    #                 if tweet1_rt.get_id() != tweet2.get_id():
    #                     if (user1_rt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"]:
    #                             for mt1 in tweet1_rt_mentions:
    #                                 for mt2 in tweet2_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for mt1 in tweet1_rt_mentions:
    #                             for mt2 in tweet2_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_rt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_rt.get_id(), tweet2.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()
    #
    #                     if tweet1_rt_qt.get_id() != tweet2.get_id():
    #                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] and (
    #                                     tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"]:
    #                                 for mt1 in tweet1_rt_qt_mentions:
    #                                     for mt2 in tweet2_mentions:
    #                                         if mt1 == mt2:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                         else:
    #                             for mt1 in tweet1_rt_qt_mentions:
    #                                 for mt2 in tweet2_mentions:
    #                                     if mt1 == mt2:
    #                                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + mt1
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
    #                                                 "mentions"] += edge_label
    #                                             self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2, weight=1,
    #                                                                                      mentions=mt1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2.get_id())])
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_mentions = tweet1_qt.get_mentions()
    #
    #                 if tweet1_qt.get_id() != tweet2.get_id():
    #                     if (user1_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"]:
    #                             for mt1 in tweet1_qt_mentions:
    #                                 for mt2 in tweet2_mentions:
    #                                     if mt1 == mt2:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for mt1 in tweet1_qt_mentions:
    #                             for mt2 in tweet2_mentions:
    #                                 if mt1 == mt2:
    #                                     if (user1_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + mt1
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2][
    #                                             "mentions"] += edge_label
    #                                         self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2, weight=1,
    #                                                                                  mentions=mt1, tweets=[
    #                                                 (tweet1_qt.get_id(), tweet2.get_id())])
    #
    #             if tweet1.get_id() != tweet2.get_id():
    #                 if (user1, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                     if (tweet1.get_id(), tweet2.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1, user2][
    #                                 "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"]:
    #                         for mt1 in tweet1_mentions:
    #                             for mt2 in tweet2_mentions:
    #                                 if mt1 == mt2:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                 else:
    #                     for mt1 in tweet1_mentions:
    #                         for mt2 in tweet2_mentions:
    #                             if mt1 == mt2:
    #                                 if (user1, user2) in self.user_level_cooccurrence_mention_network.edges:
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + mt1
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["mentions"] += edge_label
    #                                     self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_mention_network.add_edge(user1, user2, weight=1, mentions=mt1,
    #                                                                              tweets=[
    #                                                                                  (
    #                                                                                  tweet1.get_id(), tweet2.get_id())])
    #             j += 1
    #
    #     for edge in self.user_level_cooccurrence_mention_network.edges:
    #         del self.user_level_cooccurrence_mention_network.edges[edge]["tweets"]
    #
    # def user_level_cooccurrence_url_network_building(self):
    #     self.network_repository.append("user_level_cooccurrence_url_network")
    #
    #     tweets_keys = list(self.tweets.keys())
    #     for i in range(len(tweets_keys)):
    #         tweet1 = self.tweets[tweets_keys[i]]
    #         user1 = tweet1.get_twitter().get_screen_name()
    #         tweet1_urls = tweet1.get_tweet_urls(return_format="expanded_url")
    #
    #         j = i + 1
    #
    #         self.user_level_cooccurrence_url_network.add_node(user1)
    #
    #         tweet1_retweet_condition = tweet1.is_retweeted()
    #         tweet1_quote_condition = tweet1.is_quote_available()
    #
    #         if tweet1_retweet_condition:
    #             tweet1_rt = tweet1.get_retweeted()
    #             user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #
    #             if (user1, user1_rt) in self.user_level_cooccurrence_url_network.edges:
    #                 if (tweet1.get_id(), tweet1_rt.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user1_rt][
    #                     "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"]:
    #                     for ut in tweet1_urls:
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + ut
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #             else:
    #                 for ut in tweet1_urls:
    #                     if (user1, user1_rt) in self.user_level_cooccurrence_url_network.edges:
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
    #                         edge_label = "-" + ut
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
    #                             (tweet1.get_id(), tweet1_rt.get_id())]
    #                     else:
    #                         self.user_level_cooccurrence_url_network.add_edge(user1, user1_rt, weight=1, urls=ut,
    #                                                              tweets=[(tweet1.get_id(), tweet1_rt.get_id())])
    #
    #             tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #             if tweet1_inner_quote_condition:
    #                 tweet1_rt_qt = tweet1_rt.get_quote()
    #                 user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                 tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                     if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"]:
    #                         for ut1 in tweet1_urls:
    #                             for ut2 in tweet1_rt_qt_urls:
    #                                 if ut1 == ut2:
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet1_rt_qt_urls:
    #                             if ut1 == ut2:
    #                                 if (user1, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] += [
    #                                         (tweet1.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_url_network.add_edge(user1, user1_rt_qt, weight=1, urls=ut1,
    #                                                                          tweets=[
    #                                                                              (tweet1.get_id(),
    #                                                                               tweet1_rt_qt.get_id())])
    #
    #                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                     if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
    #                             tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                             self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"]:
    #                         for ut1 in tweet1_urls:
    #                             for ut2 in tweet1_rt_qt_urls:
    #                                 if ut1 == ut2:
    #                                     # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                 else:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet1_rt_qt_urls:
    #                             if ut1 == ut2:
    #                                 if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
    #                                         "urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
    #                                         (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_url_network.add_edge(user1_rt, user1_rt_qt, weight=1, urls=ut1,
    #                                                                          tweets=[(tweet1_rt.get_id(),
    #                                                                                   tweet1_rt_qt.get_id())])
    #
    #         if tweet1_quote_condition:
    #             tweet1_qt = tweet1.get_quote()
    #             user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #             tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #             if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
    #                 if (tweet1.get_id(), tweet1_qt.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user1_qt][
    #                     "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
    #                         self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"]:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet1_qt_urls:
    #                             if ut1 == ut2:
    #                                 # if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + ut1
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["urls"] += edge_label
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #             else:
    #                 for ut1 in tweet1_urls:
    #                     for ut2 in tweet1_qt_urls:
    #                         if ut1 == ut2:
    #                             if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
    #                                 edge_label = "-" + ut1
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["urls"] += edge_label
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
    #                                     (tweet1.get_id(), tweet1_qt.get_id())]
    #                             else:
    #                                 self.user_level_cooccurrence_url_network.add_edge(user1, user1_qt, weight=1, urls=ut1,
    #                                                                      tweets=[(tweet1.get_id(), tweet1_qt.get_id())])
    #
    #         while j != len(tweets_keys):
    #             tweet2 = self.tweets[tweets_keys[j]]
    #             user2 = tweet2.get_twitter().get_screen_name()
    #             tweet2_urls = tweet2.get_tweet_urls(return_format="expanded_url")
    #
    #             tweet2_retweet_condition = tweet2.is_retweeted()
    #             tweet2_quote_condition = tweet2.is_quote_available()
    #
    #             if tweet2_retweet_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #
    #                 if tweet1.get_id() != tweet2_rt.get_id():
    #                     if (user1, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt][
    #                                     "tweets"]:
    #                             for ut1 in tweet1_urls:
    #                                 for ut2 in tweet2_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_urls:
    #                             for ut2 in tweet2_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1, user2_rt, weight=1, urls=ut1,
    #                                                                              tweets=[
    #                                                                                  (tweet1.get_id(),
    #                                                                                   tweet2_rt.get_id())])
    #
    #                     tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                     if tweet2_inner_quote_condition:
    #                         tweet2_rt_qt = tweet2_rt.get_quote()
    #                         user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                         tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                         if tweet1.get_id() != tweet2_rt_qt.get_id():
    #                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                 if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] and (
    #                                         tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"]:
    #                                     for ut1 in tweet1_urls:
    #                                         for ut2 in tweet2_rt_qt_urls:
    #                                             if ut1 == ut2:
    #                                                 # if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["weight"] += 1
    #                                                 edge_label = "-" + ut1
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
    #                                                     "urls"] += edge_label
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] += [
    #                                                     (tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                             else:
    #                                 for ut1 in tweet1_urls:
    #                                     for ut2 in tweet2_rt_qt_urls:
    #                                         if ut1 == ut2:
    #                                             if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["weight"] += 1
    #                                                 edge_label = "-" + ut1
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
    #                                                     "urls"] += edge_label
    #                                                 self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] += [
    #                                                     (tweet1.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_url_network.add_edge(user1, user2_rt_qt, weight=1,
    #                                                                                      urls=ut1, tweets=[
    #                                                         (tweet1.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet2_quote_condition:
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1.get_id() != tweet2_qt.get_id():
    #                     if (user1, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1, user2_qt][
    #                                     "tweets"]:
    #                             for ut1 in tweet1_urls:
    #                                 for ut2 in tweet2_qt_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_urls:
    #                             for ut2 in tweet2_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] += [
    #                                             (tweet1.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1, user2_qt, weight=1, urls=ut1,
    #                                                                              tweets=[
    #                                                                                  (tweet1.get_id(),
    #                                                                                   tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt.get_id() != tweet2_rt.get_id():
    #                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"]:
    #                             for ut1 in tweet1_rt_urls:
    #                                 for ut2 in tweet2_rt_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_rt_urls:
    #                             for ut2 in tweet2_rt_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_rt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_rt, weight=1, urls=ut1,
    #                                                                              tweets=[(tweet1_rt.get_id(),
    #                                                                                       tweet2_rt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
    #                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
    #                                     tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"]:
    #                                 for ut1 in tweet1_rt_qt_urls:
    #                                     for ut2 in tweet2_rt_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                         else:
    #                             for ut1 in tweet1_rt_qt_urls:
    #                                 for ut2 in tweet2_rt_urls:
    #                                     if ut1 == ut2:
    #                                         if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_rt, weight=1,
    #                                                                                  urls=ut1, tweets=[
    #                                                     (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])
    #
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"]:
    #                                 for ut1 in tweet1_rt_urls:
    #                                     for ut2 in tweet2_rt_qt_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for ut1 in tweet1_rt_urls:
    #                                 for ut2 in tweet2_rt_qt_urls:
    #                                     if ut1 == ut2:
    #                                         if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] += [
    #                                                 (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_rt_qt, weight=1,
    #                                                                                  urls=ut1, tweets=[
    #                                                     (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])
    #
    #                 if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     tweet2_rt_qt = tweet2.get_retweeted().get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
    #                                 for ut1 in tweet1_rt_qt_urls:
    #                                     for ut2 in tweet2_rt_qt_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                 "tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                 for ut1 in tweet1_rt_qt_urls:
    #                                     for ut2 in tweet2_rt_qt_urls:
    #                                         if ut1 == ut2:
    #                                             if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
    #                                                     "weight"] += 1
    #                                                 edge_label = "-" + ut1
    #                                                 self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "urls"] += edge_label
    #                                                 self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
    #                                                     "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                             else:
    #                                                 self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_rt_qt,
    #                                                                                      weight=1,
    #                                                                                      urls=ut1, tweets=[
    #                                                         (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet1_quote_condition and tweet2_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt.get_id() != tweet2_qt.get_id():
    #                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"]:
    #                             for ut1 in tweet1_qt_urls:
    #                                 for ut2 in tweet2_qt_urls:
    #                                     if ut1 == ut2:
    #                                         # if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_qt_urls:
    #                             for ut2 in tweet2_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_qt, weight=1, urls=ut1,
    #                                                                              tweets=[
    #                                                                                  (tweet1_qt.get_id(),
    #                                                                                   tweet2_qt.get_id())])
    #
    #             if tweet1_retweet_condition and tweet2_quote_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet2_qt = tweet2.get_quote()
    #                 user2_qt = tweet2_qt.get_twitter().get_screen_name()
    #                 tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt.get_id() != tweet2_qt.get_id():
    #                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] and (
    #                                 tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"]:
    #                             for ut1 in tweet1_rt_urls:
    #                                 for ut2 in tweet2_qt_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_rt_urls:
    #                             for ut2 in tweet2_qt_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_rt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2_qt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_qt, weight=1, urls=ut1,
    #                                                                              tweets=[(tweet1_rt.get_id(),
    #                                                                                       tweet2_qt.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1.get_retweeted().get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
    #                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
    #                                     tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"]:
    #                                 for ut1 in tweet1_rt_qt_urls:
    #                                     for ut2 in tweet2_qt_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                         else:
    #                             for ut1 in tweet1_rt_qt_urls:
    #                                 for ut2 in tweet2_qt_urls:
    #                                     if ut1 == ut2:
    #                                         if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_qt, weight=1,
    #                                                                                  urls=ut1,
    #                                                                                  tweets=[(tweet1_rt_qt.get_id(),
    #                                                                                           tweet2_qt.get_id())])
    #
    #             if tweet2_retweet_condition and tweet1_quote_condition:
    #                 tweet2_rt = tweet2.get_retweeted()
    #                 user2_rt = tweet2_rt.get_twitter().get_screen_name()
    #                 tweet2_rt_urls = tweet2_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt.get_id() != tweet2_rt.get_id():
    #                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] and (
    #                                 tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"]:
    #                             for ut1 in tweet1_qt_urls:
    #                                 for ut2 in tweet2_rt_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                     else:
    #                         for ut1 in tweet1_qt_urls:
    #                             for ut2 in tweet2_rt_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2_rt.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_rt, weight=1, urls=ut1,
    #                                                                              tweets=[(tweet1_qt.get_id(),
    #                                                                                       tweet2_rt.get_id())])
    #
    #                 tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
    #                 if tweet2_inner_quote_condition:
    #                     tweet2_rt_qt = tweet2_rt.get_quote()
    #                     user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
    #                     tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
    #                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
    #                                     tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"]:
    #                                 for ut1 in tweet1_qt_urls:
    #                                     for ut2 in tweet2_rt_qt_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                         else:
    #                             for ut1 in tweet1_qt_urls:
    #                                 for ut2 in tweet2_rt_qt_urls:
    #                                     if ut1 == ut2:
    #                                         if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] += [
    #                                                 (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_rt_qt, weight=1,
    #                                                                                  urls=ut1, tweets=[
    #                                                     (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])
    #
    #             if tweet1_retweet_condition:
    #                 tweet1_rt = tweet1.get_retweeted()
    #                 user1_rt = tweet1_rt.get_twitter().get_screen_name()
    #                 tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_rt.get_id() != tweet2.get_id():
    #                     if (user1_rt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_rt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_rt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_rt, user2][
    #                                     "tweets"]:
    #                             for ut1 in tweet1_rt_urls:
    #                                 for ut2 in tweet2_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for ut1 in tweet1_rt_urls:
    #                             for ut2 in tweet2_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_rt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] += [
    #                                             (tweet1_rt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2, weight=1, urls=ut1,
    #                                                                              tweets=[
    #                                                                                  (tweet1_rt.get_id(),
    #                                                                                   tweet2.get_id())])
    #
    #                 tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
    #                 if tweet1_inner_quote_condition:
    #                     tweet1_rt_qt = tweet1_rt.get_quote()
    #                     user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
    #                     tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                     if tweet1_rt_qt.get_id() != tweet2.get_id():
    #                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                             if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] and (
    #                                     tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
    #                                     self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"]:
    #                                 for ut1 in tweet1_rt_qt_urls:
    #                                     for ut2 in tweet2_urls:
    #                                         if ut1 == ut2:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                         else:
    #                             for ut1 in tweet1_rt_qt_urls:
    #                                 for ut2 in tweet2_urls:
    #                                     if ut1 == ut2:
    #                                         if (user1_rt_qt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["weight"] += 1
    #                                             edge_label = "-" + ut1
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
    #                                                 "urls"] += edge_label
    #                                             self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] += [
    #                                                 (tweet1_rt_qt.get_id(), tweet2.get_id())]
    #                                         else:
    #                                             self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2, weight=1,
    #                                                                                  urls=ut1,
    #                                                                                  tweets=[(tweet1_rt_qt.get_id(),
    #                                                                                           tweet2.get_id())])
    #
    #             if tweet1_quote_condition:
    #                 tweet1_qt = tweet1.get_quote()
    #                 user1_qt = tweet1_qt.get_twitter().get_screen_name()
    #                 tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")
    #
    #                 if tweet1_qt.get_id() != tweet2.get_id():
    #                     if (user1_qt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                         if (tweet1_qt.get_id(), tweet2.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] and (
    #                                 tweet2.get_id(), tweet1_qt.get_id()) not in \
    #                                 self.user_level_cooccurrence_url_network.edges[user1_qt, user2][
    #                                     "tweets"]:
    #                             for ut1 in tweet1_qt_urls:
    #                                 for ut2 in tweet2_urls:
    #                                     if ut1 == ut2:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                     else:
    #                         for ut1 in tweet1_qt_urls:
    #                             for ut2 in tweet2_urls:
    #                                 if ut1 == ut2:
    #                                     if (user1_qt, user2) in self.user_level_cooccurrence_url_network.edges:
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["weight"] += 1
    #                                         edge_label = "-" + ut1
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["urls"] += edge_label
    #                                         self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] += [
    #                                             (tweet1_qt.get_id(), tweet2.get_id())]
    #                                     else:
    #                                         self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2, weight=1, urls=ut1,
    #                                                                              tweets=[
    #                                                                                  (tweet1_qt.get_id(),
    #                                                                                   tweet2.get_id())])
    #
    #             if tweet1.get_id() != tweet2.get_id():
    #                 if (user1, user2) in self.user_level_cooccurrence_url_network.edges:
    #                     if (tweet1.get_id(), tweet2.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user2][
    #                         "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
    #                             self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"]:
    #                         for ut1 in tweet1_urls:
    #                             for ut2 in tweet2_urls:
    #                                 if ut1 == ut2:
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                 else:
    #                     for ut1 in tweet1_urls:
    #                         for ut2 in tweet2_urls:
    #                             if ut1 == ut2:
    #                                 if (user1, user2) in self.user_level_cooccurrence_url_network.edges:
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
    #                                     edge_label = "-" + ut1
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["urls"] += edge_label
    #                                     self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
    #                                         (tweet1.get_id(), tweet2.get_id())]
    #                                 else:
    #                                     self.user_level_cooccurrence_url_network.add_edge(user1, user2, weight=1, urls=ut1,
    #                                                                          tweets=[
    #                                                                              (tweet1.get_id(), tweet2.get_id())])
    #             j += 1
    #
    #     for edge in self.user_level_cooccurrence_url_network.edges:
    #         del self.user_level_cooccurrence_url_network.edges[edge]["tweets"]
    #
    # # bipartite version of user-level hashtag/mention/url networks
    # def user_hashtag_bipartite_network_building(self):
    #     self.network_repository.append("user_hashtag_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_twitter().get_screen_name()
    #         hashtag_list = tweet.get_hashtags()
    #
    #         for hashtag in hashtag_list:
    #             if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
    #                 self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                 self.user_hashtag_bipartite_network.edges[source, hashtag]["shared_content"] += tweet.get_text()
    #             else:
    #                 self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                    shared_content=tweet.get_text())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_twitter().get_screen_name()
    #             hashtag_list = tweet.get_hashtags()
    #             for hashtag in hashtag_list:
    #
    #                 if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
    #                     self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                     self.user_hashtag_bipartite_network.edges[source, hashtag][
    #                         "shared_content"] += tweet.get_retweeted().get_text()
    #                 else:
    #                     self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                        shared_content=tweet.get_retweeted().get_text())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 hashtag_list = tweet.get_retweeted().get_quote().get_hashtags()
    #                 for hashtag in hashtag_list:
    #
    #                     if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
    #                         self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                         self.user_hashtag_bipartite_network.edges[source, hashtag][
    #                             "shared_content"] += tweet.get_retweeted().get_quote().get_text()
    #                     else:
    #                         self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                            shared_content=tweet.get_retweeted().get_quote().get_text())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_twitter().get_screen_name()
    #             hashtag_list = tweet.get_quote().get_hashtags()
    #             for hashtag in hashtag_list:
    #
    #                 if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
    #                     self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
    #                     self.user_hashtag_bipartite_network.edges[source, hashtag][
    #                         "shared_content"] += tweet.get_quote().get_text()
    #                 else:
    #                     self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
    #                                                        shared_content=tweet.get_quote().get_text())
    #
    # def user_mention_bipartite_network_building(self):
    #     self.network_repository.append("user_mention_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_twitter().get_screen_name()
    #         mention_list = tweet.get_mentions()
    #
    #         for mention in mention_list:
    #             if self.user_mention_bipartite_network.has_edge(source, mention):
    #                 self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                 self.user_mention_bipartite_network.edges[source, mention]["shared_content"] += tweet.get_text()
    #             else:
    #                 self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1, shared_content=tweet.get_text())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_twitter().get_screen_name()
    #             mention_list = tweet.get_mentions()
    #             for mention in mention_list:
    #
    #                 if self.user_mention_bipartite_network.has_edge(source, mention):
    #                     self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                     self.user_mention_bipartite_network.edges[source, mention]["shared_content"] += tweet.get_retweeted().get_text()
    #                 else:
    #                     self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                         shared_content=tweet.get_retweeted().get_text())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 mention_list = tweet.get_retweeted().get_quote().get_mentions()
    #                 for mention in mention_list:
    #
    #                     if self.user_mention_bipartite_network.has_edge(source, mention):
    #                         self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                         self.user_mention_bipartite_network.edges[source, mention][
    #                             "shared_content"] += tweet.get_retweeted().get_quote().get_text()
    #                     else:
    #                         self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                            shared_content=tweet.get_retweeted().get_quote().get_text())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_twitter().get_screen_name()
    #             mention_list = tweet.get_quote().get_mentions()
    #             for mention in mention_list:
    #
    #                 if self.user_mention_bipartite_network.has_edge(source, mention):
    #                     self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
    #                     self.user_mention_bipartite_network.edges[source, mention][
    #                         "shared_content"] += tweet.get_quote().get_text()
    #                 else:
    #                     self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
    #                                                        shared_content=tweet.get_quote().get_text())
    #
    # def user_url_bipartite_network_building(self):
    #     self.network_repository.append("user_url_bipartite_network")
    #     for tweet_id, tweet in self.tweets.items():
    #         source = tweet.get_twitter().get_screen_name()
    #         url_list = tweet.get_tweet_urls(return_format="expanded_url")
    #
    #         for url in url_list:
    #             if self.user_url_bipartite_network.has_edge(source, url):
    #                 self.user_url_bipartite_network.edges[source, url]["weight"] += 1
    #                 self.user_url_bipartite_network.edges[source, url]["shared_content"] += tweet.get_text()
    #             else:
    #                 self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                shared_content=tweet.get_text())
    #
    #         if tweet.is_retweeted():
    #             source = tweet.get_retweeted().get_twitter().get_screen_name()
    #             url_list = tweet.get_tweet_urls(return_format="expanded_url")
    #             for url in url_list:
    #
    #                 if self.user_url_bipartite_network.has_edge(source, url):
    #                     self.user_url_bipartite_network.edges[source, url]["weight"] += 1
    #                     self.user_url_bipartite_network.edges[source, url]["shared_content"] += tweet.get_retweeted().get_text()
    #                 else:
    #                     self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                    shared_content=tweet.get_retweeted().get_text())
    #             if tweet.get_retweeted().is_quote_available():
    #                 source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
    #                 url_list = tweet.get_retweeted().get_quote().get_tweet_urls(return_format="expanded_url")
    #                 for url in url_list:
    #
    #                     if self.user_url_bipartite_network.has_edge(source, url):
    #                         self.user_url_bipartite_network.edges[source, url]["weight"] += 1
    #                         self.user_url_bipartite_network.edges[source, url][
    #                             "shared_content"] += tweet.get_retweeted().get_quote().get_text()
    #                     else:
    #                         self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                        shared_content=tweet.get_retweeted().get_quote().get_text())
    #         elif tweet.is_quote_available():
    #             source = tweet.get_quote().get_twitter().get_screen_name()
    #             url_list = tweet.get_quote().get_tweet_urls(return_format="expanded_url")
    #             for url in url_list:
    #
    #                 if self.user_url_bipartite_network.has_edge(source, url):
    #                     self.user_url_bipartite_network.edges[source, url]["weight"] += 1
    #                     self.user_url_bipartite_network.edges[source, url][
    #                         "shared_content"] += tweet.get_quote().get_text()
    #                 else:
    #                     self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
    #                                                    shared_content=tweet.get_quote().get_text())

    def network_building(self, requested_network="tweet_level_retweet_network"):
        if requested_network == "tweet_level_retweet_network":
            return self.tweet_level_retweet_network_building()
        elif requested_network == "tweet_level_quote_network":
            return self.tweet_level_quote_network_building()
        elif requested_network == "tweet_level_reply_network":
            return self.tweet_level_reply_network_building()
        elif requested_network == "tweet_level_quote_reply_network":
            return self.tweet_level_quote_reply_network_building()
        elif requested_network == "tweet_level_retweet_reply_network":
            return self.tweet_level_retweet_reply_network_building()
        elif requested_network == "tweet_level_retweet_quote_network":
            return self.tweet_level_retweet_quote_network_building()
        elif requested_network == "tweet_level_retweet_quote_reply_network":
            return self.tweet_level_retweet_quote_reply_network_building()
        elif requested_network == "tweet_level_cooccurrence_hashtag_network":
            return self.tweet_level_cooccurrence_hashtag_network_building()
        elif requested_network == "tweet_level_cooccurrence_mention_network":
            return self.tweet_level_cooccurrence_mention_network_building()
        elif requested_network == "tweet_level_cooccurrence_url_network":
            return self.tweet_level_cooccurrence_url_network_building()
        elif requested_network == "tweet_hashtag_bipartite_network":
            return self.tweet_hashtag_bipartite_network_building()
        elif requested_network == "tweet_mention_bipartite_network":
            return self.tweet_mention_bipartite_network_building()
        elif requested_network == "tweet_url_bipartite_network":
            return self.tweet_url_bipartite_network_building()
        elif requested_network == "user_level_retweet_network":
            return self.user_level_retweet_network_building()
        elif requested_network == "user_level_quote_network":
            return self.user_level_quote_network_building()
        elif requested_network == "user_level_reply_network":
            return self.user_level_reply_network_building()
        elif requested_network == "user_level_quote_reply_network":
            return self.user_level_quote_reply_network_building()
        elif requested_network == "user_level_retweet_reply_network":
            return self.user_level_retweet_reply_network_building()
        elif requested_network == "user_level_retweet_quote_network":
            return self.user_level_retweet_quote_network_building()
        elif requested_network == "user_level_retweet_quote_reply_network":
            return self.user_level_retweet_quote_reply_network_building()
        elif requested_network == "user_level_cooccurrence_hashtag_network":
            return self.user_level_cooccurrence_hashtag_network_building()
        elif requested_network == "user_level_cooccurrence_mention_network":
            return self.user_level_cooccurrence_mention_network_building()
        elif requested_network == "user_level_cooccurrence_url_network":
            return self.user_level_cooccurrence_url_network_building()
        elif requested_network == "user_hashtag_bipartite_network":
            return self.user_hashtag_bipartite_network_building()
        elif requested_network == "user_mention_bipartite_network":
            return self.user_mention_bipartite_network_building()
        elif requested_network == "user_url_bipartite_network":
            return self.user_url_bipartite_network_building()

    def get_network(self, requested_network="tweet_level_retweet_network"):
        if requested_network in self.network_repository:
            if requested_network == "tweet_level_retweet_network":
                return self.tweet_level_retweet_network
            elif requested_network == "tweet_level_quote_network":
                return self.tweet_level_quote_network
            elif requested_network == "tweet_level_reply_network":
                return self.tweet_level_reply_network
            elif requested_network == "tweet_level_quote_reply_network":
                return self.tweet_level_quote_reply_network
            elif requested_network == "tweet_level_retweet_reply_network":
                return self.tweet_level_retweet_reply_network
            elif requested_network == "tweet_level_retweet_quote_network":
                return self.tweet_level_retweet_quote_network
            elif requested_network == "tweet_level_retweet_quote_reply_network":
                return self.tweet_level_retweet_quote_reply_network
            elif requested_network == "tweet_level_cooccurrence_hashtag_network":
                return self.tweet_level_cooccurrence_hashtag_network
            elif requested_network == "tweet_level_cooccurrence_mention_network":
                return self.tweet_level_cooccurrence_mention_network
            elif requested_network == "tweet_level_cooccurrence_url_network":
                return self.tweet_level_cooccurrence_url_network

            elif requested_network == "tweet_hashtag_bipartite_network":
                return self.tweet_hashtag_bipartite_network
            elif requested_network == "tweet_mention_bipartite_network":
                return self.tweet_mention_bipartite_network
            elif requested_network == "tweet_url_bipartite_network":
                return self.user_url_bipartite_network



            elif requested_network == "user_level_retweet_network":
                return self.user_level_retweet_network
            elif requested_network == "user_level_quote_network":
                return self.user_level_quote_network
            elif requested_network == "user_level_reply_network":
                return self.user_level_reply_network
            elif requested_network == "user_level_quote_reply_network":
                return self.user_level_quote_reply_network
            elif requested_network == "user_level_retweet_reply_network":
                return self.user_level_retweet_reply_network
            elif requested_network == "user_level_retweet_quote_network":
                return self.user_level_quote_reply_network
            elif requested_network == "user_level_retweet_quote_reply_network":
                return self.user_level_retweet_quote_reply_network
            elif requested_network == "user_level_cooccurrence_hashtag_network":
                return self.user_level_cooccurrence_hashtag_network
            elif requested_network == "user_level_cooccurrence_mention_network":
                return self.user_level_cooccurrence_mention_network
            elif requested_network == "user_level_cooccurrence_url_network":
                return self.user_level_cooccurrence_url_network

            elif requested_network == "user_hashtag_bipartite_network":
                return self.user_hashtag_bipartite_network
            elif requested_network == "user_mention_bipartite_network":
                return self.user_mention_bipartite_network
            elif requested_network == "user_url_bipartite_network":
                return self.user_url_bipartite_network

    def download_network(self, requested_network="tweet_level_retweet_network", download_format="GEXF", path="", encoding='utf-8'):     #### Tell in the docstring that the path has to be completed and should include the file format!

        assert (download_format in ["GEXF", "GML"]), "The available output formats are GEXF and GML"

        if requested_network in self.network_repository:
            if download_format == "GEXF":
                nx.write_gexf(self.get_network(requested_network=requested_network), path=path, encoding=encoding, version='1.2draft')
            elif download_format == "GML":
                nx.write_gml(self.get_network(requested_network=requested_network), path=path)
        else:
            print("The network you have requested has not been created yet.")

    def components_number(self, requested_network="tweet_level_retweet_network"):
        """
        This function calculates the number of connected components in the desired network.
        :return: an integer that shows the number of connected components.
        """
        requested_network = level_of_resolution + "_level_" + network_type
        if requested_network in self.network_repository:
            return nx.number_connected_components(self.get_network(requested_network=requested_network).to_undirected())
        else:
            print("The network type you indicated has not been created yet.")

    def centrality_measures(self, metric="degree", requested_network="tweet_level_retweet_network"):
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

        if requested_network in self.network_repository:
            network = self.get_network(requested_network=requested_network)
            if metric == "degree":
                # network = self.get_network(network_type=network_type)
                degree_centrality = nx.centrality.degree_centrality(network)
                for node_id in degree_centrality:
                    network.nodes[node_id]["degree_centrality"] = degree_centrality[node_id]
                in_degree_centrality = nx.centrality.in_degree_centrality(network)
                for node_id in in_degree_centrality:
                    network.nodes[node_id]["in_degree_centrality"] = in_degree_centrality[node_id]
                out_degree_centrality = nx.centrality.out_degree_centrality(network)
                for node_id in out_degree_centrality:
                    network.nodes[node_id]["out_degree_centrality"] = out_degree_centrality[node_id]
            elif metric == "closeness":
                closeness_centrality = nx.centrality.closeness_centrality(network)
                for node_id in closeness_centrality:
                    network.nodes[node_id]["closeness_centrality"] = closeness_centrality[node_id]
            elif metric == "betweenness":
                betweenness_centrality = nx.centrality.betweenness_centrality(network)
                for node_id in betweenness_centrality:
                    network.nodes[node_id]["betweenness_centrality"] = betweenness_centrality[node_id]
            elif metric == "eigenvector":
                eigenvector_centrality = nx.centrality.eigenvector_centrality_numpy(network)
                for node_id in eigenvector_centrality:
                    network.nodes[node_id]["eigenvector_centrality"] = eigenvector_centrality[node_id]
            elif metric == "katz":
                katz_centrality = nx.centrality.katz_centrality_numpy(network)
                for node_id in katz_centrality:
                    network.nodes[node_id]["katz_centrality"] = katz_centrality[node_id]
            elif metric == "pagerank":
                pagerank_centrality = nx.pagerank_numpy(network)
                for node_id in pagerank_centrality:
                    network.nodes[node_id]["pagerank_centrality"] = pagerank_centrality[node_id]
        else:
            print("The network type you indicated has not been created yet.")

    def community_detection(self, requested_network="tweet_level_retweet_network", return_type="network"):
        """
        This function identified communities in the network using Louvain algorithm. PLease note that, it uses the undirected
        version of the network.
        :param: return_type: The output of this function can be a network with community number as a property of each
        node, a dictionary with key-value pairs corresponding to node_id and community_id, and a dictionary with
        key-value pairs corresponding to community_id and all the nodes belonging to that community.
        :return: Depending on the value of return_type parameter the output of this function varies.
        """

        assert (return_type in ["network", "node-community", "community-nodes"]), "The type of the output could be either network, node-community, or community-nodes"

        if requested_network in self.network_repository:
            network = self.get_network(requested_network=requested_network)
            partition = community.best_partition(network.to_undirected())
            if return_type == "network":
                for node_id in partition:
                    network.nodes[node_id]["community"] = partition[node_id]
            elif return_type == "node-community":
                return partition
            elif return_type == "community-nodes":
                communities = {}
                for k, v in partition.items():
                    communities[v] = communities.get(v, []) + [k]
                return communities
        else:
            print("The network type you indicated has not been created yet.")

    # def word_count_layer(self):
    #     pass
    #
    # def character_count_layer(self):
    #     pass
    #
    # def sentence_count_layer(self):
    #     pass
    #
    # def word_complexity_layer(self):
    #     pass
    #
    # def sentence_complexity_layer(self):
    #     pass
    #
    # def syllables_complexity_layer(self):
    #     pass
    #
    # def sentiment_layer(self):
    #     pass
    #
    # def readability_layer(self):
    #     pass
# class RetweetNetwork(Network):  # node should change to nodes in order to call a particular node
#     def building_network(self):
#         """
#         This function builds the retweet network.
#         :return: This function does not return the network. It updates the class properties. To get the network, use
#         get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf is True:
#                 self.network.add_edge(tweet.get_retweeted().get_id(), tweet.get_id(), kind="retweet")
#             elif trf is False:
#                 self.network.add_node(tweet.get_id())
#
#     # def word_count_layer(self):
#     #     """
#     #     This function add the number of words in each tweet as a property to every node.
#     #     :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
#     #      nodes of the caller network object. To get the network, use get_network() function.
#     #     """
#     #     for tweet_id, tweet in self.tweets.items():
#     #         trf = tweet.is_retweeted()
#     #         if trf == True:
#     #             self.network.node[tweet.get_retweeted().get_id()]["word_count"] = tweet.get_retweeted().text_length()
#     #             self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#     #         elif trf == False:
#     #             self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#
#     def character_count_layer(self):
#         """
#         This function add the number of characters in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "character_count"] = tweet.get_retweeted().text_length(length_unit="character")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#
#     def sentence_count_layer(self):
#         """
#         This function add the number of sentences in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.nodes[tweet.get_retweeted().get_id()][
#                     "character_count"] = tweet.get_retweeted().text_length(length_unit="sentence")
#                 self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#             elif trf == False:
#                 self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#
#     def word_complexity_layer(self):
#         """
#         This function add the word complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "word_complexity"] = tweet.get_retweeted().text_complexity()
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#
#     def sentence_complexity_layer(self):
#         """
#         This function add the sentence complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "sentence_complexity"] = tweet.get_retweeted().text_complexity(complexity_unit="sentence")
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#
#     def syllables_complexity_layer(self):
#         """
#         This function add the syllables complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "syllables_complexity"] = tweet.get_retweeted().text_complexity(complexity_unit="syllables")
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#
#     def sentiment_layer(self, sentiment_engine="vader"):
#         """
#         This function add the sentiment of each tweet as a property to every node.
#         :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
#         "vad".
#         :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
#                                      "vad"]), "The sentiment_engine has to be" \
#                                               "textblob, vader, nrc," \
#                                               "hate_speech or vad"
#
#         subscores_labels = {"textblob": ["subjectivity", "polarity"],
#                             "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
#                             "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
#                                     "sadness_score", "surprise_score", "trust_score"],
#                             "hate_speech": ["hate_speech", "offensive_language", "neither"],
#                             "vad": ["valence_score", "arousal_score", "dominance_score"]}
#         for tweet_id, tweet in self.tweets.items():
#             for i in subscores_labels[sentiment_engine]:
#                 trf = tweet.is_retweeted()
#                 if trf == True:
#                     self.network.node[tweet.get_retweeted().get_id()][i] = \
#                         tweet.get_retweeted().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#                 elif trf == False:
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#
#     def readability_layer(self, readability_metric="flesch_kincaid_grade"):
#         """
#         This function add the readability of each tweet as a property to every node.
#         :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
#         "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
#         :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
#                            "coleman_liau_index", "linsear_write_formula",
#                            "dale_chall_readability_score", ]), "The metric " \
#                                                                "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
#                                                                "automated_readability_index, coleman_liau_index, linsear_write_formula," \
#                                                                "or dale_chall_readability_score."
#
#         # for tweet_id, tweet in self.tweets.items():
#         for tweet_id in tqdm(self.tweets):
#             tweet = self.tweets[tweet_id]
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.get_retweeted().text_preprocessing()}\")')
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#
#
# class QuoteNetwork(Network):
#     def building_network(self):
#         """
#         This function builds the quote network.
#         :return: This function does not return the network. It updates the class properties. To get the network, use
#         get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.add_edge(tweet.get_quote().get_id(), tweet.get_id(), kind="quote")
#             elif tqf == False:
#                 self.network.add_node(tweet.get_id())
#
#     def word_count_layer(self):
#         """
#         This function add the number of words in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["word_count"] = tweet.get_quote().text_length()
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#
#     def character_count_layer(self):
#         """
#         This function add the number of characters in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
#                     length_unit="character")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#
#     def sentence_count_layer(self):
#         """
#         This function add the number of sentences in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
#                     length_unit="sentence")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#
#     def word_complexity_layer(self):
#         """
#         This function add the word complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["word_complexity"] = tweet.get_quote().text_complexity()
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#
#     def sentence_complexity_layer(self):
#         """
#         This function add the sentence complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()][
#                     "sentence_complexity"] = tweet.get_quote().text_complexity(complexity_unit="sentence")
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#
#     def syllables_complexity_layer(self):
#         """
#         This function add the syllables complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()][
#                     "syllables_complexity"] = tweet.get_quote().text_complexity(complexity_unit="syllables")
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#
#     def sentiment_layer(self, sentiment_engine="vader"):
#         """
#         This function add the sentiment of each tweet as a property to every node.
#         :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
#         "vad".
#         :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
#                                      "vad"]), "The sentiment_engine has to be" \
#                                               "textblob, vader, nrc," \
#                                               "hate_speech or vad"
#
#         subscores_labels = {"textblob": ["subjectivity", "polarity"],
#                             "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
#                             "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
#                                     "sadness_score", "surprise_score", "trust_score"],
#                             "hate_speech": ["hate_speech", "offensive_language", "neither"],
#                             "vad": ["valence_score", "arousal_score", "dominance_score"]}
#         for tweet_id, tweet in self.tweets.items():
#             for i in subscores_labels[sentiment_engine]:
#                 tqf = tweet.is_quoted()
#                 if tqf == True:
#                     self.network.node[tweet.get_quote().get_id()][i] = \
#                         tweet.get_quote().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#                 elif tqf == False:
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#
#     def readability_layer(self, readability_metric="flesch_kincaid_grade"):
#         """
#         This function add the readability of each tweet as a property to every node.
#         :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
#         "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
#         :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
#                            "coleman_liau_index", "linsear_write_formula",
#                            "dale_chall_readability_score", ]), "The metric " \
#                                                                "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
#                                                                "automated_readability_index, coleman_liau_index, linsear_write_formula," \
#                                                                "or dale_chall_readability_score."
#
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.get_quote().text_preprocessing()}\")')
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')


# class TimeDependentLocationDependentTweetNetworkFeatures:
#     def test(self):
#         print("test")
#
# class TimeDependentLocationDependentUserNetworkFeatures:
#     def test(self):
#         print("test")
#
# class TimeDependentLocationIndependentTweetNetworkFeatures:
#     def test(self):
#         print("test")
#
# class TimeDependentLocationIndependentUserNetworkFeatures:
#     def test(self):
#         print("test")
#
# class TimeIndependentLocationDependentTweetNetworkFeatures:
#     def test(self):
#         print("test")
#
# class TimeIndependentLocationDependentUserNetworkFeatures:
#     def test(self):
#         print("test")

class TimeIndependentLocationIndependentTweetNetworkFeatures (Network):
    # def __init__(self, tweets, retweet_network=True, quote_network=True, reply_network=True):
    #     """
    #     This is a constructor for TimeIndependentLocationIndependentTweetNetworkFeatures class
    #     :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
    #     :param retweet_network: a boolean parameter that indicates whether the retweet network is created or not.
    #     :param quote_network: a boolean parameter that indicates whether the quote network is created or not.
    #     :param reply_network: a boolean parameter that indicates whether the reply network is created or not.
    #     """
    #     self.tweets = tweets
    #     # network = Network(self.tweets)
    #     if retweet_network is True:
    #         self.rt_network = Network.building_network(self.tweets, network_type="retweet")
    #     if quote_network is True:
    #         self.qt_network = Network.building_network(self.tweets, network_type="quote")
    #     if reply_network is True:
    #         self.rp_network = Network.building_network(self.tweets, network_type="reply")




    # def word_count_layer(self):
    #     pass
    #
    # def character_count_layer(self):
    #     pass
    #
    # def sentence_count_layer(self):
    #     pass
    #
    # def word_complexity_layer(self):
    #     pass
    #
    # def sentence_complexity_layer(self):
    #     pass
    #
    # def syllables_complexity_layer(self):
    #     pass
    #
    # def sentiment_layer(self):
    #     pass
    #
    # def readability_layer(self):
    #     pass


    def tweet_length_layer(self, length_unit="word", network_type=None): #In this function, I do not include quote if it is part of the tweet
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        if network_type in self.network_repository:
            unit = length_unit+"_count"
            network = self.get_network(requested_network=network_type)
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    tweet_length = self.tweets_quotes_retweets[tweet_id]["object"].text_length(length_unit=length_unit)
                    network.nodes[tweet_id][unit] = tweet_length
                else:
                    #Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def tweet_complexity_layer(self, complexity_unit="word", network_type=None):#In this function, I do not include quote if it is part of the tweet
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        if network_type in self.network_repository:
            unit = complexity_unit+"_complexity"
            network = self.get_network(requested_network=network_type)
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    tweet_complexity = self.tweets_quotes_retweets[tweet_id]["object"].text_complexity(complexity_unit=complexity_unit)
                    network.nodes[tweet_id][unit] = tweet_complexity
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def tweet_sentiment_layer(self, sentiment_engine="vader", network_type=None):#In this function, I do not include quote if it is part of the tweet
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """
        if network_type in self.network_repository:
            unit = "sentiment"
            network = self.get_network(requested_network=network_type)
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    tweet_text = self.tweets_quotes_retweets[tweet_id]["object"].get_text()
                    tweet_sentiment = self.tweets_quotes_retweets[tweet_id]["object"].sentiment_analysis(sentiment_engine=sentiment_engine, input_text=tweet_text)
                    network.nodes[tweet_id][unit] = tweet_sentiment
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def tweet_readability_layer(self, readability_metric="flesch_kincaid_grade", network_type=None):#In this function, I do not include quote if it is part of the tweet
        """
        This function add the number of words in each tweet as a property to every node.
        :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
         nodes of the caller network object. To get the network, use get_network() function.
        """

        if network_type in self.network_repository:
            unit = "readability"
            network = self.get_network(requested_network=network_type)
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    tweet_readability_score = self.tweets_quotes_retweets[tweet_id]["object"].readability(readability_metric=readability_metric)
                    network.nodes[tweet_id][unit] = tweet_readability_score
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")


class TimeIndependentLocationIndependentUserNetworkFeatures (Network):

    def user_followers_count_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "followers_count"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id]["object"].get_twitter().get_followers_count()
                else:
                 # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def user_friends_count_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "friends_count"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id][
                        "object"].get_twitter().get_friends_count()
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def user_role_count_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "user_role"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id][
                        "object"].get_twitter().get_user_role()
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def users_with_verification_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "verified"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id][
                        "object"].get_twitter().get_user_verification_status()
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def users_status_count_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "status_count"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id][
                        "object"].get_twitter().get_statusses_count()
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")

    def users_total_likes_count_layer(self, network_type=None):
        if network_type in self.network_repository:
            unit = "total_likes_count"
            network = self.get_network(requested_network=network_type)

            for tweet_id in network.nodes:
                if tweet_id in self.tweets_quotes_retweets:
                    network.nodes[tweet_id][unit] = self.tweets_quotes_retweets[tweet_id][
                        "object"].get_twitter().get_user_total_likes_count()
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
        else:
            print(f"The {network_type} has not been created yet.")


class TimeDependentLocationIndependentTweetNetworkFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
        """
        self.tweets = tweets
        self.temporal_networks = {}
        self.temporal_network_objects = {}
        self.temporal_tweets = {}
        self.tweets_retweets_retweetedquotes_quotes_timeframes = {}

    def network_building_in_each_timeframe(self, tweets_in_periods=None, network_type="tweet_level_retweet_quote_reply_network", resolution="year", frequency=1):
        if tweets_in_periods is None:
            temporal_features_object = TemporalFeatures(tweets=self.tweets)
            self.temporal_tweets = temporal_features_object.tweets_in_periods(resolution=resolution, frequency=frequency)
        else:
            self.temporal_tweets = tweets_in_periods

        for timeframe, tweets in self.temporal_tweets.items():
            self.tweets_retweets_retweetedquotes_quotes_timeframes[timeframe] = TwifexUtility.tweets_retweets_retweetedquotes_quotes(TwifexUtility.collective_tweets_to_dictionary(tweets))
            network_obj = Network(tweets=TwifexUtility.collective_tweets_to_dictionary(tweets))
            network_obj.network_building(requested_network=network_type)
            network = network_obj.get_network(requested_network=network_type)
            self.temporal_network_objects[timeframe] = network_obj
            self.temporal_networks[timeframe] = network

    def tweet_complexity_layer(self, complexity_unit="word"):
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

        unit = complexity_unit + "_complexity"
        networks_in_timeframes = {}
        for timeframe, network in self.temporal_networks.items():
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_retweets_retweetedquotes_quotes_timeframes[timeframe]:
                    tweet_complexity = self.tweets_retweets_retweetedquotes_quotes_timeframes[timeframe][tweet_id]["object"].text_complexity(
                        complexity_unit=complexity_unit)
                    network.nodes[tweet_id][unit] = tweet_complexity
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
            networks_in_timeframes[timeframe] = network

        return networks_in_timeframes

    def tweet_length_layer(self, length_unit="word"):

        unit = length_unit + "_count"
        networks_in_timeframes = {}
        for timeframe, network in self.temporal_networks.items():
            for tweet_id in network.nodes:
                if tweet_id in self.tweets_retweets_retweetedquotes_quotes_timeframes[timeframe]:
                    tweet_length = self.tweets_retweets_retweetedquotes_quotes_timeframes[timeframe][tweet_id]["object"].text_length(length_unit=length_unit)
                    network.nodes[tweet_id][unit] = tweet_length
                else:
                    # Instead of None I put -1 here, since if we set to None then networkx cannot save it as a gexf file and even if we save it as "None" (the string version) then gephi cannot properly parse it
                    network.nodes[tweet_id][unit] = -1
            networks_in_timeframes[timeframe] = network

        return networks_in_timeframes

# class TimeDependentLocationIndependentUserNetworkFeatures(TemporalFeatures, Network):
#
#
# class TimeIndependentLocationDependentTweetNetworkFeatures(PlaceFeatures, Network):
#
#
# class TimeIndependentLocationDependentUserNetworkFeatures(PlaceFeatures, Network):
#
#
# class TimeDependentLocationDependentTweetNetworkFeatures(PlaceFeatures, Network):
#
#
# class TimeDependentLocationDependentUserNetworkFeatures(PlaceFeatures, Network):

class UserTopologyFeatures:
    def __init__(self, tweets):
        """
        This is a constructor for tweetNetwork class
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
        """
        self.tweets = tweets

    def user_retweet_network(self):
        """
        This function creates the user_retweet_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has retweeted user A.
        :return: a userRetweetNetwork object.
        """
        return UserRetweetNetwork(self.tweets)

    def user_quote_network(self):
        """
        This function creates the user_quote_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has quoted user A.
        :return: a userQuoteNetwork object.
        """
        return UserQuoteNetwork(self.tweets)

    def user_reply_network(self):  # not yet deployed
        """
        This function creates the user_reply_network from the dataset. In this directed network, nodes
        represent users. Also a link from user A to B shows user B has replied to user A.
        :return: a userReplyNetwork object.
        """
        return UserReplyNetwork(self.tweets)
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


# class Network:
#     def __init__(self, tweets):
#         """
#         This is a constructor of a network class.
#         :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
#         """
#         # self.network = nx.DiGraph()
#         self.tweets = tweets
#
#     @staticmethod
#     def building_network(tweets, network_type='retweet'):
#         # network = nx.DiGraph()
#         # for tweet_id, tweet in tweets.items():
#         #     if network_type == "retweet":
#         #         t = tweet.get_id()
#         #         condition = tweet.is_retweeted()
#         #         if condition:
#         #             s = tweet.get_retweeted().get_id()
#         #     elif network_type == "quote":
#         #         t = tweet.get_id()
#         #         condition = tweet.is_quoted()
#         #         if condition:
#         #             s = tweet.get_quote().get_id()
#         #     elif network_type == "reply":
#         #         t = tweet.get_id()
#         #         condition = tweet.is_this_a_reply()
#         #         if condition:
#         #             s = tweet.get_reply_to_id()
#         #
#         #     if condition is True:
#         #         network.add_edge(s, t, kind=network_type)
#         #     elif condition is False:
#         #         network.add_node(tweet.get_id())
#         #
#         # return network
#
#         network = nx.DiGraph()
#         for tweet_id, tweet in tweets.items():
#             if network_type == "retweet":
#                 retweet_condition = tweet.is_retweeted()
#                 if retweet_condition is True:
#                     network.add_edge(tweet.get_retweeted().get_id(), tweet.get_id(), kind="retweet")
#                 elif retweet_condition is False:
#                     network.add_node(tweet.get_id())
#             elif network_type == "quote":
#                 quote_condition = tweet.is_quoted()
#                 if quote_condition is True:
#                     network.add_edge(tweet.get_quote().get_id(), tweet.get_id(), kind="quote")
#                 elif quote_condition is False:
#                     network.add_node(tweet.get_id())
#             elif network_type == "reply":
#                 reply_condition = tweet.is_this_a_reply()
#                 if reply_condition is True:
#                     network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
#                 elif reply_condition is False:
#                     network.add_node(tweet.get_id())
#         return network
#
#
#
#     def components_number(self):
#         """
#         This function calculates the number of connected components in the desired network.
#         :return: an integer that shows the number of connected components.
#         """
#         return nx.number_connected_components(self.network.to_undirected())
#
#     def centrality_measures(self, metric="degree"):
#         """
#         This function measures network centrality based on the chosen metric.
#         :param metric: metric can be "degree", "closeness", "betweenness", "eigenvector", "katz", and "pagerank". Please
#         note that for degree centrality it measures both in-degree and out-degree centrality.
#         :return: This function does not return anything, instead it add the relevant attribute to the caller network object.
#         To get the network, use get_network() function.
#         """
#
#         assert (metric in ["degree", "closeness", "betweenness", "eigenvector", "katz",
#                            "pagerank"]), "The metric has to be" \
#                                          " degree, closeness, betweenness, " \
#                                          "eigenvector, katz, or pagerank."
#         if metric == "degree":
#             degree_centrality = nx.centrality.degree_centrality(self.network)
#             for node_id in degree_centrality:
#                 self.network.node[node_id]["degree_centrality"] = degree_centrality[node_id]
#             in_degree_centrality = nx.centrality.in_degree_centrality(self.network)
#             for node_id in in_degree_centrality:
#                 self.network.node[node_id]["in_degree_centrality"] = in_degree_centrality[node_id]
#             out_degree_centrality = nx.centrality.out_degree_centrality(self.network)
#             for node_id in out_degree_centrality:
#                 self.network.node[node_id]["out_degree_centrality"] = out_degree_centrality[node_id]
#         elif metric == "closeness":
#             closeness_centrality = nx.centrality.closeness_centrality(self.network)
#             for node_id in closeness_centrality:
#                 self.network.node[node_id]["closeness_centrality"] = closeness_centrality[node_id]
#         elif metric == "betweenness":
#             betweenness_centrality = nx.centrality.betweenness_centrality(self.network)
#             for node_id in betweenness_centrality:
#                 self.network.node[node_id]["betweenness_centrality"] = betweenness_centrality[node_id]
#         elif metric == "eigenvector":
#             eigenvector_centrality = nx.centrality.eigenvector_centrality_numpy(self.network)
#             for node_id in eigenvector_centrality:
#                 self.network.node[node_id]["eigenvector_centrality"] = eigenvector_centrality[node_id]
#         elif metric == "katz":
#             katz_centrality = nx.centrality.katz_centrality_numpy(self.network)
#             for node_id in katz_centrality:
#                 self.network.node[node_id]["katz_centrality"] = katz_centrality[node_id]
#         elif metric == "pagerank":
#             pagerank_centrality = nx.pagerank_numpy(self.network)
#             for node_id in pagerank_centrality:
#                 self.network.node[node_id]["pagerank_centrality"] = pagerank_centrality[node_id]
#
#     def community_detection(self):
#         """
#         This function identified communities in the network using Louvain algorithm. PLease note that, it uses the undirected
#         version of the network.
#         :return: This function does not return anything, instead it add the relevant attribute to the caller network object.
#         To get the network, use get_network() function.
#         """
#         partition = community.best_partition(self.network.to_undirected())
#         for node_id in partition:
#             self.network.node[node_id]["community"] = partition[node_id]
#
#     # def word_count_layer(self):
#     #     pass
#     #
#     # def character_count_layer(self):
#     #     pass
#     #
#     # def sentence_count_layer(self):
#     #     pass
#     #
#     # def word_complexity_layer(self):
#     #     pass
#     #
#     # def sentence_complexity_layer(self):
#     #     pass
#     #
#     # def syllables_complexity_layer(self):
#     #     pass
#     #
#     # def sentiment_layer(self):
#     #     pass
#     #
#     # def readability_layer(self):
#     #     pass
#
#     def get_network(self):
#         return self.network
#
#
# class RetweetNetwork(Network):  # node should change to nodes in order to call a particular node
#     def building_network(self):
#         """
#         This function builds the retweet network.
#         :return: This function does not return the network. It updates the class properties. To get the network, use
#         get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf is True:
#                 self.network.add_edge(tweet.get_retweeted().get_id(), tweet.get_id(), kind="retweet")
#             elif trf is False:
#                 self.network.add_node(tweet.get_id())
#
#     def word_count_layer(self):
#         """
#         This function add the number of words in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()]["word_count"] = tweet.get_retweeted().text_length()
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#
#     def character_count_layer(self):
#         """
#         This function add the number of characters in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "character_count"] = tweet.get_retweeted().text_length(length_unit="character")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#
#     def sentence_count_layer(self):
#         """
#         This function add the number of sentences in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.nodes[tweet.get_retweeted().get_id()][
#                     "character_count"] = tweet.get_retweeted().text_length(length_unit="sentence")
#                 self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#             elif trf == False:
#                 self.network.nodes[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#
#     def word_complexity_layer(self):
#         """
#         This function add the word complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "word_complexity"] = tweet.get_retweeted().text_complexity()
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#
#     def sentence_complexity_layer(self):
#         """
#         This function add the sentence complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "sentence_complexity"] = tweet.get_retweeted().text_complexity(complexity_unit="sentence")
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#
#     def syllables_complexity_layer(self):
#         """
#         This function add the syllables complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()][
#                     "syllables_complexity"] = tweet.get_retweeted().text_complexity(complexity_unit="syllables")
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#
#     def sentiment_layer(self, sentiment_engine="vader"):
#         """
#         This function add the sentiment of each tweet as a property to every node.
#         :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
#         "vad".
#         :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
#                                      "vad"]), "The sentiment_engine has to be" \
#                                               "textblob, vader, nrc," \
#                                               "hate_speech or vad"
#
#         subscores_labels = {"textblob": ["subjectivity", "polarity"],
#                             "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
#                             "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
#                                     "sadness_score", "surprise_score", "trust_score"],
#                             "hate_speech": ["hate_speech", "offensive_language", "neither"],
#                             "vad": ["valence_score", "arousal_score", "dominance_score"]}
#         for tweet_id, tweet in self.tweets.items():
#             for i in subscores_labels[sentiment_engine]:
#                 trf = tweet.is_retweeted()
#                 if trf == True:
#                     self.network.node[tweet.get_retweeted().get_id()][i] = \
#                         tweet.get_retweeted().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#                 elif trf == False:
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#
#     def readability_layer(self, readability_metric="flesch_kincaid_grade"):
#         """
#         This function add the readability of each tweet as a property to every node.
#         :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
#         "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
#         :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
#                            "coleman_liau_index", "linsear_write_formula",
#                            "dale_chall_readability_score", ]), "The metric " \
#                                                                "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
#                                                                "automated_readability_index, coleman_liau_index, linsear_write_formula," \
#                                                                "or dale_chall_readability_score."
#
#         # for tweet_id, tweet in self.tweets.items():
#         for tweet_id in tqdm(self.tweets):
#             tweet = self.tweets[tweet_id]
#             trf = tweet.is_retweeted()
#             if trf == True:
#                 self.network.node[tweet.get_retweeted().get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.get_retweeted().text_preprocessing()}\")')
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#             elif trf == False:
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#
#
# class QuoteNetwork(Network):
#     def building_network(self):
#         """
#         This function builds the quote network.
#         :return: This function does not return the network. It updates the class properties. To get the network, use
#         get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.add_edge(tweet.get_quote().get_id(), tweet.get_id(), kind="quote")
#             elif tqf == False:
#                 self.network.add_node(tweet.get_id())
#
#     def word_count_layer(self):
#         """
#         This function add the number of words in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["word_count"] = tweet.get_quote().text_length()
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["word_count"] = tweet.text_length()
#
#     def character_count_layer(self):
#         """
#         This function add the number of characters in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet character count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
#                     length_unit="character")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="character")
#
#     def sentence_count_layer(self):
#         """
#         This function add the number of sentences in each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence count) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["character_count"] = tweet.get_quote().text_length(
#                     length_unit="sentence")
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["character_count"] = tweet.text_length(length_unit="sentence")
#
#     def word_complexity_layer(self):
#         """
#         This function add the word complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet word complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["word_complexity"] = tweet.get_quote().text_complexity()
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["word_complexity"] = tweet.text_complexity()
#
#     def sentence_complexity_layer(self):
#         """
#         This function add the sentence complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet sentence complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()][
#                     "sentence_complexity"] = tweet.get_quote().text_complexity(complexity_unit="sentence")
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["sentence_complexity"] = tweet.text_complexity(complexity_unit="sentence")
#
#     def syllables_complexity_layer(self):
#         """
#         This function add the syllables complexity of each tweet as a property to every node.
#         :return: This function does not return anything, instead it add the relevant attribute (tweet syllables complexity) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()][
#                     "syllables_complexity"] = tweet.get_quote().text_complexity(complexity_unit="syllables")
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["syllables_complexity"] = tweet.text_complexity(complexity_unit="syllables")
#
#     def sentiment_layer(self, sentiment_engine="vader"):
#         """
#         This function add the sentiment of each tweet as a property to every node.
#         :param sentiment_engine: sentiment analysis engine which can be "textblob", "vader", "nrc", "hate_speech", or
#         "vad".
#         :return: This function does not return anything, instead it add the relevant attribute (sentiment score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
#                                      "vad"]), "The sentiment_engine has to be" \
#                                               "textblob, vader, nrc," \
#                                               "hate_speech or vad"
#
#         subscores_labels = {"textblob": ["subjectivity", "polarity"],
#                             "vader": ["positivity_score", "negativity_score", "neutrality_score", "composite_score"],
#                             "nrc": ["anger_score", "anticipation_score", "disgust_score", "fear_score", "joy_score",
#                                     "sadness_score", "surprise_score", "trust_score"],
#                             "hate_speech": ["hate_speech", "offensive_language", "neither"],
#                             "vad": ["valence_score", "arousal_score", "dominance_score"]}
#         for tweet_id, tweet in self.tweets.items():
#             for i in subscores_labels[sentiment_engine]:
#                 tqf = tweet.is_quoted()
#                 if tqf == True:
#                     self.network.node[tweet.get_quote().get_id()][i] = \
#                         tweet.get_quote().sentiment_analysis(sentiment_engine=sentiment_engine)[i]
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#                 elif tqf == False:
#                     self.network.node[tweet.get_id()][i] = tweet.sentiment_analysis(sentiment_engine=sentiment_engine)[
#                         i]
#
#     def readability_layer(self, readability_metric="flesch_kincaid_grade"):
#         """
#         This function add the readability of each tweet as a property to every node.
#         :param readability_metric: The readability metric which can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
#         "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score".
#         :return: This function does not return anything, instead it add the relevant attribute (readability score) to the
#          nodes of the caller network object. To get the network, use get_network() function.
#         """
#
#         assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
#                            "coleman_liau_index", "linsear_write_formula",
#                            "dale_chall_readability_score", ]), "The metric " \
#                                                                "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
#                                                                "automated_readability_index, coleman_liau_index, linsear_write_formula," \
#                                                                "or dale_chall_readability_score."
#
#         for tweet_id, tweet in self.tweets.items():
#             tqf = tweet.is_quoted()
#             if tqf == True:
#                 self.network.node[tweet.get_quote().get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.get_quote().text_preprocessing()}\")')
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')
#             elif tqf == False:
#                 self.network.node[tweet.get_id()]["readability"] = eval(
#                     f'textstat.{readability_metric}(\"{tweet.text_preprocessing()}\")')

#TRANSFERRED
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

# #TRANSFERRED
# class SingleTweet: #Update docstring and assertions
#     def __init__(self, param):
#         """
#         This is the constructor of SingleTweet.
#         :param tweet_path: an individual tweet path.
#         :param param: a dictionary of necessary objects and modules.
#         """
#         self.tweet = None
#         self.parameters = param
#         self.text = ""
#
# #entities
#     def tweet_loader(self, tweet_path):
#         self.tweet = json.load(open(tweet_path))
#         return self
#
#     def get_entities(self): #There is an assumption here and that is the "truncated" variable is always False
#         """
#         This function extracts the full tweet entities including hashtags, mentions, urls, photos, videos, gifs, and symbols
#          from a tweet object.
#         :return: a dictionary containing all the entities.
#         """
#         tweet_entities = None
#         if self.is_retweeted():
#             tweet_entities = self.tweet["retweeted_status"]["entities"]
#             if "extended_entities" in self.tweet["retweeted_status"].keys():
#                 tweet_entities["media"] = self.tweet["retweeted_status"]["extended_entities"]["media"]
#         elif not self.is_retweeted():
#             tweet_entities = self.tweet["entities"]
#             if "extended_entities" in self.tweet.keys():
#                 tweet_entities["media"] = self.tweet["extended_entities"]["media"]
#         return tweet_entities
#
#         # if not self.is_retweeted():
#         #     if self.tweet["truncated"]:
#         #         tweet_entities = self.tweet["extended_tweet"]["entities"]
#         #         if "extended_entities" in self.tweet["extended_tweet"].keys():
#         #             tweet_entities["media"] = self.tweet["extended_tweet"]["extended_entities"]["media"]
#         #     else:
#         #         tweet_entities = self.tweet["entities"]
#         #         if "extended_entities" in self.tweet.keys():
#         #             tweet_entities["media"] = self.tweet["extended_entities"]["media"]
#         # elif self.is_retweeted():
#         #     if self.tweet["retweeted_status"]["truncated"]:
#         #         tweet_entities = self.tweet["retweeted_status"]["extended_tweet"]["entities"]
#         #         if "extended_entities" in self.tweet["retweeted_status"]["extended_tweet"].keys():
#         #             tweet_entities["media"] = self.tweet["retweeted_status"]["extended_tweet"]["extended_entities"][
#         #                 "media"]
#         #     else:
#         #         tweet_entities = self.tweet["retweeted_status"]["entities"]
#         #         if "extended_entities" in self.tweet["retweeted_status"].keys():
#         #             tweet_entities["media"] = self.tweet["retweeted_status"]["extended_entities"]["media"]
#         # return tweet_entities
#
#     def get_tweet(self):
#         """
#         :return: the tweet as a json file
#         """
#         return self.tweet
#
#     def get_url(self):
#         """
#         this function builds the tweet url.
#         :return: a string of tweet url.
#         """
#         return "https://twitter.com/" + self.get_twitter().get_screen_name() + "/status/" + \
#                self.get_id(return_format="string")
#
#     def get_inner_quote_screen_name(self): #no docstring
#         return re.findall("status.*", self.tweet["quoted_status_permalink"]["expanded"])[0].replace("status/","")
#
#     def get_in_reply_to_screen_name(self):
#         return self.tweet["in_reply_to_screen_name"]
#
#     def get_twitter(self):
#         """
#         :return: the user object embedded in the tweet object.
#         """
#         return user(self.tweet["user"])
#
#     def get_creation_time(self, output="object"):
#         """
#         It shows the creation time and date of a tweet.
#         :param output: it can be either "object", "original_string", or "improved_string". By choosing the original_string
#         the created_at field of tweet object is returned. By choosing object, a datetime object of the tweet creation time
#         including year, month, day, hour, minute and second is returned. "improved_string" returns the string version of
#         the datetime object.
#         :return: a string or datetime object of the tweet creation time.
#         """
#
#         assert (output in ["object", "original_string",
#                            "improved_string"]), "the output has to be object or original_string, or" \
#                                                 "improved_string"
#
#         if output == "object":
#             return datetime.datetime.strptime(datetime.datetime.strftime(
#                 datetime.datetime.strptime(self.tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S"),
#                 "%Y %m %d %H %M %S")
#         elif output == "original_string":
#             return self.tweet["created_at"]
#         elif output == "improved_string":
#             return datetime.datetime.strftime(
#                 datetime.datetime.strptime(self.tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S")
#
#     def get_source(self, return_format='raw'):
#         """
#         :return: a string showing th utility used to post the Tweet.
#         """
#         if return_format == "raw":
#             return self.tweet["source"]
#         elif return_format == "processed":
#             # return re.findall(">.*<", f1[10]["source"])[0].replace("<", "").replace(">", "")
#             soup = BeautifulSoup(self.get_source(), "html.parser")
#             client = soup.text
#             return client
#
#     def get_likes_count(self):
#         """
#         :return: an integer which indicates approximately how many times this Tweet has been liked by Twitter users
#         """
#         return self.tweet["favorite_count"]
#
#     def get_retweet_count(self):
#         """
#         :return: an integer which indicates how many times this tweet has been retweeted.
#         """
#         return self.tweet["retweet_count"]
#
#     def get_language(self):
#         """
#         :return: a string showing the language of the tweet.
#         """
#         return self.tweet["lang"]
#
#     def get_place(self): #You should be more specific about this field, not returning bunch of fields
#         """
#         When present, indicates that the tweet is associated (but not necessarily originating from) a Place.
#         :return: a place object.
#         """
#         return self.tweet["place"]
#
#     def get_coordinates(self):#You should be more specific about this field, not returning bunch of fields
#         """
#         Represents the geographic location of this Tweet as reported by the user or client application.
#         :return: a coordinate object
#         """
#         return self.tweet["coordinates"]
#
#     def get_tweet_urls(self, return_format="url"):
#         """
#         :return: a list of urls in this tweet.
#         """
#
#         urls = self.get_entities()["urls"]
#         if return_format == "url":
#             return [element['url'] for element in urls]
#         elif return_format == "expanded_url":
#             return [element['expanded_url'] for element in urls]
#         elif return_format == "display_url":
#             return [element['display_url'] for element in urls]
#
#     def get_hashtags(self, case_sensitivity="small", hashtag_sign=True): #make it more neat! don't return the entire array of nonesense
#         #https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
#         """
#         :param case_sensitivity: By setting this parameter to small hashtags will be returned in small format. If you set it to original, the hashtags will be returned the same as it written in the tweet..
#         :param hashtag_sign: It indicated whether the # character comes before hashtags or not.
#         :return: a list of hashtags in this tweet.
#         """
#         assert (case_sensitivity in ["small", "original"]), "the case_sensitivity has to be small or original"
#         assert (hashtag_sign in [True, False]), "the hashtag_sign has to be True or False"
#
#         entities = self.get_entities()
#         if "hashtags" in entities:
#             if case_sensitivity == "small":
#                 if hashtag_sign:
#                     return ["#"+element['text'].lower() for element in entities["hashtags"]]
#                 else:
#                     return [element['text'].lower() for element in entities["hashtags"]]
#             elif case_sensitivity == "original":
#                 if hashtag_sign:
#                     return ["#"+element['text'] for element in entities["hashtags"]]
#                 else:
#                     return [element['text'] for element in entities["hashtags"]]
#             # return entities["hashtags"]
#         else:
#             return []
#
#     def get_mentions(self, return_format="screen_name", at_sign=True):
#
#         """
#         :param return_format: It indicates in what format tweet mentions should be returned.
#         :param at_sign: It indicated whether the @ character comes before mentions or not.
#         :return: a list of mentions in this tweet.
#         """
#
#         assert (return_format in ["screen_name", "name", "id", "id_str", "entire_object"]), "the return_format has to be screen_name, name, id, id_str, or entire_object"
#         assert (at_sign in [True, False]), "the at_sign has to be True or False"
#
#         entities = self.get_entities()
#         if "user_mentions" in entities:
#             if at_sign:
#                 if return_format == "screen_name":
#                     return ["@"+element['screen_name'] for element in entities["user_mentions"]]
#                 elif return_format == "name":
#                     return ["@"+element['name'] for element in entities["user_mentions"]]
#                 elif return_format == "id":
#                     return [element['id'] for element in entities["user_mentions"]]
#                 elif return_format == "id_str":
#                     return ["@"+element['id_str'] for element in entities["user_mentions"]]
#                 elif return_format == "entire_object":
#                     return entities["user_mentions"]
#             else:
#                 if return_format == "screen_name":
#                     return [element['screen_name'] for element in entities["user_mentions"]]
#                 elif return_format == "name":
#                     return [element['name'] for element in entities["user_mentions"]]
#                 elif return_format == "id":
#                     return [element['id'] for element in entities["user_mentions"]]
#                 elif return_format == "id_str":
#                     return [element['id_str'] for element in entities["user_mentions"]]
#                 elif return_format == "entire_object":
#                     return entities["user_mentions"]
#         else:
#             return []
#
#     def get_symbols(self):#make it more neat! don't return the entire array of nonesense
#                 # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
#         """
#         :return: a list of symbols in this tweet.
#         """
#         entities = self.get_entities()
#         if "symbols" in entities:
#             return entities["symbols"]
#         else:
#             return []
#
#     def get_media(self):#make it more neat! don't return the entire array of nonesense
#         # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
#         """
#         :return: it returns the photo(s), video, and animated-gif attached to this tweet as a list.
#         """
#         entities = self.get_entities()
#         if "media" in entities:
#             return entities["media"]
#         else:
#             return []
#
#     def get_photo(self):#make it more neat! don't return the entire array of nonesense
#         """
#         :return: it returns the photo(s) attached to this tweet as a list.
#         """
#         media = self.get_media()
#         photos = []
#         for medium in media:
#             if medium["type"] == "photo":
#                 photos.append(medium)
#         return photos
#
#     def get_video(self):#make it more neat! don't return the entire array of nonesense
#         """
#         :return: it returns the video attached to this tweet in a list.
#         """
#         media = self.get_media()
#         videos = []
#         for medium in media:
#             if medium["type"] == "video":
#                 videos.append(medium)
#         return videos
#
#     def get_gif(self):#make it more neat! don't return the entire array of nonesense
#         """
#         :return: it returns the animated-gif attached to this tweet as a list.
#         """
#         media = self.get_media()
#         gifs = []
#         for medium in media:
#             if medium["type"] == "animated_gif":
#                 gifs.append(medium)
#         return gifs
#
# ### Don't forget adding poll object
#
#     def get_text(self):  ## Maybe you need to check this function for retweet and quote class
#         """
#         :return: a string showing the full text of this tweet
#         """
#         tweet_text = None
#         if self.is_retweeted():
#             tweet_text = self.tweet["retweeted_status"]["full_text"]
#         elif not self.is_retweeted():
#             tweet_text = self.tweet["full_text"]
#         return tweet_text
#
#         # elif self.is_quoted():
#         #     tweet_text = self.tweet["full_text"]
#         # elif (not self.is_retweeted()) and (not self.is_quoted()):
#         #     tweet_text = self.tweet["full_text"]
#         # return tweet_text
#
#         ####Noted in the new version
#         # if self.text != "":
#         #     return self.text
#         # else:
#         #     if not self.is_retweeted():
#         #         if self.tweet["truncated"]:
#         #             tweet_text = self.tweet["extended_tweet"]["full_text"]
#         #         else:
#         #             if "full_text" in self.tweet:
#         #                 tweet_text = self.tweet["full_text"]
#         #             else:
#         #                 tweet_text = self.tweet["text"]
#         #     elif self.is_retweeted():
#         #         if self.tweet["retweeted_status"]["truncated"]:
#         #             tweet_text = self.tweet["retweeted_status"]["extended_tweet"]["full_text"]
#         #         else:
#         #             tweet_text = self.tweet["retweeted_status"]["text"]
#         #     return tweet_text
#
#     def get_id(self, return_format='int'):
#         """
#         :return: an integer showing the unique id of this tweet.
#         """
#         if return_format == "int":
#             return self.tweet["id"]
#         elif return_format == "string":
#             return self.tweet["id_str"]
#
#     def is_this_a_reply(self):
#         """
#         :return: a boolean shows whether this tweet is a reply tweet or not.
#         """
#         return False if self.tweet["in_reply_to_status_id"] is None else True
#
#     def get_reply_to_id(self, return_format='int'):
#         """
#         :return: an integer showing the unique id of the tweet that this one is a reply to that.
#         """
#         if return_format == "int":
#             return self.tweet["in_reply_to_status_id"]
#         elif return_format == "string":
#             return self.tweet["in_reply_to_status_id_str"]
#
#     def is_retweeted(self):
#         """
#         :return: a boolean shows whether this tweet is retweeted or not.
#         """
#         return True if "retweeted_status" in self.tweet.keys() else False
#
#     def is_quoted(self):
#         """
#         :return: a boolean showing whether this is a quoted tweet or not..
#         """
#         # return True if "quoted_status" in self.tweet.keys() else False
#         return self.tweet["is_quote_status"]
#
#     def is_quote_available(self):
#         return True if "quoted_status" in self.tweet.keys() else False
#
#     def get_quote(self): #go to the buttom of this
#         """
#         :return: it returns the quoted part of the this tweet..
#         """
#         if self.is_quote_available():
#             return QuoteClass(self.tweet["quoted_status"], self.parameters)
#         else:
#             print("This tweet does not contain a quote status object")
#
#         # return QuoteClass(self.tweet["quoted_status"], self.parameters) if self.is_quoted() else None
#
#     def get_retweeted(self): #go to the buttom of this
#         """
#         :return: it returns the retweeted part of this tweet.
#         """
#         if self.is_retweeted():
#             return RetweetedClass(self.tweet["retweeted_status"], self.parameters)
#         else:
#             print("This tweet does not contain a retweet status object")
#
#     def get_quote_status_id(self, return_format='int'):
#         if self.is_quoted():
#             if return_format == "int":
#                 return self.tweet["quoted_status_id"]
#             elif return_format == "string":
#                 return self.tweet["quoted_status_id_str"]
#         else:
#             print("This tweet does not contain a quote status")
#
#     def tweet_source_status(self): #Where do these official sources come from?
#         """
#         :return: a boolean that shows whether this tweet is posted by an official source or not.
#         """
#         official_clients = ["Twitter for iPhone", "Twitter for Android", "Twitter Web Client", "Twitter for iPad",
#                             "Mobile Web (M5)", "TweetDeck", "Facebook", "Twitter for Windows", "Mobile Web (M2)",
#                             "Twitter for Windows Phone", "Mobile Web", "Google", "Twitter for BlackBerry",
#                             "Twitter for Android Tablets", "Twitter for Mac", "iOS", "Twitter for BlackBerry®"]
#
#         return True if self.get_source(return_format="processed") in official_clients else False
#
#     def tweet_stemming(self, input_text=None, inplace=False):
#         """
#         This function performs the stemming operation using Porter algorithm.
#         :param input_text: if this parameter is None, then stemming is applied on the text field of the caller object, otherwise
#         and in case of a string as an input for this parameter, the stemming is applied on the input text.
#         :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after stemming.
#         :return: when the implace parameter is equal to True, the function changes the caller object text field permanently and
#         returns the whole object, in contrast when it is equal to False the function only returns the text field after
#         the stemming without changing the text field.
#         """
#
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text is None:
#             text = self.get_text()
#         else:
#             text = input_text
#         stemmed = PorterStemmer().stem(text)
#         if inplace:
#             self.text = stemmed
#             return self
#         else:
#             return stemmed
#
#     def hashtag_splitter(self, input_text=None, inplace=False):
#         """
#         This function slices up hashtags as in most of the times, hashtags are made up of concatanation of meaningful words.
#         :param input_text: if this parameter is None, then slicing is applied on the hashtags of the caller object, otherwise
#         and in case of a string as an input for this parameter, the slicing is applied on the input text.
#         :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after slicing up the hashtags.
#         :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
#         by splitting the hashtags and returning the whole object, in contrast when it is equal to False the function only
#         returns the text field after slicing up the hashtags without changing the text field.
#         """
#
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text is None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         hashtags = self.get_hashtags()
#
#         if len(hashtags) > 0:
#             for hashtag in hashtags:
#                 hashtag_text = hashtag["text"]
#                 if text.isupper():
#                     pat = r'[A-Z0-9]+[a-z0-9]*'
#                     replacement = " ".join(re.findall(pat, hashtag_text))
#                     text = text.replace(hashtag_text, replacement)
#                 else:
#                     replacement = " ".join(wordninja.split(hashtag_text))
#                     text = text.replace(hashtag_text, replacement)
#
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def mention_replacement(self, input_text=None, inplace=False):
#         """
#         This function replaces Twitter account mentions by the accounts' screen name.
#         :param input_text: if this parameter is None, then the replacement is applied on the mention of the caller object,
#         otherwise and in case of a string as an input for this parameter, the replacement is applied on the input text.
#         :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after replacing the mentions.
#         :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
#         by replacing the mentions with the accounts screen names and returning the whole object, in contrast when it is equal
#         to False the function only returns the text field after replacing the mentions without changing the text field.
#         """
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         mentions = self.get_mentions()
#         for mention in mentions:
#             text = text.replace(mention["screen_name"], mention["name"])
#
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def url_removal(self, input_text=None, inplace=False):
#         """
#         This function removes the urls from the tweet text.
#         :param input_text: if this parameter is None, then the urls are removed from the caller object text, otherwise
#         and in case of a string as an input for this parameter, the urls are removed from the input text.
#         :param inplace: if inplace is True, the url removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the urls.
#         :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
#         by removing the urls and returning the whole object, in contrast when it is equal to False the function only
#         returns the text field after url removal.
#         """
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         extractor = URLExtract()
#         urls = extractor.find_urls(text)
#         for url in urls:
#             text = text.replace(url, "")
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def hashtags_removal(self, input_text=None, mode=2, inplace=False):
#         """
#         This function removes hashtags from tweet text according to different modes.
#         :param input_text: if this parameter is None, then the hashtag removal is applied on the caller object,
#         otherwise and in case of a string as an input for this parameter, the hashtag removal is applied to the input text.
#         :param mode: there are three modes for hashtags removal. In mode 1, the text remains intact, in Mode 2, only the
#         hashtag characters (#) are removed, and in mode 3, the whole hashtags consisting the hashtag character and the terms
#         after the hashtags are removed.
#         :param inplace: if inplace is True, the hashtag removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the hashtags.
#         :return: when the implace parameter is equal to True, the function removes the hashtags permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#          hashtags from the text.
#         """
#
#         assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if mode == 1:
#             pass
#         elif mode == 2:
#             text = text.replace("#", "")
#         elif mode == 3:
#             for h in self.get_hashtags():
#                 text = text.replace("#" + h["text"], "")
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def mentions_removal(self, input_text=None, mode=2, inplace=False):
#         """
#         This function removes mentions from tweet text according to different modes.
#         :param input_text: if this parameter is None, then the mention removal is applied on the caller object,
#         otherwise and in case of a string as an input for this parameter, the mention removal is applied to the input text.
#         :param mode: there are three modes for mention removal. In mode 1, the text remains intact, in Mode 2, only the
#         mention characters (@) are removed, and in mode 3, the whole mention consisting the mention character and the terms
#         after the mentions are removed.
#         :param inplace: if inplace is True, the mention removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the mention.
#         :return: when the implace parameter is equal to True, the function removes the mentions permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#          mentions from the text.
#         """
#
#         assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if mode == 1:
#             pass
#         elif mode == 2:
#             text = text.replace("@", "")
#         elif mode == 3:
#             for m in self.get_mentions():
#                 text = text.replace("@" + m["screen_name"], "")
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def control_characters_removal(self, input_text=None, inplace=False):
#         """
#         This functions removes common control characters carriage return (\r), line feed (\n), horizontal tab (\t).
#         :param input_text: if this parameter is None, then the control characters are removed from the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the control characters are removed from the input text.
#         :param inplace: if inplace is True, the control characters removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the control characters.
#         :return: when the implace parameter is equal to True, the function removes the control characters permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#          control characters from the text.
#         """
#
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         pattern = re.compile(r'[\r\t\n]')
#         text = pattern.sub(" ", text)
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def stopwords_removal(self, input_text=None, stopword_corpus="stone", inplace=False):
#         """
#         This function removes stopwords from the tweet according to chosen stopword corpus.
#         :param input_text: if this parameter is None, then the stopwords are removed from the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the stopwords are removed from the input text.
#         :param stopword_corpus: The stopword corpus can be "stone", "nltk", "corenlp", or "glascow". Almost every text mining
#          framework uses one of these corpuses for removing the stopwords.
#         :param inplace: if inplace is True, the stopwords removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the stopwords.
#         :return: when the implace parameter is equal to True, the function removes the stopwords permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#         stopwords from the text.
#         """
#
#         assert (stopword_corpus in ["stone", "nltk", "corenlp",
#                                     "glascow"]), "stopword_orpus can be stone, nltk, corenlp, and glascow"
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(text)
#         if stopword_corpus == "stone":
#             processed_text = " ".join(
#                 [word for word in words if word.lower() not in self.parameters["stopwords"]["stone"]])
#         elif stopword_corpus == "nltk":
#             processed_text = " ".join(
#                 [word for word in words if word.lower() not in self.parameters["stopwords"]["nltk"]])
#         elif stopword_corpus == "corenlp":
#             processed_text = " ".join(
#                 [word for word in words if word.lower() not in self.parameters["stopwords"]["corenlp"]])
#         elif stopword_corpus == "glascow":
#             processed_text = " ".join(
#                 [word for word in words if word.lower() not in self.parameters["stopwords"]["glascow"]])
#
#         if inplace:
#             self.text = processed_text
#             return self
#         else:
#             return processed_text
#
#     def whitespace_removal(self, input_text=None, inplace=False):
#         """
#         This functions removes whitespaces from the text.
#         :param input_text: if this parameter is None, then the whitespaces are removed from the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the whitespaces are removed from the input text.
#         :param inplace: if inplace is True, the whitespace removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the whitespaces.
#         :return: when the implace parameter is equal to True, the function removes the whitespaces permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#          whitespaces from the text.
#         """
#
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         text = text.strip()
#         while (text.count("  ") > 0):
#             text = text.replace("  ", " ")
#         if inplace:
#             self.text = text
#             return self
#         else:
#             return text
#
#     def punctuation_removal(self, input_text=None, inplace=False):
#         """
#         This functions removes punctuation characters from the text.
#         :param input_text: if this parameter is None, then the punctuations are removed from the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the punctuations are removed from the input text.
#         :param inplace: if inplace is True, the punctuations removal is permanently applied on the caller object text field, otherwise
#         the caller object text field remains intact and the function returns the text after removing the punctuations.
#         :return: when the implace parameter is equal to True, the function removes the punctuations permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after removing the
#          punctuations from the text.
#         """
#
#         assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         punctuation_free = textstat.remove_punctuation(text).replace(".", "").replace("\"", "").replace("“",
#                                                                                                         "").replace("”",
#                                                                                                                     "").strip()
#         if inplace:
#             self.text = punctuation_free
#             return self
#         else:
#             return punctuation_free
#
#     def text_preprocessing(self, input_text=None, url=True, case=True, punctuation=True, hashtag=2, mention=2,
#                            whitespace=True, control_characters=True, stop="stone", hashtag_split=True,
#                            mention_replacement=True):
#         """
#         This function preprocess the tweet text.
#         :param input_text: if this parameter is None, then preprocessing is performed on the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the preprocessing is applied on the input text.
#         :param url: by setting this boolean parameter True, the tweet urls are removed.
#         :param case: setting this boolean parameter True, turns the tweet text to lower case.
#         :param punctuation: by setting this boolean parameter True, the tweet punctuations are removed.
#         :param hashtag: this integer parameter represents the hashtag removal mode. There are three modes for
#         hashtags removal. In mode 1, the text remains intact, in Mode 2, only the hashtag characters (#) are removed,
#         and in mode 3, the whole hashtags consisting the hashtag character and the terms after the hashtags are removed.
#         :param mention: this integer parameter represents the mention removal mode. There are three modes for
#         mention removal. In mode 1, the text remains intact, in Mode 2, only the mention characters (@) are removed,
#         and in mode 3, the whole mention consisting the hashtag character and the terms after the hashtags are removed.
#         :param whitespace: by setting this boolean parameter True, the tweet whitespaces are removed.
#         :param control_characters: by setting this boolean parameter True, the common control characters (carriage return(\r),
#         line feed(\n), and horizontal tab(\t)) are removed.
#         :param stop: this string parameter represents the stopwords corpus for stopword removal. The stopword corpus can
#         be "stone", "nltk", "corenlp", or "glascow". Almost every text mining framework uses one of these corpuses for
#         removing the stopwords. In order to seactivates stopwords removal, this parameter has to be set to False.
#         :param hashtag_split: by setting this parameter to True, the hashtags are splitted and replaced in the text.
#         :param mention_replacement: by setting this parameter to True, the mentions are replaced by their corresponding screen names.
#         :return: when the implace parameter is equal to True, the function applies the preprocessing permanently and returns
#         the whole object, in contrast when it is equal to False the function only returns the text field after preprocessing.
#         """
#
#         assert (url in [True, False]), "url parameter can be True or False"
#         assert (case in [True, False]), "case parameter can be True or False"
#         assert (punctuation in [True, False]), "punctuation parameter can be True or False"
#         assert (hashtag in [1, 2, 3]), "hashtag parameter can be 1, 2, 3"
#         assert (mention in [1, 2, 3]), "mention parameter can be 1, 2, 3"
#         assert (whitespace in [True, False]), "whitespace parameter can be True or False"
#         assert (control_characters in [True, False]), "control_characters parameter can be True or False"
#         assert (stop in ["stone", "nltk", "corenlp", "glascow",
#                          False]), "stop parameter can be stone, nltk, corenlp, glascow, or False"
#         assert (hashtag_split in [True, False]), "hashtag_split parameter can be True or False"
#         assert (mention_replacement in [True, False]), "mention_replacement parameter can be True or False"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if control_characters == True:
#             text = self.control_characters_removal(input_text=text)
#
#         if url == True:
#             text = self.url_removal(input_text=text)
#
#         if mention_replacement == True:
#             text = self.mention_replacement(input_text=text)
#
#         if hashtag == 1:
#             pass
#         elif hashtag == 2:
#             text = self.hashtags_removal(input_text=text, mode=2)
#         elif hashtag == 3:
#             text = self.hashtags_removal(input_text=text, mode=3)
#
#         if hashtag_split == True:
#             text = self.hashtag_splitter(input_text=text)
#
#         if mention == 1:
#             pass
#         elif mention == 2:
#             text = self.mentions_removal(input_text=text)
#         elif mention == 3:
#             text = self.mentions_removal(input_text=text)
#
#         if case == True:
#             text = text.lower()
#
#         if stop != False:
#             text = self.stopwords_removal(input_text=text, stopword_corpus=stop)
#
#         if punctuation == True:
#             text = self.punctuation_removal(input_text=text)
#
#         if whitespace == True:
#             text = self.whitespace_removal(input_text=text)
#
#         #         if contraction == True
#
#         return text
#
#     def tweet_pos(self, input_text=None):
#         """
#         This function replaces every word in the tweet by its corresponding Part-of-Speech (POS) tag.
#         :param input_text: if this parameter is None, then the Part-of-Speech (POS) tagging is performed on the caller object text field,
#         otherwise and in case of a string as an input for this parameter, the Part-of-Speech tagging is performed on the input text.
#         :return: this function returns the POS tagged version of the tweet.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#         text = self.text_preprocessing(input_text=text)
#         pos_text = ""
#         spacy_text = self.parameters["spacy"](text)
#         for token in spacy_text:
#             pos_text = pos_text + " " + token.pos_
#         return pos_text.strip()
#
#     def tweet_ner(self, input_text=None):
#         """
#         This function replaces every word in the tweet by its corresponding Named-Entity-Recognition (NER) tag.
#         :param input_text: if this parameter is None, then the Named-Entity-Recognition (NER) tagging is performed on the
#         caller object text field, otherwise and in case of a string as an input for this parameter, the
#         NER tagging is performed on the input text.
#         :return: this function returns the Named-Entity-Recognition (NER) tagged version of the tweet.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#         text = self.text_preprocessing(input_text=text)
#
#         ner_text = ""
#         spacy_text = self.parameters["spacy"](text)
#         for token in spacy_text.ents:
#             ner_text = ner_text + " " + token.label_
#
#         return ner_text.strip()
#
#     def tweet_lemmatization(self, input_text=None):
#         """
#         This function replaces every word in the tweet by its corresponding lemma.
#         :param input_text: if this parameter is None, then the lemmatization is performed on the
#         caller object text field, otherwise and in case of a string as an input for this parameter, the
#         lemmatization is performed on the input text.
#         :return: this function returns the lemmatized version of the tweet.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#         text = self.text_preprocessing(input_text=text)
#
#         tweet_lemmas = ""
#         spacy_text = self.parameters["spacy"](text)
#         for token in spacy_text:
#             tweet_lemmas = tweet_lemmas + " " + token.lemma_
#
#         return tweet_lemmas.strip()
#
#     def tweet_tokens(self, preprocessing=True, lemmatization=True, input_text=None):
#         """
#         This function tokenises the tweet text field. If any customized preprocessing is required, the preprocessing can
#         be set to False and text_preprocessing function with arbitrary settings is called and feed to input_text parameter.
#         :param preprocessing: if this parameter is set to True, the default preprocessing is perfomed on tweet text.
#         :param lemmatization: if this parameter is set to True, the lemmatization is performed on the tweet text.
#         :param input_text: if this parameter is None, then the tokenisation is performed on the
#         caller object text field, otherwise and in case of a string as an input for this parameter, the
#         tokenisation is performed on the input text.
#         :return: a list of tokens.
#         """
#
#         assert (preprocessing in [True, False]), "preprocessing is a boolean parameter, so it can be True or False"
#         assert (lemmatization in [True, False]), "lemmatization is a boolean parameter, so it can be True or False"
#
#         if input_text == None:
#             if preprocessing and lemmatization:
#                 return self.tweet_splitter(self.tweet_lemmatization(self.text_preprocessing(self.get_text())))
#             elif preprocessing and lemmatization == False:
#                 return self.tweet_splitter(self.text_preprocessing(self.get_text()))
#             elif preprocessing == False and lemmatization:
#                 return self.tweet_splitter(self.tweet_lemmatization(self.get_text()))
#             elif preprocessing == False and lemmatization == False:
#                 return self.tweet_splitter(self.get_text())
#         else:
#             if preprocessing and lemmatization:
#                 return self.tweet_splitter(self.tweet_lemmatization(self.text_preprocessing(input_text=input_text)))
#             elif preprocessing and lemmatization == False:
#                 return self.tweet_splitter(self.text_preprocessing(input_text=input_text))
#             elif preprocessing == False and lemmatization:
#                 return self.tweet_splitter(self.tweet_lemmatization(input_text=input_text))
#             elif preprocessing == False and lemmatization == False:
#                 return self.tweet_splitter(input_text=input_text)
#
#     def get_emojis(self, count=True, emoji_list=True, input_text=None):
#         """
#         This function collects the emojis from tweet text.
#         :param count: if this is set to True, the function counts the number of emojis in the tweet.
#         :param emoji_list: if this is set to True, the function collects the emojis in the tweet.
#         :param input_text: if this parameter is None, then the emojis are extracted from the
#         caller object text field, otherwise and in case of a string as an input for this parameter, the
#         emojis are extracted from the input text.
#         :return: if both parameters are set to True, then the function returns a dictionary containing the list of emojis and
#         their number. if only count is set to True, the number of emojis is returned and if emoji_list is set to True, the
#         list of emojis is returned.
#         """
#         assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
#         assert (emoji_list in [True, False]), "emoji_list is a boolean parameter, so it can be True or False"
#         assert (count or emoji_list), "at least one of the count and emoji_list parameters " \
#                                       "has to be set to True"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         emojis = emoji.emoji_lis(text)
#         if emoji_list == True and count == True:
#             return {"emoji_count": len(emojis), "emoji_list": emojis}
#         elif emoji_list == True and count == False:
#             return emojis
#         elif emoji_list == False and count == True:
#             return len(emojis)
#
#             # Emoticon analysos <= doesn't work properly
#
#     def get_emoticon(self, count=True, emoticon_list=True, input_text=None):
#         """
#         This function collects the emoticons from tweet text.
#         :param count: if this is set to True, the function counts the number of emoticons in the tweet.
#         :param emoji_list: if this is set to True, the function collects the emoticons in the tweet.
#         :param input_text: if this parameter is None, then the emoticons are extracted from the
#         caller object text field, otherwise and in case of a string as an input for this parameter, the
#         emoticons are extracted from the input text.
#         :return: if both parameters are set to True, then the function returns a dictionary containing the list of emoticons and
#         their number. if only count is set to True, the number of emoticons is returned and if emoticons_list is set to True, the
#         list of emoticons is returned.
#         """
#         assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
#         assert (emoticon_list in [True, False]), "emoticon_list is a boolean parameter, so it can be True or False"
#         assert (count or emoticon_list), "at least one of the count and emoticon_list parameters " \
#                                          "has to be set to True"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(text)
#         emoticons = [word for word in words if word in self.parameters["emoticons"]]
#
#         if emoticon_list == True and count == True:
#             return {"emoticons_count": len(emoticons), "emoticon_list": emoticons}
#         elif emoticon_list == True and count == False:
#             return emoticons
#         elif emoticon_list == False and count == True:
#             return len(emoticons)
#
#     def tweet_splitter(self, input_text=None, split_unit="word"):
#         """
#         this function splits the tweet text field according to chosen splitting unit.
#         :param input_text: if this parameter is None, then the caller object text field is splitted, otherwise
#         and in case of a string as an input for this parameter, the input text is splitted up.
#         :param split_unit: the splitting unit can be "word", or "sentence".
#         :return: a list containing the splitting units.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if split_unit == "word":
#             return re.findall(r'\S+', text)
#         elif split_unit == "sentence":
#             return [i for i in re.split(r'[.?!]+', text) if i != '']
#
#     def text_length(self, input_text=None, length_unit="word"):
#         """
#         this function measures the length of the tweet based on the selected length unit.
#         :param input_text: if this parameter is None, then the length of caller object text field is measured, otherwise
#         and in case of a string as an input for this parameter, the length of input text is measured.
#         :param length_unit: the length unit can be "character", "word", or "sentence".
#         :return: an integer showing the length of the tweet text field.
#         """
#
#         assert (length_unit in ["character", "word", "sentence"]), "the unit can be character, word, or sentence"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if length_unit == "character":
#             return len(text)
#         elif length_unit == "word":
#             return len(self.tweet_splitter(split_unit="word", input_text=text))
#         elif length_unit == "sentence":
#             return len(self.tweet_splitter(split_unit="sentence", input_text=text))
#
#     def text_complexity(self, input_text=None, complexity_unit="word"):
#         """
#         this function measures the complexity of a tweet text based on the selected complexity unit.
#         :param input_text: if this parameter is None, then the complexity of caller object text field is measured, otherwise
#         and in case of a string as an input for this parameter, the complexity of input text is measured.
#         :param complexity_unit: the complexity unit can be "word", "sentence", or "syllables".
#         :return: an float showing the complexity of the tweet text.
#         """
#
#         assert (complexity_unit in ["word", "sentence", "syllables"]), "unit parameter can be word, sentence, or syllables"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if complexity_unit == "word":
#             return np.average([len(word) for word in self.tweet_splitter(split_unit="word", input_text=text)])
#         elif complexity_unit == "sentence":
#             return np.average([len(self.tweet_splitter(split_unit="word", input_text=sentence)) for sentence in
#                                self.tweet_splitter(split_unit="sentence", input_text=text)])
#         elif complexity_unit == "syllables":
#             return np.average(
#                 [textstat.syllable_count(i, lang='en_US') for i in self.tweet_splitter(split_unit="word", input_text=text)])
#
#     def text_pronoun_count(self, input_text=None, pronoun="third_singular"):
#         """
#         This function counts the number of pronouns in the tweet text according to selected pronoun for counting.
#         :param input_text: if this parameter is None, then the number of chosen pronoun in the caller object text field
#         is counted, otherwise and in case of a string as an input for this parameter, the number of chosen pronoun in the
#         input_text is counted.
#         :param pronoun: the pronoun can be "first_singular", "first_plural", "second_singular", "second_plural", "third_singular", or
#         "third_plural".
#         :return: an integer showing the number of chosen pronoun in the tweet text.
#         """
#
#         assert (pronoun in ["first_singular", "first_plural", "second_singular", "second_plural", "third_singular",
#                             "third_plural"]), "the pronoun parameter can be first_singular, first_plural, second_singular, second_plural, " \
#                                               "third_singular, or third_plural"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = [i.lower() for i in self.tweet_splitter(split_unit="word", input_text=text)]
#         if pronoun == "first_singular":
#             return words.count("i") + words.count("my") + words.count("mine") + words.count("me") + words.count(
#                 "myself") + words.count("i'm") + words.count("i've") + words.count("i'd") + words.count("i'll")
#         elif pronoun == "first_plural":
#             return words.count("we") + words.count("our") + words.count("ours") + words.count("us") + words.count(
#                 "ourselves") + words.count("we're") + words.count("we've") + words.count("we'd") + words.count("we'll")
#         elif pronoun == "second_singular":
#             return words.count("you") + words.count("your") + words.count("yours") + words.count(
#                 "yourself") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
#                 "you'll")
#         elif pronoun == "second_plural":
#             return words.count("you") + words.count("your") + words.count("yours") + words.count(
#                 "yourselves") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
#                 "you'll")
#         elif pronoun == "third_singular":
#             return words.count("he") + words.count("she") + words.count("it") + words.count("his") + words.count(
#                 "her") + words.count("its") + words.count("him") + words.count("hers") + words.count(
#                 "he's") + words.count("she's") + words.count("it's") + words.count("he'll") + words.count(
#                 "she'll") + words.count("it'll") + + words.count("he'd") + words.count("she'd") + words.count("it'd")
#         elif pronoun == "third_plural":
#             return words.count("they") + words.count("them") + words.count("their") + words.count(
#                 "theirs") + words.count("themselves") + words.count("they're") + words.count("they've") + words.count(
#                 "they'd") + words.count("they'll")
#
#     def case_analysis(self, count=True, frac=True, unit_of_analysis="character",
#                       input_text=None):  #### THINK ABOUT DIVISION BY ZERO ERROR ####
#         """
#         This function analyses the count and fraction of upper and lower letters or capital and small words in the tweet text
#         depending on the selected unit of analysis.
#         :param count: if this is set to True, the function count the number of upper and lower letters or capital and small words
#         in the tweet text.
#         :param frac: if this is set to True, the function measures the fraction of  upper and lower letters or capital and small words
#         in the tweet text.
#         :param unit_of_analysis: the unit parameter can be word or character.
#         :param input_text: if this parameter is None, then the case analysis is performed on the caller object text field
#         , otherwise and in case of a string as an input for this parameter, the case analysis is performed on the input_text.
#         :return: it returns a dictionary which its content depends on the parameters value. If the unit of analysis is
#         set to character, depending on the value of count and frac parameters, the dictionary contains
#         either the number of lowercase and uppercase characters, or ratio of lowercase and uppercase characters to all characters,
#         or both. If the unit of analysis is set to word, then depending on the value of count and frac parameters,
#         the dictionary contains either the number of capital and small words, or ratio of capital and small words to
#         all words, or both.
#         """
#
#         assert (count in [True, False]), "count is a boolean parameter, so it can be True or False"
#         assert (frac in [True, False]), "frac is a boolean parameter, so it can be True or False"
#         assert (unit_of_analysis in ["character", "word"]), "unit can be character or word"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if unit_of_analysis == "character":
#             uppercase_character_count = sum(1 for i in text if i.isupper())
#             lowercase_character_count = sum(1 for i in text if i.islower())
#             character_count = self.text_length(length_unit="character", input_text=text)
#             if count == True and frac == True:  ######### THINK ABOUT DIVISION BY ZERO ERROR ###
#                 try:
#                     return {"uppercase_character_count": uppercase_character_count,
#                             "lowercase_character_count": lowercase_character_count,
#                             "uppercase_to_lowercase": uppercase_character_count / lowercase_character_count,
#                             "lowercase_to_all_characters": lowercase_character_count / character_count,
#                             "uppercase_to_all_characters": uppercase_character_count / character_count}
#                 except ZeroDivisionError:
#                     if character_count == 0:
#                         print(
#                             "the number of characters is zero, consequently the number of lowercase character is zero")
#                     elif lowercase_character_count == 0:
#                         print("the number of lowercase characters is zero")
#
#             elif count == True and frac == False:
#                 return {"uppercase_character_count": uppercase_character_count,
#                         "lowercase_character_count": lowercase_character_count}
#             elif count == False and frac == True:
#                 try:
#                     return {"uppercase_to_lowercase": uppercase_character_count / lowercase_character_count,
#                             "lowercase_to_all_characters": lowercase_character_count / character_count,
#                             "uppercase_to_all_characters": uppercase_character_count / character_count}
#                 except ZeroDivisionError:
#                     if character_count == 0:
#                         print(
#                             "the number of characters is zero, consequently the number of lowercase characters is zero")
#                     elif lowercase_character_count == 0:
#                         print("the number of lowercase characters is zero")
#
#         elif unit_of_analysis == "word":
#             words = self.tweet_splitter(split_unit="word", input_text=text)
#             capital_words_count = len([b for b in words if b.isupper()])
#             small_words_count = len([b for b in words if b.islower()])
#             words_count = len(words)
#             if count == True and frac == True:
#                 try:
#                     return {"capital_words_count": capital_words_count, "small_words_count": small_words_count,
#                             "capital_to_small": capital_words_count / small_words_count,
#                             "capital_to_all_words": capital_words_count / words_count,
#                             "small_to_all_words": small_words_count / words_count}
#                 except ZeroDivisionError:
#                     if words_count == 0:
#                         print("the number of words is zero, consequently the number of snall words is zero")
#                     elif small_words_count == 0:
#                         print("the number of small words is zero")
#
#             elif count == True and frac == False:
#                 return {"capital_words_count": capital_words_count, "small_words_count": small_words_count}
#             elif count == False and frac == True:
#                 try:
#                     return {"capital_to_small": capital_words_count / small_words_count,
#                             "capital_to_all_words": capital_words_count / words_count,
#                             "small_to_all_words": small_words_count / words_count}
#                 except ZeroDivisionError:
#                     if words_count == 0:
#                         print("the number of words is zero, consequently the number of snall words is zero")
#                     elif small_words_count == 0:
#                         print("the number of small words is zero")
#
#     def exclamation_mark_count(self, input_text=None):
#         """
#         This function counts the number of exclamation mark in  the tweet text field.
#         :param input_text: if this parameter is None, then the number of exclamation mark in the caller object text field
#         is counted, otherwise and in case of a string as an input for this parameter, the number of exclamation mark in the
#          input_text is counted.
#         :return: an integer showing the number of exclamation mark in the tweet text.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#         return text.count("!")
#
#     def question_mark_count(self, input_text=None):
#         """
#         This function counts the number of question marks in the tweet text field.
#         :param input_text: if this parameter is None, then the number of question marks in the caller object text field
#         is counted, otherwise and in case of a string as an input for this parameter, the number of question marks in the
#          input_text is counted.
#         :return: an integer showing the number of question marks in the tweet text.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#         return text.count("?")
#
#     def abbreviations(self, input_text=None):
#         """
#         This function finds the abbreviations used in tweet text.
#         :param input_text: if this parameter is None, then the function finds the abbreviations used in the caller object text field
#         , otherwise and in case of a string as an input for this parameter, the function finds the abbreviations in the
#         input_text.
#         :return: a list of abbreviations used in the tweet text.
#         """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(split_unit="word", input_text=text)
#         return [i for i in words if i in self.parameters["abbr"]]
#
#     def vulgar_words(self, input_text=None):
#         """
#          This function finds the vulgar terms used in tweet text.
#          :param input_text: if this parameter is None, then the function finds the vulgar terms used in the caller object text field
#          , otherwise and in case of a string as an input for this parameter, the function finds the vulgar terms in the
#          input_text.
#          :return: a list of vulgar terms used in the tweet text.
#          """
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(split_unit="word", input_text=text)
#         return [i for i in words if i in self.parameters["vulgar"]]
#
#     def sentiment_analysis(self, sentiment_engine="vader", input_text=None):
#         """
#         This function performs sentiment analysis over tweet text field using various sentiment analysis engines
#         :param sentiment_engine: sentiment_engine can be "textblob", "vader", "nrc", "hate_speech", or "vad".
#         :param input_text: if this parameter is None, then the function measure the sentiment of the caller object text field
#          , otherwise and in case of a string as an input for this parameter, the function measures the sentiment of the
#          input_text.
#         :return: it returns a dictionary containing various sentiment scores depending on the chosen sentiment_engine. If
#         it is textblob, the sentiment scores are polarity and subjectivity. If it vader, the scores are positivity, negativity,
#         neutrality, and composite score. If the sentiment_engine is nrc, then the sentiment scores are anger, disgust, sadness,
#         anticipation, fear, surprise, joy, and trust. If the hate_speech engine is chosen, the scores  woud be hate_speech,
#         offensive language, and neither. And finally, if the sentiment engine is vad, the scores would be valence, arousal,
#         and dominance.
#         """
#
#         assert (sentiment_engine in ["textblob", "vader", "nrc", "hate_speech",
#                                      "vad"]), "the sentiment_engine has to be" \
#                                               "textblob, vader, nrc, hate_speech, or vad"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if sentiment_engine == "textblob":
#             return {"subjectivity": TextBlob(text).sentiment.subjectivity,
#                     "polarity": TextBlob(text).sentiment.polarity}
#         elif sentiment_engine == "vader":
#             return {"positivity_score": self.parameters["vader"].polarity_scores(text)["pos"],
#                     "negativity_score": self.parameters["vader"].polarity_scores(text)["neg"],
#                     "neutrality_score": self.parameters["vader"].polarity_scores(text)["neu"],
#                     "composite_score": self.parameters["vader"].polarity_scores(text)["compound"]}
#         elif sentiment_engine == "nrc":
#             nrc_text_list = self.tweet_splitter(split_unit="word", input_text=text)
#             anger_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     anger_score += self.parameters["nrc"][term]["anger"]
#             anticipation_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     anticipation_score += self.parameters["nrc"][term]["anticipation"]
#             disgust_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     disgust_score += self.parameters["nrc"][term]["disgust"]
#             fear_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     fear_score += self.parameters["nrc"][term]["fear"]
#             joy_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     joy_score += self.parameters["nrc"][term]["joy"]
#             sadness_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     sadness_score += self.parameters["nrc"][term]["sadness"]
#             surprise_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     surprise_score += self.parameters["nrc"][term]["surprise"]
#             trust_score = 0
#             for term in nrc_text_list:
#                 if term in self.parameters["nrc"]:
#                     trust_score += self.parameters["nrc"][term]["trust"]
#             return {"anger_score": anger_score, "anticipation_score": anticipation_score,
#                     "disgust_score": disgust_score, "fear_score": fear_score, "joy_score": joy_score,
#                     "sadness_score": sadness_score, "surprise_score": surprise_score, "trust_score": trust_score}
#         elif sentiment_engine == "hate_speech":
#             sonar2 = self.parameters["sonar"].ping(text)
#             return {"hate_speech": sonar2["classes"][0]["confidence"],
#                     "offensive_language": sonar2["classes"][1]["confidence"],
#                     "neither": sonar2["classes"][2]["confidence"]}
#         elif sentiment_engine == "vad":
#             word_list = self.tweet_splitter(split_unit="word", input_text=text)
#
#             valence_score = 0
#             for term in word_list:
#                 if term in self.parameters["vad"]:
#                     valence_score += self.parameters["vad"][term]["valence"]
#
#             arousal_score = 0
#             for term in word_list:
#                 if term in self.parameters["vad"]:
#                     arousal_score += self.parameters["vad"][term]["arousal"]
#
#             dominance_score = 0
#             for term in word_list:
#                 if term in self.parameters["vad"]:
#                     dominance_score += self.parameters["vad"][term]["dominance"]
#
#             return {"valence_score": valence_score, "arousal_score": arousal_score, "dominance_score": dominance_score}
#
#     def readability(self, readability_metric="flesch_kincaid_grade", input_text=None):
#         """
#         This function measures the readability of the tweet text according to the chosen readbility metric.
#         :param readability_metric: the readability metrics can be "flesch_kincaid_grade", "gunning_fog", "smog_index",
#         "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score"
#         :param input_text: if this parameter is None, then the function measures the readability of the caller object text field
#          , otherwise and in case of a string as an input for this parameter, the function measures the readability of the
#          input_text.
#         :return:
#         """
#
#         assert (readability_metric in ["flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
#                            "coleman_liau_index", "linsear_write_formula",
#                            "dale_chall_readability_score"]), "The metric " \
#                                                              "has to be flesch_kincaid_grade, gunning_fog, smog_index, " \
#                                                              "automated_readability_index, coleman_liau_index, linsear_write_formula," \
#                                                              "or dale_chall_readability_score."
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         if readability_metric == "flesch_reading_ease":
#             return textstat.flesch_reading_ease(text)
#         elif readability_metric == "flesch_kincaid_grade":
#             return textstat.flesch_kincaid_grade(text)
#         elif readability_metric == "gunning_fog":
#             return textstat.gunning_fog(text)
#         elif readability_metric == "smog_index":
#             return textstat.smog_index(text)
#         elif readability_metric == "automated_readability_index":
#             return textstat.automated_readability_index(text)
#         elif readability_metric == "coleman_liau_index":
#             return textstat.coleman_liau_index(text)
#         elif readability_metric == "linsear_write_formula":
#             return textstat.linsear_write_formula(text)
#         elif readability_metric == "dale_chall_readability_score":
#             return textstat.dale_chall_readability_score(text)
#
#     def long_words_count(self, threshold=6, input_text=None):
#         """
#         This function counts the number of words that are longer than a particular threshold.
#         :param threshold: an integer showing the threshhold of long words.
#         :param input_text: if this parameter is None, then the function counts the long words in the caller object text field
#          , otherwise and in case of a string as an input for this parameter, the function counts the number of long words in the
#          input_text.
#         :return: an integer number showing the number of words which are longer than a particular threshhold.
#         """
#
#         assert (isinstance(threshold, int) and threshold > 0), "threshhold has to be a positive integer"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(split_unit="word", input_text=text)
#         return len([i for i in words if len(i) > threshold])
#
#     def multiple_syllables_count(self, threshold=2, input_text=None):
#         """
#         This function counts the number of words that their syllables number is more than a particular threshold.
#         :param threshold: an integer showing the threshhold of syllables.
#         :param input_text: if this parameter is None, then the function counts the number of syllables in the caller object text field
#          , otherwise and in case of a string as an input for this parameter, the function counts the number of syllables in the
#          input_text.
#         :return: an integer number showing the number of wordsthat that their syllables number is higher than a particular threshold.
#         """
#
#         assert (isinstance(threshold, int) and threshold > 0), "threshhold has to be a positive integer"
#
#         if input_text == None:
#             text = self.get_text()
#         else:
#             text = input_text
#
#         words = self.tweet_splitter(split_unit="word", input_text=text)
#         return len([i for i in words if textstat.syllable_count(i, lang='en_US') > threshold])
#
#     def get_tweet_photos(self, saving_address):
#         photos = self.get_photo()
#         for photo in photos:
#             url = photo["media_url"]
#             local_filename = url.split('/')[-1]
#             response = requests.get(url, stream=True)
#             if response.status_code == 200:
#                 with open(saving_address + local_filename, 'wb') as f:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             f.write(chunk)
#             elif response.status_code == 404:
#                 print("the photo in the specified address is not found")
#             else:
#                 return ("the error code: ", response.status_code)
#
#     def get_tweet_videos(self, saving_address):
#         videos = self.get_video()  # So far, there is only possibility of uploading one single video in every tweet
#         for video in videos:
#             urls = video["video_info"]["variants"]
#             for variant in urls:
#                 if variant['content_type'] == 'video/mp4':
#                     url = variant["url"]
#                     break
#             response = requests.get(url, stream=True)
#             if response.status_code == 200:
#                 local_filename = url.split('/')[-1]
#                 reg = re.search(r'^.*\?', local_filename)
#                 file_name = local_filename[reg.start():reg.end()].replace("?", "")
#                 with open(saving_address + file_name, 'wb') as f:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             f.write(chunk)
#             elif response.status_code == 404:
#                 print("the video in the specified address is not found")
#             else:
#                 return ("the error code: ", response.status_code)
#
#     def get_tweet_gifs(self, saving_address):
#         gifs = self.get_gif()  # So far, there is only possibility of uploading one single gif in every tweet
#         for gif in gifs:
#             url = gif["video_info"]["variants"][0]["url"]
#             response = requests.get(url, stream=True)
#             if response.status_code == 200:
#                 file_name = url.split('/')[-1]
#                 # reg = re.search(r'^.*\?', local_filename)
#                 # file_name = local_filename[reg.start():reg.end()].replace("?","")
#                 with open(saving_address + file_name, 'wb') as f:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             f.write(chunk)
#             elif response.status_code == 404:
#                 print("the gif in the specified address is not found")
#             else:
#                 return ("the error code: ", response.status_code)


class RetweetedClass(SingleTweet):
    def __init__(self, tweet, param):
        """
        This is the constructor for the RetweetedClass.
        :param twt: a tweet object.
        :param para: a dictionary of necessary objects and modules.
        """
        super().__init__(param=param)
        self.tweet = tweet

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


class QuoteClass(SingleTweet):
    def __init__(self, tweet, param):
        """
        This is the constructor for the QuoteClass.
        :param twt: a tweet object.
        :param para: a dictionary of necessary objects and modules.
        """

        super().__init__(param=param)
        self.tweet = tweet

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





