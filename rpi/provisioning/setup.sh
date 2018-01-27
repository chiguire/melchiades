#!/bin/sh

# Requires: USB Mic (configure recording volume through alsamixer)

# Pygame is available by default on a clean Raspberry Pi installation. No need to do anything here.

# Install requests through userland installation of pipenv
# requests is an easy-to-use API to make HTTP requests
# PyAudio for recording stuff
sudo apt-get install -y python3-requests python3-pyaudio
