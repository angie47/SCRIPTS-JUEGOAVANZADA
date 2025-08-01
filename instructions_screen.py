# instructions_screen.py
import pygame
import os
from background import Background
from button import StoneButton
from settings import WIDTH, HEIGHT

class InstructionsScreen:
    def __init__(self, screen, click_sound):
        self.screen = screen
        self.bg = Background("assetts/images/backgrounds/frames/", fps=10)
        self.click_sound = click_sound

        self.title_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 60)
        self.text_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 20)
        self.small_text_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 16)

        self.instructions_text = [
        "Bienvenido a THE LEGACY OF THE MIST!",
         "",
         "Tu objetivo es guiar a tu personaje a través de los niveles,",
         "derrotando enemigos y superando desafíos.",
         "",
         "Controles:",
         "- Flechas del teclado / WASD: Mover al personaje.",
         "- Barra Espaciadora: Saltar.",
         "- Tecla 'Z' / Clic Izquierdo: Ataque básico.",
         "",
        "Consejo:",
        "Mantente en movimiento y esquiva los ataques enemigos.",
        "",
         "¡Buena suerte, aventurero!"
]

        margin = 40
        btn_width, btn_height = 300, 70

        self.btn_volver = StoneButton(
            "VOLVER AL MAPA",
            (WIDTH // 2 - btn_width // 2, HEIGHT - btn_height - margin),
            (btn_width, btn_height),
            self.click_sound
        )
        
        self.should_return_to_map = False

    def draw(self):
        self.bg.draw(self.screen)
        
        title_surface = self.title_font.render("INSTRUCCIONES", True, (255, 255, 255))
        self.screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 80))

        start_y = 200
        for line in self.instructions_text:
            current_font = self.small_text_font if not line.strip() else self.text_font
            line_surface = current_font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, start_y))
            start_y += current_font.get_height() + 5

        self.btn_volver.draw(self.screen)

    def update(self):
        self.bg.update()
        mouse_pos = pygame.mouse.get_pos()
        self.btn_volver.update(mouse_pos)

    def handle_event(self, event):
        self.should_return_to_map = False

        if self.btn_volver.handle_event(event):
            self.should_return_to_map = True
            return True
        return False