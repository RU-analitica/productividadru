import pandas as pd
import numpy as np

f_nonEmpsG = pd.read_excel('./data/base.xlsx', sheet_name='nonEmpsG')
f_nonFG = pd.read_excel('./data/base.xlsx', sheet_name='nonFG')

df_nonEmpsG = pd.DataFrame(f_nonEmpsG)
df_nonFG = pd.DataFrame(f_nonFG)

def create_dict1():
    idArr = []
    nameArr = []
    for element in df_nonEmpsG['id']:
        idArr.append(element)
    for element in df_nonEmpsG['name']:
        nameArr.append(element)

    nonEmpsG = dict(zip(idArr, nameArr))

    return nonEmpsG

def create_dict2():
    idArr = []
    nameArr = []
    for element in df_nonFG['id']:
        idArr.append(element)
    for element in df_nonFG['name']:
        nameArr.append(element)

    nonFG = dict(zip(idArr, nameArr))

    return nonFG

print(create_dict1())