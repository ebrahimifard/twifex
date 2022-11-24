from dateutil.relativedelta import *
from datetime import datetime


class TemporalTweets:
    def __init__(self, tweets):
        self._tweets = tweets

    def tweets_period(self):
        """
        :return: a sorted list of tweets creation time
        """
        tweet_dates = []
        for tweet in self._tweets:
            tweet_dates.append(tweet.get_tweet_creation_time())
        return sorted(tweet_dates)

    def tweets_in_periods(self, resolution="years", frequency=1, starting_point="first_of_month"):
        """
        :param resolution: the time resolution of tweets categories. It can be "years", "months", "weeks", "days",
        "hour", "minute" and "second".
        :param frequency: the time frequency of tweets categories. For instance, if resolution="week" and frequency=2,
        it means tweets are categorised by the time-frame of two weeks.
        :param starting_point: The starting point of the temporal tweets dictionary.
        :return: a dictionary of temporal tweets. The key-value pair in this dictionary corresponds to
        the timestamps and all the tweets that are posted within every timestamp.
        """

        assert (resolution in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                    " resolution " \
                                                                                                    "should be" \
                                                                                                    " years," \
                                                                                                    " months," \
                                                                                                    " weeks, " \
                                                                                                    "days, " \
                                                                                                    "hours," \
                                                                                                    " minutes," \
                                                                                                    " or seconds"

        assert (starting_point in ["first_of_month", "first_tweet"]), "The starting_point should be either " \
                                                                      "first_of_month, or first_tweet"

        sorted_tweet_times = self.tweets_period()

        if starting_point == "first_of_month":
            first = sorted_tweet_times[0]
            time_frame = f"{first.year}-{first.month}-1 00:00:00"
            time_frame = datetime.strptime(time_frame, "%Y-%m-%d %H:%M:%S")
        elif starting_point == "first_tweet":
            time_frame = sorted_tweet_times[0]

        last = sorted_tweet_times[-1]
        temporal_tweets = {}

        args = {resolution: frequency}

        while time_frame <= last:
            temporal_tweets[time_frame] = []
            time_frame += relativedelta(**args)

        for tweet in self._tweets:
            tweet_time = tweet.get_tweet_creation_time()
            for time_frame in temporal_tweets:
                if time_frame <= tweet_time < time_frame + relativedelta(**args):
                    temporal_tweets[time_frame].append(tweet)
                    break

        return temporal_tweets
