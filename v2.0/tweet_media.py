# from tweet import Tweet
from tweet_entities import TweetEntities


class TweetMedia(TweetEntities):
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        super().__init__(tweet_obj, tweet_json)
        self._media = self._tweet_entities["media"] if "media" in self._tweet_entities else None
    
