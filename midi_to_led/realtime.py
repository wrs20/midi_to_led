import mido
from led import Led
import sys


class RealtimeLed:
    def __init__(self, ledset, max_brightness=10):
        self.ledset = ledset
        self._notes_on = {}
        self._leds_on = set()
        self._mb = max_brightness


    def _ledrefresh(self):
        print(self._notes_on)
        
        should_be_on = set()

        for nx in self._notes_on.keys():
            l = nx % 5  # simple map onto leds
            self.ledset.set(l, 255, 0, 0, self._mb)

            should_be_on = should_be_on.union(set((l,)))
            self._leds_on = self._leds_on.union(set((l,)))

        turn_off = self._leds_on.difference(should_be_on)
        for l in turn_off:
            self.ledset.set(l, 0, 0, 0, 0)

    
    def __call__(self, msg):
        print(msg)
        if msg.type == 'note_on':
            self._notes_on[msg.note] = msg.velocity
        
        elif msg.type == 'note_off':
            del self._notes_on[msg.note]

        self._ledrefresh()



if __name__ == '__main__':
    # get input port
    devs = mido.get_input_names()
    dev = None
    for dx in devs:
        if dx.startswith('LPK25'):
            dev = dx
            break
    assert dev is not None, "Could not find LPK25."
    inport = mido.open_input(dev)
    print(inport)


    # get output port
    devs = mido.get_output_names()
    dev = None
    for dx in devs:
        if dx.startswith('FLUID'):
            dev = dx
            break
    assert dev is not None, "Could not find a fluidsynth output"
    outport = mido.open_output(dev)
    print(outport)

    
    # make led rendering objects
    ledset = Led(5)
    if len(sys.argv) > 1: bt = int(sys.argv[1])
    else: bt = 10

    rtled = RealtimeLed(ledset, bt)




    for msg in inport:
        rtled(msg)
        outport.send(msg)




