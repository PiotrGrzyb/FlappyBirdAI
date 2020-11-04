import neat
import pygame
import os
import random
import time
import pickle
import SinglePlayer
import Load_best

x = 450
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

WINDOW_H = 800
WINDOW_W = 600
VELOCITY_OF_EVERYTHING = 5

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("images", "bg.png")), (WINDOW_W, WINDOW_H))
FONT_MAIN_MENU_TITLE = pygame.font.SysFont("comicsans", 75)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def score_screen(score):
    click = False
    while True:

        score_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        score_window.blit(BG_IMG, (0, 0))
        clock = pygame.time.Clock()
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(int(WINDOW_W / 2 - 100), 400, 200, 50)
        button_2 = pygame.Rect(int(WINDOW_W / 2 - 100), 500, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                pass

        if button_2.collidepoint((mx, my)):
            if click:
                pass

        pygame.draw.rect(score_window, (50, 205, 50), button_1)
        pygame.draw.rect(score_window, (139, 0, 0), button_2)

        draw_text('Score:', FONT_MAIN_MENU_TITLE, (255, 255, 255), score_window, WINDOW_W / 2 - 80, 120)
        draw_text(str(score), FONT_MAIN_MENU_TITLE, (255, 255, 255), score_window, WINDOW_W / 2 - 20, 200)
        draw_text('Retry', FONT, (0, 0, 0), score_window, WINDOW_W / 2 - 50, 410)
        draw_text('Menu', FONT, (0, 0, 0), score_window, WINDOW_W / 2 - 40, 510)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


score_screen(5)
