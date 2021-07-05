from flask import Flask, abort
from apscheduler.schedulers.background import BackgroundScheduler

from twitter import Tweepy
from repos import TweetRepoFile
from repos import UserRepoFile

app = Flask(__name__)

my_twitter = Tweepy()
tweet_repo = TweetRepoFile()
user_repo = UserRepoFile()


@app.route('/')
def manual():
    man = """
        GET / -> read manual
        GET /user/<user_name> -> add user for recording
        DELETE /user/<user_name> -> delete user and its tweets
    """
    return man


@app.route('/user/<user_name>', methods=['GET'])
def add_user(user_name):
    user_id = my_twitter.get_user_id_from_user_name(user_name)
    if user_repo.user_exists(user_id):
        return 'User already exists, doing nothing!'
    tweet_dict, last_tweet_id = my_twitter.fetch_old_tweets(user_id)
    tweet_repo.save_tweet_dict(user_id, tweet_dict)
    result = user_repo.add_user(user_id, last_tweet_id)
    if result:
        return result
    abort(404)


@app.route('/user/<user_name>', methods=['DELETE'])
def delete_user(user_name):
    user_id = my_twitter.get_user_id_from_user_name(user_name)
    if not user_repo.user_exists(user_id):
        return 'User does not exist, doing nothing!'
    result = user_repo.delete_user(user_id)
    tweet_repo.delete_tweets(user_name)
    if result:
        return result
    abort(404)


def sensor():
    scheduler.print_jobs()


def fetch_new_tweets():
    scheduler.print_jobs()
    user_dict = user_repo.get_all_users_and_last_tweet_ids()
    for user_id in user_dict:
        last_tweet_id = user_dict[user_id]
        new_tweet_dict, new_last_tweet_id = my_twitter.fetch_new_tweets(user_id, last_tweet_id)
        tweet_repo.update_tweet_dict(user_id, new_tweet_dict)
        user_repo.update_user(user_id, new_last_tweet_id)


# APScheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(fetch_new_tweets, 'cron', minute='*')
scheduler.start()


if __name__ == '__main__':
    app.run()