"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import numpy as np
from importdata import convert_wav_to_np
import time
import sys

'''if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)'''
file = "Piano - C2.wav"
file2 = "Piano - G2.wav"
file3 = "Piano - D3.wav"
wf = wave.open(file, 'rb')
wf2 = wave.open(file2, 'rb')
wf3 = wave.open(file3, 'rb')
#TODO: need to normalize sample length. add zeros to make it divisible by buffer size
C2 = convert_wav_to_np(wf)
G2 = convert_wav_to_np(wf2)
D3 = convert_wav_to_np(wf3)

buffersize = 256

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

index = 0
index2 = 0
outputbuffer = np.array(0)
datasent=1
# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global datasent
    global index2
    #data = wf.readframes(frame_count)

    data = outputbuffer.tobytes()
    datasent = 1
    #print("call")
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                frames_per_buffer=buffersize,
                stream_callback=callback)

print("format ", p.get_format_from_width(wf.getsampwidth()))
print("channels ", wf.getnchannels())
print("rate ", wf.getframerate())

# start the stream (4)
if datasent == 1:
    outputbuffer = C2[index:index+buffersize*2]
    index += buffersize*2
    datasent = 0

stream.start_stream()
index3 = 0
t = []
# wait for stream to finish (5)
while stream.is_active():
    if datasent == 1:
        t0 = time.time()
        #outputbuffer = np.zeros(buffersize*2, dtype=int)
        outputbuffer = C2[index:index + buffersize*2]
        if index > 20000:
            outputbuffer = C2[index:index + buffersize*2] + G2[index2:index2 + buffersize*2]
            if index >200000:
                outputbuffer = C2[index:index + buffersize * 2] + G2[index2:index2 + buffersize * 2] \
                               + D3[index3:index3 + buffersize * 2]
                index3 += buffersize*2
            index2 += buffersize*2
        index += buffersize*2
        datasent = 0
        if index > 400000:
            outputbuffer = outputbuffer = np.zeros(buffersize*2, dtype=int)
        t1 = time.time()
        t.append(t1-t0)
    #time.sleep(0.00001)

print("time: ", sum(t)/float(len(t)))

print("C2: ", C2[100:120])
print("C2 + 0: ", C2[100:120]+np.zeros(20))


# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
