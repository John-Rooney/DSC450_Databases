import numpy as np
import pandas as pd

### Part 1 ###

def randx(x): # 1. A
    return np.random.uniform(low=21, high=100, size=x)

lst = pd.Series(randx(50)) # 1. B
lst[lst < 33].shape

arr = np.array(lst).reshape(5, 10)
arr = np.where(arr > 50, 50, arr) # 1. C

### Part 2 ###
import urllib.request
import json
import sqlite3

conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE tweets;')
cursor.execute('DROP TABLE user;')
conn.commit()
conn.close()

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
cursor.execute(createUserTbl)
cursor.execute(createTweetsTbl)

cursor.execute('SELECT * FROM user;')

raw = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt')
tweets = []
error = []
for line in raw.readlines():
    try:
        tweets.append(json.loads(line.decode('utf8')))
    except:
        error.append(line)

file = open('Module7_error.txt', 'w')
for i in error:
    file.write(str(i))
file.close()

insert = 'INSERT INTO Tweets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
insert2 = 'INSERT INTO User VALUES(?, ?, ?, ?, ?);'
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
    # eleven = i['user']['id']
    twelve = i['user']['name']
    thirteen = i['user']['screen_name']
    fourteen = i['user']['description']
    fifteen = i['user']['friends_count']
    values = [one, two, three, four, five, six, seven, eight, nine, ten]
    values2 = [ten, twelve, thirteen, fourteen, fifteen]
    try:
        cursor.execute(insert, values) # Tweets table
    except Exception as E:
        insertErrors.append([i, E])
    try:
        cursor.execute(insert2, values2) # User table
    except Exception as E:
        insertErrors.append([i, E])

#
# dict = {}
# for i in tweets:
#     if i['user']['id'] in dict.keys():
#         dict[i['user']['id']] += 1
#     else:
#         dict[i['user']['id']] = 1
#
# for key, value in dict.items():
#     if value > 1:
#         print(key, value)

### Part 3 ###
# A. - SQL Code Below
'''CREATE OR REPLACE TRIGGER maxCourseNum
BEFORE UPDATE OR INSERT ON course
FOR EACH ROW
WHEN (new.CourseNr >= 599)
BEGIN
    :new.CourseNr := 598;
    dbms_output.put_line('Ammended CourseNr to 598');
END;
/'''

# B.
import re
card = '1234 5678 9012 3456'
CC = re.compile(r'\d{4} ?\d{4} ?\d{4} ?\d{4}')
CC.findall(card)