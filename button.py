# button.py
import pygame

class StoneButton:
    def __init__(self, text, pos, size, click_sound):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.click_sound = click_sound
        self.font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 30)
        self.is_hovered = False
        self.is_selected = False 

        self.base_text_color = (255, 255, 255) 
        self.hover_text_color = (255, 255, 255) 

        self.base_button_color = (150, 75, 75)   
        self.hover_button_color = (200, 100, 100) 
        self.selected_button_color = (255, 215, 0) 

        self.border_color = (0, 0, 0) 
        self.border_thickness = 4     
        self.border_radius = 15       

    def draw(self, screen):
        current_bg_color = self.selected_button_color if self.is_selected else (self.hover_button_color if self.is_hovered else self.base_button_color)
        pygame.draw.rect(screen, current_bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_thickness, border_radius=self.border_radius)

        text_surface = self.font.render(self.text, True, self.base_text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.click_sound.play()
                self.is_selected = True
                return True
            else:
                self.is_selected = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_selected = False 
        return False

    def set_selected(self, selected):
        self.is_selected = selected