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

df1=pd.DataFrame(data1)

df2=pd.DataFrame(data2)

df3=df2["Grade"]
df4=df2["Marks"]

frames=[df1,df3,df4]
res=pd.concat(frames,axis=1)
res.index=range(1,len(res)+1)
#print(res)

sorted_df=res.sort_values(by="Age",ascending=False)
#print(sorted_df)

res['Age']=res['Age'].apply(lambda x:x+1)
print(res)


grouped_df=res.groupby('Name').mean('Age')
print(grouped_df)