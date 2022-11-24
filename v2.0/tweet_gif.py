# from tweet import Tweet
from tweet_media import TweetMedia
from media_download import MediaDownload


class TweetGif(TweetMedia):
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._gifs = None if self._media is None else \
            [element for element in self._media if element["type"] == "animated_gif"]

    def get_tweet_gif_url(self):
        """
        This function returns the animated-gif url in this tweet.
        :return: it returns the animated-gif url attached to this tweet in a list.
        """

        gifs_urls = []
        if self._gifs is None:
            return gifs_urls
        else:
            for gif in self._gifs:
                gifs_urls += [item["url"] for item in gif["video_info"]["variants"]]
            return gifs_urls

    def download_tweet_gif(self, path_to_save):
        """
        This function downloads the animated-gif embedded in the tweet.
        :param path_to_save: This parameter indicates where the animated-gif is saved.
        :return: It returns None
        """

        assert isinstance(path_to_save, str), "The path_to_save has to be string"

        urls = self.get_tweet_gif_url()
        MediaDownload.download_gif(urls, path_to_save)
