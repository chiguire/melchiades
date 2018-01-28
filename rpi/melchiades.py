#!/usr/bin/env python3


import os, sys, pygame, math
from pygame.locals import *

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
    def __init__(self, game_state, screen, font, w, h):
        self.game_state = game_state
        self.request_game_state = None
        self.current_timer = 0
        self.target_timer = 0
        self.screen = screen
        self.font = font
        self.debugfont = pygame.font.SysFont("Arial", 14)
        self.width = w
        self.height = h
    
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
        txt = "DEBUG> State: %s Timer: %d/%d" % (self.game_state, self.current_timer, self.target_timer)
        debug_text = self.debugfont.render(txt, True, (255,255,255), None)
        self.screen.blit(debug_text, (10, self.height - 10 - debug_text.get_rect().height))

    def draw_STATE_START(self):
        pass

    def draw_STATE_IDLE(self):
        pass

    def draw_STATE_LISTENING(self):
        pass

    def draw_STATE_RECOGNIZING(self):
        pass

    def draw_STATE_THINKING(self):
        from mtextrender import render_lines
        textsurfaces = render_lines(self.font, self.transcripted, self.width, self.height)

        for tsf in textsurfaces:
            self.screen.blit(tsf[0], tsf[1])

    def draw_STATE_ABOUT_TO_REVEAL(self):
        pass

    def draw_STATE_REVEAL(self):
        pass

    def draw_STATE_THANKS(self):
        pass

    #UPDATE

    def update(self):
        self.updatefunc[self.game_state]()
        if self.requested_game_state is not None:
            self.game_state = self.requested_game_state
            self.requested_game_state = None
    
    def update_STATE_START(self):
        self.requested_game_state = STATE_IDLE

    def update_STATE_IDLE(self):
        self.requested_game_state = STATE_LISTENING

    def update_STATE_LISTENING(self):
        import micrec
        self.heard_bytes = micrec.record_stuff()
        self.requested_game_state = STATE_RECOGNIZING

    def update_STATE_RECOGNIZING(self):
        import micrec
        self.transcripted = micrec.recognize(self.heard_bytes)
        print("Heard: %s" % self.transcripted)
        self.requested_game_state = STATE_THINKING
        self.current_timer = 0
        self.target_timer = 30*5

    def update_STATE_THINKING(self):
        if self.current_timer >= self.target_timer:
            self.requested_game_state = STATE_ABOUT_TO_REVEAL
        else:
            self.current_timer = self.current_timer + 1

    def update_STATE_ABOUT_TO_REVEAL(self):
        self.requested_game_state = STATE_REVEAL 

    def update_STATE_REVEAL(self):
        self.requested_game_state = STATE_THANKS

    def update_STATE_THANKS(self):
        self.requested_game_state = STATE_IDLE


def init_and_loop():
    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    os.environ['SDL_VIDEO_CENTERED'] = '0'
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    lefont = pygame.font.Font("Mortified.ttf", 80)

    game_state = GameState(STATE_START, screen, lefont, width, height)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP and event.key == K_q: sys.exit()

        screen.fill(black)

        game_state.draw()

        pygame.display.flip()

        game_state.update()

        pygame.time.delay(int(1000/30))

if __name__ == "__main__":
    init_and_loop()
