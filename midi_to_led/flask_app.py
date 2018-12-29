from flask import Flask, render_template, request
from led import Led


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



curr_keys = (
    'rr0', 'gg0', 'bb0', 'br0',
    'rr1', 'gg1', 'bb1', 'br1',
    'rr2', 'gg2', 'bb2', 'br2',
    'rr3', 'gg3', 'bb3', 'br3',
    'rr4', 'gg4', 'bb4', 'br4',
)





curr_vals = (
    '0', '0', '0', '0',
    '0', '0', '0', '0',
    '0', '0', '0', '0',
    '0', '0', '0', '0',
    '0', '0', '0', '0',
)


curr_state = dict()

def reset_state():
    for kx, vx in zip(curr_keys, curr_vals):
        curr_state[kx] = vx

reset_state()

globalled = Led(5)
def update_leds():
    globalled.set(4, int(curr_state['rr0']), int(curr_state['gg0']), int(curr_state['bb0']), int(curr_state['br0']))
    globalled.set(3, int(curr_state['rr1']), int(curr_state['gg1']), int(curr_state['bb1']), int(curr_state['br1']))
    globalled.set(2, int(curr_state['rr2']), int(curr_state['gg2']), int(curr_state['bb2']), int(curr_state['br2']))
    globalled.set(1, int(curr_state['rr3']), int(curr_state['gg3']), int(curr_state['bb3']), int(curr_state['br3']))
    globalled.set(0, int(curr_state['rr4']), int(curr_state['gg4']), int(curr_state['bb4']), int(curr_state['br4']))

update_leds()



@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    stdout = ''
    if request.method == 'POST':
        print(request)
        print(request.form)
        
        if request.form.get('reset_leds') == 'Reset':
            reset_state()

        elif request.form.get('update_leds') == 'Update LEDs':
            for kx in curr_keys:
                curr_state[kx] = request.form[kx]

        update_leds()

        return render_template("index.html", **curr_state)

    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return render_template("index.html", **curr_state)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8080)
