import sys
import numpy as np

from subprocess import getoutput as gop

# arquivos
pasta = gop('ls data_10hz').split('\n')

data = list()
for arquivo in pasta:
    arqOpen = open(f"data_10hz/{arquivo}")
    arqSub = arqOpen.seek(204,0)
    eeg = list()
    for row in arqOpen:
        columns = row.replace('\n','').split(',')
        columns = columns[:-1]
                
        if(columns[0] == '0'):
            data.append(eeg)
            eeg = list()

        columns = columns [1:]        
        eeg.append(columns)


data = np.array(data[1:])
# print(data)
print(data[0])
print(data[0][0])
print(data[0][0][0])
print(data.shape)



