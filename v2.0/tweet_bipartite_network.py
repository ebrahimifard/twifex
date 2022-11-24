import networkx as nx


class TweetBipartiteNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # bipartite version of tweet-level hashtag/mention/url networks
    def tweet_hashtag_bipartite_network_building(self):
        tweet_hashtag_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_id()
            hashtag_list = tweet.get_tweet_hashtags().get_tweet_hashtags()

            for hashtag in hashtag_list:
                if tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                    tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                    tweet_hashtag_bipartite_network.edges[source, hashtag][
                        "shared_author"] += tweet.get_tweet_user().get_screen_name()
                else:
                    tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                  shared_author=tweet.get_tweet_user().get_screen_name())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_id()
                hashtag_list = tweet.get_tweet_hashtags().get_tweet_hashtags()
                for hashtag in hashtag_list:

                    if tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                        tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        tweet_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_author"] += tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                      shared_author=tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id()
                    hashtag_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_hashtags().get_tweet_hashtags()
                    for hashtag in hashtag_list:

                        if tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                            tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                            tweet_hashtag_bipartite_network.edges[source, hashtag][
                                "shared_author"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                        else:
                            tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                          shared_author=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_id()
                hashtag_list = tweet.get_quote_status_object().get_tweet_hashtags().get_tweet_hashtags()
                for hashtag in hashtag_list:

                    if tweet_hashtag_bipartite_network.has_edge(source, hashtag):
                        tweet_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        tweet_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_author"] += tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                      shared_author=tweet.get_quote_status_object().get_tweet_user().get_screen_name())

        return tweet_hashtag_bipartite_network

    def tweet_mention_bipartite_network_building(self):
        tweet_mention_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_id()
            mention_list = tweet.get_tweet_mentions().get_tweet_mentions()

            for mention in mention_list:
                if tweet_mention_bipartite_network.has_edge(source, mention):
                    tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                    tweet_mention_bipartite_network.edges[source, mention][
                        "shared_author"] += tweet.get_tweet_user().get_screen_name()
                else:
                    tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                  shared_author=tweet.get_tweet_user().get_screen_name())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_id()
                mention_list = tweet.get_tweet_mentions().get_tweet_mentions()
                for mention in mention_list:

                    if tweet_mention_bipartite_network.has_edge(source, mention):
                        tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        tweet_mention_bipartite_network.edges[source, mention][
                            "shared_author"] += tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                      shared_author=tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id()
                    mention_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_mentions().get_tweet_mentions()
                    for mention in mention_list:

                        if tweet_mention_bipartite_network.has_edge(source, mention):
                            tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                            tweet_mention_bipartite_network.edges[source, mention][
                                "shared_author"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                        else:
                            tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                          shared_author=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_id()
                mention_list = tweet.get_quote_status_object().get_tweet_mentions().get_tweet_mentions()
                for mention in mention_list:

                    if tweet_mention_bipartite_network.has_edge(source, mention):
                        tweet_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        tweet_mention_bipartite_network.edges[source, mention][
                            "shared_author"] += tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                      shared_author=tweet.get_quote_status_object().get_tweet_user().get_screen_name())

        return tweet_mention_bipartite_network

    def tweet_url_bipartite_network_building(self):
        tweet_url_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_id()
            url_list = tweet.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

            for url in url_list:
                if tweet_url_bipartite_network.has_edge(source, url):
                    tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                    tweet_url_bipartite_network.edges[source, url][
                        "shared_author"] += tweet.get_tweet_user().get_screen_name()
                else:
                    tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                              shared_author=tweet.get_tweet_user().get_screen_name())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_id()
                url_list = tweet.get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if tweet_url_bipartite_network.has_edge(source, url):
                        tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                        tweet_url_bipartite_network.edges[source, url][
                            "shared_author"] += tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                  shared_author=tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_id()
                    url_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                    for url in url_list:

                        if tweet_url_bipartite_network.has_edge(source, url):
                            tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                            tweet_url_bipartite_network.edges[source, url][
                                "shared_author"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                        else:
                            tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                      shared_author=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_id()
                url_list = tweet.get_quote_status_object().get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if tweet_url_bipartite_network.has_edge(source, url):
                        tweet_url_bipartite_network.edges[source, url]["weight"] += 1
                        tweet_url_bipartite_network.edges[source, url][
                            "shared_author"] += tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    else:
                        tweet_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                  shared_author=tweet.get_quote_status_object().get_tweet_user().get_screen_name())

        return tweet_url_bipartite_network

