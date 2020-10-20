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
    ('Databases for Analytics', 'Billy Bob', 4.0),
    ('Advanced Machine Learning', 'Jen Aniston', 3.0),
    ('Biochemistry', 'Matt Damon', 3.5),
    ('Biochemistry', 'Tina Fey', None),
    ('Databases for Analytics', 'Jen Aniston', None),

]