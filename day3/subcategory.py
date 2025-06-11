import pandas as pd
data = {'Category': ['A', 'A', 'A', 'B', 'B', 'C'],
        'Subcategory': ['X', 'Y', 'X', 'X', 'Y', 'X'],
        'Values': [10, 20, 10, 30, 40, 50]}
df = pd.DataFrame(data)

# Group by 'Category' and 'Subcategory'
grouped = df.groupby(['Category', 'Subcategory'])['Values'].sum()
print(grouped)