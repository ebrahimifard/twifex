import networkx as nx


class TweetCooccurrenceNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # hashtag/mention/url networks
    def tweet_level_cooccurrence_hashtag_network_building(self):
        tweet_level_cooccurrence_hashtag_network = nx.Graph()

        for i, tweet1 in enumerate(self._tweets):
            tweet1_id = tweet1.get_tweet_id()
            tweet1_hashtags = tweet1.get_tweet_hashtags().get_tweet_hashtags()

            j = i + 1

            tweet_level_cooccurrence_hashtag_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                tweet1_rt_id = tweet1_rt.get_tweet_id()

                for ht in tweet1_hashtags:
                    if (tweet1_id, tweet1_rt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                        tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + ht
                        tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_id][
                            "hashtags"] += edge_label
                    else:
                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_rt_id, weight=1,
                                                                               hashtags=ht)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                    tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_rt_qt_hashtags:
                            if ht1 == ht2:
                                if (
                                tweet1_id, tweet1_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                    tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id,
                                                                                           tweet1_rt_qt_id,
                                                                                           weight=1,
                                                                                           hashtags=ht1)

                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_rt_qt_hashtags:
                            if ht1 == ht2:
                                if (tweet1_rt_id,
                                    tweet1_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                    tweet_level_cooccurrence_hashtag_network.edges[
                                        tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + ht1
                                    tweet_level_cooccurrence_hashtag_network.edges[
                                        tweet1_rt_id, tweet1_rt_qt_id][
                                        "hashtags"] += edge_label
                                else:
                                    tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id,
                                                                                           tweet1_rt_qt_id,
                                                                                           weight=1,
                                                                                           hashtags=ht1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                tweet1_qt_id = tweet1_qt.get_tweet_id()
                tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                for ht1 in tweet1_hashtags:
                    for ht2 in tweet1_qt_hashtags:
                        if ht1 == ht2:
                            if (tweet1_id, tweet1_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id][
                                    "weight"] += 1
                                edge_label = "-" + ht1
                                tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet1_qt_id][
                                    "hashtags"] += edge_label
                            else:
                                tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet1_qt_id,
                                                                                       weight=1,
                                                                                       hashtags=ht1)

            while j != len(self._tweets):
                tweet2 = self._tweets[j]
                tweet2_id = tweet2.get_tweet_id()
                tweet2_hashtags = tweet2.get_tweet_hashtags().get_tweet_hashtags()

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()

                    if tweet1_id != tweet2_rt_id:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (
                                    tweet1_id, tweet2_rt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_id, tweet2_rt_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                            tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                            if tweet1_id != tweet2_rt_qt_id:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (tweet1_id,
                                                tweet2_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                                tweet_level_cooccurrence_hashtag_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                tweet_level_cooccurrence_hashtag_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "hashtags"] += edge_label
                                            else:
                                                tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id,
                                                                                                       tweet2_rt_qt_id,
                                                                                                       weight=1,
                                                                                                       hashtags=ht1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_id != tweet2_qt_id:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (
                                    tweet1_id, tweet2_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_id, tweet2_qt_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt_id != tweet2_rt_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_rt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id,
                                        tweet2_rt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_rt_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt_id != tweet2_qt_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_qt_id,
                                        tweet2_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt_id != tweet2_qt_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_qt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_rt_id,
                                        tweet2_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_qt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_qt_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_hashtags = tweet2_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt_id != tweet2_rt_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_rt_hashtags:
                                if ht1 == ht2:
                                    if (tweet1_qt_id,
                                        tweet2_rt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_rt_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               hashtags=ht1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt_id != tweet2_id:
                        for ht1 in tweet1_rt_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (
                                    tweet1_rt_id, tweet2_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_rt_id, tweet2_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_id, weight=1,
                                                                                               hashtags=ht1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet2_id != tweet1_rt_qt_id:
                            for ht1 in tweet1_rt_qt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            tweet_level_cooccurrence_hashtag_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "hashtags"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_id,
                                                                                                   weight=1,
                                                                                                   hashtags=ht1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt_id != tweet2_id:
                        for ht1 in tweet1_qt_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (
                                    tweet1_qt_id, tweet2_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + ht1
                                        tweet_level_cooccurrence_hashtag_network.edges[
                                            tweet1_qt_id, tweet2_id][
                                            "hashtags"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_id, weight=1,
                                                                                               hashtags=ht1)

                if tweet1_id != tweet2_id:
                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet2_hashtags:
                            if ht1 == ht2:
                                if (tweet1_id, tweet2_id) in tweet_level_cooccurrence_hashtag_network.edges:
                                    tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    tweet_level_cooccurrence_hashtag_network.edges[tweet1_id, tweet2_id][
                                        "hashtags"] += edge_label
                                else:
                                    tweet_level_cooccurrence_hashtag_network.add_edge(tweet1_id, tweet2_id,
                                                                                           weight=1,
                                                                                           hashtags=ht1)
                j += 1

        return tweet_level_cooccurrence_hashtag_network

    def tweet_level_cooccurrence_mention_network_building(self):
        tweet_level_cooccurrence_mention_network = nx.Graph()

        for i, tweet1 in enumerate(self._tweets):
            tweet1_id = tweet1.get_tweet_id()
            tweet1_mentions = tweet1.get_tweet_mentions().get_tweet_mentions()

            j = i + 1

            tweet_level_cooccurrence_mention_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                tweet1_rt_id = tweet1_rt.get_tweet_id()

                for mt in tweet1_mentions:
                    if (tweet1_id, tweet1_rt_id) in tweet_level_cooccurrence_mention_network.edges:
                        tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + mt
                        tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_id][
                            "mentions"] += edge_label
                    else:
                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_rt_id, weight=1,
                                                                               mentions=mt)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                    tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_rt_qt_mentions:
                            if mt1 == mt2:
                                if (
                                tweet1_id, tweet1_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                    tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + mt1
                                    tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "mentions"] += edge_label
                                else:
                                    tweet_level_cooccurrence_mention_network.add_edge(tweet1_id,
                                                                                           tweet1_rt_qt_id,
                                                                                           weight=1,
                                                                                           mentions=mt1)

                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_rt_qt_mentions:
                            if mt1 == mt2:
                                if (tweet1_rt_id,
                                    tweet1_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                    tweet_level_cooccurrence_mention_network.edges[
                                        tweet1_rt_id, tweet1_rt_qt_id]["weight"] += 1
                                    edge_label = "-" + mt1
                                    tweet_level_cooccurrence_mention_network.edges[
                                        tweet1_rt_id, tweet1_rt_qt_id][
                                        "mentions"] += edge_label
                                else:
                                    tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id,
                                                                                           tweet1_rt_qt_id,
                                                                                           weight=1,
                                                                                           mentions=mt1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                tweet1_qt_id = tweet1_qt.get_tweet_id()
                tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                for mt1 in tweet1_mentions:
                    for mt2 in tweet1_qt_mentions:
                        if mt1 == mt2:
                            if (tweet1_id, tweet1_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id][
                                    "weight"] += 1
                                edge_label = "-" + mt1
                                tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet1_qt_id][
                                    "mentions"] += edge_label
                            else:
                                tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet1_qt_id,
                                                                                       weight=1,
                                                                                       mentions=mt1)

            while j != len(self._tweets):
                tweet2 = self._tweets[j]
                tweet2_id = tweet2.get_tweet_id()
                tweet2_mentions = tweet2.get_tweet_hashtags().get_tweet_hashtags()

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()

                    if tweet1_id != tweet2_rt_id:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (
                                    tweet1_id, tweet2_rt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_id, tweet2_rt_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                            tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                            if tweet1_id != tweet2_rt_qt_id:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (tweet1_id,
                                                tweet2_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                                tweet_level_cooccurrence_mention_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                tweet_level_cooccurrence_mention_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "mentions"] += edge_label
                                            else:
                                                tweet_level_cooccurrence_mention_network.add_edge(tweet1_id,
                                                                                                       tweet2_rt_qt_id,
                                                                                                       weight=1,
                                                                                                       mentions=mt1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_id != tweet2_qt_id:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (
                                    tweet1_id, tweet2_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_id, tweet2_qt_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt_id != tweet2_rt_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_rt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_rt_id,
                                        tweet2_rt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_rt_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt_id != tweet2_qt_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_qt_id,
                                        tweet2_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt_id != tweet2_qt_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_qt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_rt_id,
                                        tweet2_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_qt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_qt_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_mentions = tweet2_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt_id != tweet2_rt_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_rt_mentions:
                                if mt1 == mt2:
                                    if (tweet1_qt_id,
                                        tweet2_rt_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_rt_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1,
                                                                                               mentions=mt1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_rt_qt_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt_id != tweet2_id:
                        for mt1 in tweet1_rt_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (
                                    tweet1_rt_id, tweet2_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_rt_id, tweet2_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_id, weight=1,
                                                                                               mentions=mt1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet2_id != tweet1_rt_qt_id:
                            for mt1 in tweet1_rt_qt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_id) in tweet_level_cooccurrence_mention_network.edges:
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            tweet_level_cooccurrence_mention_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "mentions"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_mention_network.add_edge(tweet1_rt_qt_id,
                                                                                                   tweet2_id,
                                                                                                   weight=1,
                                                                                                   mentions=mt1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt_id != tweet2_id:
                        for mt1 in tweet1_qt_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (
                                    tweet1_qt_id, tweet2_id) in tweet_level_cooccurrence_mention_network.edges:
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_id]["weight"] += 1
                                        edge_label = "-" + mt1
                                        tweet_level_cooccurrence_mention_network.edges[
                                            tweet1_qt_id, tweet2_id][
                                            "mentions"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_mention_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_id, weight=1,
                                                                                               mentions=mt1)

                if tweet1_id != tweet2_id:
                    for mt1 in tweet1_mentions:
                        for mt2 in tweet2_mentions:
                            if mt1 == mt2:
                                if (tweet1_id, tweet2_id) in tweet_level_cooccurrence_mention_network.edges:
                                    tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id][
                                        "weight"] += 1
                                    edge_label = "-" + mt1
                                    tweet_level_cooccurrence_mention_network.edges[tweet1_id, tweet2_id][
                                        "mentions"] += edge_label
                                else:
                                    tweet_level_cooccurrence_mention_network.add_edge(tweet1_id, tweet2_id,
                                                                                           weight=1,
                                                                                           mentions=mt1)
                j += 1

        return tweet_level_cooccurrence_mention_network

    def tweet_level_cooccurrence_url_network_building(self):
        tweet_level_cooccurrence_url_network = nx.Graph()

        for i, tweet1 in enumerate(self._tweets):
            tweet1_id = tweet1.get_tweet_id()
            tweet1_urls = tweet1.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

            j = i + 1

            tweet_level_cooccurrence_url_network.add_node(tweet1_id)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                tweet1_rt_id = tweet1_rt.get_tweet_id()

                for ut in tweet1_urls:
                    if (tweet1_id, tweet1_rt_id) in tweet_level_cooccurrence_url_network.edges:
                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id]["weight"] += 1
                        edge_label = "-" + ut
                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_id][
                            "urls"] += edge_label
                    else:
                        tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_id, weight=1,
                                                                           urls=ut)

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                    tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_rt_qt_urls:
                            if ut1 == ut2:
                                if (tweet1_id, tweet1_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                    tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ut1
                                    tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_rt_qt_id][
                                        "urls"] += edge_label
                                else:
                                    tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_rt_qt_id,
                                                                                       weight=1,
                                                                                       urls=ut1)

                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_rt_qt_urls:
                            if ut1 == ut2:
                                if (
                                tweet1_rt_id, tweet1_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                    tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                        "weight"] += 1
                                    edge_label = "-" + ut1
                                    tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet1_rt_qt_id][
                                        "urls"] += edge_label
                                else:
                                    tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id,
                                                                                       tweet1_rt_qt_id, weight=1,
                                                                                       urls=ut1)

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                tweet1_qt_id = tweet1_qt.get_tweet_id()
                tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                for ut1 in tweet1_urls:
                    for ut2 in tweet1_qt_urls:
                        if ut1 == ut2:
                            if (tweet1_id, tweet1_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id][
                                    "weight"] += 1
                                edge_label = "-" + ut1
                                tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet1_qt_id][
                                    "urls"] += edge_label
                            else:
                                tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet1_qt_id,
                                                                                   weight=1,
                                                                                   urls=ut1)

            while j != len(self._tweets):
                tweet2 = self._tweets[j]
                tweet2_id = tweet2.get_tweet_id()
                tweet2_urls = tweet2.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()

                    if tweet1_id != tweet2_rt_id:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_id, tweet2_rt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_rt_id,
                                                                                           weight=1,
                                                                                           urls=ut1)

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                            tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                            if tweet1_id != tweet2_rt_qt_id:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (tweet1_id,
                                                tweet2_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                                tweet_level_cooccurrence_url_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "weight"] += 1
                                                edge_label = "-" + ut1
                                                tweet_level_cooccurrence_url_network.edges[
                                                    tweet1_id, tweet2_rt_qt_id][
                                                    "urls"] += edge_label
                                            else:
                                                tweet_level_cooccurrence_url_network.add_edge(tweet1_id,
                                                                                                   tweet2_rt_qt_id,
                                                                                                   weight=1,
                                                                                                   urls=ut1)

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_id != tweet2_qt_id:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (tweet1_id, tweet2_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_qt_id,
                                                                                           weight=1,
                                                                                           urls=ut1)

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_rt_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_rt_urls:
                                if ut1 == ut2:
                                    if (
                                    tweet1_rt_id, tweet2_rt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id,
                                                                                           tweet2_rt_id, weight=1,
                                                                                           urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_rt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id,
                                                                                               tweet2_rt_id,
                                                                                               weight=1, urls=ut1)

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id,
                                                                                               tweet2_rt_qt_id,
                                                                                               weight=1, urls=ut1)

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id,
                                                                                               tweet2_rt_qt_id,
                                                                                               weight=1, urls=ut1)

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_qt_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (
                                    tweet1_qt_id, tweet2_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id,
                                                                                           tweet2_qt_id, weight=1,
                                                                                           urls=ut1)

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_id()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote_status_object()
                    tweet2_qt_id = tweet2_qt.get_tweet_id()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_qt_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_qt_urls:
                                if ut1 == ut2:
                                    if (
                                    tweet1_rt_id, tweet2_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_qt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id,
                                                                                           tweet2_qt_id, weight=1,
                                                                                           urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt_id != tweet2_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id,
                                                                                               tweet2_qt_id,
                                                                                               weight=1, urls=ut1)

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    tweet2_rt_id = tweet2_rt.get_tweet_id()
                    tweet2_rt_urls = tweet2_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_rt_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_rt_urls:
                                if ut1 == ut2:
                                    if (
                                    tweet1_qt_id, tweet2_rt_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_rt_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id,
                                                                                           tweet2_rt_id, weight=1,
                                                                                           urls=ut1)

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        tweet2_rt_qt_id = tweet2_rt_qt.get_tweet_id()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_qt_id != tweet2_rt_qt_id:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_rt_qt_urls:
                                    if ut1 == ut2:
                                        if (tweet1_qt_id,
                                            tweet2_rt_qt_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_qt_id, tweet2_rt_qt_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id,
                                                                                               tweet2_rt_qt_id,
                                                                                               weight=1,
                                                                                               urls=ut1)

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    tweet1_rt_id = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt_id != tweet2_id:
                        for ut1 in tweet1_rt_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_rt_id, tweet2_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_rt_id, tweet2_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_id, tweet2_id,
                                                                                           weight=1,
                                                                                           urls=ut1)

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        tweet1_rt_qt_id = tweet1_rt_qt.get_tweet_id()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet2_id != tweet1_rt_qt_id:
                            for ut1 in tweet1_rt_qt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (tweet1_rt_qt_id,
                                            tweet2_id) in tweet_level_cooccurrence_url_network.edges:
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            tweet_level_cooccurrence_url_network.edges[
                                                tweet1_rt_qt_id, tweet2_id][
                                                "urls"] += edge_label
                                        else:
                                            tweet_level_cooccurrence_url_network.add_edge(tweet1_rt_qt_id,
                                                                                               tweet2_id,
                                                                                               weight=1,
                                                                                               urls=ut1)

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    tweet1_qt_id = tweet1_qt.get_tweet_id()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt_id != tweet2_id:
                        for ut1 in tweet1_qt_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (tweet1_qt_id, tweet2_id) in tweet_level_cooccurrence_url_network.edges:
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        tweet_level_cooccurrence_url_network.edges[tweet1_qt_id, tweet2_id][
                                            "urls"] += edge_label
                                    else:
                                        tweet_level_cooccurrence_url_network.add_edge(tweet1_qt_id, tweet2_id,
                                                                                           weight=1,
                                                                                           urls=ut1)

                if tweet1_id != tweet2_id:
                    for ut1 in tweet1_urls:
                        for ut2 in tweet2_urls:
                            if ut1 == ut2:
                                if (tweet1_id, tweet2_id) in tweet_level_cooccurrence_url_network.edges:
                                    tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id][
                                        "weight"] += 1
                                    edge_label = "-" + ut1
                                    tweet_level_cooccurrence_url_network.edges[tweet1_id, tweet2_id][
                                        "urls"] += edge_label
                                else:
                                    tweet_level_cooccurrence_url_network.add_edge(tweet1_id, tweet2_id,
                                                                                       weight=1,
                                                                                       urls=ut1)
                j += 1

        return tweet_level_cooccurrence_url_network
