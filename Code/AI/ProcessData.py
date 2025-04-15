import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

data=pd.read_csv('data.csv',on_bad_lines='skip')

data.head()

data.shape

data.info()

data.describe()

data['strength'].value_counts()

data=data.dropna(axis=0)

## shape of the data
data.shape

data['password']=data['password'].astype('str')

data.info()

def cal_len(x):
    '''
    Calculates the length of a given password.
    '''
    x=str(x)
    return len(x)

def cal_capL(x):
    '''
    Calculates the number of capital letters in the password.
    '''
    x=str(x)
    cnt=0
    for i in x:
        if(i.isupper()):
            cnt+=1
    return cnt

def cal_smL(x):
    '''
    Calculates the nu,ber of small letters in the password.
    '''
    x=str(x)
    cnt=0
    for i in x:
        if(i.islower()):
            cnt+=1
    return cnt

def cal_spc(x):
    '''
    Calculates the number of special characters in the password.
    '''
    x=str(x)
    return (len(x)-len(re.findall('[\w]',x)))


length=lambda x:cal_len(x)
capital=lambda x:cal_capL(x)
small=lambda x:cal_smL(x)
special=lambda x:cal_spc(x)

data['length']=pd.DataFrame(data.password.apply(length))
data['capital']=pd.DataFrame(data.password.apply(capital))
data['small']=pd.DataFrame(data.password.apply(small))
data['special']=pd.DataFrame(data.password.apply(special))

# five elements from the top
data.head()

def cal_num(x):
    '''
    Calculates the number of numeric values in the password.
    '''
    x=str(x)
    cnt=0
    for i in x:
        if(i.isnumeric()):
            cnt+=1
    return cnt

numeric=lambda x:cal_num(x)
data['numeric']=pd.DataFrame(data.password.apply(cal_num))

data.head()

data.to_csv('processed.csv',index=None)