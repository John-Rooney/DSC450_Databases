
data = open('animal.txt', 'r')
data = data.readlines()

def B1(data):
    """Find animals in txt related to tiger and not common"""
    for row in data:
        animal = row.find('tiger')
        category = row.find('common')
        if animal > -1 and category == -1:
            print(row.split(', ')[1])
    return

def B2(data):
    """Find animals in text not related to tiger"""
    for row in data:
        animal = row.find('tiger')
        if animal == -1:
            print(row.split(', ')[1])
    return
