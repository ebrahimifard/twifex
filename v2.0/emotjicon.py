import emoji
import emot
# import re


class Emotjicon:
    def __init__(self):
        self._tweet = None

        # self._emoticons_dict = []
        # with open("./resources/emoticons.txt") as f:
        #     self._emoticons_dict = [term.strip() for term in f.readlines()]

    def parse_tweet_object(self, tweet_obj):
        self._tweet = tweet_obj

    def get_tweet_emojis(self):
        """
        This function collects the emojis from tweet text.
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        emojis are extracted from the input text.
        :return: It returns the list of emojis in the tweet text.
        """

        text = self._tweet.get_tweet_text()
        emojis = emoji.emoji_lis(text)

        return emojis

    def get_tweet_emoticon(self):
        """
        This function collects the emoticons from tweet text.
        :return: It returns the list of emoticons in the tweet text.
        """

        # text = self._tweet.get_tweet_text()
        # tokens = re.findall(r'\S+', text)
        #
        # emoticons = [word for word in tokens if word in self._emoticons_dict]
        text = self._tweet.get_tweet_text()
        emot_obj = emot.core.emot()
        emoticons = emot_obj.emoticons(text)['value']

        return emoticons

    def replace_emoji_with_text(self, inplace=False, language="en"):
        """
        This function replaces emojis with their equivalent text.
        :param inplace: if inplace is True, the caller object text field is permanently updated, otherwise the caller object text field remains intact and the function returns the text after replacing emojis with their equivalent text.
        :param language: By default, the language is English (language='en') but also supported languages are: Spanish ('es'), Portuguese ('pt'), Italian ('it'), French ('fr'), German ('de'), Farsi/Persian ('fa')
        :return: It returns the tweet object with the updated text field if the inplace field is set to True, otherwise it returns the updated tweet text field.
        """

        text = self._tweet.get_tweet_text()
        updated_text = emoji.demojize(text, language=language).replace(":", "")

        if inplace:
            self._tweet.set_tweet_text(updated_text)
            return self._tweet
        else:
            return updated_text

    def replace_emoticon_with_text(self, inplace=False):
        """
        This function replaces emoticons with their equivalent text.
        :param inplace: if inplace is True, the caller object text field is permanently updated, otherwise the caller object text field remains intact and the function returns the text after replacing emoticons with their equivalent text.
        :return: It returns the tweet object with the updated text field if the inplace field is set to True, otherwise it returns the updated tweet text field.
        """
        text = self._tweet.get_tweet_text()

        emot_obj = emot.core.emot()
        emoticons = emot_obj.emoticons(text)
        emoticons_dict = dict(zip(emoticons["value"], emoticons["mean"]))

        for em in emoticons_dict:
            text = text.replace(em, emoticons_dict[em])

        if inplace:
            self._tweet.set_tweet_text(text)
            return self._tweet
        else:
            return text

    def remove_emojis(self, inplace=False):
        """
        This function removes emojis from the tweet text.
        :param inplace: if inplace is True, the emoji removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the emojis.
        :return: when the implace parameter is set to True, the function removes the emojis permanently and returns
        the whole object, in contrast when it is set to False the function only returns the text field after removing the
         emojis from the text.
        """
        emojis = self.get_tweet_emojis()
        text = self._tweet.get_tweet_text()
        for item in emojis:
            text = text.replace(item, "")

        if inplace:
            self._tweet.set_tweet_text(text)
            return self._tweet
        else:
            return text

    def remove_emoticons(self, inplace=False):
        """
        This function removes emoticons from the tweet text.
        :param inplace: if inplace is True, the emoticon removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the emoticons.
        :return: when the implace parameter is set to True, the function removes the emoticons permanently and returns
        the whole object, in contrast when it is set to False the function only returns the text field after removing the
         emoticon from the text.
        """
        emoticons = self.get_tweet_emoticon()
        text = self._tweet.get_tweet_text()
        for item in emoticons:
            text = text.replace(item, "")

        if inplace:
            self._tweet.set_tweet_text(text)
            return self._tweet
        else:
            return text
