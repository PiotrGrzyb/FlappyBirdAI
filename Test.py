import neat
import pygame
import os
import random
import time

WINDOW_H = 800
WINDOW_W = 600
VELOCITY_OF_EVERYTHING = 6

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("images", "bg.png")), (WINDOW_W, WINDOW_H))

GEN = 0


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


def draw_window(window, birds, pipes, ground, score, gen):
    window.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    for bird in birds:
        bird.draw(window)

    score_text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_text, (WINDOW_W - 10 - score_text.get_width(), 10))

    gen_text = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    window.blit(gen_text, (10, 10))
    ground.draw(window)

    pygame.display.update()


class Pipe:
    GAPS = 200
    P_VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bot = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOT_PIPE = PIPE_IMG

        self.checkpoint = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450, 1)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bot = self.height + self.GAPS

    def move(self):
        self.x -= VELOCITY_OF_EVERYTHING

    def draw(self, window):
        window.blit(self.TOP_PIPE, (self.x, self.top))
        window.blit(self.BOT_PIPE, (self.x, self.bot))

    def collision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        bot_mask = pygame.mask.from_surface(self.BOT_PIPE)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bot - round(bird.y))

        # bot/top_point powinno zwrócić NULL jeśli nie ma kolizji

        bot_point = bird_mask.overlap(bot_mask, bot_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bot_point:
            return True

        return False


class Ground:
    VELOCITY = 5
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self, y):
        self.x1 = 0
        self.x2 = self.WIDTH
        self.y = y

    def move(self):
        self.x1 -= VELOCITY_OF_EVERYTHING
        self.x2 -= VELOCITY_OF_EVERYTHING

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def main(genomes, config):
    clock = pygame.time.Clock()
    global GEN
    GEN += 1
    # color_light = (0, 0, 0)
    # color_dark = (0, 0, 0)

    ground = Ground(WINDOW_H-70)
    pipes = [Pipe(WINDOW_H-100)]
    birds = []
    nets = []
    gen = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(FlappyBird(230, 350))
        g.fitness = 0
        gen.append(g)

    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    score = 0

    running = True
    while running:
        clock.tick(30)
        # mouse = pygame.mouse.get_pos()
        # if WINDOW_W / 2 <= mouse[0] <= WINDOW_W / 2 + 140 and WINDOW_H / 2 <= mouse[1] <= WINDOW_H / 2 + 40:
        #    pygame.draw.rect(window, color_light, [WINDOW_W / 2, WINDOW_H / 2, 140, 40])

        # else:
        #    pygame.draw.rect(window, color_dark, [WINDOW_W / 2, WINDOW_H / 2, 140, 40])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        which_pipe = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width():
                which_pipe = 1
        else:
            running = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            gen[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[which_pipe].height), abs(bird.y - pipes[which_pipe].bot)))

            if output[0] > 0.5:
                bird.jump()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if WINDOW_W / 2 <= mouse[0] <= WINDOW_W / 2 + 140 and WINDOW_H / 2 <= mouse[1] <= WINDOW_H / 2 + 40:
        #         pygame.quit()

        # bird.move()
        add_pipe = False
        removed = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collision(bird):
                    gen[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    gen.pop(x)

                if not pipe.checkpoint and pipe.x < bird.x:
                    pipe.checkpoint = True
                    add_pipe = True

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                removed.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in gen:
                g.fitness += 5
            pipes.append(Pipe(600))

        for rmv in removed:
            pipes.remove(rmv)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 630 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                gen.pop(x)

        ground.move()
        draw_window(window, birds, pipes, ground, score, GEN)


def run(config_files):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_files)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)

    winner = population.run(main, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_file = os.path.join(local_directory, "config.txt")
    run(config_file)
