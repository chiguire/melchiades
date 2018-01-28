# melchiades
The Marvellous Melchiades 3000 software. Made for the Global Game Jam 2018

Made by: Yole Quintero and Ciro Durán

The code you see in this Global Game Jam package is what was committed to our repo at https://github.com/chiguire/melchiades, under the tag 'ggj18'.

## Hardware requirements

* Arduino Mega - A sketch is provided. See pin definitions for an idea of where to connect what
* Raspberry Pi - A script in Python is ran, which connects to the Arduino and outputs to the screen display.
* Lots of LEDs
* Two Neopixel strips (3 and 7 long respectively)
* A servo
* 4 Force Sensing Resistors
* A webcam
* An ultrasonic distance sensor

## API Requirements

The game extensively uses publicly available Internet APIs to work. The API keys are not provided in this repository, you can obtain these freely by yourself.

* Google Speech API - Use the free tier of Google Cloud API to access this API. Follow the instructions to log in from your Pi.
* Giphy API - It is way easier to obtain an API key for this. Put it in the same directory as the README.md.

## File structure

* arduino - Sketches made for the Arduino.
* rpi - Python scripts for the game.
* rpi/provisioning - A shell script that installs and lists the Python script dependencies. It wasn't tested, more like we were adding dependencies as they came.
* rpi/littletests - Running these should provide sanity checks that separate parts run.

## What does this game do?

See a demonstration at https://youtu.be/wHjRDhshu2Y

The idea of the game is to run a show at the event's show&tell. We are hiring for operators of The Marvellous Melchiades 3000, a machine that is able to speak to spirits. A person who wants to know their future stands in front of the machine, presses a button and speaks their question loudly. The machine will then display what the spirits have interpreted their question as, and then will say their fate, through the display and through the various dials and lights.

it is up to the operator to read this output and give a convincing interpretation to the customer.

The audience will vote whether the interpreter was convincing or not.

