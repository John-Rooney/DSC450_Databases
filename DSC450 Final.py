import urllib.request
import json
import sqlite3
import time
import re
import matplotlib.pyplot as plt
import pandas as pd

### Part 1 ###
# A.
numTweets = [50_000, 100_000, 500_000]
for num in numTweets:
    start=time.time()
    with urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt') as t:
        with open('final_tweets.txt', 'w') as f:
            for i in range(num):
                try:
                    tweet = t.readline()
                    f.write(tweet.decode('utf-8'))
                except:
                    continue
    end = time.time()
    print(end-start, num)
# 17.754178762435913 seconds for 50,000 tweets
# 32.30730128288269 seconds for 100,000 tweets
# 143.31574988365173 seconds for 500,000 tweets

# B.
tweets=[]
with open('final_tweets.txt', 'r') as f:
    for line in f.readlines():
        tweets.append(json.loads(line))

cols = ['created_at', 'id_str', 'text', 'source', 'in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'contributors']
colLen = [0, 0, 0, 0, 0, 0, 0, 0]

# User
cols2 = ['name', 'screen_name', 'description']
colLen2 = [0, 0, 0]

# geo
colLen3 = 0

for tweet in tweets:
    for idx, col in enumerate(cols):
        if tweet[col] != None:
            if len(str(tweet[col])) > colLen[idx]:
                colLen[idx] = len(str(tweet[col]))

    for idx, col in enumerate(cols2):
        if tweet['user'][col] != None:
            if len(str(tweet['user'][col])) > colLen2[idx]:
                colLen2[idx] = len(str(tweet['user'][col]))

    if tweet['geo'] != None:
        if len(str(tweet['geo']['type'])) > colLen3:
            colLen3 = len(str(tweet['geo']['type']))

# ([30, 18, 434, 173, 10, 15, 18, 0], [20, 15, 160], 5)
# Max Data Type Length
# ['created_at', 'id_str', 'text', 'source', 'in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'contributors']
# tweets: [30, 18, 434, 173, 10, 15, 0]
# schema: [30, 30, 140, 60, 30, 30, 30]

# ['user']
# ['name', 'screen_name', 'description']
# [20, 15, 160]
# [25, 25, 30]

# ['geo']['type']
# tweets 5
# schema 25
