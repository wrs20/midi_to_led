import mido









if __name__ == '__main__':
    devs = mido.get_input_names()
    dev = None
    for dx in devs:
        if dx.startswith('LPK25'):
            dev = dx
            break
    assert dev is not None, "Could not find LPK25."
    inport = mido.open_input(dev)
    print(inport)
    for msg in inport:
        print(msg)


