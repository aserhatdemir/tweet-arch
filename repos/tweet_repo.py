import json
from twitter import Tweet
import os


class TweetRepo:
    def save_tweet(self, tweet: Tweet):
        pass

    def save_tweet_dict(self, user_name, tweet_dict):
        pass

    def get_tweet(self, tweet_id):
        pass


class TweetRepoFile(TweetRepo):
    def save_tweet(self, tweet: Tweet):
        # file_name = Tweet.user_id + '.json'
        # with open(file_name, "w", encoding='utf8') as outfile:
        #     json.dump(tweet_dict_, outfile, indent=4, ensure_ascii=False)
        pass

    def save_tweet_dict(self, user_id, tweet_dict):
        file_name = 'tweets/' + user_id + '.json'
        with open(file_name, "w", encoding='utf8') as file:
            json.dump(tweet_dict, file, indent=4, ensure_ascii=False)

    def update_tweet_dict(self, user_name, tweet_dict):
        file_name = 'tweets/' + user_name + '.json'
        with open(file_name, "r+", encoding='utf8') as file:
            file_data = json.load(file)
            file_data.update(tweet_dict)  # merge the dictionaries
            # set offset position to point to the beginning of the file
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)

    def get_tweet(self, tweet_id):
        pass

    def delete_tweets(self, user_id):
        file_name = 'tweets/' + user_id + '.json'
        file_name_deleted = 'tweets_deleted/' + user_id + '.json'
        try:
            os.rename(file_name, file_name_deleted)
            # os.remove(file_name)
        except OSError as e:
            print(file_name)
            print(file_name_deleted)
            print(e.strerror)

