# from tweet import Tweet
from tweet_media import TweetMedia
from media_download import MediaDownload


class TweetPhoto(TweetMedia):
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._photos = None if self._media is None else \
            [element for element in self._media if element["type"] == "photo"]

    def get_tweet_photo_urls(self):
        """
        This function returns the list of photo urls in this tweet.
        :return: it returns the photo urls attached to this tweet as a list.
        """
        
        if self._photos is None:
            return []
        else:
            return [photo["media_url"] for photo in self._photos]

    def download_tweet_photos(self, path_to_save):
        """
        This function downloads the photos embedded in the tweet.
        :param path_to_save: This parameter indicates where the photos are saved.
        :return: It returns None
        """

        assert isinstance(path_to_save, str), "The path_to_save has to be string"

        urls = self.get_tweet_photo_urls()
        MediaDownload.download_photo(urls, path_to_save)
