

class SourceAnalysis:
    # Bovet, A., & Makse, H. A. (2019). Influence of fake news in Twitter during the 2016 US
    # presidential election. Nature communications, 10(1), 1-14.
    official_Twitter_clients = ["Twitter for iPhone", "Twitter for Android", "Twitter Web Client", "Twitter for iPad",
                        "Mobile Web (M5)", "TweetDeck", "Facebook", "Twitter for Windows", "Mobile Web (M2)",
                        "Twitter for Windows Phone", "Mobile Web", "Google", "Twitter for BlackBerry",
                        "Twitter for Android Tablets", "Twitter for Mac", "iOS", "Twitter for BlackBerry®"]

    @classmethod
    def is_official_client(cls, tweet):
        return True if tweet.get_tweet_client() in cls.official_Twitter_clients else False
