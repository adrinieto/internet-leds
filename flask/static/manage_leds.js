function change_led_state(id, state) {
    console.log("Changing led" + id + " status to " + state + "...");
    $.ajax({
        url: "/api/leds/" + id,
        type: 'PUT',
        contentType: "application/json",
        data: JSON.stringify({state: state}),
        success: function (result) {
            if (state != result.state) {
                // get the toggle instance for this checkbox
                var toggle = $("#" + result.id).data('bs.toggle');
                // change toggle state without calling the listener
                if (result.state) {
                    toggle.on(true);
                } else {
                    toggle.off(true);
                }
            }
        }
    })
}