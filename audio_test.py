# coding:utf-8

import pygame.mixer
from time import sleep

pygame.mixer.init()
pygame.mixer.music.load("start.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(1)
sleep(1)
pygame.mixer.music.load("alert.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
sleep(10)
pygame.mixer.music.stop()
sleep(1)
pygame.mixer.music.load("stop.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(1)
