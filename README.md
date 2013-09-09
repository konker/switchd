Switchd
==============================================================================

A Python daemon which monitors a hardware power switch for the Raspberry Pi,
  and performs a clean system shutdown when activated.

Designed for the Mausberry Circuits [Illuminated LED shutdown switch](http://mausberry-circuits.myshopify.com/products/illuminated-led-shutdown-switch)

## Dependencies
    - see requirements.txt
        - RPi.GPIO
        - pyev
        - python-daemon

## Configuration
config/switchd.json holds the configuration.

* GPIO_in: GPIO pin to which you have attached the wire marked "OUT" on the switch.
* GPIO_out: GPIO pin to which you have attached the wire marked "IN" on the switch.
* command: The command to execute when the switch has been depressed for 2 seconds.

## Installation
An init.d script is provided for automatic starting of the daemon. See etc/README.

## Alternatives
You could also just use the mausberry curcuits shell script as described here:
[http://mausberry-circuits.myshopify.com/pages/setup](http://mausberry-circuits.myshopify.com/pages/setup)

## License
See LICENCE

