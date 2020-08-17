"""
Voice and VoiceList classes.


Written by Jared Snapp
"""
# Future to do: Need to add voice stealing.  Will need to keep track of which sample has been playing the longest.
# Possible restructure: Could have two lists, one with used voices and the other with unused voices. Then would move
# the voice back and forth between both lists. Would make finding an unused voice easy.  For voice stealing could
# just take the index 0 in the used list. Would need to pop and re append that voice.

import numpy as np
# TODO: use python error handling to handle errors in this class.

# TODO: Voice class will be identified by note. Update VoiceList.
class VoiceList:
    def __init__(self, voice_count, buffersize):
        self.buffersize = buffersize
        self.voice_count = voice_count
        self.voice_list = []
        for i in range(0, voice_count):
            self.voice_list.append(Voice(False, self.buffersize))

    def get_voice(self, sample, volume):
        for voice in self.voice_list:
            if voice.active == False:
                voice.use(sample, volume)
                return True
        return False

    def mix(self):
        data = np.zeros(self.buffersize*2, dtype=np.int16)
        for voice in self.voice_list:
            if voice.active:
                data2 = voice.next_frame()
                if len(data2) == self.buffersize*2:
                    data = data + data2
                else:
                    print("Error: data2 is small", len(data2))
        return data

    def note_off(self, note):
        for voice in self.voice_list:
            if voice.note == note and voice.note_on:
                voice.note_on = False



class Voice:
    def __init__(self, active, buffersize):
        self.active = active
        self.index = 0
        self.buffer_size = buffersize
        self.sample = None
        self.signal = None
        self.note = None
        self.volume = 0
        self.note_on = False
        # TODO: Voice class will be identified by the note. Add note data.

    def increment(self):
        #TODO: add in handling if index is out of range
        self.index = self.index+2*self.buffer_size

    def next_frame(self):
        # Get next frame
        data = self.signal[self.index:self.index + self.buffer_size * 2]
        # Apply envelope
        data = self.envelope(data)

        # check if at end of sample
        if len(data) < self.buffer_size*2:
            data = np.append(data, np.zeros((self.buffer_size * 2) - len(data), dtype=np.int16))
            self.active = False
        if self.active:
            self.increment()
        return data

    def use(self, sample, volume):
        #TODO: Add in check for if voice is already in use.  Don't use if it is.
        self.index = 0
        self.volume = volume
        self.sample = sample
        self.signal = self.sample.signal
        self.note = self.sample.note
        self.active = True
        self.note_on = True
        self.note_off_index = 0
        self.decay_rate = -0.9/44100

    def envelope(self, data):
        # Volume and decay / sustain
        # It is necessary to calculate factor before multiplying array. Otherwise array might overflow and clip
        output = (self.volume/127)*data
        output = output.astype('int16')
        if self.note_on == False:
            left = output[0::2]
            right = output[1::2]
            decay = []
            for index in range(0, left.size):
                # generate decay envelope x = 0.9x + 1
                decay_step = self.decay_rate * self.note_off_index + 1
                if decay_step <= 0:
                    decay_step = 0
                decay.append(decay_step)
                self.note_off_index += 1
            if decay_step == 0:
                self.active = False
            decay = np.array(decay)
            left = left*decay
            right = right*decay
            merged = np.empty(left.size + right.size, dtype='int16')
            merged[0::2] = left
            merged[1::2] = right
            output = merged.astype('int16')
        return output


