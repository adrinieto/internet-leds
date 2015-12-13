var socket = null;

function startSocket() {
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        $('.led_toggle').bootstrapToggle('enable');
        $('#connection_status').removeClass('alert-danger').removeClass('alert-info').addClass('alert-success');
        $('#connection_status p').text("Connected");

    });
    socket.on('disconnect', function () {
        $('.led_toggle').bootstrapToggle('disable');
        $('#connection_status').removeClass('alert-success').addClass('alert-danger');
        $('#connection_status p').text("Lost connection to server. Trying to connect...");
    });

    socket.on('led_state', function (msg) {
        for (var i in msg.leds) {
            var led = msg.leds[i];
            // get the toggle instance for this checkbox
            var toggle = $("#" + led.id).data('bs.toggle');
            // change toggle state without calling the listener
            if (led.state) {
                toggle.on(true);
            } else {
                toggle.off(true);
            }
        }
    })

    socket.on('log', function (msg) {
        $('#log').prepend('<p>' + msg.msg + '<\p>');
    })
}

function change_led_state(id, state) {
    console.log("Changing led" + id + " status to " + state + "...");
    socket.emit('set_led_state', {id: parseInt(id), state: state});
}