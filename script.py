import copy
import sys
from subprocess import getoutput as gop

import matplotlib.pyplot as plt
import mne
import numpy as np
from mne.time_frequency import psd_welch as psdw

def loadData(arquivo):
    arqOpen = open(f'data_10hz/{arquivo}')
    fileLimitTime = 0
    
    for _ in range(6):
        next(arqOpen)
    
    eeg = list()
    person = list()
    for row in arqOpen:
        columns = row.split(',')

        if columns:
            columns = columns[:7]
                    
            if(columns[0] == '0'):
                if(len(eeg) == 256):
                    fileLimitTime +=1
                    for k in eeg:
                        person.append(list(map(lambda i : float(i), k[1:])))
                eeg = list()
            
            eeg.append(columns)

    return [np.array(person).T, fileLimitTime]

def prepareRaw(data):
    info = mne.create_info(
        ch_names=['eeg'] * 6, 
        sfreq=256, 
        ch_types=['eeg'] * 6)

    raw = mne.io.RawArray(data, info)

    for _ in range(5):
        raw.filter(l_freq=5, h_freq=50)

    return raw


def scaleValue(max, min):
    return ((min*100)/max)

def findAlphaTime(raw, tmin, window):
    faixas = list()
    
    alpha = psdw(raw, tmin=tmin, tmax=tmin+window, fmin=8, fmax=12, verbose=False)[0]   
    theta = psdw(raw, tmin=tmin, tmax=tmin+window, fmin=5, fmax=7, verbose=False)[0]
    beta = psdw(raw, tmin=tmin, tmax=tmin+window, fmin=12, fmax=30, verbose=False)[0]
    gamma = psdw(raw, tmin=tmin, tmax=tmin+window, fmin=25, fmax=100, verbose=False)[0]
    
    faixas.append(np.average(alpha))
    faixas.append(np.average(theta))
    faixas.append(np.average(beta))
    faixas.append(np.average(gamma))
    
    indexMaiorFaixa = np.argmax(np.array(faixas))
    
    if (indexMaiorFaixa == 0):
        indexSegMaiorFaixa = np.argmax(np.array(faixas[1:]))+1
        print(f'{tmin}: {scaleValue(faixas[indexMaiorFaixa], faixas[indexSegMaiorFaixa])}')

def plotWindowTime(raw, tmin, window, fmax=30):
    psds, freqs = psdw(raw, tmin=tmin, tmax=tmin+window, fmax=fmax)
    psd_Average = np.average(psds, axis=0) ** 2
    plt.plot(freqs, psd_Average)
    plt.show()
                    
def main():
    # arquivos
    arquivos = gop('ls data_10hz').split('\n')
    times = [[95, 96, 234, 367, 597, 786],
            [39, 46, 110, 130, 280, 363],
            [103, 114, 136, 154, 171, 185]]
    window = 3
    
    for arqPos, arq in enumerate(arquivos):
        data, fileLimitTime = loadData(arq)
        print(data.shape)
        raw = prepareRaw(data)

        # acha os tempos do ritmo alpha
        # for i in range(fileLimitTime - window):
        #     findAlphaTime(raw, i, window)

        # plota os tempos selecionados
        for i in times[arqPos]:
            plotWindowTime(raw, i, window)

if __name__ == '__main__':
    main()
