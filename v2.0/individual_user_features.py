from tweet_text_analysis import TweetTextAnalysis
import re
import numpy as np
from datetime import datetime


class IndividualUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name, retweet_flag=False, quote_flag=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()
        self._retweet_flag = retweet_flag
        self._quote_flag = quote_flag
        
    #screen_name
    def user_screen_name_length(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_length"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_length"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_length"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            screen_name_length = len(screen_name)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = screen_name_length

    def user_screen_name_digits_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_digits_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_digits_count"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_digits_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[0-9]'
            screen_name_digits_count = len(re.findall(pat, screen_name))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = screen_name_digits_count

    def user_screen_name_letters_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_letters_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_letters_count"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_letters_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[a-zA-Z]'
            screen_name_letters_count = len(re.findall(pat, screen_name))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = screen_name_letters_count

    def user_screen_name_digits_to_letter_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_digits_to_letter_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_digits_to_letter_fraction"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_digits_to_letter_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat1 = r'[0-9]'
            pat2 = r'[a-zA-Z]'
            digits_count = len(re.findall(pat1, screen_name))
            letters_count = len(re.findall(pat2, screen_name))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = digits_count / letters_count if letters_count != 0 else None

    def user_screen_name_maximum_adjacent_letters_to_all_letters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_maximum_adjacent_letters_to_all_letters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_maximum_adjacent_letters_to_all_letters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_maximum_adjacent_letters_to_all_letters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat1 = r'[a-zA-Z]'
            pat2 = r'[a-zA-Z]+'
            letters_count = len(re.findall(pat1, screen_name))
            max_adjacent_letters = max([len(sequence) for sequence in re.findall(pat2, screen_name)])
            self._tweets_features[tweet.get_tweet_id()][feature_id] = max_adjacent_letters / letters_count if letters_count != 0 else None

    def user_screen_name_maximum_adjacent_digits_to_all_digits_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_maximum_adjacent_digits_to_all_digits_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_maximum_adjacent_digits_to_all_digits_fraction"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_maximum_adjacent_digits_to_all_digits_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat1 = r'[0-9]'
            pat2 = r'[0-9]+'
            digits_count = len(re.findall(pat1, screen_name))
            adjacent_digits_list = re.findall(pat2, screen_name)
            max_adjacent_digits = max([len(sequence) for sequence in adjacent_digits_list]) if adjacent_digits_list else 0
            self._tweets_features[tweet.get_tweet_id()][feature_id] = max_adjacent_digits / digits_count if digits_count != 0 else None

    def user_screen_name_average_distance_between_subsequent_letters(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_average_distance_between_subsequent_letters"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_average_distance_between_subsequent_letters"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_average_distance_between_subsequent_letters"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[a-zA-Z]'
            letters_count = len(re.findall(pat, screen_name))
            occurrences = [(m.start(), m.end()) for m in re.finditer(pat, screen_name)]
            distance_between_subsequent_letters_sum = 0
            counter = 1
            for index, element in enumerate(occurrences):
                if counter < len(occurrences):
                    diff = occurrences[index + 1][0] - occurrences[index][1]
                    distance_between_subsequent_letters_sum += diff
                    counter += 1
            self._tweets_features[tweet.get_tweet_id()][feature_id] = distance_between_subsequent_letters_sum / letters_count if letters_count != 0 else None

    def user_screen_name_average_distance_between_subsequent_digits(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_average_distance_between_subsequent_digits"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_average_distance_between_subsequent_digits"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_average_distance_between_subsequent_digits"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[0-9]'
            digits_count = len(re.findall(pat, screen_name))
            occurrences = [(m.start(), m.end()) for m in re.finditer(pat, screen_name)]
            distance_between_subsequent_digits_sum = 0
            counter = 1
            for index, element in enumerate(occurrences):
                if counter < len(occurrences):
                    diff = occurrences[index + 1][0] - occurrences[index][1]
                    distance_between_subsequent_digits_sum += diff
                    counter += 1
            self._tweets_features[tweet.get_tweet_id()][feature_id] = distance_between_subsequent_digits_sum / digits_count if digits_count != 0 else None

    def user_screen_name_vowels_to_all_letters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_vowels_to_all_letters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_vowels_to_all_letters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_vowels_to_all_letters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat1 = r'[a-zA-Z]'
            pat2 = r'[aeiouAEIOU]'
            letters_count = len(re.findall(pat1, screen_name))
            vowels_count = len(re.findall(pat2, screen_name))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = vowels_count / letters_count if letters_count != 0 else None

    def user_screen_name_average_distance_between_subsequent_vowels(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_average_distance_between_subsequent_vowels"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_average_distance_between_subsequent_vowels"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_average_distance_between_subsequent_vowels"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[aeiouAEIOU]'
            vowels_count = len(re.findall(pat, screen_name))
            occurrences = [(m.start(), m.end()) for m in re.finditer(pat, screen_name)]
            distance_between_subsequent_vowels_sum = 0
            counter = 1
            for index, element in enumerate(occurrences):
                if counter < len(occurrences):
                    diff = occurrences[index + 1][0] - occurrences[index][1]
                    distance_between_subsequent_vowels_sum += diff
                    counter += 1
            self._tweets_features[tweet.get_tweet_id()][feature_id] = distance_between_subsequent_vowels_sum / vowels_count if vowels_count != 0 else None

    def user_screen_name_average_distance_between_subsequent_consonants(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[
                feature_id] = "retweet_" + "user_screen_name_average_distance_between_subsequent_consonants"
        elif self._quote_flag:
            self._features_id_name_dict[
                feature_id] = "quote_" + "user_screen_name_average_distance_between_subsequent_consonants"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_average_distance_between_subsequent_consonants"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            pat = r'[BCDFGJKLMNPQSTVXZHRWYbcdfgjklmnpqstvxzhrwy]'
            consonants_count = len(re.findall(pat, screen_name))
            occurrences = [(m.start(), m.end()) for m in re.finditer(pat, screen_name)]
            distance_between_subsequent_consonants_sum = 0
            counter = 1
            for index, element in enumerate(occurrences):
                if counter < len(occurrences):
                    diff = occurrences[index + 1][0] - occurrences[index][1]
                    distance_between_subsequent_consonants_sum += diff
                    counter += 1
            self._tweets_features[tweet.get_tweet_id()][feature_id] = distance_between_subsequent_consonants_sum / consonants_count if consonants_count != 0 else None

    def user_screen_name_non_alphanumeric_to_all_characters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_screen_name_non_alphanumeric_to_all_characters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_screen_name_non_alphanumeric_to_all_characters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "user_screen_name_non_alphanumeric_to_all_characters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            screen_name = user_obj.get_screen_name()
            screen_name_length = self._text_analysis.text_length(input_text=screen_name, length_unit="character")
            non_alphanumeric_characters_count = self._text_analysis.special_character_count(character="_", input_text=screen_name)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = non_alphanumeric_characters_count / screen_name_length if screen_name_length != 0 else None

    #protected
    def user_is_account_protected(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_is_account_protected"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_is_account_protected"
        else:
            self._features_id_name_dict[feature_id] = "user_is_account_protected"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.is_user_protected()

    #verified
    def user_is_account_verified(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_is_account_verified"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_is_account_verified"
        else:
            self._features_id_name_dict[feature_id] = "user_is_account_verified"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.is_user_verified()

    #followers/followees count
    def user_followers_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_followers_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_followers_count"
        else:
            self._features_id_name_dict[feature_id] = "user_followers_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.get_user_followers_count()

    def user_followees_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_followees_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_followees_count"
        else:
            self._features_id_name_dict[feature_id] = "user_followees_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.get_user_friends_count()

    def user_role(self):
        """
        user role measures the ratio of followers to followees of a user. A user with a high follower to followee ratio
        is a broadcaster. Conversely, a user with a low follower to followee ratio is a receiver.
        :return: a float number showing the ratio of followers to friends.
        """
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_role"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_role"
        else:
            self._features_id_name_dict[feature_id] = "user_role"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            followers_count = user_obj.get_user_followers_count()
            followees_count = user_obj.get_user_friends_count()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = followers_count / followees_count if followees_count != 0 else None

    def user_reputation(self):
        """
        this function measures the relative importance of a user on Twitter. The reputation is defined as the ratio
        between the number of friends and the number of followers as: (followers #) / (followers # + friends #).
        :return: a float number showing the ratio (followers #) / (followers # + friends #).
        """
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_reputation"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_reputation"
        else:
            self._features_id_name_dict[feature_id] = "user_reputation"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            followers_count = user_obj.get_user_followers_count()
            followees_count = user_obj.get_user_friends_count()
            self._tweets_features[tweet.get_tweet_id()][feature_id] = followers_count / (followees_count + followers_count) if (followees_count + followers_count) != 0 else None

    def user_status_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_status_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_status_count"
        else:
            self._features_id_name_dict[feature_id] = "user_status_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.get_user_statuses_count()

    def user_likes_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_likes_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_likes_count"
        else:
            self._features_id_name_dict[feature_id] = "user_likes_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_obj.get_user_favourites_count()

    #creation_time
    def user_account_age(self, reference_datetime="now", age_unit="days"):
        """
        This function calculates the age of the account until today with the resolution of day.
        :return: the account age with the resolution of day.
        """

        assert (age_unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                    " resolution " \
                                                                                                    "should be" \
                                                                                                    " years," \
                                                                                                    " months," \
                                                                                                    " weeks, " \
                                                                                                    "days, " \
                                                                                                    "hours," \
                                                                                                    " minutes," \
                                                                                                    " or seconds"

        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"user_account_age_from_{reference_datetime}_in_{age_unit}"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_account_age_from_{reference_datetime}_in_{age_unit}"
        else:
            self._features_id_name_dict[feature_id] = "user_account_age_from_{reference_datetime}_in_{age_unit}"

        if reference_datetime == "now":
            age_baseline = datetime.now()
        else:
            age_baseline = datetime.strptime(reference_datetime, "%d-%m-%Y %H:%M:%S")

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            account_creation_time = user_obj.get_user_creation_time()
            account_creation_time_no_timezone = datetime.strptime(account_creation_time.strftime("%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
            user_age = eval(f"(age_baseline - account_creation_time_no_timezone).{age_unit}")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_age

    def user_average_follow_speed(self, reference_datetime="now", age_unit="days"):
        """
        this function calculates the average speed of this account in following other Twitter accounts.
        :return: a float number showing the average follow speed in this account.
        """

        assert (age_unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                    " resolution " \
                                                                                                    "should be" \
                                                                                                    " years," \
                                                                                                    " months," \
                                                                                                    " weeks, " \
                                                                                                    "days, " \
                                                                                                    "hours," \
                                                                                                    " minutes," \
                                                                                                    " or seconds"

        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"user_average_follow_speed_from_{reference_datetime}_in_{age_unit}"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + f"user_average_follow_speed_from_{reference_datetime}_in_{age_unit}"
        else:
            self._features_id_name_dict[feature_id] = f"user_average_follow_speed_from_{reference_datetime}_in_{age_unit}"

        if reference_datetime == "now":
            age_baseline = datetime.now()
        else:
            age_baseline = datetime.strptime(reference_datetime, "%d-%m-%Y %H:%M:%S")

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            followers_count = user_obj.get_user_followers_count()
            account_creation_time = user_obj.get_user_creation_time()
            account_creation_time_no_timezone = datetime.strptime(account_creation_time.strftime("%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
            user_age = eval(f"(age_baseline - account_creation_time_no_timezone).{age_unit}")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = followers_count / user_age if user_age !=0 else None

    def user_being_followed_speed(self, reference_datetime="now", age_unit="days"):
        """
        this function calculates the average speed of being followed by other accounts.
        :return: a float number showing the average speed of being followed by other accounts.
        """

        assert (age_unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                  " resolution " \
                                                                                                  "should be" \
                                                                                                  " years," \
                                                                                                  " months," \
                                                                                                  " weeks, " \
                                                                                                  "days, " \
                                                                                                  "hours," \
                                                                                                  " minutes," \
                                                                                                  " or seconds"

        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[
                feature_id] = "retweet_" + f"user_being_followed_speed_from_{reference_datetime}_in_{age_unit}"
        elif self._quote_flag:
            self._features_id_name_dict[
                feature_id] = "quote_" + f"user_being_followed_speed_from_{reference_datetime}_in_{age_unit}"
        else:
            self._features_id_name_dict[
                feature_id] = f"user_being_followed_speed_from_{reference_datetime}_in_{age_unit}"

        if reference_datetime == "now":
            age_baseline = datetime.now()
        else:
            age_baseline = datetime.strptime(reference_datetime, "%d-%m-%Y %H:%M:%S")

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            followees_count = user_obj.get_user_friends_count()
            account_creation_time = user_obj.get_user_creation_time()
            account_creation_time_no_timezone = datetime.strptime(account_creation_time.strftime("%d-%m-%Y %H:%M:%S"),"%d-%m-%Y %H:%M:%S")
            user_age = eval(f"(age_baseline - account_creation_time_no_timezone).{age_unit}")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = followees_count / user_age if user_age != 0 else None

    def user_average_like_speed(self, reference_datetime="now", age_unit="days"):
        """
        this function calculates the average speed of this account in liking tweets.
        :return: a float number showing the average like speed in this account.
        """
        assert (age_unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                  " resolution " \
                                                                                                  "should be" \
                                                                                                  " years," \
                                                                                                  " months," \
                                                                                                  " weeks, " \
                                                                                                  "days, " \
                                                                                                  "hours," \
                                                                                                  " minutes," \
                                                                                                  " or seconds"

        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[
                feature_id] = "retweet_" + f"user_average_like_speed_from_{reference_datetime}_in_{age_unit}"
        elif self._quote_flag:
            self._features_id_name_dict[
                feature_id] = "quote_" + f"user_average_like_speed_from_{reference_datetime}_in_{age_unit}"
        else:
            self._features_id_name_dict[
                feature_id] = f"user_average_like_speed_from_{reference_datetime}_in_{age_unit}"

        if reference_datetime == "now":
            age_baseline = datetime.now()
        else:
            age_baseline = datetime.strptime(reference_datetime, "%d-%m-%Y %H:%M:%S")

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            likes_count = user_obj.get_user_favourites_count()
            account_creation_time = user_obj.get_user_creation_time()
            account_creation_time_no_timezone = datetime.strptime(account_creation_time.strftime("%d-%m-%Y %H:%M:%S"),"%d-%m-%Y %H:%M:%S")
            user_age = eval(f"(age_baseline - account_creation_time_no_timezone).{age_unit}")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = likes_count / user_age if user_age != 0 else None

    # Check for division by zero error (accounts with the age of zero)?
    def user_average_status_speed(self, reference_datetime="now", age_unit="days"):
        """
        this function calculates the average speed of this account in posting tweets.
        :return: a float number showing the average tweet speed in this account.
        """
        assert (age_unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]), "The time" \
                                                                                                  " resolution " \
                                                                                                  "should be" \
                                                                                                  " years," \
                                                                                                  " months," \
                                                                                                  " weeks, " \
                                                                                                  "days, " \
                                                                                                  "hours," \
                                                                                                  " minutes," \
                                                                                                  " or seconds"

        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[
                feature_id] = "retweet_" + f"user_average_status_speed_from_{reference_datetime}_in_{age_unit}"
        elif self._quote_flag:
            self._features_id_name_dict[
                feature_id] = "quote_" + f"user_average_status_speed_from_{reference_datetime}_in_{age_unit}"
        else:
            self._features_id_name_dict[
                feature_id] = f"user_average_status_speed_from_{reference_datetime}_in_{age_unit}"

        if reference_datetime == "now":
            age_baseline = datetime.now()
        else:
            age_baseline = datetime.strptime(reference_datetime, "%d-%m-%Y %H:%M:%S")

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            status_count = user_obj.get_user_statuses_count()
            account_creation_time = user_obj.get_user_creation_time()
            account_creation_time_no_timezone = datetime.strptime(account_creation_time.strftime("%d-%m-%Y %H:%M:%S"),"%d-%m-%Y %H:%M:%S")
            user_age = eval(f"(age_baseline - account_creation_time_no_timezone).{age_unit}")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = status_count / user_age if user_age != 0 else None

    def user_has_profile_picture(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_has_profile_picture"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_has_profile_picture"
        else:
            self._features_id_name_dict[feature_id] = "user_has_profile_picture"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if user_obj.get_profile_image_url() is not None else False

    def user_has_profile_banner(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_has_profile_banner"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_has_profile_banner"
        else:
            self._features_id_name_dict[feature_id] = "user_has_profile_banner"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if user_obj.get_profile_banner_url() is not None else False

    def user_has_profile_description(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_has_profile_description"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_has_profile_description"
        else:
            self._features_id_name_dict[feature_id] = "user_has_profile_description"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            user_description = user_obj.get_user_description()
            if user_description is None:
                user_description_presence = False
            elif len(user_description) == 0:
                user_description_presence = False
            else:
                user_description_presence = True
            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_description_presence

    def user_description_pos_frequency(self):
        pos_tags = self._text_analysis.get_pos_tags()
        pos_features_dict = {}
        if self._retweet_flag:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"user_description_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id
        elif self._quote_flag:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"user_description_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id
        else:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"user_description_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
                feature_indicator = "retweet_" + "user_description_pos_frequency_"
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
                feature_indicator = "quote_" + "user_description_pos_frequency_"
            else:
                user_obj = tweet.get_tweet_user()
                feature_indicator = "user_description_pos_frequency_"

            user_description = user_obj.get_user_description()
            if user_description is None:
                user_description_presence = False
            elif len(user_description) == 0:
                user_description_presence = False
            else:
                user_description_presence = True

            if user_description_presence:
                pos_freq = self._text_analysis.tweet_pos_count(input_text=user_description)
                for tag in pos_freq:
                    self._tweets_features[tweet.get_tweet_id()][pos_features_dict[feature_indicator+tag]] = pos_freq[tag]
            else:
                for tag in pos_tags:
                    self._tweets_features[tweet.get_tweet_id()][pos_features_dict[feature_indicator+tag]] = 0

    def user_description_ner_frequency(self):
        ner_tags = self._text_analysis.get_ner_tags()
        ner_features_dict = {}
        if self._retweet_flag:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"user_description_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id
        elif self._quote_flag:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"user_description_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id
        else:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"user_description_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
                feature_indicator = "retweet_" + "user_description_ner_frequency_"
            elif self._quote_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
                feature_indicator = "quote_" + "user_description_ner_frequency_"
            else:
                user_obj = tweet.get_tweet_user()
                feature_indicator = "user_description_ner_frequency_"

            user_description = user_obj.get_user_description()
            if user_description is None:
                user_description_presence = False
            elif len(user_description) == 0:
                user_description_presence = False
            else:
                user_description_presence = True

            if user_description_presence:
                ner_freq = self._text_analysis.tweet_ner_count(input_text=user_description)
                for tag in ner_freq:
                    self._tweets_features[tweet.get_tweet_id()][ner_features_dict[feature_indicator + tag]] = ner_freq[tag]
            else:
                for tag in ner_tags:
                    self._tweets_features[tweet.get_tweet_id()][ner_features_dict[feature_indicator + tag]] = 0

    def user_description_length(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_description_length"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_description_length"
        else:
            self._features_id_name_dict[feature_id] = "user_description_length"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            user_description = user_obj.get_user_description()
            if user_description is None:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = None
            else:
                self._tweets_features[tweet.get_tweet_id()][feature_id] = len(user_description)

    def user_has_profile_location(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "user_has_profile_location"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "user_has_profile_location"
        else:
            self._features_id_name_dict[feature_id] = "user_has_profile_location"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                user_obj = tweet.get_tweet_retweet_object().get_tweet_user()
            elif self._quote_flag:
                user_obj = tweet.get_quote_status_object().get_tweet_user()
            else:
                user_obj = tweet.get_tweet_user()

            user_location = user_obj.get_user_location()
            if user_location is None:
                user_location_presence = False
            elif len(user_location) == 0:
                user_location_presence = False
            else:
                user_location_presence = True
            self._tweets_features[tweet.get_tweet_id()][feature_id] = user_location_presence



