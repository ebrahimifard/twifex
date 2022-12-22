from tweet_text_analysis import TweetTextAnalysis


class IndividualContentFeatures:
    def __init__(self, tweets, features, feature_id_to_name, retweet_flag=False, quote_flag=False):
        self._tweets_obj = tweets
        self._tweets_collection = tweets.get_tweets_list()
        self._tweets_features = features
        self._features_id_name_dict = feature_id_to_name
        self._text_analysis = TweetTextAnalysis()
        self._retweet_flag = retweet_flag
        self._quote_flag = quote_flag

    def tweet_character_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_character_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_character_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_character_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_length

    def tweet_word_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_word_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_word_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_word_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_length

    def tweet_sentence_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_sentence_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_sentence_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_sentence_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_length = self._text_analysis.text_length(input_text=twt_txt, length_unit="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_length

    def tweet_word_complexity(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_word_complexity"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_word_complexity"
        else:
            self._features_id_name_dict[feature_id] = "tweet_word_complexity"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_complexity = self._text_analysis.text_complexity(input_text=twt_txt, complexity_unit="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_complexity

    def tweet_sentence_complexity(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_sentence_complexity"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_sentence_complexity"
        else:
            self._features_id_name_dict[feature_id] = "tweet_sentence_complexity"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_complexity = self._text_analysis.text_complexity(input_text=twt_txt, complexity_unit="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_complexity

    def tweet_syllables_complexity(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_syllables_complexity"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_syllables_complexity"
        else:
            self._features_id_name_dict[feature_id] = "tweet_syllables_complexity"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_text_complexity = self._text_analysis.text_complexity(input_text=twt_txt, complexity_unit="syllables")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_text_complexity

    def tweet_has_more_characters_than_threshold(self, threshold=0):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"tweet_has_more_characters_than_{threshold}"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + f"tweet_has_more_characters_than_{threshold}"
        else:
            self._features_id_name_dict[feature_id] = f"tweet_has_more_characters_than_{threshold}"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_character_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if twt_character_count > threshold else False

    def tweet_has_more_words_than_threshold(self, threshold=0):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"tweet_has_more_words_than_{threshold}"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + f"tweet_has_more_words_than_{threshold}"
        else:
            self._features_id_name_dict[feature_id] = f"tweet_has_more_words_than_{threshold}"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_word_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if twt_word_count > threshold else False

    def tweet_has_more_sentences_than_threshold(self, threshold=0):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + f"tweet_has_more_sentences_than_{threshold}"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + f"tweet_has_more_sentences_than_{threshold}"
        else:
            self._features_id_name_dict[feature_id] = f"tweet_has_more_sentences_than_{threshold}"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_sentence_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = True if twt_sentence_count > threshold else False

    def tweet_lowercase_characters_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_characters_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_characters_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_characters_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_characters_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_characters_count

    def tweet_uppercase_characters_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_uppercase_characters_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_uppercase_characters_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_uppercase_characters_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_characters_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_uppercase_characters_count

    def tweet_lowercase_words_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_words_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_words_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_words_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_words_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_words_count

    def tweet_uppercase_words_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_uppercase_words_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_uppercase_words_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_uppercase_words_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_words_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_uppercase_words_count

    def tweet_lowercase_sentences_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_sentences_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_sentences_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_sentences_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentences_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_sentences_count

    def tweet_uppercase_sentences_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_uppercase_sentences_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_uppercase_sentences_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_uppercase_sentences_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_uppercase_sentences_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_uppercase_sentences_count

    def tweet_lowercase_to_uppercase_characters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_characters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_characters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_characters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_characters_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            twt_uppercase_characters_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_characters_count / twt_uppercase_characters_count if twt_uppercase_characters_count != 0 else None

    def tweet_lowercase_to_uppercase_words_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_words_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_words_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_words_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_words_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            twt_uppercase_words_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_words_count / twt_uppercase_words_count if twt_uppercase_words_count != 0 else None

    def tweet_lowercase_to_uppercase_sentences_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_uppercase_sentences_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_uppercase_sentences_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_uppercase_sentences_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentences_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            twt_uppercase_sentences_count = self._text_analysis.uppercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_sentences_count / twt_uppercase_sentences_count if twt_uppercase_sentences_count != 0 else None

    def tweet_lowercase_to_all_characters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_all_characters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_all_characters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_all_characters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_characters_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="character")
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_characters_count / twt_characters_count if twt_characters_count != 0 else None

    def tweet_lowercase_to_all_words_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_all_words_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_all_words_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_all_words_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_words_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="word")
            twt_words_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_words_count / twt_words_count if twt_words_count != 0 else None

    def tweet_lowercase_to_all_sentences_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_lowercase_to_all_sentences_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_lowercase_to_all_sentences_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_lowercase_to_all_sentences_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_lowercase_sentences_count = self._text_analysis.lowercase_count(input_text=twt_txt, unit_of_analysis="sentence")
            twt_sentences_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="sentence")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_lowercase_sentences_count / twt_sentences_count if twt_sentences_count != 0 else None

    def tweet_exclamation_mark_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_exclamation_mark_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_exclamation_mark_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_exclamation_mark_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            exclamation_mark_count = self._text_analysis.exclamation_mark_count(input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = exclamation_mark_count

    def tweet_question_mark_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_question_mark_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_question_mark_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_question_mark_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            question_mark_count = self._text_analysis.question_mark_count(input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = question_mark_count

    def tweet_exclamation_mark_to_all_characters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_exclamation_mark_to_all_characters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_exclamation_mark_to_all_characters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_exclamation_mark_to_all_characters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            exclamation_mark_count = self._text_analysis.exclamation_mark_count(input_text=twt_txt)
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = exclamation_mark_count / twt_characters_count if twt_characters_count != 0 else None

    def tweet_question_mark_to_all_characters_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_question_mark_to_all_characters_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_question_mark_to_all_characters_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_question_mark_to_all_characters_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            question_mark_count = self._text_analysis.question_mark_count(input_text=twt_txt)
            twt_characters_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="character")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = question_mark_count / twt_characters_count if twt_characters_count != 0 else None

    def tweet_abbreviation_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_abbreviation_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_abbreviation_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_abbreviation_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            abbr_list = self._text_analysis.abbreviations(input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(abbr_list)

    def tweet_abbreviation_to_all_words_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_abbreviation_to_all_words_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_abbreviation_to_all_words_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_abbreviation_to_all_words_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_words_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            twt_abbr_count = len(self._text_analysis.abbreviations(input_text=twt_txt))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_abbr_count / twt_words_count if twt_words_count != 0 else None

    def tweet_vulgar_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_vulgar_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_vulgar_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_vulgar_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            vulgar_list = self._text_analysis.vulgar_words(input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = len(vulgar_list)

    def tweet_vulgar_to_all_words_fraction(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_vulgar_to_all_words_fraction"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_vulgar_to_all_words_fraction"
        else:
            self._features_id_name_dict[feature_id] = "tweet_vulgar_to_all_words_fraction"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            twt_words_count = self._text_analysis.text_length(input_text=twt_txt, length_unit="word")
            twt_vulgar_count = len(self._text_analysis.vulgar_words(input_text=twt_txt))
            self._tweets_features[tweet.get_tweet_id()][feature_id] = twt_vulgar_count / twt_words_count if twt_words_count != 0 else None

    def tweet_pos_frequency(self):
        pos_tags = self._text_analysis.get_pos_tags()
        pos_features_dict = {}
        if self._retweet_flag:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"tweet_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id
        elif self._quote_flag:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"tweet_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id
        else:
            for pos_tag in pos_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"tweet_pos_frequency_{pos_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                pos_features_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                twt_obj = tweet.get_tweet_retweet_object()
                # twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
                feature_indicator = "retweet_" + "tweet_pos_frequency_"
            elif self._quote_flag:
                twt_obj = tweet.get_quote_status_object()
                # twt_txt = tweet.get_quote_status_object().get_tweet_text()
                feature_indicator = "quote_" + "tweet_pos_frequency_"
            else:
                twt_obj = tweet
                # twt_txt = tweet.get_tweet_text()
                feature_indicator = "tweet_pos_frequency_"

            self._text_analysis.parse_tweet_object(twt_obj)
            pos_freq = self._text_analysis.tweet_pos_count()
            # pos_freq = self._text_analysis.tweet_pos_count(input_text=twt_txt)
            for tag in pos_freq:
                self._tweets_features[tweet.get_tweet_id()][pos_features_dict[feature_indicator+tag]] = pos_freq[tag]

    def tweet_ner_frequency(self):
        ner_tags = self._text_analysis.get_ner_tags()
        ner_features_dict = {}
        if self._retweet_flag:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"tweet_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id
        elif self._quote_flag:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"tweet_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id
        else:
            for ner_tag in ner_tags:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"tweet_ner_frequency_{ner_tag}"
                self._features_id_name_dict[feature_id] = feature_name
                ner_features_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
                feature_indicator = "retweet_" + "tweet_ner_frequency_"
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
                feature_indicator = "quote_" + "tweet_ner_frequency_"
            else:
                twt_txt = tweet.get_tweet_text()
                feature_indicator = "tweet_ner_frequency_"

            ner_freq = self._text_analysis.tweet_ner_count(input_text=twt_txt)
            for tag in ner_freq:
                self._tweets_features[tweet.get_tweet_id()][ner_features_dict[feature_indicator+tag]] = ner_freq[tag]

    def tweet_pronouns_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_pronouns_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_pronouns_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_pronouns_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()
            first_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_singular")
            first_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_plural")
            second_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="second_singular")
            second_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="second_plural")
            third_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_singular")
            third_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_plural")
            pronouns_count = first_singular_pronoun_count + first_plural_pronoun_count + second_singular_pronoun_count + second_plural_pronoun_count + third_singular_pronoun_count + third_plural_pronoun_count
            self._tweets_features[tweet.get_tweet_id()][feature_id] = pronouns_count

    def tweet_first_singular_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_first_singular_pronoun_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_first_singular_pronoun_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_first_singular_pronoun_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            first_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_singular")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = first_singular_pronoun_count

    def tweet_first_plural_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_first_plural_pronoun_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_first_plural_pronoun_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_first_plural_pronoun_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            first_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_plural")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = first_plural_pronoun_count

    def tweet_second_singular_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_pronouns_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_pronouns_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_pronouns_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            first_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_singular")
            first_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="first_plural")
            second_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="second_singular")
            second_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="second_plural")
            third_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_singular")
            third_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_plural")
            pronouns_count = first_singular_pronoun_count + first_plural_pronoun_count + second_singular_pronoun_count + second_plural_pronoun_count + third_singular_pronoun_count + third_plural_pronoun_count
            self._tweets_features[tweet.get_tweet_id()][feature_id] = pronouns_count

    def tweet_second_plural_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_second_plural_pronoun_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_second_plural_pronoun_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_second_plural_pronoun_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            second_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="second_plural")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = second_plural_pronoun_count

    def tweet_third_singular_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_third_singular_pronoun_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_third_singular_pronoun_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_third_singular_pronoun_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            third_singular_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_singular")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = third_singular_pronoun_count

    def tweet_third_plural_pronoun_count(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_third_plural_pronoun_count"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_third_plural_pronoun_count"
        else:
            self._features_id_name_dict[feature_id] = "tweet_third_plural_pronoun_count"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            third_plural_pronoun_count = self._text_analysis.text_pronoun_count(input_text=twt_txt, pronoun="third_plural")
            self._tweets_features[tweet.get_tweet_id()][feature_id] = third_plural_pronoun_count

    def tweet_flesch_reading_ease_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_flesch_reading_ease_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_flesch_reading_ease_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_flesch_reading_ease_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            flesch_reading_ease_readability_score = self._text_analysis.readability(readability_metric="flesch_reading_ease", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = flesch_reading_ease_readability_score

    def tweet_flesch_kincaid_grade_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_flesch_kincaid_grade_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_flesch_kincaid_grade_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_flesch_kincaid_grade_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            flesch_kincaid_grade_readability_score = self._text_analysis.readability(readability_metric="flesch_kincaid_grade", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = flesch_kincaid_grade_readability_score

    def tweet_gunning_fog_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_gunning_fog_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_gunning_fog_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_gunning_fog_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            gunning_fog_readability_score = self._text_analysis.readability(readability_metric="gunning_fog", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = gunning_fog_readability_score

    def tweet_smog_index_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_smog_index_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_smog_index_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_smog_index_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            smog_index_readability_score = self._text_analysis.readability(readability_metric="smog_index", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = smog_index_readability_score

    def tweet_automated_readability_index_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_automated_readability_index_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_automated_readability_index_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_automated_readability_index_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            automated_readability_index_readability_score = self._text_analysis.readability(readability_metric="automated_readability_index", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = automated_readability_index_readability_score

    def tweet_coleman_liau_index_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_coleman_liau_index_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_coleman_liau_index_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_coleman_liau_index_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            coleman_liau_index_readability_score = self._text_analysis.readability(readability_metric="coleman_liau_index", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = coleman_liau_index_readability_score

    def tweet_linsear_write_formula_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_linsear_write_formula_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_linsear_write_formula_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_linsear_write_formula_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            linsear_write_formula_readability_score = self._text_analysis.readability(readability_metric="linsear_write_formula", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = linsear_write_formula_readability_score

    def tweet_dale_chall_readability_score_readability_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_dale_chall_readability_score_readability_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_dale_chall_readability_score_readability_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_dale_chall_readability_score_readability_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            dale_chall_readability_score_readability_score = self._text_analysis.readability(readability_metric="dale_chall_readability_score", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = dale_chall_readability_score_readability_score

    def tweet_subjectivity_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_subjectivity_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_subjectivity_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_subjectivity_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="textblob", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["subjectivity"]

    def tweet_polarity_score(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_polarity_score"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_polarity_score"
        else:
            self._features_id_name_dict[feature_id] = "tweet_polarity_score"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="textblob", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["polarity"]

    def tweet_positivity_score_by_vader(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_positivity_score_by_vader"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_positivity_score_by_vader"
        else:
            self._features_id_name_dict[feature_id] = "tweet_positivity_score_by_vader"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="vader", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["positivity_score"]

    def tweet_negativity_score_by_vader(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_negativity_score_by_vader"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_negativity_score_by_vader"
        else:
            self._features_id_name_dict[feature_id] = "tweet_negativity_score_by_vader"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="vader", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["negativity_score"]

    def tweet_neutrality_score_by_vader(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_neutrality_score_by_vader"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_neutrality_score_by_vader"
        else:
            self._features_id_name_dict[feature_id] = "tweet_neutrality_score_by_vader"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="vader", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["neutrality_score"]

    def tweet_compound_sentiment_score_by_vader(self):
        feature_id = max(list(self._features_id_name_dict.keys())) + 1
        if self._retweet_flag:
            self._features_id_name_dict[feature_id] = "retweet_" + "tweet_compound_score_by_vader"
        elif self._quote_flag:
            self._features_id_name_dict[feature_id] = "quote_" + "tweet_compound_score_by_vader"
        else:
            self._features_id_name_dict[feature_id] = "tweet_compound_score_by_vader"

        for tweet in self._tweets_collection:
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
            else:
                twt_txt = tweet.get_tweet_text()

            sentiment_score = self._text_analysis.sentiment_analysis(sentiment_engine="vader", input_text=twt_txt)
            self._tweets_features[tweet.get_tweet_id()][feature_id] = sentiment_score["composite_score"]

    def tweet_nrc_emotions_score(self):
        vader_emotions = self._text_analysis.get_vader_emotional_dimensions()
        vader_emotions_dict = {}
        if self._retweet_flag:
            for vader_emotion in vader_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"tweet_nrc_emotions_score_{vader_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vader_emotions_dict[feature_name] = feature_id
        elif self._quote_flag:
            for vader_emotion in vader_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"tweet_nrc_emotions_score_{vader_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vader_emotions_dict[feature_name] = feature_id
        else:
            for vader_emotion in vader_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"tweet_nrc_emotions_score_{vader_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vader_emotions_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
                feature_indicator = "retweet_" + "tweet_nrc_emotions_score_"
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
                feature_indicator = "quote_" + "tweet_nrc_emotions_score_"
            else:
                twt_txt = tweet.get_tweet_text()
                feature_indicator = "tweet_nrc_emotions_score_"

            vader_emotions = self._text_analysis.sentiment_analysis(sentiment_engine="nrc", input_text=twt_txt)
            for emotion in vader_emotions:
                self._tweets_features[tweet.get_tweet_id()][vader_emotions_dict[feature_indicator+emotion.replace("_score", "")]] = vader_emotions[emotion]

    def tweet_vad_sentiment_score(self):
        vad_emotions = self._text_analysis.get_vad_emotional_dimensions()
        vad_emotions_dict = {}
        if self._retweet_flag:
            for vad_emotion in vad_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "retweet_" + f"tweet_vad_sentiment_score_{vad_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vad_emotions_dict[feature_name] = feature_id
        elif self._quote_flag:
            for vad_emotion in vad_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = "quote_" + f"tweet_vad_sentiment_score_{vad_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vad_emotions_dict[feature_name] = feature_id
        else:
            for vad_emotion in vad_emotions:
                feature_id = max(list(self._features_id_name_dict.keys())) + 1
                feature_name = f"tweet_vad_sentiment_score_{vad_emotion}"
                self._features_id_name_dict[feature_id] = feature_name
                vad_emotions_dict[feature_name] = feature_id

        for tweet in self._tweets_collection:
            feature_indicator = ""
            if self._retweet_flag:
                twt_txt = tweet.get_tweet_retweet_object().get_tweet_text()
                feature_indicator = "retweet_" + "tweet_vad_sentiment_score_"
            elif self._quote_flag:
                twt_txt = tweet.get_quote_status_object().get_tweet_text()
                feature_indicator = "quote_" + "tweet_vad_sentiment_score_"
            else:
                twt_txt = tweet.get_tweet_text()
                feature_indicator = "tweet_vad_sentiment_score_"

            vad_emotions = self._text_analysis.sentiment_analysis(sentiment_engine="vad", input_text=twt_txt)
            for emotion in vad_emotions:
                self._tweets_features[tweet.get_tweet_id()][vad_emotions_dict[feature_indicator+emotion.replace("_score", "")]] = vad_emotions[emotion]

