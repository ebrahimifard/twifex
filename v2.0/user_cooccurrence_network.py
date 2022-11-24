import networkx as nx


class UserCooccurrenceNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # user-level co-occurence hashtag/mention/url networks
    def user_level_cooccurrence_hashtag_network_building(self):  # Thinking of pruning hashtags      #also adding tweet_ids as a feature instead of deleting them (convert them to a a string)
        user_level_cooccurrence_hashtag_network = nx.Graph()

        for i, tweet1 in enumerate(self._tweets):
            user1 = tweet1.get_tweet_user().get_screen_name()
            tweet1_hashtags = tweet1.get_tweet_hashtags().get_tweet_hashtags()

            j = i + 1

            user_level_cooccurrence_hashtag_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                user1_rt = tweet1_rt.get_tweet_user().get_screen_name()

                if (user1, user1_rt) in user_level_cooccurrence_hashtag_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt][
                                "tweets"] and (tweet1_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"]:
                        for ht in tweet1_hashtags:
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ht
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt][
                                "hashtags"] += edge_label
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                else:
                    for ht in tweet1_hashtags:
                        if (user1, user1_rt) in user_level_cooccurrence_hashtag_network.edges:
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ht
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt][
                                "hashtags"] += edge_label
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                        else:
                            user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt, weight=1,
                                                                                  hashtags=ht,
                                                                                  tweets=[(tweet1.get_tweet_id(),
                                                                                           tweet1_rt.get_tweet_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                    tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if (user1, user1_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                    "tweets"] and (
                                tweet1_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet1_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_rt_qt_hashtags:
                                if ht1 == ht2:
                                    if (user1, user1_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_hashtag_network.add_edge(user1, user1_rt_qt,
                                                                                              weight=1,
                                                                                              hashtags=ht1,
                                                                                              tweets=[
                                                                                                  (tweet1.get_tweet_id(),
                                                                                                   tweet1_rt_qt.get_tweet_id())])

                    if (user1_rt, user1_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                    "tweets"] and (
                                tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet1_rt_qt_hashtags:
                                    if ht1 == ht2:
                                        # if (user1_rt, user1_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_rt_qt_hashtags:
                                if ht1 == ht2:
                                    if (
                                    user1_rt, user1_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user1_rt_qt,
                                                                                              weight=1,
                                                                                              hashtags=ht1, tweets=[
                                                (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                if (user1, user1_qt) in user_level_cooccurrence_hashtag_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                "tweets"] and (tweet1_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_hashtag_network.edges[user1, user1_qt]["tweets"]:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet1_qt_hashtags:
                                if ht1 == ht2:
                                    # if (user1, user1_qt) in user_level_cooccurrence_hashtag_network.edges:
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "hashtags"] += edge_label
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                else:
                    for ht1 in tweet1_hashtags:
                        for ht2 in tweet1_qt_hashtags:
                            if ht1 == ht2:
                                if (user1, user1_qt) in user_level_cooccurrence_hashtag_network.edges:
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "weight"] += 1
                                    edge_label = "-" + ht1
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "hashtags"] += edge_label
                                    user_level_cooccurrence_hashtag_network.edges[user1, user1_qt][
                                        "tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                                else:
                                    user_level_cooccurrence_hashtag_network.add_edge(user1, user1_qt, weight=1,
                                                                                          hashtags=ht1,
                                                                                          tweets=[
                                                                                              (tweet1.get_tweet_id(),
                                                                                               tweet1_qt.get_tweet_id())])

            while j != len(self._tweets):
                tweet2 = self._tweets[j]
                user2 = tweet2.get_tweet_user().get_screen_name()
                tweet2_hashtags = tweet2.get_tweet_hashtags().get_tweet_hashtags()

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()

                    if tweet1.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1, user2_rt]["tweets"]:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1, user2_rt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                            tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                            if tweet1.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                                if (user1, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                    if (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                "tweets"] and (
                                            tweet2_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_rt_qt][
                                                "tweets"]:
                                        for ht1 in tweet1_hashtags:
                                            for ht2 in tweet2_rt_qt_hashtags:
                                                if ht1 == ht2:
                                                    # if (user1, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "tweets"] += [(tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                else:
                                    for ht1 in tweet1_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                if (user1,
                                                    user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_hashtag_network.add_edge(user1,
                                                                                                          user2_rt_qt,
                                                                                                          weight=1,
                                                                                                          hashtags=ht1,
                                                                                                          tweets=[
                                                                                                              (
                                                                                                              tweet1.get_tweet_id(),
                                                                                                              tweet2_rt_qt.get_tweet_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1, user2_qt]["tweets"]:
                                for ht1 in tweet1_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (user1, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1, user2_qt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_rt, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                        "tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (
                                        user1_rt, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_rt,
                                                                                                  user2_rt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                            if (user1_rt_qt, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"] and (
                                        tweet2_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt,
                                                user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt,
                                                                                                      user2_rt,
                                                                                                      weight=1,
                                                                                                      hashtags=ht1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_rt.get_tweet_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"]:
                                    for ht1 in tweet1_rt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt,
                                                user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_hashtag_network.add_edge(user1_rt,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      hashtags=ht1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[
                                            user1_rt_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[
                                            user1_rt_qt, user2_rt_qt]["tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [(tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                # if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                if (user1_rt_qt,
                                                    user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1_rt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ht1
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "hashtags"] += edge_label
                                                    user_level_cooccurrence_hashtag_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_hashtag_network.add_edge(
                                                        user1_rt_qt, user2_rt_qt,
                                                        weight=1, hashtags=ht1,
                                                        tweets=[
                                                            (tweet1_rt_qt.get_tweet_id(),
                                                             tweet2_rt_qt.get_tweet_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_qt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                        "tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            # if (user1_qt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (
                                        user1_qt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_qt,
                                                                                                  user2_qt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])
                                    # else:
                                    #     user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2_qt, weight=1, hashtags=ht1, tweets=[(tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_hashtags = tweet2_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_rt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                        "tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_qt_hashtags:
                                    if ht1 == ht2:
                                        if (
                                        user1_rt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_rt,
                                                                                                  user2_qt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                            if (user1_rt_qt, user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"] and (
                                        tweet2_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_qt_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt,
                                                user2_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt,
                                                                                                      user2_qt,
                                                                                                      weight=1,
                                                                                                      hashtags=ht1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_qt.get_tweet_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_hashtags = tweet2_rt.get_tweet_hashtags().get_tweet_hashtags()

                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_qt, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                        "tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_rt_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_rt_hashtags:
                                    if ht1 == ht2:
                                        if (
                                        user1_qt, user2_rt) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_qt,
                                                                                                  user2_rt,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_hashtags = tweet2_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_qt, user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"]:
                                    for ht1 in tweet1_qt_hashtags:
                                        for ht2 in tweet2_rt_qt_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_rt_qt_hashtags:
                                        if ht1 == ht2:
                                            if (user1_qt,
                                                user2_rt_qt) in user_level_cooccurrence_hashtag_network.edges:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_hashtag_network.add_edge(user1_qt,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      hashtags=ht1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_qt.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_hashtags = tweet1_rt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_rt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_rt, user2) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                        "tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_rt, user2]["tweets"]:
                                for ht1 in tweet1_rt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for ht1 in tweet1_rt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1_rt, user2) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_rt, user2,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_hashtags = tweet1_rt_qt.get_tweet_hashtags().get_tweet_hashtags()

                        if tweet1_rt_qt.get_tweet_id() != tweet2.get_tweet_id():
                            if (user1_rt_qt, user2) in user_level_cooccurrence_hashtag_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
                                            "tweets"] and (
                                        tweet2.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_hashtag_network.edges[user1_rt_qt, user2][
                                            "tweets"]:
                                    for ht1 in tweet1_rt_qt_hashtags:
                                        for ht2 in tweet2_hashtags:
                                            if ht1 == ht2:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                            else:
                                for ht1 in tweet1_rt_qt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            if (user1_rt_qt,
                                                user2) in user_level_cooccurrence_hashtag_network.edges:
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + ht1
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2][
                                                    "hashtags"] += edge_label
                                                user_level_cooccurrence_hashtag_network.edges[
                                                    user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_hashtag_network.add_edge(user1_rt_qt,
                                                                                                      user2,
                                                                                                      weight=1,
                                                                                                      hashtags=ht1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2.get_tweet_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_hashtags = tweet1_qt.get_tweet_hashtags().get_tweet_hashtags()

                    if tweet1_qt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_qt, user2) in user_level_cooccurrence_hashtag_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                        "tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_hashtag_network.edges[user1_qt, user2]["tweets"]:
                                for ht1 in tweet1_qt_hashtags:
                                    for ht2 in tweet2_hashtags:
                                        if ht1 == ht2:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for ht1 in tweet1_qt_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        if (user1_qt, user2) in user_level_cooccurrence_hashtag_network.edges:
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ht1
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "hashtags"] += edge_label
                                            user_level_cooccurrence_hashtag_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_hashtag_network.add_edge(user1_qt, user2,
                                                                                                  weight=1,
                                                                                                  hashtags=ht1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])

                if tweet1.get_tweet_id() != tweet2.get_tweet_id():
                    if (user1, user2) in user_level_cooccurrence_hashtag_network.edges:
                        if (tweet1.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                    "tweets"] and (tweet2.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_hashtag_network.edges[user1, user2]["tweets"]:
                            for ht1 in tweet1_hashtags:
                                for ht2 in tweet2_hashtags:
                                    if ht1 == ht2:
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                    else:
                        for ht1 in tweet1_hashtags:
                            for ht2 in tweet2_hashtags:
                                if ht1 == ht2:
                                    if (user1, user2) in user_level_cooccurrence_hashtag_network.edges:
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "weight"] += 1
                                        edge_label = "-" + ht1
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "hashtags"] += edge_label
                                        user_level_cooccurrence_hashtag_network.edges[user1, user2][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_hashtag_network.add_edge(user1, user2,
                                                                                              weight=1,
                                                                                              hashtags=ht1,
                                                                                              tweets=[
                                                                                                  (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])
                j += 1

        for edge in user_level_cooccurrence_hashtag_network.edges:
            del user_level_cooccurrence_hashtag_network.edges[edge]["tweets"]

        return user_level_cooccurrence_hashtag_network

    def user_level_cooccurrence_mention_network_building(self):
        user_level_cooccurrence_mention_network = nx.Graph()

        # tweets_keys = list(self.tweets.keys())
        for i, tweet1 in enumerate(self._tweets):
            # tweet1 = self.tweets[tweets_keys[i]]
            user1 = tweet1.get_tweet_user().get_screen_name()
            tweet1_mentions = tweet1.get_tweet_mentions().get_tweet_mentions()

            j = i + 1

            user_level_cooccurrence_mention_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                user1_rt = tweet1_rt.get_tweet_user().get_screen_name()

                if (user1, user1_rt) in user_level_cooccurrence_mention_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt][
                                "tweets"] and (tweet1_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"]:
                        for mt in tweet1_mentions:
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + mt
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt][
                                "mentions"] += edge_label
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                else:
                    for mt in tweet1_mentions:
                        if (user1, user1_rt) in user_level_cooccurrence_mention_network.edges:
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + mt
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt][
                                "mentions"] += edge_label
                            user_level_cooccurrence_mention_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                        else:
                            user_level_cooccurrence_mention_network.add_edge(user1, user1_rt, weight=1,
                                                                                  mentions=mt,
                                                                                  tweets=[(tweet1.get_tweet_id(),
                                                                                           tweet1_rt.get_tweet_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                    tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                    if (user1, user1_rt_qt) in user_level_cooccurrence_mention_network.edges:
                        if (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                    "tweets"] and (
                                tweet1_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet1_rt_qt_mentions:
                                    if mt1 == mt2:
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_rt_qt_mentions:
                                if mt1 == mt2:
                                    if (user1, user1_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_mention_network.add_edge(user1, user1_rt_qt,
                                                                                              weight=1,
                                                                                              mentions=mt1,
                                                                                              tweets=[
                                                                                                  (tweet1.get_tweet_id(),
                                                                                                   tweet1_rt_qt.get_tweet_id())])

                    if (user1_rt, user1_rt_qt) in user_level_cooccurrence_mention_network.edges:
                        if (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                    "tweets"] and (
                                tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet1_rt_qt_mentions:
                                    if mt1 == mt2:
                                        # if (user1_rt, user1_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_rt_qt_mentions:
                                if mt1 == mt2:
                                    if (
                                    user1_rt, user1_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_mention_network.add_edge(user1_rt, user1_rt_qt,
                                                                                              weight=1,
                                                                                              mentions=mt1, tweets=[
                                                (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                if (user1, user1_qt) in user_level_cooccurrence_mention_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                            user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                "tweets"] and (tweet1_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_mention_network.edges[user1, user1_qt]["tweets"]:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet1_qt_mentions:
                                if mt1 == mt2:
                                    # if (user1, user1_qt) in user_level_cooccurrence_mention_network.edges:
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "weight"] += 1
                                    edge_label = "-" + mt1
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "mentions"] += edge_label
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                else:
                    for mt1 in tweet1_mentions:
                        for mt2 in tweet1_qt_mentions:
                            if mt1 == mt2:
                                if (user1, user1_qt) in user_level_cooccurrence_mention_network.edges:
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "weight"] += 1
                                    edge_label = "-" + mt1
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "mentions"] += edge_label
                                    user_level_cooccurrence_mention_network.edges[user1, user1_qt][
                                        "tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                                else:
                                    user_level_cooccurrence_mention_network.add_edge(user1, user1_qt, weight=1,
                                                                                          mentions=mt1,
                                                                                          tweets=[
                                                                                              (tweet1.get_tweet_id(),
                                                                                               tweet1_qt.get_tweet_id())])

            while j != len(self._tweets):
                # tweet2 = self.tweets[tweets_keys[j]]
                tweet2 = self._tweets[j]
                user2 = tweet2.get_tweet_user().get_screen_name()
                tweet2_mentions = tweet2.get_tweet_mentions().get_tweet_mentions()

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()

                    if tweet1.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1, user2_rt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1, user2_rt]["tweets"]:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1, user2_rt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1, user2_rt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                            tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                            if tweet1.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                                if (user1, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                    if (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                "tweets"] and (
                                            tweet2_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                            user_level_cooccurrence_mention_network.edges[user1, user2_rt_qt][
                                                "tweets"]:
                                        for mt1 in tweet1_mentions:
                                            for mt2 in tweet2_rt_qt_mentions:
                                                if mt1 == mt2:
                                                    # if (user1, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "tweets"] += [(tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                else:
                                    for mt1 in tweet1_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                if (user1,
                                                    user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_mention_network.add_edge(user1,
                                                                                                          user2_rt_qt,
                                                                                                          weight=1,
                                                                                                          mentions=mt1,
                                                                                                          tweets=[
                                                                                                              (
                                                                                                              tweet1.get_tweet_id(),
                                                                                                              tweet2_rt_qt.get_tweet_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1, user2_qt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1, user2_qt]["tweets"]:
                                for mt1 in tweet1_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (user1, user2_qt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1, user2_qt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_rt, user2_rt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                        "tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (
                                        user1_rt, user2_rt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_rt,
                                                                                                  user2_rt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                            if (user1_rt_qt, user2_rt) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"] and (
                                        tweet2_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt,
                                                user2_rt) in user_level_cooccurrence_mention_network.edges:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_mention_network.add_edge(user1_rt_qt,
                                                                                                      user2_rt,
                                                                                                      weight=1,
                                                                                                      mentions=mt1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_rt.get_tweet_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"]:
                                    for mt1 in tweet1_rt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt,
                                                user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_mention_network.add_edge(user1_rt,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      mentions=mt1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[
                                            user1_rt_qt, user2_rt_qt]["tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[
                                            user1_rt_qt, user2_rt_qt]["tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [(tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                # if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                if (user1_rt_qt,
                                                    user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + mt1
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "mentions"] += edge_label
                                                    user_level_cooccurrence_mention_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_mention_network.add_edge(
                                                        user1_rt_qt, user2_rt_qt,
                                                        weight=1, mentions=mt1,
                                                        tweets=[
                                                            (tweet1_rt_qt.get_tweet_id(),
                                                             tweet2_rt_qt.get_tweet_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_qt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                        "tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            # if (user1_qt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (
                                        user1_qt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_qt,
                                                                                                  user2_qt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_mentions = tweet2_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_rt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                        "tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_qt_mentions:
                                    if mt1 == mt2:
                                        if (
                                        user1_rt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_rt,
                                                                                                  user2_qt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                            if (user1_rt_qt, user2_qt) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"] and (
                                        tweet2_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_qt_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt,
                                                user2_qt) in user_level_cooccurrence_mention_network.edges:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_mention_network.add_edge(user1_rt_qt,
                                                                                                      user2_qt,
                                                                                                      weight=1,
                                                                                                      mentions=mt1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_qt.get_tweet_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_mentions = tweet2_rt.get_tweet_mentions().get_tweet_mentions()

                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_qt, user2_rt) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                        "tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_rt_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_rt_mentions:
                                    if mt1 == mt2:
                                        if (
                                        user1_qt, user2_rt) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_qt,
                                                                                                  user2_rt,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_mentions = tweet2_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_qt, user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"]:
                                    for mt1 in tweet1_qt_mentions:
                                        for mt2 in tweet2_rt_qt_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_rt_qt_mentions:
                                        if mt1 == mt2:
                                            if (user1_qt,
                                                user2_rt_qt) in user_level_cooccurrence_mention_network.edges:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_mention_network.add_edge(user1_qt,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      mentions=mt1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_qt.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_mentions = tweet1_rt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_rt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_rt, user2) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                        "tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_rt, user2]["tweets"]:
                                for mt1 in tweet1_rt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for mt1 in tweet1_rt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1_rt, user2) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_rt, user2,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_mentions = tweet1_rt_qt.get_tweet_mentions().get_tweet_mentions()

                        if tweet1_rt_qt.get_tweet_id() != tweet2.get_tweet_id():
                            if (user1_rt_qt, user2) in user_level_cooccurrence_mention_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
                                            "tweets"] and (
                                        tweet2.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_mention_network.edges[user1_rt_qt, user2][
                                            "tweets"]:
                                    for mt1 in tweet1_rt_qt_mentions:
                                        for mt2 in tweet2_mentions:
                                            if mt1 == mt2:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                            else:
                                for mt1 in tweet1_rt_qt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            if (user1_rt_qt,
                                                user2) in user_level_cooccurrence_mention_network.edges:
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2]["weight"] += 1
                                                edge_label = "-" + mt1
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2][
                                                    "mentions"] += edge_label
                                                user_level_cooccurrence_mention_network.edges[
                                                    user1_rt_qt, user2]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_mention_network.add_edge(user1_rt_qt,
                                                                                                      user2,
                                                                                                      weight=1,
                                                                                                      mentions=mt1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2.get_tweet_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_mentions = tweet1_qt.get_tweet_mentions().get_tweet_mentions()

                    if tweet1_qt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_qt, user2) in user_level_cooccurrence_mention_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                        "tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_mention_network.edges[user1_qt, user2]["tweets"]:
                                for mt1 in tweet1_qt_mentions:
                                    for mt2 in tweet2_mentions:
                                        if mt1 == mt2:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for mt1 in tweet1_qt_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        if (user1_qt, user2) in user_level_cooccurrence_mention_network.edges:
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + mt1
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "mentions"] += edge_label
                                            user_level_cooccurrence_mention_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_mention_network.add_edge(user1_qt, user2,
                                                                                                  weight=1,
                                                                                                  mentions=mt1,
                                                                                                  tweets=[
                                                                                                      (
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])

                if tweet1.get_tweet_id() != tweet2.get_tweet_id():
                    if (user1, user2) in user_level_cooccurrence_mention_network.edges:
                        if (tweet1.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1, user2][
                                    "tweets"] and (tweet2.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_mention_network.edges[user1, user2]["tweets"]:
                            for mt1 in tweet1_mentions:
                                for mt2 in tweet2_mentions:
                                    if mt1 == mt2:
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                    else:
                        for mt1 in tweet1_mentions:
                            for mt2 in tweet2_mentions:
                                if mt1 == mt2:
                                    if (user1, user2) in user_level_cooccurrence_mention_network.edges:
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "weight"] += 1
                                        edge_label = "-" + mt1
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "mentions"] += edge_label
                                        user_level_cooccurrence_mention_network.edges[user1, user2][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_mention_network.add_edge(user1, user2,
                                                                                              weight=1,
                                                                                              mentions=mt1,
                                                                                              tweets=[
                                                                                                  (
                                                                                                      tweet1.get_tweet_id(),
                                                                                                      tweet2.get_tweet_id())])
                j += 1

        for edge in user_level_cooccurrence_mention_network.edges:
            del user_level_cooccurrence_mention_network.edges[edge]["tweets"]

        return user_level_cooccurrence_mention_network

    def user_level_cooccurrence_url_network_building(self):
        user_level_cooccurrence_url_network = nx.Graph()

        # tweets_keys = list(self.tweets.keys())
        for i, tweet1 in enumerate(self._tweets):
            # tweet1 = self.tweets[tweets_keys[i]]
            user1 = tweet1.get_tweet_user().get_screen_name()
            tweet1_urls = tweet1.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

            j = i + 1

            user_level_cooccurrence_url_network.add_node(user1)

            tweet1_retweet_condition = tweet1.is_tweet_retweeted()
            tweet1_quote_condition = tweet1.is_quote_status_object_available()

            if tweet1_retweet_condition:
                tweet1_rt = tweet1.get_tweet_retweet_object()
                user1_rt = tweet1_rt.get_tweet_user().get_screen_name()

                if (user1, user1_rt) in user_level_cooccurrence_url_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                            user_level_cooccurrence_url_network.edges[user1, user1_rt][
                                "tweets"] and (tweet1_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"]:
                        for ut in tweet1_urls:
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ut
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                else:
                    for ut in tweet1_urls:
                        if (user1, user1_rt) in user_level_cooccurrence_url_network.edges:
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["weight"] += 1
                            edge_label = "-" + ut
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["urls"] += edge_label
                            user_level_cooccurrence_url_network.edges[user1, user1_rt]["tweets"] += [
                                (tweet1.get_tweet_id(), tweet1_rt.get_tweet_id())]
                        else:
                            user_level_cooccurrence_url_network.add_edge(user1, user1_rt, weight=1, urls=ut,
                                                                              tweets=[(tweet1.get_tweet_id(),
                                                                                       tweet1_rt.get_tweet_id())])

                tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                if tweet1_inner_quote_condition:
                    tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                    user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                    tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if (user1, user1_rt_qt) in user_level_cooccurrence_url_network.edges:
                        if (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"] and (
                                tweet1_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1, user1_rt_qt]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet1_rt_qt_urls:
                                    if ut1 == ut2:
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_rt_qt_urls:
                                if ut1 == ut2:
                                    if (user1, user1_rt_qt) in user_level_cooccurrence_url_network.edges:
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_url_network.add_edge(user1, user1_rt_qt,
                                                                                          weight=1, urls=ut1,
                                                                                          tweets=[
                                                                                              (tweet1.get_tweet_id(),
                                                                                               tweet1_rt_qt.get_tweet_id())])

                    if (user1_rt, user1_rt_qt) in user_level_cooccurrence_url_network.edges:
                        if (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                    "tweets"] and (
                                tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet1_rt_qt_urls:
                                    if ut1 == ut2:
                                        # if (user1_rt, user1_rt_qt) in user_level_cooccurrence_url_network.edges:
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_rt_qt_urls:
                                if ut1 == ut2:
                                    if (user1_rt, user1_rt_qt) in user_level_cooccurrence_url_network.edges:
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1_rt, user1_rt_qt][
                                            "tweets"] += [
                                            (tweet1_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_url_network.add_edge(user1_rt, user1_rt_qt,
                                                                                          weight=1, urls=ut1,
                                                                                          tweets=[
                                                                                              (tweet1_rt.get_tweet_id(),
                                                                                               tweet1_rt_qt.get_tweet_id())])

            if tweet1_quote_condition:
                tweet1_qt = tweet1.get_quote_status_object()
                user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                if (user1, user1_qt) in user_level_cooccurrence_url_network.edges:
                    if (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                            user_level_cooccurrence_url_network.edges[user1, user1_qt][
                                "tweets"] and (tweet1_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                            user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"]:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet1_qt_urls:
                                if ut1 == ut2:
                                    # if (user1, user1_qt) in user_level_cooccurrence_url_network.edges:
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ut1
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt][
                                        "urls"] += edge_label
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                else:
                    for ut1 in tweet1_urls:
                        for ut2 in tweet1_qt_urls:
                            if ut1 == ut2:
                                if (user1, user1_qt) in user_level_cooccurrence_url_network.edges:
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt]["weight"] += 1
                                    edge_label = "-" + ut1
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt][
                                        "urls"] += edge_label
                                    user_level_cooccurrence_url_network.edges[user1, user1_qt]["tweets"] += [
                                        (tweet1.get_tweet_id(), tweet1_qt.get_tweet_id())]
                                else:
                                    user_level_cooccurrence_url_network.add_edge(user1, user1_qt, weight=1,
                                                                                      urls=ut1,
                                                                                      tweets=[(tweet1.get_tweet_id(),
                                                                                               tweet1_qt.get_tweet_id())])

            while j != len(self._tweets):
                # tweet2 = self.tweets[tweets_keys[j]]
                tweet2 = self._tweets[j]
                user2 = tweet2.get_tweet_user().get_screen_name()
                tweet2_urls = tweet2.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                tweet2_retweet_condition = tweet2.is_tweet_retweeted()
                tweet2_quote_condition = tweet2.is_quote_status_object_available()

                if tweet2_retweet_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()

                    if tweet1.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1, user2_rt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1, user2_rt]["tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                        "tweets"]:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1, user2_rt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1, user2_rt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[
                                                                                                  (tweet1.get_tweet_id(),
                                                                                                   tweet2_rt.get_tweet_id())])

                        tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                        if tweet2_inner_quote_condition:
                            tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                            user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                            tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                            if tweet1.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                                if (user1, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                    if (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
                                                "tweets"] and (
                                            tweet2_rt_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                            user_level_cooccurrence_url_network.edges[user1, user2_rt_qt][
                                                "tweets"]:
                                        for ut1 in tweet1_urls:
                                            for ut2 in tweet2_rt_qt_urls:
                                                if ut1 == ut2:
                                                    # if (user1, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt]["weight"] += 1
                                                    edge_label = "-" + ut1
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt]["tweets"] += [
                                                        (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                else:
                                    for ut1 in tweet1_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                if (user1,
                                                    user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt]["weight"] += 1
                                                    edge_label = "-" + ut1
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1, user2_rt_qt]["tweets"] += [
                                                        (tweet1.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_url_network.add_edge(user1,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      urls=ut1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                if tweet2_quote_condition:
                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1, user2_qt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1, user2_qt]["tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                        "tweets"]:
                                for ut1 in tweet1_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1, user2_qt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1, user2_qt][
                                                "tweets"] += [
                                                (tweet1.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1, user2_qt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[
                                                                                                  (tweet1.get_tweet_id(),
                                                                                                   tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_rt, user2_rt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2_rt]["tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2_rt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_rt, user2_rt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[(
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()

                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                            if (user1_rt_qt, user2_rt) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"] and (
                                        tweet2_rt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt][
                                            "tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt_qt,
                                                user2_rt) in user_level_cooccurrence_url_network.edges:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_url_network.add_edge(user1_rt_qt,
                                                                                                  user2_rt,
                                                                                                  weight=1,
                                                                                                  urls=ut1, tweets=[
                                                        (tweet1_rt_qt.get_tweet_id(), tweet2_rt.get_tweet_id())])

                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt, user2_rt_qt][
                                            "tweets"]:
                                    for ut1 in tweet1_rt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt,
                                                user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_url_network.add_edge(user1_rt,
                                                                                                  user2_rt_qt,
                                                                                                  weight=1,
                                                                                                  urls=ut1, tweets=[
                                                        (tweet1_rt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())])

                    if tweet1_inner_quote_condition and tweet2_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        tweet2_rt_qt = tweet2.get_tweet_retweet_object().get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_rt_qt][
                                            "tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_rt_qt][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                # if (user1_rt_qt, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                if (user1_rt_qt,
                                                    user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1_rt, user2_rt_qt][
                                                        "weight"] += 1
                                                    edge_label = "-" + ut1
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "urls"] += edge_label
                                                    user_level_cooccurrence_url_network.edges[
                                                        user1_rt_qt, user2_rt_qt][
                                                        "tweets"] += [
                                                        (tweet1_rt_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                                else:
                                                    user_level_cooccurrence_url_network.add_edge(user1_rt_qt,
                                                                                                      user2_rt_qt,
                                                                                                      weight=1,
                                                                                                      urls=ut1,
                                                                                                      tweets=[
                                                                                                          (
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_rt_qt.get_tweet_id())])

                if tweet1_quote_condition and tweet2_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_qt, user2_qt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2_qt]["tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            # if (user1_qt, user2_qt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2_qt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_qt, user2_qt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[
                                                                                                  (
                                                                                                  tweet1_qt.get_tweet_id(),
                                                                                                  tweet2_qt.get_tweet_id())])

                if tweet1_retweet_condition and tweet2_quote_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet2_qt = tweet2.get_quote_status_object()
                    user2_qt = tweet2_qt.get_tweet_user().get_screen_name()
                    tweet2_qt_urls = tweet2_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_tweet_id() != tweet2_qt.get_tweet_id():
                        if (user1_rt, user2_qt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                        "tweets"] and (
                                    tweet2_qt.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2_qt]["tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_qt_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2_qt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2_qt][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_rt, user2_qt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[(
                                                                                                      tweet1_rt.get_tweet_id(),
                                                                                                      tweet2_qt.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1.get_tweet_retweet_object().get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_tweet_id() != tweet2_qt.get_tweet_id():
                            if (user1_rt_qt, user2_qt) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"] and (
                                        tweet2_qt.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2_qt][
                                            "tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_qt_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_rt_qt,
                                                user2_qt) in user_level_cooccurrence_url_network.edges:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_rt_qt, user2_qt]["tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_url_network.add_edge(user1_rt_qt,
                                                                                                  user2_qt,
                                                                                                  weight=1,
                                                                                                  urls=ut1,
                                                                                                  tweets=[(
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2_qt.get_tweet_id())])

                if tweet2_retweet_condition and tweet1_quote_condition:
                    tweet2_rt = tweet2.get_tweet_retweet_object()
                    user2_rt = tweet2_rt.get_tweet_user().get_screen_name()
                    tweet2_rt_urls = tweet2_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_tweet_id() != tweet2_rt.get_tweet_id():
                        if (user1_qt, user2_rt) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                        "tweets"] and (
                                    tweet2_rt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2_rt]["tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_rt_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_rt_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2_rt) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2_rt][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2_rt.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_qt, user2_rt,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[(
                                                                                                      tweet1_qt.get_tweet_id(),
                                                                                                      tweet2_rt.get_tweet_id())])

                    tweet2_inner_quote_condition = tweet2_rt.is_quote_status_object_available()
                    if tweet2_inner_quote_condition:
                        tweet2_rt_qt = tweet2_rt.get_quote_status_object()
                        user2_rt_qt = tweet2_rt_qt.get_tweet_user().get_screen_name()
                        tweet2_rt_qt_urls = tweet2_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_qt.get_tweet_id() != tweet2_rt_qt.get_tweet_id():
                            if (user1_qt, user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"] and (
                                        tweet2_rt_qt.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_qt, user2_rt_qt][
                                            "tweets"]:
                                    for ut1 in tweet1_qt_urls:
                                        for ut2 in tweet2_rt_qt_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                            else:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_rt_qt_urls:
                                        if ut1 == ut2:
                                            if (user1_qt,
                                                user2_rt_qt) in user_level_cooccurrence_url_network.edges:
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt]["weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[
                                                    user1_qt, user2_rt_qt]["tweets"] += [
                                                    (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_url_network.add_edge(user1_qt,
                                                                                                  user2_rt_qt,
                                                                                                  weight=1,
                                                                                                  urls=ut1, tweets=[
                                                        (tweet1_qt.get_tweet_id(), tweet2_rt_qt.get_tweet_id())])

                if tweet1_retweet_condition:
                    tweet1_rt = tweet1.get_tweet_retweet_object()
                    user1_rt = tweet1_rt.get_tweet_user().get_screen_name()
                    tweet1_rt_urls = tweet1_rt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_rt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_rt, user2) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2]["tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_rt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                        "tweets"]:
                                for ut1 in tweet1_rt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for ut1 in tweet1_rt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1_rt, user2) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_rt, user2][
                                                "tweets"] += [
                                                (tweet1_rt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_rt, user2,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[
                                                                                                  (
                                                                                                  tweet1_rt.get_tweet_id(),
                                                                                                  tweet2.get_tweet_id())])

                    tweet1_inner_quote_condition = tweet1_rt.is_quote_status_object_available()
                    if tweet1_inner_quote_condition:
                        tweet1_rt_qt = tweet1_rt.get_quote_status_object()
                        user1_rt_qt = tweet1_rt_qt.get_tweet_user().get_screen_name()
                        tweet1_rt_qt_urls = tweet1_rt_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                        if tweet1_rt_qt.get_tweet_id() != tweet2.get_tweet_id():
                            if (user1_rt_qt, user2) in user_level_cooccurrence_url_network.edges:
                                if (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                            "tweets"] and (
                                        tweet2.get_tweet_id(), tweet1_rt_qt.get_tweet_id()) not in \
                                        user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                            "tweets"]:
                                    for ut1 in tweet1_rt_qt_urls:
                                        for ut2 in tweet2_urls:
                                            if ut1 == ut2:
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                            else:
                                for ut1 in tweet1_rt_qt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            if (
                                            user1_rt_qt, user2) in user_level_cooccurrence_url_network.edges:
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "weight"] += 1
                                                edge_label = "-" + ut1
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "urls"] += edge_label
                                                user_level_cooccurrence_url_network.edges[user1_rt_qt, user2][
                                                    "tweets"] += [
                                                    (tweet1_rt_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                            else:
                                                user_level_cooccurrence_url_network.add_edge(user1_rt_qt,
                                                                                                  user2, weight=1,
                                                                                                  urls=ut1,
                                                                                                  tweets=[(
                                                                                                          tweet1_rt_qt.get_tweet_id(),
                                                                                                          tweet2.get_tweet_id())])

                if tweet1_quote_condition:
                    tweet1_qt = tweet1.get_quote_status_object()
                    user1_qt = tweet1_qt.get_tweet_user().get_screen_name()
                    tweet1_qt_urls = tweet1_qt.get_tweet_urls().get_tweet_urls(return_format="expanded_url")

                    if tweet1_qt.get_tweet_id() != tweet2.get_tweet_id():
                        if (user1_qt, user2) in user_level_cooccurrence_url_network.edges:
                            if (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2]["tweets"] and (
                                    tweet2.get_tweet_id(), tweet1_qt.get_tweet_id()) not in \
                                    user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                        "tweets"]:
                                for ut1 in tweet1_qt_urls:
                                    for ut2 in tweet2_urls:
                                        if ut1 == ut2:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                        else:
                            for ut1 in tweet1_qt_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        if (user1_qt, user2) in user_level_cooccurrence_url_network.edges:
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "weight"] += 1
                                            edge_label = "-" + ut1
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "urls"] += edge_label
                                            user_level_cooccurrence_url_network.edges[user1_qt, user2][
                                                "tweets"] += [
                                                (tweet1_qt.get_tweet_id(), tweet2.get_tweet_id())]
                                        else:
                                            user_level_cooccurrence_url_network.add_edge(user1_qt, user2,
                                                                                              weight=1, urls=ut1,
                                                                                              tweets=[
                                                                                                  (
                                                                                                  tweet1_qt.get_tweet_id(),
                                                                                                  tweet2.get_tweet_id())])

                if tweet1.get_tweet_id() != tweet2.get_tweet_id():
                    if (user1, user2) in user_level_cooccurrence_url_network.edges:
                        if (tweet1.get_tweet_id(), tweet2.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1, user2][
                                    "tweets"] and (tweet2.get_tweet_id(), tweet1.get_tweet_id()) not in \
                                user_level_cooccurrence_url_network.edges[user1, user2]["tweets"]:
                            for ut1 in tweet1_urls:
                                for ut2 in tweet2_urls:
                                    if ut1 == ut2:
                                        user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1, user2][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                    else:
                        for ut1 in tweet1_urls:
                            for ut2 in tweet2_urls:
                                if ut1 == ut2:
                                    if (user1, user2) in user_level_cooccurrence_url_network.edges:
                                        user_level_cooccurrence_url_network.edges[user1, user2]["weight"] += 1
                                        edge_label = "-" + ut1
                                        user_level_cooccurrence_url_network.edges[user1, user2][
                                            "urls"] += edge_label
                                        user_level_cooccurrence_url_network.edges[user1, user2]["tweets"] += [
                                            (tweet1.get_tweet_id(), tweet2.get_tweet_id())]
                                    else:
                                        user_level_cooccurrence_url_network.add_edge(user1, user2, weight=1,
                                                                                          urls=ut1,
                                                                                          tweets=[
                                                                                              (tweet1.get_tweet_id(),
                                                                                               tweet2.get_tweet_id())])
                j += 1

        for edge in user_level_cooccurrence_url_network.edges:
            del user_level_cooccurrence_url_network.edges[edge]["tweets"]

        return user_level_cooccurrence_url_network
