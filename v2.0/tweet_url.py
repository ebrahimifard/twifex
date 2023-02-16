# from tweet import Tweet
from tweet_entities import TweetEntities
from urlextract import URLExtract
import tldextract
import urlexpander
from urllib.parse import urlsplit

class TweetUrl(TweetEntities):
    def __init__(self, tweet_obj=None, tweet_json={}):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._urls = self._tweet_entities["urls"] if "urls" in self._tweet_entities else None

        self._extractor = URLExtract()
        self._expansion_errors = ["\__CONNECTIONPOOL_ERROR__", "\__CLIENT_ERROR__"]
        self._default_url_scheme = "http://"

    def get_tweet_urls(self, input_text=None, return_format="url"):
        """
        This function represents the urls which are embedded in this tweet.
        :param return_format: It indicates the return format of urls which can can be "url", "display_url", or
        "expanded_url".
        :return: a list of urls in this tweet.
        """

        assert (return_format in ["url", "display_url", "expanded_url"]), "the return_format has to be  url, " \
                                                                          "display_url, or expanded_url"

        if input_text is not None:
            text = input_text
            url_list = self._extractor.find_urls(text)
            if return_format == "url":
                return url_list
            elif return_format == "expanded_url":
                urls_with_scheme = []
                for url in url_list:
                    if urlsplit(url).scheme == '':
                        urls_with_scheme.append(f"{self._default_url_scheme}{url}")
                    else:
                        urls_with_scheme.append(url)

                expanded_urls = []
                for schemed_url in urls_with_scheme:
                    exp_url = urlexpander.expand(schemed_url)
                    for err in self._expansion_errors:
                        if err in exp_url:
                            exp_url = exp_url.replace(err, "")
                    expanded_urls.append(exp_url)
                return expanded_urls
            #when the input_text is not None, the return format can be eitehr url or expanded url (since we do not have access to url object) and if the user set the return format to display_url the return format would be url
            elif return_format == "display_url":
                return url_list
        elif input_text is None:
            if self._urls is None:
                return []
            else:
                if return_format == "url":
                    return [element['url'] for element in self._urls]
                elif return_format == "expanded_url":
                    return [element['expanded_url'] for element in self._urls]
                elif return_format == "display_url":
                    return [element['display_url'] for element in self._urls]

    def domain_replacement(self, input_text=None, inplace=False):
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text is not None:
            text = input_text
            urls = self.get_tweet_urls(input_text=text)
            for url in urls:
                ext = tldextract.extract(url)
                text = text.replace(url, ext.domain + "." + ext.suffix)
            return text
        elif input_text is None:
            text = self._tweet.get_tweet_text()
            if self._urls is not None:
                urls = self._extractor.find_urls(text)
                for url in urls:
                    ext = tldextract.extract(url)
                    text = text.replace(url, ext.domain + "." + ext.suffix)

            if inplace:
                self._tweet.set_tweet_text(text)
                return self._tweet
            else:
                return text

    def url_removal(self, input_text=None, inplace=False):
        """
        This function removes the urls from the tweet text.
        :param input_text: if this parameter is None, then the urls are removed from the caller object text, otherwise
        and in case of a string as an input for this parameter, the urls are removed from the input text.
        :param inplace: if inplace is True, the url removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the urls.
        :return: when the inplace parameter is equal to True, the function changes the caller object text field permanently
        by removing the urls and returning the whole object, in contrast when it is equal to False the function only
        returns the text field after url removal.
        """
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        if input_text is not None:
            text = input_text
            urls = self._extractor.find_urls(text)
            for url in urls:
                text = text.replace(url, "")
            return text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                urls = self._extractor.find_urls(text)
                for url in urls:
                    text = text.replace(url, "")
                if inplace:
                    self._tweet.set_tweet_text(text)
                    return self._tweet
                else:
                    return text
            elif self._tweet is None:
                return
