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

twifex = Twifex()

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

modified_tweets = []
for file in tqdm([i for i in os.listdir(path3) if os.path.isfile(path3+i)]):
    if ".json" in file:
        modified_tweets.append(twifex.single_tweet(path3+file))
        print(file)
    else:
        pass


p = twifex.collective_tweets(modified_tweets).topology_based_features().time_independent_features().time_independent_location_independent_network_features().tweet_features()
p.network_building(network_type="retweet")
print("hi")
# p.tweet_length_layer()