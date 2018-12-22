from colr import color
from time import sleep

class TermLed:
    
    def __init__(self, led_count):

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

    def refresh(self):
        s = '\r' + ''.join([str(lx) for lx in self.ledlist])
        print(s, sep='', end='    ', flush=True) 



if __name__ == '__main__':

    tl = TermLed(5)


    b = 0

    while True:
        sleep(0.01)
        tl.set(0, 255, 0, 0, b)
        tl.set(1, 0, 255, 0, b)
        tl.set(2, 0, 0, 255, b)
        tl.set(3, 255, 128, 0, b)
        tl.set(4, 255, 0, 128, b)       
        b += 10
        b %= 255


