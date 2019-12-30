import os
import matplotlib.pyplot as plt

from pydub import AudioSegment
import librosa
import numpy as np

def graph_spectrogram(wav_file):
    rate, data = get_wav_info(wav_file)
    nfft = 200 # 윈도우 길이
    fs = rate # frequency
    noverlap = 120 # Overlap between windows 
    nchannels = data.ndim
    
    S = librosa.feature.melspectrogram(data, sr=fs, n_mels=128, n_fft=nfft, hop_length=(nfft-noverlap))
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S

# Load a wav file
def get_wav_info(wav_file):
    data, rate = librosa.load(wav_file, sr=44100)
    return rate, data

# Used to standardize volume of audio clip
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# Load raw audio files for speech synthesis
def load_raw_audio(audio_dir):
    activates = []
    backgrounds = []
    negatives = []
    for filename in os.listdir(audio_dir):
        if filename.endswith("wav"):
            if filename.startswith('background'):
                background = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                backgrounds.append(background)
            elif filename.startswith('shi'):
                activate = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                activates.append(activate)
            elif filename.startswith('sha'):
                negative = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                negatives.append(negative)
            elif filename.startswith('jon'):
                negative = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                negatives.append(negative)
    return activates, negatives, backgrounds