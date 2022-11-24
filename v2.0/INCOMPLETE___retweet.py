# from tweet import Tweet
#
#
# class Retweet(Tweet):
#     def __init__(self, tweet):
#         """
#         This is the constructor for the RetweetedClass.
#         :param twt: a tweet object.
#         :param para: a dictionary of necessary objects and modules.
#         """
#         super().__init__()
#         self.tweet = tweet
#
#     def get_entities(self):
#         """
#         This function extracts the full retweet entities including hashtags, mentions, urls, photos, videos, gifs, and symbols
#          from a tweet object.
#         :return: a dictionary containing all the entities.
#         """
#         if self.tweet["truncated"]:
#             tweet_entities = self.tweet["extended_tweet"]["entities"]
#             if "extended_entities" in self.tweet["extended_tweet"].keys():
#                 tweet_entities["media"] = self.tweet["extended_tweet"]["extended_entities"]["media"]
#         else:
#             tweet_entities = self.tweet["entities"]
#             if "extended_entities" in self.tweet.keys():
#                 tweet_entities["media"] = self.tweet["extended_entities"]["media"]
#         return tweet_entities
#
#     def get_text(self):  ## Maybe you need to check this function for retweet and quote class
#         """
#         :return: a string showing the full text of this retweet
#         """
#         if self.tweet["truncated"]:
#             tweet_text = self.tweet["extended_tweet"]["full_text"]
#         else:
#             if "full_text" in self.tweet:
#                 tweet_text = self.tweet["full_text"]
#             else:
#                 tweet_text = self.tweet["text"]
#         return tweet_text