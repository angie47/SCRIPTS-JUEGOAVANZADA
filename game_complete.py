import pygame
import os
from settings import WIDTH, HEIGHT

class GameCompleteScreen:
    def __init__(self, screen):
        self.screen = screen
        # Fondo del menú (usa tu imagen)
        bg_path = "assetts/images/menu_background.png"
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        else:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0, 0, 0))

        # Fuentes retro
        self.font_title = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 50)
        self.font_sub = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 28)
        self.font_hint = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 22)

        self.done = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.done = True

    def update(self):
        pass

    def draw_text_with_shadow(self, text, font, color, x, y):
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x + 2, y + 2))
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))

    def draw(self):
        # Fondo
        self.screen.blit(self.background, (0, 0))

        # Mensajes
        title = "¡FELICIDADES!"
        sub = "¡Has completado todos los niveles!"
        hint = "Presiona [M] para volver al menú"

        self.draw_text_with_shadow(title, self.font_title, (0, 255, 0), WIDTH // 2 - 200, HEIGHT // 2 - 120)
        self.draw_text_with_shadow(sub, self.font_sub, (255, 255, 0), WIDTH // 2 - 300, HEIGHT // 2 - 50)
        self.draw_text_with_shadow(hint, self.font_hint, (255, 255, 255), WIDTH // 2 - 250, HEIGHT // 2 + 50)
