from tweet_entities import TweetEntities
import re


class TweetMention(TweetEntities):
    def __init__(self, tweet_obj=None, tweet_json={}):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._mentions = self._tweet_entities["user_mentions"] if "user_mentions" in self._tweet_entities else None

    def get_tweet_mentions(self, input_text=None, return_format="screen_name", at_symbol=True, distinct_mentions=True):
        """
        This function returns a list of mentions in this tweet.
        :param return_format: It indicates in what format tweet mentions should be returned.
        :param at_symbol: It indicated whether the @ character comes before mentions or not.
        :param distinct_mentions: By setting this parameter to True, duplicate mentions are ignored.
        :return: a list of mentions in this tweet.
        """

        assert (return_format in ["screen_name", "name", "id"]), "the return_format has to be screen_name, name, or id"
        assert (at_symbol in [True, False]), "the at_sign has to be True or False"
        assert (distinct_mentions in [True, False]), "the distinct_mentions has to be True or False"

        if input_text is not None:
            text = input_text
            pattern = r'@(\w+)'
            mt_list = []
            matches = list(re.finditer(pattern, text, flags=re.UNICODE))
            for match_index, match_mt in enumerate(matches):
                flag = True
                start_index = match_mt.start()
                end_index = match_mt.end()

                if match_index != 0:
                    if start_index == matches[match_index-1].end():
                        flag = False
                if match_index != len(matches)-1:
                    if end_index == matches[match_index+1].start():
                        flag = False
                if flag:
                    mt_list.append(text[start_index+1:end_index])
            mentions = list(set(mt_list)) if distinct_mentions else mt_list
            mentions = ["@" + element if at_symbol else element for element in mentions]
            return mentions
        elif input_text is None:
            if self._tweet is not None:
                if self._mentions is None:
                    return []
                else:
                    mentions = [element[return_format] for element in self._mentions]
                    mentions = list(set(mentions)) if distinct_mentions else mentions
                    mentions = ["@" + element if at_symbol else element for element in mentions]
                    return mentions
            elif self._tweet is None:
                return

    def mention_replacement(self, inplace=False):
        """
        This function replaces Twitter account mentions by the accounts' screen name.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after replacing the mentions.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently
        by replacing the mentions with the accounts screen names and returning the whole object, in contrast when it is equal
        to False the function only returns the text field after replacing the mentions without changing the text field.
        """
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if self._tweet is not None:
            text = self._tweet.get_tweet_text()
            if self._mentions is not None:
                for mention in self._mentions:
                    text = text.replace(mention["screen_name"], mention["name"])
            if inplace:
                self._tweet.set_tweet_text(text)
                return self._tweet
            else:
                return text
        elif self._tweet is None:
            return

    def mentions_removal(self, input_text=None, mode=2, inplace=False):
        """
        This function removes mentions from tweet text according to different modes.
        :param input_text: if this parameter is None, then the mention removal is applied on the caller object,
        otherwise and in case of a string as an input for this parameter, the mention removal is applied to the input text.
        :param mode: there are three modes for mention removal. In mode 1, the text remains intact, in Mode 2, only the
        mention characters (@) are removed, and in mode 3, the whole mention consisting the mention character and the terms
        after the mentions are removed.
        :param inplace: if inplace is True, the mention removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the mention.
        :return: when the implace parameter is equal to True, the function removes the mentions permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         mentions from the text.
        """

        assert (mode in [1, 2, 3]), "The mode can be 1, 2, or 3"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text is not None:
            text = input_text
            if mode == 1:
                pass
            elif mode == 2:
                text = text.replace("@", "")
            elif mode == 3:
                for m in self.get_tweet_mentions(input_text=text):
                    text = text.replace(m, "")
            return text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                if mode == 1:
                    pass
                elif mode == 2:
                    text = text.replace("@", "")
                elif mode == 3:
                    for m in self.get_tweet_mentions():
                        text = text.replace(m, "")
                if inplace:
                    self._tweet.set_tweet_text(text)
                    return self._tweet
                else:
                    return text
            elif self._tweet is None:
                return
