import json
from twitter import Tweet
import os


class UserRepo:
    def add_user(self, user_data):
        pass

    def get_user_and_last_tweet_id(self, user_id):
        pass

    def user_exists(self, user_id):
        pass


class UserRepoFile(UserRepo):
    def __init__(self):
        self._file_name = 'users.json'

    def add_user(self, user_id, last_tweet_id=None):
        with open(self._file_name, "r+", encoding='utf8') as file:
            file_data = json.load(file)
            file_data[user_id] = last_tweet_id
            # set offset position to point to the beginning of the file
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)
            return {user_id: last_tweet_id}

    def update_user(self, user_id, last_tweet_id):
        self.add_user(user_id, last_tweet_id)

    def delete_user(self, user_id):
        with open(self._file_name, "r", encoding='utf8') as file:
            file_data = json.load(file)
        removed_value = file_data.pop(user_id)
        with open(self._file_name, "w", encoding='utf8') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)
        return {user_id: removed_value}

    def get_user_and_last_tweet_id(self, user_id):
        with open(self._file_name, "r", encoding='utf8') as file:
            file_data = json.load(file)
            return {file_data: file_data[user_id]}

    def user_exists(self, user_id):
        with open(self._file_name, "r", encoding='utf8') as file:
            file_data = json.load(file)
            return user_id in file_data.keys()

    def get_all_users_and_last_tweet_ids(self):
        with open(self._file_name, "r", encoding='utf8') as file:
            file_data = json.load(file)
            return file_data


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

    def delete_tweets(self, user_name):
        file_name = 'tweets/' + user_name + '.json'
        file_name_deleted = 'tweets_deleted/' + user_name + '.json'
        try:
            os.rename(file_name, file_name_deleted)
            # os.remove(file_name)
        except OSError as e:
            print(e.strerror)



