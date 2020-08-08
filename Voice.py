import numpy as np
# TODO: use python error handling to handle errors in this class.


class VoiceList():
    def __init__(self, voice_count, buffersize):
        self.buffersize = buffersize
        self.voice_count = voice_count
        self.voice_list = []
        for i in range(0, voice_count):
            self.voice_list.append(Voice(False, self.buffersize))

    def get_voice(self, data):
        for voice in self.voice_list:
            if voice.active == False:
                voice.use(data)
                return

    def mix(self):
        data = np.zeros(self.buffersize*2, dtype=np.int16)
        for voice in self.voice_list:
            if voice.active:
                data2 = voice.next_frame()
                if len(data2) == self.buffersize*2:
                    data = data + data2
                else:
                    print("Error: data2 is small", len(data2))
                #print(data2)
        return data


class Voice():
    def __init__(self, active, buffersize, data=np.array(0)):
        self.active = active
        self.index = 0
        self.buffersize = buffersize
        self.DataArray = data  # TODO: make zeros of buffersize

    def increment(self):
        #TODO: add in handling if index is out of range
        self.index = self.index+2*self.buffersize

    def frame(self):
        #TODO: add in handling for when data doesn't fill buffersize. Append 0s to the end and turn off active
        return self.DataArray[self.index:self.index+self.buffersize*2]

    def next_frame(self):
        #TODO: what to do if frame() turns off active? don't increment?
        data = self.frame()
        if len(data) < self.buffersize*2:
            #print("Data Short: ",len(data))
            data = np.append(data, np.zeros((self.buffersize*2)-len(data), dtype=np.int16))
            #print("Fixed: ", len(data))
            self.active = False
        if self.active:
            self.increment()
        return data

    def use(self, data):
        #TODO: Add in check for if voice is already in use.  Don't use if it is.
        self.index = 0
        self.DataArray = data
        self.active = True


