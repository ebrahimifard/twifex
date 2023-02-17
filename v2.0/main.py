from tweet import Tweet
from tweets import Tweets
from features import Features
from file_collection import FileCollection
from tweet_hashtag import TweetHashtag
from tweet_mention import TweetMention
from tweet_url import TweetUrl


from tqdm import tqdm
import pickle as pk
import networkx as nx
from datetime import datetime


# json file collection
test_folder_path = "./../tests/Amir_Ahangi/"
fc = FileCollection()
fc.collect_json(test_folder_path)
json_paths = fc.get_all_json()
print(f"The number of tweets in {test_folder_path} is {len(json_paths)}")

# building tweet objects
tweet_objects = []
exceptions = []
for path in tqdm(json_paths):
    # print("--------------------")
    # print(path)
    tweet_objects.append((Tweet(path), path))


finding_quote_tweets_flag = False
if finding_quote_tweets_flag:
    for pair_obj in tweet_objects:
        if pair_obj[0].is_tweet_quoted() and not pair_obj[0].is_tweet_retweeted():
            print(pair_obj)


# # Checking some condition withing the test tweets and dumping the result in a pickle file
# all_conditions = {}
# for twt_obj in tweet_objects:
#     c_rt = twt_obj[0].is_tweet_retweeted()
#     c_qt = twt_obj[0].is_quote_object_available()
#
#     if c_rt and c_qt:
#         c_fig = True if len(twt_obj[0].get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_vid = True if len(twt_obj[0].get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_gif = True if len(twt_obj[0].get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_url = True if len(twt_obj[0].get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_hsh = True if len(twt_obj[0].get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_mnt = True if len(twt_obj[0].get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rep = twt_obj[0].is_tweet_a_reply()
#         c_geo = twt_obj[0].get_tweet_location().is_tweet_geotagged()
#         c_txt = True if len(twt_obj[0].get_tweet_text()) > 0 else False
#
#         c_rt_fig = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_rt_vid = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_rt_gif = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_rt_url = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_rt_hsh = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_rt_mnt = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rt_rep = twt_obj[0].get_tweet_retweet_object().is_tweet_a_reply()
#         c_rt_geo = twt_obj[0].get_tweet_retweet_object().get_tweet_location().is_tweet_geotagged()
#         c_rt_txt = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_text()) > 0 else False
#
#         c_qt_fig = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_qt_vid = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_qt_gif = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_qt_url = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_qt_hsh = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_qt_mnt = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_qt_rep = twt_obj[0].get_tweet_quote_object().is_tweet_a_reply()
#         c_qt_geo = twt_obj[0].get_tweet_quote_object().get_tweet_location().is_tweet_geotagged()
#         c_qt_txt = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_text()) > 0 else False
#
#         all_conditions[twt_obj[1]] = {"c_rt":c_rt , "c_qt":c_qt , "c_fig":c_fig, "c_vid":c_vid, "c_gif":c_gif, "c_url":c_url, "c_hsh":c_hsh, "c_mnt":c_mnt, "c_rep":c_rep, "c_geo":c_geo, "c_txt":c_txt, "c_rt_fig":c_rt_fig, "c_rt_vid":c_rt_vid, "c_rt_gif":c_rt_gif, "c_rt_url":c_rt_url, "c_rt_hsh":c_rt_hsh, "c_rt_mnt":c_rt_mnt, "c_rt_rep":c_rt_rep, "c_rt_geo":c_rt_geo, "c_rt_txt":c_rt_txt, "c_qt_fig":c_qt_fig, "c_qt_vid":c_qt_vid, "c_qt_gif":c_qt_gif, "c_qt_url":c_qt_url, "c_qt_hsh":c_qt_hsh, "c_qt_mnt":c_qt_mnt, "c_qt_rep":c_qt_rep, "c_qt_geo":c_qt_geo, "c_qt_txt":c_qt_txt}
#
#     elif not c_rt and c_qt:
#         c_fig = True if len(twt_obj[0].get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_vid = True if len(twt_obj[0].get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_gif = True if len(twt_obj[0].get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_url = True if len(twt_obj[0].get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_hsh = True if len(twt_obj[0].get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_mnt = True if len(twt_obj[0].get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rep = twt_obj[0].is_tweet_a_reply()
#         c_geo = twt_obj[0].get_tweet_location().is_tweet_geotagged()
#         c_txt = True if len(twt_obj[0].get_tweet_text()) > 0 else False
#
#         c_qt_fig = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_qt_vid = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_qt_gif = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_qt_url = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_qt_hsh = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_qt_mnt = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_qt_rep = twt_obj[0].get_tweet_quote_object().is_tweet_a_reply()
#         c_qt_geo = twt_obj[0].get_tweet_quote_object().get_tweet_location().is_tweet_geotagged()
#         c_qt_txt = True if len(twt_obj[0].get_tweet_quote_object().get_tweet_text()) > 0 else False
#
#         all_conditions[twt_obj[1]] = {"c_rt":c_rt , "c_qt":c_qt , "c_fig":c_fig, "c_vid":c_vid, "c_gif":c_gif, "c_url":c_url, "c_hsh":c_hsh, "c_mnt":c_mnt, "c_rep":c_rep, "c_geo":c_geo, "c_txt":c_txt, "c_rt_fig":False, "c_rt_vid":False, "c_rt_gif":False, "c_rt_url":False, "c_rt_hsh":False, "c_rt_mnt":False, "c_rt_rep":False, "c_rt_geo":False, "c_rt_txt":False, "c_qt_fig":c_qt_fig, "c_qt_vid":c_qt_vid, "c_qt_gif":c_qt_gif, "c_qt_url":c_qt_url, "c_qt_hsh":c_qt_hsh, "c_qt_mnt":c_qt_mnt, "c_qt_rep":c_qt_rep, "c_qt_geo":c_qt_geo, "c_qt_txt":c_qt_txt}
#
#
#     elif c_rt and not c_qt:
#         c_fig = True if len(twt_obj[0].get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_vid = True if len(twt_obj[0].get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_gif = True if len(twt_obj[0].get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_url = True if len(twt_obj[0].get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_hsh = True if len(twt_obj[0].get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_mnt = True if len(twt_obj[0].get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rep = twt_obj[0].is_tweet_a_reply()
#         c_geo = twt_obj[0].get_tweet_location().is_tweet_geotagged()
#         c_txt = True if len(twt_obj[0].get_tweet_text()) > 0 else False
#
#         c_rt_fig = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_rt_vid = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_rt_gif = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_rt_url = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_rt_hsh = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_rt_mnt = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rt_rep = twt_obj[0].get_tweet_retweet_object().is_tweet_a_reply()
#         c_rt_geo = twt_obj[0].get_tweet_retweet_object().get_tweet_location().is_tweet_geotagged()
#         c_rt_txt = True if len(twt_obj[0].get_tweet_retweet_object().get_tweet_text()) > 0 else False
#
#         all_conditions[twt_obj[1]] = {"c_rt":c_rt , "c_qt":c_qt , "c_fig":c_fig, "c_vid":c_vid, "c_gif":c_gif, "c_url":c_url, "c_hsh":c_hsh, "c_mnt":c_mnt, "c_rep":c_rep, "c_geo":c_geo, "c_txt":c_txt, "c_rt_fig":c_rt_fig, "c_rt_vid":c_rt_vid, "c_rt_gif":c_rt_gif, "c_rt_url":c_rt_url, "c_rt_hsh":c_rt_hsh, "c_rt_mnt":c_rt_mnt, "c_rt_rep":c_rt_rep, "c_rt_geo":c_rt_geo, "c_rt_txt":c_rt_txt, "c_qt_fig":False, "c_qt_vid":False, "c_qt_gif":False, "c_qt_url":False, "c_qt_hsh":False, "c_qt_mnt":False, "c_qt_rep":False, "c_qt_geo":False, "c_qt_txt":False}
#
#     elif not c_rt and not c_qt:
#         c_fig = True if len(twt_obj[0].get_tweet_photos().get_tweet_photo_urls()) > 0 else False
#         c_vid = True if len(twt_obj[0].get_tweet_video().get_tweet_video_url()) > 0 else False
#         c_gif = True if len(twt_obj[0].get_tweet_gif().get_tweet_gif_url()) > 0 else False
#         c_url = True if len(twt_obj[0].get_tweet_urls().get_tweet_urls()) > 0 else False
#         c_hsh = True if len(twt_obj[0].get_tweet_hashtags().get_tweet_hashtags()) > 0 else False
#         c_mnt = True if len(twt_obj[0].get_tweet_mentions().get_tweet_mentions()) > 0 else False
#         c_rep = twt_obj[0].is_tweet_a_reply()
#         c_geo = twt_obj[0].get_tweet_location().is_tweet_geotagged()
#         c_txt = True if len(twt_obj[0].get_tweet_text()) > 0 else False
#
#         all_conditions[twt_obj[1]] = {"c_rt":c_rt , "c_qt":c_qt , "c_fig":c_fig, "c_vid":c_vid, "c_gif":c_gif, "c_url":c_url, "c_hsh":c_hsh, "c_mnt":c_mnt, "c_rep":c_rep, "c_geo":c_geo, "c_txt":c_txt, "c_rt_fig":False, "c_rt_vid":False, "c_rt_gif":False, "c_rt_url":False, "c_rt_hsh":False, "c_rt_mnt":False, "c_rt_rep":False, "c_rt_geo":False, "c_rt_txt":False, "c_qt_fig":False, "c_qt_vid":False, "c_qt_gif":False, "c_qt_url":False, "c_qt_hsh":False, "c_qt_mnt":False, "c_qt_rep":False, "c_qt_geo":False, "c_qt_txt":False}
# pk.dump(all_conditions, open("all_conditions.pk", "wb"))


# Checking network building

# building a tweets object
test_tweets = Tweets([i[0] for i in tweet_objects])

tweet_hashtag_flag = False
tweet_mention_flag = False
tweet_url_flag = False
network_building_flag = False
temporal_tweets_flag = False
spatial_tweets_flag = False
features_flag = True

individual_features_flag = False
mass_features_flag = True

individual_content_features_flag = False
individual_user_features_flag = False
individual_meta_features_flag = False

mass_content_features_flag = True
mass_user_features_flag = True
mass_meta_features_flag = True

individual_retweet_content_features_flag = False
individual_retweet_user_features_flag = False
individual_retweet_meta_features_flag = False
individual_quote_content_features_flag = False
individual_quote_user_features_flag = False
individual_quote_meta_features_flag = False

if tweet_hashtag_flag:
    hashtag_obj = TweetHashtag()
    text = "Stay tuned! Santa should have this #cuttingedge #thisishuge #whatisthis remix ready for you by Christmas Eve##a12_1_ ###stackoverflòw ##12_1,-equalsign #army #jhope #this-is-not-a-hashtag #nufsaid ##_asdd  #$ASDsad #asdasd%dsf ##asddd#sadasd#asdasd #سشیشسی_شسیasd🎁"
    hashtag_list = hashtag_obj.get_tweet_hashtags(input_text=text)
    text_splitted_hashtags = hashtag_obj.hashtag_splitter(input_text=text)
    text_removed_hashtags = hashtag_obj.hashtags_removal(input_text=text)
    print()
if tweet_mention_flag:
    mention_obj = TweetMention()
    text = "hello @realDonaldTrump @elonmusk @NCTsmtown_127 @bayer04_en #test #first_tweets #first @@F1 ##Tweets hello hello"
    mention_list = mention_obj.get_tweet_mentions(input_text=text)
    text_removed_mentioned = mention_obj.mentions_removal(input_text=text)
    print()
if tweet_url_flag:
    url_obj = TweetUrl()
    text = "hello hello www.google.com https://bit.ly/3GxSnfz There is always a Polar Bear plunge to participate in Santa Monica to start your New Year in the cold Pacific Ocean.  Or if you like to stay dry enjoy First Day Hikes which you can find at http://parks.ca.gov or follow this bitly link... http://facebook.com/29078041094225 Left out the part where we agreed on everything. — Musk Scolds Dilbert Creator Scott Adams After Poll On 'Elites' Trying to Reduce Population: 'Run Antivirus Software In Your Brain' https://mediaite.com/a/puzpj I'm reading a book a week in 2023. Classics, sci-fi, nonfiction, or anything people highly recommend. I'll keep adjusting the list. Start on Monday, done by Sunday. Might make lowkey videos of takeaways. If you want to read along, the current list is here: http://lexfridman.com/reading-list"
    url_list = url_obj.get_tweet_urls(input_text=text)
    expanded_url_list = url_obj.get_tweet_urls(input_text=text, return_format="expanded_url")
    text_removed_urls = url_obj.url_removal(input_text=text)
    print()
if network_building_flag:
    # First: tweet-level networks
    tweet_level_reply_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_reply_network_building()
    tweet_level_retweet_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_retweet_network_building()
    tweet_level_quote_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_quote_network_building()
    tweet_level_quote_reply_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_quote_reply_network_building()
    tweet_level_retweet_reply_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_retweet_reply_network_building()
    tweet_level_retweet_quote_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_retweet_quote_network_building()
    tweet_level_retweet_quote_reply_network = test_tweets.get_tweets_network().get_tweet_network().tweet_level_retweet_quote_reply_network_building()

    nx.write_gexf(tweet_level_reply_network, f"./outputs/networks/tweet_level_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_retweet_network, f"./outputs/networks/tweet_level_retweet_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_quote_network, f"./outputs/networks/tweet_level_quote_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_quote_reply_network, f"./outputs/networks/tweet_level_quote_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_retweet_reply_network, f"./outputs/networks/tweet_level_retweet_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_retweet_quote_network, f"./outputs/networks/tweet_level_retweet_quote_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_retweet_quote_reply_network, f"./outputs/networks/tweet_level_retweet_quote_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")

    # Second: user-level networks
    user_level_reply_network = test_tweets.get_tweets_network().get_user_network().user_level_reply_network_building()
    user_level_retweet_network = test_tweets.get_tweets_network().get_user_network().user_level_retweet_network_building()
    user_level_quote_network = test_tweets.get_tweets_network().get_user_network().user_level_quote_network_building()
    user_level_quote_reply_network = test_tweets.get_tweets_network().get_user_network().user_level_quote_reply_network_building()
    user_level_retweet_reply_network = test_tweets.get_tweets_network().get_user_network().user_level_retweet_reply_network_building()
    user_level_retweet_quote_network = test_tweets.get_tweets_network().get_user_network().user_level_retweet_quote_network_building()
    user_level_retweet_quote_reply_network = test_tweets.get_tweets_network().get_user_network().user_level_retweet_quote_reply_network_building()

    nx.write_gexf(user_level_reply_network, f"./outputs/networks/user_level_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_retweet_network, f"./outputs/networks/user_level_retweet_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_quote_network, f"./outputs/networks/user_level_quote_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_quote_reply_network, f"./outputs/networks/user_level_quote_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_retweet_reply_network, f"./outputs/networks/user_level_retweet_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_retweet_quote_network, f"./outputs/networks/user_level_retweet_quote_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_retweet_quote_reply_network, f"./outputs/networks/user_level_retweet_quote_reply_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")

    # Third: tweet-level cooccurrence network
    tweet_level_cooccurrence_hashtag_network = test_tweets.get_tweets_network().get_tweet_cooccurrence_network().tweet_level_cooccurrence_hashtag_network_building()
    tweet_level_cooccurrence_mention_network = test_tweets.get_tweets_network().get_tweet_cooccurrence_network().tweet_level_cooccurrence_mention_network_building()
    tweet_level_cooccurrence_url_network = test_tweets.get_tweets_network().get_tweet_cooccurrence_network().tweet_level_cooccurrence_url_network_building()

    nx.write_gexf(tweet_level_cooccurrence_hashtag_network, f"./outputs/networks/tweet_level_cooccurrence_hashtag_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_cooccurrence_mention_network, f"./outputs/networks/tweet_level_cooccurrence_mention_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_level_cooccurrence_url_network, f"./outputs/networks/tweet_level_cooccurrence_url_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")

    # Fourth: user-level cooccurrence network
    user_level_cooccurrence_hashtag_network = test_tweets.get_tweets_network().get_user_cooccurrence_network().user_level_cooccurrence_hashtag_network_building()
    user_level_cooccurrence_mention_network = test_tweets.get_tweets_network().get_user_cooccurrence_network().user_level_cooccurrence_mention_network_building()
    user_level_cooccurrence_url_network = test_tweets.get_tweets_network().get_user_cooccurrence_network().user_level_cooccurrence_url_network_building()

    nx.write_gexf(user_level_cooccurrence_hashtag_network, f"./outputs/networks/user_level_cooccurrence_hashtag_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_cooccurrence_mention_network, f"./outputs/networks/user_level_cooccurrence_mention_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_level_cooccurrence_url_network, f"./outputs/networks/user_level_cooccurrence_url_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")

    # Fifth: tweet-level bipartite network
    tweet_hashtag_bipartite_network = test_tweets.get_tweets_network().get_tweet_bipartite_network().tweet_hashtag_bipartite_network_building()
    tweet_mention_bipartite_network = test_tweets.get_tweets_network().get_tweet_bipartite_network().tweet_mention_bipartite_network_building()
    tweet_url_bipartite_network = test_tweets.get_tweets_network().get_tweet_bipartite_network().tweet_url_bipartite_network_building()

    nx.write_gexf(tweet_hashtag_bipartite_network, f"./outputs/networks/tweet_hashtag_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_mention_bipartite_network, f"./outputs/networks/tweet_mention_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(tweet_url_bipartite_network, f"./outputs/networks/tweet_url_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")

    # Sixth: user-level bipartite network
    user_hashtag_bipartite_network = test_tweets.get_tweets_network().get_user_bipartite_network().user_hashtag_bipartite_network_building()
    user_mention_bipartite_network = test_tweets.get_tweets_network().get_user_bipartite_network().user_mention_bipartite_network_building()
    user_url_bipartite_network = test_tweets.get_tweets_network().get_user_bipartite_network().user_url_bipartite_network_building()

    nx.write_gexf(user_hashtag_bipartite_network, f"./outputs/networks/user_hashtag_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_mention_bipartite_network, f"./outputs/networks/user_mention_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
    nx.write_gexf(user_url_bipartite_network, f"./outputs/networks/user_url_bipartite_network_{datetime.strftime(datetime.now(), format='%m-%d-%Y')}.gexf")
if temporal_tweets_flag:
    tweets_period = test_tweets.get_temporal_tweets().tweets_period()
    for res in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]:
        for st_point in ["first_of_month", "first_tweet"]:
            for freq in range(1, 11):
                print(res, st_point, freq)
                tweets_in_periods = test_tweets.get_temporal_tweets().tweets_in_periods(resolution=res, frequency=freq, starting_point=st_point)
if spatial_tweets_flag:
    for unit in ["country", "city", "poi", "polygon_coordinates", "point_coordinates", ]:
        print(unit)
        tweets_distinct_locations = test_tweets.get_spatial_tweets().get_tweets_distinct_locations(spatial_unit=unit)
        tweets_with_location = test_tweets.get_spatial_tweets().get_tweets_with_location(spatial_unit=unit)

if features_flag:
    tweets_features = Features(test_tweets)
    if individual_features_flag:
        if individual_content_features_flag:
            individual_content_features = tweets_features.individual_content_features()
            individual_content_features.tweet_character_count()
            individual_content_features.tweet_word_count()
            individual_content_features.tweet_sentence_count()
            individual_content_features.tweet_word_complexity()
            individual_content_features.tweet_sentence_complexity()
            individual_content_features.tweet_syllables_complexity()
            individual_content_features.tweet_has_more_characters_than_threshold()
            individual_content_features.tweet_has_more_words_than_threshold()
            individual_content_features.tweet_has_more_sentences_than_threshold()
            individual_content_features.tweet_lowercase_characters_count()
            individual_content_features.tweet_uppercase_characters_count()
            individual_content_features.tweet_lowercase_words_count()
            individual_content_features.tweet_uppercase_words_count()
            individual_content_features.tweet_lowercase_sentences_count()
            individual_content_features.tweet_uppercase_sentences_count()
            individual_content_features.tweet_lowercase_to_uppercase_characters_fraction()
            individual_content_features.tweet_lowercase_to_uppercase_words_fraction()
            individual_content_features.tweet_lowercase_to_uppercase_sentences_fraction()
            individual_content_features.tweet_lowercase_to_all_characters_fraction()
            individual_content_features.tweet_lowercase_to_all_words_fraction()
            individual_content_features.tweet_lowercase_to_all_sentences_fraction()
            individual_content_features.tweet_exclamation_mark_count()
            individual_content_features.tweet_question_mark_count()
            individual_content_features.tweet_exclamation_mark_to_all_characters_fraction()
            individual_content_features.tweet_question_mark_to_all_characters_fraction()
            individual_content_features.tweet_abbreviation_count()
            individual_content_features.tweet_abbreviation_to_all_words_fraction()
            individual_content_features.tweet_vulgar_count()
            individual_content_features.tweet_vulgar_to_all_words_fraction()
            individual_content_features.tweet_pos_frequency()
            individual_content_features.tweet_ner_frequency()
            individual_content_features.tweet_pronouns_count()
            individual_content_features.tweet_first_singular_pronoun_count()
            individual_content_features.tweet_first_plural_pronoun_count()
            individual_content_features.tweet_second_singular_pronoun_count()
            individual_content_features.tweet_second_plural_pronoun_count()
            individual_content_features.tweet_third_singular_pronoun_count()
            individual_content_features.tweet_third_plural_pronoun_count()
            individual_content_features.tweet_flesch_reading_ease_readability_score()
            individual_content_features.tweet_flesch_kincaid_grade_readability_score()
            individual_content_features.tweet_gunning_fog_readability_score()
            individual_content_features.tweet_smog_index_readability_score()
            individual_content_features.tweet_automated_readability_index_readability_score()
            individual_content_features.tweet_coleman_liau_index_readability_score()
            individual_content_features.tweet_linsear_write_formula_readability_score()
            individual_content_features.tweet_dale_chall_readability_score_readability_score()
            individual_content_features.tweet_subjectivity_score()
            individual_content_features.tweet_polarity_score()
            individual_content_features.tweet_positivity_score_by_vader()
            individual_content_features.tweet_negativity_score_by_vader()
            individual_content_features.tweet_neutrality_score_by_vader()
            individual_content_features.tweet_compound_sentiment_score_by_vader()
            individual_content_features.tweet_nrc_emotions_score()
            individual_content_features.tweet_vad_sentiment_score()
        if individual_user_features_flag:
            individual_user_features = tweets_features.individual_user_features()
            individual_user_features.user_screen_name_length()
            individual_user_features.user_screen_name_digits_count()
            individual_user_features.user_screen_name_letters_count()
            individual_user_features.user_screen_name_digits_to_letter_fraction()
            individual_user_features.user_screen_name_maximum_adjacent_letters_to_all_letters_fraction()
            individual_user_features.user_screen_name_maximum_adjacent_digits_to_all_digits_fraction()
            individual_user_features.user_screen_name_average_distance_between_subsequent_letters()
            individual_user_features.user_screen_name_average_distance_between_subsequent_digits()
            individual_user_features.user_screen_name_vowels_to_all_letters_fraction()
            individual_user_features.user_screen_name_average_distance_between_subsequent_vowels()
            individual_user_features.user_screen_name_average_distance_between_subsequent_consonants()
            individual_user_features.user_screen_name_non_alphanumeric_to_all_characters_fraction()
            individual_user_features.user_is_account_protected()
            individual_user_features.user_is_account_verified()
            individual_user_features.user_followers_count()
            individual_user_features.user_followees_count()
            individual_user_features.user_role()
            individual_user_features.user_reputation()
            individual_user_features.user_status_count()
            individual_user_features.user_likes_count()
            individual_user_features.user_account_age()
            individual_user_features.user_average_follow_speed()
            individual_user_features.user_being_followed_speed()
            individual_user_features.user_average_like_speed()
            individual_user_features.user_average_status_speed()
            individual_user_features.user_has_profile_picture()
            individual_user_features.user_has_profile_banner()
            individual_user_features.user_has_profile_description()
            individual_user_features.user_description_pos_frequency()
            individual_user_features.user_description_ner_frequency()
            individual_user_features.user_description_length()
            individual_user_features.user_has_profile_location()
        if individual_meta_features_flag:
            individual_meta_features = tweets_features.individual_meta_features()
            individual_meta_features.tweet_month()
            individual_meta_features.tweet_week()
            individual_meta_features.tweet_day_of_month()
            individual_meta_features.tweet_weekday()
            individual_meta_features.tweet_hour()
            individual_meta_features.tweet_minute()
            individual_meta_features.tweet_second()
            individual_meta_features.tweet_is_in_certain_period()
            individual_meta_features.any_hashtag()
            individual_meta_features.hashtags_count()
            individual_meta_features.any_mention()
            individual_meta_features.mentions_count()
            individual_meta_features.any_url()
            individual_meta_features.urls_count()
            individual_meta_features.any_photo()
            individual_meta_features.photos_count()
            individual_meta_features.any_video()
            individual_meta_features.any_gif()
            individual_meta_features.likes_count()
            individual_meta_features.retweets_count()
            individual_meta_features.is_this_a_reply()
            individual_meta_features.is_this_geotagged_with_point_coordinates()
            individual_meta_features.is_this_geotagged_with_polygone_coordinates()
            individual_meta_features.is_this_a_retweet()
            individual_meta_features.is_this_a_quote()
            if individual_retweet_content_features_flag:
                retweet_content_features = individual_meta_features.retweet_content_features()
                retweet_content_features.tweet_character_count()
                retweet_content_features.tweet_word_count()
                retweet_content_features.tweet_sentence_count()
                retweet_content_features.tweet_word_complexity()
                retweet_content_features.tweet_sentence_complexity()
                retweet_content_features.tweet_syllables_complexity()
                retweet_content_features.tweet_has_more_characters_than_threshold()
                retweet_content_features.tweet_has_more_words_than_threshold()
                retweet_content_features.tweet_has_more_sentences_than_threshold()
                retweet_content_features.tweet_lowercase_characters_count()
                retweet_content_features.tweet_uppercase_characters_count()
                retweet_content_features.tweet_lowercase_words_count()
                retweet_content_features.tweet_uppercase_words_count()
                retweet_content_features.tweet_lowercase_sentences_count()
                retweet_content_features.tweet_uppercase_sentences_count()
                retweet_content_features.tweet_lowercase_to_uppercase_characters_fraction()
                retweet_content_features.tweet_lowercase_to_uppercase_words_fraction()
                retweet_content_features.tweet_lowercase_to_uppercase_sentences_fraction()
                retweet_content_features.tweet_lowercase_to_all_characters_fraction()
                retweet_content_features.tweet_lowercase_to_all_words_fraction()
                retweet_content_features.tweet_lowercase_to_all_sentences_fraction()
                retweet_content_features.tweet_exclamation_mark_count()
                retweet_content_features.tweet_question_mark_count()
                retweet_content_features.tweet_exclamation_mark_to_all_characters_fraction()
                retweet_content_features.tweet_question_mark_to_all_characters_fraction()
                retweet_content_features.tweet_abbreviation_count()
                retweet_content_features.tweet_abbreviation_to_all_words_fraction()
                retweet_content_features.tweet_vulgar_count()
                retweet_content_features.tweet_vulgar_to_all_words_fraction()
                retweet_content_features.tweet_pos_frequency()
                retweet_content_features.tweet_ner_frequency()
                retweet_content_features.tweet_pronouns_count()
                retweet_content_features.tweet_first_singular_pronoun_count()
                retweet_content_features.tweet_first_plural_pronoun_count()
                retweet_content_features.tweet_second_singular_pronoun_count()
                retweet_content_features.tweet_second_plural_pronoun_count()
                retweet_content_features.tweet_third_singular_pronoun_count()
                retweet_content_features.tweet_third_plural_pronoun_count()
                retweet_content_features.tweet_flesch_reading_ease_readability_score()
                retweet_content_features.tweet_flesch_kincaid_grade_readability_score()
                retweet_content_features.tweet_gunning_fog_readability_score()
                retweet_content_features.tweet_smog_index_readability_score()
                retweet_content_features.tweet_automated_readability_index_readability_score()
                retweet_content_features.tweet_coleman_liau_index_readability_score()
                retweet_content_features.tweet_linsear_write_formula_readability_score()
                retweet_content_features.tweet_dale_chall_readability_score_readability_score()
                retweet_content_features.tweet_subjectivity_score()
                retweet_content_features.tweet_polarity_score()
                retweet_content_features.tweet_positivity_score_by_vader()
                retweet_content_features.tweet_negativity_score_by_vader()
                retweet_content_features.tweet_neutrality_score_by_vader()
                retweet_content_features.tweet_compound_sentiment_score_by_vader()
                retweet_content_features.tweet_nrc_emotions_score()
                retweet_content_features.tweet_vad_sentiment_score()
            if individual_retweet_user_features_flag:
                retweet_user_features = individual_meta_features.retweet_user_features()
                retweet_user_features.user_screen_name_length()
                retweet_user_features.user_screen_name_digits_count()
                retweet_user_features.user_screen_name_letters_count()
                retweet_user_features.user_screen_name_digits_to_letter_fraction()
                retweet_user_features.user_screen_name_maximum_adjacent_letters_to_all_letters_fraction()
                retweet_user_features.user_screen_name_maximum_adjacent_digits_to_all_digits_fraction()
                retweet_user_features.user_screen_name_average_distance_between_subsequent_letters()
                retweet_user_features.user_screen_name_average_distance_between_subsequent_digits()
                retweet_user_features.user_screen_name_vowels_to_all_letters_fraction()
                retweet_user_features.user_screen_name_average_distance_between_subsequent_vowels()
                retweet_user_features.user_screen_name_average_distance_between_subsequent_consonants()
                retweet_user_features.user_screen_name_non_alphanumeric_to_all_characters_fraction()
                retweet_user_features.user_is_account_protected()
                retweet_user_features.user_is_account_verified()
                retweet_user_features.user_followers_count()
                retweet_user_features.user_followees_count()
                retweet_user_features.user_role()
                retweet_user_features.user_reputation()
                retweet_user_features.user_status_count()
                retweet_user_features.user_likes_count()
                retweet_user_features.user_account_age()
                retweet_user_features.user_average_follow_speed()
                retweet_user_features.user_being_followed_speed()
                retweet_user_features.user_average_like_speed()
                retweet_user_features.user_average_status_speed()
                retweet_user_features.user_has_profile_picture()
                retweet_user_features.user_has_profile_banner()
                retweet_user_features.user_has_profile_description()
                retweet_user_features.user_description_pos_frequency()
                retweet_user_features.user_description_ner_frequency()
                retweet_user_features.user_description_length()
                retweet_user_features.user_has_profile_location()
            if individual_retweet_meta_features_flag:
                retweet_meta_features = individual_meta_features.retweet_meta_features()
                retweet_meta_features.tweet_month()
                retweet_meta_features.tweet_week()
                retweet_meta_features.tweet_day_of_month()
                retweet_meta_features.tweet_weekday()
                retweet_meta_features.tweet_hour()
                retweet_meta_features.tweet_minute()
                retweet_meta_features.tweet_second()
                retweet_meta_features.tweet_is_in_certain_period()
                retweet_meta_features.any_hashtag()
                retweet_meta_features.hashtags_count()
                retweet_meta_features.any_mention()
                retweet_meta_features.mentions_count()
                retweet_meta_features.any_url()
                retweet_meta_features.urls_count()
                retweet_meta_features.any_photo()
                retweet_meta_features.photos_count()
                retweet_meta_features.any_video()
                retweet_meta_features.any_gif()
                retweet_meta_features.likes_count()
                retweet_meta_features.retweets_count()
                retweet_meta_features.is_this_a_reply()
                retweet_meta_features.is_this_geotagged_with_point_coordinates()
                retweet_meta_features.is_this_geotagged_with_polygone_coordinates()
                retweet_meta_features.is_this_a_retweet()
                retweet_meta_features.is_this_a_quote()
            if individual_quote_content_features_flag:
                quote_content_features = individual_meta_features.quote_content_features()
                quote_content_features.tweet_character_count()
                quote_content_features.tweet_word_count()
                quote_content_features.tweet_sentence_count()
                quote_content_features.tweet_word_complexity()
                quote_content_features.tweet_sentence_complexity()
                quote_content_features.tweet_syllables_complexity()
                quote_content_features.tweet_has_more_characters_than_threshold()
                quote_content_features.tweet_has_more_words_than_threshold()
                quote_content_features.tweet_has_more_sentences_than_threshold()
                quote_content_features.tweet_lowercase_characters_count()
                quote_content_features.tweet_uppercase_characters_count()
                quote_content_features.tweet_lowercase_words_count()
                quote_content_features.tweet_uppercase_words_count()
                quote_content_features.tweet_lowercase_sentences_count()
                quote_content_features.tweet_uppercase_sentences_count()
                quote_content_features.tweet_lowercase_to_uppercase_characters_fraction()
                quote_content_features.tweet_lowercase_to_uppercase_words_fraction()
                quote_content_features.tweet_lowercase_to_uppercase_sentences_fraction()
                quote_content_features.tweet_lowercase_to_all_characters_fraction()
                quote_content_features.tweet_lowercase_to_all_words_fraction()
                quote_content_features.tweet_lowercase_to_all_sentences_fraction()
                quote_content_features.tweet_exclamation_mark_count()
                quote_content_features.tweet_question_mark_count()
                quote_content_features.tweet_exclamation_mark_to_all_characters_fraction()
                quote_content_features.tweet_question_mark_to_all_characters_fraction()
                quote_content_features.tweet_abbreviation_count()
                quote_content_features.tweet_abbreviation_to_all_words_fraction()
                quote_content_features.tweet_vulgar_count()
                quote_content_features.tweet_vulgar_to_all_words_fraction()
                quote_content_features.tweet_pos_frequency()
                quote_content_features.tweet_ner_frequency()
                quote_content_features.tweet_pronouns_count()
                quote_content_features.tweet_first_singular_pronoun_count()
                quote_content_features.tweet_first_plural_pronoun_count()
                quote_content_features.tweet_second_singular_pronoun_count()
                quote_content_features.tweet_second_plural_pronoun_count()
                quote_content_features.tweet_third_singular_pronoun_count()
                quote_content_features.tweet_third_plural_pronoun_count()
                quote_content_features.tweet_flesch_reading_ease_readability_score()
                quote_content_features.tweet_flesch_kincaid_grade_readability_score()
                quote_content_features.tweet_gunning_fog_readability_score()
                quote_content_features.tweet_smog_index_readability_score()
                quote_content_features.tweet_automated_readability_index_readability_score()
                quote_content_features.tweet_coleman_liau_index_readability_score()
                quote_content_features.tweet_linsear_write_formula_readability_score()
                quote_content_features.tweet_dale_chall_readability_score_readability_score()
                quote_content_features.tweet_subjectivity_score()
                quote_content_features.tweet_polarity_score()
                quote_content_features.tweet_positivity_score_by_vader()
                quote_content_features.tweet_negativity_score_by_vader()
                quote_content_features.tweet_neutrality_score_by_vader()
                quote_content_features.tweet_compound_sentiment_score_by_vader()
                quote_content_features.tweet_nrc_emotions_score()
                quote_content_features.tweet_vad_sentiment_score()
            if individual_quote_user_features_flag:
                quote_user_features = individual_meta_features.quote_user_features()
                quote_user_features.user_screen_name_length()
                quote_user_features.user_screen_name_digits_count()
                quote_user_features.user_screen_name_letters_count()
                quote_user_features.user_screen_name_digits_to_letter_fraction()
                quote_user_features.user_screen_name_maximum_adjacent_letters_to_all_letters_fraction()
                quote_user_features.user_screen_name_maximum_adjacent_digits_to_all_digits_fraction()
                quote_user_features.user_screen_name_average_distance_between_subsequent_letters()
                quote_user_features.user_screen_name_average_distance_between_subsequent_digits()
                quote_user_features.user_screen_name_vowels_to_all_letters_fraction()
                quote_user_features.user_screen_name_average_distance_between_subsequent_vowels()
                quote_user_features.user_screen_name_average_distance_between_subsequent_consonants()
                quote_user_features.user_screen_name_non_alphanumeric_to_all_characters_fraction()
                quote_user_features.user_is_account_protected()
                quote_user_features.user_is_account_verified()
                quote_user_features.user_followers_count()
                quote_user_features.user_followees_count()
                quote_user_features.user_role()
                quote_user_features.user_reputation()
                quote_user_features.user_status_count()
                quote_user_features.user_likes_count()
                quote_user_features.user_account_age()
                quote_user_features.user_average_follow_speed()
                quote_user_features.user_being_followed_speed()
                quote_user_features.user_average_like_speed()
                quote_user_features.user_average_status_speed()
                quote_user_features.user_has_profile_picture()
                quote_user_features.user_has_profile_banner()
                quote_user_features.user_has_profile_description()
                quote_user_features.user_description_pos_frequency()
                quote_user_features.user_description_ner_frequency()
                quote_user_features.user_description_length()
                quote_user_features.user_has_profile_location()
            if individual_quote_meta_features_flag:
                quote_meta_features = individual_meta_features.quote_meta_features()
                quote_meta_features.tweet_month()
                quote_meta_features.tweet_week()
                quote_meta_features.tweet_day_of_month()
                quote_meta_features.tweet_weekday()
                quote_meta_features.tweet_hour()
                quote_meta_features.tweet_minute()
                quote_meta_features.tweet_second()
                quote_meta_features.tweet_is_in_certain_period()
                quote_meta_features.any_hashtag()
                quote_meta_features.hashtags_count()
                quote_meta_features.any_mention()
                quote_meta_features.mentions_count()
                quote_meta_features.any_url()
                quote_meta_features.urls_count()
                quote_meta_features.any_photo()
                quote_meta_features.photos_count()
                quote_meta_features.any_video()
                quote_meta_features.any_gif()
                quote_meta_features.likes_count()
                quote_meta_features.retweets_count()
                quote_meta_features.is_this_a_reply()
                quote_meta_features.is_this_geotagged_with_point_coordinates()
                quote_meta_features.is_this_geotagged_with_polygone_coordinates()
                quote_meta_features.is_this_a_retweet()
                quote_meta_features.is_this_a_quote()
    if mass_features_flag:
        if mass_content_features_flag:
            mass_content_features = tweets_features.mass_content_features(temporal=False, spatial=False)
            mass_content_features.tweets_character_count_statistics()
            mass_content_features.tweets_word_count_statistics()
            mass_content_features.tweets_sentence_count_statistics()
            mass_content_features.tweets_syllables_count_statistics()
            mass_content_features.tweets_word_length_statistics()
            mass_content_features.tweets_sentence_length_statistics()
            mass_content_features.tweets_lowercase_character_count_statistics()
            mass_content_features.tweets_uppercase_character_count_statistics()
            mass_content_features.tweets_lowercase_word_count_statistics()
            mass_content_features.tweets_uppercase_word_count_statistics()
            mass_content_features.tweets_lowercase_sentence_count_statistics()
            mass_content_features.tweets_uppercase_sentence_count_statistics()
            mass_content_features.tweet_lowercase_to_uppercase_characters_fraction_statistics()
            mass_content_features.tweet_lowercase_to_uppercase_words_fraction_statistics()
            mass_content_features.tweet_lowercase_to_uppercase_sentences_fraction_statistics()
            mass_content_features.tweets_lowercase_to_all_characters_fraction_statistics()
            mass_content_features.tweets_lowercase_to_all_words_fraction_statistics()
            mass_content_features.tweets_lowercase_to_all_sentences_fraction_statistics()
            mass_content_features.tweets_exclamation_mark_count_statistics()
            mass_content_features.tweets_question_mark_count_statistics()
            mass_content_features.tweets_exclamation_mark_to_all_characters_fraction_statistics()
            mass_content_features.tweets_question_mark_to_all_characters_fraction_statistics()
            mass_content_features.tweets_abbreviation_count_statistics()
            mass_content_features.tweets_abbreviation_to_all_words_fraction_statistics()
            mass_content_features.tweets_vulgar_count_statistics()
            mass_content_features.tweets_vulgar_to_all_words_fraction_statistics()
            mass_content_features.tweets_pos_tags_count_statistics()
            mass_content_features.tweets_ner_tags_count_statistics()
            print()
        if mass_user_features_flag:
            pass
        if mass_meta_features_flag:
            pass

    features = tweets_features.get_features()
    features_guideline = tweets_features.get_features_names()



# for path in tqdm(json_paths):
#     try:
#         tweet_objects.append(Tweet(path))
#     except:
#         exceptions.append(path)

print("finished")
