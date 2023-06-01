
import pandas as pd
import math as math


table_a = pd.DataFrame({
    'A': ['all', 1, 4, 4,6,5,8,'all'], 
    'B': [2, 2, 3, 2,6,7,12,'all'], 
    'C': [3, 3, 3, 3,6,1,8,13], 
    'D': [4, 4, 4, 4,6,1,13,9]
})

table_b = pd.DataFrame({
    'A': ['all', 1, 'all', 4,5,'all','all','all'], 
    'B': [2, 2, 2, 'all',7,'all','all','all'], 
    'C': [3, 3, 'all', 3,'all',8,13,'all'], 
    'target': ['xyz', 'zyx', 'tyz', 'abc','yyy','ppp','hgf','hhh']
})


priority_keys = ['A', 'B', 'C']
dummy_keys = ['D']
existing_keys = []

def get_priorities(row, table_b):
    df = table_b.copy()
    for k in priority_keys + dummy_keys:
        df[k + "_a"] = row[k]
    df["p1"] = 0
    df["p2"] = 0
    for i, k in enumerate(priority_keys):
        p = len(priority_keys) - i
        match = (df[k] == df[k + "_a"])
        partialmatch = (~match) & (df[k]=='all')
        df["p1"] = df["p1"] + (p * match)
        df["p2"] = df["p2"] + (p * partialmatch)
    
    df["exact"] = (df["p1"]==math.factorial(len(priority_keys))) # extra point for exact match
    df["priority"] = df["exact"] + df["p1"] + df["p2"]
    df = df[df["p1"]>0]  # atleast one column should be exact match

    return df.sort_values(by="priority", ascending=False)

def assign_label(row_a, table_b):
    global existing_keys
    prioritydf = get_priorities(row_a, table_b)
    for i, row in prioritydf.iterrows():
        key = (*tuple(row[k + "_a"] for k in priority_keys), *tuple(row[k + "_a"] for k in dummy_keys))
        if key not in existing_keys:
            existing_keys.append(key)
            row_a["target"] = row["target"]
            row_a["debug"] = (i, row['priority'])
            table_b.drop(index=i, inplace=True)
            return row_a


def merge(table_a, table_b):
    table_b = table_b.copy()
    result = table_a.apply(assign_label, axis=1, table_b=table_b)
    return result.dropna(how="all")

merge(table_a, table_b)    
# get_priorities(table_a.iloc[3], table_b)
