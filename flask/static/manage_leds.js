function change_led_state(id, state) {
    console.log("Changing led" + id + " status to " + state + "...");
    $.ajax({
        url: "/api/leds/" + id,
        type: 'PUT',
        contentType: "application/json",
        data: JSON.stringify({state: state}),
        success: function (result) {
            if (state != result.state) {
                $("#" + result.id).prop('checked', result.state).change();
            }
        }
    })
}