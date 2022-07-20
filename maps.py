import pygame
import sys

import logic
import objects
import visual
#объявление переменных
pygame.init()
width = None
height = None
display = None
clock = pygame.time.Clock()

ground = 69

d_velocity = 2.0

#обновление рекордов
def update_rec(name, score):
    i = 1;
    j=19;
    with open("records.txt", "rt") as file:
        list_date = file.read().split()
    file.close()
    while i < 19:
        if( int(list_date[i]) < score):
            while j>i:
                list_date[j] = list_date[j-2]
                list_date[j-1] = list_date[j-3]
                j-=2
            list_date[i] = score
            list_date[i-1] = name
            break
        i+=2
    file = open("records.txt", "wt")
    i=0
    while i<19:
        file.write(list_date[i] + ' ' + str(list_date[i+1]) + '\n')
        i+=2
    file.close()
    return False

#инициализация окна
def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground
    #interface.init(display)

def all_rest(pigs, birds, blocks):
    threshold = 0.15
    for pig in pigs:
        if pig.velocity.magnitude >= threshold:
            return False

    for bird in birds:
        if bird.velocity.magnitude >= threshold:
            return False

    for block in blocks:
        if block.velocity.magnitude >= threshold:
            return False

    return True
#функция закрытия
def close():
    pygame.quit()
    sys.exit()
#класс, описывающий игровое поле
class Maps:
    #конструктор
    def __init__(self):
        self.level = 1
        self.max_level = 10
        self.color = {'background': (51, 51, 51)}
        self.score = 0
        self.name = 'name'

    #ожидание закрытия
    def wait_level(self):
        time = 0
        while time < 3:
            #если есть событие
            for event in pygame.event.get():
                #и это событие - нажатие крестика, то закрываем программу
                if event.type == pygame.QUIT:
                    close()
                #если нажата клавиша 'q', то тоже закрываем
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
            time += 1
            clock.tick(1)

        return

    #проверка результата в конце уровня
    def check_win(self, pigs, birds):
        #если свиней больше нет - победа
        if pigs == []:
            print("WON!")
            return True
        #если свиньи остались, а птиц больше нет - поражение
        if (not pigs == []) and birds == []:
            print("LOST!")
            return False

    #функция паузы
    def pause(self, hero_num):
        # рисуем кнопки и текст
        pause_text = visual.Label(400, 100, 400, 200, None, self.color['background'])
        pause_text.set_text("GAME PAUSED", 70, "Fonts/Comic_Kings.ttf", (244, 208, 63))

        replay = visual.Button(100, 400, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.set_text("RESTART", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        resume = visual.Button(450, 400, 300, 100, None, (88, 214, 141), (171, 235, 198))
        resume.set_text("RESUME", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = visual.Button(800, 400, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.set_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        while True:
            # если нажата какая-то кнопка - выполняем соответвующее действие
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_p:
                        return
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action(hero_num, self.name)
                    if resume.isActive():
                        return
                    if exit.isActive():
                        return

            replay.draw()
            resume.draw()
            exit.draw()
            pause_text.draw()

            pygame.display.update()
            clock.tick(60)

    #отрисовка уровней
    def draw_map(self, hero_num, name):
        self.name = name
        #объявляем массивы для свиней, птиц, блоков и стен, а так же счетчик очков
        birds = []
        pigs = []
        blocks = []
        walls = []
        #self.score = 0
        #в зависимости от уровня, добавляем свиней, птиц, стены и тд
        if self.level == 1:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1100, height - 40, 25))
            pigs.append(logic.Pig(1500, height - 40, 25))

            blocks.append(logic.Block(1000, height - 60, 60))

        elif self.level == 2:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1000, height - 40, 25))
            pigs.append(logic.Pig(1300, height - 40, 25))

            blocks.append(logic.Block(850, height - 60, 60))
            blocks.append(logic.Block(850, height -160, 60))
            blocks.append(logic.Block(750, height - 60, 60))

        elif self.level == 3:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(820, height - 40, 25))
            pigs.append(logic.Pig(920, height - 40, 25))

            blocks.append(logic.Block(700, height - 100, 100))
            blocks.append(logic.Block(700, height - 2*60, 100))
            blocks.append(logic.Block(1200, height - 100, 100))

        elif self.level == 4:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1200, 350, 25))
            pigs.append(logic.Pig(1300, height - 60, 25))

            walls.append(objects.Wall(700, 400, 500, 20))

            blocks.append(logic.Block(800, height - 100, 100))

        elif self.level == 5:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1000, 500 - 60, 25))
            pigs.append(logic.Pig(1000, height - 60, 25))

            walls.append(objects.Wall(500, 500, 100, height - 500))
            walls.append(objects.Wall(800, 450, 500, 30))

            blocks.append(logic.Block(850, 500 - 100, 100))
            blocks.append(logic.Block(750, height - 100, 100))

        elif self.level == 6:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1300, 500 - 60, 25))
            pigs.append(logic.Pig(1100, height - 60, 25))

            walls.append(objects.Wall(700, 100, 30, 350))
            walls.append(objects.Wall(700, 450, 500, 30))

            blocks.append(logic.Block(1000, height - 100, 100))

        elif self.level == 7:
            for i in range(4):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1100, 500 - 60, 25))
            pigs.append(logic.Pig(1300, 500 - 60, 25))
            pigs.append(logic.Pig(1200, height - 60, 25))

            walls.append(objects.Wall(800, 250, 30, 200))
            walls.append(objects.Wall(700, 450, 500, 30))

        elif self.level == 8:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1100, height - 60, 25))
            pigs.append(logic.Pig(1200, height - 60, 25))

            walls.append(objects.Wall(700, 250, 30, height - 250))

        elif self.level == 9:
            for i in range(3):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(800, height - 60, 25))
            pigs.append(logic.Pig(1100, height - 60, 25))

            blocks.append(logic.Block(950, height - 100, 100))
            blocks.append(logic.Block(950, height - 2*60, 100))

            walls.append(objects.Wall(600, 400, 30, height - 400))

        elif self.level == 10:
            for i in range(4):
                new_bird = logic.Bird(hero_num, 40*i + 5*i, height - 20, 25, None)
                birds.append(new_bird)

            pigs.append(logic.Pig(1100, height - 60, 25))
            pigs.append(logic.Pig(1200, 400 - 60, 25))
            pigs.append(logic.Pig(1450, height - 60, 25))

            blocks.append(logic.Block(900, 300, 100))
            blocks.append(logic.Block(800, height - 2*60, 100))

            walls.append(objects.Wall(700, 400, 500, 40))
            walls.append(objects.Wall(1000, 500, 30, height - 500))

        self.start_level(birds, pigs, blocks, walls, hero_num)

    #начать уровень сначала
    def replay_level(self, hero_num):
        self.level -= 1
        self.draw_map(hero_num, self.name)

    #начать игру с первого уровня
    def start_again(self, hero_num):
        self.level = 1
        self.score = 0
        self.draw_map(hero_num, self.name)

    #отрисовка экрана после победы в уровне
    def level_cleared(self, hero_num):
        self.level += 1

        level_cleared_text = visual.Label(400, 100, 400, 200, None, self.color['background'])
        if self.level <= self.max_level:
            level_cleared_text.set_text("LEVEL " + str(self.level - 1) + " CLEARED!", 80, "Fonts/Comic_Kings.ttf", (255, 255, 255))
        else:
            level_cleared_text.set_text("ALL LEVEL CLEARED!", 80, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        score_text = visual.Label(450, 300, 300, 100, None, self.color['background'])
        score_text.set_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        replay = visual.Button(100, 500, 300, 100, self.replay_level, (244, 208, 63), (247, 220, 111))
        replay.set_text("PLAY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        if self.level <= self.max_level:
            next = visual.Button(450, 500, 300, 100, self.draw_map, (88, 214, 141), (171, 235, 198))
            next.set_text("CONTINUE", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        else:
            next = visual.Button(450, 500, 300, 100, self.start_again, (88, 214, 141), (171, 235, 198))
            next.set_text("START AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = visual.Button(800, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.set_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action(hero_num)
                    if next.isActive():
                        next.action(hero_num, self.name)
                    if exit.isActive():
                        update_rec(self.name, self.score)
                        exit.action()
            replay.draw()
            next.draw()
            exit.draw()
            level_cleared_text.draw()
            score_text.draw()

            pygame.display.update()
            clock.tick(60)

    # отрисовка экрана после проигрыща в уровне
    def level_failed(self, hero_num):
        level_failed_text = visual.Label(400, 100, 400, 200, None, self.color['background'])
        level_failed_text.set_text("LEVEL FAILED!", 80, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        name_text = visual.Label(250, 300, 300, 100, None, self.color['background'])
        name_text.set_text("NAME: " + str(self.name), 55, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        score_text = visual.Label(750, 300, 300, 100, None, self.color['background'])
        score_text.set_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        replay = visual.Button(250, 500, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.set_text("TRY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = visual.Button(650, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.set_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        update_rec(self.name, self.score)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action(hero_num, self.name)
                    if exit.isActive():
                        exit.action()

            replay.draw()
            exit.draw()
            level_failed_text.draw()
            score_text.draw()
            name_text.draw()

            pygame.display.update()
            clock.tick(60)

    # запуск уровня
    def start_level(self, birds, pigs, blocks, walls, hero_num):
        loop = True

        slingshot = logic.Slingshot(200, height - 200, 30, 200)

        birds[0].load(slingshot)

        mouse_click = False
        flag = 1

        pigs_to_remove = []
        blocks_to_remove = []

        name_text = visual.Label(100, 10, 100, 50, None, self.color['background'])
        name_text.set_text("NAME: " + str(self.name), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        score_text = visual.Label(550, 10, 100, 50, None, self.color['background'])
        score_text.set_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        birds_remaining = visual.Label(120, 50, 100, 50, None, self.color['background'])
        birds_remaining.set_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        pigs_remaining = visual.Label(110, 90, 100, 50, None, self.color['background'])
        pigs_remaining.set_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        self.draw_map()
                    if event.key == pygame.K_p:
                        self.pause(hero_num)
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if birds[0].mouse_selected():
                        mouse_click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = False
                    if birds[0].mouse_selected():
                        flag = 0

            if (not birds[0].loaded) and all_rest(pigs, birds, blocks):
                print("LOADED!")
                birds.pop(0)
                if self.check_win(pigs, birds) == 1:
                    self.score += len(birds)*100
                    self.level_cleared(hero_num)
                elif self.check_win(pigs,birds) == 0:
                    self.level_failed(hero_num)

                if not birds == []:
                    birds[0].load(slingshot)
                flag = 1

            if mouse_click:
                birds[0].reposition(slingshot, mouse_click)

            if not flag:
                birds[0].unload()

            background_image = pygame.image.load('Images/background.png')
            display.blit(background_image, (0, 0))

            slingshot.draw(birds[0])

            for i in range(len(pigs)):
                for j in range(len(blocks)):
                    pig_v, block_v = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    pigs[i], blocks[j], result_block_pig = logic.collision_handler(pigs[i], blocks[j], "BALL_N_BLOCK")
                    pig_v1, block_v1 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block_pig:
                        if abs(pig_v - pig_v1) > d_velocity:
                            blocks_to_remove.append(blocks[j])
                            blocks[j].destroy()
                        if abs(block_v - block_v1) > d_velocity:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].dead()

            for i in range(len(birds)):
                if not (birds[i].loaded or birds[i].velocity.magnitude == 0):
                    for j in range(len(blocks)):
                        birds_v, block_v = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        birds[i], blocks[j], result_bird_block = logic.collision_handler(birds[i], blocks[j], "BALL_N_BLOCK")
                        birds_v1, block_v1 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude

                        if result_bird_block:
                            if abs(birds_v - birds_v1) > d_velocity:
                                if not blocks[j] in blocks_to_remove:
                                    blocks_to_remove.append(blocks[j])
                                    blocks[j].destroy()

            for i in range(len(pigs)):
                pigs[i].move()
                for j in range(i+1, len(pigs)):
                    pig1_v, pig2_v = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    pigs[i], pigs[j], result = logic.collision_handler(pigs[i], pigs[j], "BALL")
                    pig1_v1, pig2_v1 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    result = True
                    if result:
                        if abs(pig1_v - pig1_v1) > d_velocity:
                            if not pigs[j] in pigs_to_remove:
                                pigs_to_remove.append(pigs[j])
                                pigs[j].dead()
                        if abs(pig2_v - pig2_v1) > d_velocity:
                            if not pigs[i] in pigs_to_remove:
                                pigs_to_remove.append(pigs[i])
                                pigs[i].dead()

                for wall in walls:
                    pigs[i] = wall.collision_manager(pigs[i])

                pigs[i].draw()

            for i in range(len(birds)):
                if (not birds[i].loaded) and birds[i].velocity.magnitude:
                    birds[0].move()
                    for j in range(len(pigs)):
                        bird_v, pig_v = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        birds[i], pigs[j], result_bird_pig = logic.collision_handler(birds[i], pigs[j], "BALL")
                        bird_v1, pig_v1 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        result = True
                        if result_bird_pig:
                            if abs(bird_v - bird_v1) > d_velocity:
                                if not pigs[j] in pigs_to_remove:
                                    pigs_to_remove.append(pigs[j])
                                    pigs[j].dead()

                if birds[i].loaded:
                    birds[i].project_path()

                for wall in walls:
                    birds[i] = wall.collision_manager(birds[i])

                birds[i].draw()

            for i in range(len(blocks)):
                for j in range(i + 1, len(blocks)):
                    block1_v, block2_v = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    blocks[i], blocks[j], result_block = logic.block_collision_handler(blocks[i], blocks[j])
                    block1_v1, block2_v1 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block:
                        if abs(block1_v - block1_v1) > d_velocity:
                            if not blocks[j] in blocks_to_remove:
                                blocks_to_remove.append(blocks[j])
                                blocks[j].destroy()
                        if abs(block2_v - block2_v1) > d_velocity:
                            if not blocks[i] in blocks_to_remove:
                                blocks_to_remove.append(blocks[i])
                                blocks[i].destroy()

                blocks[i].move()

                for wall in walls:
                    blocks[i] = wall.collision_manager(blocks[i], "BLOCK")

                blocks[i].draw()

            for wall in walls:
                wall.draw()

            score_text.set_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            score_text.draw()
            name_text.draw()

            birds_remaining.set_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            birds_remaining.draw()

            pigs_remaining.set_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            pigs_remaining.draw()

            pygame.display.update()

            if all_rest(pigs, birds, blocks):
                for pig in pigs_to_remove:
                    if pig in pigs:
                        pigs.remove(pig)
                        self.score += 100

                for block in blocks_to_remove:
                    if block in blocks:
                        blocks.remove(block)
                        self.score += 50

                pigs_to_remove = []
                blocks_to_remove = []

            clock.tick(60)