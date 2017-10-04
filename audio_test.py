# coding:utf-8

import pygame.mixer
from time import sleep

pygame.mixer.init()
pygame.mixer.music.load("alert.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
sleep(10)
pygame.mixer.music.stop()

