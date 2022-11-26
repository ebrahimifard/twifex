from tweet_text_analysis import TweetTextAnalysis


class IndividualUserFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_collection = tweets
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    #screen_name
    def user_screen_name_length(self):
        pass

    def user_screen_name_digits_count(self):
        pass

    def user_screen_name_letters_count(self):
        pass

    def user_screen_name_digits_to_letter_fraction(self):
        pass

    def user_screen_name_maximum_adjacent_letters_to_all_letters_fraction(self):
        pass

    def user_screen_name_maximum_adjacent_digits_to_all_digits_fraction(self):
        pass

    def user_screen_name_average_distance_between_subsequent_letters(self):
        pass

    def user_screen_name_average_distance_between_subsequent_digits(self):
        pass

    def user_screen_name_vowels_to_all_letters_fraction(self):
        pass

    def user_screen_name_average_distance_between_subsequent_vowels(self):
        pass

    def user_screen_name_average_distance_between_subsequent_consonants(self):
        pass

    def user_screen_name_non_alphanumeric_to_all_characters_fraction(self):
        pass

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

    def user_description_universal_pos(self):
        pass

    def user_description_detailed_pos(self):
        pass

    def user_description_ner(self):
        pass
    
    def user_description_length(self):
        pass

    def user_has_profile_location(self):
        pass



