from tweet_network import TweetNetwork
from user_network import UserNetwork
from tweet_cooccurrence_network import TweetCooccurrenceNetwork
from user_cooccurrence_network import UserCooccurrenceNetwork
from tweet_bipartite_network import TweetBipartiteNetwork
from user_bipartite_network import UserBipartiteNetwork


class Network:
    def __init__(self, tweets):

        assert isinstance(tweets, list), "The tweets has to be a list"

        self._tweet_network = TweetNetwork(tweets)
        self._user_network = UserNetwork(tweets)
        self._tweet_cooccurrence_network = TweetCooccurrenceNetwork(tweets)
        self._user_cooccurrence_network = UserCooccurrenceNetwork(tweets)
        self._tweet_bipartite_network = TweetBipartiteNetwork(tweets)
        self._user_bipartite_network = UserBipartiteNetwork(tweets)

    def get_tweet_network(self):
        return self._tweet_network

    def get_user_network(self):
        return self._user_network

    def get_tweet_cooccurrence_network(self):
        return self._tweet_cooccurrence_network

    def get_user_cooccurrence_network(self):
        return self._user_cooccurrence_network

    def get_tweet_bipartite_network(self):
        return self._tweet_bipartite_network

    def get_user_bipartite_network(self):
        return self._user_bipartite_network










    # def network_building(self, requested_network="tweet_level_retweet_network"):
    #     if requested_network == "tweet_level_retweet_network":
    #         return self.tweet_level_retweet_network_building()
    #     elif requested_network == "tweet_level_quote_network":
    #         return self.tweet_level_quote_network_building()
    #     elif requested_network == "tweet_level_reply_network":
    #         return self.tweet_level_reply_network_building()
    #     elif requested_network == "tweet_level_quote_reply_network":
    #         return self.tweet_level_quote_reply_network_building()
    #     elif requested_network == "tweet_level_retweet_reply_network":
    #         return self.tweet_level_retweet_reply_network_building()
    #     elif requested_network == "tweet_level_retweet_quote_network":
    #         return self.tweet_level_retweet_quote_network_building()
    #     elif requested_network == "tweet_level_retweet_quote_reply_network":
    #         return self.tweet_level_retweet_quote_reply_network_building()
    #     elif requested_network == "tweet_level_cooccurrence_hashtag_network":
    #         return self.tweet_level_cooccurrence_hashtag_network_building()
    #     elif requested_network == "tweet_level_cooccurrence_mention_network":
    #         return self.tweet_level_cooccurrence_mention_network_building()
    #     elif requested_network == "tweet_level_cooccurrence_url_network":
    #         return self.tweet_level_cooccurrence_url_network_building()
    #     elif requested_network == "tweet_hashtag_bipartite_network":
    #         return self.tweet_hashtag_bipartite_network_building()
    #     elif requested_network == "tweet_mention_bipartite_network":
    #         return self.tweet_mention_bipartite_network_building()
    #     elif requested_network == "tweet_url_bipartite_network":
    #         return self.tweet_url_bipartite_network_building()
    #     elif requested_network == "user_level_retweet_network":
    #         return self.user_level_retweet_network_building()
    #     elif requested_network == "user_level_quote_network":
    #         return self.user_level_quote_network_building()
    #     elif requested_network == "user_level_reply_network":
    #         return self.user_level_reply_network_building()
    #     elif requested_network == "user_level_quote_reply_network":
    #         return self.user_level_quote_reply_network_building()
    #     elif requested_network == "user_level_retweet_reply_network":
    #         return self.user_level_retweet_reply_network_building()
    #     elif requested_network == "user_level_retweet_quote_network":
    #         return self.user_level_retweet_quote_network_building()
    #     elif requested_network == "user_level_retweet_quote_reply_network":
    #         return self.user_level_retweet_quote_reply_network_building()
    #     elif requested_network == "user_level_cooccurrence_hashtag_network":
    #         return self.user_level_cooccurrence_hashtag_network_building()
    #     elif requested_network == "user_level_cooccurrence_mention_network":
    #         return self.user_level_cooccurrence_mention_network_building()
    #     elif requested_network == "user_level_cooccurrence_url_network":
    #         return self.user_level_cooccurrence_url_network_building()
    #     elif requested_network == "user_hashtag_bipartite_network":
    #         return self.user_hashtag_bipartite_network_building()
    #     elif requested_network == "user_mention_bipartite_network":
    #         return self.user_mention_bipartite_network_building()
    #     elif requested_network == "user_url_bipartite_network":
    #         return self.user_url_bipartite_network_building()
    #
    # def get_network(self, requested_network="tweet_level_retweet_network"):
    #     if requested_network in self.network_repository:
    #         if requested_network == "tweet_level_retweet_network":
    #             return self.tweet_level_retweet_network
    #         elif requested_network == "tweet_level_quote_network":
    #             return self.tweet_level_quote_network
    #         elif requested_network == "tweet_level_reply_network":
    #             return self.tweet_level_reply_network
    #         elif requested_network == "tweet_level_quote_reply_network":
    #             return self.tweet_level_quote_reply_network
    #         elif requested_network == "tweet_level_retweet_reply_network":
    #             return self.tweet_level_retweet_reply_network
    #         elif requested_network == "tweet_level_retweet_quote_network":
    #             return self.tweet_level_retweet_quote_network
    #         elif requested_network == "tweet_level_retweet_quote_reply_network":
    #             return self.tweet_level_retweet_quote_reply_network
    #         elif requested_network == "tweet_level_cooccurrence_hashtag_network":
    #             return self.tweet_level_cooccurrence_hashtag_network
    #         elif requested_network == "tweet_level_cooccurrence_mention_network":
    #             return self.tweet_level_cooccurrence_mention_network
    #         elif requested_network == "tweet_level_cooccurrence_url_network":
    #             return self.tweet_level_cooccurrence_url_network
    #
    #         elif requested_network == "tweet_hashtag_bipartite_network":
    #             return self.tweet_hashtag_bipartite_network
    #         elif requested_network == "tweet_mention_bipartite_network":
    #             return self.tweet_mention_bipartite_network
    #         elif requested_network == "tweet_url_bipartite_network":
    #             return self.user_url_bipartite_network
    #
    #
    #
    #         elif requested_network == "user_level_retweet_network":
    #             return self.user_level_retweet_network
    #         elif requested_network == "user_level_quote_network":
    #             return self.user_level_quote_network
    #         elif requested_network == "user_level_reply_network":
    #             return self.user_level_reply_network
    #         elif requested_network == "user_level_quote_reply_network":
    #             return self.user_level_quote_reply_network
    #         elif requested_network == "user_level_retweet_reply_network":
    #             return self.user_level_retweet_reply_network
    #         elif requested_network == "user_level_retweet_quote_network":
    #             return self.user_level_quote_reply_network
    #         elif requested_network == "user_level_retweet_quote_reply_network":
    #             return self.user_level_retweet_quote_reply_network
    #         elif requested_network == "user_level_cooccurrence_hashtag_network":
    #             return self.user_level_cooccurrence_hashtag_network
    #         elif requested_network == "user_level_cooccurrence_mention_network":
    #             return self.user_level_cooccurrence_mention_network
    #         elif requested_network == "user_level_cooccurrence_url_network":
    #             return self.user_level_cooccurrence_url_network
    #
    #         elif requested_network == "user_hashtag_bipartite_network":
    #             return self.user_hashtag_bipartite_network
    #         elif requested_network == "user_mention_bipartite_network":
    #             return self.user_mention_bipartite_network
    #         elif requested_network == "user_url_bipartite_network":
    #             return self.user_url_bipartite_network
    #
    # def download_network(self, requested_network="tweet_level_retweet_network", download_format="GEXF", path="", encoding='utf-8'):     #### Tell in the docstring that the path has to be completed and should include the file format!
    #
    #     assert (download_format in ["GEXF", "GML"]), "The available output formats are GEXF and GML"
    #
    #     if requested_network in self.network_repository:
    #         if download_format == "GEXF":
    #             nx.write_gexf(self.get_network(requested_network=requested_network), path=path, encoding=encoding, version='1.2draft')
    #         elif download_format == "GML":
    #             nx.write_gml(self.get_network(requested_network=requested_network), path=path)
    #     else:
    #         print("The network you have requested has not been created yet.")
    #
    # def components_number(self, requested_network="tweet_level_retweet_network"):
    #     """
    #     This function calculates the number of connected components in the desired network.
    #     :return: an integer that shows the number of connected components.
    #     """
    #     requested_network = level_of_resolution + "_level_" + network_type
    #     if requested_network in self.network_repository:
    #         return nx.number_connected_components(self.get_network(requested_network=requested_network).to_undirected())
    #     else:
    #         print("The network type you indicated has not been created yet.")
    #
    # def centrality_measures(self, metric="degree", requested_network="tweet_level_retweet_network"):
    #     """
    #     This function measures network centrality based on the chosen metric.
    #     :param metric: metric can be "degree", "closeness", "betweenness", "eigenvector", "katz", and "pagerank". Please
    #     note that for degree centrality it measures both in-degree and out-degree centrality.
    #     :return: This function does not return anything, instead it add the relevant attribute to the caller network object.
    #     To get the network, use get_network() function.
    #     """
    #
    #     assert (metric in ["degree", "closeness", "betweenness", "eigenvector", "katz",
    #                        "pagerank"]), "The metric has to be" \
    #                                      " degree, closeness, betweenness, " \
    #                                      "eigenvector, katz, or pagerank."
    #
    #     if requested_network in self.network_repository:
    #         network = self.get_network(requested_network=requested_network)
    #         if metric == "degree":
    #             # network = self.get_network(network_type=network_type)
    #             degree_centrality = nx.centrality.degree_centrality(network)
    #             for node_id in degree_centrality:
    #                 network.nodes[node_id]["degree_centrality"] = degree_centrality[node_id]
    #             in_degree_centrality = nx.centrality.in_degree_centrality(network)
    #             for node_id in in_degree_centrality:
    #                 network.nodes[node_id]["in_degree_centrality"] = in_degree_centrality[node_id]
    #             out_degree_centrality = nx.centrality.out_degree_centrality(network)
    #             for node_id in out_degree_centrality:
    #                 network.nodes[node_id]["out_degree_centrality"] = out_degree_centrality[node_id]
    #         elif metric == "closeness":
    #             closeness_centrality = nx.centrality.closeness_centrality(network)
    #             for node_id in closeness_centrality:
    #                 network.nodes[node_id]["closeness_centrality"] = closeness_centrality[node_id]
    #         elif metric == "betweenness":
    #             betweenness_centrality = nx.centrality.betweenness_centrality(network)
    #             for node_id in betweenness_centrality:
    #                 network.nodes[node_id]["betweenness_centrality"] = betweenness_centrality[node_id]
    #         elif metric == "eigenvector":
    #             eigenvector_centrality = nx.centrality.eigenvector_centrality_numpy(network)
    #             for node_id in eigenvector_centrality:
    #                 network.nodes[node_id]["eigenvector_centrality"] = eigenvector_centrality[node_id]
    #         elif metric == "katz":
    #             katz_centrality = nx.centrality.katz_centrality_numpy(network)
    #             for node_id in katz_centrality:
    #                 network.nodes[node_id]["katz_centrality"] = katz_centrality[node_id]
    #         elif metric == "pagerank":
    #             pagerank_centrality = nx.pagerank_numpy(network)
    #             for node_id in pagerank_centrality:
    #                 network.nodes[node_id]["pagerank_centrality"] = pagerank_centrality[node_id]
    #     else:
    #         print("The network type you indicated has not been created yet.")
    #
    # def community_detection(self, requested_network="tweet_level_retweet_network", return_type="network"):
    #     """
    #     This function identified communities in the network using Louvain algorithm. PLease note that, it uses the undirected
    #     version of the network.
    #     :param: return_type: The output of this function can be a network with community number as a property of each
    #     node, a dictionary with key-value pairs corresponding to node_id and community_id, and a dictionary with
    #     key-value pairs corresponding to community_id and all the nodes belonging to that community.
    #     :return: Depending on the value of return_type parameter the output of this function varies.
    #     """
    #
    #     assert (return_type in ["network", "node-community", "community-nodes"]), "The type of the output could be either network, node-community, or community-nodes"
    #
    #     if requested_network in self.network_repository:
    #         network = self.get_network(requested_network=requested_network)
    #         partition = community.best_partition(network.to_undirected())
    #         if return_type == "network":
    #             for node_id in partition:
    #                 network.nodes[node_id]["community"] = partition[node_id]
    #         elif return_type == "node-community":
    #             return partition
    #         elif return_type == "community-nodes":
    #             communities = {}
    #             for k, v in partition.items():
    #                 communities[v] = communities.get(v, []) + [k]
    #             return communities
    #     else:
    #         print("The network type you indicated has not been created yet.")

    # def word_count_layer(self):
    #     pass
    #
    # def character_count_layer(self):
    #     pass
    #
    # def sentence_count_layer(self):
    #     pass
    #
    # def word_complexity_layer(self):
    #     pass
    #
    # def sentence_complexity_layer(self):
    #     pass
    #
    # def syllables_complexity_layer(self):
    #     pass
    #
    # def sentiment_layer(self):
    #     pass
    #
    # def readability_layer(self):
    #     pass