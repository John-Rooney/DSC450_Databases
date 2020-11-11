import urllib.request
import json
import sqlite3
import time
import re

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

raw = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt')
tweets = []
error = []
for line in raw.readlines():
    try:
        tweets.append(json.loads(line.decode('utf8')))
    except:
        error.append(line)

# file = open('Module7_error.txt', 'w')
# for i in error:
#     file.write(str(i))
# file.close()

insertTweets = 'INSERT INTO Tweets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
insertUser = 'INSERT INTO User VALUES(?, ?, ?, ?, ?);'
insertGeo = 'INSERT INTO Geo VALUES(?, ?, ?, ?);'
insertErrors = []

for i in tweets:
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
    if i['geo'] == None:
        eleven, sixteen, seventeen = (None, None, None)
    else:
        eleven, sixteen = i['geo']['coordinates']
        seventeen = i['geo']['type']
    twelve = i['user']['name']
    thirteen = i['user']['screen_name']
    fourteen = i['user']['description']
    fifteen = i['user']['friends_count']
    values = [one, two, three, four, five, six, seven, eight, nine, ten]
    values2 = [ten, twelve, thirteen, fourteen, fifteen]
    values3 = [two, seventeen, eleven, sixteen]
    try:
        cursor.execute(insertTweets, values)  # Tweets table
    except Exception as E:
        insertErrors.append([i, E])
    try:
        cursor.execute(insertUser, values2)  # User table
    except Exception as E:
        insertErrors.append([i, E])
    try:
        cursor.execute(insertGeo, values3)  # User table
    except Exception as E:
        insertErrors.append([i, E])

# print(cursor.execute('SELECT COUNT(*) FROM User;').fetchone())
# print(cursor.execute('SELECT COUNT(*) FROM Tweets;').fetchone())
# print(cursor.execute('SELECT COUNT(*) FROM Geo;').fetchone())

# Part 1
# A.
s = time.time()
result = cursor.execute('SELECT * FROM Tweets WHERE id_str LIKE "%777%" OR id_str LIKE "%88%";').fetchall()
e = time.time()
# time = 0.013 Seconds, 1751 tweets

# B.
s = time.time()
raw = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt')
result = []
re1 = re.compile(r'777')
re2 = re.compile(r'88')
for line in raw.readlines():
    try:
        tweet = json.loads(line.decode('utf8'))
        if re1.search(tweet['id_str']) or re2.search(tweet['id_str']):
            result.append(line)
    except:
        continue
e = time.time()
# time = 3.61 seconds, 1751 tweets

# C.
s = time.time()
result = cursor.execute('SELECT COUNT(DISTINCT in_reply_to_user_id) FROM Tweets;').fetchall()
e = time.time()
# 0.007 seconds, Count = 1746

# D.
