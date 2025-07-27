import pygame
import os
import random
from settings import WIDTH, HEIGHT

GROUND_Y = HEIGHT - 100  # posición del suelo

class LevelOneScreen:
    def __init__(self, screen, player_sprite):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # --- FONDO ANIMADO ---
        self.background_frames = []
        bg_path = "assetts/images/level1/background"
        for file in sorted(os.listdir(bg_path)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(bg_path, file)).convert_alpha()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                self.background_frames.append(img)
        self.current_bg_frame = 0
        self.bg_frame_rate = 8
        self.bg_frame_counter = 0

        # --- JUGADOR ---
        self.player_sprite = player_sprite
        self.player_sprite.frames = [
            pygame.transform.scale(frame, (60, 60)).convert_alpha()
            for frame in self.player_sprite.frames
        ]
        self.player_rect = self.player_sprite.frames[0].get_rect(midbottom=(100, GROUND_Y))
        self.player_speed = 5

        # Fisica del salto
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1

        # --- NIEBLA ---
        self.fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.fog.fill((200, 200, 200, 50))
        self.fog_x = -WIDTH

        # --- OBSTACULOS ---
        self.obstacles = []
        self.spawn_timer = 0

        # --- GAME OVER ---
        self.game_over = False
        self.font = pygame.font.Font(None, 60)

        # --- MÚSICA NIVEL ---
        pygame.mixer.music.load("assetts/music/music_nivel1.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_jumping and not self.game_over:
                self.is_jumping = True
                self.jump_velocity = -15
            if event.key == pygame.K_r and self.game_over:
                self.__init__(self.screen, self.player_sprite)

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        # Movimiento horizontal
        if keys[pygame.K_a] and self.player_rect.left > 0:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_d] and self.player_rect.right < WIDTH:
            self.player_rect.x += self.player_speed

        # Salto
        if self.is_jumping:
            self.player_rect.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y
                self.is_jumping = False

        # Actualizar animacion jugador
        self.player_sprite.update()

        # Mover niebla
        self.fog_x += 1
        if self.fog_x > 0:
            self.fog_x = 0

        # Spawnear obstáculos pequeños
        self.spawn_timer += 1
        if self.spawn_timer > 80:
            width = random.randint(25, 40)
            height = random.randint(25, 40)
            x = WIDTH + 50
            y = GROUND_Y - height
            rect = pygame.Rect(x, y, width, height)
            self.obstacles.append(rect)
            self.spawn_timer = 0

        # Mover obstaculos
        for rect in self.obstacles:
            rect.x -= 6

        # Colisiones
        for rect in self.obstacles:
            if self.player_rect.colliderect(rect):
                self.game_over = True

        # Fondo animado
        self.bg_frame_counter += 1
        if self.bg_frame_counter >= self.bg_frame_rate:
            self.current_bg_frame = (self.current_bg_frame + 1) % len(self.background_frames)
            self.bg_frame_counter = 0

    def draw(self):
        # Fondo
        self.screen.blit(self.background_frames[self.current_bg_frame], (0, 0))

        # Obstaculos
        for rect in self.obstacles:
            pygame.draw.rect(self.screen, (200, 0, 0), rect)

        # Jugador
        current_frame = self.player_sprite.frames[self.player_sprite.current_frame]
        self.screen.blit(current_frame, self.player_rect)

        # Niebla
        self.screen.blit(self.fog, (self.fog_x, 0))

        # Game Over
        if self.game_over:
            text = self.font.render("GAME OVER - R para reiniciar", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
