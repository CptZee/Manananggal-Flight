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

import pygame, math, os, webbrowser
from random import randint

def main():
    global FPS, gravity, clock, dead, score, run, started, runs, obstacles, manananggal, manananggal_img
    global obstacle_img, win, roof_img, indicator_font, bg_img, screen_width, screen_height, point_sound 
    global highscore, github_url, github_logo, logo_x, logo_y, logo_width, logo_height, game_over_sound
    global music

    pygame.init()

    FPS = 45
    gravity = 1
    dead = False
    score = -2
    run = True
    started = False
    runs = 0
    highscore = 0
    obstacles = []
    screen_width, screen_height = 800, 600
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Manananggal Flight: Urban Skies Adventure")
    clock = pygame.time.Clock()
    script_dir = os.path.dirname(__file__)
    manananggal_img = pygame.image.load("Assets/manananggal.png")
    bg_img = pygame.image.load("Assets/background.png")
    obstacle_img = pygame.image.load("Assets/obstacle.png")
    roof_img = pygame.image.load("Assets/roof.png")
    github_logo = pygame.image.load("Assets/Github.png")
    point_sound = pygame.mixer.Sound("Assets/point.wav")
    game_over_sound = pygame.mixer.Sound("Assets/game_over.wav")
    music = pygame.mixer.Sound("Assets/music.wav")
    icon_path = "Assets/icon.png"
    indicator_font = pygame.font.SysFont('Comic Sans', 30)
    github_url = "https://github.com/CptZee/Mananangal-Fly"
    logo_width, logo_height = github_logo.get_rect().size
    logo_x = screen_width - logo_width - 10
    logo_y = screen_height - logo_height - 10
    
    #Set the values for the mananangal
    manananggal = Manananggal()
    manananggal.x = 250
    manananggal.y = 250
    manananggal.vel = 0

    icon_image = pygame.image.load(icon_path)

    pygame.display.set_icon(icon_image)

    music.play(loops=-1)
    music.set_volume(0.2)

    RestartGame()
    while run:
        RunGame()
    
    pygame.quit()

def ObstaclePair() :
    r = randint(75, 350)
    obstacles.append(Obstacle("DOWN", 900, r))
    obstacles.append(Obstacle("UP", 900, 600-(r+125)))
    global score
    score += 1
    if score > 0:
        point_sound.play()

def AnimateRoof() :
    win.blit(roof_img, ((runs%111)*-7, 500))

def RunGame():
    global run, runs, started, restart_timer, score, highscore
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
                        Manananggal.jump()
            elif event.type == pygame.QUIT :
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if logo_x <= mouse_x <= logo_x + logo_width and logo_y <= mouse_y <= logo_y + logo_height:
                    webbrowser.open('https://github.com/CptZee/Manananggal-Fly')
                if not started :
                    started = True
                if not dead :
                    Manananggal.jump()

        win.blit(bg_img, (0, 0))
        if runs % 45 == 0 and started :
            ObstaclePair()
        for o in obstacles :
            o.update()
            o.checkCollide()

        if started != True :
            DisplayIndicator(["Press 'space bar' or 'click' to start the game",
              "Press 'esc' to exit the game"], -100)
        if score >= 0:
            DisplayIndicator(["Score: " + str(score),
                            "Highscore: " + str(highscore)], 220)
        else: 
            DisplayIndicator(["Mananangal Flight",
                              "Highscore: " + str(highscore)], 180)
           
        
        Manananggal.update()
        win.blit(manananggal, (Manananggal.x,Manananggal.y))
        AnimateRoof()

        win.blit(github_logo, (logo_x, logo_y))
        pygame.display.update()
        clock.tick(FPS)
        highscore = max(score, highscore)
        if dead:
            game_over_sound.play()
            RestartGame()
        if not dead:
            runs += 1

def DisplayIndicator(text_lines, y_adjustment):
    y_offset = (screen_height // 2 - len(text_lines) * indicator_font.get_linesize() // 2) - y_adjustment
    
    for line in text_lines:
        text_surface = indicator_font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width/2, y_offset))
        win.blit(text_surface, text_rect)
        y_offset += indicator_font.get_linesize()

def RestartGame():
    global dead, started, runs, score, obstacles, restart_timer

    dead = False
    started = False
    runs = 0
    score = -2
    restart_timer = 0
    obstacles.clear()
    
    DisplayIndicator(["Mananangal Flight",
                        "Highscore: " + str(highscore)], 180)

    Manananggal.x = 250
    Manananggal.y = 250
    Manananggal.vel = 0

##
##  Different classes
##  TODO: Migrate them to their own .py file
##

class Manananggal :
    x = 250
    y = 250
    vel = 0

    def update() :
        if started :
            if Manananggal.y < 475 :
                Manananggal.y += Manananggal.vel
                Manananggal.vel += gravity
            else :
                Manananggal.y = 475
                global dead
                dead = True
            if Manananggal.y < 0 :
                Manananggal.y = 0
                Manananggal.vel = 0
        else :
            Manananggal.y = 250 + math.sin(runs/10)*15
        Manananggal.getAngle()

    def jump() :
        Manananggal.vel = -10

    def getAngle() :
        global manananggal
        manananggal = pygame.transform.rotate(manananggal_img, -3*Manananggal.vel)

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
        global dead
        if self.dir == "DOWN" :
            if Manananggal.x + 48 > self.x and self.x + 75 > Manananggal.x :
                if Manananggal.y + 2 < self.len :
                    dead = True
        else :
            if Manananggal.x + 48 > self.x and self.x + 75 > Manananggal.x :
                if Manananggal.y + 45 > 600-self.len :
                    dead = True

main()