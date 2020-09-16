def sumNum(string):
    """returns mean of single string of numbers separated by commas (i.e. '1, 2, 3')"""
    total = 0
    lst = string.split(',')
    n = len(lst)
    for num in lst:
        total += int(num)
    print(str(total / n))
    return total / n


sumNum('10, 20, 30')
sumNum('-10, 0, 10')


def generateInsert(table, values):
    """returns SQL insert statement, 1st arg: table name, 2nd arg: list of string values"""
    string = ''
    for i in values:
        letters = 0
        for a in i:
            if a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                letters += 1

        # if at least 1 letter in value, added to string w/ quotes
        if letters > 0:
            string += '\'' + str(i) + '\'' + ','

        # if no letters in value, added to string w/o quotes
        else:
            string += str(i) + ','

    # To remove last comma
    string = string[:-1]
    print('INSERT INTO {} VALUES({});'.format(table, string))
    return 'INSERT INTO {} VALUES({});'.format(table, string)


generateInsert('Students', ['1', 'Jane', 'A+'])
generateInsert('Students', ['123', 'Billy', 'B-'])