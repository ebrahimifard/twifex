# from tweet import Tweet
from tweet_media import TweetMedia
from media_download import MediaDownload


class TweetVideo(TweetMedia):
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._videos = None if self._media is None else \
            [element for element in self._media if element["type"] == "video"]

    def get_tweet_video_url(self):
        """
        This function returns the video url in this tweet.
        :return: it returns the video url attached to this tweet in a list.
        """

        videos_urls = []
        if self._videos is None:
            return videos_urls
        else:
            for video in self._videos:
                if "video_info" in video:
                    videos_urls += [item["url"] for item in video["video_info"]["variants"] if
                                    item["content_type"] == 'video/mp4']
            return videos_urls

    def download_tweet_video(self, path_to_save):
        """
        This function downloads the video embedded in the tweet.
        :param path_to_save: This parameter indicates where the video is saved.
        :return: It returns None
        """

        assert isinstance(path_to_save, str), "The path_to_save has to be string"

        urls = self.get_tweet_video_url()
        MediaDownload.download_video(urls, path_to_save)
