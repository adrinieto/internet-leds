function change_led_state(id, state) {
    console.log("Changing led" + id + " status to " + state + "...");
    $.ajax({
        url: "/api/leds/" + id,
        type: 'PUT',
        contentType: "application/json",
        data: JSON.stringify({state: state}),
        success: function (result) {
            if (result.state == true) {
                $("#" + result.id).removeClass("power_on")
                    .addClass("power_off")
                    .html("Power Off")
                    .off('click').on('click', function () {
                        change_led_state($(this).attr("id"), false)
                    })
            } else {
                $("#" + result.id).removeClass("power_off")
                    .addClass("power_on")
                    .html("Power On")
                    .off('click').on('click', function () {
                        change_led_state($(this).attr("id"), true)
                    })
            }
        }
    })
}