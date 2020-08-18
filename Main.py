
''' Scan through folder and open all the wav files. Create an array of the data with all the notes in it.
Fill the missing notes with pitch shifted versions of the existing ones.'''



''' Create a audio stream using PyAudio.  Move data to stream in 4-8 sample sections?  
Keep less than 4 ms (~22us per sample). Have a class of audio data ready to fill with audio data and 
add to the stream.'''


import Voice as vc
import importdata as id
import AudioStream as audio
from Midi import MidiQueue
import time



run = True
times = []

# Initialize
Voices = vc.VoiceList(32, audio.buffersize)
print("Importing data")
id.import_data()
md = MidiQueue()

# start audio stream
audio.startstream()
print("Initialized")

while run:

    t4 = time.time()
    midi_event = md.service_midi()
    if midi_event is not None:
        if midi_event.note_on:
            #print(" Note:", midi_event.note, "Note On ", " velocity:", midi_event.velocity)
            samp = id.Samples.get_sample(midi_event.note)
            if samp != None:
                #print("Getting Voice")
                result = Voices.get_voice(samp, midi_event.velocity)
                if result == False:
                    print("No Voices")
            else:
                print("No sample")
        if midi_event.note_off:
            #print(" Note:", midi_event.note, "Note Off", " velocity:", midi_event.velocity)
            Voices.note_off(midi_event.note)
        if midi_event.sustain_on:
            Voices.sustain_on()
        if midi_event.sustain_off:
            Voices.sustain_off()

    # TODO: release notes

    if audio.datasent:
        # move new data to buffer
        t1 = time.time()
        audio.outputbuffer = Voices.mix()
        #print(audio.outputbuffer)
        audio.datasent = False
        times.append(t1)
    t5 = time.time()
    #print("Loop time: ", t5-t4)

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