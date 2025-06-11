import pandas as pd

# Define a dictionary containing employee data
data1 = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
         'Age': [27, 24, 22, 32],
         'Address': ['Kathmandu', 'Bhaktapur', 'Lalitpur', 'Pokhara']
        }

# Define a dictionary containing employee data
data2 = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
         'Marks': [27, 24, 22, 32],
         'Grade': ['A', 'A', 'C', 'B']
        }

# Create DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Extract the 'Grade' and 'Marks' columns from df2
df3 = df2["Grade"]
df4 = df2["Marks"]

# Combine the DataFrames along columns
frames = [df1, df3, df4]
res = pd.concat(frames, axis=1)

# Set the index to start from 1 instead of 0
res.index = range(1, len(res) + 1)

# Modify 'Age' by adding 1 to each value
res['Age'] = res['Age'].apply(lambda x: x + 1)

# Sorting by 'Age' in descending order
sorted_df = res.sort_values(by="Age", ascending=False)

# Display the modified DataFrame after sorting
print("Sorted DataFrame by Age:")
print(sorted_df)

# Group by 'Grade' and calculate the mean for numeric columns (like 'Age' and 'Marks')
grouped_df = res.groupby('Name')['Age'].mean()

# Display the grouped DataFrame
print("\nGrouped DataFrame by Grade:")
print(grouped_df)

sorted_by_name = grouped_df.sort_index(ascending=False)
print(sorted_by_name)