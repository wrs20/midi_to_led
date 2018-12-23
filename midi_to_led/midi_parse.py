
import mido
from pitch import pitch
import led
from math import ceil
import numpy as np
from ctypes import c_uint8 as UINT8
from numpy_playback import NumpyPlayback

class MidiNote:
    def __init__(self, channel, note, velocity, start_time, end_time=None):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = end_time

    def make_end_time(self):
        if self.end_time is None:
            self.end_time = self.start_time + 0.1
    
    def __repr__(self):
        return '{} {} {} {} {}'.format(
            self.channel, self.note, self.velocity, self.start_time, self.end_time
        )

class MidiFile:
    def __init__(self, filename):
        self.filename = filename
        self.midi = mido.MidiFile(filename)
        
        pitch_max = 0.0
        pitch_min = 999999.0
        velocity_max = 0
        
        channels = set()
        for msgx in self.midi:
            if msgx.type in ('note_on', 'note_off'):
                p = pitch[msgx.note]
                pitch_max = max(pitch_max, p)
                pitch_min = min(pitch_min, p)
                if not msgx.channel in channels:
                    channels = channels.union({msgx.channel})
                
                velocity_max = max(velocity_max, msgx.velocity)
        
        self.pitch_max = pitch_max
        self.pitch_min = pitch_min
        self.length = self.midi.length
        self.channels = channels
        self.velocity_max = velocity_max

        note_channels = {}
        
        for chx in channels:
            note_channels[chx] = {}
        
        notes = []

        curr_time = 0.0
        for msgx in self.midi:
            curr_time += msgx.time
            if msgx.type == 'note_on':
                chl = note_channels[msgx.channel]
                note = msgx.note
                new_note = MidiNote(
                    msgx.channel, note, msgx.velocity, curr_time, None
                )
                if note in chl.keys(): chl[note].append(new_note)
                else: chl[note] = [new_note]

            elif msgx.type == 'note_off':
                chl = note_channels[msgx.channel]
                note = msgx.note
                assert note in chl.keys()
                off_note = chl[note].pop()
                off_note.end_time = curr_time
                notes.append(off_note)

        # give end times to notes that the midi never spec'd end times
        # for
        for chx in note_channels:
            chl = note_channels[chx]
            for notex in chl.keys():
                for nx in chl[notex]:
                    nx.make_end_time()
                    notes.append(nx)
        
        self.notes = notes

class MapMidiNotes:
    """
    Map midi notes onto leds and colours
    """
    def __init__(self, midifile, ledset):
        self.midifile = midifile
        self.ledset = ledset
        
        bin_width = (self.midifile.pitch_max - self.midifile.pitch_min) / self.ledset.led_count

        note_to_ledcolour = []
        for nx in range(128):
            freq = pitch[nx]
            if freq < self.midifile.pitch_min or freq > self.midifile.pitch_max:
                note_to_ledcolour.append(None)
            else:
                ld = int((freq - self.midifile.pitch_min) / bin_width)
                ld = max(0, ld)
                ld = min(ld, self.ledset.led_count - 1)

                # colour map goes here, start with white
                note_to_ledcolour.append((ld, (255, 255, 255)))

        self.note_to_ledcolour = tuple(note_to_ledcolour)

    def __call__(self, note):
        return self.note_to_ledcolour[note]


class RenderNotes:
    def __init__(self, midi_file, midi_map, vel_func, rate=30):
        self.rate = rate
        self.period = 1.0 / rate
        self.midi = midi_file
        self.map = midi_map
        self.led_count = midi_map.ledset.led_count
        self.vel_func = vel_func

        self.num_frames = int(ceil(self.midi.length / self.period))
        self.data = np.zeros((self.num_frames, self.led_count, 4), dtype=UINT8)

        for note in self.midi.notes:
            s = self._time_to_frame(note.start_time)
            e = self._time_to_frame(note.end_time)
            l = self.map(note.note)
            v = self._scale_velocity(note.velocity)
            b = self._get_brightness(s, e, v)
            data = np.zeros((e - s, 4), dtype=UINT8)
            data[:, 0] = l[1][0]
            data[:, 1] = l[1][1]
            data[:, 2] = l[1][2]
            data[:, 3] = b
            self._combine(s, e, l[0], data)
    
    def _combine(self, start, end, led, data):
        o = self.data[start:end:, led, :].view()
        np.bitwise_or(o, data, out=o)

    def _scale_velocity(self, v):
        v = int((v/self.midi.velocity_max) * 255)
        v = max(v, 0)
        return min(v, 255)

    def _get_brightness(self, sf, ef, v):
        nf = ef - sf
        ff = np.zeros(nf, dtype=UINT8)
        st = 0.0
        et = self._frame_to_time(nf)
        for fx in range(nf):
            b = self.vel_func(st, et, v, self._frame_to_time(fx))
            b = max(0, b)
            b = min(255, b)
            ff[fx] = b
        ff[-1] = 0
        return ff

    def _time_to_frame(self, t):
        b = int(t / self.period)
        b = max(0, b)
        return min(b, self.num_frames - 1)

    def _frame_to_time(self, f): return self.period * f

    
def linear_decay(s, e, v, t):
    return (-1.0 * v / (e-s)) * t + v


if __name__ == '__main__':
    import sys
    mf = MidiFile(sys.argv[1])
    ld = led.Led(5)
    mm = MapMidiNotes(mf, ld)
    rn = RenderNotes(mf, mm, linear_decay)
    pb = NumpyPlayback(ld, rn.rate, rn.data)
    rate = pb()
    print(rn.rate, rate, "{: 2.1f}%".format(100.* (rate/rn.rate)))







