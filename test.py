from twifex import *
from tqdm import tqdm
from pprint import pprint
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt


path1 = "./tests/new_tweets/"
path2 = "./tests/people_timeline/"
path3 = "./tests/modified_tweets/"
path4 = "./tests/searched_tweets/"
path5 = "./tests/data/"
path6 = "./tests/just_to_test_hashtag_network/"

twifex = Twifex()


###################################################################################
new_tweets = []
for file in tqdm([i for i in os.listdir(path1) if os.path.isfile(path1+i)]):
    if ".json" in file:
        new_tweets.append(twifex.single_tweet(path1+file))
    else:
        pass

timeline_tweets = []
for file in tqdm([i for i in os.listdir(path2) if os.path.isfile(path2+i)]):
    if ".json" in file:
        timeline_tweets.append(twifex.single_tweet(path2+file))
    else:
        pass

searched_tweets = []
for file in tqdm([i for i in os.listdir(path4) if os.path.isfile(path4+i)]):
    if ".json" in file:
        searched_tweets.append(twifex.single_tweet(path4+file))
    else:
        pass

data_tweets = []
for file in tqdm([i for i in os.listdir(path5) if os.path.isfile(path5+i)]):
    if ".json" in file:
        data_tweets.append(twifex.single_tweet(path5+file))
    else:
        pass

modified_tweets = []
for file in tqdm([i for i in os.listdir(path3) if os.path.isfile(path3+i)]):
    if ".json" in file:
        modified_tweets.append(twifex.single_tweet(path3+file))
    else:
        pass

hashtag_tweets = []
for file in tqdm([i for i in os.listdir(path6) if os.path.isfile(path6+i)]):
    if ".json" in file:
        hashtag_tweets.append(twifex.single_tweet(path6+file))
    else:
        pass
###################################################################################
# _tweets = hashtag_tweets
_tweets = new_tweets

p = twifex.collective_tweets(_tweets).topology_based_features().time_independent_features().time_independent_location_independent_network_features().tweet_features()
q = twifex.collective_tweets(_tweets).topology_based_features().time_independent_features().time_independent_location_independent_network_features().user_features()

p.user_level_retweet_network_building()
print("1")
p.user_level_quote_network_building()
print("2")
p.user_level_reply_network_building()
print("3")
p.user_level_retweet_quote_network_building()
print("4")
p.user_level_quote_reply_network_building()
print("5")
p.user_level_retweet_reply_network_building()
print("6")
p.user_level_retweet_quote_reply_network_building()
print("7")

p.user_level_cooccurrence_hashtag_network_building()
print("8")
p.user_level_cooccurrence_mention_network_building()
print("9")
p.user_level_cooccurrence_url_network_building()
print("10")


p.user_mention_bipartite_network_building()
print("11")
p.user_hashtag_bipartite_network_building()
print("12")
p.user_url_bipartite_network_building()
print("13")



p.tweet_level_retweet_network_building()
print("14")
p.tweet_level_quote_network_building()
print("15")
p.tweet_level_reply_network_building()
print("16")
p.tweet_level_retweet_quote_network_building()
print("17")
p.tweet_level_quote_reply_network_building()
print("18")
p.tweet_level_retweet_reply_network_building()
print("19")
p.tweet_level_retweet_quote_reply_network_building()
print("20")


p.tweet_level_cooccurrence_hashtag_network_building()
print("21")
p.tweet_level_cooccurrence_mention_network_building()
print("22")
p.tweet_level_cooccurrence_url_network_building()
print("22")

p.tweet_hashtag_bipartite_network_building()
print("23")
p.tweet_mention_bipartite_network_building()
print("24")
p.tweet_url_bipartite_network_building()
print("25")

p.download_network(requested_network="user_level_retweet_network", path="./gexfs/user_level_retweet_network.gexf")
print("26")
p.download_network(requested_network="user_level_quote_network", path="./gexfs/user_level_quote_network.gexf")
print("27")
p.download_network(requested_network="user_level_reply_network", path="./gexfs/user_level_reply_network.gexf")
print("28")
p.download_network(requested_network="user_level_retweet_quote_network", path="./gexfs/user_level_retweet_quote_network.gexf")
print("29")
p.download_network(requested_network="user_level_quote_reply_network", path="./gexfs/user_level_quote_reply_network.gexf")
print("30")
p.download_network(requested_network="user_level_retweet_reply_network", path="./gexfs/user_level_retweet_reply_network.gexf")
print("31")
p.download_network(requested_network="user_level_retweet_quote_reply_network", path="./gexfs/user_level_retweet_quote_reply_network.gexf")
print("32")
p.download_network(requested_network="user_level_cooccurrence_hashtag_network", path="./gexfs/user_level_cooccurrence_hashtag_network.gexf")
print("33")
p.download_network(requested_network="user_level_cooccurrence_mention_network", path="./gexfs/user_level_cooccurrence_mention_network.gexf")
print("34")
p.download_network(requested_network="user_level_cooccurrence_url_network", path="./gexfs/user_level_cooccurrence_url_network.gexf")
print("35")
p.download_network(requested_network="user_mention_bipartite_network", path="./gexfs/user_mention_bipartite_network.gexf")
print("36")
p.download_network(requested_network="user_hashtag_bipartite_network", path="./gexfs/user_hashtag_bipartite_network.gexf")
print("37")
p.download_network(requested_network="user_url_bipartite_network", path="./gexfs/user_url_bipartite_network.gexf")
print("38")

p.download_network(requested_network="tweet_level_retweet_network", path="./gexfs/tweet_level_retweet_network.gexf")
print("39")
p.download_network(requested_network="tweet_level_quote_network", path="./gexfs/tweet_level_quote_network.gexf")
print("40")
p.download_network(requested_network="tweet_level_reply_network", path="./gexfs/tweet_level_reply_network.gexf")
print("41")
p.download_network(requested_network="tweet_level_retweet_quote_network", path="./gexfs/tweet_level_retweet_quote_network.gexf")
print("42")
p.download_network(requested_network="tweet_level_quote_reply_network", path="./gexfs/tweet_level_quote_reply_network.gexf")
print("43")
p.download_network(requested_network="tweet_level_retweet_reply_network", path="./gexfs/tweet_level_retweet_reply_network.gexf")
print("44")
p.download_network(requested_network="tweet_level_retweet_quote_reply_network", path="./gexfs/tweet_level_retweet_quote_reply_network.gexf")
print("45")
p.download_network(requested_network="tweet_level_cooccurrence_hashtag_network", path="./gexfs/tweet_level_cooccurrence_hashtag_network.gexf")
print("46")
p.download_network(requested_network="tweet_level_cooccurrence_mention_network", path="./gexfs/tweet_level_cooccurrence_mention_network.gexf")
print("47")
p.download_network(requested_network="tweet_level_cooccurrence_url_network", path="./gexfs/tweet_level_cooccurrence_url_network.gexf")
print("48")
p.download_network(requested_network="tweet_mention_bipartite_network", path="./gexfs/tweet_mention_bipartite_network.gexf")
print("49")
p.download_network(requested_network="tweet_hashtag_bipartite_network", path="./gexfs/tweet_hashtag_bipartite_network.gexf")
p.download_network(requested_network="tweet_hashtag_bipartite_network", path="./gexfs/tweet_hashtag_bipartite_network.gexf")
print("50")
p.download_network(requested_network="tweet_url_bipartite_network", path="./gexfs/tweet_url_bipartite_network.gexf")
print("51")

p.tweet_length_layer(network_type="tweet_level_retweet_quote_network")
print("52")
p.tweet_complexity_layer(network_type="tweet_level_retweet_quote_reply_network")
print("53")
p.tweet_sentiment_layer(network_type="tweet_level_retweet_quote_reply_network")
print("54")
p.tweet_readability_layer(network_type="tweet_level_retweet_quote_reply_network")
print("55")

p.download_network(requested_network="tweet_url_bipartite_network", path="./gexfs/tweet_level_retweet_quote_reply_network_with_tweet_feature_layer.gexf")
print("56")
