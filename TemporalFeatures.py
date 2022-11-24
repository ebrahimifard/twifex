import datetime
from dateutil.relativedelta import *

class TemporalFeatures:
    def __init__(self, tweets):
        """
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object
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
            print(len(self.tweets))
            for tweet_id, tweet in self.tweets.items():
                tweet_time = tweet.get_creation_time()
                for time_frame in temporal_tweets:
                    if time_frame <= tweet_time < time_frame + relativedelta(minutes=frequency):
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