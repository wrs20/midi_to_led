
from led import *
import numpy as np
import sys
from ctypes import c_uint8 as UINT8
from time import time

class NumpyPlayback:
    def __init__(self, ledset, rate, data):
        self.ledset = ledset
        self.rate = rate
        self.data = data
        self.period = 1.0/rate
        assert data.shape[1] == ledset.led_count


    def __call__(self):
        num_frames = self.data.shape[0]
        num_leds = self.data.shape[1]
        ledsetfunc = self.ledset.set
        
        t0 = time()
        for framex in range(num_frames):
            next_time = time() + self.period
            for ledx in range(num_leds):
                d = self.data[framex, ledx, :]
                ledsetfunc(ledx, int(d[0]), int(d[1]), int(d[2]), int(d[3]))

            while time() < next_time:
                pass
        t1 = time()
        return num_frames / (t1 - t0)


if __name__ == '__main__':
    
    
    nl = 5
    nf = 120
    data = np.zeros((nf, nl, 4), dtype=UINT8)

    for fx in range(nf):
        data[fx, :, :] = np.random.randint(low=0, high=255, size=(nl,4))

    
    l0 = Led(nl)
    p0 = NumpyPlayback(l0, 120, data)
    arate = p0()
    print("\n", arate)



