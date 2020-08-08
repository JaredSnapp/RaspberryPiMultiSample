
''' Scan through folder and open all the wav files. Create an array of the data with all the notes in it.
Fill the missing notes with pitch shifted versions of the existing ones.'''



''' Create a audio stream using PyAudio.  Move data to stream in 4-8 sample sections?  
Keep less than 4 ms (~22us per sample). Have a class of audio data ready to fill with audio data and 
add to the stream.'''

'''
class Voice:
    dataPresent = 0  # flag to tell loop whether to process this voice
    data = []  # contains actual audio data


#initialize things
import_data()
start_stream()
init_voices()


while True:
    ServiceMidi()
    ServiceVoices()
    ServiceEffects()

'''
import Voice as vc
import Sample
import importdata as id
import AudioStream as audio
import numpy as np
import Midi as md
import time

Voices = vc.VoiceList(16, audio.buffersize)

id.import_data()
new_note = 1
run = True
times = []
count = 0
# start audio stream
audio.startstream()
print("Init done.")
while run:

    new_note = md.service_midi()
    if new_note != -1:
        #print(new_note)
        # TODO: may have multiple new notes
        Voices.get_voice(id.Samples.get_sample(new_note))
        #print(id.Sample_List[0].DataArray)
        new_note = -1
        count += 1
        if count > 50:
            break

    if audio.datasent:
        # move new data to buffer
        t1 = time.time()
        audio.outputbuffer = Voices.mix()
        #print(audio.outputbuffer)
        audio.datasent = False
        times.append(t1)

tdiff = []
prevt = 0
for t in times:
    tdiff.append(t-prevt)
    prevt = t
print(tdiff)

# stop audio stream
audio.stopstream()

# for sample in voices:
    # if sample has audio
        # add sample to mix

#send mix to audio stream