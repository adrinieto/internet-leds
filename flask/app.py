from datetime import datetime
from pprint import pprint
from flask import Flask, jsonify, request, abort, make_response, render_template
from flask_socketio import SocketIO
from arduino import Arduino

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

arduino = Arduino("COM4")


@socketio.on('connect')
def handle_connect():
    print('Client connected!')
    socketio.emit('led_state', {'leds': arduino.leds})


@socketio.on('disconnect')
def handle_connect():
    print('Client disconnected!')


@socketio.on('set_led_state')
def handle_set_led_state(message):
    arduino.set_led_state(message['id'], message['state'])
    socketio.emit('led_state', {'leds': arduino.leds})

    now = datetime.now()
    msg = "[%s] %s changed led %s to %s" % (
    now, request.remote_addr, message['id'], 'ON' if message['state'] else 'OFF')
    socketio.emit('log', {'msg': msg})


@app.route('/')
def index():
    return render_template('index.html', leds=arduino.leds)


@app.route('/api/leds')
def get_leds():
    return jsonify({'leds': arduino.leds})


@app.route('/api/leds/<int:led_id>')
def get_led(led_id):
    led = [led for led in arduino.leds if led['id'] == led_id]
    if not led:
        abort(404)
    return jsonify({'led': led[0]})


@app.route('/api/leds/<int:led_id>', methods=['PUT'])
def set_led_state(led_id):
    led = [led for led in arduino.leds if led['id'] == led_id]
    if not led or not request.json:
        abort(404)
    if 'state' not in request.json or type(request.json['state']) is not bool:
        abort(400)
    arduino.set_led_state(led_id, request.json['state'])
    socketio.emit('led_state', {'leds': arduino.leds})
    return jsonify(led[0])


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # socketio.run(app, debug=False, host='0.0.0.0')  # Allow access from Internet
