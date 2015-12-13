Internet Leds
=============
A small example of how to control leds with and API written in Python-Flask with an interface to Arduino.

The web client uses sockets to communicate with the server and with other clients.
It also has an API (`http:/localhost:5000/api`) to consult the leds statuses and update their state.