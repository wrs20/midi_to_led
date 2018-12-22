from midi_to_led import led_events

import time

eq = led_events.EventQueue()

eq.put(
    led_events.Event(time.time() + 5, print, ('a', 'b'))
)
eq.start()


