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

# C.
conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()

createUserTbl = '''
CREATE TABLE user(
    id NUMBER(16),
    name VARCHAR2(25),
    screen_name VARCHAR2(25),
    description VARCHAR2(30),
    friends_count NUMBER(5),

    CONSTRAINT User_PK
        PRIMARY KEY (id)
)
'''
createTweetsTbl = """
CREATE TABLE Tweets
(
    created_at VARCHAR2(30),
    id_str VARCHAR2(30) PRIMARY KEY,
    text VARCHAR2(140),
    source VARCHAR2(60),
    in_reply_to_user_id VARCHAR2(30),
    in_reply_to_screen_name VARCHAR2(30),
    in_reply_to_status_id NUMBER(18),
    retweet_count NUMBER(8),
    contributors VARCHAR2(30),
    user_id NUMBER(16),

    CONSTRAINT Tweet_FK
        FOREIGN KEY (user_id)
            REFERENCES user(id)
);
"""
createGeoTbl = """
CREATE TABLE Geo(
    id_str VARCHAR2(30),
    type VARCHAR2(25),
    longitude NUMBER,
    latitude NUMBER,

    CONSTRAINT Geo_PK
        PRIMARY KEY (id_str),

    CONSTRAINT Geo_FK
        FOREIGN KEY (id_str)
            REFERENCES Tweets(id_str)
);"""

cursor.execute(createUserTbl)
cursor.execute(createTweetsTbl)
cursor.execute(createGeoTbl)

cursor.execute('DROP TABLE tweets;')
cursor.execute('DROP TABLE user;')
cursor.execute('DROP TABLE Geo;')
conn.commit()
conn.close()

tweets = []
start = time.time()
with urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt') as t:
    for i in range(500_000):
        tweet = t.readline()
        try:
            print(i)
            tweets.append(json.loads(tweet.decode('utf8')))
        except:
            pass

insertTweets = 'INSERT INTO Tweets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
insertUser = 'INSERT INTO User VALUES(?, ?, ?, ?, ?);'
insertGeo = 'INSERT INTO Geo VALUES(?, ?, ?, ?);'
insertErrors = []

for idx, i in enumerate(tweets):
    one = i['created_at']
    two = i['id_str']
    three = i['text']
    four = i['source']
    five = i['in_reply_to_user_id']
    six = i['in_reply_to_screen_name']
    seven = i['in_reply_to_status_id']
    eight = i['retweet_count']
    nine = i['contributors']
    ten = i['user']['id']
    if i['geo'] != None:
        eleven, sixteen = i['geo']['coordinates']
        seventeen = i['geo']['type']
    else:
        eleven, sixteen, seventeen = (None, None, None)
    twelve = i['user']['name']
    thirteen = i['user']['screen_name']
    fourteen = i['user']['description']
    fifteen = i['user']['friends_count']
    values = [one, two, three, four, five, six, seven, eight, nine, ten]
    values2 = [ten, twelve, thirteen, fourteen, fifteen]
    values3 = [two, seventeen, eleven, sixteen]
    try:
        cursor.execute(insertTweets, values)  # Tweets table
    except:
        pass
    try:
        cursor.execute(insertUser, values2)  # User table
    except:
        pass
    try:
        if i['geo'] != None:
            cursor.execute(insertGeo, values3)  # Geo table
    except:
        pass
    print(idx)

end = time.time()
print(end - start)

# 25.712281227111816 seconds for 50,000 tweets; 49,973 Tweets, 48,371 User, 1,121 Geo
# 38.08688259124756 seconds for 100,000 tweets; 99,946 Tweets, 95,103 User, 2,253 Geo
# 172.37015652656555 seconds for 500,000 tweets; 499,776 Tweets, 447,304 User, 11,983 Geo

print(cursor.execute('SELECT count(*) FROM Tweets;').fetchone())
print(cursor.execute('SELECT count(*) FROM User;').fetchone())
print(cursor.execute('SELECT count(*) FROM Geo;').fetchone())

# D.
start = time.time()
tweets = []
with open('final_tweets.txt', 'r') as f:
    for tweet in f:
        try:
            tweets.append(json.loads(tweet))
        except:
            pass

for i in tweets[:50000]:
    one = i['created_at']
    two = i['id_str']
    three = i['text']
    four = i['source']
    five = i['in_reply_to_user_id']
    six = i['in_reply_to_screen_name']
    seven = i['in_reply_to_status_id']
    eight = i['retweet_count']
    nine = i['contributors']
    ten = i['user']['id']
    if i['geo'] != None:
        eleven, sixteen = i['geo']['coordinates']
        seventeen = i['geo']['type']
    else:
        eleven, sixteen, seventeen = (None, None, None)
    twelve = i['user']['name']
    thirteen = i['user']['screen_name']
    fourteen = i['user']['description']
    fifteen = i['user']['friends_count']
    values = [one, two, three, four, five, six, seven, eight, nine, ten]
    values2 = [ten, twelve, thirteen, fourteen, fifteen]
    values3 = [two, seventeen, eleven, sixteen]
    try:
        cursor.execute(insertTweets, values)  # Tweets table
    except:
        pass
    try:
        cursor.execute(insertUser, values2)  # User table
    except:
        pass
    try:
        if i['geo'] != None:
            cursor.execute(insertGeo, values3)  # Geo table
    except:
        pass

end = time.time()
print(end - start)

# 16.035093069076538 seconds for 50,000 tweets; 49,977 Tweets, 47,881 User, 1,305 Geo
# 17.02628779411316 seconds for 100,000 tweets; 99,947 Tweets, 94,045 User, 2,679 Geo
# 17.29100012779236 seconds for 207,543 tweets; 207,447 Tweets, 191,001 User, 5,829 Geo

print(cursor.execute('SELECT count(*) FROM Tweets;').fetchone())
print(cursor.execute('SELECT count(*) FROM User;').fetchone())
print(cursor.execute('SELECT count(*) FROM Geo;').fetchone())

# E.
begin = time.time()
tweets = []
errors = []
with open('final_tweets.txt', 'r') as f:
    for tweet in f:
        try:
            tweets.append(json.loads(tweet))
        except:
            pass

last = len(tweets)
remain = last % 1000
iter = 100 #last // 1000

count = 0
start = 0
end = 1000
values = []
values2 = []
values3 = []
while count <= iter:
    for i in tweets[start:end]:
        one = i['created_at']
        two = i['id_str']
        three = i['text']
        four = i['source']
        five = i['in_reply_to_user_id']
        six = i['in_reply_to_screen_name']
        seven = i['in_reply_to_status_id']
        eight = i['retweet_count']
        nine = i['contributors']
        ten = i['user']['id']
        if i['geo'] != None:
            eleven, sixteen = i['geo']['coordinates']
            seventeen = i['geo']['type']
        else:
            eleven, sixteen, seventeen = (None, None, None)
        twelve = i['user']['name']
        thirteen = i['user']['screen_name']
        fourteen = i['user']['description']
        fifteen = i['user']['friends_count']
        values.append([one, two, three, four, five, six, seven, eight, nine, ten])
        values2.append([ten, twelve, thirteen, fourteen, fifteen])
        values3.append([two, seventeen, eleven, sixteen])
    try:
        cursor.executemany(insertTweets, values)  # Tweets table
    except Exception as E:
        errors.append([E, i])
    try:
        cursor.executemany(insertUser, values2)  # User table
    except Exception as E:
        errors.append([E, i])
    try:
        if i['geo'] != None:
            cursor.executemany(insertGeo, values3)  # Geo table
    except Exception as E:
        errors.append([E, i])
    count += 1
    if count < iter:
        start += 1000
        end += 1000
    else:
        start = last - remain
        end = last
    values = []
    values2 = []
    values3 = []

stop = time.time()
print(stop - begin)
print(cursor.execute('SELECT count(*) FROM Tweets;').fetchone())
print(cursor.execute('SELECT count(*) FROM User;').fetchone())
print(cursor.execute('SELECT count(*) FROM Geo;').fetchone())

# 15.444014549255371 seconds for 50,000 tweets in file; 37,506 Tweets, 6,795 User, 1,000 Geo
# 16.265013694763184 seconds for 100,000 tweets in file; 76,723 Tweets, 11,489 User, 2,143 Geo
# 19.389507293701172 seconds for 207,543 tweets in file; 165,615 Tweets, 19,100 User, 2,769 Geo

# F.
# Plot for 1. A.
# 17.754178762435913 seconds for 50,000 tweets
# 32.30730128288269 seconds for 100,000 tweets
# 143.31574988365173 seconds for 500,000 tweets

plt.bar(x=['50,000', '100,000', '500,000'], height=[17.75, 32.31, 143.32], color='#5e79ff')
plt.xlabel('Tweets Loaded')
plt.ylabel('Seconds Elapsed')
plt.title('1. A. Plot')

# Plot for 1. C.
# 25.712281227111816 seconds for 50,000 tweets
# 38.08688259124756 seconds for 100,000 tweets
# 172.37015652656555 seconds for 500,000 tweets

plt.bar(x=['50,000', '100,000', '500,000'], height=[25.71, 38.1, 172.4], color='#5e79ff')
plt.xlabel('Tweets Loaded')
plt.ylabel('Seconds Elapsed')
plt.title('1. C. Plot')

# Plot for 1. D.
# 16.035093069076538 seconds for 50,000 tweets
# 17.02628779411316 seconds for 100,000 tweets
# 17.29100012779236 seconds for 207,543 tweets

plt.bar(x=['50,000', '100,000', '207,543'], height=[16.04, 17.03, 17.29], color='#5e79ff')
plt.xlabel('Tweets Loaded')
plt.ylabel('Seconds Elapsed')
plt.title('1. D. Plot')

# Plot for 1. E.
# 15.444014549255371 seconds for 50,000 tweets in file; 37,506 Tweets, 6,795 User, 1,000 Geo
# 16.265013694763184 seconds for 100,000 tweets in file; 76,723 Tweets, 11,489 User, 2,143 Geo
# 19.389507293701172 seconds for 207,543 tweets in file; 165,615 Tweets, 19,100 User, 2,769 Geo

plt.bar(x=['50,000', '100,000', '207,543'], height=[15.44, 16.27, 19.39], color='#5e79ff')
plt.xlabel('Tweets Loaded')
plt.ylabel('Seconds Elapsed')
plt.title('1. E. Plot')