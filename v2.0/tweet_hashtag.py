from tweet_entities import TweetEntities
import wordninja
import re


class TweetHashtag(TweetEntities):
    def __init__(self, tweet_obj=None, tweet_json={}):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._hashtags = self._tweet_entities["hashtags"] if "hashtags" in self._tweet_entities else None

    def get_tweet_hashtags(self, input_text=None, case_sensitivity="small", hashtag_symbol=True, distinct_hashtags=True):
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

        def inner_hashtags_processing(inner_hashtags, inner_case_sensitivity="small", inner_hashtag_symbol=True, inner_distinct_hashtags=True):
            inner_hashtags = list(set(inner_hashtags)) if inner_distinct_hashtags else inner_hashtags
            inner_hashtags = ["#" + inner_element if inner_hashtag_symbol else inner_element for inner_element in inner_hashtags]
            inner_hashtags = [inner_element.lower() if inner_case_sensitivity == "small" else inner_element for inner_element in inner_hashtags]
            return inner_hashtags

        if input_text is not None:
            text = input_text
            pattern = r'#(\w+)'
            string_numbers = [str(u) for u in range(0, 10)]
            ht_list = []
            matches = list(re.finditer(pattern, text, flags=re.UNICODE))
            for match_index, match_ht in enumerate(matches):
                flag = True
                start_index = match_ht.start()
                end_index = match_ht.end()

                if match_index != 0:
                    if start_index == matches[match_index-1].end():
                        flag = False
                if match_index != len(matches)-1:
                    if end_index == matches[match_index+1].start():
                        flag = False

                if flag:
                    if text[start_index+1] not in string_numbers:
                        ht_list.append(text[start_index+1:end_index])

            return inner_hashtags_processing(inner_hashtags=ht_list, inner_case_sensitivity=case_sensitivity, inner_hashtag_symbol=hashtag_symbol, inner_distinct_hashtags=distinct_hashtags)

        elif input_text is None:
            if self._hashtags is None:
                return []
            else:
                hashtags = [element['text'] for element in self._hashtags]
                return inner_hashtags_processing(inner_hashtags=hashtags, inner_case_sensitivity=case_sensitivity, inner_hashtag_symbol=hashtag_symbol, inner_distinct_hashtags=distinct_hashtags)

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

        if input_text is not None:
            text = input_text
            hashtags = self.get_tweet_hashtags(input_text=text, case_sensitivity="original")
            for hashtag in hashtags:
                for ht in list(re.finditer(hashtag, text)):
                    hashtag_text = hashtag[1:]
                    hashtag_first_index, hashtag_last_index = ht.start(), ht.end()
                    text = text.replace(text[hashtag_first_index + 1:hashtag_last_index]," #".join(wordninja.split(hashtag_text)))
            return text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                for hashtag in self._hashtags:
                    hashtag_text = hashtag["text"]
                    hashtag_first_index, hashtag_last_index = hashtag["indices"][0], hashtag["indices"][1]
                    text = text.replace(text[hashtag_first_index + 1:hashtag_last_index], " #".join(wordninja.split(hashtag_text)))
                if inplace:
                    self._tweet.set_tweet_text(text)
                    return self._tweet
                else:
                    return text
            elif self._tweet is None:
                return

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

        if input_text is not None:
            text = input_text
            if mode == 1:
                pass
            elif mode == 2:
                text = text.replace("#", "")
            elif mode == 3:
                for h in self.get_tweet_hashtags(input_text=text, case_sensitivity="original"):
                    text = text.replace(h, "")
            return text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                if mode == 1:
                    pass
                elif mode == 2:
                    text = text.replace("#", "")
                elif mode == 3:
                    for h in self.get_tweet_hashtags(case_sensitivity="original"):
                        text = text.replace(h, "")
                if inplace:
                    self._tweet.set_tweet_text(text)
                    return self._tweet
                else:
                    return text
            elif self._tweet is None:
                return
