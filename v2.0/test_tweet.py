from tweet import Tweet
import pytest
from file_collection import FileCollection


@pytest.fixture
def tweet_objects(test_folder_path):
    fc = FileCollection()
    fc.collect_json(test_folder_path)
    json_paths = fc.get_all_json()
    tweet_objects = {}
    for path in json_paths:
        tweet_objects[path.name] = (Tweet(path), path)

    return tweet_objects


def test_get_tweet_creation_time(tweet_objects):
    creation_times = {
        file_name1: ,
        file_name2:
    }
    for tweet in tweet_objects:
        assert tweet_objects[tweet] == tweet_objects[tweet].get_tweet_creation_time()

def test_get_tweet_id():
    pass

def test_get_tweet_text():
    pass

def test_get_tweet_client():
    pass

def test_is_tweet_truncated():
    pass

def test_is_tweet_a_reply():
    pass

def test_get_reply_to_id():
    pass

def test_get_tweet_in_reply_to_screen_name():
    pass

def test_get_tweet_user():
    pass

def test_get_tweet_location():
    pass

def test_get_tweet_quote_id():
    pass

def test_is_tweet_quoted():
    pass

def test_is_quote_object_available():
    pass

def test_get_tweet_quote_object():
    pass

def test_is_tweet_retweeted():
    pass

def test_get_tweet_retweet_object():
    pass

def test_get_tweet_quote_count():
    pass

def test_get_tweet_reply_count():
    pass

def test_get_tweet_likes_count():
    pass

def test_get_tweet_retweets_count():
    pass

def test_get_tweet_hashtags():
    pass

def test_get_tweet_mentions():
    pass

def test_get_tweet_urls():
    pass

def test_get_tweet_photos():
    pass

def test_get_tweet_video():
    pass

def test_get_tweet_gif():
    pass

def test_get_tweet_entities():
    pass

def test_get_tweet_language():
    pass

def test_get_tweet_matching_rules():
    pass

def test_get_tweet_current_user_retweet():
    pass

def test_get_tweet_scopes():
    pass

def test_get_tweet_withheld_copyright():
    pass

def test_get_tweet_withheld_in_countries():
    pass

def test_get_tweet_withheld_scope():
    pass

def test_get_tweet_object():
    pass

def test_get_tweet_url():
    pass

def test_set_tweet_text():
    pass
