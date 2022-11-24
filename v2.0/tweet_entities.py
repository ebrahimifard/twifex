

class TweetEntities:
    def __init__(self, tweet_obj, tweet_json):

        # assert isinstance(tweet_obj, Tweet), "The tweet_obj has to be an instance of Tweet class"
        assert isinstance(tweet_json, dict), "The tweet_json has to be a dict"

        self._tweet = tweet_obj
        self._tweet_entities = {}

        if self._tweet.is_tweet_retweeted():
            if self._tweet.is_tweet_quoted():
                self._tweet_entities["hashtags"] = tweet_json["retweeted_status"]["entities"]["hashtags"]
                self._tweet_entities["symbols"] = tweet_json["retweeted_status"]["entities"]["symbols"]
                self._tweet_entities["user_mentions"] = tweet_json["retweeted_status"]["entities"]["user_mentions"]
                self._tweet_entities["urls"] = [element for element in
                                                tweet_json["retweeted_status"]["entities"]["urls"]
                                                if "twitter.com" not in element["expanded_url"]]
            else:
                self._tweet_entities = tweet_json["retweeted_status"]["entities"]
            if "extended_entities" in tweet_json["retweeted_status"].keys():
                self._tweet_entities["media"] = tweet_json["retweeted_status"]["extended_entities"]["media"]
        elif self._tweet.is_tweet_quoted():
            self._tweet_entities["hashtags"] = tweet_json["entities"]["hashtags"]
            self._tweet_entities["symbols"] = tweet_json["entities"]["symbols"]
            self._tweet_entities["user_mentions"] = tweet_json["entities"]["user_mentions"]
            self._tweet_entities["urls"] = [element for element in tweet_json["entities"]["urls"]
                                            if "twitter.com" not in element["expanded_url"]]
            if "extended_entities" in tweet_json.keys():
                self._tweet_entities["media"] = tweet_json["extended_entities"]["media"]
        else:
            self._tweet_entities["hashtags"] = tweet_json["entities"]["hashtags"]
            self._tweet_entities["symbols"] = tweet_json["entities"]["symbols"]
            self._tweet_entities["user_mentions"] = tweet_json["entities"]["user_mentions"]
            self._tweet_entities["urls"] = [element for element in tweet_json["entities"]["urls"]
                                            if "twitter.com" not in element["expanded_url"]]
            if "extended_entities" in tweet_json.keys():
                self._tweet_entities["media"] = tweet_json["extended_entities"]["media"]
