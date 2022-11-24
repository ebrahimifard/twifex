import json
from user import User
import datetime
from bs4 import BeautifulSoup
import re


from tweet_hashtag import TweetHashtag
from tweet_mention import TweetMention
from tweet_url import TweetUrl
from tweet_photo import TweetPhoto
from tweet_video import TweetVideo
from tweet_gif import TweetGif

from tweet_location import TweetLocation


class Tweet:
    def __init__(self, tweet_path, **kwargs):
        """
        This is the constructor of SingleTweet.
        :param tweet_path: an individual tweet path.
        """

        # assert isinstance(tweet_path, str), "The tweet_path has to be a string"
        if len(kwargs) == 0:
            with open(tweet_path, encoding='utf-8') as f:
                tweet = json.load(f)
        else:
            tweet = kwargs["tweet_object"]
        # tweet = json.load(open(tweet_path)) if len(kwargs) == 0 else kwargs["tweet_object"]
        self._creation_time = tweet["created_at"] if "created_at" in tweet.keys() else None
        self._id = tweet["id_str"] if "id_str" in tweet.keys() else None
        self._is_tweet_retweeted = True if "retweeted_status" in tweet.keys() else False

        self._client = BeautifulSoup(tweet["source"], "html.parser").text if "source" in tweet.keys() else None
        self._truncated = tweet["truncated"] if "truncated" in tweet.keys() else None

        # self._text = [tweet["retweeted_status"]["full_text"]
        #               if "full_text" in tweet["retweeted_status"].keys() else None][0] \
        #     if self._is_tweet_retweeted else [tweet["full_text"] if "full_text" in tweet.keys() else None][0]

        if self._is_tweet_retweeted:
            if tweet["retweeted_status"]["truncated"] and "extended_tweet" in tweet["retweeted_status"].keys():
                self._text = tweet["retweeted_status"]["extended_tweet"]["full_text"]
            elif "full_text" in tweet["retweeted_status"].keys():
                self._text = tweet["retweeted_status"]["full_text"]
            elif "text" in tweet["retweeted_status"].keys():
                self._text = tweet["retweeted_status"]["text"]
            else:
                self._text = None
        else:
            if self._truncated and "extended_tweet" in tweet.keys():
                self._text = tweet["extended_tweet"]["full_text"]
            elif "full_text" in tweet.keys():
                self._text = tweet["full_text"]
            elif "text" in tweet.keys():
                self._text = tweet["text"]
            else:
                self._text = None

        self._in_reply_to_status_id = tweet["in_reply_to_status_id_str"] if \
            "in_reply_to_status_id_str" in tweet.keys() else None
        self._in_reply_to_user_id = tweet["in_reply_to_user_id_str"] \
            if "in_reply_to_user_id_str" in tweet.keys() else None
        self._in_reply_to_screen_name = tweet["in_reply_to_screen_name"] \
            if "in_reply_to_screen_name" in tweet.keys() else None

        self._user = User(tweet["user"]) if "user" in tweet.keys() else None

        self._coordinates = tweet["coordinates"] if "coordinates" in tweet.keys() else None
        self._place = tweet["place"] if "place" in tweet.keys() else None
        self._location = TweetLocation(self._place, self._coordinates)

        # Here, the first line checks whether this tweet comprises any quotes (other tweets).
        # The second line returns the id of that tweet (if it exists)
        # The third line returns the the screen_name of the user who posted the quote in the first place
        # The fourth line checks whether that tweet actually is embedded in this tweet or not
        # The fourth line returns that tweet as an object (if it exists)
        self._is_quote_status = tweet["is_quote_status"] if "is_quote_status" in tweet.keys() else None
        self._quoted_status_id = tweet["quoted_status_id_str"] if self._is_quote_status else None
        self._quote_screen_name = re.findall("status.*", tweet["quoted_status_permalink"]["expanded"])[0].replace("status/", "") if "quoted_status_permalink" in tweet.keys() else None
        self._is_quote_status_object_available = True if "quoted_status" in tweet.keys() else False
        self._quoted_status_object = Tweet(tweet_path=None, tweet_object=tweet["quoted_status"]) \
            if self._is_quote_status_object_available else None
        
        self._retweeted_status = Tweet(tweet_path=None, tweet_object=tweet["retweeted_status"]) \
            if self._is_tweet_retweeted else None

        self._quote_count = tweet["quote_count"] if "quote_count" in tweet.keys() else None
        self._reply_count = tweet["reply_count"] if "reply_count" in tweet.keys() else None
        self._retweet_count = tweet["retweet_count"] if "retweet_count" in tweet.keys() else None
        self._likes_count = tweet["favorite_count"] if "favorite_count" in tweet.keys() else None

        self._hashtags = TweetHashtag(self, tweet)
        self._mentions = TweetMention(self, tweet)
        self._urls = TweetUrl(self, tweet)
        self._photos = TweetPhoto(self, tweet)
        self._video = TweetVideo(self, tweet)
        self._gif = TweetGif(self, tweet)
        
        self._favorited = tweet["favorited"] if "favorited" in tweet.keys() else None
        self._retweeted = tweet["retweeted"] if "retweeted" in tweet.keys() else None
        self._possibly_sensitive = tweet["possibly_sensitive"] if "possibly_sensitive" in tweet.keys() else None
        self._filter_level = tweet["filter_level"] if "filter_level" in tweet.keys() else None
        self._lang = tweet["lang"] if "lang" in tweet.keys() else None
        self._matching_rules = tweet["matching_rules"] if "matching_rules" in tweet.keys() else None
        self._current_user_retweet = tweet["current_user_retweet"] if "current_user_retweet" in tweet.keys() else None
        self._scopes = tweet["scopes"] if "scopes" in tweet.keys() else None
        self._withheld_copyright = tweet["withheld_copyright"] if "withheld_copyright" in tweet.keys() else None
        self._withheld_in_countries = tweet["withheld_in_countries"] if "withheld_in_countries" in tweet.keys() \
            else None
        self._withheld_scope = tweet["withheld_scope"] if "withheld_scope" in tweet.keys() else None

    def get_tweet_creation_time(self, output="datetime_object"):
        """
        It shows the creation time and date of a tweet.
        :param output: it can be either "object", "original_string", or "improved_string". By choosing the
        original_string the created_at field of tweet object is returned. By choosing object, a datetime object of the
        tweet creation time including year, month, day, hour, minute and second is returned. "improved_string" returns
        the string version of the datetime object.
        :return: a string or datetime object of the tweet creation time.
        """

        assert (output in ["datetime_object", "original_string",
                           "improved_string"]), "the output has to be object or original_string, or" \
                                                "improved_string"

        if output == "datetime_object":
            return datetime.datetime.strptime(datetime.datetime.strftime(
                datetime.datetime.strptime(self._creation_time, "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S"),
                "%Y %m %d %H %M %S")
        elif output == "original_string":
            return self._creation_time
        elif output == "improved_string":
            return datetime.datetime.strftime(
                datetime.datetime.strptime(self._creation_time, "%a %b %d %H:%M:%S %z %Y"), "%Y %m %d %H %M %S")

    def get_tweet_id(self):
        """
        This function returns the unique id of this tweet.
        :return: a string showing the unique id of this tweet.
        """
        return self._id

    def get_tweet_text(self):
        """
        This function returns the tweet text.
        :return: a string showing the full text of this tweet.
        """

        return self._text

    def get_tweet_client(self):
        """
        This function returns the utility used to post the tweet.
        :return: a string showing the utility used to post the Tweet.
        """

        return self._client

    def is_tweet_truncated(self):
        return self._truncated

    def is_tweet_a_reply(self):
        """
        This function indicates whether this is a reply tweet or not.
        :return: a boolean shows whether this tweet is a reply tweet or not.
        """
        return False if self._in_reply_to_status_id is None else True

    def get_reply_to_id(self):
        """
        If this is a reply tweet, this function represents the id of the parent tweet.
        :return: a string showing the unique id of the tweet that this one is a reply to that.
        """
        return self._in_reply_to_status_id

    def get_tweet_in_reply_to_screen_name(self):
        """
        If the tweet is a reply to another tweet, this function returns the screen name of the parent tweet.
        :return: a string of parent tweet screen name.
        """
        return self._in_reply_to_screen_name

    def get_tweet_user(self):
        """
        This tweet returns the user object of the tweet.
        :return: the user object embedded in the tweet object.
        """
        return self._user

    def get_tweet_location(self):
        return self._location

    def is_tweet_quoted(self):
        """
        This function indicates whether this is a quote tweet or not.
        :return: a boolean showing whether this is a quoted tweet or not.
        """
        return self._is_quote_status

    def get_tweet_quote_id(self):
        """
        If this is a quote tweet, the quoted_status_id field surfaces and this function returns it.
        :return: it returns the string representation tweet id of the quoted tweet.
        """
        return self._quoted_status_id

    def get_inner_quote_screen_name(self):
        """
        If this is a quote tweet, the quoted_status_permalink field surfaces and this function returns it.
        :return: it returns the string representation screen_name of the quoted tweet.
        """
        return self._quote_screen_name

    def is_quote_status_object_available(self):
        """
        This function indicates whether this tweet comprises a quote object or not.
        :return: a boolean showing whether this tweet comprises a quote object or not.
        """
        return self._is_quote_status_object_available

    def get_quote_status_object(self):
        """
        If this is a quote tweet, the quoted_status field surfaces and this function returns it.
        :return: it returns the QuoteTweet object of the original Tweet that was quoted.
        """
        return self._quoted_status_object

    def is_tweet_retweeted(self):
        """
        This function indicates whether this is a retweet or not.
        :return: a boolean shows whether this tweet is retweeted or not.
        """
        return self._is_tweet_retweeted

    def get_tweet_retweet_object(self):
        """
        If this tweet consists of a retweet object, this function returns it.
        :return: it returns the retweeted part of this tweet.
        """
        return self._retweeted_status

    def get_tweet_quote_count(self):
        return self._quote_count

    def get_tweet_reply_count(self):
        return self._reply_count

    def get_tweet_likes_count(self):
        """
        This function returns the approximate number of times this tweet has been liked by Twitter users.
        :return: an integer which indicates approximately how many times this Tweet has been liked by Twitter users
        """
        return self._likes_count

    def get_tweet_retweets_count(self):
        """
        This function returns the number of times this Tweet has been retweeted.
        :return: an integer which indicates how many times this tweet has been retweeted.
        """
        return self._retweet_count

    def get_tweet_hashtags(self):
        return self._hashtags

    def get_tweet_mentions(self):
        return self._mentions

    def get_tweet_urls(self):
        return self._urls

    def get_tweet_photos(self):
        return self._photos

    def get_tweet_video(self):
        return self._video

    def get_tweet_gif(self):
        return self._gif

    def get_tweet_entities(self):
        """
        This function extracts the full tweet entities including hashtags, mentions, urls, photos, videos, gifs, and
        symbols from a tweet object.
        :return: a dictionary containing all the entities.
        """
        return {"hashtags": self.get_tweet_hashtags(), "mentions": self.get_tweet_mentions(),
                "urls": self.get_tweet_urls(), "photos": self.get_tweet_photos(), "video": self.get_tweet_video(),
                "gif": self.get_tweet_gif(), }

    def get_tweet_language(self):
        """
        This function returns the language identifier corresponding to the machine-detected language of the Tweet text,
        or und if no language could be detected.
        :return: a string showing the language of the tweet.
        """
        return self._lang

    def get_tweet_matching_rules(self):
        return self._matching_rules

    def get_tweet_current_user_retweet(self):
        return self._current_user_retweet

    def get_tweet_scopes(self):
        return self._scopes

    def get_tweet_withheld_copyright(self):
        return self._withheld_copyright

    def get_tweet_withheld_in_countries(self):
        return self._withheld_in_countries

    def get_tweet_withheld_scope(self):
        return self._withheld_scope

    def get_tweet_object(self):
        """
        This function returns the tweet object as a dictionary.
        :return: the tweet as a dictionary.
        """
        return self

    def get_tweet_url(self):
        """
        this function builds the tweet url.
        :return: a string of tweet url.
        """
        return "https://twitter.com/" + self.get_tweet_user().get_screen_name() + "/status/" + \
               self.get_tweet_id()

    def set_tweet_text(self, updated_text):

        assert isinstance(updated_text, str), "The updated_text has to be a string"

        self._text = updated_text

