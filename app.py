from arduino import Arduino
from flask import Flask, jsonify, request, abort, make_response, render_template

app = Flask(__name__)
arduino = Arduino()


@app.route('/')
def index():
    return render_template('index.html', leds=arduino.leds)


@app.route('/api/leds')
def get_leds():
    return jsonify({'leds': arduino.leds})


@app.route('/api/leds/<int:led_id>')
def get_led(led_id):
    led = [led for led in arduino.leds if led['id'] == led_id]
    if len(led) == 0:
        abort(404)
    return jsonify({'led': led[0]})


@app.route('/api/leds/<int:led_id>', methods=['PUT'])
def set_led_state(led_id):
    led = [led for led in arduino.leds if led['id'] == led_id]
    if len(led) == 0 or not request.json:
        abort(404)
    if 'state' not in request.json or type(request.json['state']) is not bool:
        abort(400)
    arduino.write_led_state(led_id, request.json['state'])
    led[0]['state'] = request.json['state']
    return jsonify(led[0])


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, host='0.0.0.0')  # Allow access from Internet
