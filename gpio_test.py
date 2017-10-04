# coding:utf-8
#http://robocad.blog.jp/archives/678444.html

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

GPIO.output(21, GPIO.HIGH)
sleep(1)
GPIO.output(21, GPIO.LOW)
sleep(1)
GPIO.output(21, GPIO.HIGH)
sleep(1)
GPIO.output(21, GPIO.LOW)
sleep(1)
GPIO.output(21, GPIO.HIGH)
sleep(1)
GPIO.output(21, GPIO.LOW)
sleep(1)

GPIO.cleanup() 


#https://www.hackster.io/glowascii/raspberry-pi-shutdown-restart-button-d5fd07

print "callback test"

def event_callback(gpio_pin):
    print("GPIO[%d] callback" % gpio_pin)

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(13, GPIO.RISING, callback=event_callback, bouncetime=2000)

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print '\nbreak'
    GPIO.remove_event_detect(13)
    GPIO.cleanup()



