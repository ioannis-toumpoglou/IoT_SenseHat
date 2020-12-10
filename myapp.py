from flask import Flask, render_template, request, session, g, url_for, redirect
from sense_emu import SenseHat
import random

users = []
users.append([1, 'John', '01234'])
users.append([2, 'Maria', '56789'])

s = SenseHat()
s.clear(0,0,0)

app = Flask(__name__)
app.secret_key = "12345"


@app.route('/')
def home_page():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('index.html')


@app.route('/logme', methods=['POST','GET'])
def logme():
    session.pop('user_id', None)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user[1] == username and user[2] == password:
                session['user_id'] = user[0]
                return redirect(url_for('home_page'))
    return render_template('login.html')


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        for user in users:
            if user[0] == session['user_id']:
                g.user = user
                g.s = s


@app.context_processor
def a_processor():
    def roundv(value, digits):
        return round(value, digits)
    return {'roundv': roundv}


@app.route('/sense', methods=['POST','GET'])
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('sense.html')


@app.route('/ships', methods=['POST','GET'])
def ships():
    if not g.user:
        return redirect(url_for('logme'))

    green = [0,200,0]
    black = [0,0,0]
    blue = [0,0,255]
    shipmap = [green]*10 + [black]*54
    random.shuffle(shipmap)

    if request.method == 'POST':
        horizontal = int(request.form['horizontal'])
        vertical = int(request.form['vertical'])

        if horizontal > 7:
            random.shuffle(shipmap)
            s.set_pixels(shipmap)
        elif vertical > 7:
            pass
        else:
            s.set_pixel(horizontal, vertical, blue)

    return render_template('ships.html')


# always at the end of the code

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
