def get_user_role(self):
    """
    user role measures the ratio of followers to followees of a user. A user with a high follower to followee ratio
    is a broadcaster. Conversely, a user with a low follower to followee ratio is a receiver.
    :return: a float number showing the ratio of followers to friends.
    """
    if self.get_friends_count() == 0:
        return np.nan
    else:
        return (self.get_followers_count()) / (self.get_friends_count())


def get_user_reputation(self):
    """
    this function measures the relative importance of a user on Twitter. The reputation is defined as the ratio
    between the number of friends and the number of followers as: (followers #) / (followers # + friends #).
    :return: a float number showing the ratio (followers #) / (followers # + friends #).
    """
    if self.get_followers_count() + self.get_friends_count() == 0:
        return np.nan
    else:
        return (self.get_followers_count()) / (self.get_followers_count() + self.get_friends_count())


# Should we consider units other that "day"?
# Should we consider reference dates other than "today"?
def get_account_age(self):
    """
    This function calculates the age of the account until today with the resolution of day.
    :return: the account age with the resolution of day.
    """
    today = datetime.datetime.now()
    account_creation_time = self.get_account_birthday()
    return (today.date() - account_creation_time.date()).days


# Check for division by zero error (accounts with the age of zero)?
def get_average_follow_speed(self):
    """
    this function calculates the average speed of this account in following other Twitter accounts.
    :return: a float number showing the average follow speed in this account.
    """
    return self.get_followers_count() / self.get_account_age()


# Check for division by zero error (accounts with the age of zero)?
def get_being_followed_speed(self):
    """
    this function calculates the average speed of being followed by other accounts.
    :return: a float number showing the average speed of being followed by other accounts.
    """
    return self.get_friends_count() / self.get_account_age()


# Check for division by zero error (accounts with the age of zero)?
def get_average_like_speed(self):
    """
    this function calculates the average speed of this account in liking tweets.
    :return: a float number showing the average like speed in this account.
    """
    return self.get_user_total_likes_count() / self.get_account_age()


# Check for division by zero error (accounts with the age of zero)?
def get_average_status_speed(self):
    """
    this function calculates the average speed of this account in posting tweets.
    :return: a float number showing the average tweet speed in this account.
    """
    return self.get_status_count() / self.get_account_age()

# Your username cannot be longer than 15 characters.
# A username can only contain alphanumeric characters (letters A-Z, numbers 0-9) with the exception of underscores
# https://www.techwalla.com/articles/what-characters-are-allowed-in-a-twitter-name
# https://help.twitter.com/en/managing-your-account/twitter-username-rules

# FIND A WAY TO CAPTURE THE PERMUTATION OF UPPERCASE, LOWERCASE, AND NUMBERS AND UNDERSCORE IN USER SCREENNAME
# def user_profile_screen_name_analysis(self):
#     """
#     This function analyses the length , the number of digits, letters and underscores in the screen name. These are
#     the only valid characters in the screen names.
#     :return: a dictionary that shows the number of characters, digits, letters and underscores in the screen name.
#     """
#     return {"digit_count": len([i for i in self.get_screen_name() if i in [str(dig) for dig in range(0, 10)]]),
#             "letter_count": len([i for i in self.get_screen_name() if i.isalpha()]),
#             "underscore_count": len([i for i in self.get_screen_name() if i == "_"]),
#             "screen_name_length": len(self.get_screen_name())
#             }