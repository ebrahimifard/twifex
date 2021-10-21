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
###################################################################################
_tweets = new_tweets


f1, f2, f3, f4 = [], [], [], []
for tweet in tqdm(_tweets):
    if tweet.is_retweeted():
        if tweet.get_retweeted().is_quoted():
            f4.append(tweet)
        else:
            f2.append(tweet)
    elif tweet.is_quoted():
        f3.append(tweet)
    else:
        f1.append(tweet)


p = twifex.collective_tweets(_tweets).topology_based_features().time_independent_features().time_independent_location_independent_network_features().tweet_features()
p.network_building(network_type="retweet")
print("hi1")
try:
    p.tweet_length_layer()
except:
    print("exception")
print("hi2")



q = twifex.collective_tweets(_tweets).topology_based_features().time_independent_features().time_independent_location_independent_network_features().user_features()
q.network_building(network_type="reply")
q.user_followers_count_layer()
q.user_friends_count_layer()
q.user_role_count_layer()
q.download_network(path="./net5.gexf")

print("hi3")