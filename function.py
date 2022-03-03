import numpy as np


with open("file/test1.csv") as file_name:
    arr = np.loadtxt(file_name, dtype=str)


df = []
l = []
for i in arr:
    for j in range(0, len(i), 2):
        l.append(i[j:j+2])
    df.append(l)
    l = []
    
for k in df : 
    if k[0]=="50":
        print(k[0])
