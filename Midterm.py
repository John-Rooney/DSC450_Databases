import sqlite3

conn = sqlite3.connect('dsc450.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE Grade;')
cursor.execute('DROP TABLE Course;')
cursor.execute('DROP TABLE Student;')

conn.commit()
conn.close()

createStudent = """
CREATE TABLE Student(
    StudentID NUMBER(6),
    Name VARCHAR2(20),
    Address VARCHAR2(30),
    GradYear NUMBER(4),
    
    CONSTRAINT Student_PK
        Primary Key (StudentID)
);
"""
createCourse = """
CREATE TABLE Course(
    CName VARCHAR2(30),
    Department VARCHAR2(20),
    Credits NUMBER(1),
    
    CONSTRAINT Course_PK
        PRIMARY KEY (CName)
);
"""
createGrade = """
CREATE TABLE Grade(
    CName VARCHAR2(30),
    StudentID NUMBER(6),
    CGrade NUMBER(2, 1),
    
    CONSTRAINT GRADE_PK
        Primary Key (CName, StudentID),
        
    CONSTRAINT Grade_FK_SID
        FOREIGN KEY (StudentID)
            REFERENCES Student(StudentID),
    
    CONSTRAINT GRADE_FK_CName
        FOREIGN KEY (CName)
            REFERENCES Course(CName)
);
"""

cursor.execute(createStudent)
cursor.execute(createCourse)
cursor.execute(createGrade)

students = [
    (111111, 'Billy Bob', '123 Main St', 2014),
    (222222, 'Jen Aniston', '456 Drewery Lane', 2015),
    (333333, 'Matt Damon', '789 Wall St', 2015),
    (444444, 'Tina Fey', '1010 Locust St', 2016),
    (555555, 'Will Smith', '666 Broken Blvd', 2014)
]
courses = [
    ('Databases for Analytics', 'DSC', 4),
    ('Advanced Machine Learning', 'DSC', 4),
    ('Biochemistry', 'CHE', 3),
    ('Underwater Basket-weaving', 'PE', 6)
]
grades = [
    ('Databases for Analytics', 111111, 4.0),
    ('Advanced Machine Learning', 222222, 3.0),
    ('Biochemistry', 333333, 3.5),
    ('Biochemistry', 444444, None),
    ('Databases for Analytics', 222222, None),
    ('Advanced Machine Learning', 111111, None),
    ('Biochemistry', 111111, 2.0),
    ('Databases for Analytics', 444444, 3.0),
    ('Advanced Machine Learning', 333333, 2.5),
    ('Biochemistry', 222222, 4.0)
]

cursor.executemany('INSERT INTO Student VALUES(?, ?, ?, ?);', students)
cursor.executemany('INSERT INTO Course VALUES(?, ?, ?);', courses)
cursor.executemany('INSERT INTO Grade VALUES(?, ?, ?);', grades)

view = ''' CREATE VIEW AllCols AS
    SELECT Student.StudentID, Name, Address, GradYear, Course.CName, CGrade, Department, Credits
    FROM Student LEFT OUTER JOIN Grade ON Student.StudentID = Grade.StudentID
    LEFT OUTER JOIN Course ON Course.CName = Grade.CName
    UNION
    SELECT Student.StudentID, Name, Address, GradYear, Course.CName, CGrade, Department, Credits
    FROM Course LEFT OUTER JOIN Grade ON Course.CName = Grade.CName
    LEFT OUTER JOIN Student ON Grade.StudentID = Student.StudentID'''

cursor.execute(view)
AllCols = cursor.execute('SELECT * FROM AllCols;').fetchall()
# for i in cursor.execute('SELECT * FROM AllCols;').fetchall():
#     print(i)
# cursor.execute('DROP VIEW AllCols;')

file = open('midterm.txt', 'w')
for i in AllCols:
    file.write(str(i)[1:-1] + '\n')
file.close()

file = open('midterm.txt', 'r')
data = file.readlines()
file.close()

dict = {}
for i in data:
    values = i.replace('\'', '').strip().split(', ')
    if values[-2] not in dict.keys():
        dict[values[-2]] = values[-1]
    elif values[-2] in dict.keys():
        if dict[values[-2]] != values[-1]:
            print('Error: CName -> Credits Not Consistent')
            print(i)

