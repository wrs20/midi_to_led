from flask import Flask, render_template, request, send_from_directory, send_file
from led import Led
import cv2
from time import sleep, time
import io

app = Flask(__name__, static_url_path='/')
app.config['TEMPLATES_AUTO_RELOAD'] = True

from threading import Thread, Lock


curr_keys = (
    'rr0', 'gg0', 'bb0', 'br0',
    'rr1', 'gg1', 'bb1', 'br1',
    'rr2', 'gg2', 'bb2', 'br2',
    'rr3', 'gg3', 'bb3', 'br3',
    'rr4', 'gg4', 'bb4', 'br4',
)


curr_vals = (
    '0', '0', '0', '10',
    '0', '0', '0', '10',
    '0', '0', '0', '10',
    '0', '0', '0', '10',
    '0', '0', '0', '10',
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

camera = cv2.VideoCapture(0)
while not camera.isOpened():
    sleep(1)
    camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

def get_cap():
    return_value, image = camera.read()
    # cv2.imwrite('templates/cap.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    cv2.imwrite('/dev/shm/cap.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])



cap_bytes = None
cap_lock = Lock()

def get_cap_bytes():
    _, image = camera.read()
    _, jpg_bytes = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    global cap_bytes
    
    cap_lock.acquire()
    cap_bytes = io.BytesIO(jpg_bytes)
    cap_lock.release()
    

get_cap_bytes()

last_cap_rq = time()

def continuous_cap():
    global last_cap_rq
    while(1):
        get_cap_bytes()
        if time() - last_cap_rq > 5:
            reset_state()
            update_leds()
            last_cap_rq = time()
        


gthread = Thread(target=continuous_cap)
gthread.start()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/cap.jpg')
def send_cap():
    #get_cap_bytes()
    cap_lock.acquire()
    send_buf = io.BytesIO(cap_bytes.getbuffer())
    cap_lock.release()
    r = send_file(send_buf, attachment_filename='cap.jpg', mimetype='image/jpg')

    global last_cap_rq
    last_cap_rq = time()

    return r
    #return send_from_directory('templates', 'cap.jpg')


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
        #get_cap()

        return render_template("index.html", **curr_state)

    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return render_template("index.html", **curr_state)


app.debug = False
app.run(host='0.0.0.0', port=8080)


