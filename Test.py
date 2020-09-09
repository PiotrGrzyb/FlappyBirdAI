import pygame
import os
import random
import time

WINDOW_H = 800
WINDOW_W = 500

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))


class FlappyBird:
    IMG = BIRD_IMG
    ROTATE = 25
    VELOCITY = 20
    ANIMATION_FRAME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.last_jump = 0
        self.velocity = 0
        self.last_height = self.y
        self.img_numbers = 0
        self.img = self.IMG[0]

    def jump(self):
        self.velocity = -10.00
        self.last_jump = 0
        self.last_height = self.y

    def move(self):
        self.last_jump += 1
        way = self.velocity * self.last_jump + 1.5 * self.last_jump ** 2

        if way >= 16:
            way = 16

        if way < 0:
            way -= 2

        self.y = self.y + way
        if way < 0 or self.y < self.last_height + 50:
            if self.tilt < self.ROTATE:
                self.tilt = self.ROTATE
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATE

    def draw(self, window):
        self.img_numbers += 1

        if self.img_numbers < self.ANIMATION_FRAME:
            self.img = self.IMG[0]
        elif self.img_numbers < self.ANIMATION_FRAME * 2:
            self.img = self.IMG[1]
        elif self.img_numbers < self.ANIMATION_FRAME * 3:
            self.img = self.IMG[2]
        elif self.img_numbers < self.ANIMATION_FRAME * 4:
            self.img = self.IMG[1]
        elif self.img_numbers < self.ANIMATION_FRAME * 4 + 1:
            self.img = self.IMG[0]
            self.img_numbers = 0

        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_numbers = self.ANIMATION_FRAME * 2

        rotate_img = pygame.transform.rotate(self.img, self.tilt)
        rect = rotate_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotate_img, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(window, bird):
    window.blit(BG_IMG, (0, 0))
    bird.draw(window)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    bird = FlappyBird(200, 200)
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))

    run = True
    while run:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()
        if WINDOW_W / 2 <= mouse[0] <= WINDOW_W / 2 + 140 and WINDOW_H / 2 <= mouse[1] <= WINDOW_H / 2 + 40:
            pygame.draw.rect(window, color_light, [WINDOW_W / 2, WINDOW_H / 2, 140, 40])

        else:
            pygame.draw.rect(window, color_dark, [WINDOW_W / 2, WINDOW_H / 2, 140, 40])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(window, bird)
    pygame.quit()
    quit()


main()

