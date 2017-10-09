# coding:utf-8

import RPi.GPIO as GPIO
from time import sleep

def event_callback(gpio_pin):
    print("GPIO[%d] callback" % gpio_pin)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(13, GPIO.RISING, callback=event_callback, bouncetime=2000)

for var in range(0, 20):
    GPIO.output(21, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(21, GPIO.LOW)
    sleep(0.5)

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print '\nbreak'
    GPIO.remove_event_detect(13)
    GPIO.cleanup()
