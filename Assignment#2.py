def validateInsert(string):
    """Simple SQL Insert statement check"""
    if string[0:12] == 'INSERT INTO ' and string[-1] == ';':

        firstP = string.find('(')
        lastP = string.find(')')

        values = string[firstP:lastP + 1]
        table = string.split()[2]

        print('Inserting {} into {} table'.format(values, table))
    else:
        print('Invalid Insert')

validateInsert('INSERT INTO Students VALUES (1, Jane, A+);')
validateInsert('INSERT INTO Students VALUES (1, Jane, A+)')
validateInsert('INSERT Students VALUES (1, Jane, A+);')
validateInsert('INSERT INTO Phones VALUES (42, 312-555-1212);')