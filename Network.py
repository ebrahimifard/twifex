import networkx as nx


class Network:
    def __init__(self, tweets):
        """
        This is a constructor of a network class.
        :param tweets: a dictionary that maps every tweet_id to its corresponding SingleTweet object.
        """
        # self.network = nx.DiGraph()
        self.tweets = tweets
        # self.network = nx.DiGraph()

        ### The network here should be DiGraph and not MultiGraph becasue it is not possible to have multiple edges for retweet, quote, and reply networks.
        self.tweet_level_retweet_network = nx.DiGraph()
        self.tweet_level_quote_network = nx.DiGraph()
        self.tweet_level_reply_network = nx.DiGraph()
        self.tweet_level_quote_reply_network = nx.DiGraph()
        self.tweet_level_retweet_reply_network = nx.DiGraph()
        self.tweet_level_retweet_quote_network = nx.DiGraph()
        self.tweet_level_retweet_quote_reply_network = nx.DiGraph()

        self.tweet_level_cooccurrence_hashtag_network = nx.Graph()
        self.tweet_level_cooccurrence_mention_network = nx.Graph()
        self.tweet_level_cooccurrence_url_network = nx.Graph()

        self.tweet_hashtag_bipartite_network = nx.DiGraph()
        self.tweet_mention_bipartite_network = nx.DiGraph()
        self.tweet_url_bipartite_network = nx.DiGraph()



        ### But here we need to have a multi graph becasue a user can retweet/quote/reply to the other user at the same time
        self.user_level_retweet_network = nx.DiGraph()
        self.user_level_quote_network = nx.DiGraph()
        self.user_level_reply_network = nx.DiGraph()
        self.user_level_quote_reply_network = nx.MultiDiGraph()
        self.user_level_retweet_reply_network = nx.MultiDiGraph()
        self.user_level_retweet_quote_network = nx.MultiDiGraph()
        self.user_level_retweet_quote_reply_network = nx.MultiDiGraph()

        self.user_level_cooccurrence_hashtag_network = nx.Graph()
        self.user_level_cooccurrence_mention_network = nx.Graph()
        self.user_level_cooccurrence_url_network = nx.Graph()

        self.user_hashtag_bipartite_network = nx.DiGraph()
        self.user_mention_bipartite_network = nx.DiGraph()
        self.user_url_bipartite_network = nx.DiGraph()



        self.network_repository = []

        self.quote_reply_key_keepers = {}
        self.retweet_reply_key_keepers = {}
        self.retweet_quote_key_keepers = {}
        self.retweet_quote_reply_key_keepers = {}


        self.tweets_quotes_retweets = TwifexUtility.tweets_retweets_retweetedquotes_quotes(tweets)
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

    ### Tweet-level network
    # retweet/quote/reply networks
    def tweet_level_retweet_network_building(self):
        self.network_repository.append("tweet_level_retweet_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()

            if retweet_condition:
                self.tweet_level_retweet_network.add_edge(tweet.get_id(),
                                                          tweet.get_retweeted().get_id(), kind="retweet")
            else:
                self.tweet_level_retweet_network.add_node(tweet.get_id())

    def tweet_level_quote_network_building(self):
        self.network_repository.append("tweet_level_quote_network")
        for tweet_id, tweet in self.tweets.items():
            quote_condition = tweet.is_quote_available()

            if quote_condition:
                self.tweet_level_quote_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    self.tweet_level_quote_network.add_edge(tweet.get_quote().get_id(),
                                                            tweet.get_quote().get_quote_status_id(), kind="quote")
            else:
                self.tweet_level_quote_network.add_node(tweet.get_id())

    def tweet_level_reply_network_building(self):
        self.network_repository.append("tweet_level_reply_network")
        for tweet_id, tweet in self.tweets.items():
            reply_condition = tweet.is_this_a_reply()

            if reply_condition:
                self.tweet_level_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
            else:
                self.tweet_level_reply_network.add_node(tweet.get_id())

    # quote-reply/retweet-reply/retweet-quote networks
    def tweet_level_quote_reply_network_building(self):
        self.network_repository.append("tweet_level_quote_reply_network")
        for tweet_id, tweet in self.tweets.items():
            quote_condition = tweet.is_quote_available()
            reply_condition = tweet.is_this_a_reply()

            if quote_condition is True and reply_condition is True:
                self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="quote")
                inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_quote().is_quoted()
                if inner_reply_condition_level_one:
                    self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
                                                                  tweet.get_quote().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
                                                                  tweet.get_quote().get_quote_status_id(), kind="quote")

            elif quote_condition is True and reply_condition is False:
                self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                inner_reply_condition = tweet.get_quote().is_this_a_reply()
                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_reply_condition:
                    self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
                                                                  tweet.get_quote().get_reply_to_id(), kind="reply")
                if inner_quote_condition:
                    self.tweet_level_quote_reply_network.add_edge(tweet.get_quote().get_id(),
                                                                  tweet.get_quote().get_quote_status_id(), kind="quote")
            elif quote_condition is False and reply_condition is True:
                self.tweet_level_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
            elif quote_condition is False and reply_condition is False:
                self.tweet_level_quote_reply_network.add_node(tweet.get_id())

    def tweet_level_retweet_reply_network_building(self):
        self.network_repository.append("tweet_level_retweet_reply_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            reply_condition = tweet.is_this_a_reply()

            if retweet_condition is True and reply_condition is True:  #######This condition seems impossible to happen
                self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
                self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
                inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
                if inner_reply_condition:
                    self.tweet_level_retweet_reply_network.add_edge(tweet.get_retweeted().get_id(),
                                                                    tweet.get_retweeted().get_reply_to_id(), kind="reply")
            elif retweet_condition is True and reply_condition is False:
                self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
                inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
                if inner_reply_condition:
                    self.tweet_level_retweet_reply_network.add_edge(tweet.get_retweeted().get_id(),
                                                                    tweet.get_retweeted().get_reply_to_id(), kind="reply")
            elif retweet_condition is False and reply_condition is True:
                self.tweet_level_retweet_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
            elif retweet_condition is False and reply_condition is False:
                self.tweet_level_retweet_reply_network.add_node(tweet.get_id())

    def tweet_level_retweet_quote_network_building(self):
        self.network_repository.append("tweet_level_retweet_quote_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            quote_condition = tweet.is_quote_available()

            ####### if retweet_condition is True and quote_condition is True: #This condition seems impossible to happen
            if retweet_condition is True and quote_condition is False:
                self.tweet_level_retweet_quote_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
                if inner_quote_condition_level_one:
                    self.tweet_level_retweet_quote_network.add_edge(tweet.get_retweeted().get_id(),
                                                                    tweet.get_retweeted().get_quote().get_id(), kind="quote")
                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    if inner_quote_condition_level_two:
                        self.tweet_level_retweet_quote_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
                                         tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
            elif retweet_condition is False and quote_condition is True:
                self.tweet_level_retweet_quote_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    self.tweet_level_retweet_quote_network.add_edge(tweet.get_quote().get_id(),
                                                                    tweet.get_quote().get_quote_status_id(), kind="quote")
            elif retweet_condition is False and quote_condition is False:
                self.tweet_level_retweet_quote_network.add_node(tweet.get_id())

    # retweet-quote-reply network
    def tweet_level_retweet_quote_reply_network_building(self):
        self.network_repository.append("tweet_level_retweet_quote_reply_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            quote_condition = tweet.is_quote_available()
            reply_condition = tweet.is_this_a_reply()


            # The first two conditions never occur
            # if retweet_condition is True and quote_condition is True and reply_condition is True:
            # elif retweet_condition is True and quote_condition is True and reply_condition is False:
            if retweet_condition is True and quote_condition is False and reply_condition is True:  #######This condition seems impossible to happen
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
                inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
                if inner_reply_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_reply_to_id(),
                                     kind="reply")
                if inner_quote_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(),
                                     kind="quote")
                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
                    if inner_quote_condition_level_two:
                        self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
                                         tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
                    if inner_reply_condition_level_two:
                        self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
                                         tweet.get_retweeted().get_quote().get_reply_to_id(), kind="reply")

            elif retweet_condition is True and quote_condition is False and reply_condition is False:
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind="retweet")
                inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
                if inner_reply_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(), kind="quote")
                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()
                    if inner_quote_condition_level_two:
                        self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
                                         tweet.get_retweeted().get_quote().get_quote_status_id(), kind="quote")
                    if inner_reply_condition_level_two:
                        self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_retweeted().get_quote().get_id(),
                                         tweet.get_retweeted().get_quote().get_reply_to_id(), kind="reply")

            elif retweet_condition is False and quote_condition is True and reply_condition is True:
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
                inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_quote().is_quoted()
                if inner_reply_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_quote_status_id(), kind="quote")

            elif retweet_condition is False and quote_condition is True and reply_condition is False:
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind="quote")
                inner_reply_condition_level_one = tweet.get_quote().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_quote().is_quoted()
                if inner_reply_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_reply_to_id(), kind="reply")
                if inner_quote_condition_level_one:
                    self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_quote().get_id(), tweet.get_quote().get_quote_status_id(), kind="quote")

            elif retweet_condition is False and quote_condition is False and reply_condition is True:
                self.tweet_level_retweet_quote_reply_network.add_edge(tweet.get_id(), tweet.get_reply_to_id(), kind="reply")
            elif retweet_condition is False and quote_condition is False and reply_condition is False:
                self.tweet_level_retweet_quote_reply_network.add_node(tweet.get_id())

            # # if retweet_condition is True and quote_condition is True: #This condition seems impossible to happen
            # if retweet_condition is True and quote_condition is False:
            #     network.add_edge(tweet.get_id(), tweet.get_retweeted().get_id(), kind=network_type)
            #     inner_quote_condition = tweet.get_retweeted().is_quoted()
            #     if inner_quote_condition:
            #         network.add_edge(tweet.get_retweeted().get_id(), tweet.get_retweeted().get_quote().get_id(), kind=network_type)
            # elif retweet_condition is False and quote_condition is True:
            #     network.add_edge(tweet.get_id(), tweet.get_quote().get_id(), kind=network_type)
            # elif retweet_condition is False and quote_condition is False:
            #     network.add_node(tweet.get_id())

    # hashtag/mention/url networks
    def tweet_level_cooccurrence_hashtag_network_building(self):
        self.network_repository.append("tweet_level_cooccurrence_hashtag_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            tweet1_id = tweet1.get_id()
            tweet1_hashtags = tweet1.get_hashtags()

            j = i + 1

            self.tweet_level_cooccurrence_hashtag_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                tweet1_rt_id = tweet1_rt.get_id()

                for ht in tweet1_hashtags:
                    if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + ht
                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id]["hashtags"] += edge_label
                    else:
                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, hashtags=ht)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                    tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_rt_qt_hashtags:
                            if ht1 == ht2:
                                if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
                                                                              hashtags=ht1)

                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_rt_qt_hashtags:
                            if ht1 == ht2:
                                if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
                                                                              hashtags=ht1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                tweet1_qt_id = tweet1_qt.get_id()
                tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                for ht1 in tweet1_hashtags:
                    for ht2 in tweet1_qt_hashtags:
                        if ht1 == ht2:
                            if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
                                edge_label = "-" + ht1
                                self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id][
                                    "hashtags"] += edge_label
                            else:
                                self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
                                                                          hashtags=ht1)

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                tweet2_id = tweet2.get_id()
                tweet2_hashtags = tweet2.get_hashtags()

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()

                    if tweet1_id != tweet2_rt_id:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
                                                                                  hashtags=ht1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                            tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                            if tweet1_id != tweet2_rt_qt_id:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                                self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "hashtags"] += edge_label
                                            else:
                                                self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_rt_qt_id,
                                                                                          weight=1,
                                                                                          hashtags=ht1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1_id != tweet2_qt_id:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
                                                                                  hashtags=ht1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_hashtags = tweet1_rt.get_hashtags()

                    if tweet1_rt_id != tweet2_rt_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_rt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
                                                                                  hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
                                                                                      weight=1, hashtags=ht1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
                                                                                      weight=1, hashtags=ht1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
                                                                                      weight=1, hashtags=ht1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1_qt_id != tweet2_qt_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
                                                                                  hashtags=ht1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1_rt_id != tweet2_qt_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
                                                                                  hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
                                                                                      weight=1, hashtags=ht1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_hashtags = tweet2_rt.get_hashtags()

                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    if tweet1_qt_id != tweet2_rt_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_rt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
                                                                                  hashtags=ht1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
                                                                                      weight=1,
                                                                                      hashtags=ht1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    if tweet1_rt_id != tweet2_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_id, tweet2_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
                                                                                  hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet2_id != tweet1_rt_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_id,
                                                                                      weight=1,
                                                                                      hashtags=ht1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    if tweet1_qt_id != tweet2_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_qt_id, tweet2_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
                                                                                  hashtags=ht1)

                if tweet1_id != tweet2_id:
                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet2_hashtags:
                            if ht1 == ht2:
                                if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_hashtag_network.edges:
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_id, weight=1,
                                                                              hashtags=ht1)
                j += 1

    def tweet_level_cooccurrence_mention_network_building(self):
        self.network_repository.append("tweet_level_cooccurrence_mention_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            tweet1_id = tweet1.get_id()
            tweet1_mentions = tweet1.get_mentions()

            j = i + 1

            self.tweet_level_cooccurrence_mention_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                tweet1_rt_id = tweet1_rt.get_id()

                for mt in tweet1_mentions:
                    if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + mt
                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id]["mentions"] += edge_label
                    else:
                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, mentions=mt)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                    tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_rt_qt_mentions:
                            if mt1 == mt2:
                                if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + mt1
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "mentions"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
                                                                              mentions=mt1)

                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_rt_qt_mentions:
                            if mt1 == mt2:
                                if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + mt1
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                        "mentions"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
                                                                              mentions=mt1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                tweet1_qt_id = tweet1_qt.get_id()
                tweet1_qt_mentions = tweet1_qt.get_mentions()

                for mt1 in tweet1_mentions:
                    for mt2 in tweet1_qt_mentions:
                        if mt1 == mt2:
                            if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
                                edge_label = "-" + mt1
                                self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id][
                                    "mentions"] += edge_label
                            else:
                                self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
                                                                          mentions=mt1)

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                tweet2_id = tweet2.get_id()
                tweet2_mentions = tweet2.get_mentions()

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()

                    if tweet1_id != tweet2_rt_id:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
                                                                                  mentions=mt1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                            tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                            if tweet1_id != tweet2_rt_qt_id:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                                self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "mentions"] += edge_label
                                            else:
                                                self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_rt_qt_id,
                                                                                          weight=1,
                                                                                          mentions=mt1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1_id != tweet2_qt_id:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
                                                                                  mentions=mt1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_mentions = tweet1_rt.get_mentions()

                    if tweet1_rt_id != tweet2_rt_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_rt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
                                                                                  mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
                                                                                      weight=1, mentions=mt1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
                                                                                      weight=1, mentions=mt1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
                                                                                      weight=1, mentions=mt1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1_qt_id != tweet2_qt_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
                                                                                  mentions=mt1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1_rt_id != tweet2_qt_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
                                                                                  mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
                                                                                      weight=1, mentions=mt1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_mentions = tweet2_rt.get_mentions()

                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    if tweet1_qt_id != tweet2_rt_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_rt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
                                                                                  mentions=mt1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
                                                                                      weight=1,
                                                                                      mentions=mt1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    if tweet1_rt_id != tweet2_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_id, tweet2_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
                                                                                  mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet2_id != tweet1_rt_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            self.tweet_level_cooccurrence_mention_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "mentions"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id, tweet2_id,
                                                                                      weight=1,
                                                                                      mentions=mt1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    if tweet1_qt_id != tweet2_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.tweet_level_cooccurrence_mention_network.edges[tweet1_qt_id, tweet2_id][
                                            "mentions"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
                                                                                  mentions=mt1)

                if tweet1_id != tweet2_id:
                    for mt1 in tweet1_mentions:
                        for mt2 in tweet2_mentions:
                            if mt1 == mt2:
                                if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_mention_network.edges:
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id]["weight"] += 1
                                    edge_label = "-" + mt1
                                    self.tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id][
                                        "mentions"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_id, weight=1,
                                                                              mentions=mt1)
                j += 1

    def tweet_level_cooccurrence_url_network_building(self):
        self.network_repository.append("tweet_level_cooccurrence_url_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            tweet1_id = tweet1.get_id()
            tweet1_urls = tweet1.get_tweet_urls(return_format="expanded_url")

            j = i + 1

            self.tweet_level_cooccurrence_url_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                tweet1_rt_id = tweet1_rt.get_id()

                for ut in tweet1_urls:
                    if (tweet1_id, tweet1_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + ut
                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id]["urls"] += edge_label
                    else:
                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, urls=ut)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                    tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_rt_qt_urls:
                            if ut1 == ut2:
                                if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + ut1
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "urls"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
                                                                          urls=ut1)

                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_rt_qt_urls:
                            if ut1 == ut2:
                                if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + ut1
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                        "urls"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
                                                                          urls=ut1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                tweet1_qt_id = tweet1_qt.get_id()
                tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                for ut1 in tweet1_urls:
                    for ut2 in tweet1_qt_urls:
                        if ut1 == ut2:
                            if (tweet1_id, tweet1_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
                                edge_label = "-" + ut1
                                self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id][
                                    "urls"] += edge_label
                            else:
                                self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
                                                                      urls=ut1)

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                tweet2_id = tweet2.get_id()
                tweet2_urls = tweet2.get_tweet_urls(return_format="expanded_url")

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()

                    if tweet1_id != tweet2_rt_id:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
                                                                              urls=ut1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                            tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                            if tweet1_id != tweet2_rt_qt_id:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                                self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + ut1
                                                self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                    "urls"] += edge_label
                                            else:
                                                self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_rt_qt_id,
                                                                                      weight=1,
                                                                                      urls=ut1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_id != tweet2_qt_id:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (tweet1_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
                                                                              urls=ut1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_rt_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_rt_urls:
                                if ut1 == ut2:
                                    if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
                                                                              urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
                                                                                  weight=1, urls=ut1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
                                                                                  weight=1, urls=ut1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
                                                                                  weight=1, urls=ut1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_qt_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
                                                                              urls=ut1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_id()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote()
                    tweet2_qt_id = tweet2_qt.get_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_qt_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
                                                                              urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
                                                                                  weight=1, urls=ut1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    tweet2_rt_id = tweet2_rt.get_id()
                    tweet2_rt_urls = tweet2_rt.get_tweet_urls(return_format="expanded_url")

                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_rt_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_rt_urls:
                                if ut1 == ut2:
                                    if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
                                                                              urls=ut1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
                                                                                  weight=1,
                                                                                  urls=ut1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    tweet1_rt_id = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_rt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
                                                                              urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet2_id != tweet1_rt_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            self.tweet_level_cooccurrence_url_network.edges[tweet1_rt_qt_id, tweet2_id][
                                                "urls"] += edge_label
                                        else:
                                            self.tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id, tweet2_id,
                                                                                  weight=1,
                                                                                  urls=ut1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    tweet1_qt_id = tweet1_qt.get_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_qt_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id][
                                            "urls"] += edge_label
                                    else:
                                        self.tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
                                                                              urls=ut1)

                if tweet1_id != tweet2_id:
                    for ut1 in tweet1_urls:
                        for ut2 in tweet2_urls:
                            if ut1 == ut2:
                                if (tweet1_id, tweet2_id) in self.tweet_level_cooccurrence_url_network.edges:
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id]["weight"] += 1
                                    edge_label = "-" + ut1
                                    self.tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id][
                                        "urls"] += edge_label
                                else:
                                    self.tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_id, weight=1,
                                                                          urls=ut1)
                j += 1

    # bipartite version of tweet-level hashtag/mention/url networks
    def tweet_hashtag_bipartite_network_building(self):
        self.network_repository.append("tweet_hashtag_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_id()
            hashtag_list = tweet.get_hashtags()

            for hashtag in hashtag_list:
                if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                    self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                    self.tweet_hashtag_bipartite_network.edges[source, hashtag][
                        "shared_author"] += tweet.get_twitter().get_screen_name()
                else:
                    self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                        shared_author=tweet.get_twitter().get_screen_name())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_id()
                hashtag_list = tweet.get_hashtags()
                for hashtag in hashtag_list:

                    if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                        self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        self.tweet_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
                    else:
                        self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                            shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_id()
                    hashtag_list = tweet.get_retweeted().get_quote().get_hashtags()
                    for hashtag in hashtag_list:

                        if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                            self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                            self.tweet_hashtag_bipartite_network.edges[source, hashtag][
                                "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                        else:
                            self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_id()
                hashtag_list = tweet.get_quote().get_hashtags()
                for hashtag in hashtag_list:

                    if self.tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                        self.tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        self.tweet_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
                    else:
                        self.tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                            shared_author=tweet.get_quote().get_twitter().get_screen_name())

    def tweet_mention_bipartite_network_building(self):
        self.network_repository.append("tweet_mention_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_id()
            mention_list = tweet.get_mentions()

            for mention in mention_list:
                if self.tweet_mention_bipartite_network.has_edge(source, mention):
                    self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                    self.tweet_mention_bipartite_network.edges[source, mention]["shared_author"] += tweet.get_twitter().get_screen_name()
                else:
                    self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                       shared_author=tweet.get_twitter().get_screen_name())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_id()
                mention_list = tweet.get_mentions()
                for mention in mention_list:

                    if self.tweet_mention_bipartite_network.has_edge(source, mention):
                        self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        self.tweet_mention_bipartite_network.edges[source, mention][
                            "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
                    else:
                        self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                           shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_id()
                    mention_list = tweet.get_retweeted().get_quote().get_mentions()
                    for mention in mention_list:

                        if self.tweet_mention_bipartite_network.has_edge(source, mention):
                            self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                            self.tweet_mention_bipartite_network.edges[source, mention][
                                "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                        else:
                            self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                               shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_id()
                mention_list = tweet.get_quote().get_mentions()
                for mention in mention_list:

                    if self.tweet_mention_bipartite_network.has_edge(source, mention):
                        self.tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        self.tweet_mention_bipartite_network.edges[source, mention][
                            "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
                    else:
                        self.tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                           shared_author=tweet.get_quote().get_twitter().get_screen_name())

    def tweet_url_bipartite_network_building(self):
        self.network_repository.append("tweet_url_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_id()
            url_list = tweet.get_tweet_urls(return_format="expanded_url")

            for url in url_list:
                if self.tweet_url_bipartite_network.has_edge(source, url):
                    self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                    self.tweet_url_bipartite_network.edges[source, url]["shared_author"] += tweet.get_twitter().get_screen_name()
                else:
                    self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                    shared_author=tweet.get_twitter().get_screen_name())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_id()
                url_list = tweet.get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if self.tweet_url_bipartite_network.has_edge(source, url):
                        self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                        self.tweet_url_bipartite_network.edges[source, url][
                            "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
                    else:
                        self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                        shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_id()
                    url_list = tweet.get_retweeted().get_quote().get_tweet_urls(return_format="expanded_url")
                    for url in url_list:

                        if self.tweet_url_bipartite_network.has_edge(source, url):
                            self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                            self.tweet_url_bipartite_network.edges[source, url][
                                "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                        else:
                            self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                            shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_id()
                url_list = tweet.get_quote().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if self.tweet_url_bipartite_network.has_edge(source, url):
                        self.tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                        self.tweet_url_bipartite_network.edges[source, url][
                            "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
                    else:
                        self.tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                        shared_author=tweet.get_quote().get_twitter().get_screen_name())
    ####################################################################

    ### User-level network
    # retweet/quote/reply networks
    def user_level_retweet_network_building(self):
        self.network_repository.append("user_level_retweet_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            source = tweet.get_twitter().get_screen_name()
            if retweet_condition:
                destination = tweet.get_retweeted().get_twitter().get_screen_name()
                if self.user_level_retweet_network.has_edge(source, destination):
                    self.user_level_retweet_network.edges[source, destination]["weight"] += 1
                else:
                    self.user_level_retweet_network.add_edge(source, destination, kind="retweet", weight=1)
            else:
                self.user_level_retweet_network.add_node(source)

    def user_level_quote_network_building(self):
        self.network_repository.append("user_level_quote_network")
        for tweet_id, tweet in self.tweets.items():
            quote_condition = tweet.is_quote_available()

            source = tweet.get_twitter().get_screen_name()
            if quote_condition:
                destination = tweet.get_quote().get_twitter().get_screen_name()
                if self.user_level_quote_network.has_edge(source, destination):
                    self.user_level_quote_network.edges[source, destination]["weight"] += 1
                else:
                    self.user_level_quote_network.add_edge(source, destination, kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote().get_twitter().get_screen_name()
                    inner_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if self.user_level_quote_network.has_edge(inner_source, inner_destination):
                        self.user_level_quote_network.edges[inner_source, inner_destination]["weight"] += 1
                    else:
                        self.user_level_quote_network.add_edge(inner_source, inner_destination, kind="quote", weight=1)
            else:
                self.user_level_quote_network.add_node(source)

    def user_level_reply_network_building(self):
        self.network_repository.append("user_level_reply_network")
        for tweet_id, tweet in self.tweets.items():
            reply_condition = tweet.is_this_a_reply()

            source = tweet.get_twitter().get_screen_name()
            if reply_condition:
                destination = tweet.get_in_reply_to_screen_name()
                if self.user_level_reply_network.has_edge(source, destination):
                    self.user_level_reply_network.edges[source, destination]["weight"] += 1
                else:
                    self.user_level_reply_network.add_edge(source, destination, kind="reply", weight=1)
            else:
                self.user_level_reply_network.add_node(source)

    # quote-reply/retweet-reply/retweet-quote networks
    def user_level_quote_reply_network_building(self):
        self.network_repository.append("user_level_quote_reply_network")
        for tweet_id, tweet in self.tweets.items():
            quote_condition = tweet.is_quote_available()
            reply_condition = tweet.is_this_a_reply()

            key_code = 0
            source = tweet.get_twitter().get_screen_name()

            if quote_condition is True and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                quote_destination = tweet.get_quote().get_twitter().get_screen_name()

                # key_code = 0
                if (source, quote_destination, "quote") in self.quote_reply_key_keepers.keys():
                    self.user_level_quote_reply_network.edges[source, quote_destination, self.quote_reply_key_keepers[
                        (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    self.quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    self.user_level_quote_reply_network.add_edge(source, quote_destination, key=self.quote_reply_key_keepers[
                        (source, quote_destination, "quote")], kind="quote", weight=1)

                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.quote_reply_key_keepers.keys():
                    self.user_level_quote_reply_network.edges[
                        source, reply_destination, self.quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_quote_reply_network.add_edge(source, reply_destination, key=self.quote_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote().get_twitter().get_screen_name()
                    inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (
                            inner_source, inner_quote_destination, "quote") in self.quote_reply_key_keepers.keys():
                        self.user_level_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)
                    inner_reply_condition = tweet.get_quote().is_this_a_reply()
                    if inner_reply_condition:
                        inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.quote_reply_key_keepers.keys():
                            self.user_level_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, network_type)]][
                                "weight"] += 1
                        else:
                            self.quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)

            elif quote_condition is True and reply_condition is False:
                # source = tweet.get_twitter().get_screen_name()
                quote_destination = tweet.get_quote().get_twitter().get_screen_name()

                # key_code = 0
                if (source, quote_destination, "quote") in self.quote_reply_key_keepers.keys():
                    self.user_level_quote_reply_network.edges[source, quote_destination, self.quote_reply_key_keepers[
                        (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    self.quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    self.user_level_quote_reply_network.add_edge(source, quote_destination, key=self.quote_reply_key_keepers[
                        (source, quote_destination, "quote")], kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote().get_twitter().get_screen_name()
                    inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (inner_source, inner_quote_destination, "quote") in self.quote_reply_key_keepers.keys():
                        self.user_level_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)
                    inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
                    if inner_reply_destination:
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.quote_reply_key_keepers.keys():
                            self.user_level_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            self.quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)

            elif quote_condition is False and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.quote_reply_key_keepers.keys():
                    self.user_level_quote_reply_network.edges[
                        source, reply_destination, self.quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_quote_reply_network.add_edge(source, reply_destination, key=self.quote_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

            elif quote_condition is False and reply_condition is False:
                self.user_level_quote_reply_network.add_node(source)

    def user_level_retweet_reply_network_building(self):
        self.network_repository.append("user_level_retweet_reply_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            reply_condition = tweet.is_this_a_reply()

            key_code = 0
            source = tweet.get_twitter().get_screen_name()

            if retweet_condition is True and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()

                if (source, retweet_destination, "retweet") in self.retweet_reply_key_keepers.keys():
                    self.user_level_retweet_reply_network.edges[source, retweet_destination, self.retweet_reply_key_keepers[
                        (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    self.retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    self.user_level_retweet_reply_network.add_edge(source, retweet_destination, key=self.retweet_reply_key_keepers[
                        (source, retweet_destination, "retweet")], kind="retweet", weight=1)

                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.retweet_reply_key_keepers.keys():
                    self.user_level_retweet_reply_network.edges[
                        source, reply_destination, self.retweet_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_retweet_reply_network.add_edge(source, reply_destination, key=self.retweet_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

                inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
                if inner_reply_condition:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in self.retweet_reply_key_keepers.keys():
                        self.user_level_retweet_reply_network.edges[
                            inner_source, inner_reply_destination, self.retweet_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        self.retweet_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        self.user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
                                               key=self.retweet_reply_key_keepers[
                                                   (inner_source, inner_reply_destination, "reply")],
                                               kind="reply", weight=1)

            elif retweet_condition is True and reply_condition is False:
                # source = tweet.get_twitter().get_screen_name()
                retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()

                if (source, retweet_destination, "retweet") in self.retweet_reply_key_keepers.keys():
                    self.user_level_retweet_reply_network.edges[source, retweet_destination, self.retweet_reply_key_keepers[
                        (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    self.retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    self.user_level_retweet_reply_network.add_edge(source, retweet_destination, key=self.retweet_reply_key_keepers[
                        (source, retweet_destination, "retweet")], kind="retweet", weight=1)

                inner_reply_condition = tweet.get_retweeted().is_this_a_reply()
                if inner_reply_condition:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in self.retweet_reply_key_keepers.keys():
                        self.user_level_retweet_reply_network.edges[
                            inner_source, inner_reply_destination, self.retweet_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        self.retweet_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        self.user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
                                               key=self.retweet_reply_key_keepers[
                                                   (inner_source, inner_reply_destination, "reply")],
                                               kind="reply", weight=1)

            elif retweet_condition is False and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.retweet_reply_key_keepers.keys():
                    self.user_level_retweet_reply_network.edges[
                        source, reply_destination, self.retweet_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_retweet_reply_network.add_edge(source, reply_destination, key=self.retweet_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

            elif retweet_condition is False and reply_condition is False:
                self.user_level_retweet_reply_network.add_node(source)

    def user_level_retweet_quote_network_building(self):
        self.network_repository.append("user_level_retweet_quote_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            quote_condition = tweet.is_quote_available()

            key_code = 0
            source = tweet.get_twitter().get_screen_name()
            # if retweet_condition is True and quote_condition is True: #Not possible
            if retweet_condition is True and quote_condition is False:
                # source = tweet.get_twitter().get_screen_name()
                retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()

                if (source, retweet_destination, "retweet") in self.retweet_quote_key_keepers.keys():
                    self.user_level_retweet_quote_network.edges[source, retweet_destination, self.retweet_quote_key_keepers[
                        (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    self.retweet_quote_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_network.add_edge(source, retweet_destination, key=self.retweet_quote_key_keepers[
                        (source, retweet_destination, "retweet")], kind="retweet", weight=1)

                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    # inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (inner_source, inner_quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
                        self.user_level_retweet_quote_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    if inner_quote_condition_level_two:
                        inner_source_level_two = inner_quote_destination
                        inner_quote_destination_level_two = tweet.get_quote().get_inner_quote_screen_name()
                        if (inner_source_level_two, inner_quote_destination_level_two,
                            "quote") in self.retweet_quote_key_keepers.keys():
                            self.user_level_retweet_quote_network.edges[
                                inner_source_level_two, inner_quote_destination_level_two,
                                self.retweet_quote_key_keepers[
                                    (inner_source_level_two, inner_quote_destination_level_two, "quote")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_key_keepers[
                                (inner_source_level_two, inner_quote_destination_level_two, "quote")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_network.add_edge(inner_source_level_two, inner_quote_destination_level_two,
                                                   key=self.retweet_quote_key_keepers[
                                                       (inner_source_level_two, inner_quote_destination_level_two,
                                                        "quote")],
                                                   kind="quote", weight=1)

            elif retweet_condition is False and quote_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                quote_destination = tweet.get_quote().get_twitter().get_screen_name()

                # key_code = 0
                if (source, quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
                    self.user_level_retweet_quote_network.edges[source, quote_destination, self.retweet_quote_key_keepers[
                        (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    self.retweet_quote_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_network.add_edge(source, quote_destination, key=self.retweet_quote_key_keepers[
                        (source, quote_destination, "quote")], kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (inner_source, inner_quote_destination, "quote") in self.retweet_quote_key_keepers.keys():
                        self.user_level_retweet_quote_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)

            elif retweet_condition is False and quote_condition is False:
                self.user_level_retweet_quote_network.add_node(source)

    # retweet-quote-reply network
    def user_level_retweet_quote_reply_network_building(self):
        self.network_repository.append("user_level_retweet_quote_reply_network")
        for tweet_id, tweet in self.tweets.items():
            retweet_condition = tweet.is_retweeted()
            quote_condition = tweet.is_quote_available()
            reply_condition = tweet.is_this_a_reply()

            key_code = 0
            source = tweet.get_twitter().get_screen_name()

            if retweet_condition is True and quote_condition is False and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()

                if (source, retweet_destination, "retweet") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[source, retweet_destination, self.retweet_quote_reply_key_keepers[
                        (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, retweet_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, retweet_destination, "retweet")], kind="retweet", weight=1)

                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, self.retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

                inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()

                if inner_reply_condition_level_one:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_reply_destination, "reply")],
                                               kind="reply", weight=1)
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()

                    if inner_reply_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_reply_destination = tweet.get_retweeted().get_quote().get_in_reply_to_screen_name()

                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)
                    if inner_quote_condition_level_two:
                        inner_source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                        inner_quote_destination = inner_quote_destination
                        if (
                                inner_source, inner_quote_destination,
                                "quote") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                    (source, inner_quote_destination, "quote")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_quote_destination, "quote")],
                                                   kind="quote", weight=1)
            elif retweet_condition is True and quote_condition is False and reply_condition is False:
                # source = tweet.get_twitter().get_screen_name()
                retweet_destination = tweet.get_retweeted().get_twitter().get_screen_name()

                if (source, retweet_destination, "retweet") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[source, retweet_destination, self.retweet_quote_reply_key_keepers[
                        (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, retweet_destination,
                                           key=self.retweet_quote_reply_key_keepers[
                                               (source, retweet_destination, "retweet")], kind="retweet",
                                           weight=1)

                inner_reply_condition_level_one = tweet.get_retweeted().is_this_a_reply()
                inner_quote_condition_level_one = tweet.get_retweeted().is_quote_available()

                if inner_reply_condition_level_one:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_retweeted().get_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_reply_destination, "reply")],
                                               kind="reply", weight=1)
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_retweeted().get_quote().is_quoted()
                    inner_reply_condition_level_two = tweet.get_retweeted().get_quote().is_this_a_reply()

                    if inner_reply_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_reply_destination = tweet.get_retweeted().get_quote().get_in_reply_to_screen_name()

                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)
                    if inner_quote_condition_level_two:
                        inner_source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                        inner_quote_destination = inner_quote_destination
                        if (
                                inner_source, inner_quote_destination,
                                "quote") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                    (source, inner_quote_destination, "quote")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_quote_destination, "quote")],
                                                   kind="quote", weight=1)
            elif retweet_condition is False and quote_condition is True and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                quote_destination = tweet.get_quote().get_twitter().get_screen_name()

                # key_code = 0
                if (source, quote_destination, "quote") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[source, quote_destination, self.retweet_quote_reply_key_keepers[
                        (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, quote_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, quote_destination, "quote")], kind="quote", weight=1)

                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, self.retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)
                    inner_reply_condition = tweet.get_quote().is_this_a_reply()
                    if inner_reply_condition:
                        inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is True and reply_condition is False:
                # source = tweet.get_twitter().get_screen_name()
                quote_destination = tweet.get_quote().get_twitter().get_screen_name()

                # key_code = 0
                if (source, quote_destination, "quote") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[source, quote_destination, self.retweet_quote_reply_key_keepers[
                        (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, quote_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, quote_destination, "quote")], kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote().is_quoted()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote().get_inner_quote_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in self.retweet_quote_reply_key_keepers.keys():
                        self.user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        self.retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                               key=self.retweet_quote_reply_key_keepers[
                                                   (inner_source, inner_quote_destination, "quote")],
                                               kind="quote", weight=1)
                    inner_reply_condition = tweet.get_quote().is_this_a_reply()
                    if inner_reply_condition:
                        inner_reply_destination = tweet.get_quote().get_in_reply_to_screen_name()
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in self.retweet_quote_reply_key_keepers.keys():
                            self.user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, self.retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            self.retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            self.user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                   key=self.retweet_quote_reply_key_keepers[
                                                       (inner_source, inner_reply_destination, "reply")],
                                                   kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is False and reply_condition is True:
                # source = tweet.get_twitter().get_screen_name()
                reply_destination = tweet.get_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in self.retweet_quote_reply_key_keepers.keys():
                    self.user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, self.retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    self.retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    self.user_level_retweet_quote_reply_network.add_edge(source, reply_destination, key=self.retweet_quote_reply_key_keepers[
                        (source, reply_destination, "reply")], kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is False and reply_condition is False:
                self.user_level_retweet_quote_reply_network.add_node(source)

    # user-level co-occurence hashtag/mention/url networks
    def user_level_cooccurrence_hashtag_network_building(self):  # Thinking of pruning hashtags      #also adding tweet_ids as a feature instead of deleting them (convert them to a a string)
        self.network_repository.append("user_level_cooccurrence_hashtag_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            user1 = tweet1.get_twitter().get_screen_name()
            tweet1_hashtags = tweet1.get_hashtags()

            j = i + 1

            self.user_level_cooccurrence_hashtag_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                user1_rt = tweet1_rt.get_twitter().get_screen_name()

                if (user1, user1_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                    if (tweet1.get_id(), tweet1_rt.get_id()) not in \
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt][
                                "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"]:
                        for ht in tweet1_hashtags:
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ht
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["hashtags"] += edge_label
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                else:
                    for ht in tweet1_hashtags:
                        if (user1, user1_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ht
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["hashtags"] += edge_label
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                        else:
                            self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt, weight=1, hashtags=ht,
                                                                     tweets=[(tweet1.get_id(), tweet1_rt.get_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                    tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] and (
                                tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet1_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_rt_qt_hashtags:
                                if ht1 == ht2:
                                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt_qt, weight=1,
                                                                                 hashtags=ht1,
                                                                                 tweets=[(tweet1.get_id(),
                                                                                          tweet1_rt_qt.get_id())])

                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
                                tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet1_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_rt_qt_hashtags:
                                if ht1 == ht2:
                                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user1_rt_qt, weight=1,
                                                                                 hashtags=ht1, tweets=[
                                                (tweet1_rt.get_id(), tweet1_rt_qt.get_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                user1_qt = tweet1_qt.get_twitter().get_screen_name()
                tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                    if (tweet1.get_id(), tweet1_qt.get_id()) not in \
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"]:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_qt_hashtags:
                                if ht1 == ht2:
                                    # if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["hashtags"] += edge_label
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                else:
                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_qt_hashtags:
                            if ht1 == ht2:
                                if (user1, user1_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["hashtags"] += edge_label
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                                else:
                                    self.user_level_cooccurrence_hashtag_network.add_edge(user1, user1_qt, weight=1, hashtags=ht1,
                                                                             tweets=[
                                                                                 (tweet1.get_id(), tweet1_qt.get_id())])

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                user2 = tweet2.get_twitter().get_screen_name()
                tweet2_hashtags = tweet2.get_hashtags()

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()

                    if tweet1.get_id() != tweet2_rt.get_id():
                        if (user1, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"]:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                        else:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_rt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1.get_id(), tweet2_rt.get_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                            tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                            if tweet1.get_id() != tweet2_rt_qt.get_id():
                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                    if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt]["tweets"] and (
                                            tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt]["tweets"]:
                                        for ht1 in tweet1_hashtags:
                                            for ht2 in tweet2_rt_qt_hashtags:
                                                if ht1 == ht2:
                                                    # if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "tweets"] += [(tweet1.get_id(), tweet2_rt_qt.get_id())]
                                else:
                                    for ht1 in tweet1_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_rt_qt,
                                                                                             weight=1,
                                                                                             hashtags=ht1, tweets=[
                                                            (tweet1.get_id(), tweet2_rt_qt.get_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1.get_id() != tweet2_qt.get_id():
                        if (user1, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"]:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                        else:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (user1, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2_qt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1.get_id(), tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_hashtags = tweet1_rt.get_hashtags()

                    if tweet1_rt.get_id() != tweet2_rt.get_id():
                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_rt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2_rt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
                                        tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt]["tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_rt,
                                                                                         weight=1,
                                                                                         hashtags=ht1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt]["tweets"]:
                                    for ht1 in tweet1_rt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_rt_qt,
                                                                                         weight=1,
                                                                                         hashtags=ht1, tweets=[
                                                        (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_rt_qt,
                                                                                             weight=1, hashtags=ht1,
                                                                                             tweets=[
                                                                                                 (tweet1_rt_qt.get_id(),
                                                                                                  tweet2_rt_qt.get_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1_qt.get_id() != tweet2_qt.get_id():
                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            # if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_qt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2_qt.get_id())])
                                    # else:
                                    #     self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_qt, weight=1, hashtags=ht1, tweets=[(tweet1_qt.get_id(), tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_hashtags()

                    if tweet1_rt.get_id() != tweet2_qt.get_id():
                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2_qt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2_qt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
                                        tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt]["tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_qt_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2_qt,
                                                                                         weight=1,
                                                                                         hashtags=ht1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2_qt.get_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_hashtags = tweet2_rt.get_hashtags()

                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    if tweet1_qt.get_id() != tweet2_rt.get_id():
                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_rt, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2_rt.get_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                        if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt]["tweets"]:
                                    for ht1 in tweet1_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_hashtag_network.edges:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_rt_qt,
                                                                                         weight=1,
                                                                                         hashtags=ht1, tweets=[
                                                        (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_hashtags()

                    if tweet1_rt.get_id() != tweet2.get_id():
                        if (user1_rt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1_rt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                        if tweet1_rt_qt.get_id() != tweet2.get_id():
                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] and (
                                        tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_hashtags:
                                            if ht1 == ht2:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ht1
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
                                                    "hashtags"] += edge_label
                                                self.user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                                            else:
                                                self.user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt, user2, weight=1,
                                                                                         hashtags=ht1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2.get_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_hashtags()

                    if tweet1_qt.get_id() != tweet2.get_id():
                        if (user1_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1_qt, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + ht1
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "hashtags"] += edge_label
                                            self.user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2, weight=1,
                                                                                     hashtags=ht1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2.get_id())])

                if tweet1.get_id() != tweet2.get_id():
                    if (user1, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1.get_id(), tweet2.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                    "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (user1, user2) in self.user_level_cooccurrence_hashtag_network.edges:
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ht1
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["hashtags"] += edge_label
                                        self.user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                                    else:
                                        self.user_level_cooccurrence_hashtag_network.add_edge(user1, user2, weight=1, hashtags=ht1,
                                                                                 tweets=[
                                                                                     (
                                                                                     tweet1.get_id(), tweet2.get_id())])
                j += 1

        for edge in self.user_level_cooccurrence_hashtag_network.edges:
            del self.user_level_cooccurrence_hashtag_network.edges[edge]["tweets"]

    def user_level_cooccurrence_mention_network_building(self):
        self.network_repository.append("user_level_cooccurrence_mention_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            user1 = tweet1.get_twitter().get_screen_name()
            tweet1_mentions = tweet1.get_mentions()

            j = i + 1

            self.user_level_cooccurrence_mention_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                user1_rt = tweet1_rt.get_twitter().get_screen_name()

                if (user1, user1_rt) in self.user_level_cooccurrence_mention_network.edges:
                    if (tweet1.get_id(), tweet1_rt.get_id()) not in \
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt][
                                "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"]:
                        for mt in tweet1_mentions:
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + mt
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["mentions"] += edge_label
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                else:
                    for mt in tweet1_mentions:
                        if (user1, user1_rt) in self.user_level_cooccurrence_mention_network.edges:
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + mt
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["mentions"] += edge_label
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                        else:
                            self.user_level_cooccurrence_mention_network.add_edge(user1, user1_rt, weight=1, mentions=mt,
                                                                     tweets=[(tweet1.get_id(), tweet1_rt.get_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                    tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                        if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] and (
                                tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet1_rt_qt_mentions:
                                    if mt1 == mt2:
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_rt_qt_mentions:
                                if mt1 == mt2:
                                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_mention_network.add_edge(user1, user1_rt_qt, weight=1,
                                                                                 mentions=mt1,
                                                                                 tweets=[(tweet1.get_id(),
                                                                                          tweet1_rt_qt.get_id())])

                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                        if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
                                tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet1_rt_qt_mentions:
                                    if mt1 == mt2:
                                        # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_rt_qt_mentions:
                                if mt1 == mt2:
                                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user1_rt_qt, weight=1,
                                                                                 mentions=mt1, tweets=[
                                                (tweet1_rt.get_id(), tweet1_rt_qt.get_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                user1_qt = tweet1_qt.get_twitter().get_screen_name()
                tweet1_qt_mentions = tweet1_qt.get_mentions()

                if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
                    if (tweet1.get_id(), tweet1_qt.get_id()) not in \
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"]:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_qt_mentions:
                                if mt1 == mt2:
                                    # if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + mt1
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["mentions"] += edge_label
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                else:
                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_qt_mentions:
                            if mt1 == mt2:
                                if (user1, user1_qt) in self.user_level_cooccurrence_mention_network.edges:
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + mt1
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["mentions"] += edge_label
                                    self.user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                                else:
                                    self.user_level_cooccurrence_mention_network.add_edge(user1, user1_qt, weight=1, mentions=mt1,
                                                                             tweets=[
                                                                                 (tweet1.get_id(), tweet1_qt.get_id())])

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                user2 = tweet2.get_twitter().get_screen_name()
                tweet2_mentions = tweet2.get_mentions()

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()

                    if tweet1.get_id() != tweet2_rt.get_id():
                        if (user1, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"]:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                        else:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1, user2_rt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1.get_id(), tweet2_rt.get_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                            tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                            if tweet1.get_id() != tweet2_rt_qt.get_id():
                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                    if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt]["tweets"] and (
                                            tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt]["tweets"]:
                                        for mt1 in tweet1_mentions:
                                            for mt2 in tweet2_rt_qt_mentions:
                                                if mt1 == mt2:
                                                    # if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "tweets"] += [(tweet1.get_id(), tweet2_rt_qt.get_id())]
                                else:
                                    for mt1 in tweet1_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_mention_network.add_edge(user1, user2_rt_qt,
                                                                                             weight=1,
                                                                                             mentions=mt1, tweets=[
                                                            (tweet1.get_id(), tweet2_rt_qt.get_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1.get_id() != tweet2_qt.get_id():
                        if (user1, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"]:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                        else:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (user1, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1, user2_qt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1.get_id(), tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_mentions = tweet1_rt.get_mentions()

                    if tweet1_rt.get_id() != tweet2_rt.get_id():
                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_rt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2_rt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
                                        tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt]["tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_rt,
                                                                                         weight=1,
                                                                                         mentions=mt1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt]["tweets"]:
                                    for mt1 in tweet1_rt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_rt_qt,
                                                                                         weight=1,
                                                                                         mentions=mt1, tweets=[
                                                        (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_rt_qt,
                                                                                             weight=1, mentions=mt1,
                                                                                             tweets=[
                                                                                                 (tweet1_rt_qt.get_id(),
                                                                                                  tweet2_rt_qt.get_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1_qt.get_id() != tweet2_qt.get_id():
                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            # if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_qt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_mentions()

                    if tweet1_rt.get_id() != tweet2_qt.get_id():
                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2_qt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2_qt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
                                        tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt]["tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_qt_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2_qt,
                                                                                         weight=1,
                                                                                         mentions=mt1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2_qt.get_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_mentions = tweet2_rt.get_mentions()

                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    if tweet1_qt.get_id() != tweet2_rt.get_id():
                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_rt, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2_rt.get_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_mentions()

                        if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt]["tweets"]:
                                    for mt1 in tweet1_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_mention_network.edges:
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2_rt_qt,
                                                                                         weight=1,
                                                                                         mentions=mt1, tweets=[
                                                        (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_mentions()

                    if tweet1_rt.get_id() != tweet2.get_id():
                        if (user1_rt, user2) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1_rt, user2) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_rt, user2, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_rt.get_id(), tweet2.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_mentions()

                        if tweet1_rt_qt.get_id() != tweet2.get_id():
                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] and (
                                        tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_mentions:
                                            if mt1 == mt2:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + mt1
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
                                                    "mentions"] += edge_label
                                                self.user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                                            else:
                                                self.user_level_cooccurrence_mention_network.add_edge(user1_rt_qt, user2, weight=1,
                                                                                         mentions=mt1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2.get_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_mentions()

                    if tweet1_qt.get_id() != tweet2.get_id():
                        if (user1_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1_qt, user2) in self.user_level_cooccurrence_mention_network.edges:
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + mt1
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "mentions"] += edge_label
                                            self.user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_mention_network.add_edge(user1_qt, user2, weight=1,
                                                                                     mentions=mt1, tweets=[
                                                    (tweet1_qt.get_id(), tweet2.get_id())])

                if tweet1.get_id() != tweet2.get_id():
                    if (user1, user2) in self.user_level_cooccurrence_mention_network.edges:
                        if (tweet1.get_id(), tweet2.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1, user2][
                                    "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (user1, user2) in self.user_level_cooccurrence_mention_network.edges:
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + mt1
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["mentions"] += edge_label
                                        self.user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                                    else:
                                        self.user_level_cooccurrence_mention_network.add_edge(user1, user2, weight=1, mentions=mt1,
                                                                                 tweets=[
                                                                                     (
                                                                                     tweet1.get_id(), tweet2.get_id())])
                j += 1

        for edge in self.user_level_cooccurrence_mention_network.edges:
            del self.user_level_cooccurrence_mention_network.edges[edge]["tweets"]

    def user_level_cooccurrence_url_network_building(self):
        self.network_repository.append("user_level_cooccurrence_url_network")

        tweets_keys = list(self.tweets.keys())
        for i in range(len(tweets_keys)):
            tweet1 = self.tweets[tweets_keys[i]]
            user1 = tweet1.get_twitter().get_screen_name()
            tweet1_urls = tweet1.get_tweet_urls(return_format="expanded_url")

            j = i + 1

            self.user_level_cooccurrence_url_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_retweeted()
            tweet1_quote_condition = tweet1.is_quote_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_retweeted()
                user1_rt = tweet1_rt.get_twitter().get_screen_name()

                if (user1, user1_rt) in self.user_level_cooccurrence_url_network.edges:
                    if (tweet1.get_id(), tweet1_rt.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user1_rt][
                        "tweets"] and (tweet1_rt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"]:
                        for ut in tweet1_urls:
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ut
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                else:
                    for ut in tweet1_urls:
                        if (user1, user1_rt) in self.user_level_cooccurrence_url_network.edges:
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ut
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
                            self.user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_id(), tweet1_rt.get_id())]
                        else:
                            self.user_level_cooccurrence_url_network.add_edge(user1, user1_rt, weight=1, urls=ut,
                                                                 tweets=[(tweet1.get_id(), tweet1_rt.get_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote()
                    user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                    tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                        if (tweet1.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] and (
                                tweet1_rt_qt.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet1_rt_qt_urls:
                                    if ut1 == ut2:
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_rt_qt_urls:
                                if ut1 == ut2:
                                    if (user1, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] += [
                                            (tweet1.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_url_network.add_edge(user1, user1_rt_qt, weight=1, urls=ut1,
                                                                             tweets=[
                                                                                 (tweet1.get_id(),
                                                                                  tweet1_rt_qt.get_id())])

                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                        if (tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] and (
                                tweet1_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet1_rt_qt_urls:
                                    if ut1 == ut2:
                                        # if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_rt_qt_urls:
                                if ut1 == ut2:
                                    if (user1_rt, user1_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"] += [
                                            (tweet1_rt.get_id(), tweet1_rt_qt.get_id())]
                                    else:
                                        self.user_level_cooccurrence_url_network.add_edge(user1_rt, user1_rt_qt, weight=1, urls=ut1,
                                                                             tweets=[(tweet1_rt.get_id(),
                                                                                      tweet1_rt_qt.get_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote()
                user1_qt = tweet1_qt.get_twitter().get_screen_name()
                tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
                    if (tweet1.get_id(), tweet1_qt.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user1_qt][
                        "tweets"] and (tweet1_qt.get_id(), tweet1.get_id()) not in \
                            self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"]:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_qt_urls:
                                if ut1 == ut2:
                                    # if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ut1
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["urls"] += edge_label
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                else:
                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_qt_urls:
                            if ut1 == ut2:
                                if (user1, user1_qt) in self.user_level_cooccurrence_url_network.edges:
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ut1
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["urls"] += edge_label
                                    self.user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_id(), tweet1_qt.get_id())]
                                else:
                                    self.user_level_cooccurrence_url_network.add_edge(user1, user1_qt, weight=1, urls=ut1,
                                                                         tweets=[(tweet1.get_id(), tweet1_qt.get_id())])

            while j != len(tweets_keys):
                tweet2 = self.tweets[tweets_keys[j]]
                user2 = tweet2.get_twitter().get_screen_name()
                tweet2_urls = tweet2.get_tweet_urls(return_format="expanded_url")

                tweet2_retweet_condition = tweet2.is_retweeted()
                tweet2_quote_condition = tweet2.is_quote_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()

                    if tweet1.get_id() != tweet2_rt.get_id():
                        if (user1, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                        "tweets"]:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                        else:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1, user2_rt, weight=1, urls=ut1,
                                                                                 tweets=[
                                                                                     (tweet1.get_id(),
                                                                                      tweet2_rt.get_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote()
                            user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                            tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                            if tweet1.get_id() != tweet2_rt_qt.get_id():
                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                    if (tweet1.get_id(), tweet2_rt_qt.get_id()) not in \
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] and (
                                            tweet2_rt_qt.get_id(), tweet1.get_id()) not in \
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"]:
                                        for ut1 in tweet1_urls:
                                            for ut2 in tweet2_rt_qt_urls:
                                                if ut1 == ut2:
                                                    # if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["weight"] += 1
                                                    edge_label = "-" + ut1
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] += [
                                                        (tweet1.get_id(), tweet2_rt_qt.get_id())]
                                else:
                                    for ut1 in tweet1_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                if (user1, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["weight"] += 1
                                                    edge_label = "-" + ut1
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    self.user_level_cooccurrence_url_network.edges[user1, user2_rt_qt]["tweets"] += [
                                                        (tweet1.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_url_network.add_edge(user1, user2_rt_qt, weight=1,
                                                                                         urls=ut1, tweets=[
                                                            (tweet1.get_id(), tweet2_rt_qt.get_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1.get_id() != tweet2_qt.get_id():
                        if (user1, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                        "tweets"]:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                        else:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] += [
                                                (tweet1.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1, user2_qt, weight=1, urls=ut1,
                                                                                 tweets=[
                                                                                     (tweet1.get_id(),
                                                                                      tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_id() != tweet2_rt.get_id():
                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_rt, weight=1, urls=ut1,
                                                                                 tweets=[(tweet1_rt.get_id(),
                                                                                          tweet2_rt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_id() != tweet2_rt.get_id():
                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] and (
                                        tweet2_rt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_rt, weight=1,
                                                                                     urls=ut1, tweets=[
                                                        (tweet1_rt_qt.get_id(), tweet2_rt.get_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"]:
                                    for ut1 in tweet1_rt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_rt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_rt_qt, weight=1,
                                                                                     urls=ut1, tweets=[
                                                        (tweet1_rt.get_id(), tweet2_rt_qt.get_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt]["tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                if (user1_rt_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ut1
                                                    self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [(tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())]
                                                else:
                                                    self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_rt_qt,
                                                                                         weight=1,
                                                                                         urls=ut1, tweets=[
                                                            (tweet1_rt_qt.get_id(), tweet2_rt_qt.get_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_id() != tweet2_qt.get_id():
                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            # if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_qt, weight=1, urls=ut1,
                                                                                 tweets=[
                                                                                     (tweet1_qt.get_id(),
                                                                                      tweet2_qt.get_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote()
                    user2_qt = tweet2_qt.get_twitter().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_id() != tweet2_qt.get_id():
                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_id(), tweet2_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] and (
                                    tweet2_qt.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2_qt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2_qt, weight=1, urls=ut1,
                                                                                 tweets=[(tweet1_rt.get_id(),
                                                                                          tweet2_qt.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_retweeted().get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_id() != tweet2_qt.get_id():
                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] and (
                                        tweet2_qt.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_qt_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt_qt, user2_qt) in self.user_level_cooccurrence_url_network.edges:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2_qt, weight=1,
                                                                                     urls=ut1,
                                                                                     tweets=[(tweet1_rt_qt.get_id(),
                                                                                              tweet2_qt.get_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_retweeted()
                    user2_rt = tweet2_rt.get_twitter().get_screen_name()
                    tweet2_rt_urls = tweet2_rt.get_tweet_urls(return_format="expanded_url")

                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_id() != tweet2_rt.get_id():
                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_id(), tweet2_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] and (
                                    tweet2_rt.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2_rt) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2_rt.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_rt, weight=1, urls=ut1,
                                                                                 tweets=[(tweet1_qt.get_id(),
                                                                                          tweet2_rt.get_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote()
                        user2_rt_qt = tweet2_rt_qt.get_twitter().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_qt.get_id() != tweet2_rt_qt.get_id():
                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_qt.get_id(), tweet2_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_id(), tweet1_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"]:
                                    for ut1 in tweet1_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                            else:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_qt, user2_rt_qt) in self.user_level_cooccurrence_url_network.edges:
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_qt.get_id(), tweet2_rt_qt.get_id())]
                                            else:
                                                self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2_rt_qt, weight=1,
                                                                                     urls=ut1, tweets=[
                                                        (tweet1_qt.get_id(), tweet2_rt_qt.get_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_retweeted()
                    user1_rt = tweet1_rt.get_twitter().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_id() != tweet2.get_id():
                        if (user1_rt, user2) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_rt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                        "tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] += [
                                                (tweet1_rt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_rt, user2, weight=1, urls=ut1,
                                                                                 tweets=[
                                                                                     (tweet1_rt.get_id(),
                                                                                      tweet2.get_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote()
                        user1_rt_qt = tweet1_rt_qt.get_twitter().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_id() != tweet2.get_id():
                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_id(), tweet2.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] and (
                                        tweet2.get_id(), tweet1_rt_qt.get_id()) not in \
                                        self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_urls:
                                            if ut1 == ut2:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            if (user1_rt_qt, user2) in self.user_level_cooccurrence_url_network.edges:
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ut1
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "urls"] += edge_label
                                                self.user_level_cooccurrence_url_network.edges[user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_id(), tweet2.get_id())]
                                            else:
                                                self.user_level_cooccurrence_url_network.add_edge(user1_rt_qt, user2, weight=1,
                                                                                     urls=ut1,
                                                                                     tweets=[(tweet1_rt_qt.get_id(),
                                                                                              tweet2.get_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote()
                    user1_qt = tweet1_qt.get_twitter().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_id() != tweet2.get_id():
                        if (user1_qt, user2) in self.user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_id(), tweet2.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] and (
                                    tweet2.get_id(), tweet1_qt.get_id()) not in \
                                    self.user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                        "tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2) in self.user_level_cooccurrence_url_network.edges:
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["weight"] += 1
                                            edge_label = "-" + ut1
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["urls"] += edge_label
                                            self.user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] += [
                                                (tweet1_qt.get_id(), tweet2.get_id())]
                                        else:
                                            self.user_level_cooccurrence_url_network.add_edge(user1_qt, user2, weight=1, urls=ut1,
                                                                                 tweets=[
                                                                                     (tweet1_qt.get_id(),
                                                                                      tweet2.get_id())])

                if tweet1.get_id() != tweet2.get_id():
                    if (user1, user2) in self.user_level_cooccurrence_url_network.edges:
                        if (tweet1.get_id(), tweet2.get_id()) not in self.user_level_cooccurrence_url_network.edges[user1, user2][
                            "tweets"] and (tweet2.get_id(), tweet1.get_id()) not in \
                                self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (user1, user2) in self.user_level_cooccurrence_url_network.edges:
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ut1
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["urls"] += edge_label
                                        self.user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_id(), tweet2.get_id())]
                                    else:
                                        self.user_level_cooccurrence_url_network.add_edge(user1, user2, weight=1, urls=ut1,
                                                                             tweets=[
                                                                                 (tweet1.get_id(), tweet2.get_id())])
                j += 1

        for edge in self.user_level_cooccurrence_url_network.edges:
            del self.user_level_cooccurrence_url_network.edges[edge]["tweets"]

    # bipartite version of user-level hashtag/mention/url networks
    def user_hashtag_bipartite_network_building(self):
        self.network_repository.append("user_hashtag_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_twitter().get_screen_name()
            hashtag_list = tweet.get_hashtags()

            for hashtag in hashtag_list:
                if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
                    self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                    self.user_hashtag_bipartite_network.edges[source, hashtag]["shared_content"] += tweet.get_text()
                else:
                    self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                       shared_content=tweet.get_text())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_twitter().get_screen_name()
                hashtag_list = tweet.get_hashtags()
                for hashtag in hashtag_list:

                    if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
                        self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        self.user_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_content"] += tweet.get_retweeted().get_text()
                    else:
                        self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                           shared_content=tweet.get_retweeted().get_text())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    hashtag_list = tweet.get_retweeted().get_quote().get_hashtags()
                    for hashtag in hashtag_list:

                        if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
                            self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                            self.user_hashtag_bipartite_network.edges[source, hashtag][
                                "shared_content"] += tweet.get_retweeted().get_quote().get_text()
                        else:
                            self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                               shared_content=tweet.get_retweeted().get_quote().get_text())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_twitter().get_screen_name()
                hashtag_list = tweet.get_quote().get_hashtags()
                for hashtag in hashtag_list:

                    if self.user_hashtag_bipartite_network.has_edge(source, hashtag):
                        self.user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        self.user_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_content"] += tweet.get_quote().get_text()
                    else:
                        self.user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                           shared_content=tweet.get_quote().get_text())

    def user_mention_bipartite_network_building(self):
        self.network_repository.append("user_mention_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_twitter().get_screen_name()
            mention_list = tweet.get_mentions()

            for mention in mention_list:
                if self.user_mention_bipartite_network.has_edge(source, mention):
                    self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                    self.user_mention_bipartite_network.edges[source, mention]["shared_content"] += tweet.get_text()
                else:
                    self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1, shared_content=tweet.get_text())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_twitter().get_screen_name()
                mention_list = tweet.get_mentions()
                for mention in mention_list:

                    if self.user_mention_bipartite_network.has_edge(source, mention):
                        self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        self.user_mention_bipartite_network.edges[source, mention]["shared_content"] += tweet.get_retweeted().get_text()
                    else:
                        self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                            shared_content=tweet.get_retweeted().get_text())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    mention_list = tweet.get_retweeted().get_quote().get_mentions()
                    for mention in mention_list:

                        if self.user_mention_bipartite_network.has_edge(source, mention):
                            self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                            self.user_mention_bipartite_network.edges[source, mention][
                                "shared_content"] += tweet.get_retweeted().get_quote().get_text()
                        else:
                            self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                               shared_content=tweet.get_retweeted().get_quote().get_text())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_twitter().get_screen_name()
                mention_list = tweet.get_quote().get_mentions()
                for mention in mention_list:

                    if self.user_mention_bipartite_network.has_edge(source, mention):
                        self.user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        self.user_mention_bipartite_network.edges[source, mention][
                            "shared_content"] += tweet.get_quote().get_text()
                    else:
                        self.user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                           shared_content=tweet.get_quote().get_text())

    def user_url_bipartite_network_building(self):
        self.network_repository.append("user_url_bipartite_network")
        for tweet_id, tweet in self.tweets.items():
            source = tweet.get_twitter().get_screen_name()
            url_list = tweet.get_tweet_urls(return_format="expanded_url")

            for url in url_list:
                if self.user_url_bipartite_network.has_edge(source, url):
                    self.user_url_bipartite_network.edges[source, url]["weight"] += 1
                    self.user_url_bipartite_network.edges[source, url]["shared_content"] += tweet.get_text()
                else:
                    self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                   shared_content=tweet.get_text())

            if tweet.is_retweeted():
                source = tweet.get_retweeted().get_twitter().get_screen_name()
                url_list = tweet.get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if self.user_url_bipartite_network.has_edge(source, url):
                        self.user_url_bipartite_network.edges[source, url]["weight"] += 1
                        self.user_url_bipartite_network.edges[source, url]["shared_content"] += tweet.get_retweeted().get_text()
                    else:
                        self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                       shared_content=tweet.get_retweeted().get_text())
                if tweet.get_retweeted().is_quote_available():
                    source = tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    url_list = tweet.get_retweeted().get_quote().get_tweet_urls(return_format="expanded_url")
                    for url in url_list:

                        if self.user_url_bipartite_network.has_edge(source, url):
                            self.user_url_bipartite_network.edges[source, url]["weight"] += 1
                            self.user_url_bipartite_network.edges[source, url][
                                "shared_content"] += tweet.get_retweeted().get_quote().get_text()
                        else:
                            self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                           shared_content=tweet.get_retweeted().get_quote().get_text())
            elif tweet.is_quote_available():
                source = tweet.get_quote().get_twitter().get_screen_name()
                url_list = tweet.get_quote().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if self.user_url_bipartite_network.has_edge(source, url):
                        self.user_url_bipartite_network.edges[source, url]["weight"] += 1
                        self.user_url_bipartite_network.edges[source, url][
                            "shared_content"] += tweet.get_quote().get_text()
                    else:
                        self.user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                       shared_content=tweet.get_quote().get_text())

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