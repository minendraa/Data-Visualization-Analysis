import pandas as pd 

data1 = {'ID': [1, 2, 3, 4],
         'Name': ['Alice', 'Bob', 'Charlie', 'David'],
         'Age': [25, 30, 35, 40]}

df1 = pd.DataFrame(data1)

data2 = {'ID': [2, 3, 4, 5],
         'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
         'Salary': [50000, 60000, 70000, 80000]}

df2 = pd.DataFrame(data2)

# Inner merge (only rows with matching 'ID')
merged_inner = pd.merge(df1, df2, on='ID', how='inner')

print("Inner Merge Result:")
print(merged_inner)

# Outer merge (all rows, filling with NaN where necessary)
merged_outer = pd.merge(df1, df2, on='ID', how='outer')

print("\nOuter Merge Result:")
print(merged_outer)
