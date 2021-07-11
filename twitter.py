import json
import tweepy


class Tweet:
    def __init__(self, tweet_id, user_id, text, image_id=None):
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.text = text
        self.image_id = image_id


class TwitterAPI:
    def _connect_to_twitter_api(self):
        pass

    def fetch_old_tweets(self, user_id):
        pass

    def fetch_new_tweets(self, user_id, last_tweet_id):
        pass


class Tweepy(TwitterAPI):
    def __init__(self):
        self._search_count = 200
        self._connect_to_twitter_api()

    def _connect_to_twitter_api(self):
        with open('secrets.json') as secret_file:
            secrets = json.load(secret_file)

        consumer_key = secrets['consumer_key']
        consumer_secret = secrets['consumer_secret']

        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        try:
            redirect_url = self._auth.get_authorization_url()
        except tweepy.TweepError:
            print('Error! Failed to get request token.')

        self._api = tweepy.API(self._auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        try:
            self._api.verify_credentials()
            print('Authenticated to Twitter API')
        except tweepy.TweepError:
            print("Could not authenticate to Twitter API")

    def get_user_id_from_user_name(self, user_name):
        user = self._api.get_user(screen_name=user_name)
        return user.id_str

    def get_user_name_from_user_id(self, user_id_):
        user = self._api.get_user(user_id=user_id_)
        return user.screen_name

    def fetch_old_tweets(self, user_id):
        tweet_dict = {}
        last_tweet = self._api.user_timeline(user_id=user_id, include_rts=False, count=1)[0]
        last_tweet_id = last_tweet.id
        while True:
            tweets = self._api.user_timeline(user_id=user_id, max_id=last_tweet_id, include_rts=False, count=self._search_count)
            for tweet in tweets:
                tweet_dict[tweet.id_str] = {'text': tweet.text, 'user_id': tweet.user.id_str}
            if len(tweets) <= 1:
                break
            last_tweet_id = tweets[-1].id

        # return tuple
        return tweet_dict, last_tweet.id_str

    def fetch_new_tweets(self, user_id, last_tweet_id):
        tweet_dict = {}
        while True:
            tweets = self._api.user_timeline(user_id=user_id, since_id=last_tweet_id, include_rts=False, count=self._search_count)
            for tweet in tweets:
                tweet_dict[tweet.id_str] = {'text': tweet.text, 'user_id': tweet.user.id_str}
            if len(tweets) <= 1:
                break
            last_tweet_id = tweets[-1].id

        # return tuple
        return tweet_dict, last_tweet_id

