

class ColourMap:
    def __init__(self, rf, gf, bf):
        # where rf, gf and bf map [0,1] onto [0,1]
        self.rf = rf
        self.gf = gf
        self.bf = bf

    def __call__(self, a, b, x):
        r = b - a
        x = (x - a) / r
        rv = self.rf(x)
        gv = self.gf(x)
        bv = self.bf(x)
        assert rv >= 0 and rv <= 1.0
        assert gv >= 0 and gv <= 1.0
        assert bv >= 0 and bv <= 1.0
        return (int(255 * rv), int(255 * gv), int(255 * bv))


class ConstVal:
    def __init__(self, intensity=1.0):
        self.i = intensity
    def __call__(self, x):
        return self.i


def _linear(a, fa, b, fb, x):
    r = float(b - a)
    g = float(fb - fa) / r
    return g * float(x) + fa


def cyan_to_magenta(a, b, x):
    return (
        int(255 * _linear(0, 0, 1, 1, x)),
        int(150 * _linear(0, 1, 1, 0, x)),
        100
    )

def red_to_green(a, b, x):
    return (
        int(255 * _linear(0, 0, 1, 1, x)),
        int(255 * _linear(0, 1, 1, 0, x)),
        0
    )

def warm_white(a, b, x):
    return (255, 140, 60)

