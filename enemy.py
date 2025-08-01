import pygame
import os

class EnemySprite:
    def __init__(self, path, scale=1.2):  # misma escala que el personaje
        self.animations = {}
        self.current_action = "Walk"  # iniciar caminando
        self.current_frame = 0
        self.animation_speed = 0.15
        self.timer = 0

        # Cargar animaciones
        self.load_animations(path, scale)

        # Imagen inicial y posición
        if self.current_action in self.animations:
            self.image = self.animations[self.current_action][0]
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(900, 550))  # ajusta si quieres otra posición inicial

    def load_animations(self, path, scale):
        actions = ["Idle", "Walk", "Attack", "Hurt", "Dead"]
        for action in actions:
            action_path = os.path.join(path, f"{action}.png")
            if os.path.exists(action_path):
                sheet = pygame.image.load(action_path).convert_alpha()
                frame_height = sheet.get_height()
                frame_width = frame_height
                frame_count = sheet.get_width() // frame_width
                frames = []
                for i in range(frame_count):
                    frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
                    frames.append(frame)
                self.animations[action] = frames
            else:
                print(f"Advertencia: No se encontró la animación {action_path}")

    def set_action(self, action):
        if action in self.animations and action != self.current_action:
            self.current_action = action
            self.timer = 0
            self.current_frame = 0

    def update(self):
        if self.current_action not in self.animations:
            return
        self.timer += self.animation_speed
        if self.timer >= len(self.animations[self.current_action]):
            self.timer = 0
        self.current_frame = int(self.timer)
        self.image = self.animations[self.current_action][self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
