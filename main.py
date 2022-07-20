import pygame
import sys

import maps
import heroes
import visual
import logic
import objects

#параметры окна
pygame.init()
width = 1200
height = 679
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
background_image = pygame.image.load('Images/background.png')
display.blit(background_image, (0,0))
pygame.display.set_caption('My Angry Birds')
icon = pygame.image.load("Images/red_bird.png")
pygame.display.set_icon(icon)

heroes.init(display)
logic.init(display)
objects.init(display)
maps.init(display)
#visual.init(display)

background = (51, 51, 51)
#функция выхода из игры
def close():
    pygame.quit()
    sys.exit()
#функция выбора персонажа
def choise(hero):
    num = hero.draw_choise()
    return num
#функция начала игры
def start_game(map, hero_num, name):
    map.draw_map(hero_num, name)

def input_name():
    input_box = visual.InputBox(width/2 - 100, height / 2 - 50, 300, 100)
    start_button = visual.Button(width / 2 - 320, height / 2 + 100, 300, 100, None, (88, 214, 141), (171, 235, 198))
    start_button.set_text("Start", 80, "Fonts/arfmoochikncheez.ttf", (0,0,0))
    exit_button = visual.Button(width / 2 + 20, height / 2 + 100, 300, 100, None, (241, 148, 138), (245, 183, 177))
    exit_button.set_text("Exit", 80, "Fonts/arfmoochikncheez.ttf",(0,0,0) )
    game_name = visual.Label(width / 2 - 150, height / 2 - 280, 300, 100, None, None)
    game_name.set_text("Enter your name", 50, "Fonts/arfmoochikncheez.ttf", (240,240,240))
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                    return input_box.text
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isActive():
                    done = True
                    return input_box.text
                if exit_button.isActive():
                    return 0
            input_box.handle_event(event)

        input_box.update()

        display.blit(background_image, (0, 0))
        input_box.draw(display)
        game_name.draw()
        start_button.draw()
        exit_button.draw()

        pygame.display.flip()
        clock.tick(30)

#показать рекорды
def view_rec():
    i=1;
    with open("records.txt", "rt") as file:
        label = visual.Label(width / 2 - 150, i*50, 300, 100, None)
        text = visual.Label(width / 2 - 150, height / 2 - 350, 300, 100, None)
        text.set_text('Records', 48, "Fonts/Comic_Kings.ttf", (240,240,240))
        display.blit(background_image, (0, 0))
        text.draw()
        for line in file.readlines():
            label.set_text(str(i) + ". "+line, 24, "Fonts/Comic_Kings.ttf", (0,0,0))
            label.draw()
            i+=1
            label.move(width / 2 - 150, i*50)
    file.close()

    button = visual.Button(width / 2 - 100, height / 2 + 250, 200, 70, None, (88, 214, 141), (171, 235, 198))
    button.set_text("Back", 55, "Fonts/arfmoochikncheez.ttf", (0,0,0))
    button.draw()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.isActive():
                    return

        button.draw()
        pygame.display.update()
        clock.tick(20)
#отрисовка начального экрана
def GAME():
    map = maps.Maps()
    hero = heroes.Choise()
    num = None

    title = visual.Label(440, 10, 320, 200, None, background)
    title.set_text("ANGRY BIRDS", 80, "Fonts/arfmoochikncheez.ttf", (255, 255, 255))

    start = visual.Button(430, 150, 340, 100, start_game, (88, 214, 141), (171, 235, 198))
    start.set_text("START GAME", 60, "Fonts/arfmoochikncheez.ttf", background)

    choice_hero = visual.Button(430, 270, 340, 100, choise, (244, 208, 63), (247, 220, 111))
    choice_hero.set_text("CHOISE HERO", 60, "Fonts/arfmoochikncheez.ttf", background)

    record = visual.Button(430, 390, 340, 100, view_rec, (244, 208, 63), (247, 220, 111))
    record.set_text("RECORD", 60, "Fonts/arfmoochikncheez.ttf", background)

    exit = visual.Button(430, 510, 340, 100, close, (241, 148, 138), (245, 183, 177))
    exit.set_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", background)

    me= visual.Label(450, 600, 300, 100, None, background)
    me.set_text("Created by...", 60, "Fonts/arfmoochikncheez.ttf", (100, 100, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit.isActive():
                    exit.action()
                if record.isActive():
                    record.action()
                if start.isActive():
                    name =input_name()
                    if name:
                        start_game(map, num, name)
                if choice_hero.isActive():
                    num = choice_hero.action(hero)


        #display.fill(background)
        display.blit(background_image, (0,0))

        start.draw()
        record.draw()
        choice_hero.draw()
        exit.draw()
        title.draw()
        me.draw()

        pygame.display.update()
        clock.tick(60)

GAME()