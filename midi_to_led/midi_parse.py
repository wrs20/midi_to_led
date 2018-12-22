
import mido
from pitch import pitch
import led

class MidiFile:
    def __init__(self, filename):
        self.filename = filename
        self.midi = mido.MidiFile(filename)
        
        pitch_max = 0.0
        pitch_min = 999999.0
        for trackx in self.midi.tracks:
            for msgx in trackx:
                if msgx.type == 'note_on':
                    p = pitch[msgx.note]
                    pitch_max = max(pitch_max, p)
                    pitch_min = min(pitch_min, p)
        
        self.pitch_max = pitch_max
        self.pitch_min = pitch_min


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




