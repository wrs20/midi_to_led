
import mido


class MidiFile:
    def __init__(self, filename):
        self.filename = filename
        self.midi = mido.MidiFile(filename)
        
        notes = []
        for trackx in self.midi.tracks:
            for msgx in trackx:
                if msgx.type == 'note_on':
                    notes.append(msgx)
        
        self.notes = notes

if __name__ == '__main__':
    import sys
    mf = MidiFile(sys.argv[1])




