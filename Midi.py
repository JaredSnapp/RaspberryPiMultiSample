#!/usr/bin/env python
"""
List available ports.
This is a simple version of mido-ports.
"""
'''
from __future__ import print_function
import mido

def print_ports(heading, port_names):
    print(heading)
    for name in port_names:
        print("    '{}'".format(name))
    print()


print()
print_ports('Input Ports:', mido.get_input_names())
print_ports('Output Ports:', mido.get_output_names())
'''

import mido

class MidiQueue:
    def __init__(self):
        self.queue = []
        self.inport = mido.open_input('Arturia KeyStep 32')

    def service_midi(self):
        self.service_midi_port()
        return self.service_queue()

    def service_midi_port(self):
        msg = None
        for msg in self.inport.iter_pending():
            #print("Midi: ", msg)
            if msg.type == 'note_on':
                print("Note On: ", msg.note)
                self.add_event(msg.note, note_on=True, velocity=msg.velocity)
            if msg.type == 'note_off':
                print("Note Off: ", msg.note)
                self.add_event(msg.note, note_off=True)

    def add_event(self, note, note_on=False, note_off=False, velocity=0):
        # TODO: need to check if there is already an event in the queue for this note.
        # there shouldn't be two note_on's in a list without a note_off.  Is this a possible error? Already handled by
        # midi queue.
        event = MidiEvent(note, note_on, note_off, velocity)
        self.queue.append(event)

    def service_queue(self):
        if len(self.queue) >= 1:
            # Return queue[0] and remove it from list:
            return self.queue.pop(0)
        else:
            # return None if there is nothing in the queue
            return None


class MidiEvent:
    def __init__(self, note, note_on=False, note_off=False, velocity=0):
        self.note = note
        self.note_on = note_on
        self.note_off = note_off
        self.velocity = velocity
