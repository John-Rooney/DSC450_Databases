
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