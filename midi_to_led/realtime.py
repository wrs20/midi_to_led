import mido
from led import Led
import sys
import numpy as np
from ctypes import c_uint8 as UINT8

class RealtimeLed:
    def __init__(self, ledset, max_brightness=10):
        self.ledset = ledset
        self._notes_on = {}
        self._mb = max_brightness
        self.leds_on = np.zeros((self.ledset.led_count, 4), dtype=UINT8)

    def _ledrefresh(self):
        print(self._notes_on)
        
        should_be_on = set()
        self.leds_on.fill(0)

        for nx in self._notes_on.keys():
            l = nx % 5  # simple map onto leds
            c = np.array((255, 0, 0, self._mb), dtype=UINT8)
            np.maximum(c, self.leds_on[l, :], self.leds_on[l, :])
        
        for lx in range(self.ledset.led_count):
            t = self.leds_on[lx, :]
            self.ledset.set(lx, int(t[0]), int(t[1]), int(t[2]), int(t[3]))

    
    def __call__(self, msg):
        print(msg)
        if msg.type == 'note_on':
            self._notes_on[msg.note] = msg.velocity
        
        elif msg.type == 'note_off':
            if msg.note in self._notes_on.keys():
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




