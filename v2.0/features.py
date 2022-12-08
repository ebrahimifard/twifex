from individual_content_features import IndividualContentFeatures
from individual_user_features import IndividualUserFeatures
from individual_meta_features import IndividualMetaFeatures
from mass_content_features import MassContentFeatures
from mass_user_features import MassUserFeatures
from mass_meta_features import MassMetaFeatures
from network_content_features import NetworkContentFeatures
from network_user_features import NetworkUserFeatures
from network_meta_features import NetworkMetaFeatures


class Features:
    def __init__(self, tweets):
        self._tweets = tweets
        self._features_dict = {}
        for tweet in self._tweets.get_tweets_list():
            self._features_dict[tweet.get_tweet_id()] = {}
        self._feature_id_to_name = {0: "__NO_FEATURE__", }

    def get_features(self):
        return self._features_dict

    def get_features_names(self):
        return self._feature_id_to_name

    def get_reverse_features_names(self):
        return {j: i for i, j in self._feature_id_to_name.items()}

    def individual_content_features(self):
        return IndividualContentFeatures(self._tweets, self._features_dict, self._feature_id_to_name)

    def individual_user_features(self):
        return IndividualUserFeatures(self._tweets, self._features_dict, self._feature_id_to_name)

    def individual_meta_features(self):
        return IndividualMetaFeatures(self._tweets, self._features_dict, self._feature_id_to_name)

    # def mass_content_features(self):
    #     return MassContentFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
    #
    # def mass_user_features(self):
    #     return MassUserFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
    #
    # def mass_meta_features(self):
    #     return MassMetaFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
    #
    # def network_content_features(self):
    #     return NetworkContentFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
    #
    # def network_user_features(self):
    #     return NetworkUserFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
    #
    # def network_meta_features(self):
    #     return NetworkMetaFeatures(self._tweets, self._features_dict, self._feature_id_to_name)
