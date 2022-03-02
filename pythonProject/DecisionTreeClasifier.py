import joblib
import numpy as np
import librosa
from keras.models import Sequential

def compareSounds():
    # Importing the model
    scaler = joblib.load('scalerDecisionTree.pkl')
    clf = joblib.load('classifierDecisionTree')

    """Predicting a sound"""

    model = Sequential()

    songname = "D:/Disertatie/Disertatie/pythonProject/From.wav"

    y, sr = librosa.load(songname, mono=True, duration=5)

    feature_list = []
    #feature_list.append(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))
    feature_list.append(np.mean(librosa.feature.rms(y=y)))
    feature_list.append(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    feature_list.append(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
    feature_list.append(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
    feature_list.append(np.mean(librosa.feature.zero_crossing_rate(y)))
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    for e in mfcc:
        feature_list.append(np.mean(e))

    prediction = clf.predict([feature_list])

    print(prediction)

if __name__ == '__main__':
    compareSounds()
