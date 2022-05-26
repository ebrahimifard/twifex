def tweet_level_hashtag_network_building(self):
    self.network_repository.append("tweet_level_hashtag_network")

    tweets_keys = list(self.tweets.keys())
    for i in range(len(tweets_keys)):
        tweet1 = self.tweets[tweets_keys[i]]
        tweet1_id = tweet1.get_id()
        tweet1_hashtags = tweet1.get_hashtags()

        j = i + 1

        self.tweet_level_hashtag_network.add_node(tweet1_id)

        tweet1_retweet_condition = tweet1.is_retweeted()
        tweet1_quote_condition = tweet1.is_quote_available()

        if tweet1_retweet_condition:
            tweet1_rt = tweet1.get_retweeted()
            tweet1_rt_id = tweet1_rt.get_id()

            for ht in tweet1_hashtags:
                if (tweet1_id, tweet1_rt_id) in self.tweet_level_hashtag_network.edges:
                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                    edge_label = "-" + ht
                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_rt_id]["hashtags"] += edge_label
                else:
                    self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet1_rt_id, weight=1, hashtags=ht)

            tweet1_inner_quote_condition = tweet1_rt.is_quote_available()
            if tweet1_inner_quote_condition:
                tweet1_rt_qt = tweet1_rt.get_quote()
                tweet1_rt_qt_id = tweet1_rt_qt.get_id()
                tweet1_rt_qt_hashtags = tweet1_rt_qt.get_hashtags()

                for ht1 in tweet1_hashtags:
                    for ht2 in tweet1_rt_qt_hashtags:
                        if ht1 == ht2:
                            if (tweet1_id, tweet1_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id]["weight"] += 1
                                edge_label = "-" + ht1
                                self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id][
                                    "hashtags"] += edge_label
                            else:
                                self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet1_rt_qt_id, weight=1,
                                                                          hashtags=ht1)

                for ht1 in tweet1_hashtags:
                    for ht2 in tweet1_rt_qt_hashtags:
                        if ht1 == ht2:
                            if (tweet1_rt_id, tweet1_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                edge_label = "-" + ht1
                                self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                    "hashtags"] += edge_label
                            else:
                                self.tweet_level_hashtag_network.add_edge(tweet1_rt_id, tweet1_rt_qt_id, weight=1,
                                                                          hashtags=ht1)

        if tweet1_quote_condition:
            tweet1_qt = tweet1.get_quote()
            tweet1_qt_id = tweet1_qt.get_id()
            tweet1_qt_hashtags = tweet1_qt.get_hashtags()

            for ht1 in tweet1_hashtags:
                for ht2 in tweet1_qt_hashtags:
                    if ht1 == ht2:
                        if (tweet1_id, tweet1_qt_id) in self.tweet_level_hashtag_network.edges:
                            self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_qt_id]["weight"] += 1
                            edge_label = "-" + ht1
                            self.tweet_level_hashtag_network.edges[tweet1_id, tweet1_qt_id][
                                "hashtags"] += edge_label
                        else:
                            self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet1_qt_id, weight=1,
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
                                if (tweet1_id, tweet2_rt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_rt_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_rt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet2_rt_id, weight=1,
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
                                        if (tweet1_id, tweet2_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                            self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet2_rt_qt_id,
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
                                if (tweet1_id, tweet2_qt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_qt_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet2_qt_id, weight=1,
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
                                if (tweet1_rt_id, tweet2_rt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_rt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_id, weight=1,
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
                                    if (tweet1_rt_qt_id, tweet2_rt_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_id,
                                                                                  weight=1, hashtags=ht1)

                if tweet2_inner_quote_condition:
                    tweet2_rt_qt = tweet2.get_retweeted().get_quote()
                    tweet2_rt_qt_id = tweet2_rt_qt.get_id()
                    tweet2_rt_qt_hashtags = tweet2_rt_qt.get_hashtags()

                    if tweet1_rt_id != tweet2_rt_qt_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_rt_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id, tweet2_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_rt_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_rt_id, tweet2_rt_qt_id,
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
                                    if (tweet1_rt_qt_id, tweet2_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_rt_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_rt_qt_id,
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
                                if (tweet1_qt_id, tweet2_qt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_qt_id, tweet2_qt_id, weight=1,
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
                                if (tweet1_rt_id, tweet2_qt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_rt_id, tweet2_qt_id, weight=1,
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
                                    if (tweet1_rt_qt_id, tweet2_qt_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_qt_id,
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
                                if (tweet1_qt_id, tweet2_rt_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_rt_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_id, weight=1,
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
                                    if (tweet1_qt_id, tweet2_rt_qt_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_rt_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_qt_id, tweet2_rt_qt_id,
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
                                if (tweet1_rt_id, tweet2_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_rt_id, tweet2_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_rt_id, tweet2_id, weight=1,
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
                                    if (tweet1_rt_qt_id, tweet2_id) in self.tweet_level_hashtag_network.edges:
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        self.tweet_level_hashtag_network.edges[tweet1_rt_qt_id, tweet2_id][
                                            "hashtags"] += edge_label
                                    else:
                                        self.tweet_level_hashtag_network.add_edge(tweet1_rt_qt_id, tweet2_id,
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
                                if (tweet1_qt_id, tweet2_id) in self.tweet_level_hashtag_network.edges:
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    self.tweet_level_hashtag_network.edges[tweet1_qt_id, tweet2_id][
                                        "hashtags"] += edge_label
                                else:
                                    self.tweet_level_hashtag_network.add_edge(tweet1_qt_id, tweet2_id, weight=1,
                                                                              hashtags=ht1)

            if tweet1_id != tweet2_id:
                for ht1 in tweet1_hashtags:
                    for ht2 in tweet2_hashtags:
                        if ht1 == ht2:
                            if (tweet1_id, tweet2_id) in self.tweet_level_hashtag_network.edges:
                                self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_id]["weight"] += 1
                                edge_label = "-" + ht1
                                self.tweet_level_hashtag_network.edges[tweet1_id, tweet2_id][
                                    "hashtags"] += edge_label
                            else:
                                self.tweet_level_hashtag_network.add_edge(tweet1_id, tweet2_id, weight=1,
                                                                          hashtags=ht1)
            j += 1