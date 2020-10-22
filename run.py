import praw
import configparser
import pickledb
from time import sleep


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
reddit_target_subreddit = config['REDDIT']['reddit_target_subreddit']
max_posts = int(config['OPTIONS']['max_posts'])
sleep_timer = int(config['OPTIONS']['sleep_timer'])

db = pickledb.load('data.db', False)

reddit = praw.Reddit(
    username=reddit_user,
    password=reddit_pass,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='Reddit Saved Image Poster (by u/impshum)'
)


def main():
    for i, post in enumerate(reddit.user.me().saved(limit=None)):
        name = post.name
        if name[:2] == 't3' and post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            if not db.exists(name):
                reddit.subreddit(reddit_target_subreddit).submit(title=post.title, url=post.url)
                post.unsave()
                db.set(name, 1)
                db.dump()
                print(post.title)
                if i == max_posts - 1:
                    return
                sleep(sleep_timer)


if __name__ == '__main__':
    main()
