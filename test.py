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



p.user_level_hashtag_network_building()
p.user_level_mention_network_building()
p.user_level_url_network_building()
p.mention_network_building()
p.hashtag_network_building()
p.url_network_building()
p.tweet_level_hashtag_network_building()

print("Hi")

