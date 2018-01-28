#!/bin/sh

MELCHIADES_PATH=/home/pi/workspaces/melchiades
SERVICE_ACCOUNT_FILENAME=$MELCHIADES_PATH/MarvellousMelchiades3000-9e8f5cf8371a.json

# Requires: USB Mic (configure recording volume through alsamixer)

# Pygame is available by default on a clean Raspberry Pi installation. No need to do anything here.

# Install requests through userland installation of pipenv
# requests is an easy-to-use API to make HTTP requests
# PyAudio for recording stuff
sudo apt-get install -y python3-requests python3-pyaudio

# Install Google Cloud SDK (taken from https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
# Create an environment variable for the correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install -y google-cloud-sdk

# Configure access to Google Speech API as described in 
# https://cloud.google.com/speech/docs/quickstart
# https://cloud.google.com/docs/authentication/getting-started
export GOOGLE_APPLICATION_CREDENTIALS=$SERVICE_ACCOUNT_FILENAME

gcloud init
gcloud auth application-default login
gcloud auth activate-service-account --key-file=$SERVICE_ACCOUNT_FILENAME
sudo pip3 install --upgrade google-cloud-speech

# Make sure you have authenticated to Google. This provisioning doesn't cover getting an API key

sudo pip3 install giphy_client

# Neither covers getting a Giphy API. You will have to get one and put it at [melchiades-path]/giphy_key.txt

# Pillow is part of the default RPi installation (maybe?) PIL is guaranteed
# sudo pip3 install Pillow

# Why not trei your webcam before dispairing?
sudo apt-get install fswebcam
# fswebcam -d /dev/video0 -r 640x480 test.jpg

# Font: Mortified by Walter E Stewart

# sudo pip3 install pyserial
# pySerial already part of Raspi install
