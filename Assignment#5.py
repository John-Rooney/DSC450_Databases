
import sqlite3
import csv
fd = open('Public_Chauffeurs_Short_hw3.csv', 'r')
reader = csv.reader(fd)

conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()

# cursor.execute('DROP TABLE Chauff;')

createTbl = """
CREATE TABLE Chauff
(
    License_Number VARCHAR(15),
    Renewed Date,
    Status VARCHAR(30),
    Status_Date Date,
    Driver_Type VARCHAR(30),
    License_Type VARCHAR(30),
    Original_Issue Date Date,
    Name VARCHAR(30),
    Sex VARCHAR(6),
    Chauffeur_City VARCHAR(30),
    Chauffeur_State VARCHAR(15),
    Record_Number VARCHAR(15),


    CONSTRAINT Chauff_PK
        PRIMARY KEY(License_Number, Name)
);
"""
cursor.execute(createTbl)
insert = 'INSERT INTO Chauff VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

for row in reader:
    cursor.execute(insert, row)

fd.close()
conn.commit()
conn.close()

### PART 2 ###
import io
import json
file = io.open('Assignment4.txt', mode='r', encoding="utf-8")
tweetdata = file.read()
file.close()
tweetdata = tweetdata.split('EndOfTweet')

tweets = []
for i in tweetdata:
    tweets.append(json.loads(i))

conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()
createTbl = """
CREATE TABLE Tweets
(
    created_at VARCHAR(30),
    id_str VARCHAR(30),
    text VARCHAR(140),
    source VARCHAR(60),
    in_reply_to_user_id VARCHAR(30),
    in_reply_to_screen_name VARCHAR(30),
    in_reply_to_status_id NUMBER(18),
    retweet_count NUMBER(8),
    contributors VARCHAR(30),
    
    CONSTRAINT Tweets_PK
        PRIMARY KEY (id_str) 
);
"""

insert = 'INSERT INTO Tweets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'

cursor.execute(createTbl)
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
    values = [one, two, three, four, five, six, seven, eight, nine]
    cursor.execute(insert, values)

conn.commit()
conn.close()