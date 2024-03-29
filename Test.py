import datetime
import gzip
import neat
import pygame
import os
import random
import time
import pickle
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import visualize

x = 450
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

WINDOW_H = 800
WINDOW_W = 600
VELOCITY_OF_EVERYTHING = 5
DIFF = 0
INPUTS = 0

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)
FONT_MAIN_MENU_TITLE = pygame.font.SysFont("comicsans", 75)
SMALL_FONT = pygame.font.SysFont("comicsans", 25)
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
        self.velocity = -2.1 * VELOCITY_OF_EVERYTHING
        self.last_jump = 0
        self.last_height = self.y

    def move(self):
        self.last_jump += 1
        way = self.velocity * self.last_jump + 1.5 * self.last_jump ** 2

        if way >= 15:
            way = 15

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


def draw_window(window, birds, pipes, ground, score, gen, alive):
    window.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    for bird in birds:
        bird.draw(window)

    score_text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_text, (WINDOW_W - 10 - score_text.get_width(), 10))

    gen_text = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    window.blit(gen_text, (10, 10))

    alive_text = FONT.render("Alive: " + str(alive), 1, (255, 255, 255))
    window.blit(alive_text, (10, 50))

    ground.draw(window)

    pygame.display.update()


def draw_window_single(window, bird, pipes, ground, score):
    window.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    bird.draw(window)

    score_text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_text, (WINDOW_W - 10 - score_text.get_width(), 10))

    ground.draw(window)

    pygame.display.update()


class Pipe:
    P_VELOCITY = 5
    GAPS = 200

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bot = 0
        self.middle = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOT_PIPE = PIPE_IMG

        self.checkpoint = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450, 1)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bot = self.height + self.GAPS
        self.middle = self.height + self.GAPS / 2

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

        bot_point = bird_mask.overlap(bot_mask, bot_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bot_point:
            return True

        return False


class HardPipe:
    P_VELOCITY = 5
    GAPS = 170

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bot = 0
        self.middle = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOT_PIPE = PIPE_IMG

        self.checkpoint = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450, 1)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bot = self.height + self.GAPS
        self.middle = self.height + self.GAPS / 2

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


def evaluate_genomes(genomes, config):
    clock = pygame.time.Clock()
    global GEN, INPUTS
    GEN += 1

    ground = Ground(WINDOW_H - 70)

    if DIFF == 0:
        ticking_rate = 30
        pipes = [Pipe(WINDOW_H - 100)]
    else:
        ticking_rate = 60
        pipes = [HardPipe(WINDOW_H - 100)]

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
        clock.tick(ticking_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GEN = 0
                    running = False
                    main()
                if event.key == pygame.K_x:
                    running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_s:
                    file_name = "winner" + str(INPUTS) + "inputs_" + datetime.datetime.now().strftime(
                        "%H-%M-%S") + ".pkl"
                    file_name_img = "winner" + str(INPUTS) + "inputs_" + datetime.datetime.now().strftime(
                        "%H-%M-%S")
                    node_names = {-1: '1', -2: '2', -3: '3', -4: '4', -5: '5', -6: '6', -6: '6', 0: 'Out'}
                    visualize.draw_net(config, gen[0], True, node_names=node_names, file_name=file_name_img)
                    with gzip.open(str(file_name), 'w', compresslevel=5) as f:
                        data = (gen[0], nets[0])
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

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

            output = network_activate(nets[x], bird, pipes[which_pipe], INPUTS)

            if output[0] > 0.5:
                bird.jump()

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
            if DIFF == 0:
                pipes.append(Pipe(600))
            else:
                pipes.append(HardPipe(600))

        for rmv in removed:
            pipes.remove(rmv)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                gen.pop(x)
        alive = len(birds)
        ground.move()
        draw_window(window, birds, pipes, ground, score, GEN, alive)


def network_activate(network, bird, pipes, inputs):
    if inputs == 2:
        out = network.activate((bird.y, abs(bird.y - pipes.height)))
    elif inputs == 3:
        out = network.activate((bird.y, abs(bird.y - pipes.height), abs(bird.y - pipes.bot)))
    elif inputs == 4:
        out = network.activate((bird.y, abs(bird.y - pipes.height), abs(bird.y - pipes.bot), bird.velocity))
    elif inputs == 5:
        out = network.activate((bird.y, abs(bird.y - pipes.height), abs(bird.y - pipes.bot), bird.velocity,
                                abs(bird.y - pipes.middle)))
    else:
        main()
    return out


def run(config_files):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_files)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)

    winner = population.run(evaluate_genomes, 50)
    global GEN
    GEN = 0
    file_name = "winner" + str(INPUTS) + "inputs_" + datetime.datetime.now().strftime(
        "%H-%M-%S") + ".pkl"
    with gzip.open(str(file_name), 'w', compresslevel=5) as f:
        pickle.dump(winner, f, protocol=pickle.HIGHEST_PROTOCOL)


def run_best(config_files):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_files)

    population = neat.Population(config)
    population.run(best_main, 50)


def best_main(genomes, config):
    clock = pygame.time.Clock()
    ground = Ground(WINDOW_H - 70)
    pipes = [Pipe(WINDOW_H - 100)]

    try:
        Tk().withdraw()
        filename = askopenfilename()
        os.path.split(filename)
        finalfilename = os.path.split(filename)[1]
    except FileNotFoundError:
        main()
        
    try:
        with gzip.open(finalfilename) as f:
            gen, net = pickle.load(f)
    except FileNotFoundError:
        main()

    bird = FlappyBird(230, 350)

    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    score = 0

    if DIFF == 0:
        ticking_rate = 30
        pipes = [Pipe(WINDOW_H - 100)]
    else:
        ticking_rate = 60
        pipes = [HardPipe(WINDOW_H - 100)]

    running = True
    while running:

        clock.tick(ticking_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                    running = False

        which_pipe = 0
        if bird:
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].TOP_PIPE.get_width():
                which_pipe = 1
        else:
            running = False
            break

        bird.move()
        try:
            output = network_activate(net, bird, pipes[which_pipe], INPUTS)
        except RuntimeError:
            wrong_inputs_screen()

        if output[0] > 0.5:
            bird.jump()

        add_pipe = False
        removed = []
        for pipe in pipes:
            if pipe.collision(bird):
                break

            if not pipe.checkpoint and pipe.x < bird.x:
                pipe.checkpoint = True
                add_pipe = True

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                removed.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            if DIFF == 0:
                pipes.append(Pipe(600))
            else:
                pipes.append(HardPipe(610))

        for rmv in removed:
            pipes.remove(rmv)

        if bird.y + bird.img.get_height() > 730 or bird.y < 0:
            break

        if score > 100:
            break
        ground.move()
        draw_window_single(window, bird, pipes, ground, score)


def single_main():
    clock = pygame.time.Clock()
    ground = Ground(WINDOW_H - 70)
    bird = FlappyBird(230, 350)
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    score = 0

    if DIFF == 0:
        ticking_rate = 30
        pipes = [Pipe(WINDOW_H - 100)]
    else:
        ticking_rate = 60
        pipes = [HardPipe(WINDOW_H - 100)]

    running = True
    while running:
        clock.tick(ticking_rate)
        bird.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    main()
                    running = False

        add_pipe = False
        removed = []
        for pipe in pipes:
            if pipe.collision(bird):
                score_screen(score)

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                removed.append(pipe)

            if not pipe.checkpoint and pipe.x < bird.x:
                pipe.checkpoint = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            if DIFF == 0:
                pipes.append(Pipe(600))
            else:
                pipes.append(HardPipe(600))

        for rmv in removed:
            pipes.remove(rmv)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            score_screen(score)

        ground.move()
        draw_window_single(window, bird, pipes, ground, score)


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
                single_main()

        if button_2.collidepoint((mx, my)):
            if click:
                main()

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


def choice_menu():
    click = False
    global INPUTS
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
                INPUTS = 2
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configTwoInputs.txt")
                run(config_file)
        if button_2.collidepoint((mx, my)):
            if click:
                INPUTS = 3
                run(config_file)
        if button_3.collidepoint((mx, my)):
            if click:
                INPUTS = 4
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configFourInputs.txt")
                run(config_file)
        if button_4.collidepoint((mx, my)):
            if click:
                INPUTS = 5
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configFiveInputs.txt")
                run(config_file)
        if button_5.collidepoint((mx, my)):
            if click:
                pass
        if button_6.collidepoint((mx, my)):
            if click:
                pass
        if button_7.collidepoint((mx, my)):
            if click:
                main()

        pygame.draw.rect(choice_window, (255, 255, 255), button_1)
        pygame.draw.rect(choice_window, (255, 255, 255), button_2)
        pygame.draw.rect(choice_window, (128, 128, 128), button_3)
        pygame.draw.rect(choice_window, (128, 128, 128), button_4)
        pygame.draw.rect(choice_window, (0, 0, 0), button_5)
        pygame.draw.rect(choice_window, (0, 0, 0), button_6)
        pygame.draw.rect(choice_window, (139, 0, 0), button_7)

        draw_text('Choose number of inputs', FONT, (255, 255, 255), choice_window, WINDOW_W / 6, 20)
        draw_text('2', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 110)
        draw_text('3', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 210)
        draw_text('4', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 310)
        draw_text('5', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 410)
        draw_text('6', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 510)
        draw_text('7', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 610)
        draw_text('Back', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 40, 710)

        if DIFF == 1:
            draw_text('Hard difficulty', SMALL_FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 150, 760)
        else:
            draw_text('Easy difficulty', SMALL_FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 150, 760)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def choice_menu_best():
    click = False
    global INPUTS
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
                INPUTS = 2
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configTwoInputs.txt")
                run_best(config_file)
        if button_2.collidepoint((mx, my)):
            if click:
                INPUTS = 3
                run_best(config_file)
        if button_3.collidepoint((mx, my)):
            if click:
                INPUTS = 4
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configFourInputs.txt")
                run_best(config_file)
        if button_4.collidepoint((mx, my)):
            if click:
                INPUTS = 5
                local_directory = os.path.dirname(__file__)
                config_file = os.path.join(local_directory, "configFiveInputs.txt")
                run_best(config_file)
        if button_5.collidepoint((mx, my)):
            if click:
                pass
        if button_6.collidepoint((mx, my)):
            if click:
                pass
        if button_7.collidepoint((mx, my)):
            if click:
                main()

        pygame.draw.rect(choice_window, (255, 255, 255), button_1)
        pygame.draw.rect(choice_window, (255, 255, 255), button_2)
        pygame.draw.rect(choice_window, (128, 128, 128), button_3)
        pygame.draw.rect(choice_window, (128, 128, 128), button_4)
        pygame.draw.rect(choice_window, (0, 0, 0), button_5)
        pygame.draw.rect(choice_window, (0, 0, 0), button_6)
        pygame.draw.rect(choice_window, (139, 0, 0), button_7)

        draw_text('Choose number of inputs', FONT, (255, 255, 255), choice_window, WINDOW_W / 6, 20)
        draw_text('2', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 110)
        draw_text('3', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 210)
        draw_text('4', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 310)
        draw_text('5', FONT, (0, 0, 0), choice_window, WINDOW_W / 2 - 10, 410)
        draw_text('6', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 510)
        draw_text('7', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 10, 610)
        draw_text('Back', FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 40, 710)

        if DIFF == 1:
            draw_text('Hard difficulty', SMALL_FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 150, 760)
        else:
            draw_text('Easy difficulty', SMALL_FONT, (255, 255, 255), choice_window, WINDOW_W / 2 - 150, 760)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def difficulty_menu_best():
    global DIFF
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
                DIFF = 0
                choice_menu_best()

        if button_2.collidepoint((mx, my)):
            if click:
                DIFF = 1
                choice_menu_best()

        if button_3.collidepoint((mx, my)):
            if click:
                main()

        pygame.draw.rect(difficulty_window, (50, 205, 50), button_1)
        pygame.draw.rect(difficulty_window, (139, 0, 0), button_2)
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


def difficulty_menu():
    global DIFF
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
                DIFF = 0
                choice_menu()

        if button_2.collidepoint((mx, my)):
            if click:
                DIFF = 1
                choice_menu()

        if button_3.collidepoint((mx, my)):
            if click:
                main()

        pygame.draw.rect(difficulty_window, (50, 205, 50), button_1)
        pygame.draw.rect(difficulty_window, (139, 0, 0), button_2)
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


def difficulty_menu_single():
    global DIFF
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
                DIFF = 0
                single_main()

        if button_2.collidepoint((mx, my)):
            if click:
                DIFF = 1
                single_main()

        if button_3.collidepoint((mx, my)):
            if click:
                main()

        pygame.draw.rect(difficulty_window, (50, 205, 50), button_1)
        pygame.draw.rect(difficulty_window, (139, 0, 0), button_2)
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
                main()
        pygame.draw.rect(wrong_inputs_window, (50, 205, 50), button_1)
        draw_text('Selected network file does not', FONT, (0, 0, 0), wrong_inputs_window, 40, 110)
        draw_text('not have the correct number of', FONT, (0, 0, 0), wrong_inputs_window,  40, 210)
        draw_text('inputs', FONT, (0, 0, 0), wrong_inputs_window, WINDOW_W / 2 - 60, 310)
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


def main():
    click = False
    while True:

        menu_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        menu_window.blit(BG_IMG, (0, 0))
        clock = pygame.time.Clock()
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(int(WINDOW_W / 2 - 100), 130, 200, 50)
        button_2 = pygame.Rect(int(WINDOW_W / 2 - 100), 230, 200, 50)
        button_3 = pygame.Rect(int(WINDOW_W / 2 - 100), 330, 200, 50)
        button_4 = pygame.Rect(int(WINDOW_W / 2 - 100), 430, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                difficulty_menu()
        if button_2.collidepoint((mx, my)):
            if click:
                difficulty_menu_single()
        if button_3.collidepoint((mx, my)):
            if click:
                difficulty_menu_best()
        if button_4.collidepoint((mx, my)):
            if click:
                pygame.quit()

        pygame.draw.rect(menu_window, (255, 255, 255), button_1)
        pygame.draw.rect(menu_window, (255, 255, 255), button_2)
        pygame.draw.rect(menu_window, (255, 255, 255), button_3)
        pygame.draw.rect(menu_window, (255, 255, 255), button_4)

        draw_text('FlappyAI', FONT_MAIN_MENU_TITLE, (255, 255, 255), menu_window, WINDOW_W / 2 - 110, 20)
        draw_text('Teach AI', FONT, (0, 0, 0), menu_window, WINDOW_W / 2 - 80, 140)
        draw_text('Play', FONT, (0, 0, 0), menu_window, WINDOW_W / 2 - 40, 240)
        draw_text('Load adult', FONT, (0, 0, 0), menu_window, WINDOW_W / 2 - 90, 340)
        draw_text('Quit', FONT, (0, 0, 0), menu_window, WINDOW_W / 2 - 40, 440)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    # execute only if run as a script
    main()
