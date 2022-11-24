from tweet_entities import TweetEntities
import wordninja


class TweetHashtag(TweetEntities):
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._hashtags = self._tweet_entities["hashtags"] if "hashtags" in self._tweet_entities else None

    def get_tweet_hashtags(self, case_sensitivity="small", hashtag_symbol=True, distinct_hashtags=True):
        """
        This function returns a list of hashtags in this tweet.
        :param case_sensitivity: By setting this parameter to small hashtags will be returned in small format.
        If you set it to original, the hashtags will be returned the same as it written in the tweet..
        :param hashtag_symbol: It indicated whether the # character comes before hashtags or not.
        :param distinct_hashtags: By setting this parameter to True, duplicate hashtags are ignored.
        :return: a list of hashtags in this tweet.
        """
        assert (case_sensitivity in ["small", "original"]), "the case_sensitivity has to be small or original"
        assert (hashtag_symbol in [True, False]), "the hashtag_symbol has to be True or False"
        assert (distinct_hashtags in [True, False]), "the distinct_hashtags has to be True or False"

        if self._hashtags is None:
            return []
        else:
            hashtags = [element['text'] for element in self._hashtags]
            hashtags = list(set(hashtags)) if distinct_hashtags else hashtags
            hashtags = ["#"+element if hashtag_symbol else element for element in hashtags]
            hashtags = [element.lower() if case_sensitivity == "small" else element for element in hashtags]
            return hashtags

    def hashtag_splitter(self, input_text=None, inplace=False):
        """
        This function slices up hashtags as in most of the times, hashtags are made up of concatenation of meaningful
        words.
        :param input_text: if this parameter is None, then the hashtag splitter is applied on the caller object,
        otherwise and in case of a string as an input for this parameter, the hashtag splitter is applied to the input text.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after slicing up the hashtags.
        :return: It returns the text field after slicing up the hashtags.
        """
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text is None:
            text = self._tweet.get_tweet_text()
        else:
            text = input_text

        if self._hashtags is not None:
            for hashtag in self._hashtags:
                hashtag_text = hashtag["text"]
                hashtag_first_index, hashtag_last_index = hashtag["indices"][0], hashtag["indices"][1]
                text = text.replace(text[hashtag_first_index+1:hashtag_last_index], "  #".join(wordninja.split(hashtag_text)))

        if inplace:
            self._tweet.set_tweet_text(text)
            return self._tweet
        else:
            return text

    def hashtags_removal(self, input_text=None, mode=2, inplace=False):
        """
        This function removes hashtags from tweet text according to different modes.
        :param input_text: if this parameter is None, then the hashtag removal is applied on the caller object,
        otherwise and in case of a string as an input for this parameter, the hashtag removal is applied to the input text.
        :param mode: there are three modes for hashtags removal. In mode 1, the text remains intact, in Mode 2, only the
        hashtag characters (#) are removed, and in mode 3, the whole hashtags consisting the hashtag character and the terms
        after the hashtags are removed.
        :param inplace: if inplace is True, the hashtag removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the hashtags.
        :return: when the implace parameter is equal to True, the function removes the hashtags permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         hashtags from the text.
        """

        assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text is None:
            text = self._tweet.get_tweet_text()
        else:
            text = input_text

        if mode == 1:
            pass
        elif mode == 2:
            text = text.replace("#", "")
        elif mode == 3:
            for h in self.get_tweet_hashtags():
                text = text.replace("#" + h, "")
        if inplace:
            self._tweet.set_tweet_text(text)
            return self._tweet
        else:
            return text
