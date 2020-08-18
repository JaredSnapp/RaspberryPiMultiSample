import numpy as np
import wave
import Sample as smp

Sample_List = []
Samples = smp.SampleList()

def convert_wav_to_np(wf):
    samples = wf.getnframes()
    audio = wf.readframes(samples)

    # Convert buffer to float32 using NumPy
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)

    return audio_as_np_int16


def import_data():
    # make list of wav files in folder
    file = "Piano - C2.wav"
    file2 = "Piano - G2.wav"
    file3 = "Piano - D3.wav"

    # open wav files
    wf = wave.open(file, 'rb')
    wf2 = wave.open(file2, 'rb')
    wf3 = wave.open(file3, 'rb')

    #print(wf.getsampwidth())

    # convert to np arrays
    C2 = convert_wav_to_np(wf)
    G2 = convert_wav_to_np(wf2)
    D3 = convert_wav_to_np(wf3)

    Samples.add_sample(48, C2)
    Samples.add_sample(55, G2)
    Samples.add_sample(62, D3)

    Samples.fill_out_pitches()

'''
    Samples.pitch_shift(24, 25)
    Samples.pitch_shift(24, 26)
    Samples.pitch_shift(24, 27)
    Samples.pitch_shift(24, 28)
    Samples.pitch_shift(24, 29)
    Samples.pitch_shift(24, 30)
    #Samples.pitch_shift(24, 31)
    Samples.pitch_shift(24, 32)
    Samples.pitch_shift(24, 33)
    Samples.pitch_shift(24, 34)
    Samples.pitch_shift(24, 35)
    Samples.pitch_shift(24, 36)
    Samples.pitch_shift(24, 60)
'''

    #Samples.plot_freq(24)
    #Samples.plot_freq(25)

    # read in wav files into Samples class (numpy arrays and metadata). Parse file names for note names (eg G2)
    # create pitch shifted versions of Samples to fill keyboard



