import pandas as pd
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})
df2 = pd.DataFrame({'ID': [2, 3, 4], 'Age': [25,33, 30]})

left_join = pd.merge(df1, df2, on='ID', how='left')
print(left_join)

right_join = pd.merge(df1, df2, on='ID', how='right')
print(right_join)
