import os

from pydub import AudioSegment
import librosa
import numpy as np

def graph_spectrogram(wav_file, minus=True, nfft=2048, hop=512):
    rate, data = get_wav_info(wav_file)
    fs = rate # frequency
    
    S = librosa.feature.melspectrogram(data, sr=fs, n_mels=128, n_fft=nfft, hop_length=hop)
    log_S = librosa.power_to_db(S, ref=np.max)
    if not minus:
        return log_S
    
    data_minus = -data
    S_minus = librosa.feature.melspectrogram(data_minus, sr=fs, n_mels=128, n_fft=nfft, hop_length=hop)
    log_S_minus = librosa.power_to_db(S_minus, ref=np.max)
    return log_S, log_S_minus

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
            elif filename.startswith('negative'):
                negative = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                if len(negative) < 1000:
                    negatives.append(negative)
            else:
                activate = AudioSegment.from_wav(os.path.join(audio_dir, filename))
                activates.append(activate)
    return activates, negatives, backgrounds

def make_beep_wav(wav, y, output_name):
    beep, _ = librosa.load('./data/beep.wav', sr = 44100)
    data, _ = librosa.load(wav, sr=44100)
    length = y.shape[0]
    for i in range(1, length):
        tmp = int(len(data)*(i)/length)
        t_1 = y[i-1]
        t = y[i]
        if (t_1 == 0) and (t == 1):
            if tmp > 22000 :
                data[tmp-22000:tmp] =  beep[:22000]*0.5
            else:
                data[:tmp] =  beep[:tmp]*0.5
    librosa.output.write_wav(output_name, data, sr=44100)

def output_postprocessing(outputs, th):
    for output in outputs:
        output[output<th] = 0
        output[output>=th] = 1
    return outputs
