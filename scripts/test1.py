from colr import color


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
