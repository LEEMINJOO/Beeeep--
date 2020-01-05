import os
import pandas as pd
from pytube import YouTube
from moviepy.editor import *
import librosa
import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model, Sequential
from keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from keras.layers import GRU, Bidirectional, BatchNormalization, Reshape, multiply
from keras.optimizers import Adam
import tensorflow as tf

def download_url(url, type='mp4'):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension=type).order_by('resolution').first().download(filename="tmp")
    # yt.streams.first().download(filename="tmp")


def make_model(input_shape):
    X_input = Input(shape=input_shape)
    X = Conv1D(196, kernel_size=15, strides=4)(X_input)  # CONV1D
    X = BatchNormalization()(X)  # Batch normalization
    X = Activation('relu')(X)  # ReLu activation
    X = Dropout(0.2)(X)                                         # dropout (use 0.8)

    X = GRU(units=128, return_sequences=True)(X)  # GRU (use 128 units and return the sequences)
    X = Dropout(0.2)(X)                                         # dropout (use 0.8)
    X = BatchNormalization()(X)  # Batch normalization
    y = Activation("softmax")(X)
    X = multiply([y, X])

    X = GRU(units=128, return_sequences=True)(X)  # GRU (use 128 units and return the sequences)
    X = Dropout(0.2)(X)                                         # dropout (use 0.8)
    X = BatchNormalization()(X)  # Batch normalization
    X = Dropout(0.2)(X)   # dropout (use 0.8)
    y = Activation("softmax")(X)
    X = multiply([y, X])
    X = TimeDistributed(Dense(1, activation="sigmoid"))(X)  # time distributed  (sigmoid)

    model = Model(inputs=X_input, outputs=X)
    return model

def graph_spectrogram(wav_file):
    rate, data = get_wav_info(wav_file)
    nfft = 200  # 윈도우 길이
    fs = rate  # frequency
    noverlap = 120  # Overlap between windows
    nchannels = data.ndim

    S = librosa.feature.melspectrogram(data, sr=fs, n_mels=128, n_fft=nfft, hop_length=(nfft - noverlap))
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S

# Load a wav file
def get_wav_info(wav_file):
    data, rate = librosa.load(wav_file, sr=44100)
    return rate, data

def make_beep_wav(wav, y, output_name):
    beep, _ = librosa.load('beep.wav', sr=44100)
    data, _ = librosa.load(wav, sr=44100)
    length = y.shape[0]
    for i in range(1, length):
        tmp = int(len(data)*(i)/length)
        t_1 = y[i-1]
        t = y[i]
        if (t_1 == 0) and (t == 1):
            if tmp > 22000 :
                data[tmp-22000:tmp] = beep[:22000]*0.5
            else:
                data[:tmp] = beep[:tmp]*0.5
    librosa.output.write_wav(output_name, data, sr=44100)

def output_postprocessing(outputs, th):
    for output in outputs:
        output[output<th] = 0
        output[output>=th] = 1
    return outputs

def main():

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.Session(config=config)
    # Sinsagae
    # url = 'https://www.youtube.com/watch?v=n6RCAIbSPBQ'
    # ZZAngu
    url = 'https://www.youtube.com/watch?v=ymHbDFokS-g'
    download_url(url)
    videoclip = VideoFileClip("tmp.mp4")
    audioclip = videoclip.audio
    audioclip.write_audiofile("tmp.wav")
    X = []
    X.append(np.transpose(graph_spectrogram("tmp.wav")))
    X = np.array(X)
    X = (X - X.min()) / (X.max() - X.min())
    print(X.shape)

    n_freq = 128
    model = make_model(input_shape=(None, n_freq))
    model.load_weights("attention.hdf5")
    model.summary()
    y = output_postprocessing(model.predict(X), 0.7)
    make_beep_wav("tmp.wav", y[0], "result.wav")
    videoclip.audio = AudioFileClip("result.wav")
    print(y.shape)
    videoclip = videoclip.subclip(28, 34)
    videoclip.write_videofile("result.mp4")

main()