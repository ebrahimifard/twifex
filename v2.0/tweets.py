from network import Network
from temporal_tweets import TemporalTweets
from spatial_tweets import SpatialTweets


class Tweets:
    def __init__(self, tweets_list):

        assert isinstance(tweets_list, list), "The tweets_list has to be a list"

        self._tweets = tweets_list
        self._tweets_networks = Network(self._tweets)
        self._tweets_temporal = TemporalTweets(self._tweets)
        self._tweets_spatial = SpatialTweets(self._tweets)

    def get_tweets_list(self):
        return self._tweets

    def reap_all_tweets(self):
        """
        This function collects all the tweet objects (even those which are embedded within retweet or quote objects) in input tweet list.
        :return: a dictionary where each key-value pair corresponds to tweet_id and its corresponding tweet object.
        """
        all_tweets = {}
        for tweet in self._tweets:
            all_tweets[tweet.get_tweet_id()] = tweet

            if tweet.is_tweet_retweeted():
                tweet_rt = tweet.get_tweet_retweet_object()
                all_tweets[tweet_rt.get_tweet_id()] = tweet_rt

                if tweet_rt.is_quote_status_object_available():
                    tweet_rt_qt = tweet_rt.get_quote_status_object()
                    all_tweets[tweet_rt_qt.get_tweet_id()] = tweet_rt_qt

            if tweet.is_quote_status_object_available():
                tweet_qt = tweet.get_quote_status_object()
                all_tweets[tweet_qt.get_tweet_id()] = tweet_qt

        return all_tweets

    def get_tweets_network(self):
        return self._tweets_networks

    def get_temporal_tweets(self):
        return self._tweets_temporal

    def get_spatial_tweets(self):
        return self._tweets_spatial
