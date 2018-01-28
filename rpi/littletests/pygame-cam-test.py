#!/usr/bin/env python3

# NOTE: Does not work with Logitech Notebook Deluxe :-(
import sys, pygame
from pygame.locals import *
import pygame.camera

pygame.init()
pygame.camera.init()

size = width, height = 1080, 860
black = 0, 0, 0

camlist = pygame.camera.list_cameras()
print(camlist)
cam = pygame.camera.Camera(camlist[0], (640,480))

screen = pygame.display.set_mode(size)
cam.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    image = cam.get_image()

    screen.fill(black)

    screen.blit(image,(0,0))

    pygame.display.flip()
    pygame.time.delay(int(1000/30))
