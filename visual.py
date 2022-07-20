import pygame
import sys

pygame.init()
display = None

def init(screen):
    global display
    display = screen
# класс описывающий кнопки
class Button:
    def __init__(self, x, y, w, h, action=None, colorNotActive=(189, 195, 199), colorActive=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.colorActive = colorActive
        self.colorNotActive = colorNotActive

        self.action = action

        self.font = None
        self.text = None
        self.text_pos = None

    # устанвка текста
    def set_text(self, text, size=20, font="Times New Roman", text_color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, text_color)
        self.text_pos = self.text.get_rect()

        self.text_pos.center = (self.x + self.w/2, self.y + self.h/2)

    # открисовка уровня
    def draw(self):
        if self.isActive():
            if not self.colorActive == None:
                pygame.draw.rect(display, self.colorActive, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.colorNotActive, (self.x, self.y, self.w, self.h))

        if self.text:
            display.blit(self.text, self.text_pos)

    # проверка, наведен ли курсор на кнопку
    def isActive(self):
        pos = pygame.mouse.get_pos()

        if (self.x < pos[0] < self.x + self.w) and (self.y < pos[1] < self.y + self.h):
            return True
        else:
            return False
# класс, описывающий текс, выводимый на экран(label), наследуется от кнопки, но перееопределена функция отрисовки
class Label(Button):
    def draw(self):
        if self.text:
            display.blit(self.text, self.text_pos)

    def move(self, x, y):
        self.x = x
        self.y = y


#класс для поля ввода
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0,0,0)
        self.font = pygame.font.Font("Fonts/arfmoochikncheez.ttf", 45)
        self.text = text
        self.txt_surface = pygame.font.Font(None, 60).render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        global name
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    name = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 60).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
