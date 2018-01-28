#!/usr/bin/env python3

import os, sys, pygame, math
from pygame.locals import *

def render_lines(f, text, w, h):
    #lefont.render("A VERY BIG QUESTION INDEED", True, (255, 127, 0), None)
    all_fit = False
    text_partitions = [text]
    while not all_fit:
        all_fit, surfaces_or_partitions = render_partitions(text, text_partitions, f, w)
        if not all_fit:
            text_partitions = surfaces_or_partitions
        else:
            surfaces = surfaces_or_partitions
    return [(surface, calculate_position(surface, w, h, i, len(surfaces))) for i, surface in enumerate(surfaces)]

def calculate_position(srf, w, h, i, n):
    rect = srf.get_rect()
    whole_text_height = rect.height*n
    return ((w - rect.width)/2.0, (h - whole_text_height-60)/2.0 + rect.height*i)

def render_partitions(text, text_partitions, f, w):
    tsfs = []
    for partition in text_partitions:
        tsf = f.render(partition, True, (255, 127, 0), None)
        if tsf.get_width() > w:
            return (False, partition_text(text, len(text_partitions) + 1))
        tsfs.append(tsf)
    return (True, tsfs)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def partition_text(text, n):
    words = text.split()
    words_chunked = chunks(words, int(math.ceil(len(words)/n)))
    return [' '.join(words) for words in words_chunked]
    
pygame.init()

size = width, height = 1080, 860
black = 0, 0, 0

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(size, pygame.NOFRAME)
lefont = pygame.font.Font("Mortified.ttf", 80)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP and event.key == K_q: sys.exit()

    screen.fill(black)

    textsurfaces = render_lines(lefont, "A VERY BIG QUESTION INDEED", width, height)

    for tsf in textsurfaces:
        screen.blit(tsf[0], tsf[1])

    pygame.display.flip()
    pygame.time.delay(int(1000/30))
