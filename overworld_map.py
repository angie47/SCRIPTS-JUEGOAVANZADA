# overworld_map.py
import pygame
import os
from background import Background
from button import StoneButton
from settings import WIDTH, HEIGHT

class OverworldMap:
    def __init__(self, screen, click_sound):
        self.screen = screen
        self.bg = Background("assetts/images/backgrounds/frames/", fps=10)
        self.click_sound = click_sound

        self.font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 36)
        self.title_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 60)

        self.levels = [
            {"name": "NIVEL 1", "position": (WIDTH // 2 - 150, HEIGHT // 2 - 100), "state": "NIVEL1"},
            {"name": "NIVEL 2", "position": (WIDTH // 2 - 150, HEIGHT // 2 + 0), "state": "NIVEL2"},
            {"name": "NIVEL 3", "position": (WIDTH // 2 - 150, HEIGHT // 2 + 100), "state": "NIVEL3"}
        ]
        self.level_buttons = []
        btn_width, btn_height = 300, 70

        for level_data in self.levels:
            btn = StoneButton(
                level_data["name"],
                level_data["position"],
                (btn_width, btn_height),
                self.click_sound
            )
            self.level_buttons.append(btn)

        margin = 40
        self.btn_volver_menu = StoneButton(
            "VOLVER AL MENU",
            (margin, HEIGHT - btn_height - margin),
            (btn_width + 50, btn_height),
            self.click_sound
        )
        
        self.btn_instrucciones = StoneButton(
            "INSTRUCCIONES",
            (WIDTH - btn_width - margin, HEIGHT - btn_height - margin),
            (btn_width + 50, btn_height),
            self.click_sound
        )

        self.selected_level_state = None
        self.should_return_to_menu = False
        self.should_show_instructions = False

    def draw(self):
        self.bg.draw(self.screen)

        title_surface = self.title_font.render("MAPA DE NIVELES", True, (255, 255, 255))
        self.screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 80))

        for btn in self.level_buttons:
            btn.draw(self.screen)

        self.btn_volver_menu.draw(self.screen)
        self.btn_instrucciones.draw(self.screen)

    def update(self):
        self.bg.update()
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.level_buttons:
            btn.update(mouse_pos)
        self.btn_volver_menu.update(mouse_pos)
        self.btn_instrucciones.update(mouse_pos)

    def handle_event(self, event):
        self.selected_level_state = None
        self.should_return_to_menu = False
        self.should_show_instructions = False

        for i, btn in enumerate(self.level_buttons):
            if btn.handle_event(event):
                self.selected_level_state = self.levels[i]["state"]
                for other_btn in self.level_buttons + [self.btn_volver_menu, self.btn_instrucciones]:
                    if other_btn != btn:
                        other_btn.set_selected(False)
                return True

        if self.btn_volver_menu.handle_event(event):
            self.should_return_to_menu = True
            for other_btn in self.level_buttons + [self.btn_instrucciones]:
                other_btn.set_selected(False)
            return True
        
        if self.btn_instrucciones.handle_event(event):
            self.should_show_instructions = True
            for other_btn in self.level_buttons + [self.btn_volver_menu]:
                other_btn.set_selected(False)
            return True

        return False