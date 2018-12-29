from flask import Flask, render_template, request

from subprocess import PIPE, Popen

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_uptime():
    return check_output_wrapper(('uptime',))

def check_output_wrapper(cmd):
    r = ''
    rc = None
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        rc = p.communicate()
    except Exception as e:
        r += str(e)
        if rc is not None:
            r += rc[0].decode('utf-8') + rc[1].decode('utf-8')

    if p.returncode != 0:
        r = str(p.returncode) + '\n' + rc[0].decode('utf-8') + '\n' + rc[1].decode('utf-8')
    elif rc is not None:
        r = rc[0].decode('utf-8')
    else:
        r = 'Something is broken.'
    return r

# assumes the following in /etc/sudoers
"""
pi ALL=NOPASSWD: /sbin/halt, /sbin/reboot, /sbin/poweroff
"""

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    stdout = ''
    if request.method == 'POST':
        print(request)

        #if request.form.get('clear_print_queue') == 'Clear Print Queue':
        #    # pass
        #    print("Clear Queue")
        #    stdout = 'Error: not implemented.'
        #elif  request.form.get('reboot_pi') == 'Reboot Pi':
        #    print("Reboot pi")
        #    # assuming that this user can execute 'sudo reboot' without password
        #    stdout = check_output_wrapper(('sudo', 'reboot'),)
        #elif  request.form.get('shutdown_pi') == 'Shutdown Pi':
        #    # assuming that this user can execute 'sudo poweroff' without password
        #    print("shutdown pi")
        #    stdout = check_output_wrapper(('sudo', 'poweroff'),)

        return render_template("index.html",uptime=get_uptime(), stdout=stdout)

    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return render_template("index.html")


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8080)
