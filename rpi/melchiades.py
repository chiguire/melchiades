#!/usr/bin/env python3

import os, sys, pygame, math, requests
from pygame.locals import *
import gifplayer
import serial
import ard

size = width, height = 1080, 860
black = 0, 0, 0

STATE_START = "STATE_START"
STATE_IDLE = "STATE_IDLE"
STATE_LISTENING = "STATE_LISTENING"
STATE_RECOGNIZING = "STATE_RECOGNIZING"
STATE_THINKING = "STATE_THINKING"
STATE_ABOUT_TO_REVEAL = "STATE_ABOUT_TO_REVEAL"
STATE_REVEAL = "STATE_REVEAL"
STATE_THANKS = "STATE_THANKS"

class GameState:
    def __init__(self, game_state, ser, screen, font, w, h):
        self.game_state = game_state
        self.request_game_state = None
        self.current_timer = 0
        self.target_timer = 0
        self.screen = screen
        self.font = font
        self.debugfont = pygame.font.SysFont("Arial", 14)
        self.width = w
        self.height = h
        self.ser = ser
        self.read_from_serial = ""
    
        self.drawfunc = {
            STATE_START: self.draw_STATE_START,
            STATE_IDLE: self.draw_STATE_IDLE,
            STATE_LISTENING: self.draw_STATE_LISTENING,
            STATE_RECOGNIZING: self.draw_STATE_RECOGNIZING,
            STATE_THINKING: self.draw_STATE_THINKING,
            STATE_ABOUT_TO_REVEAL: self.draw_STATE_ABOUT_TO_REVEAL,
            STATE_REVEAL: self.draw_STATE_REVEAL,
            STATE_THANKS: self.draw_STATE_THANKS
        }

        self.updatefunc = {
            STATE_START: self.update_STATE_START,
            STATE_IDLE: self.update_STATE_IDLE,
            STATE_LISTENING: self.update_STATE_LISTENING,
            STATE_RECOGNIZING: self.update_STATE_RECOGNIZING,
            STATE_THINKING: self.update_STATE_THINKING,
            STATE_ABOUT_TO_REVEAL: self.update_STATE_ABOUT_TO_REVEAL,
            STATE_REVEAL: self.update_STATE_REVEAL,
            STATE_THANKS: self.update_STATE_THANKS
        }
            

    def draw(self):
        self.drawfunc[self.game_state]()
        txt = "DEBUG> State: %s Timer: %d/%d Serial: %s" % (self.game_state, self.current_timer, self.target_timer, self.read_from_serial)
        debug_text = self.debugfont.render(txt, True, (255,255,255), None)
        self.screen.blit(debug_text, (10, self.height - 10 - debug_text.get_rect().height))

    def draw_STATE_START(self):
        self.screen.fill(black)


    def draw_STATE_IDLE(self):
        self.screen.fill(black)
        pass

    def draw_STATE_LISTENING(self):
        self.screen.fill(black)
        pass

    def draw_STATE_RECOGNIZING(self):
        self.screen.fill(black)
        pass

    def draw_STATE_THINKING(self):
        self.screen.fill(black)
        from mtextrender import render_lines
        textsurfaces = render_lines(self.font, self.transcripted, self.width, self.height)

        for tsf in textsurfaces:
            self.screen.blit(tsf[0], tsf[1])

    def draw_STATE_ABOUT_TO_REVEAL(self):
        self.screen.fill(black)
        pass

    def draw_STATE_REVEAL(self):
        self.screen.fill(black, Rect(0, self.height - 50, self.width, 50))
        r = self.gif_image.get_rect()
        p = ( (self.width - r.width) / 2, (self.height - r.height) / 2)
        self.gif_image.render(self.screen, p)

    def draw_STATE_THANKS(self):
        self.screen.fill(black)
        pass

    #UPDATE

    def update(self):
        try:
            self.read_from_serial = self.ser.readline().decode('ascii').strip()
        except:
            self.read_from_serial = ""
        self.updatefunc[self.game_state]()
        if self.requested_game_state is not None:
            self.game_state = self.requested_game_state
            self.requested_game_state = None
    
    def update_STATE_START(self):
        self.requested_game_state = STATE_IDLE
        try:
            self.ser.write(b'1')
        except:
            pass

    def update_STATE_IDLE(self):
        arduino_state = ard.try_to_read_arduino_state(self.read_from_serial)
        try:
            self.ser.write(b'1')
        except:
            pass

        if arduino_state is None:
            pass
        else:
            if arduino_state.button0 or arduino_state.button1 or arduino_state.button2 or arduino_state.button3:
                self.requested_game_state = STATE_LISTENING

    def update_STATE_LISTENING(self):
        import micrec
        self.heard_bytes = micrec.record_stuff()
        self.requested_game_state = STATE_RECOGNIZING

    def update_STATE_RECOGNIZING(self):
        import micrec
        self.transcripted = micrec.recognize(self.heard_bytes)
        print("Heard: %s" % self.transcripted)

        if self.transcripted == "":
            print("Heard nothing")
            self.requested_game_state = STATE_IDLE
        else:
            self.requested_game_state = STATE_THINKING

    def update_STATE_THINKING(self):
        import giphy
        gif_url = giphy.giphy_translate(self.transcripted)
        print("Gif URL: %s" % str(gif_url))

        if gif_url is None:
            self.requested_game_state = STATE_IDLE
            return
        gif_response = requests.get(gif_url)

        if gif_response.status_code == 200:
            gif_bytes = gif_response.content
            gif_filename = "temp.gif"
            with open(gif_filename, "wb") as gif_file:
                gif_file.write(gif_bytes)
            self.gif_image = gifplayer.GIFImage(gif_filename) 
            self.current_timer = 0
            self.target_timer = 200
            self.requested_game_state = STATE_ABOUT_TO_REVEAL
        

    def update_STATE_ABOUT_TO_REVEAL(self):
        try:
            self.ser.write(b'2')
        except:
            pass
        self.requested_game_state = STATE_REVEAL 

    def update_STATE_REVEAL(self):
        if self.current_timer >= self.target_timer:
            self.requested_game_state = STATE_THANKS
        else:
            self.current_timer = self.current_timer + 1

    def update_STATE_THANKS(self):
        self.requested_game_state = STATE_IDLE


def init_and_loop():
    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    os.environ['SDL_VIDEO_CENTERED'] = '0'
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    lefont = pygame.font.Font("Mortified.ttf", 80)
    ser = serial.Serial(port="/dev/serial/by-id/usb-Arduino_Srl_Arduino_Mega_754313433343510140C1-if00", baudrate=9600, write_timeout=0.05)

    game_state = GameState(STATE_START, ser, screen, lefont, width, height)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP and event.key == K_q: sys.exit()

        
        game_state.draw()

        pygame.display.flip()

        game_state.update()

        pygame.time.delay(int(1000/30))

if __name__ == "__main__":
    init_and_loop()
