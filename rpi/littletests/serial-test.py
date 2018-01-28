#!/usr/bin/env python3

import serial

ser = serial.Serial("/dev/serial/by-id/usb-Arduino_Srl_Arduino_Mega_754313433343510140C1-if00", 9600)
while True:
        print("Read: " + ser.readline().decode('ascii').strip())

