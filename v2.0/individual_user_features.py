from tweet_text_analysis import TweetTextAnalysis
import re
import numpy as np


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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()
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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()
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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()
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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()
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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

            pat1 = r'[0-9]'
            pat2 = r'[0-9]+'
            digits_count = len(re.findall(pat1, screen_name))
            max_adjacent_digits = max([len(sequence) for sequence in re.findall(pat2, screen_name)])
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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

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
                screen_name = tweet.get_tweet_retweet_object().get_tweet_user().get_screen_name()
            elif self._quote_flag:
                screen_name = tweet.get_quote_status_object().get_tweet_user().get_screen_name()
            else:
                screen_name = tweet.get_tweet_user().get_screen_name()

            screen_name_length = self._text_analysis.text_length(input_text=screen_name, length_unit="character")
            non_alphanumeric_characters_count = self._text_analysis.special_character_count(character="_", input_text=screen_name)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = non_alphanumeric_characters_count / screen_name_length if screen_name_length != 0 else None

    #protected
    def user_is_account_protected(self):
        pass

    #verified
    def user_is_account_verified(self):
        pass

    #followers/followees count
    def user_followers_count(self):
        pass

    def user_followees_count(self):
        pass

    def user_role(self):
        """
        user role measures the ratio of followers to followees of a user. A user with a high follower to followee ratio
        is a broadcaster. Conversely, a user with a low follower to followee ratio is a receiver.
        :return: a float number showing the ratio of followers to friends.
        """
        if self.get_friends_count() == 0:
            return np.nan
        else:
            return (self.get_followers_count()) / (self.get_friends_count())

    def user_reputation(self):
        """
        this function measures the relative importance of a user on Twitter. The reputation is defined as the ratio
        between the number of friends and the number of followers as: (followers #) / (followers # + friends #).
        :return: a float number showing the ratio (followers #) / (followers # + friends #).
        """
        if self.get_followers_count() + self.get_friends_count() == 0:
            return np.nan
        else:
            return (self.get_followers_count()) / (self.get_followers_count() + self.get_friends_count())

    def user_status_count(self):
        pass

    def user_likes_count(self):
        pass

    #creation_time
    # Should we consider units other that "day"?
    # Should we consider reference dates other than "today"?
    def user_account_age(self):
        """
        This function calculates the age of the account until today with the resolution of day.
        :return: the account age with the resolution of day.
        """
        today = datetime.datetime.now()
        account_creation_time = self.get_account_birthday()
        return (today.date() - account_creation_time.date()).days

    # Check for division by zero error (accounts with the age of zero)?
    def user_average_follow_speed(self):
        """
        this function calculates the average speed of this account in following other Twitter accounts.
        :return: a float number showing the average follow speed in this account.
        """
        return self.get_followers_count() / self.get_account_age()

    # Check for division by zero error (accounts with the age of zero)?
    def user_being_followed_speed(self):
        """
        this function calculates the average speed of being followed by other accounts.
        :return: a float number showing the average speed of being followed by other accounts.
        """
        return self.get_friends_count() / self.get_account_age()

    # Check for division by zero error (accounts with the age of zero)?
    def user_average_like_speed(self):
        """
        this function calculates the average speed of this account in liking tweets.
        :return: a float number showing the average like speed in this account.
        """
        return self.get_user_total_likes_count() / self.get_account_age()

    # Check for division by zero error (accounts with the age of zero)?
    def user_average_status_speed(self):
        """
        this function calculates the average speed of this account in posting tweets.
        :return: a float number showing the average tweet speed in this account.
        """
        return self.get_status_count() / self.get_account_age()

    def user_has_profile_picture(self):
        pass

    def user_has_profile_banner(self):
        pass

    def user_has_profile_description(self):
        pass

    def user_description_pos(self):
        pass

    def user_description_ner(self):
        pass

    def user_description_length(self):
        pass

    def user_has_profile_location(self):
        pass



