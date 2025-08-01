# character_select.py
import pygame
import os
from button import StoneButton
from background import Background
from character_sprite import CharacterSprite
from player import Player
from settings import WIDTH, HEIGHT

TARGET_SIZE = (400, 400)

class PopupButton:
    def __init__(self, text, pos, size, sound_hover, sound_click):
        self.text = text
        self.base_rect = pygame.Rect(pos, size)
        self.rect = self.base_rect.copy()
        self.sound_hover = sound_hover
        self.sound_click = sound_click
        self.font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 22)
        # Colores más bonitos (botón rosado suave)
        self.base_color = (255, 182, 193)
        self.edge_color = (255, 105, 180)
        self.text_color = (50, 50, 50)
        self.hovered = False
        self.clicked = False
        self.grow_scale = 1.12
        self.played_hover = False

    def draw(self, screen):
        rect = self.rect
        pygame.draw.rect(screen, self.base_color, rect, border_radius=12)
        pygame.draw.rect(screen, self.edge_color, rect, 3, border_radius=12)
        text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                                rect.centery - text_surf.get_height() // 2))

    def update(self, mouse_pos):
        if self.base_rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.rect = self.base_rect.inflate(
                    self.base_rect.width * (self.grow_scale - 1),
                    self.base_rect.height * (self.grow_scale - 1),
                )
                self.hovered = True
                if not self.played_hover:
                    self.sound_hover.play()
                    self.played_hover = True
        else:
            if self.hovered:
                self.rect = self.base_rect.copy()
                self.played_hover = False
            self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.sound_click.play()
            self.clicked = True
        return self.clicked


class CharacterSelectScreen:
    def __init__(self, screen):
        self.screen = screen
        self.bg = Background("assetts/images/backgrounds/frames/", fps=10)
        self.blur_scale = 0.18

        click_sound = pygame.mixer.Sound(os.path.join("assetts/sounds/click.mp3"))
        hover_sound = pygame.mixer.Sound(os.path.join("assetts/sounds/hover.mp3"))

        margin = 40
        btn_width, btn_height = 250, 75
        self.btn_volver = StoneButton("VOLVER", (margin, HEIGHT - btn_height - margin), (btn_width, btn_height), click_sound)

        # Datos de personajes
        self.character_data = [
            {"name": "YAMATO","sprite_path": "assetts/images/characters/yamato/idle.png",
             "sprite_width": 200,"sprite_height": 200,"num_frames": 4,"sprite_scale": 4,
             "max_health": 150,"attack": 25,"speed": 5,},
            {"name": "KIZAME","sprite_path": "assetts/images/characters/kizame/idle.png",
             "sprite_width": 100,"sprite_height": 100,"num_frames": 10,"sprite_scale": 4,
             "max_health": 100,"attack": 30,"speed": 7,},
            {"name": "RIN","sprite_path": "assetts/images/characters/rin/idle.png",
             "sprite_width": 150,"sprite_height": 150,"num_frames": 8,"sprite_scale": 4,
             "max_health": 80,"attack": 40,"speed": 6,},
        ]
        self.descriptions = [
            "Guerrero equilibrado con alta defensa y ataque cuerpo a cuerpo.",
            "Arquero ágil, ataques a distancia y gran velocidad.",
            "Maga con hechizos de área, defensa baja pero gran daño."
        ]

        self.display_sprites = []
        for char_info in self.character_data:
            self.display_sprites.append(CharacterSprite(
                char_info["sprite_path"],char_info["sprite_width"],char_info["sprite_height"],
                char_info["num_frames"],fps=8,scale=char_info["sprite_scale"]))

        self.char_positions = self.calculate_positions_horizontal_centered(
            TARGET_SIZE, len(self.display_sprites), HEIGHT // 2 - 60, WIDTH, separation=-70
        )

        self.selected_index = None
        self.hover_index = None
        self.popup_hover_sound = hover_sound
        self.popup_click_sound = click_sound
        self.close_btn = None
        self.select_btn = None
        self.selected_player_instance = None
        self.should_return_to_menu = False

    def calculate_positions_horizontal_centered(self, size, num_sprites, y_center, screen_width, separation=-70):
        w, h = size
        total_width = num_sprites * w + (num_sprites - 1) * separation
        start_x = (screen_width - total_width) // 2
        positions = [(start_x + i * (w + separation), y_center - h // 2) for i in range(num_sprites)]
        return positions

    def update(self):
        self.bg.update()
        mouse_pos = pygame.mouse.get_pos()
        self.btn_volver.update(mouse_pos)
        self.hover_index = None
        for idx, char_sprite in enumerate(self.display_sprites):
            char_sprite.update()
            rect = pygame.Rect(*self.char_positions[idx], *TARGET_SIZE)
            if rect.collidepoint(mouse_pos):
                self.hover_index = idx

        if self.selected_index is not None:
            box_w, box_h = 560, 340
            box_x, box_y = WIDTH // 2 - box_w // 2, HEIGHT // 2 - box_h // 2
            btn_w, btn_h = 120, 36
            select_w = 170
            btn_margin = 24
            close_btn_pos = (box_x + btn_margin, box_y + box_h - btn_h - btn_margin)
            select_btn_pos = (box_x + box_w - select_w - btn_margin, box_y + box_h - btn_h - btn_margin)
            if not self.close_btn:
                self.close_btn = PopupButton("CERRAR", close_btn_pos, (btn_w, btn_h),
                                             self.popup_hover_sound, self.popup_click_sound)
            else:
                self.close_btn.base_rect.topleft = close_btn_pos
                self.close_btn.rect = self.close_btn.base_rect.copy()
            if not self.select_btn:
                self.select_btn = PopupButton("SELECCIONAR", select_btn_pos, (select_w, btn_h),
                                              self.popup_hover_sound, self.popup_click_sound)
            else:
                self.select_btn.base_rect.topleft = select_btn_pos
                self.select_btn.rect = self.select_btn.base_rect.copy()
            self.close_btn.update(mouse_pos)
            self.select_btn.update(mouse_pos)

    def handle_event(self, event):
        self.selected_player_instance = None
        self.should_return_to_menu = False
        if self.btn_volver.handle_event(event):
            self.should_return_to_menu = True
            self.btn_volver.set_selected(False)
            return True
        if self.selected_index is not None:
            if self.close_btn and self.close_btn.handle_event(event):
                self.selected_index = None
                self.close_btn.clicked = False
                return True
            elif self.select_btn and self.select_btn.handle_event(event):
                info = self.character_data[self.selected_index]
                self.selected_player_instance = Player(
                    name=info["name"],sprite_path=info["sprite_path"],
                    sprite_width=info["sprite_width"],sprite_height=info["sprite_height"],
                    num_frames=info["num_frames"],sprite_scale=info["sprite_scale"],
                    max_health=info["max_health"],attack=info["attack"],speed=info["speed"])
                print(f"Personaje '{self.selected_player_instance.name}' seleccionado.")
                self.selected_index = None
                self.select_btn.clicked = False
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hover_index is not None:
            self.selected_index = self.hover_index
            return True
        return False

    def draw(self):
        frame = self.bg.frames[self.bg.current_frame]
        blur = pygame.transform.smoothscale(frame,
                                            (int(WIDTH * self.blur_scale), int(HEIGHT * self.blur_scale)))
        blur = pygame.transform.smoothscale(blur, (WIDTH, HEIGHT))
        self.screen.blit(blur, (0, 0))
        font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 48)
        txt = font.render("SELECCION DE PERSONAJE", True, (255, 182, 193))  # Texto rosado
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 80))
        for idx, char_sprite in enumerate(self.display_sprites):
            scaled_sprite = pygame.transform.smoothscale(
                char_sprite.frames[char_sprite.current_frame], TARGET_SIZE)
            self.screen.blit(scaled_sprite, self.char_positions[idx])
        self.btn_volver.draw(self.screen)
        if self.selected_index is not None:
            self.draw_character_popup(self.selected_index)

    def draw_character_popup(self, idx):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        box_w, box_h = 560, 340
        box_x, box_y = WIDTH // 2 - box_w // 2, HEIGHT // 2 - box_h // 2
        # Panel rosado pastel
        pygame.draw.rect(self.screen, (255, 182, 193), (box_x, box_y, box_w, box_h), border_radius=30)
        pygame.draw.rect(self.screen, (255, 105, 180), (box_x, box_y, box_w, box_h), 4, border_radius=30)
        sprite_big = pygame.transform.smoothscale(self.display_sprites[idx].frames[0], (110, 110))
        self.screen.blit(sprite_big, (box_x + 40, box_y + 80))
        font_title = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 38)
        font_desc = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 19)
        name_surface = font_title.render(self.character_data[idx]["name"], True, (255, 20, 147))
        self.screen.blit(name_surface, (box_x + 200, box_y + 60))
        desc = self.descriptions[idx]
        max_width = box_w - 220 - 30
        words, lines, temp = desc.split(), [], ""
        for word in words:
            test_line = (temp + " " + word).strip()
            if font_desc.size(test_line)[0] > max_width:
                lines.append(temp)
                temp = word
            else:
                temp = test_line
        if temp: lines.append(temp)
        for i, line in enumerate(lines):
            line_surface = font_desc.render(line, True, (0, 0, 0))
            self.screen.blit(line_surface, (box_x + 200, box_y + 110 + i * 27))
        if self.close_btn and self.select_btn:
            self.close_btn.draw(self.screen)
            self.select_btn.draw(self.screen)
