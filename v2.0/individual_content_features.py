from tweet_text_analysis import TweetTextAnalysis


class IndividualContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name):
        self._tweets_collection = tweets
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()

    def tweet_character_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_length.__name__

        for tweet in self._tweets_collection:
            twt_text = tweet.set_tweet_text()
            self._tweets_features[tweet][feature_id] = len(twt_text)

    def tweet_word_count(self):
        pass

    def tweet_sentence_count(self):
        pass

    def tweet_word_complexity(self):
        pass

    def tweet_sentence_complexity(self):
        pass

    def tweet_syllables_complexity(self):
        pass

    def tweet_has_more_characters_than_threshold(self, threshold=0):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        self._features_id_name_dict[feature_id] = tweet_month.__name__

        for tweet in self._tweets_collection:
            twt_text = tweet.set_tweet_text()
            self._tweets_features[tweet][feature_id] = True if len(twt_text) > threshold else False

    def tweet_has_more_words_than_threshold(self, threshold=0):
        pass

    def tweet_has_more_sentences_than_threshold(self, threshold=0):
        pass

    def tweet_lowercase_characters_count(self):
        pass

    def tweet_uppercase_characters_count(self):
        pass

    def tweet_lowercase_words_count(self):
        pass

    def tweet_uppercase_words_count(self):
        pass

    def tweet_lowercase_sentences_count(self):
        pass

    def tweet_uppercase_sentences_count(self):
        pass

    def tweet_lowercase_to_uppercase_characters_fraction(self):
        pass

    def tweet_lowercase_to_uppercase_words_fraction(self):
        pass

    def tweet_lowercase_to_uppercase_sentences_fraction(self):
        pass

    def tweet_lowercase_to_all_characters_fraction(self):
        pass

    def tweet_lowercase_to_all_words_fraction(self):
        pass

    def tweet_lowercase_to_all_sentences_fraction(self):
        pass

    def tweet_exclamation_mark_count(self):
        pass

    def tweet_question_mark_count(self):
        pass

    def tweet_exclamation_mark_to_all_characters_fraction(self):
        pass

    def tweet_question_mark_to_all_characters_fraction(self):
        pass

    def tweet_abbreviation_count(self):
        pass

    def tweet_abbreviation_to_all_words_fraction(self):
        pass

    def tweet_vulgar_count(self):
        pass

    def tweet_vulgar_to_all_words_fraction(self):
        pass

    def tweet_universal_pos_frequency(self):
        pass

    def tweet_detailed_pos_frequency(self):
        pass

    def tweet_ner_frequency(self):
        pass

    def tweet_pronouns_count(self):
        pass

    def tweet_first_singular_pronoun_count(self):
        pass

    def tweet_first_plural_pronoun_count(self):
        pass

    def tweet_second_singular_pronoun_count(self):
        pass

    def tweet_second_plural_pronoun_count(self):
        pass

    def tweet_third_singular_pronoun_count(self):
        pass

    def tweet_third_plural_pronoun_count(self):
        pass

    def tweet_flesch_reading_ease_readability_score(self):
        pass

    def tweet_flesch_kincaid_grade_readability_score(self):
        pass

    def tweet_gunning_fog_readability_score(self):
        pass

    def tweet_smog_index_readability_score(self):
        pass

    def tweet_automated_readability_index_readability_score(self):
        pass

    def tweet_coleman_liau_index_readability_score(self):
        pass

    def tweet_linsear_write_formula_readability_score(self):
        pass

    def tweet_dale_chall_readability_score_readability_score(self):
        pass

    def tweet_subjectivity_score(self):
        pass

    def tweet_polarity_score(self):
        pass

    def tweet_positivity_score_by_VADER(self):
        pass

    def tweet_negativity_score_by_VADER(self):
        pass

    def tweet_neutrality_score_by_VADER(self):
        pass

    def tweet_compound_sentiment_score_by_VADER(self):
        pass

    def tweet_nrc_emotions_score(self):
        pass

    def tweet_VAD_sentiment_score(self):
        pass

