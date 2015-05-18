#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess
import os, sys
import Image

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 26
GPIO.setup(SWITCH, GPIO.IN)
REPRINT = 19
GPIO.setup(REPRINT, GPIO.IN)
RESET = 13
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 24
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

while True:
        if (GPIO.input(SWITCH)):
                snap = 0
                while snap < 4:
                        print("pose!")
                        GPIO.output(BUTTON_LED, False)
                        GPIO.output(POSE_LED, True)
                        time.sleep(1)
                        for i in range(1):
                                GPIO.output(POSE_LED, False)
                                time.sleep(0.4)
                                GPIO.output(POSE_LED, True)
                                time.sleep(0.4)
                        for i in range(5):
                                GPIO.output(POSE_LED, False)
                                time.sleep(0.1)
                                GPIO.output(POSE_LED, True)
                                time.sleep(0.1)
                        GPIO.output(POSE_LED, False)
                        print("SNAP")
                        gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth_%s_%Y-%m-%d-%H%M%S.jpg" % (snap), stderr=subprocess.STDOUT, shell=True)
                        print(gpout)
                        if "ERROR" not in gpout: 
                                snap += 1
                        GPIO.output(POSE_LED, False)
                        time.sleep(0.5)
                print("please wait while your photos print...")
                GPIO.output(PRINT_LED, True)
                # build image and send to printer
                subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
                # TODO: implement a reboot button
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
        #if (GPIO.input(RESET)):
                #gpout = subprocess.check_output("sudo reboot", stderr=subprocess.STDOUT, shell=True)
                #print(gpout)
                #time.sleep(1)