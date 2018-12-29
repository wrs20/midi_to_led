import mido
from led import Led
import sys
import numpy as np
from ctypes import c_uint8 as UINT8
from colour_map import *

class _BaseMap:
    def __init__(self, ledset, max_brightness):
        self.ledset = ledset
        self.mb = max_brightness
        self.init_colour_map()

    def init_colour_map(self):
        pass

    def __call__(self, note, velocity):
        l = note % self.ledset.led_count
        c = np.array((255, 0, 0, 9), dtype=UINT8)
        b = np.zeros((self.ledset.led_count, 4), dtype=UINT8)
        b[l, :] = c
        return b


class RedLedMap(_BaseMap):
    pass


class ThreeBumpLedMap(_BaseMap):

    def __call__(self, note, velocity):
        lc = self.ledset.led_count
        b = np.zeros((self.ledset.led_count, 4), dtype=UINT8)
        
        l = note % 12
        l = (l / 11.) * 4
        l = int(l)
        l %= 5
        l = 4 - l
        
        p = note % 12
        # c = cyan_to_magenta(0.0, 11.0, float(p)/11.0)
        c = red_to_green(0.0, 11.0, float(p)/11.0)
        print(l, p, c)
        
        for ox, bx in zip((-1, 0, 1),
                (
                    int(30),
                    int(self.mb), 
                    int(30)
                )
            ):

            l2 = l + ox
            if l2 >= 0 and l2 < lc:
                b[l2, 0:3:] = c
                b[l2,3] = bx

        return b





class RealtimeLed:
    def __init__(self, ledset, rtledmap):
        self.ledset = ledset
        self._notes_on = {}
        self.m = rtledmap
        self.leds_on = np.zeros((self.ledset.led_count, 4), dtype=UINT8)

    def _ledrefresh(self):
        
        should_be_on = set()
        self.leds_on.fill(0)

        for nx in self._notes_on.keys():
            c = self.m(nx, self._notes_on[nx])
            np.maximum(c, self.leds_on[:], self.leds_on[:])
        
        for lx in range(self.ledset.led_count):
            t = self.leds_on[lx, :]
            self.ledset.set(lx, int(t[0]), int(t[1]), int(t[2]), int(t[3]))

    
    def __call__(self, msg):
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
    if len(sys.argv) > 1: mb = int(sys.argv[1])
    else: mb = 10

    ledset = Led(5)
    # rtmap = RedLedMap(ledset, mb)
    rtmap = ThreeBumpLedMap(ledset, mb)
    rtled = RealtimeLed(ledset, rtmap)




    for msg in inport:
        rtled(msg)
        outport.send(msg)




