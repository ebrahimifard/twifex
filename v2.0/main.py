from tweet import Tweet
from tweets import Tweets
from file_collection import FileCollection

from tqdm import tqdm
import pickle as pk
import networkx as nx
from datetime import datetime


# json file collection
test_folder_path = "./../tests/"
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

network_building_flag = False
temporal_tweets_flag = True
spatial_tweets_flag = True
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



# for path in tqdm(json_paths):
#     try:
#         tweet_objects.append(Tweet(path))
#     except:
#         exceptions.append(path)

print("finished")
