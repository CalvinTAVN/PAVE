'''
UI elements for PAVE dashboard
'''

import pygame
from pygame.locals import *
pygame.init()

# Colors
colors = {
    "bg": (11, 20, 39),
    "sec": (64, 121, 140),
    "green": (35, 206, 107),
    "red": (249, 112, 104),
    "white": (237, 245, 252)
}

# Fonts
fonts = {
    'default': pygame.font.SysFont('Segoe UI', 20),
    'small': pygame.font.SysFont('Segoe UI', 16),
    'large': pygame.font.SysFont('Segoe UI', 24),
}

# UI elements
class Screen:
    def __init__(self, h, w, elements):
        self.elements = elements
        self.screen = pygame.display.set_mode((h, w), pygame.RESIZABLE)

    def draw(self, screen):
        self.screen.fill(colors['bg'])
        for element in self.elements:
            element.draw(screen, self.screen.get_height(), self.screen.get_width())

    def check_click(self, pos):
        for element in self.elements:
            element.check_click(pos, self.screen.get_height(), self.screen.get_width())

class Button:
    def __init__(self, rect, text, color, font, action):
        self.rect = rect
        self.text = text
        self.color = color
        self.font = font
        self.action = action

    def get_rect(self, h, w):
        return pygame.rect.Rect([self.rect[0] / 100 * w, self.rect[1] / 100 * h, self.rect[2] / 100 * w, self.rect[3] / 100 * h])

    def draw(self, screen, h, w):
        r = self.get_rect(h, w)
        pygame.draw.rect(screen, self.color, r)
        text = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (r.x + 5, r.y + 5))

    def check_click(self, pos, h, w):
        if self.get_rect(h, w).collidepoint(pos):
            self.action()

class H_Slider:
    def __init__(self, rect, text, color, font, low, high):
        self.rect = rect
        self.color = color
        self.font = font
        self.text = text
        self.x = 0
        self.low = low
        self.high = high

    def get_rect(self, h, w):
        return pygame.rect.Rect([self.rect[0] / 100 * w, self.rect[1] / 100 * h, self.rect[2] / 100 * w, self.rect[3] / 100 * h])

    def transform(self, x):
        a = (x - self.low) / (self.high - self.low)
        return a

    def draw(self, screen, h, w):
        r = self.get_rect(h, w)
        pygame.draw.rect(screen, self.color, r)
        pygame.draw.rect(screen, colors['white'], pygame.rect.Rect([
            r.x + self.transform(self.x) * (self.get_rect(h, w).width - 10),
            r.y, 10, r.height
        ]))
        text = self.font.render(f"{self.text} | {self.transform(self.x):.2f}", True, (0, 0, 0))
        screen.blit(text, (r.x + 5, r.y + 5))

    def check_click(self, pos, h, w):
        pass

class V_Slider:
    def __init__(self, rect, text, color, font, low, high):
        self.rect = rect
        self.color = color
        self.font = font
        self.text = text
        self.y = 0
        self.low = low
        self.high = high

    def get_rect(self, h, w):
        return pygame.rect.Rect([self.rect[0] / 100 * w, self.rect[1] / 100 * h, self.rect[2] / 100 * w, self.rect[3] / 100 * h])

    def transform(self, y):
        a = (y - self.low) / (self.high - self.low)
        return a

    def draw(self, screen, h, w):
        r = self.get_rect(h, w)
        pygame.draw.rect(screen, self.color, r)
        pygame.draw.rect(screen, colors['white'], pygame.rect.Rect([
            r.x, r.y + self.transform(self.y) * (self.get_rect(h, w).height - 10),
            r.width, 10
        ]))
        text = self.font.render(f"{self.text} | {self.transform(self.y):.2f}", True, (0, 0, 0))
        screen.blit(text, (r.x + 5, r.y + 5))

    def check_click(self, pos, h, w):
        pass