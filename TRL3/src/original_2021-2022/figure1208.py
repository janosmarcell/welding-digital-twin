#!/usr/bin/env python
# coding: utf-8

# In[104]:


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from operator import add

all_pairs = []

def append_to_pairs(row, col_name, num):
    plot_val1 = []
    plot_val2 = []
    pairs = []
    vals = row[col_name].split(';')
    vals = list(map(int, vals))
    for i in np.arange(num):
        if len(vals) <= i:
            plot_values[i].append(0)
        else:
            plot_values[i].append(vals[i])
    for val in vals:
        pairs.append([int(row['sens']), val])
        all_pairs.append([int(row['sens']), val])
    return pairs

def append_to_pairs_lack(row):
    plot_val1 = []
    plot_val2 = []
    pairs = []
    vals = row['lack of fusion'].split(';')
    vals = list(map(int, vals))
    for i in np.arange(2):
        if len(vals) <= i:
            plot_values[i].append(0)
        else:
            plot_values[i].append(vals[i])
    for val in vals:
        pairs.append([int(row['sens']), val])
        all_pairs.append([int(row['sens']), val])
    return pairs

def append_to_pairs_imp(row):
    pairs = []
    vals = row['imperfect shape_B'].split(';')
    vals = list(map(int, vals))
    for i in np.arange(5):
        if len(vals) <= i:
            plot_values[i].append(0)
        else:
            plot_values[i].append(vals[i])
    for val in vals:
        pairs.append([int(row['sens']), val])
        all_pairs.append([int(row['sens']), val])
    return pairs

def add_all_i(i):
    sum = 0
    l = []
    for j in np.arange(10):
        #sum = list( map(add, sum, np.array(plot_values)[:,j]) )
        #print(np.array(plot_values, dtype=np.ndarray))
        s = np.sum(tonparray(plot_values)[:i,j])
        l.append(s)
    return np.array(l)

def add_all_i_v2(i):
    l = []
    arrval = tonparray(plot_values)
    sumrow = np.arange(10)
    for row_ind in np.arange(i):
        sumrow = sumrow + arrval[row_ind]
    return sumrow

def tonparray(arr):
    full_arr = []
    for row in arr:
        full_arr.append(np.array(row))
    return np.array(full_arr, dtype=object)


# In[105]:


number_of_max_cluster = 5 # hány darab klaszter fordul elő maximálisan abban az oszlopban
col_name = 'imperfect shape_B' # az oszlop neve

data = pd.read_csv("sens.csv", delimiter=';', dtype=str)
plot_values = [[],[],[],[],[]]
for index, row in data.iterrows():
    append_to_pairs(row, col_name, number_of_max_cluster)

plt.rcParams.update({'font.size': 16}) # betű méret

N = number_of_max_cluster
ind = np.arange(len(plot_values[0]))
width = 0.5 # oszlopok szélesssége

plt.figure(figsize=(14,6)) # az ábra arányai és mérete
for i in np.arange(number_of_max_cluster):
    plt.bar(np.arange(len(plot_values[i])), plot_values[i], width, bottom=add_all_i(i))
    

plt.ylabel('Number of points')
plt.xlabel('Sensitivity threshold (%)')
plt.title('Imperfect shape')
plt.xticks(ind, np.arange(90,100))
#plt.yticks(np.arange(0, 81, 10))
plt.legend(('Cluster #1', 'Cluster #2', 'Cluster #3', 'Cluster #4', 'Cluster #5'))

plt.show()


# In[4]:


number_of_max_cluster = 2 # hány darab klaszter fordul elő maximálisan abban az oszlopban
col_name = 'lack of fusion' # az oszlop neve

data = pd.read_csv("sens.csv", delimiter=';', dtype=str)
plot_values = [[],[],[],[],[]]
for index, row in data.iterrows():
    append_to_pairs(row, col_name, number_of_max_cluster)


plt.rcParams.update({'font.size': 16}) # betű méret

N = number_of_max_cluster
ind = np.arange(len(plot_values[0]))
width = 0.5 # oszlopok szélesssége

plt.figure(figsize=(14,6)) # az ábra arányai és mérete
for i in np.arange(number_of_max_cluster):
    plt.bar(np.arange(len(plot_values[i])), plot_values[i], width, bottom=add_all_i_v2(i))

plt.ylabel('Number of points')
plt.xlabel('Sensitivity threshold (%)')
plt.title('Lack of fusion')
plt.xticks(ind, np.arange(90,100))
#plt.yticks(np.arange(0, 81, 10))
plt.legend(('Cluster #1', 'Cluster #2', 'Cluster #3', 'Cluster #4', 'Cluster #5'))

plt.show()


# In[109]:


number_of_max_cluster = 1 # hány darab klaszter fordul elő maximálisan abban az oszlopban
col_name = 'cavities' # az oszlop neve

data = pd.read_csv("sens.csv", delimiter=';', dtype=str)
plot_values = [[],[],[],[],[]]
for index, row in data.iterrows():
    append_to_pairs(row, col_name, number_of_max_cluster)


plt.rcParams.update({'font.size': 16}) # betű méret

N = number_of_max_cluster
ind = np.arange(len(plot_values[0]))
width = 0.5 # oszlopok szélesssége

plt.figure(figsize=(14,6)) # az ábra arányai és mérete
for i in np.arange(number_of_max_cluster):
    plt.bar(np.arange(len(plot_values[i])), plot_values[i], width, bottom=add_all_i_v2(i))

plt.ylabel('Number of points')
plt.xlabel('Sensitivity threshold (%)')
plt.title('Cavities')
plt.xticks(ind, np.arange(90,100))
#plt.yticks(np.arange(0, 81, 10))
plt.legend(('Cluster #1', 'Cluster #2', 'Cluster #3', 'Cluster #4', 'Cluster #5'))

plt.show()


# In[111]:


number_of_max_cluster = 1 # hány darab klaszter fordul elő maximálisan abban az oszlopban
col_name = 'solid inclusion' # az oszlop neve

data = pd.read_csv("sens.csv", delimiter=';', dtype=str)
plot_values = [[],[],[],[],[]]
for index, row in data.iterrows():
    append_to_pairs(row, col_name, number_of_max_cluster)


plt.rcParams.update({'font.size': 16}) # betű méret

N = number_of_max_cluster
ind = np.arange(len(plot_values[0]))
width = 0.5 # oszlopok szélesssége

plt.figure(figsize=(14,6)) # az ábra arányai és mérete
for i in np.arange(number_of_max_cluster):
    plt.bar(np.arange(len(plot_values[i])), plot_values[i], width, bottom=add_all_i_v2(i))

plt.ylabel('Number of points')
plt.xlabel('Sensitivity threshold (%)')
plt.title('Solid inclusion')
plt.xticks(ind, np.arange(90,100))
#plt.yticks(np.arange(0, 81, 10))
plt.legend(('Cluster #1', 'Cluster #2', 'Cluster #3', 'Cluster #4', 'Cluster #5'))

plt.show()

