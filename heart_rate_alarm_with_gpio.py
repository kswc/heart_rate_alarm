# coding:utf-8

import os
import sys
import time
import pygame.mixer
import multiprocessing
import RPi.GPIO as GPIO
from time import sleep
from heart_rate_monitor import HeartRateMonitor

class HeartRateAlarm:

    def __init__(self, alarm_heart_rate_min=40, alarm_heart_rate_max=180):
        self.alarm_heart_rate_min = alarm_heart_rate_min
        self.alarm_heart_rate_max = alarm_heart_rate_max
        self.alarm_now = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(13, GPIO.RISING, callback=self.stop_and_shutdown, bouncetime=200)

        self.led = LEDBlinker()
        self.shared_heart_rate = multiprocessing.Value('i', 0)
        self.shared_heart_rate_update_time = multiprocessing.Value('d', 0)
        self.led_process = multiprocessing.Process(target=self.led.blink_with_bpm, args=(self.shared_heart_rate, self.shared_heart_rate_update_time))
        self.led_process.start()

        self.monitor = HeartRateMonitor(self.check_heart_rate)
        print("monitor start")
        self.monitor.start()
        print("monitor listening")
        self.led.start()

        pygame.mixer.init()
        pygame.mixer.music.load("start.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(1)

    def check_heart_rate(self, hr):
        if self.alarm_heart_rate_min <= hr <= self.alarm_heart_rate_max:
            sys.stdout.write("%d " % hr)
            sys.stdout.flush()
            if self.alarm_now:
                sys.stdout.write("alarm off. ")
                self.alarm_now = False
                pygame.mixer.music.stop()
        else:
            sys.stdout.write("%d! " % hr)
            sys.stdout.flush()
            if not self.alarm_now:
                sys.stdout.write("alarm on. ")
                self.alarm_now = True
                pygame.mixer.music.load("alert.mp3")
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)
        self.shared_heart_rate.value = hr
        self.shared_heart_rate_update_time.value = time.time()

    def stop(self):
        self.alarm_now = False
        print("monitor stop")
        self.monitor.stop()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("stop.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(1)
        sleep(1)
        self.shared_heart_rate.value = 0
        self.led_process.terminate()
        self.led.stop()
        GPIO.cleanup() 

    def stop_and_shutdown(self, gpio_pin):
        print("GPIO[%d] callback" % gpio_pin)
        if gpio_pin != 13:
            return
        self.stop()
        sleep(1)
        print("sudo shutdown -h now")
        #sys.exit(0)
        os.system("sudo shutdown -h now")


class LEDBlinker:

    def __init__(self):
        pass

    def start(self):
        for var in range(0, 20):
            GPIO.output(21, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(21, GPIO.LOW)
            sleep(0.1)

    def blink_with_bpm(self, bpm, update_time):
        while True:
            temp_bpm = bpm.value
            if update_time.value < time.time() - 3:
                GPIO.output(21, GPIO.HIGH)
                sleep(1)
            elif temp_bpm == 0:
                GPIO.output(21, GPIO.LOW)
                sleep(1)
            else:
                GPIO.output(21, GPIO.HIGH)
                sleep(60.0 / temp_bpm / 2)
                GPIO.output(21, GPIO.LOW)
                sleep(60.0 / temp_bpm / 2)

    def stop(self):
        for var in range(0, 10):
            GPIO.output(21, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(21, GPIO.LOW)
            sleep(0.1)


if __name__ == '__main__':
    alarm_heart_rate_min = 40
    alarm_heart_rate_max = 150
    alarm = HeartRateAlarm(alarm_heart_rate_min, alarm_heart_rate_max)
    print("press Ctrl-C to stop this script.")

    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            alarm.stop()
            sys.exit(0)
