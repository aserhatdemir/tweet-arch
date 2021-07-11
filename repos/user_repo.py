import json


class User:
    def __init__(self, user_id, last_tweet_id):
        self.user_id = user_id
        self.last_tweet_id = last_tweet_id


class UserRepo:
    def add_user(self, user_data):
        pass

    def get_user_and_last_tweet_id(self, user_id):
        pass

    def user_exists(self, user_id):
        pass


class UserRepoFile(UserRepo):
    def __init__(self):
        self._file_name = './users.json'

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
