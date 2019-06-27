import copy
import sys
from re import search
from subprocess import getoutput as gop

import matplotlib.pyplot as plt
import mne
import numpy as np


def loadData(arquivo):
    arqOpen = open(f'data_10hz/{arquivo}')
    
    for _ in range(6):
        next(arqOpen)
    
    person = list()
    eeg = list()
    for row in arqOpen:
        columns = row.replace('\n','').split(',')

        if columns:
            columns = [float(i) for i in columns[:11]]
                    
            if(columns[0] == 0):
                if(len(eeg) == 256):
                    person.append(copy.deepcopy(eeg))
                eeg = list()
                
            columns = columns[1:]    
                
            # eeg.append(np.array(columns).reshape(10,1))
            eeg.append(columns)

    return np.array(person)

def reshapeData(data):
    newData = list()
    for d in data:
        row = list()
        for j in range(0,10):
            values = list()
            for i in d:
                values.append(i[j])
            row.append(copy.deepcopy(values))
        newData.append(copy.deepcopy(row))
    
    return np.array(newData)


                    
def main():
    # arquivos
    arquivos = gop('ls data_10hz').split('\n')
   
    # (234, 10, 256)  reshapaduuuu
    # 
    # # for arq in arquivos:
    # d1 = reshapeData(loadData(arquivos[2]))
    # print(d1.shape)

    # d1 = d1[0]

    # ch_names = ['1','2','3','4','5','6','7','8','9','10']
    # ch_types = ['eeg'] * 10

    # info = mne.create_info(
    #     ch_names=ch_names, 
    #     sfreq=256, 
    #     ch_types=ch_types)

    # print(info)
    # print(d1.shape)

    # raw = mne.io.RawArray(d1, info)

    # # raw.drop_channels(['x','nd','y'])
    # montage = mne.channels.read_montage('standard_1020')
    # raw.set_montage(montage)
    # raw.plot_psd()
    # print()

    # # Grafico no domínio da frequencia
    # plt.plot(np.linspace(0,1,256), raw.get_data()[0])
    # plt.xlabel('tempo (s)')
    # plt.ylabel('Dados EEG (mV/cm²)')


if __name__ == '__main__':
    main()
