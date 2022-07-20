import pygame
import sys

import visual

pygame.init()
width = None
height = None
display = None

def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    visual.init(display)

def close():
    pygame.quit()
    sys.exit()
#класс описывающий процесс выбора персонажа
class Choise:
    def __init__(self):
        self.hero = ""
        self.color = {'background': (51, 51, 51)}

    # рисуем доступных персонажей и кнопки
    # при нажатии кнопки, устанавливаем соответсвующего персонажа
    def draw_choise(self):
        loop = True
        text = visual.Label(400, 100, 400, 200, None,  self.color['background'])
        text.set_text("CHOISE YOUR HERO!", 80, "Fonts/Comic_Kings.ttf", (255, 255, 255))

        red = visual.Button(100, 300, 300, 100, None, (241, 148, 138), (245, 183, 177))
        red.set_text("RED", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        yellow = visual.Button(450, 300, 300, 100, None, (244, 208, 63), (247, 220, 111))
        yellow.set_text("YELLOW", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        blue = visual.Button(800, 300, 300, 100, None, (70, 200, 250), (65, 215, 255))
        blue.set_text("BLUE", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if red.isActive():
                        return 1
                    if blue.isActive():
                        return 2
                    if yellow.isActive():
                        return 3


            background_image = pygame.image.load('Images/background.png')
            display.blit(background_image, (0, 0))

            red_image = pygame.image.load('Images/red_bird.png')
            display.blit(red_image, (225, 420))

            yellow_image = pygame.image.load('Images/yellow_bird.png')
            display.blit(yellow_image, (575, 420))

            blue_image = pygame.image.load('Images/blue_bird.png')
            display.blit(blue_image, (925, 420))

            text.draw()
            red.draw()
            yellow.draw()
            blue.draw()

            pygame.display.update()