import networkx as nx


class UserBipartiteNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # bipartite version of user-level hashtag/mention/url networks
    def user_hashtag_bipartite_network_building(self):
        user_hashtag_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_user().get_screen_name()
            hashtag_list = tweet.get_tweet_hashtags().get_tweet_hashtags()

            for hashtag in hashtag_list:
                if user_hashtag_bipartite_network.has_edge(source, hashtag):
                    user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                    user_hashtag_bipartite_network.edges[source, hashtag]["shared_content"] += tweet.get_tweet_text()
                else:
                    user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                 shared_content=tweet.get_tweet_text())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                hashtag_list = tweet.get_tweet_hashtags().get_tweet_hashtags()
                for hashtag in hashtag_list:

                    if user_hashtag_bipartite_network.has_edge(source, hashtag):
                        user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        user_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_content"] += tweet.get_tweet_retweet_object().get_tweet_text()
                    else:
                        user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                     shared_content=tweet.get_tweet_retweet_object().get_tweet_text())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                    hashtag_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_hashtags().get_tweet_hashtags()
                    for hashtag in hashtag_list:

                        if user_hashtag_bipartite_network.has_edge(source, hashtag):
                            user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                            user_hashtag_bipartite_network.edges[source, hashtag][
                                "shared_content"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text()
                        else:
                            user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                         shared_content=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                hashtag_list = tweet.get_quote_status_object().get_tweet_hashtags().get_tweet_hashtags()
                for hashtag in hashtag_list:

                    if user_hashtag_bipartite_network.has_edge(source, hashtag):
                        user_hashtag_bipartite_network.edges[source, hashtag]["weight"] += 1
                        user_hashtag_bipartite_network.edges[source, hashtag][
                            "shared_content"] += tweet.get_quote_status_object().get_tweet_text()
                    else:
                        user_hashtag_bipartite_network.add_edge(source, hashtag, kind="hashtag", weight=1,
                                                                     shared_content=tweet.get_quote_status_object().get_tweet_text())

        return user_hashtag_bipartite_network

    def user_mention_bipartite_network_building(self):
        user_mention_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_user().get_screen_name()
            mention_list = tweet.get_tweet_mentions().get_tweet_mentions()

            for mention in mention_list:
                if user_mention_bipartite_network.has_edge(source, mention):
                    user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                    user_mention_bipartite_network.edges[source, mention]["shared_content"] += tweet.get_tweet_text()
                else:
                    user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                 shared_content=tweet.get_tweet_text())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                mention_list = tweet.get_tweet_mentions().get_tweet_mentions()
                for mention in mention_list:

                    if user_mention_bipartite_network.has_edge(source, mention):
                        user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        user_mention_bipartite_network.edges[source, mention][
                            "shared_content"] += tweet.get_tweet_retweet_object().get_tweet_text()
                    else:
                        user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                     shared_content=tweet.get_tweet_retweet_object().get_tweet_text())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                    mention_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_mentions().get_tweet_mentions()
                    for mention in mention_list:

                        if user_mention_bipartite_network.has_edge(source, mention):
                            user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                            user_mention_bipartite_network.edges[source, mention][
                                "shared_content"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text()
                        else:
                            user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                         shared_content=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                mention_list = tweet.get_quote_status_object().get_tweet_mentions().get_tweet_mentions()
                for mention in mention_list:

                    if user_mention_bipartite_network.has_edge(source, mention):
                        user_mention_bipartite_network.edges[source, mention]["weight"] += 1
                        user_mention_bipartite_network.edges[source, mention][
                            "shared_content"] += tweet.get_quote_status_object().get_tweet_text()
                    else:
                        user_mention_bipartite_network.add_edge(source, mention, kind="mention", weight=1,
                                                                     shared_content=tweet.get_quote_status_object().get_tweet_text())

        return user_mention_bipartite_network

    def user_url_bipartite_network_building(self):
        user_url_bipartite_network = nx.DiGraph()
        for tweet in self._tweets:
            source = tweet.get_tweet_user().get_screen_name()
            url_list = tweet.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

            for url in url_list:
                if user_url_bipartite_network.has_edge(source, url):
                    user_url_bipartite_network.edges[source, url]["weight"] += 1
                    user_url_bipartite_network.edges[source, url]["shared_content"] += tweet.get_tweet_text()
                else:
                    user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                             shared_content=tweet.get_tweet_text())

            if tweet.is_tweet_retweeted():
                source = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                url_list = tweet.get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if user_url_bipartite_network.has_edge(source, url):
                        user_url_bipartite_network.edges[source, url]["weight"] += 1
                        user_url_bipartite_network.edges[source, url][
                            "shared_content"] += tweet.get_tweet_retweet_object().get_tweet_text()
                    else:
                        user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                 shared_content=tweet.get_tweet_retweet_object().get_tweet_text())
                if tweet.get_tweet_retweet_object().is_quote_status_object_available():
                    source = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                    url_list = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                    for url in url_list:

                        if user_url_bipartite_network.has_edge(source, url):
                            user_url_bipartite_network.edges[source, url]["weight"] += 1
                            user_url_bipartite_network.edges[source, url][
                                "shared_content"] += tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text()
                        else:
                            user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                     shared_content=tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_text())
            elif tweet.is_quote_status_object_available():
                source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                url_list = tweet.get_quote_status_object().get_tweet_urls().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if user_url_bipartite_network.has_edge(source, url):
                        user_url_bipartite_network.edges[source, url]["weight"] += 1
                        user_url_bipartite_network.edges[source, url][
                            "shared_content"] += tweet.get_quote_status_object().get_tweet_text()
                    else:
                        user_url_bipartite_network.add_edge(source, url, kind="url", weight=1,
                                                                 shared_content=tweet.get_quote_status_object().get_tweet_text())

        return user_url_bipartite_network
