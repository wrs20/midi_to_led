
import mido
from pitch import pitch
import led

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
        
        channels = set()
        for msgx in self.midi:
            if msgx.type in ('note_on', 'note_off'):
                p = pitch[msgx.note]
                pitch_max = max(pitch_max, p)
                pitch_min = min(pitch_min, p)
                if not msgx.channel in channels:
                    channels = channels.union({msgx.channel})
        
        self.pitch_max = pitch_max
        self.pitch_min = pitch_min
        self.length = self.midi.length
        self.channels = channels

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
        return self.note_to_ledspec[note]

if __name__ == '__main__':
    import sys
    mf = MidiFile(sys.argv[1])
    ld = led.TermLed(5)
    mm = MapMidiNotes(mf, ld)
    print(mm.note_to_ledcolour)
    print(mf.length)
    print(mf.channels)




