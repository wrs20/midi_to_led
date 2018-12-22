from colr import color






class TermLed:
    
    def __init__(self, led_count):

        class _led:
            def __init__(self):
                self.colour = [0,0,0,0]
            def __call__(self, *args):
                self.colour = args
            def __repr__(self):
                return color(u"\u2588", fore=self.colour[0:3:], style='bright')

        self.led_count = led_count
        self.ledlist = [_led() for lx in range(led_count)]

    def set(self, led, r, g, b, brightness):
        self.ledlist[led](r, g, b, brightness)
        self.refresh()

    def refresh(self):
        s = ''.join([str(lx) for lx in self.ledlist])
        print("----")
        print(s, sep='', end='\r', flush=True) 

if __name__ == '__main__':

    tl = TermLed(5)
    tl.set(0, 255, 0, 0, 255)
    tl.set(0, 0, 255, 0, 255)
    tl.set(0, 0, 0, 255, 255)
    tl.set(0, 255, 128, 0, 255)
    tl.set(0, 255, 0, 128, 255)

    while True:
        pass

    quit()
    while True:
        print(
            color(u"\u2588", fore=(0, 0, 0), style='bright'), 
            color(u"\u2588", fore=(255, 0, 0), style='bright'), 
            color(u"\u2588", fore=(0, 255, 0), style='bright'), 
            color(u"\u2588", fore=(0, 0, 255), style='bright'), 
            sep='', 
            end='\r', 
            flush=True
        )
