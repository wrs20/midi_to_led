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
        bt = int((brightness / 255) * 31)
        self.ledlist[led] = [0xE0 | bt, b, g, r]
        self.refresh()

    def setAll(self, r, g, b, brightness):
        bt = int((brightness / 255) * 31)
        for i in range(len(self.ledlist)):
            self.ledlist[i] = [0xE0 | bt, b, g, r]
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
    
    if len(sys.argv[:]) == 1:
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
    else:

            off = [0, 0, 0, 0]
            white = [255, 255, 255, 255]
            red = [255, 0, 0, 255]
            orange = [255, 64, 0, 255]
            yellow = [255, 255, 0, 255]
            lime = [0, 255, 64, 255]
            green = [0, 255, 0, 255]
            mint = [0, 255, 64, 255]
            cyan = [0, 255, 255, 255]

            blue = [0, 0, 255, 255]
            purple = [64, 0, 255, 255]
            magenta = [255, 0, 255, 255]
            pink = [255, 0, 64, 255]

            colour = [0, 0, 0, 0]

            if len(sys.argv) == 2:
                if sys.argv[1] == "white":
                    colour = white
                elif sys.argv[1] == "red":
                    colour = red
                elif sys.argv[1] == "orange":
                    colour = orange
                elif sys.argv[1] == "yellow":
                    colour = yellow
                elif sys.argv[1] == "lime":
                    colour = lime
                elif sys.argv[1] == "green":
                    colour = green
                elif sys.argv[1] == "mint":
                    colour = mint
                elif sys.argv[1] == "cyan":
                    colour = cyan
                elif sys.argv[1] == "blue":
                    colour = blue
                elif sys.argv[1] == "purple":
                    colour = purple
                elif sys.argv[1] == "magenta":
                    colour = magenta
                elif sys.argv[1] == "pink":
                    colour = pink
                else:
                    colour = off
                    
            elif len(sys.argv) == 5:
                for i in range(1, 5):
                    colour[i - 1] = int(sys.argv[i])
            else:
                print("Arg Error")
                quit()
            
            tl.setAll(colour[0], colour[1], colour[2], colour[3])
            a = input("Press the any key to quit\n")




