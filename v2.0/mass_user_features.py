from tweet_text_analysis import TweetTextAnalysis


class MassUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name, temporal=False, spatial=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

        self._temporal = temporal
        self._spatial = spatial

    def users_followers_fraction(self, period=True, threshold=100):
        """
        This function finds the fraction of users whose followers number is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        followers number is equal to threshold, otherwise it counts the number of users whose
        followers number is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of followers.
        :return: a float number that shows the fraction of users whose followers number is equal or greater (depending on period)
        than threshold.
        """
        all_users = self.get_distinct_users()
        target = 0
        for user in all_users:
            if period:
                if user.get_followers_count() >= threshold:
                    target += 1
            else:
                if user.get_followers_count() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def users_friends_fraction(self, period=True, threshold=100):
        """
        This function finds the fraction of users whose friends (followee) number is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        friends number is equal to threshold, otherwise it counts the number of users whose
        friends number is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of friends.
        :return: a float number that shows the fraction of users whose friends number is equal or greater (depending on period)
        than threshold.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if period:
                if user.get_friends_count() >= threshold:
                    target += 1
            else:
                if user.get_friends_count() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def users_role_fraction(self, period=True, threshold=1):
        """
        This function finds the fraction of users whose role is equal or greater (depending on period)
        than threshold.
        :param period: if this boolean parameter is False, then he function counts the number of users whose
        role is equal to threshold, otherwise it counts the number of users whose
        role is equal or greater than the threshold.
        :param threshold: an integer number that shows the minimum of the user role.
        :return: a float number that shows the fraction of users whose role is equal or greater (depending on period)
        than threshold.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if period:
                if user.get_user_role() >= threshold:
                    target += 1
            else:
                if user.get_user_role() == threshold:
                    target += 1
        return target / self.distinct_users_count()

    def verified_users_fraction(self):
        """
        This function finds the fraction of verified users in the dataset.
        :return: a float number showing the fraction of verified users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.get_user_verification_status() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_location_fraction(self):
        """
        This function finds the fraction of geolocated users in the dataset.
        :return: a float number showing the fraction of geolocated users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_location() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_photo_fraction(self):
        """
        This function finds the fraction of users with profile picture in the dataset.
        :return: a float number showing the fraction of users with profile picture.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_picture() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_url_fraction(self):
        """
        This function finds the fraction of users with profile url in the dataset.
        :return: a float number showing the fraction of users with profile url.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_url() == True:
                target += 1
        return target / self.distinct_users_count()

    def users_with_description_fraction(self):
        """
        This function finds the fraction of users with profile description in the dataset.
        :return: a float number showing the fraction of users with profile description.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_has_profile_description() == True:
                target += 1
        return target / self.distinct_users_count()

    def protected_users_fraction(self):
        """
        This function finds the fraction of protected users in the dataset.
        :return: a float number showing the fraction of protected users.
        """
        target = 0
        all_users = self.get_distinct_users()
        for user in all_users:
            if user.user_protected_profile() == True:
                target += 1
        return target / self.distinct_users_count()

    def top_twitters(self, threshold_mode=True, threshold=5, top_k_mode=False, top_k=10):
        """
        This function finds either the users whose tweets number is more than the threshold (threshold-mode), or
        top k users with highest tweets number (top_k-mode).
        :param threshold_mode: a boolean parameter that activates threshhold-mode.
        :param threshold: an integer showing the threshhold of the threshold-mode.
        :param top_k_mode: a boolean parameter that activates top_k-mode.
        :param top_k: an integer showing the top_k in top_k-mode.
        :return:
        """
        assert (threshold_mode != top_k_mode), "Only one of the threshold-mode and top_k-mode can be active at the " \
                                               "same time."
        users = {}
        for tweet_id in self.tweets:
            tweet_id = self.tweets[tweet_id].get_id()
            user_id = self.tweets[tweet_id].get_twitter().get_user_id()
            users[user_id] = users.get(user_id, []) + [tweet_id]
        top_users = {user: len(users[user]) for user in users}

        if threshold_mode and not top_k_mode:
            return {user: top_users[user] for user in top_users if top_users[user] > threshold}
        elif top_k_mode and not threshold_mode:
            return {m[0]: m[1] for m in sorted(top_users.items(), key=lambda p: p[1], reverse=True)[:top_k]}

    def users_tweet_count_histogram(self):
        """
        This function counts the frequency of users for distinct number of tweets.
        :return: a sorted dictionary that maps frequency of users to tweet number.
        """
        all_users = self.top_twitters(threshold_mode=False, threshold=50, top_k_mode=True,
                                      top_k=self.distinct_users_count())
        histogram = {}
        for user in all_users:
            histogram[all_users[user]] = histogram.get(all_users[user], 0) + 1
        return {m[0]: m[1] for m in sorted(histogram.items(), key=lambda p: p[0])}

    def distinct_users_count(self):
        """
        This function counts the number of all distinct users who posted at least one tweet in the dataset.
        :return: an integer showing the number of distinct users
        """
        users = set()
        for tweet_id in self.tweets:
            users.add(self.tweets[tweet_id].get_twitter().get_user_id())
        return len(users)

    def get_distinct_users(self, output="users_list"):
        """
        This function gives all distinct users who posted at least one tweet in the dataset.
        :param output: the output can be "users_list" or "users_id", or "users_tweet_dictionary".
        :return: a list of all distinct users_object or user_ids.
        """

        assert (output in ["users_list", "id",
                           "users_tweet_dictionary"]), "the output paramater can be users_list or id, or " \
                                                       "users_tweet_dictionary"

        users = set()
        users_object = []
        users_tweet_dict = {}
        for tweet_id in self.tweets:
            user_obj = self.tweets[tweet_id].get_twitter()
            user_id = user_obj.get_user_id()
            if user_id not in users:
                users.add(user_id)
                users_object.append(user_obj)
            users_tweet_dict[user_id] = users_tweet_dict.get(user_id, []) + [self.tweets[tweet_id]]
        if output == "users_list":
            return users_object
        elif output == "id":
            return list(users)
        elif output == "users_tweet_dictionary":
            return users_tweet_dict
    # def get_users_with_duplicated_tweets(self):
    #     user_tweet_dict = {p:q for p,q in self.get_distinct_users(output="users_tweet_dictionary").items() if len(q)>1}
    #     users_redundant_dict = {}
    #     for user_id, tweet_list in user_tweet_dict.items():
    #         users_redundant_dict[user_id] = {}
    #         for pair in combinations(tweet_list, 2):
    #             dist = TwifexUtility.levenshtein_distance(pair[0], pair[1])
    #             if dist == 0:
    #                 users_redundant_dict[user_id][len(users_redundant_dict[user_id])+1] =

