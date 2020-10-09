
def B1(data):
    """Find animals in txt related to tiger and not common"""
    file = open(data, 'r')
    lines = file.readlines()

    for row in lines:
        animal = row.find('tiger')
        category = row.find('common')
        if animal > -1 and category == -1:
            print(row.split(', ')[1])
    file.close()
    return


def B2(data):
    file = open(data, 'r')
    lines = file.readlines()
    """Find animals in text not related to tiger"""
    for row in lines:
        animal = row.find('tiger')
        if animal == -1:
            print(row.split(', ')[1])
    file.close()
    return


### PART 2 ###
import sqlite3
conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE Employee;')
cursor.execute('DROP TABLE Role;')
conn.commit()
conn.close()

createTbl = """
CREATE TABLE Employee
(
    First VARCHAR(12) NOT NULL,
    Last VARCHAR(15) NOT NULL,
    Address VARCHAR(30),
    
    CONSTRAINT Employee_PK
        PRIMARY KEY(First, Last)
);
"""

createTbl2 = """
CREATE TABLE Role
(
    Job VARCHAR(25) NOT NULL,
    Salary NUMBER(5, 0),
    Assistant VARCHAR(30),
    
    CONSTRAINT Role_PK
        PRIMARY KEY(Job)
);
"""

cursor.execute(createTbl)
cursor.execute(createTbl2)

insert1 = 'INSERT OR IGNORE INTO Employee VALUES(?, ?, ?);'
insert2 = 'INSERT OR IGNORE INTO Role VALUES(?, ?, ?)'

f = open('data_module4_part2.txt', 'r')
for i in f.readlines():
    # print(i)
    # print(type(i))
    cursor.execute(insert1, i.split(', ')[:3])
    if i.split(', ')[-1] != 'NULL\n':
        cursor.execute(insert2, i.strip().split(', ')[3:])
    else:
        alt = i.split(', ')[3:5]
        alt.append(None)
        cursor.execute(insert2, alt)

f.close()

empResult = cursor.execute('SELECT * FROM Employee;')
empResult.fetchall()
roleResult = cursor.execute('SELECT * FROM Role;')
roleResult.fetchall()

conn.commit()
conn.close()