import mido
from led import Led



class RealtimeLed:
    def __init__(self, ledset):
        self.ledset = ledset
        self._notes_on = {}

    def _ledrefresh(self):
        print(self._notes_on)
    
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
    rtled = RealtimeLed(ledset)




    for msg in inport:
        rtled(msg)
        outport.send(msg)




