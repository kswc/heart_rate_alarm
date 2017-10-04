# coding:utf-8

import sys
import pygame.mixer
from time import sleep
from heart_rate_monitor import HeartRateMonitor

class HeartRateAlarm:

    def __init__(self, alarm_heart_rate_min = 40, alarm_heart_rate_max = 180):
        self.alarm_heart_rate_min = alarm_heart_rate_min
        self.alarm_heart_rate_max = alarm_heart_rate_max
        self.alarm_now = False

        self.monitor = HeartRateMonitor(self.check_heart_rate)
        print("monitor start")
        self.monitor.start()
        print("monitor listening")

        pygame.mixer.init()
        pygame.mixer.music.load("start.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(1)

    def check_heart_rate(self, hr):
        if(hr < self.alarm_heart_rate_min or self.alarm_heart_rate_max < hr):
            sys.stdout.write("%d! " % hr)
            sys.stdout.flush()
            if(not self.alarm_now):
                sys.stdout.write("alarm on. ")
                self.alarm_now = True
                pygame.mixer.music.load("alert.mp3")
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)
        else:
            sys.stdout.write("%d " % hr)
            sys.stdout.flush()
            if(self.alarm_now):
                sys.stdout.write("alarm off. ")
                self.alarm_now = False
                pygame.mixer.music.stop()

    def stop(self):
        self.alarm_now = False
        print("monitor stop")
        self.monitor.stop()
        pygame.mixer.music.load("stop.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(1)
        pygame.mixer.music.stop()


if __name__ == '__main__':
    alarm_heart_rate_min = 60
    alarm_heart_rate_max = 80
    alarm = HeartRateAlarm(alarm_heart_rate_min, alarm_heart_rate_max)
    print("press Ctrl-C to stop this script.")

    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            alarm.stop()
            sys.exit(0)
