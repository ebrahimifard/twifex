import networkx as nx


class UserNetwork:
    def __init__(self, tweets):
        self._tweets = tweets

    # retweet/quote/reply networks
    def user_level_retweet_network_building(self):
        user_level_retweet_network = nx.DiGraph()
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            source = tweet.get_tweet_user().get_screen_name()
            if retweet_condition:
                destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
                if user_level_retweet_network.has_edge(source, destination):
                    user_level_retweet_network.edges[source, destination]["weight"] += 1
                else:
                    user_level_retweet_network.add_edge(source, destination, kind="retweet", weight=1)
            else:
                user_level_retweet_network.add_node(source)

        return user_level_retweet_network

    def user_level_quote_network_building(self):
        user_level_quote_network = nx.DiGraph()
        for tweet in self._tweets:
            quote_condition = tweet.is_quote_status_object_available()

            source = tweet.get_tweet_user().get_screen_name()
            if quote_condition:
                destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                if user_level_quote_network.has_edge(source, destination):
                    user_level_quote_network.edges[source, destination]["weight"] += 1
                else:
                    user_level_quote_network.add_edge(source, destination, kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    inner_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if inner_destination is None:
                        inner_destination = "unknown"
                    if user_level_quote_network.has_edge(inner_source, inner_destination):
                        user_level_quote_network.edges[inner_source, inner_destination]["weight"] += 1
                    else:
                        user_level_quote_network.add_edge(inner_source, inner_destination, kind="quote", weight=1)
            else:
                user_level_quote_network.add_node(source)

        return user_level_quote_network

    def user_level_reply_network_building(self):
        user_level_reply_network = nx.DiGraph()
        for tweet in self._tweets:
            reply_condition = tweet.is_tweet_a_reply()

            source = tweet.get_tweet_user().get_screen_name()
            if reply_condition:
                destination = tweet.get_tweet_in_reply_to_screen_name()
                if user_level_reply_network.has_edge(source, destination):
                    user_level_reply_network.edges[source, destination]["weight"] += 1
                else:
                    user_level_reply_network.add_edge(source, destination, kind="reply", weight=1)
            else:
                user_level_reply_network.add_node(source)

        return user_level_reply_network

    # quote-reply/retweet-reply/retweet-quote networks
    def user_level_quote_reply_network_building(self):
        user_level_quote_reply_network = nx.MultiDiGraph()
        quote_reply_key_keepers = {}

        for tweet in self._tweets:
            quote_condition = tweet.is_quote_status_object_available()
            reply_condition = tweet.is_tweet_a_reply()

            key_code = 0
            source = tweet.get_tweet_user().get_screen_name()

            if quote_condition is True and reply_condition is True:
                quote_destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()

                if (source, quote_destination, "quote") in quote_reply_key_keepers.keys():
                    user_level_quote_reply_network.edges[
                        source, quote_destination, quote_reply_key_keepers[
                            (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    user_level_quote_reply_network.add_edge(source, quote_destination,
                                                                 key=quote_reply_key_keepers[
                                                                     (source, quote_destination, "quote")],
                                                                 kind="quote", weight=1)

                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in quote_reply_key_keepers.keys():
                    user_level_quote_reply_network.edges[
                        source, reply_destination, quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_quote_reply_network.add_edge(source, reply_destination,
                                                                 key=quote_reply_key_keepers[
                                                                     (source, reply_destination, "reply")],
                                                                 kind="reply", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    inner_quote_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if inner_quote_destination is None:
                        inner_quote_destination = "unknown"
                    if (
                            inner_source, inner_quote_destination, "quote") in quote_reply_key_keepers.keys():
                        user_level_quote_reply_network.edges[
                            inner_source, inner_quote_destination, quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                     key=quote_reply_key_keepers[
                                                                         (inner_source, inner_quote_destination,
                                                                          "quote")],
                                                                     kind="quote", weight=1)
                    inner_reply_condition = tweet.get_quote_status_object().is_tweet_a_reply()
                    if inner_reply_condition:
                        inner_reply_destination = tweet.get_quote_status_object().get_tweet_in_reply_to_screen_name()
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in quote_reply_key_keepers.keys():
                            user_level_quote_reply_network.edges[
                                inner_source, inner_reply_destination, quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                         key=quote_reply_key_keepers[
                                                                             (inner_source, inner_reply_destination,
                                                                              "reply")],
                                                                         kind="reply", weight=1)

            elif quote_condition is True and reply_condition is False:
                quote_destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()

                if (source, quote_destination, "quote") in quote_reply_key_keepers.keys():
                    user_level_quote_reply_network.edges[
                        source, quote_destination, quote_reply_key_keepers[
                            (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    user_level_quote_reply_network.add_edge(source, quote_destination,
                                                                 key=quote_reply_key_keepers[
                                                                     (source, quote_destination, "quote")],
                                                                 kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    inner_source = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                    inner_quote_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if inner_quote_destination is None:
                        inner_quote_destination = "unknown"
                    if (inner_source, inner_quote_destination, "quote") in quote_reply_key_keepers.keys():
                        user_level_quote_reply_network.edges[
                            inner_source, inner_quote_destination, quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        quote_reply_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                     key=quote_reply_key_keepers[
                                                                         (inner_source, inner_quote_destination,
                                                                          "quote")],
                                                                     kind="quote", weight=1)
                    inner_reply_destination = tweet.get_quote_status_object().get_tweet_in_reply_to_screen_name()
                    if inner_reply_destination:
                        if (
                                inner_source, inner_reply_destination,
                                "reply") in quote_reply_key_keepers.keys():
                            user_level_quote_reply_network.edges[
                                inner_source, inner_reply_destination, quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            user_level_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                         key=quote_reply_key_keepers[
                                                                             (inner_source, inner_reply_destination,
                                                                              "reply")],
                                                                         kind="reply", weight=1)

            elif quote_condition is False and reply_condition is True:
                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in quote_reply_key_keepers.keys():
                    user_level_quote_reply_network.edges[
                        source, reply_destination, quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_quote_reply_network.add_edge(source, reply_destination,
                                                                 key=quote_reply_key_keepers[
                                                                     (source, reply_destination, "reply")],
                                                                 kind="reply", weight=1)

            elif quote_condition is False and reply_condition is False:
                user_level_quote_reply_network.add_node(source)

        return user_level_quote_reply_network

    def user_level_retweet_reply_network_building(self):
        user_level_retweet_reply_network = nx.MultiDiGraph()
        retweet_reply_key_keepers = {}
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            reply_condition = tweet.is_tweet_a_reply()

            key_code = 0
            source = tweet.get_tweet_user().get_screen_name()

            if retweet_condition is True and reply_condition is True:
                retweet_destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()

                if (source, retweet_destination, "retweet") in retweet_reply_key_keepers.keys():
                    user_level_retweet_reply_network.edges[
                        source, retweet_destination, retweet_reply_key_keepers[
                            (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    user_level_retweet_reply_network.add_edge(source, retweet_destination,
                                                                   key=retweet_reply_key_keepers[
                                                                       (source, retweet_destination, "retweet")],
                                                                   kind="retweet", weight=1)

                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in retweet_reply_key_keepers.keys():
                    user_level_retweet_reply_network.edges[
                        source, reply_destination, retweet_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_retweet_reply_network.add_edge(source, reply_destination,
                                                                   key=retweet_reply_key_keepers[
                                                                       (source, reply_destination, "reply")],
                                                                   kind="reply", weight=1)

                inner_reply_condition = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                if inner_reply_condition:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_tweet_retweet_object().get_tweet_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_reply_key_keepers.keys():
                        user_level_retweet_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                       key=retweet_reply_key_keepers[
                                                                           (inner_source, inner_reply_destination,
                                                                            "reply")],
                                                                       kind="reply", weight=1)

            elif retweet_condition is True and reply_condition is False:
                retweet_destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()

                if (source, retweet_destination, "retweet") in retweet_reply_key_keepers.keys():
                    user_level_retweet_reply_network.edges[
                        source, retweet_destination, retweet_reply_key_keepers[
                            (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    retweet_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    user_level_retweet_reply_network.add_edge(source, retweet_destination,
                                                                   key=retweet_reply_key_keepers[
                                                                       (source, retweet_destination, "retweet")],
                                                                   kind="retweet", weight=1)

                inner_reply_condition = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                if inner_reply_condition:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_tweet_retweet_object().get_tweet_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_reply_key_keepers.keys():
                        user_level_retweet_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                       key=retweet_reply_key_keepers[
                                                                           (inner_source, inner_reply_destination,
                                                                            "reply")],
                                                                       kind="reply", weight=1)

            elif retweet_condition is False and reply_condition is True:
                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in retweet_reply_key_keepers.keys():
                    user_level_retweet_reply_network.edges[
                        source, reply_destination, retweet_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    retweet_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_retweet_reply_network.add_edge(source, reply_destination,
                                                                   key=retweet_reply_key_keepers[
                                                                       (source, reply_destination, "reply")],
                                                                   kind="reply", weight=1)

            elif retweet_condition is False and reply_condition is False:
                user_level_retweet_reply_network.add_node(source)

        return user_level_retweet_reply_network

    def user_level_retweet_quote_network_building(self):
        user_level_retweet_quote_network = nx.MultiDiGraph()
        retweet_quote_key_keepers = {}
        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            quote_condition = tweet.is_quote_status_object_available()

            key_code = 0
            source = tweet.get_tweet_user().get_screen_name()

            #The following condition is impossible so we skip it
            # if retweet_condition is True and quote_condition is True:

            if retweet_condition is True and quote_condition is False:
                retweet_destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()

                if (source, retweet_destination, "retweet") in retweet_quote_key_keepers.keys():
                    user_level_retweet_quote_network.edges[
                        source, retweet_destination, retweet_quote_key_keepers[
                            (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    retweet_quote_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    user_level_retweet_quote_network.add_edge(source, retweet_destination,
                                                                   key=retweet_quote_key_keepers[
                                                                       (source, retweet_destination, "retweet")],
                                                                   kind="retweet", weight=1)

                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_quote_status_object_available()
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()

                    if (inner_source, inner_quote_destination, "quote") in retweet_quote_key_keepers.keys():
                        user_level_retweet_quote_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
                                                                       key=retweet_quote_key_keepers[
                                                                           (inner_source, inner_quote_destination,
                                                                            "quote")],
                                                                       kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    if inner_quote_condition_level_two:
                        inner_source_level_two = inner_quote_destination
                        inner_quote_destination_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().get_inner_quote_screen_name()
                        if inner_quote_destination_level_two is None:
                            inner_quote_destination_level_two = "unknown"
                        if (inner_source_level_two, inner_quote_destination_level_two,
                            "quote") in retweet_quote_key_keepers.keys():
                            user_level_retweet_quote_network.edges[
                                inner_source_level_two, inner_quote_destination_level_two,
                                retweet_quote_key_keepers[
                                    (inner_source_level_two, inner_quote_destination_level_two, "quote")]][
                                "weight"] += 1
                        else:
                            retweet_quote_key_keepers[
                                (inner_source_level_two, inner_quote_destination_level_two, "quote")] = key_code
                            key_code += 1
                            user_level_retweet_quote_network.add_edge(inner_source_level_two,
                                                                           inner_quote_destination_level_two,
                                                                           key=retweet_quote_key_keepers[
                                                                               (inner_source_level_two,
                                                                                inner_quote_destination_level_two,
                                                                                "quote")],
                                                                           kind="quote", weight=1)

            elif retweet_condition is False and quote_condition is True:
                quote_destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
                if (source, quote_destination, "quote") in retweet_quote_key_keepers.keys():
                    user_level_retweet_quote_network.edges[
                        source, quote_destination, retweet_quote_key_keepers[
                            (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    retweet_quote_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    user_level_retweet_quote_network.add_edge(source, quote_destination,
                                                                   key=retweet_quote_key_keepers[
                                                                       (source, quote_destination, "quote")],
                                                                   kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if inner_quote_destination is None:
                        inner_quote_destination = "unknown"
                    if (inner_source, inner_quote_destination, "quote") in retweet_quote_key_keepers.keys():
                        user_level_retweet_quote_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_key_keepers[(inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_network.add_edge(inner_source, inner_quote_destination,
                                                                       key=retweet_quote_key_keepers[
                                                                           (inner_source, inner_quote_destination,
                                                                            "quote")],
                                                                       kind="quote", weight=1)

            elif retweet_condition is False and quote_condition is False:
                user_level_retweet_quote_network.add_node(source)

        return user_level_retweet_quote_network

    # retweet-quote-reply network
    def user_level_retweet_quote_reply_network_building(self):
        user_level_retweet_quote_reply_network = nx.MultiDiGraph()
        retweet_quote_reply_key_keepers = {}

        for tweet in self._tweets:
            retweet_condition = tweet.is_tweet_retweeted()
            quote_condition = tweet.is_quote_status_object_available()
            reply_condition = tweet.is_tweet_a_reply()

            key_code = 0
            source = tweet.get_tweet_user().get_screen_name()

            if retweet_condition is True and quote_condition is False and reply_condition is True:
                retweet_destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()

                if (source, retweet_destination, "retweet") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, retweet_destination, retweet_quote_reply_key_keepers[
                            (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, retweet_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, retweet_destination,
                                                                              "retweet")], kind="retweet", weight=1)

                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, reply_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, reply_destination, "reply")],
                                                                         kind="reply", weight=1)

                inner_reply_condition_level_one = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_quote_status_object_available()

                if inner_reply_condition_level_one:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_tweet_retweet_object().get_tweet_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_reply_destination,
                                                                                  "reply")],
                                                                             kind="reply", weight=1)
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_quote_destination,
                                                                                  "quote")],
                                                                             kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    inner_reply_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_a_reply()

                    if inner_reply_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_reply_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_in_reply_to_screen_name()

                        if (
                                inner_source, inner_reply_destination,
                                "reply") in retweet_quote_reply_key_keepers.keys():
                            user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                                 inner_reply_destination,
                                                                                 key=
                                                                                 retweet_quote_reply_key_keepers[
                                                                                     (inner_source,
                                                                                      inner_reply_destination,
                                                                                      "reply")],
                                                                                 kind="reply", weight=1)
                    if inner_quote_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_quote_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_inner_quote_screen_name()
                        if inner_quote_destination is None:
                            inner_quote_destination = "unknown"
                        if (
                                inner_source, inner_quote_destination,
                                "quote") in retweet_quote_reply_key_keepers.keys():
                            user_level_retweet_quote_reply_network.edges[
                                source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                    (source, inner_quote_destination, "quote")]][
                                "weight"] += 1
                        else:
                            retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")] = key_code
                            key_code += 1
                            user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                                 inner_quote_destination,
                                                                                 key=
                                                                                 retweet_quote_reply_key_keepers[
                                                                                     (inner_source,
                                                                                      inner_quote_destination,
                                                                                      "quote")],
                                                                                 kind="quote", weight=1)
            elif retweet_condition is True and quote_condition is False and reply_condition is False:
                retweet_destination = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()

                if (source, retweet_destination, "retweet") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, retweet_destination, retweet_quote_reply_key_keepers[
                            (source, retweet_destination, "retweet")]]["weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, retweet_destination, "retweet")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, retweet_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, retweet_destination,
                                                                              "retweet")], kind="retweet",
                                                                         weight=1)

                inner_reply_condition_level_one = tweet.get_tweet_retweet_object().is_tweet_a_reply()
                inner_quote_condition_level_one = tweet.get_tweet_retweet_object().is_quote_status_object_available()

                if inner_reply_condition_level_one:
                    inner_source = retweet_destination
                    inner_reply_destination = tweet.get_tweet_retweet_object().get_tweet_in_reply_to_screen_name()

                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_reply_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_reply_destination,
                                                                                  "reply")],
                                                                             kind="reply", weight=1)
                if inner_quote_condition_level_one:
                    inner_source = retweet_destination
                    inner_quote_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_user().get_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_quote_destination,
                                                                                  "quote")],
                                                                             kind="quote", weight=1)

                    inner_quote_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_quoted()
                    inner_reply_condition_level_two = tweet.get_tweet_retweet_object().get_quote_status_object().is_tweet_a_reply()

                    if inner_reply_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_reply_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_tweet_in_reply_to_screen_name()

                        if (
                                inner_source, inner_reply_destination,
                                "reply") in retweet_quote_reply_key_keepers.keys():
                            user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                    (inner_source, inner_reply_destination, "reply")]][
                                "weight"] += 1
                        else:
                            retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")] = key_code
                            key_code += 1
                            user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                                 inner_reply_destination,
                                                                                 key=
                                                                                 retweet_quote_reply_key_keepers[
                                                                                     (inner_source,
                                                                                      inner_reply_destination,
                                                                                      "reply")],
                                                                                 kind="reply", weight=1)
                    if inner_quote_condition_level_two:
                        inner_source = inner_quote_destination
                        inner_quote_destination = tweet.get_tweet_retweet_object().get_quote_status_object().get_inner_quote_screen_name()
                        if inner_quote_destination is None:
                            inner_quote_destination = "unknown"
                        if (
                                inner_source, inner_quote_destination,
                                "quote") in retweet_quote_reply_key_keepers.keys():
                            user_level_retweet_quote_reply_network.edges[
                                inner_source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                    (inner_source, inner_quote_destination, "quote")]][
                                "weight"] += 1
                        else:
                            retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")] = key_code
                            key_code += 1
                            user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                                 inner_quote_destination,
                                                                                 key=
                                                                                 retweet_quote_reply_key_keepers[
                                                                                     (inner_source,
                                                                                      inner_quote_destination,
                                                                                      "quote")],
                                                                                 kind="quote", weight=1)
            elif retweet_condition is False and quote_condition is True and reply_condition is True:
                quote_destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()

                if (source, quote_destination, "quote") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, quote_destination, retweet_quote_reply_key_keepers[
                            (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, quote_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, quote_destination, "quote")],
                                                                         kind="quote", weight=1)

                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, reply_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, reply_destination, "reply")],
                                                                         kind="reply", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                inner_reply_condition = tweet.get_quote_status_object().is_tweet_a_reply()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_quote_destination,
                                                                                  "quote")],
                                                                             kind="quote", weight=1)
                if inner_reply_condition:
                    inner_source = quote_destination
                    inner_reply_destination = tweet.get_quote_status_object().get_tweet_in_reply_to_screen_name()
                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                             inner_reply_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_reply_destination,
                                                                                  "reply")],
                                                                             kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is True and reply_condition is False:
                quote_destination = tweet.get_quote_status_object().get_tweet_user().get_screen_name()

                if (source, quote_destination, "quote") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, quote_destination, retweet_quote_reply_key_keepers[
                            (source, quote_destination, "quote")]]["weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, quote_destination, "quote")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, quote_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, quote_destination, "quote")],
                                                                         kind="quote", weight=1)

                inner_quote_condition = tweet.get_quote_status_object().is_tweet_quoted()
                inner_reply_condition = tweet.get_quote_status_object().is_tweet_a_reply()
                if inner_quote_condition:
                    inner_source = quote_destination
                    inner_quote_destination = tweet.get_quote_status_object().get_inner_quote_screen_name()
                    if (
                            inner_source, inner_quote_destination,
                            "quote") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_quote_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_quote_destination, "quote")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_quote_destination, "quote")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source, inner_quote_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_quote_destination,
                                                                                  "quote")],
                                                                             kind="quote", weight=1)
                if inner_reply_condition:
                    inner_source = quote_destination
                    inner_reply_destination = tweet.get_quote_status_object().get_tweet_in_reply_to_screen_name()
                    if (
                            inner_source, inner_reply_destination,
                            "reply") in retweet_quote_reply_key_keepers.keys():
                        user_level_retweet_quote_reply_network.edges[
                            inner_source, inner_reply_destination, retweet_quote_reply_key_keepers[
                                (inner_source, inner_reply_destination, "reply")]][
                            "weight"] += 1
                    else:
                        retweet_quote_reply_key_keepers[
                            (inner_source, inner_reply_destination, "reply")] = key_code
                        key_code += 1
                        user_level_retweet_quote_reply_network.add_edge(inner_source,
                                                                             inner_reply_destination,
                                                                             key=
                                                                             retweet_quote_reply_key_keepers[
                                                                                 (inner_source,
                                                                                  inner_reply_destination,
                                                                                  "reply")],
                                                                             kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is False and reply_condition is True:
                reply_destination = tweet.get_tweet_in_reply_to_screen_name()
                if (source, reply_destination, "reply") in retweet_quote_reply_key_keepers.keys():
                    user_level_retweet_quote_reply_network.edges[
                        source, reply_destination, retweet_quote_reply_key_keepers[
                            (source, reply_destination, "reply")]][
                        "weight"] += 1
                else:
                    retweet_quote_reply_key_keepers[(source, reply_destination, "reply")] = key_code
                    key_code += 1
                    user_level_retweet_quote_reply_network.add_edge(source, reply_destination,
                                                                         key=retweet_quote_reply_key_keepers[
                                                                             (source, reply_destination, "reply")],
                                                                         kind="reply", weight=1)
            elif retweet_condition is False and quote_condition is False and reply_condition is False:
                user_level_retweet_quote_reply_network.add_node(source)

        return user_level_retweet_quote_reply_network

