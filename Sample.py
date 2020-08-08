
import numpy as np
import AudioStream as audio

class SampleList():
    def __init__(self):
        self.sample_list = []

    def add_sample(self, note, data):
        self.sample_list.append(Sample(True, note, data))

    def get_sample(self, note):
        for samp in self.sample_list:
            if samp.note == note:
                return samp.DataArray
        return np.zeros(audio.buffersize, dtype=np.int16)



class Sample():
    def __init__(self, stereo, note, data):
        self.stereo = stereo
        self.note = note
        self.DataArray = data








