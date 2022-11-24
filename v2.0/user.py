import datetime
from media_download import MediaDownload


class User:
    def __init__(self, user_json):
        """
        This is the constructor of user class.
        :param user_json: The tweet object which is an object instantiated from Tweet, Retweet, or Quote classes.
        """

        assert isinstance(user_json, dict), "The user_json has to be a dict"

        # user = tweet_object.get_tweet_user()
        self._user_id = user_json["id_str"] if "id_str" in user_json.keys() else None
        self._name = user_json["name"] if "name" in user_json.keys() else None
        self._screen_name = user_json["screen_name"] if "screen_name" in user_json.keys() else None
        self._location = user_json["location"] if "location" in user_json.keys() else None

        self._has_url = [True if user_json["url"] is not None else False][0] if "url" in user_json.keys() else None
        self._entities = user_json["entities"] if "entities" in user_json.keys() else None

        if self._has_url:
            if self._entities is not None:
                self._url = self._entities["url"]["urls"][0]["expanded_url"]
            else:
                self._url = user_json["url"]
        else:
            self._url = None
        # self._url = self._entities["url"]["urls"][0]["expanded_url"] if self._has_url else None

        self._description = user_json["description"] if "description" in user_json.keys() else None

        if self._entities is not None:
            if len(self._entities["description"]["urls"]) > 0:
                self._description_urls = [element["expanded_url"] for element in self._entities["description"]["urls"]]
            else:
                self._description_urls = []
        else:
            self._description_urls = []

        self._protected = user_json["protected"] if "protected" in user_json.keys() else None
        self._verified = user_json["verified"] if "verified" in user_json.keys() else None
        self._followers_count = user_json["followers_count"] if "followers_count" in user_json.keys() else None
        self._friends_count = user_json["friends_count"] if "friends_count" in user_json.keys() else None
        self._listed_count = user_json["listed_count"] if "listed_count" in user_json.keys() else None
        self._favourites_count = user_json["favourites_count"] if "favourites_count" in user_json.keys() else None
        self._statuses_count = user_json["statuses_count"] if "statuses_count" in user_json.keys() else None
        self._created_at = user_json["created_at"] if "created_at" in user_json.keys() else None
        self._profile_banner_url = user_json["profile_banner_url"] if "profile_banner_url" in user_json.keys() else None
        self._profile_image_url_https = user_json["profile_image_url_https"] \
            if "profile_image_url_https" in user_json.keys() else None
        self._default_profile = user_json["default_profile"] if "default_profile" in user_json.keys() else None
        self._default_profile_image = user_json["default_profile_image"] \
            if "default_profile_image" in user_json.keys() else None
        self._withheld_in_countries = user_json["withheld_in_countries"] \
            if "withheld_in_countries" in user_json.keys() else None
        self._withheld_scope = user_json["withheld_scope"] if "withheld_scope" in user_json.keys() else None

    def get_user_id(self):
        """
        This function gives the user unique id.
        :return: an integer showing the user unique id.
        """
        return self._user_id

    def get_user_name(self):
        """
        The name of the user, as they’ve defined it. Not necessarily a person’s name. Typically capped at 50 characters,
         but subject to change.
        :return: a string showing the user defined name.
        """
        return self._name

    def get_screen_name(self):
        """
        The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject
         to change. Typically a maximum of 15 characters long, but some historical accounts may exist with longer names.
        :return: a string showing the screen name of the user_json.
        """
        return self._screen_name

    def get_user_location(self):
        """
        this function shows the user-defined location for this account’s profile. Not necessarily a location, nor
        machine-parseable.
        :return: a string showing the user-defined location for this account.
        """
        return self._location

    def get_user_url(self):  # need to add url in class attributes
        """
        this function shows a URL provided by the user in association with their profile.
        :return: a string showing the url provided by the user_json.
        """
        return self._url

    def get_user_description(self):
        """
        this function shows the user-defined string describing their account.
        :return: a string showing the user defined profile description.
        """
        return self._description

    def get_user_description_urls(self):
        """
        this function shows the user-defined string describing their account.
        :return: a string showing the user defined profile description.
        """
        return self._description_urls

    def is_user_protected(self):
        """
        this function shows the protection status of the account. When true, indicates that this user has chosen to
        protect his/her tweets.
        :return: a boolean showing the protection status of the account.
        """
        return self._protected

    def is_user_verified(self):
        """
        this function shows the verification status of this account.
        :return: a boolean showing the verification status of this account.
        """
        return self._verified

    def get_user_followers_count(self):
        """
        The number of followers this account has.
        :return: an integer showing the number of account holder's followers.
        """
        return self._followers_count

    def get_user_friends_count(self):
        """
        The number of users this account is following (AKA their “followings”)
        :return: an integer showing the number of account holder's friends (followings).
        """
        return self._friends_count

    def get_user_listed_count(self):
        return self._listed_count

    def get_user_favourites_count(self):
        """
        The number of Tweets this user has liked in the account’s lifetime.
        :return: an integer show the number of Tweets that this account has liked in the account’s lifetime.
        """
        return self._favourites_count

    def get_user_statuses_count(self):
        """
        The number of Tweets (including retweets) issued by the user in the account's lifetime
        :return: an integer  showing the number of Tweets issued by the user_json.
        """
        return self._statuses_count

    def get_user_creation_time(self, output="datetime_object"):
        """
        It shows the  date and time that the user account was created on Twitter.
        :param output: it can be either "object" or "string". By choosing the object, the datetime object will be
        returned and by selecting string, the string version of datetime object will be returned.
        :return: a string ot datetime object depending on the output parameter.
        """
        assert (output in ["datetime_object", "string"]), "the output has to be object or string"

        if output == "datetime_object":
            return datetime.datetime.strptime(self._created_at, "%a %b %d %H:%M:%S %z %Y")
        elif output == "string":
            return self._created_at

    def get_profile_banner_url(self):
        return self._profile_banner_url

    def get_profile_image_url(self):
        return self._profile_image_url_https

    def is_default_profile(self):
        return self._default_profile

    def is_default_profile_image(self):
        return self._default_profile_image

    def get_withheld_in_countries(self):
        return self._withheld_in_countries

    def get_withheld_scope(self):
        return self._withheld_scope

    def download_user_profile_picture(self, saving_path):
        """
        this function download the user profile picture.
        :param saving_path: the address to save the photo.
        :return: a photo
        """
        """
        this function download the user profile picture.
        :return: a string showing the user-defined location for this account.
        """
        url = self.get_profile_image_url()
        MediaDownload.download_photo([url], saving_path)
