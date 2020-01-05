import os
import numpy as np
from td_utils import graph_spectrogram

def get_random_time_segment(segment_ms, total_ms=10000.0):
    segment_start = np.random.randint(low=0, high=total_ms-segment_ms)   # Make sure segment doesn't run past the 10sec background 
    segment_end = segment_start + segment_ms - 1

    return (segment_start, segment_end)

def is_overlapping(segment_time, previous_segments):
    segment_start, segment_end = segment_time
    overlap = False

    for previous_start, previous_end in previous_segments:
        if segment_start <= previous_end and segment_end >= previous_start:
            overlap = True

    return overlap

def insert_audio_clip(background, audio_clip, previous_segments):
    total_ms = len(background)
    segment_ms = len(audio_clip)
    segment_time = get_random_time_segment(segment_ms, total_ms)

    count = 0 
    while is_overlapping(segment_time, previous_segments):
        segment_time = get_random_time_segment(segment_ms, total_ms)
        count += 1
        if count > 50 :
            return background, None

    previous_segments.append(segment_time)
    new_background = background.overlay(audio_clip, position = segment_time[0])
    
    return new_background, segment_time

def insert_ones(y, segment_time, total_ms=10000.0):
    Ty = y.shape[1]
    segment_end_y = int(segment_time[1] * Ty / total_ms)
    segment_len = int((segment_time[1]-segment_time[0]) * Ty / total_ms)
    for i in range(segment_end_y + 1, segment_end_y + segment_len + 1):
        if i < Ty:
            y[0, i] = 1
    return y

def create_training_data(background, activates, negatives, filename, kernel=15, stride=4):
    background.export('./data/tmp.wav', format="wav")
    mel = graph_spectrogram('./data/tmp.wav', minus=False)
    Ty = int((mel.shape[1]-kernel)/stride + 1)

    y = np.zeros((1, Ty))
    total_ms = len(background)
    previous_segments = []
    input_ms = 0

    while((input_ms/total_ms)<0.5):
        number_of_activates = np.random.randint(0, 4)
        random_indices = np.random.randint(len(activates), size=number_of_activates)
        random_activates = [activates[i] for i in random_indices]
        
        for random_activate in random_activates:
            random_activate += np.random.randint(-2,5)
            background, segment_time = insert_audio_clip(background, random_activate, previous_segments)
            if segment_time is not None:
#                 print('active')
                segment_start, segment_end = segment_time
                input_ms += (segment_end - segment_start)
                y = insert_ones(y, segment_time=segment_time, total_ms=total_ms)

        number_of_negatives = np.random.randint(0, 4)
        random_indices = np.random.randint(len(negatives), size=number_of_negatives)
        random_negatives = [negatives[i] for i in random_indices]

        for random_negative in random_negatives:
            random_negative += np.random.randint(-2,5)
            background, segment_time = insert_audio_clip(background, random_negative, previous_segments)
            if segment_time is not None:
#                 print('negative')
                segment_start, segment_end = segment_time
                input_ms += (segment_end - segment_start)
                
    file_handle = background.export(filename, format="wav")
    x, x_minus = graph_spectrogram(filename)
    return x, x_minus, y
