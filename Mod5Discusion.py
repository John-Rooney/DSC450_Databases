
Students = {1: ['Jack', 'Grad'], 2: ['Jane', 'UGrad'], 3: ['Karen', 'Grad'], 4: ['Jack', 'UGrad']}

Courses = {100: ['Intro to Databases', 4], 200: ['Research Colloquium', 2]}

Enrollments = {1: [100, 200], 2: 100, 4: 200}

crsNum = []
for (key, value) in Students.items():
    if 'Jack' in value:
        crsNum.append(Enrollments[key])

crsNum2 = set()
for i in crsNum:
    if type(i) == list:
        for a in i:
            crsNum2.add(a)
    else:
        crsNum2.add(i)
print(crsNum2)