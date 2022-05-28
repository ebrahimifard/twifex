def tweet_url_bipartite_network_building(self):
    self.network_repository.append("tweet_url_network")
    for tweet_id, tweet in self.tweets.items():
        source = tweet.get_id()
        url_list = tweet.get_tweet_urls(return_format="expanded_url")

        for url in url_list:
            if self.tweet_url_network.has_edge(source, url):
                self.tweet_url_network.edges[source, url]["weight"] += 1
                self.tweet_url_network.edges[source, url]["shared_author"] += tweet.get_twitter().get_screen_name()
            else:
                self.tweet_url_network.add_edge(source, url, kind="url", weight=1,
                                                   shared_author=tweet.get_twitter().get_screen_name())

        if tweet.is_retweeted():
            source = tweet.get_retweeted().get_id()
            url_list = tweet.get_tweet_urls(return_format="expanded_url")
            for url in url_list:

                if self.tweet_url_network.has_edge(source, url):
                    self.tweet_url_network.edges[source, url]["weight"] += 1
                    self.tweet_url_network.edges[source, url][
                        "shared_author"] += tweet.get_retweeted().get_twitter().get_screen_name()
                else:
                    self.tweet_url_network.add_edge(source, url, kind="url", weight=1,
                                                       shared_author=tweet.get_retweeted().get_twitter().get_screen_name())
            if tweet.get_retweeted().is_quote_available():
                source = tweet.get_retweeted().get_quote().get_id()
                url_list = tweet.get_retweeted().get_quote().get_tweet_urls(return_format="expanded_url")
                for url in url_list:

                    if self.tweet_url_network.has_edge(source, url):
                        self.tweet_url_network.edges[source, url]["weight"] += 1
                        self.tweet_url_network.edges[source, url][
                            "shared_author"] += tweet.get_retweeted().get_quote().get_twitter().get_screen_name()
                    else:
                        self.tweet_url_network.add_edge(source, url, kind="url", weight=1,
                                                           shared_author=tweet.get_retweeted().get_quote().get_twitter().get_screen_name())
        elif tweet.is_quote_available():
            source = tweet.get_quote().get_id()
            url_list = tweet.get_quote().get_tweet_urls(return_format="expanded_url")
            for url in url_list:

                if self.tweet_url_network.has_edge(source, url):
                    self.tweet_url_network.edges[source, url]["weight"] += 1
                    self.tweet_url_network.edges[source, url][
                        "shared_author"] += tweet.get_quote().get_twitter().get_screen_name()
                else:
                    self.tweet_url_network.add_edge(source, url, kind="url", weight=1,
                                                       shared_author=tweet.get_quote().get_twitter().get_screen_name())