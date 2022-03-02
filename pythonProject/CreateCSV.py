import csv
import os
import numpy as np
import librosa.display
import matplotlib.pyplot as plt

""" Extracting the Spectrogram """
directory = os.getcwd()

def createSpecgram():
    global directory
    cmap = plt.get_cmap('inferno')
    plt.figure(figsize=(8, 8))
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            y, sr = librosa.load(filename, mono=True)
            plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=1024, cmap=cmap, sides='default', mode='default', scale='dB')
            plt.axis('off')
            plt.savefig(f'{directory}/{filename[:-3].replace(".", "")}.png')
            plt.clf()


def createDataSet():
    """
        Converting audio into spectograms
        Extracting features from Spectrogram and they are:
        Mel-frequency cepstral coefficients (MFCC)(20 in number)
        Spectral Centroid,
        Zero Crossing Rate
        Chroma Frequencies
        Spectral Roll-off.
        """
    header = 'filename chroma_stft ee spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header = header.split()
    file = open('dataset.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            songname = f'{directory}/{filename}'
            y, sr = librosa.load(songname, mono=True, duration=30)
            rms = librosa.feature.rms(y=y)
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
            for e in mfcc:
                to_append += f' {np.mean(e)}'
            file = open('dataset.csv', 'a', newline='')
            with file:
                writer = csv.writer(file)
                writer.writerow(to_append.split())

if __name__ == '__main__':
    createSpecgram()
    createDataSet()





