import pygame
import os

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


def wrong_inputs_screen():
    click = False
    while True:
        wrong_inputs_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        wrong_inputs_window.blit(BG_IMG, (0, 0))
        clock = pygame.time.Clock()
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(int(WINDOW_W / 2 - 100), 700, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                pass
        pygame.draw.rect(wrong_inputs_window, (50, 205, 50), button_1)
        draw_text('Selected network does not have', FONT, (0, 0, 0), wrong_inputs_window, 40, 110)
        draw_text('sufficent number of inputs', FONT, (0, 0, 0), wrong_inputs_window,  65, 210)
        draw_text('that were previously chosen', FONT, (0, 0, 0), wrong_inputs_window, 60, 310)
        draw_text('Back', FONT, (255, 255, 255), wrong_inputs_window, WINDOW_W / 2 - 40, 710)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)


wrong_inputs_screen()

