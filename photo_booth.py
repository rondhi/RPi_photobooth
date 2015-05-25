#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess
import os, sys
import datetime

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 12
GPIO.setup(SWITCH, GPIO.IN)
REPRINT = 16
GPIO.setup(REPRINT, GPIO.IN)
PRINT_LED = 18
POSE_LED = 23
BUTTON_LED = 19
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

while True:
        if (GPIO.input(SWITCH)):
                snap = 1
                while snap < 5:
                        print("pose!")
                        GPIO.output(BUTTON_LED, False)
                        GPIO.output(POSE_LED, True)
                        time.sleep(1)
                        for i in range(2):
                                GPIO.output(POSE_LED, False)
                                time.sleep(0.3)
                                GPIO.output(POSE_LED, True)
                                time.sleep(0.3)
                        for i in range(5):
                                GPIO.output(POSE_LED, False)
                                time.sleep(0.1)
                                GPIO.output(POSE_LED, True)
                                time.sleep(0.1)
                        GPIO.output(POSE_LED, False)
                        print("SNAP")
                        dt = str(time.strftime("%Y-%m-%d_%H%M%S"))
                        last_photo_taken = "/home/pi/temp/snap_%s_%s.jpg" % (snap, dt)
                        take_photo_command = "gphoto2 --capture-image-and-download --filename " + last_photo_taken
                        gpout = subprocess.check_output(take_photo_command, stderr=subprocess.STDOUT, shell=True)
                        print(gpout)
                        if "ERROR" not in gpout: 
                                snap += 1
                        GPIO.output(POSE_LED, False)
                        time.sleep(0.5)
                print("please wait while your photos print...")
                GPIO.output(PRINT_LED, True)
                # build image and send to printer
                subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
                # Wait to ensure that print queue doesn't pile up
                # TODO: check status of printer instead of using this arbitrary wait time
                #time.sleep(110)
                print("ready for next round")
                GPIO.output(PRINT_LED, False)
                GPIO.output(BUTTON_LED, True)
                time.sleep(1)
        if (GPIO.input(REPRINT)):
                gpout = subprocess.check_output("lp /home/pi/reprint.jpg", stderr=subprocess.STDOUT, shell=True)
                print(gpout)
                time.sleep(1)
