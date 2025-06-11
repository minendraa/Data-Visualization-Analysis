import pandas as pd
data={
    'Category':['A','B','C','A','B','C'],
    'Values':[10,20,30,40,50,60]
}

df=pd.DataFrame(data)

grouped = df.groupby('Category')['Values'].sum()
print(grouped)
