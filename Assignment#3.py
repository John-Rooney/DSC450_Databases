import sqlite3

createtbl = """
CREATE TABLE Animal
(
  AID       NUMBER(3, 0),
  AName      VARCHAR2(30) NOT NULL,
  ACategory VARCHAR2(18),

  TimeToFeed NUMBER(4,2),

  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);
"""

inserts = ["INSERT INTO Animal VALUES(1, 'Galapagos Penguin', 'exotic', 0.5);",
           "INSERT INTO Animal VALUES(2, 'Emperor Penguin', 'rare', 0.75);",
           "INSERT INTO Animal VALUES(3, 'Sri Lankan sloth bear', 'exotic', 2.5);",
           "INSERT INTO Animal VALUES(4, 'Grizzly bear', 'common', 3.0);",
           "INSERT INTO Animal VALUES(5, 'Giant Panda bear', 'exotic', 1.5);",
           "INSERT INTO Animal VALUES(6, 'Florida black bear', 'rare', 1.75);",
           "INSERT INTO Animal VALUES(7, 'Siberian tiger', 'rare', 3.25);",
           "INSERT INTO Animal VALUES(8, 'Bengal tiger', 'common', 2.75);",
           "INSERT INTO Animal VALUES(9, 'South China tiger', 'exotic', 2.5);",
           "INSERT INTO Animal VALUES(10, 'Alpaca', 'common', 0.25);",
           "INSERT INTO Animal VALUES(11, 'Llama', NULL, 3.5);"]

conn = sqlite3.connect('dsc450.db') # open the connection
cursor = conn.cursor()
# conn.execute('DROP TABLE ANIMAL;')
cursor.execute(createtbl)   # create the Animal table
# for ins in inserts:         # insert the rows
#     cursor.execute(ins)

conn.commit()   # finalize inserted data
conn.close()    # close the connection


def queryToTxt(query):
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    result = cursor.execute(query)
    resultTxt = str(result.fetchall())
    conn.commit()
    conn.close()
    resultTxt = resultTxt.replace('), (', '),  (')
    # print(resultTxt)
    resultVals = resultTxt.split(',  ')
    f = open('animal.txt', 'w')
    for i in resultVals:
        if i[0] == '[':
            i = i[1:]
            f.write(i + '\n')
        elif i[-1] == ']':
            i = i[:-1]
            f.write(i + '\n')
        else:
            f.write(i + '\n')
    f.close()
    return

queryToTxt('SELECT * FROM ANIMAL;')


def txtToTable(txt):
    f = open(txt, 'r')
    valueList = []
    for i in f.readlines():
        valueList.append(eval(i))

    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    insert = 'INSERT INTO ANIMAL VALUES(?, ?, ?, ?);'
    cursor.executemany(insert, valueList)
    conn.commit()
    count = cursor.execute('SELECT count(*) FROM ANIMAL;')
    print(count.fetchall())
    conn.close()

txtToTable('animal.txt')