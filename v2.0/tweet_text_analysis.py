import re
from nltk import PorterStemmer
import textstat
import spacy
import en_core_web_sm
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from tweet_hashtag import TweetHashtag
from tweet_mention import TweetMention
from tweet_url import TweetUrl
import html


class TweetTextAnalysis:
    def __init__(self):
        self._tweet = None

        path_to_stopword_corpus = {"stone": "./resources/stopwords(Stone).txt",
                                   "nltk": "./resources/stopwords(nltk).txt",
                                   "corenlp": "./resources/stopwords(corenlp).txt",
                                   "glascow": "./resources/stopwords(glascow).txt"}

        self._stopwords_dict = {}
        for corpus, corpus_path in path_to_stopword_corpus.items():
            with open(corpus_path) as f:
                self._stopwords_dict[corpus] = [stopword.strip() for stopword in f.readlines()]

        # Initialization of SpaCy
        self._nlp = spacy.load("en_core_web_sm")
        # self._nlp = en_core_web_sm.load()

        # Initialization of Vulgar dictionary
        path_to_vulgar_corpus = "./resources/vulgar.txt"
        self._vulgar_words_list = [term.strip() for term in open(path_to_vulgar_corpus).readlines()]

        # Initialization of abbreviations dictionary
        path_to_abbreviations_corpus = "./resources/abbr.txt"
        self._abbreviations_list = [term.strip() for term in open(path_to_abbreviations_corpus).readlines()]

        # Initialization of NRC sentiment analysis
        path_to_nrc_corpus = "./resources/NRC.txt"
        nrc_raw = open(path_to_nrc_corpus).readlines()
        nrc_dic = {}
        for i in nrc_raw:
            tmp = i.strip().split("\t")
            lemma = tmp[0]
            sentiment = tmp[1]
            score = tmp[2]
            if lemma in nrc_dic.keys():
                nrc_dic[lemma][sentiment] = int(score)
            else:
                nrc_dic[lemma] = {sentiment: int(score)}
        self._nrc_corpus = nrc_dic

        # Initialization of VAD sentiment analysis
        path_to_vad_corpus = "./resources/BRM-emot-submit.csv"
        emotions = pd.read_csv(path_to_vad_corpus)
        emotions = emotions[["Word", "V.Mean.Sum", "A.Mean.Sum", "D.Mean.Sum"]]
        emotions.columns = ["word", "valence", "arousal", "dominance"]
        emotions = emotions.T
        emotions.columns = emotions.loc["word"]
        emotions = emotions.drop(["word"], axis="index")
        self._vad_dic = pd.DataFrame.to_dict(emotions)

        # Initialization of VADER sentiment analysis
        self._vader_analyser = SentimentIntensityAnalyzer()

        #POS tags
        self._pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X"]

        #NER_tags
        self._ner_tags = ["CARDINAL", "DATE", "EVENT", "FAC", "GPE", "LANGUAGE", "LAW", "LOC", "MONEY", "NORP", "ORDINAL", "ORG", "PERCENT", "PERSON", "PRODUCT", "QUANTITY", "TIME", "WORK_OF_ART"]

        #vader_emotions
        self._vader_emotions = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

        #vad_dimensions
        self._vad_dimensions = ["valence", "arousal", "dominance"]

        self._tweet_length_limit = 280

    def parse_tweet_object(self, tweet_obj):
        self._tweet = tweet_obj

    def tweet_html_entities_parsing(self, input_text=None, inplace=False):

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        def inner_tweet_html_entities_parsing(inner_input_text=None):
            inner_text = inner_input_text
            # This only works for Python 3.4+
            # In Python3.3 or older:
            # import html.parser
            # html.parser.HTMLParser().unescape('Suzy &amp; John')
            return html.unescape(inner_text)

        if input_text is not None:
            return inner_tweet_html_entities_parsing(inner_input_text=input_text)
        elif input_text is None:
            if self._tweet is not None:
                modified_text = inner_tweet_html_entities_parsing(inner_input_text=self._tweet.get_tweet_text())
                if inplace:
                    self._tweet.set_tweet_text(modified_text)
                    return self._tweet
                else:
                    return modified_text
            elif self._tweet is None:
                return

    def tweet_splitter(self, input_text=None, split_unit="word"):
        """
        this function splits the tweet text field according to chosen splitting unit.
        :param input_text: if this parameter is None, then the caller object text field is splitted, otherwise
        and in case of a string as an input for this parameter, the input text is splitted up.
        :param split_unit: the splitting unit can be "word", or "sentence".
        :return: a list containing the splitting units.
        """

        assert (split_unit in ["word", "sentence"]), "The split_unit argument can be set to word or sentence"

        def inner_tweet_splitter(inner_input_text=None, inner_split_unit="word"):
            inner_text = inner_input_text
            if inner_split_unit == "word":
                return re.findall(r'\S+', inner_text)
            elif inner_split_unit == "sentence":
                return [i for i in re.split(r'[.?!]+', inner_text) if i != '']

        if input_text is not None:
            return inner_tweet_splitter(inner_input_text=input_text, inner_split_unit=split_unit)
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                return inner_tweet_splitter(inner_input_text=text, inner_split_unit=split_unit)
            elif self._tweet is None:
                return

    def tweet_stemming(self, input_text=None, inplace=False):
        """
        This function performs the stemming operation using Porter algorithm.
        :param input_text: if this parameter is None, then stemming is applied on the text field of the caller object, otherwise
        and in case of a string as an input for this parameter, the stemming is applied on the input text.
        :param inplace: if inplace is True, the change is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after stemming.
        :return: when the implace parameter is equal to True, the function changes the caller object text field permanently and
        returns the whole object, in contrast when it is equal to False the function only returns the text field after
        the stemming without changing the text field.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        def inner_tweet_stemming(inner_input_text=None):
            inner_stemmed_text = PorterStemmer().stem(inner_input_text)
            return inner_stemmed_text

        if input_text is not None:
            return inner_tweet_stemming(inner_input_text=input_text)
        elif input_text is None:
            if self._tweet is not None:
                stemmed_text = inner_tweet_stemming(inner_input_text=self._tweet.get_tweet_text())
                if inplace:
                    self._tweet.set_tweet_text(stemmed_text)
                    return self._tweet
                else:
                    return stemmed_text
            elif self._tweet is None:
                return

    def control_characters_removal(self, control_chars_list=r'[\r\t\n]', substitute_char=" ", input_text=None, inplace=False):
        """
        This functions removes common control characters carriage return (\r), line feed (\n), horizontal tab (\t).
        :param input_text: if this parameter is None, then the control characters are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the control characters are removed from the input text.
        :param inplace: if inplace is True, the control characters removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the control characters.
        :param control_chars_list: this parameter indicates the list of characters which will be removed.
        :param substitute_char: the control characters will be replaced by teh value of this parameter.
        :return: when the implace parameter is equal to True, the function removes the control characters permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         control characters from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        def inner_control_characters_removal(inner_control_chars_list=r'[\r\t\n]', inner_substitute_char=" ", inner_input_text=None):
            inner_text = inner_input_text
            inner_pattern = re.compile(inner_control_chars_list)
            inner_modified_text = inner_pattern.sub(inner_substitute_char, inner_text)
            return inner_modified_text

        if input_text is not None:
            return inner_control_characters_removal(inner_control_chars_list=control_chars_list, inner_substitute_char=substitute_char, inner_input_text=input_text)

        elif input_text is None:
            if self._tweet is not None:
                modified_text = inner_control_characters_removal(inner_control_chars_list=control_chars_list, inner_substitute_char=substitute_char, inner_input_text=self._tweet.get_tweet_text())
                if inplace:
                    self._tweet.set_tweet_text(modified_text)
                    return self._tweet
                else:
                    return modified_text
            elif self._tweet is None:
                return

    def stopwords_removal(self, input_text=None, stopword_corpus="stone", inplace=False):
        """
        This function removes stopwords from the tweet according to chosen stopword corpus.
        :param input_text: if this parameter is None, then the stopwords are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the stopwords are removed from the input text.
        :param stopword_corpus: The stopword corpus can be "stone", "nltk", "corenlp", "glascow", or "spacy". Almost every text mining
         framework uses one of these corpuses for removing the stopwords.
        :param inplace: if inplace is True, the stopwords removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the stopwords.
        :return: when the implace parameter is equal to True, the function removes the stopwords permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
        stopwords from the text.
        """

        assert (stopword_corpus in ["stone", "nltk", "corenlp",
                                    "glascow", "spacy"]), "stopword_orpus can be stone, nltk, corenlp, and glascow"
        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        ##### self inside the inner function
        selected_corpus = self._stopwords_dict[stopword_corpus]
        def inner_stopwords_removal(inner_input_text=None, inner_stopword_corpus="stone"):
            if inner_stopword_corpus == "spacy":
                inner_processed_text = ""
                inner_spacy_text = self._nlp(inner_input_text)
                for inner_token in inner_spacy_text:
                    if not inner_token.token.is_stop:
                        inner_processed_text = inner_processed_text + " " + inner_token
                inner_processed_text = inner_processed_text.strip()
            else:
                inner_words = self.tweet_splitter(inner_input_text)
                inner_processed_text = " ".join([inner_word for inner_word in inner_words if inner_word.lower() not in selected_corpus])
            return inner_processed_text

        if input_text is not None:
            text = input_text
            return inner_stopwords_removal(inner_input_text=input_text, inner_stopword_corpus=stopword_corpus)
        elif input_text is None:
            if self._tweet is not None:
                processed_text = inner_stopwords_removal(inner_input_text=self._tweet.get_tweet_text(), inner_stopword_corpus=stopword_corpus)
                if inplace:
                    self._tweet.set_tweet_text(processed_text)
                    return self._tweet
                else:
                    return processed_text
            elif self._tweet is None:
                return

    def whitespace_removal(self, input_text=None, inplace=False):
        """
        This functions removes whitespaces from the text.
        :param input_text: if this parameter is None, then the whitespaces are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the whitespaces are removed from the input text.
        :param inplace: if inplace is True, the whitespace removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the whitespaces.
        :return: when the implace parameter is equal to True, the function removes the whitespaces permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         whitespaces from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        def inner_whitespace_removal(inner_input_text=None):
            inner_modified_text = inner_input_text.strip()
            while inner_modified_text.count("  ") > 0:
                inner_modified_text = inner_modified_text.replace("  ", " ")
            return inner_modified_text

        if input_text is not None:
            return inner_whitespace_removal(inner_input_text=input_text)
        elif input_text is None:
            if self._tweet is not None:
                modified_text = inner_whitespace_removal(inner_input_text=self._tweet.get_tweet_text())
                if inplace:
                    self._tweet.set_tweet_text(modified_text)
                    return self._tweet
                else:
                    return modified_text
            elif self._tweet is None:
                return

    def punctuation_removal(self, input_text=None, inplace=False):
        """
        This functions removes punctuation characters from the text.
        :param input_text: if this parameter is None, then the punctuations are removed from the caller object text field,
        otherwise and in case of a string as an input for this parameter, the punctuations are removed from the input text.
        :param inplace: if inplace is True, the punctuations removal is permanently applied on the caller object text field, otherwise
        the caller object text field remains intact and the function returns the text after removing the punctuations.
        :return: when the implace parameter is equal to True, the function removes the punctuations permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after removing the
         punctuations from the text.
        """

        assert (inplace in [True, False]), "inplace is a boolean parameter, so it can be True or False"

        def inner_punctuation_removal(inner_input_text=None):
            inner_text = inner_input_text
            inner_punctuation_free = textstat.remove_punctuation(inner_text).replace("(", "").replace(")", "").replace("[",
                                                                                                           "").replace(
                "]", "").replace("{", "").replace("}", "").replace("—", "").replace("–", "").replace("-", "").replace(
                ".", "").replace("?", "").replace("!", "").replace(",", "").replace(";", "").replace(":", "").replace(
                "…", "").replace("‘", "").replace("’", "").replace("'", "").replace("\"", "").replace("“", "").replace(
                "”", "").strip()
            return inner_punctuation_free

        if input_text is not None:
            return inner_punctuation_removal(inner_input_text=input_text)
        elif input_text is None:
            if self._tweet is not None:
                modified_text = inner_punctuation_removal(inner_input_text=self._tweet.get_tweet_text())
                if inplace:
                    self._tweet.set_tweet_text(modified_text)
                    return self._tweet
                else:
                    return modified_text
            elif self._tweet is None:
                return


########################################################################################################################


    def tweet_text_preprocessing(self, input_text=None, html_entities_parsing=True, url=True, case=True, punctuation=True, hashtag=2, mention=2,
                           whitespace=True, control_chars=True, control_chars_list=r'[\r\t\n]', substitute_char=" ",
                           stopword=True, stopword_corpus="stone", hashtag_split=True, mention_replacement=True, inplace=False):
        """
        This function preprocess the tweet text.
        :param input_text: if this parameter is None, then preprocessing is performed on the caller object text field,
        otherwise and in case of a string as an input for this parameter, the preprocessing is applied on the input text.
        :param html_entities_parsing: Setting this parameter converts all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) to the corresponding Unicode characters.
        :param url: by setting this boolean parameter True, the tweet urls are removed.
        :param case: setting this boolean parameter True, turns the tweet text to lower case.
        :param punctuation: by setting this boolean parameter True, the tweet punctuations are removed.
        :param hashtag: this integer parameter represents the hashtag removal mode. There are three modes for
        hashtags removal. In mode 1, the text remains intact, in Mode 2, only the hashtag characters (#) are removed,
        and in mode 3, the whole hashtags consisting the hashtag character and the terms after the hashtags are removed.
        :param mention: this integer parameter represents the mention removal mode. There are three modes for
        mention removal. In mode 1, the text remains intact, in Mode 2, only the mention characters (@) are removed,
        and in mode 3, the whole mention consisting the hashtag character and the terms after the hashtags are removed.
        :param whitespace: by setting this boolean parameter True, the tweet whitespaces are removed.
        :param control_chars: by setting this boolean parameter True, the common control characters (carriage return(\r),
        line feed(\n), and horizontal tab(\t)) are removed.
        :param control_chars_list: this parameter indicates the list of characters which will be removed.
        :param substitute_char: the control characters will be replaced by teh value of this parameter.
        :param stopword: when this parameter is set to True, the stopwords will be removed.
        :param stopword_corpus: this string parameter represents the stopwords corpus for stopword removal. The stopword corpus can
        be "stone", "nltk", "corenlp", or "glascow". Almost every text mining framework uses one of these corpuses for
        removing the stopwords. In order to seactivates stopwords removal, this parameter has to be set to False.
        :param hashtag_split: by setting this parameter to True, the hashtags are splitted and replaced in the text.
        :param mention_replacement: by setting this parameter to True, the mentions are replaced by their corresponding screen names.
        :return: when the implace parameter is equal to True, the function applies the preprocessing permanently and returns
        the whole object, in contrast when it is equal to False the function only returns the text field after preprocessing.
        """

        assert (url in [True, False]), "url parameter can be True or False"
        assert (case in [True, False]), "case parameter can be True or False"
        assert (punctuation in [True, False]), "punctuation parameter can be True or False"
        assert (hashtag in [1, 2, 3]), "hashtag parameter can be 1, 2, 3"
        assert (mention in [1, 2, 3]), "mention parameter can be 1, 2, 3"
        assert (whitespace in [True, False]), "whitespace parameter can be True or False"
        assert (control_chars in [True, False]), "control_characters parameter can be True or False"
        assert (stopword in [True, False]), "stopword parameter can be True or False"
        assert (stopword_corpus in ["stone", "nltk", "corenlp", "glascow"]), "stop parameter can be stone, nltk, corenlp, glascow, or False"
        assert (hashtag_split in [True, False]), "hashtag_split parameter can be True or False"
        assert (mention_replacement in [True, False]), "mention_replacement parameter can be True or False"

        if input_text is not None:
            text = input_text
            hashtag_obj = TweetHashtag()
            mention_obj = TweetMention()
            url_obj = TweetUrl()

            if html_entities_parsing:
                text = self.tweet_html_entities_parsing(input_text=text)
            #fill this part in, write functions that are independent of tweet object
            if url is True:
                text = url_obj.url_removal(input_text=text)
            # if mention_replacement is True:
            #     ###
            #     pass
            if hashtag_split is True:
                text = hashtag_obj.hashtag_splitter(input_text=text)
            if hashtag == 1:
                pass
            elif hashtag == 2:
                text = hashtag_obj.hashtags_removal(input_text=text, mode=2)
            elif hashtag == 3:
                text = hashtag_obj.hashtags_removal(input_text=text, mode=3)
            if mention == 1:
                pass
            elif mention == 2:
                text = mention_obj.mentions_removal(input_text=text, mode=2)
            elif mention == 3:
                text = mention_obj.mentions_removal(input_text=text, mode=3)
            if stopword is True:
                text = self.stopwords_removal(input_text=text, stopword_corpus=stopword_corpus)
            if punctuation is True:
                text = self.punctuation_removal(input_text=text)
            if control_chars is True:
                text = self.control_characters_removal(control_chars_list=control_chars_list,
                                                       substitute_char=substitute_char, input_text=text)
            if case is True:
                text = text.lower()
            if whitespace is True:
                text = self.whitespace_removal(input_text=text)
            return text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
                if html_entities_parsing:
                    text = self.tweet_html_entities_parsing()
                if url is True:
                    text = self._tweet.get_tweet_urls().url_removal()
                if mention_replacement is True:
                    text = self._tweet.get_tweet_mentions().mention_replacement()
                if hashtag_split is True:
                    text = self._tweet.get_tweet_hashtags().hashtag_splitter()
                if hashtag == 1:
                    pass
                elif hashtag == 2:
                    text = self._tweet.get_tweet_hashtags().hashtags_removal(mode=2)
                elif hashtag == 3:
                    text = self._tweet.get_tweet_hashtags().hashtags_removal(mode=3)
                if mention == 1:
                    pass
                elif mention == 2:
                    text = self._tweet.get_tweet_mentions().mentions_removal(mode=2)
                elif mention == 3:
                    text = self._tweet.get_tweet_mentions().mentions_removal(mode=3)
                if stopword is True:
                    text = self.stopwords_removal(stopword_corpus=stopword_corpus)
                if punctuation is True:
                    text = self.punctuation_removal()
                if control_chars is True:
                    text = self.control_characters_removal(control_chars_list=control_chars_list, substitute_char=substitute_char)
                if case is True:
                    text = text.lower()
                if whitespace is True:
                    text = self.whitespace_removal()
                if inplace:
                    self._tweet.set_tweet_text(text)
                    return self._tweet
                else:
                    return text
            elif self._tweet is None:
                return

    ########################################################################################################################



    def get_pos_tags(self):
        return self._pos_tags

    def tweet_pos(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding Part-of-Speech (POS) tag.
        :param input_text: if this parameter is None, then the Part-of-Speech (POS) tagging is performed on the caller object text field,
        otherwise and in case of a string as an input for this parameter, the Part-of-Speech tagging is performed on the input text.
        :return: this function returns the POS tagged version of the tweet.
        """

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        processed_text = self.tweet_text_preprocessing(input_text=text)

        pos_text_list = []
        spacy_text = self._nlp(processed_text)
        for token in spacy_text:
            pos_text_list.append(token.pos_)
        return pos_text_list

    def tweet_pos_count(self, input_text=None):

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        pos_text_list = self.tweet_pos(input_text=text)
        pos_tag_count = {p: 0 for p in self.get_pos_tags()}

        for pos_tag in pos_text_list:
            pos_tag_count[pos_tag] += 1
        return pos_tag_count

    def get_ner_tags(self):
        return self._ner_tags

    def tweet_ner(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding Named-Entity-Recognition (NER) tag.
        :param input_text: if this parameter is None, then the Named-Entity-Recognition (NER) tagging is performed on the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        NER tagging is performed on the input text.
        :return: this function returns the Named-Entity-Recognition (NER) tagged version of the tweet.
        """

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        processed_text = self.tweet_text_preprocessing(input_text=text)

        ner_text_list = []
        spacy_text = self._nlp(processed_text)
        for token in spacy_text.ents:
            ner_text_list.append(token.label_)

        return ner_text_list

    def tweet_ner_count(self, input_text=None):

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        ner_text_list = self.tweet_ner(input_text=text)
        ner_tag_count = {p: 0 for p in self.get_ner_tags()}

        for ner_tag in ner_text_list:
            ner_tag_count[ner_tag] += 1

        return ner_tag_count

    def tweet_lemmatization(self, input_text=None):
        """
        This function replaces every word in the tweet by its corresponding lemma.
        :param input_text: if this parameter is None, then the lemmatization is performed on the
        caller object text field, otherwise and in case of a string as an input for this parameter, the
        lemmatization is performed on the input text.
        :return: this function returns the lemmatized version of the tweet.
        """
        if input_text is None:
            text = self._tweet.get_tweet_text()
        else:
            text = input_text
        text = self.tweet_text_preprocessing(input_text=text)

        tweet_lemmas = ""
        spacy_text = self._nlp(text)
        for token in spacy_text:
            tweet_lemmas = tweet_lemmas + " " + token.lemma_

        return tweet_lemmas.strip()

    def text_complexity(self, input_text=None, complexity_unit="word"):
        """
        this function measures the complexity of a tweet text based on the selected complexity unit.
        :param input_text: if this parameter is None, then the complexity of caller object text field is measured, otherwise
        and in case of a string as an input for this parameter, the complexity of input text is measured.
        :param complexity_unit: the complexity unit can be "word", "sentence", or "syllables".
        :return: an float showing the complexity of the tweet text.
        """

        assert (complexity_unit in ["word", "sentence", "syllables"]), "unit parameter can be word, " \
                                                                       "sentence, or syllables"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        if complexity_unit == "word":
            return np.average([len(word) for word in self.tweet_splitter(split_unit="word", input_text=text)])
        elif complexity_unit == "sentence":
            return np.average([len(self.tweet_splitter(split_unit="word", input_text=sentence)) for sentence in
                               self.tweet_splitter(split_unit="sentence", input_text=text)])
        elif complexity_unit == "syllables":
            return np.average([textstat.syllable_count(i, lang='en_US') for i in self.tweet_splitter(split_unit="word", input_text=text)])

    def text_pronoun_count(self, input_text=None, pronoun="third_singular"):
        """
        This function counts the number of pronouns in the tweet text according to selected pronoun for counting.
        :param input_text: if this parameter is None, then the number of chosen pronoun in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of chosen pronoun in the
        input_text is counted.
        :param pronoun: the pronoun can be "first_singular", "first_plural", "second_singular", "second_plural", "third_singular", or
        "third_plural".
        :return: an integer showing the number of chosen pronoun in the tweet text.
        """

        assert (pronoun in ["first_singular", "first_plural", "second_singular", "second_plural", "third_singular",
                            "third_plural"]), "the pronoun parameter can be first_singular, first_plural, second_singular, second_plural, " \
                                              "third_singular, or third_plural"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        words = [i.lower() for i in self.tweet_splitter(split_unit="word", input_text=text)]
        if pronoun == "first_singular":
            return words.count("i") + words.count("my") + words.count("mine") + words.count("me") + words.count(
                "myself") + words.count("i'm") + words.count("i've") + words.count("i'd") + words.count("i'll")
        elif pronoun == "first_plural":
            return words.count("we") + words.count("our") + words.count("ours") + words.count("us") + words.count(
                "ourselves") + words.count("we're") + words.count("we've") + words.count("we'd") + words.count("we'll")
        elif pronoun == "second_singular":
            return words.count("you") + words.count("your") + words.count("yours") + words.count(
                "yourself") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
                "you'll")
        elif pronoun == "second_plural":
            return words.count("you") + words.count("your") + words.count("yours") + words.count(
                "yourselves") + words.count("you're") + words.count("you've") + words.count("you'd") + words.count(
                "you'll")
        elif pronoun == "third_singular":
            return words.count("he") + words.count("she") + words.count("it") + words.count("his") + words.count(
                "her") + words.count("its") + words.count("him") + words.count("hers") + words.count(
                "he's") + words.count("she's") + words.count("it's") + words.count("he'll") + words.count(
                "she'll") + words.count("it'll") + + words.count("he'd") + words.count("she'd") + words.count("it'd")
        elif pronoun == "third_plural":
            return words.count("they") + words.count("them") + words.count("their") + words.count(
                "theirs") + words.count("themselves") + words.count("they're") + words.count("they've") + words.count(
                "they'd") + words.count("they'll")

    def lowercase_count(self, input_text=None, unit_of_analysis="character"):
        """
         This function analyses the count and fraction of upper and lower letters or capital and small words in the tweet text
         depending on the selected unit of analysis.
         :param unit_of_analysis: the unit parameter can be character, word, or sentence.
         :param input_text: if this parameter is None, then the case analysis is performed on the caller object text field
         , otherwise and in case of a string as an input for this parameter, the case analysis is performed on the input_text.
         :return: it returns the number of lowercase characters or small words in the tweet depending on the selected unit of analysis.
         """

        assert (unit_of_analysis in ["character", "word", "sentence"]), "unit can be character or word"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        lower_count = 0
        if unit_of_analysis == "character":
            lower_count = sum(1 for i in text if i.islower())
        elif unit_of_analysis == "word":
            words = self.tweet_splitter(split_unit="word", input_text=text)
            lower_count = len([b for b in words if b.islower()])
        elif unit_of_analysis == "sentence":
            sentences = self.tweet_splitter(split_unit="sentence", input_text=text)
            for sentence in sentences:
                updated_sentence = self.whitespace_removal(input_text=sentence).replace(" ", "")
                if len(updated_sentence) == sum(1 for i in updated_sentence if i.islower()):
                    lower_count += 1
        return lower_count

    def uppercase_count(self, input_text=None, unit_of_analysis="character"):
        """
         This function analyses the count and fraction of upper and lower letters or capital and small words in the tweet text
         depending on the selected unit of analysis.
         :param unit_of_analysis: the unit parameter can be character, word, or sentence.
         :param input_text: if this parameter is None, then the case analysis is performed on the caller object text field
         , otherwise and in case of a string as an input for this parameter, the case analysis is performed on the input_text.
         :return: it returns the number of uppercase characters or capital words in the tweet depending on the selected unit of analysis.
         """

        assert (unit_of_analysis in ["character", "word", "sentence"]), "unit can be character or word"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        upper_count = 0
        if unit_of_analysis == "character":
            upper_count = sum(1 for i in text if i.isupper())
        elif unit_of_analysis == "word":
            words = self.tweet_splitter(split_unit="word", input_text=text)
            upper_count = len([b for b in words if b.isupper()])
        elif unit_of_analysis == "sentence":
            sentences = self.tweet_splitter(split_unit="sentence", input_text=text)
            for sentence in sentences:
                updated_sentence = self.whitespace_removal(input_text=sentence).replace(" ", "")
                if len(updated_sentence) == sum(1 for i in updated_sentence if i.isupper()):
                    upper_count += 1

        return upper_count

    def special_character_count(self, character="", input_text=None):
        """
        This function counts the number of occurrence of an indicated character in the tweet text field.
        :param input_text: if this parameter is None, then the number of exclamation mark in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of exclamation mark in the
         input_text is counted.
        :param character: this parameter specifies which character is counted by the function.
        :return: an integer showing the number of occurrence of an indicated character in the tweet text.
        """
        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        return text.count(character)

    def exclamation_mark_count(self, input_text=None):
        """
        This function counts the number of exclamation mark in  the tweet text field.
        :param input_text: if this parameter is None, then the number of exclamation mark in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of exclamation mark in the
         input_text is counted.
        :return: an integer showing the number of exclamation mark in the tweet text.
        """
        if input_text is not None:
            text = input_text
            return self.special_character_count(input_text=text, character="!")
        elif input_text is None:
            if self._tweet is not None:
                return self.special_character_count(character="!")
            elif self._tweet is None:
                return

    def question_mark_count(self, input_text=None):
        """
        This function counts the number of question marks in the tweet text field.
        :param input_text: if this parameter is None, then the number of question marks in the caller object text field
        is counted, otherwise and in case of a string as an input for this parameter, the number of question marks in the
         input_text is counted.
        :return: an integer showing the number of question marks in the tweet text.
        """
        if input_text is not None:
            text = input_text
            return self.special_character_count(input_text=text, character="?")
        elif input_text is None:
            if self._tweet is not None:
                return self.special_character_count(character="?")
            elif self._tweet is None:
                return

    def abbreviations(self, input_text=None):
        """
        This function finds the abbreviations used in tweet text.
        :param input_text: if this parameter is None, then the function finds the abbreviations used in the caller object text field
        , otherwise and in case of a string as an input for this parameter, the function finds the abbreviations in the
        input_text.
        :return: a list of abbreviations used in the tweet text.
        """
        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        words = self.tweet_splitter(split_unit="word", input_text=text)
        return [i for i in words if i in self._abbreviations_list]

    def vulgar_words(self, input_text=None):
        """
         This function finds the vulgar terms used in tweet text.
         :param input_text: if this parameter is None, then the function finds the vulgar terms used in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function finds the vulgar terms in the
         input_text.
         :return: a list of vulgar terms used in the tweet text.
         """
        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        words = self.tweet_splitter(split_unit="word", input_text=text)
        return [i for i in words if i.lower() in self._vulgar_words_list]

    def readability(self, readability_metric="flesch_reading_ease", input_text=None):
        """
        This function measures the readability of the tweet text according to the chosen readbility metric.
        :param readability_metric: the readability metrics can be "flesch_reading_ease", "flesch_kincaid_grade", "gunning_fog", "smog_index",
        "automated_readability_index", "coleman_liau_index", "linsear_write_formula", or "dale_chall_readability_score"
        :param input_text: if this parameter is None, then the function measures the readability of the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function measures the readability of the
         input_text.
        :return:
        """

        assert (readability_metric in ["flesch_reading_ease", "flesch_kincaid_grade", "gunning_fog", "smog_index", "automated_readability_index",
                           "coleman_liau_index", "linsear_write_formula",
                           "dale_chall_readability_score"]), "The metric " \
                                                             "has to be flesch_reading_ease, flesch_kincaid_grade, gunning_fog, smog_index, " \
                                                             "automated_readability_index, coleman_liau_index, linsear_write_formula," \
                                                             "or dale_chall_readability_score."

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        if readability_metric == "flesch_reading_ease":
            return textstat.flesch_reading_ease(text)
        elif readability_metric == "flesch_kincaid_grade":
            return textstat.flesch_kincaid_grade(text)
        elif readability_metric == "gunning_fog":
            return textstat.gunning_fog(text)
        elif readability_metric == "smog_index":
            return textstat.smog_index(text)
        elif readability_metric == "automated_readability_index":
            return textstat.automated_readability_index(text)
        elif readability_metric == "coleman_liau_index":
            return textstat.coleman_liau_index(text)
        elif readability_metric == "linsear_write_formula":
            return textstat.linsear_write_formula(text)
        elif readability_metric == "dale_chall_readability_score":
            return textstat.dale_chall_readability_score(text)

    def long_words_count(self, threshold=6, input_text=None):
        """
        This function counts the number of words that are longer than a particular threshold.
        :param threshold: an integer showing the threshold of long words.
        :param input_text: if this parameter is None, then the function counts the long words in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function counts the number of long words in the
         input_text.
        :return: an integer number showing the number of words which are longer than a particular threshold.
        """

        assert (isinstance(threshold, int) and threshold > 0), "threshold has to be a positive integer"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        words = self.tweet_splitter(split_unit="word", input_text=text)
        return len([i for i in words if len(i) > threshold])

    def multiple_syllables_count(self, threshold=2, input_text=None):
        """
        This function counts the number of words that their syllables number is more than a particular threshold.
        :param threshold: an integer showing the threshhold of syllables.
        :param input_text: if this parameter is None, then the function counts the number of syllables in the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function counts the number of syllables in the
         input_text.
        :return: an integer number showing the number of wordsthat that their syllables number is higher than a particular threshold.
        """

        assert (isinstance(threshold, int) and threshold > 0), "threshold has to be a positive integer"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        words = self.tweet_splitter(split_unit="word", input_text=text)
        return len([i for i in words if textstat.syllable_count(i, lang='en_US') > threshold])

    def text_length(self, input_text=None, length_unit="word"):
        """
        this function measures the length of the tweet based on the selected length unit.
        :param input_text: if this parameter is None, then the length of caller object text field is measured, otherwise
        and in case of a string as an input for this parameter, the length of input text is measured.
        :param length_unit: the length unit can be "character", "word", or "sentence".
        :return: an integer showing the length of the tweet text field.
        """

        assert (length_unit in ["character", "word", "sentence"]), "the unit can be character, word, or sentence"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        # This will replace the html entities with their corresponding unicode
        text = self.tweet_html_entities_parsing(input_text=text)


        ### When a tweet is a reply, it can exceeds 280 characters limit since the mentions of the recepeints will be added to the reply.
        ### It becomes even more complicated if the reply is retweeted because you cannot immediately recognise whther the tweet is a reply or not
        # if len(text) > 300:
        #     print()
        #
        # if len(text) > self._tweet_length_limit:
        #     if input_text is None and self._tweet is not None:
        #         if self._tweet.is_tweet_retweeted():
        #             retweet_obj = tweet.get_tweet_retweet_object()
        #             if retweet_obj.is_tweet_a_reply():
        #                 screen_name = retweet_obj.get_tweet_in_reply_to_screen_name()
        #                 text = text.replace("@"+screen_name, "")

        if length_unit == "character":
            return len(text)
        elif length_unit == "word":
            return len(self.tweet_splitter(split_unit="word", input_text=text))
        elif length_unit == "sentence":
            return len(self.tweet_splitter(split_unit="sentence", input_text=text))

    def get_vader_emotional_dimensions(self):
        return self._vader_emotions

    def get_vad_emotional_dimensions(self):
        return self._vad_dimensions

    def sentiment_analysis(self, sentiment_engine="vader", input_text=None):
        """
        This function performs sentiment analysis over tweet text field using various sentiment analysis engines
        :param sentiment_engine: sentiment_engine can be "textblob", "vader", "nrc", or "vad".
        :param input_text: if this parameter is None, then the function measure the sentiment of the caller object text field
         , otherwise and in case of a string as an input for this parameter, the function measures the sentiment of the
         input_text.
        :return: it returns a dictionary containing various sentiment scores depending on the chosen sentiment_engine. If
        it is textblob, the sentiment scores are polarity and subjectivity. If it vader, the scores are positivity, negativity,
        neutrality, and composite score. If the sentiment_engine is nrc, then the sentiment scores are anger, disgust, sadness,
        anticipation, fear, surprise, joy, and trust. If the hate_speech engine is chosen, the scores  woud be hate_speech,
        offensive language, and neither. And finally, if the sentiment engine is vad, the scores would be valence, arousal,
        and dominance.
        """

        assert (sentiment_engine in ["textblob", "vader", "nrc", "vad"]), \
            "the sentiment_engine has to be" "textblob, vader, nrc, or vad"

        if input_text is not None:
            text = input_text
        elif input_text is None:
            if self._tweet is not None:
                text = self._tweet.get_tweet_text()
            elif self._tweet is None:
                return

        if sentiment_engine == "textblob":
            return {"subjectivity": TextBlob(text).sentiment.subjectivity,
                    "polarity": TextBlob(text).sentiment.polarity}
        elif sentiment_engine == "vader":
            return {"positivity_score": self._vader_analyser.polarity_scores(text)["pos"],
                    "negativity_score": self._vader_analyser.polarity_scores(text)["neg"],
                    "neutrality_score": self._vader_analyser.polarity_scores(text)["neu"],
                    "composite_score": self._vader_analyser.polarity_scores(text)["compound"]}
        elif sentiment_engine == "nrc":
            nrc_text_list = [i.lower() for i in self.tweet_splitter(split_unit="word", input_text=text)]
            anger_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    anger_score += self._nrc_corpus[term]["anger"]
            anticipation_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    anticipation_score += self._nrc_corpus[term]["anticipation"]
            disgust_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    disgust_score += self._nrc_corpus[term]["disgust"]
            fear_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    fear_score += self._nrc_corpus[term]["fear"]
            joy_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    joy_score += self._nrc_corpus[term]["joy"]
            sadness_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    sadness_score += self._nrc_corpus[term]["sadness"]
            surprise_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    surprise_score += self._nrc_corpus[term]["surprise"]
            trust_score = 0
            for term in nrc_text_list:
                if term in self._nrc_corpus:
                    trust_score += self._nrc_corpus[term]["trust"]
            return {"anger_score": anger_score, "anticipation_score": anticipation_score,
                    "disgust_score": disgust_score, "fear_score": fear_score, "joy_score": joy_score,
                    "sadness_score": sadness_score, "surprise_score": surprise_score, "trust_score": trust_score}
        elif sentiment_engine == "vad":
            word_list = [i.lower() for i in self.tweet_splitter(split_unit="word", input_text=text)]

            valence_score = 0
            for term in word_list:
                if term in self._vad_dic:
                    valence_score += self._vad_dic[term]["valence"]

            arousal_score = 0
            for term in word_list:
                if term in self._vad_dic:
                    arousal_score += self._vad_dic[term]["arousal"]

            dominance_score = 0
            for term in word_list:
                if term in self._vad_dic:
                    dominance_score += self._vad_dic[term]["dominance"]

            return {"valence_score": valence_score, "arousal_score": arousal_score, "dominance_score": dominance_score}