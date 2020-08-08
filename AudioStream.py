"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import time
import numpy as np
import time


framerate = 44100
channels = 2
buffersize = 512
outputbuffer = np.array(0)
datasent=True

# TODO: Must be a better way to do this.  Make a class?
stream = 0
p = 0

def startstream():
    global stream
    global p
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # setup output buffer
    outputbuffer = np.array(0)
    datasent=True

    # open stream using callback (3)
    stream = p.open(format=p.get_format_from_width(2),
                    channels=channels,
                    rate=framerate,
                    output=True,
                    frames_per_buffer=buffersize,
                    stream_callback=callback)

    # start the stream (4)
    stream.start_stream()


# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global datasent
    data = outputbuffer.tobytes()
    datasent = True
    return (data, pyaudio.paContinue)

'''
times = []
count = 0
# wait for stream to finish (5)
while stream.is_active():
    if datasent:
        times.append(time.time())
        outputbuffer = np.zeros(512, dtype=int)
        datasent = False
        count += 1
        if count > 100:
            break
    #time.sleep(0.00001)

#doesn't work
print("time: ", sum(times)/float(len(times)))
print(times)
prevt = 0
for t in times:
    print(t-prevt)
    prevt = t
'''
def stopstream():
    # stop stream (6)
    stream.stop_stream()
    stream.close()

    # close PyAudio (7)
    p.terminate()
