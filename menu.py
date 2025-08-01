# menu.py
import pygame
import os
from button import StoneButton
from background import Background
from settings import WIDTH, HEIGHT

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg = Background("assetts/images/backgrounds/frames/", fps=10)

        font_path = "assetts/fonts/PressStart2P-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 80)
        self.mist_font = pygame.font.Font(font_path, 160)

        click_sound = pygame.mixer.Sound(os.path.join("assetts/sounds/click.mp3"))

        margin = 40
        btn_width, btn_height = 340, 75
        
        self.btn_personajes = StoneButton(
            "PERSONAJES",
            (WIDTH - btn_width - margin, HEIGHT - btn_height - margin),
            (btn_width, btn_height),
            click_sound
        )
        self.btn_salir = StoneButton(
            "SALIR",
            (margin, HEIGHT - btn_height - margin),
            (btn_width, btn_height),
            click_sound
        )
        self.buttons = [self.btn_personajes, self.btn_salir]

    def draw(self):
        self.bg.draw(self.screen)
        x_base = 60
        y_base = 80

        white_color = (255, 255, 255)
        golden_color = (255, 215, 0)

        the_surface = self.title_font.render("THE", True, white_color)
        self.screen.blit(the_surface, (x_base, y_base))
        current_y = y_base + the_surface.get_height() + 40

        legacy_surface = self.title_font.render("LEGACY", True, white_color)
        mist_surface = self.mist_font.render("MIST", True, golden_color)
        
        self.screen.blit(legacy_surface, (x_base, current_y))
        
        mist_x = x_base + legacy_surface.get_width() + 60
        mist_y = current_y - (mist_surface.get_height() - legacy_surface.get_height()) // 2 
        self.screen.blit(mist_surface, (mist_x, mist_y))
        
        current_y += self.title_font.get_height() + 40

        ofthe_surface = self.title_font.render("OF THE", True, white_color)
        self.screen.blit(ofthe_surface, (x_base, current_y))

        for btn in self.buttons:
            btn.draw(self.screen)

    def update(self):
        self.bg.update()
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse_pos)

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                for other_btn in self.buttons:
                    if other_btn != btn:
                        other_btn.set_selected(False)
                return True
        return False