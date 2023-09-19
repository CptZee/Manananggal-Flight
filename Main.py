# ------------------------------------------------------------------------------------------
# Copyright (C) 2023 Aaron James R. Mission & Ellysa Mae Kayo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------

import pygame, math, os, sys
from random import randint
from time import sleep

def main():
    global FPS, gravity, clock, dead, score, run, started, runs, obstacles, mananangal, mananangal_img
    global obstacle_img, win, roof_img, timer_font, indicator_font, bg_img, screen_width, screen_height 

    pygame.init()

    FPS = 45
    gravity = 1
    dead = False
    score = -2
    run = True
    started = False
    runs = 0
    obstacles = []
    screen_width, screen_height = 800, 600
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mananangal Flying Game!")
    clock = pygame.time.Clock()
    script_dir = os.path.dirname(__file__)
    mananangal_img = pygame.image.load(os.path.join(script_dir, 'mananangal.png'))
    bg_img = pygame.image.load(os.path.join(script_dir, 'background.png'))
    obstacle_img = pygame.image.load(os.path.join(script_dir, 'obstacle.png'))
    roof_img = pygame.image.load(os.path.join(script_dir, 'roof.png'))
    timer_font = pygame.font.SysFont('Comic Sans MS', 30)
    indicator_font = pygame.font.SysFont('Comic Sans MS', 30)


    #Set the values for the mananangal
    mananangal = Mananangal()
    mananangal.x = 250
    mananangal.y = 250
    mananangal.vel = 0

    icon_path = os.path.join(script_dir, 'icon.png')
    icon_image = pygame.image.load(icon_path)

    pygame.display.set_icon(icon_image)

    RestartGame()
    while run:
        RunGame()
    
    pygame.quit()

def Die() :
    global dead
    dead = True
    run = False

def ObstaclePair() :
    r = randint(75, 350)
    obstacles.append(Obstacle("DOWN", 900, r))
    obstacles.append(Obstacle("UP", 900, 600-(r+125)))
    global score
    score += 1

def AnimateRoof() :
    win.blit(roof_img, ((runs%111)*-7, 500))

def RunGame():
    global run, runs, started, restart_timer
    while run:
        pygame.time.delay(5)
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    run = False
                elif event.key == pygame.K_SPACE :
                    if not started :
                        started = True
                    if not dead :
                        Mananangal.jump()
            elif event.type == pygame.QUIT :
                run = False

        win.blit(bg_img, (0, 0))
        if started != True :
            DisplayIndicator("Press 'space bar' to start the game")
        if runs % 45 == 0 and started :
            ObstaclePair()
        for o in obstacles :
            o.update()
            o.checkCollide()
        Mananangal.update()
        win.blit(mananangal, (Mananangal.x,Mananangal.y))
        AnimateRoof()

        scoreboard = timer_font.render(str(score), False, (0, 0, 0))
        if score > -1 :
            scorebase = pygame.draw.rect(win, (255, 255, 255), (7, 5, len(str(score))*15+10, 35))
            win.blit(scoreboard, (10, 0))
        pygame.display.update()
        clock.tick(FPS)
        if dead:
            RestartGame()
        if not dead:
            runs += 1

def DisplayIndicator(text):
    text_surface = indicator_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width/2, (screen_height/2) + 50))
    win.blit(text_surface, text_rect)

def RestartGame():
    global dead, started, runs, score, obstacles, restart_timer

    dead = False
    started = False
    runs = 0
    score = -2
    restart_timer = 0
    obstacles.clear()

    Mananangal.x = 250
    Mananangal.y = 250
    Mananangal.vel = 0

##
##  Different classes
##  TODO: Migrate them to their own .py file
##

class Mananangal :
    x = 250
    y = 250
    vel = 0

    def update() :
        if started :
            if Mananangal.y < 475 :
                Mananangal.y += Mananangal.vel
                Mananangal.vel += gravity
            else :
                Mananangal.y = 475
                Die()
            if Mananangal.y < 0 :
                Mananangal.y = 0
                Mananangal.vel = 0
        else :
            Mananangal.y = 250 + math.sin(runs/10)*15
        Mananangal.getAngle()

    def jump() :
        Mananangal.vel = -10

    def getAngle() :
        global mananangal
        mananangal = pygame.transform.rotate(mananangal_img, -3*Mananangal.vel)

class Obstacle() :
    def __init__(self, dir, x, len) :
        self.dir = dir
        self.x = x
        self.len = len

    def update(self) :
        if self.dir == "UP" :
            win.blit(obstacle_img, (self.x, 600-self.len))
        else :
            win.blit(pygame.transform.rotate(obstacle_img, 180), (self.x, self.len-431))
        if not dead :
            self.x -= 7

    def checkCollide(self) :
        if self.dir == "DOWN" :
            if Mananangal.x + 48 > self.x and self.x + 75 > Mananangal.x :
                if Mananangal.y + 2 < self.len :
                    Die()
        else :
            if Mananangal.x + 48 > self.x and self.x + 75 > Mananangal.x :
                if Mananangal.y + 45 > 600-self.len :
                    Die()

main()