from time import sleep
import time


class _Led:
    spi = None
    ledstart = [0x00, 0x00, 0x00, 0x00]
    ledstop = [0xff, 0xff, 0xff, 0xff]
    ledlist = []
    allledsoff = [0xe0, 0x00, 0x00, 0x00]

    brightnessOff = [0xe0]
    brightnessDim = [0xe1]
    brightnessFull = [0xff]

    def __init__(self, ledCount):

        import spidev
        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)
        self.spi.max_speed_hz = 1000000
        # sets all leds to OFF
        for i in range(ledCount):
            self.ledlist.append(self.allledsoff)
        self.led_count = ledCount

    def set(self, led, r, g, b, brightness):
        self.ledlist[led] = [0xE0 | brightness, b, g, r]
        self.refresh()

    def setAll(self, r, g, b, brightness):
        for i in range(len(self.ledlist)):
            self.ledlist[i] = [0xE0 | brightness, b, g, r]
        self.refresh()

    def refresh(self):
        ledsetup = self.ledstart[:]
        for i in range(len(self.ledlist)):
            ledsetup += self.ledlist[i]
        ledsetup += self.ledstop
        self.spi.xfer(ledsetup)


class TermLed:
    """
    Represents leds in terminal using coloured blocks.
    24b colour terminal reccomended.
    """
    
    def __init__(self, led_count):
        from colr import color
        class _led:
            def __init__(self):
                self.colour = [0,0,0,0]
            def __call__(self, *args):
                self.colour = args
            def __repr__(self):
                b = self.colour[3] / 255
                c = (
                    int(self.colour[0] * b),
                    int(self.colour[1] * b),
                    int(self.colour[2] * b)
                )
                return color(u"\u2588", fore=c, style='bright')

        self.led_count = led_count
        self.ledlist = [_led() for lx in range(led_count)]

    def set(self, led, r, g, b, brightness):
        self.ledlist[led](r, g, b, brightness)
        self.refresh()

    def setAll(self, r, g, b, brightness):
        for led in self.ledlist:
            led(r, g, b, brightness)

    def refresh(self):
        s = '\r' + ''.join([str(lx) for lx in self.ledlist])
        print(s, sep='', end='    ', flush=True) 


try:
    # assuming spidev is only importable on an rpi with LEDs
    import spidev
    Led = _Led
    
    # turn off leds on ctrl+c
    import signal
    import sys    
    def _TURN_OFF_ALL_LEDS(sig=None, frame=None):
        lx = Led(5)
        lx.setAll(0,0,0,0)

        # bodge to make this function usable with atexit
        if sig is not None:
            sys.exit(0)
    
    signal.signal(signal.SIGINT, _TURN_OFF_ALL_LEDS)

    # turn off all leds on python exit
    import atexit
    atexit.register(_TURN_OFF_ALL_LEDS)

except Exception as e:
    print("Cannot use real LEDs, using terminal.")
    Led = TermLed


if __name__ == '__main__':

    tl = Led(5)

    b = 0

    while True:
        sleep(0.1)
        tl.set(0, 255, 0, 0, b)
        tl.set(1, 0, 255, 0, b)
        tl.set(2, 0, 0, 255, b)
        tl.set(3, 255, 128, 0, b)
        tl.set(4, 255, 0, 128, b)       
        b += 1
        b %= 255


