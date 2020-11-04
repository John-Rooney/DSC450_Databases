
### Part 1 ###
import pandas as pd

# A.
df = pd.read_csv('Employee.txt', names=['first', 'middle', 'last', 'phone', 'bday', 'street', 'city', 'state', 'gender', 'salary', 'SS', 'num'])
males = df[df.iloc[:, 8] == 'M']

# B.
minSalary = df[df['gender'] == 'F']['salary'].min()

# C.
for i in df['salary'].groupby(df['middle']):
    print(i)