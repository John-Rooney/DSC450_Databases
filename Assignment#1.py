
def sumNum(string):
    total = 0
    lst = string.split(',')
    n = len(lst)
    for num in lst:
        total += int(num)
    # print(str(total/n))
    return total / n
sumNum('10, 20, 30')

def GI(table, values):
    string = ''
    for i in values:
        for a in i:
            if a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                string += '\'' + str(i) + '\'' + ','
                break
            elif a in '1234567890':
                string += str(i) + ','
                break
    string = string[:-1] # To remove last comma
    # print('INSERT INTO {} VALUES({});'.format(table, string))
    return ('INSERT INTO {} VALUES({});'.format(table, string))

a = GI('TestTable', ['3', 'hello', '!345'])