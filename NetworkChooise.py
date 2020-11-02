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


def choice_menu():
    click = False
    local_directory = os.path.dirname(__file__)
    config_file = os.path.join(local_directory, "config.txt")
    while True:

        choice_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        choice_window.blit(BG_IMG, (0, 0))
        clock = pygame.time.Clock()
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(int(WINDOW_W / 2 - 100), 100, 200, 50)
        button_2 = pygame.Rect(int(WINDOW_W / 2 - 100), 200, 200, 50)
        button_3 = pygame.Rect(int(WINDOW_W / 2 - 100), 300, 200, 50)
        button_4 = pygame.Rect(int(WINDOW_W / 2 - 100), 400, 200, 50)
        button_5 = pygame.Rect(int(WINDOW_W / 2 - 100), 500, 200, 50)
        button_6 = pygame.Rect(int(WINDOW_W / 2 - 100), 600, 200, 50)
        button_7 = pygame.Rect(int(WINDOW_W / 2 - 100), 700, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                pass
        if button_2.collidepoint((mx, my)):
            if click:
                pass
        if button_3.collidepoint((mx, my)):
            if click:
                pass
        if button_4.collidepoint((mx, my)):
            if click:
                pass
        if button_5.collidepoint((mx, my)):
            if click:
                pass
        if button_6.collidepoint((mx, my)):
            if click:
                pass
        if button_7.collidepoint((mx, my)):
            if click:
                main_menu()

        pygame.draw.rect(choice_window, (255, 255, 255), button_1)
        pygame.draw.rect(choice_window, (255, 255, 255), button_2)
        pygame.draw.rect(choice_window, (128, 128, 128), button_3)
        pygame.draw.rect(choice_window, (128, 128, 128), button_4)
        pygame.draw.rect(choice_window, (0, 0, 0), button_5)
        pygame.draw.rect(choice_window, (0, 0, 0), button_6)

        draw_text('Choose number of inputs', FONT, (255, 255, 255), choice_window, WINDOW_W / 6, 20)
        draw_text('2', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 110)
        draw_text('3', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 210)
        draw_text('4', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 310)
        draw_text('5', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 410)
        draw_text('6', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 510)
        draw_text('7', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 610)
        draw_text('Back', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 40, 710)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


choice_menu()
