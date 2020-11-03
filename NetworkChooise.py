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


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def difficulty_menu():
    click = False
    while True:

        difficulty_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        difficulty_window.blit(BG_IMG, (0, 0))
        clock = pygame.time.Clock()
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(int(WINDOW_W / 2 - 100), 200, 200, 50)
        button_2 = pygame.Rect(int(WINDOW_W / 2 - 100), 300, 200, 50)
        button_3 = pygame.Rect(int(WINDOW_W / 2 - 100), 700, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                pass

        if button_2.collidepoint((mx, my)):
            if click:
                pass
        if button_3.collidepoint((mx, my)):
            if click:
                pass

        pygame.draw.rect(difficulty_window, (50, 205, 50), button_1)
        pygame.draw.rect(difficulty_window, (139,0,0), button_2)
        pygame.draw.rect(difficulty_window, (128, 128, 128), button_3)

        draw_text('Choose difficulty', FONT, (255, 255, 255), difficulty_window, WINDOW_W / 4 + 10, 20)
        draw_text('Normal', FONT, (0, 0, 0), difficulty_window, WINDOW_W / 2 - 60, 210)
        draw_text('Hard', FONT, (0, 0, 0), difficulty_window, WINDOW_W / 2 - 40, 310)
        draw_text('Back', FONT, (255, 255, 255), difficulty_window, WINDOW_W / 2 - 40, 710)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

difficulty_menu()
