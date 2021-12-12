import math
import json
import requests
import itertools
import numpy as np
import time
from datetime import datetime, timedelta
import praw
import pandas as pd
## Almost all of this code was taken from Pj's tutorial on how to scrape reddit data
## using the pushshift API: https://medium.com/@pasdan/how-to-scrap-reddit-using-pushshift-io-via-python-a3ebcc9b83f4
## as well as his associated Jupyter notebook: https://github.com/slaps-lab/bibliotheca/blob/master/networks/scrapping_reddit_data.ipynb
## we used the code snippets and compiled them together to create a data collection program that
## fits our specific use case. We are in no way claiming ownership of this data collection program.

# basically find what percent needs to be positive to win the game


#configuration for reddit API using our user information
config = {
    "username" : "FlyNavy2022",
    "client_id" : "IJeutosyv7jQFIqlykv_rQ",
    "client_secret" : "yliLHJrnWsR5A_2akgwGKvKzW6FLVg",
    "user_agent" : "Big Truss NFL NLP project by /u/GoNavy2022"
}
reddit = praw.Reddit(client_id = config['client_id'], \
                     client_secret = config['client_secret'], \
                     user_agent = config['user_agent'])

#date of game you wish to search the preceeding week for
game_end = '2020-10-26 00:00:00.00'
game_end_obj = datetime.strptime(game_end, '%Y-%m-%d %H:%M:%S.%f') #the end of the time period you wish to search

def main():


    subreddit = 'Bengals'      #insert team subreddit you wish to search here
    posts = []


    offset = (game_end_obj - timedelta(days=6)).timestamp() #how many days prior you wish to search
    start_at = math.floor(offset)

    for interval in give_me_intervals(start_at, 5):

        pulled_posts = pull_posts_for(
            subreddit,
            interval[0],
            interval[1]
        )

        posts.extend(pulled_posts)

        print(f'collected #{len(pulled_posts)} for {interval[0]} - {interval[1]})')
        time.sleep(1)

    with open('pushshift_posts.json', 'w') as pushshift_posts:
        pushshift_posts.write(json.dumps(posts))
    with open('pushshift_posts.json', 'r') as pushshift_json:
        posts = json.loads(pushshift_json.read())




    reddit_data = []

    submission_count = 0
    total_submission_count = len(posts)

    submission_ids = np.unique([ post['id'] for post in posts ])
    for submission_id in submission_ids:
        submission = reddit.submission(id=submission_id)
        submission_author = submission.author
        if submission_author != None:
            submission_author = submission.author.name
        else:
            submission_author = 'deleted'

        reddit_data.append({
            'text': submission.selftext,
        })

        submission.comments.replace_more(limit=None)
        for comment in submission.comments:

            comment_author = comment.author
            if comment_author != None:
                comment_author = comment.author.name
            else:
                comment_author = 'deleted'

            #only pulling text to ease cleaning
            reddit_data.append({
                'text': comment.body,
            })
            print("running" + str(submission_count)) #error checking line
        submission_count += 1

        if submission_count % 500 == 0:
            print(submission_count, total_submission_count)

    print(f'len: {len(reddit_data)}')

    with open('dataset.json', 'w') as reddit_data_output:
        reddit_data_output.write(json.dumps(reddit_data))



    df = pd.read_json (r'dataset.json')
    df.to_csv('Bengals8_2020.txt', index=False)




###helper function to pull from Pushshift.io, these are unchanged from our cited source ####
def get_json(url):
    response = requests.get(url)
    assert response.status_code == 200

    return json.loads(response.content)

#makes requests from uri and handles HTTP
def make_request(uri, max_retries = 5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)
    current_tries = 1
    while current_tries < max_retries:
        try:
            time.sleep(1)
            response = fire_away(uri)
            return response
        except:
            time.sleep(1)
            current_tries += 1
    return fire_away(uri)

#take in 500 posts and see if more exist
def pull_posts_for(subreddit, start_at, end_at):

    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'prefix': 't4_'
        }, posts))

    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'

    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                subreddit, start_at, end_at, SIZE))['data'])
    n = len(post_collections)
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)

        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format( \
                    subreddit, new_start_at, end_at, SIZE))['data'])

        n = len(more_posts)
        post_collections.extend(more_posts)
    return post_collections

#method for building time period intervals for data scraping
def give_me_intervals(start_at, number_of_days_per_interval = 3):


    end_at = math.ceil(game_end_obj.timestamp() )

    ## 1 day = 86400,
    period = (86400 * number_of_days_per_interval)
    end = start_at + period
    yield (int(start_at), int(end))
    padding = 1
    while end <= end_at:
        start_at = end + padding
        end = (start_at - padding) + period
        yield int(start_at), int(end)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("---%s seconds ___" % (time.time() - start_time))
