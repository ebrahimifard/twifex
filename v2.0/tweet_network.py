import networkx as nx


class TweetNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # retweet/quote/reply networks
    def tweet_level_retweet_network_building(self):
        tweet_level_retweet_network = nx.DiGraph()
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()

            if retweet_condition:
                tweet_level_retweet_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
            else:
                tweet_level_retweet_network.add_node(tweet.get_tweet_id())

        return tweet_level_retweet_network

    def tweet_level_quote_network_building(self):
        tweet_level_quote_network = nx.DiGraph()
        for tweet in self._tweets:
            quote_condition = tweet.is_quote_status_object_available()

            if quote_condition:
                tweet_level_quote_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")
                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    tweet_level_quote_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")
            else:
                tweet_level_quote_network.add_node(tweet.get_tweet_id())

        return tweet_level_quote_network

    def tweet_level_reply_network_building(self):
        tweet_level_reply_network = nx.DiGraph()
        for tweet in self._tweets:
            reply_condition = tweet.is_tweet_a_reply()

            if reply_condition:
                tweet_level_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
            else:
                tweet_level_reply_network.add_node(tweet.get_tweet_id())

        return tweet_level_reply_network

    # quote-reply/retweet-reply/retweet-quote networks
    def tweet_level_quote_reply_network_building(self):
        tweet_level_quote_reply_network = nx.DiGraph()
        for tweet in self._tweets:
            quote_condition = tweet.is_quote_status_object_available()
            reply_condition = tweet.is_tweet_a_reply()

            if quote_condition is True and reply_condition is True:
                tweet_level_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")
                tweet_level_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="quote")

                inner_reply_condition_level_one = tweet.get_quote_status_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_reply_condition_level_one:
                    tweet_level_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    tweet_level_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")
            elif quote_condition is True and reply_condition is False:
                tweet_level_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")

                inner_reply_condition = tweet.get_quote_status_object().is_tweet_a_reply()
                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_reply_condition:
                    tweet_level_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition:
                    tweet_level_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")
            elif quote_condition is False and reply_condition is True:
                tweet_level_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
            elif quote_condition is False and reply_condition is False:
                tweet_level_quote_reply_network.add_node(tweet.get_tweet_id())

        return tweet_level_quote_reply_network

    def tweet_level_retweet_reply_network_building(self):
        tweet_level_retweet_reply_network = nx.DiGraph()
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            reply_condition = tweet.is_tweet_a_reply()

            # This condition seems impossible to happen
            if retweet_condition is True and reply_condition is True:
                tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
                tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")

                inner_reply_condition = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                if inner_reply_condition:
                    tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_reply_to_id(), kind="reply")
            elif retweet_condition is True and reply_condition is False:
                tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
                inner_reply_condition = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                if inner_reply_condition:
                    tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_reply_to_id(), kind="reply")
            elif retweet_condition is False and reply_condition is True:
                tweet_level_retweet_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
            elif retweet_condition is False and reply_condition is False:
                tweet_level_retweet_reply_network.add_node(tweet.get_tweet_id())

        return tweet_level_retweet_reply_network

    def tweet_level_retweet_quote_network_building(self):
        tweet_level_retweet_quote_network = nx.DiGraph()
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            quote_condition = tweet.is_quote_status_object_available()

            # The following condition seems impossible to happen so we skip it
            # if retweet_condition is True and reply_condition is True:
            if retweet_condition is True and quote_condition is False:
                tweet_level_retweet_quote_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_tweet_quoted()
                if inner_quote_condition_level_one:
                    tweet_level_retweet_quote_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), kind="quote")
                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    if inner_quote_condition_level_two:
                        tweet_level_retweet_quote_network.add_edge(tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_quote_id(), kind="quote")
            elif retweet_condition is False and quote_condition is True:
                tweet_level_retweet_quote_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")
                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    tweet_level_retweet_quote_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")
            elif retweet_condition is False and quote_condition is False:
                tweet_level_retweet_quote_network.add_node(tweet.get_tweet_id())

        return tweet_level_retweet_quote_network

    # retweet-quote-reply network
    def tweet_level_retweet_quote_reply_network_building(self):
        tweet_level_retweet_quote_reply_network = nx.DiGraph()
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            quote_condition = tweet.is_quote_status_object_available()
            reply_condition = tweet.is_tweet_a_reply()

            # The two following conditions never occur and we skip them
            # if retweet_condition is True and quote_condition is True and reply_condition is True:
            # elif retweet_condition is True and quote_condition is True and reply_condition is False:

            # This condition seems impossible to happen
            if retweet_condition is True and quote_condition is False and reply_condition is True:
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
                inner_reply_condition_level_one = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_quote_status_object_available()
                if inner_reply_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), kind="quote")
                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    inner_reply_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_a_reply()
                    if inner_quote_condition_level_two:
                        tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_quote_id(), kind="quote")
                    if inner_reply_condition_level_two:
                        tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_reply_to_id(), kind="reply")

            elif retweet_condition is True and quote_condition is False and reply_condition is False:
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_tweet_retweet_object().get_tweet_id(), kind="retweet")
                inner_reply_condition_level_one = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_quote_status_object_available()
                if inner_reply_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), kind="quote")
                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    inner_reply_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_a_reply()
                    if inner_quote_condition_level_two:
                        tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_quote_id(), kind="quote")
                    if inner_reply_condition_level_two:
                        tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id(), tweet.get_tweet_retweet_object().get_quote_status_object().get_reply_to_id(), kind="reply")

            elif retweet_condition is False and quote_condition is True and reply_condition is True:
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
                inner_reply_condition_level_one = tweet.get_quote_status_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_reply_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")

            elif retweet_condition is False and quote_condition is True and reply_condition is False:
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_quote_status_object().get_tweet_id(), kind="quote")
                inner_reply_condition_level_one = tweet.get_quote_status_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_reply_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote_status_object().get_tweet_id(), tweet.get_quote_status_object().get_tweet_quote_id(), kind="quote")

            elif retweet_condition is False and quote_condition is False and reply_condition is True:
                tweet_level_retweet_quote_reply_network.add_edge(tweet.get_tweet_id(), tweet.get_reply_to_id(), kind="reply")
            elif retweet_condition is False and quote_condition is False and reply_condition is False:
                tweet_level_retweet_quote_reply_network.add_node(tweet.get_tweet_id())

        return tweet_level_retweet_quote_reply_network
