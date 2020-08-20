
import numpy as np
import AudioStream as audio
from fractions import Fraction
from scipy import signal
import time

class SampleList():
    def __init__(self):
        self.sample_list = []
        self.times = []  # timing diagnostic

    def add_sample(self, note, data):
        self.sample_list.append(Sample(True, note, data))

    def get_sample(self, note):
        for samp in self.sample_list:
            if samp.note == note:
                return samp
        return None

    def fill_out_pitches(self):
        # TODO: Not currently filling out bottom pitches. Also C# is missing
        max_shift = 12
        # fill original pitches list.
        og_pitches = []
        for samp in self.sample_list:
            og_pitches.append(samp.note)
        og_pitches.sort()
        print(og_pitches)

        time_list = []
        # create list of shifts and which note to shift
        max = 0
        for index in range(0, len(og_pitches)):
            t1 = time.time()
            # calculate min shift for this note
            if index == 0:
                min = og_pitches[index] - max_shift
            elif max > og_pitches[index]-max_shift:
                min = max
            else:
                min = og_pitches[index]-max_shift

            # calculate max shift for this note
            max_index = len(og_pitches)-1
            if index == max_index:
                max = og_pitches[index] + max_shift
            else:
                max = og_pitches[index+1] - og_pitches[index]
                max = round(max/2) + og_pitches[index]
                if max > og_pitches[index]+max_shift:
                    print("Max = ", max)
                    max = og_pitches[index]+max_shift
            print("Index: ", index, "Min shift: ", min, "Max shift: ", max)
            t2 = time.time()
            tl = []
            # pitchshift this note
            for new_note in range(min, max):
                if new_note != og_pitches[index]:
                    t3 = time.time()
                    self.pitch_shift(og_pitches[index], new_note)
                    print("Done pitch shifting note ", new_note, " Times list: ", self.times)
                    tl.append(time.time()-t3)
            time_list.append([t1, t2, tl])
        #print("Time List: \n", time_list)

    def pitch_shift(self, og_note, shifted_note):
        # Get original Sample and note/freq
        og_sample = self.get_sample(og_note)
        shift_sample = Sample(True, shifted_note, [0])

        # get shift amount (I, D)
        f0 = og_sample.freq()
        f1 = shift_sample.freq()
        frac = Fraction(round(f0*1000), round(f1*1000))
        I = frac.numerator
        D = frac.denominator
        #print("I: ", I," D: ", D)


        # Split into left and right signals
        L_signal, R_signal = og_sample.split_LR()

        # Interpolate and decimate
        t1 = time.time()
        shifted_L = signal.resample_poly(L_signal, I, D)
        t2 = time.time()
        shifted_R = signal.resample_poly(R_signal, I, D)
        t3 = time.time()
        #signal.resample(L_signal, I, D)
        t4 = time.time()
        #xsignal.resample(R_signal, I, D)
        t5 = time.time()
        self.times.append(t2-t1)
        self.times.append(t3-t2)
        self.times.append(t4-t3)
        self.times.append(t5-t4)

        shifted_L = shifted_L.astype('int16')
        shifted_R = shifted_R.astype('int16')

        # Merge left and right signals
        merged_signal = shift_sample.merge_LR(shifted_L, shifted_R)

        # create new sample and append to list
        shift_sample.signal = merged_signal
        self.sample_list.append(shift_sample)


    def freq(note):
        # TODO: need to add comments about what frequency/ midi notes etc.
        n = note - 21
        return 27.5 * 2 ** (n / 12)


    def plot_freq(self, note):
        import matplotlib.pyplot as plt
        T = 1/44100

        samp = self.get_sample(note)
        left, right = samp.split_LR()
        # create time array
        t = []
        for ele in range(0, len(left)):
            t.append(ele)
        ''' DFT '''
        Xf = np.fft.fft(left)
        freqs = np.fft.fftfreq(len(left), T)

        ''' Plot '''
        fig, axs = plt.subplots(2)
        axs[0].plot(t, left)
        axs[1].plot(freqs, np.abs(Xf))
        axs[1].set_yscale('log')
        axs[1].set_xscale('log')
        axs[1].set_xlim(10,20000)
        plt.show()



class Sample():
    def __init__(self, stereo, note, data):
        self.stereo = stereo
        self.note = note
        self.signal = data

    def freq(self):
        n = self.note - 21
        return 27.5 * 2 ** (n / 12)

    def split_LR(self):
        L = self.signal[0::2]
        R = self.signal[1::2]
        return L, R

    def merge_LR(self, L, R):
        merge = np.empty(L.size + R.size, dtype=L.dtype)
        merge[0::2] = L
        merge[1::2] = R
        return merge









