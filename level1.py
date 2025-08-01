import pygame
import os
from settings import WIDTH, HEIGHT

GROUND_Y = HEIGHT - 100

# ===================== ENEMY SPRITE =====================
class EnemySprite:
    def __init__(self, path, scale=3.5):
        self.animations = {}
        self.current_action = "Walk"
        self.current_frame = 0
        self.animation_speed = 0.15
        self.timer = 0
        self.dead_animation_done = False
        self.knockback = 0
        self.load_animations(path, scale)
        self.image = self.animations[self.current_action][0]
        self.rect = self.image.get_rect(midbottom=(900, GROUND_Y))

    def load_animations(self, path, scale):
        actions = ["Walk", "Dead"]
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

    def set_action(self, action):
        if action in self.animations and action != self.current_action:
            self.current_action = action
            self.timer = 0
            self.current_frame = 0

    def update(self):
        if self.knockback > 0:
            self.rect.x += self.knockback
            self.knockback -= 1
        if self.current_action == "Dead" and self.dead_animation_done:
            return
        self.timer += self.animation_speed
        if self.timer >= len(self.animations[self.current_action]):
            if self.current_action == "Dead":
                self.dead_animation_done = True
            self.timer = 0
        self.current_frame = int(self.timer)
        self.image = self.animations[self.current_action][self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ===================== BULLET =====================
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 12

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()


# ===================== LEVEL ONE =====================
class LevelOneScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Música más baja
        pygame.mixer.music.set_volume(0.3)

        # Fondo
        bg_path = "assetts/images/level1/background.png"
        self.background = pygame.image.load(bg_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Player
        self.player = player
        self.player_rect = self.player.sprite.frames[self.player.sprite.current_frame].get_rect(midbottom=(100, GROUND_Y))
        self.player_speed = 5
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1

        # Salud jugador (más vida)
        self.player_max_health = 20
        self.player_health = self.player_max_health
        self.player_hit_timer = 0

        # Balas
        self.bullets = pygame.sprite.Group()
        snd_path = "assetts/sounds/shoot.wav"
        self.shoot_sound = pygame.mixer.Sound(snd_path) if os.path.exists(snd_path) else None
        if self.shoot_sound:
            self.shoot_sound.set_volume(1.0)  # disparo más fuerte

        # Enemigo único (lento)
        enemy_path = "assetts/images/enemies/Minotaur_2"
        self.enemy = EnemySprite(enemy_path, scale=3.5)
        self.enemy_health_max = 15
        self.enemy_health = self.enemy_health_max
        self.enemy_speed = 1  # más lento

        # Sonidos
        hit_path = "assetts/sounds/hit.wav"
        self.hit_sound = pygame.mixer.Sound(hit_path) if os.path.exists(hit_path) else None
        lament_path = "assetts/sounds/lament.wav"
        self.lament_sound = pygame.mixer.Sound(lament_path) if os.path.exists(lament_path) else None

        # Estados
        self.game_over = False
        self.level_completed = False
        self.font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 40)
        self.completion_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_jumping and not self.game_over:
                self.is_jumping = True
                self.jump_velocity = -15
            if event.key == pygame.K_r and self.game_over:
                self.__init__(self.screen, self.player)
            if event.key == pygame.K_z and not self.game_over:
                self.shoot()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
            self.shoot()

    def shoot(self):
        b = Bullet(self.player_rect.right, self.player_rect.centery)
        self.bullets.add(b)
        if self.shoot_sound:
            self.shoot_sound.play()

    def update(self):
        if self.game_over:
            return None
        if self.level_completed:
            self.completion_timer += 1
            if self.completion_timer > 120:
                return "NEXT_LEVEL"
            return None

        keys = pygame.key.get_pressed()
        # WASD completo
        if keys[pygame.K_w] and self.player_rect.top > 0:
            self.player_rect.y -= self.player_speed
        if keys[pygame.K_s] and self.player_rect.bottom < HEIGHT:
            self.player_rect.y += self.player_speed
        if keys[pygame.K_a] and self.player_rect.left > 0:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_d] and self.player_rect.right < WIDTH:
            self.player_rect.x += self.player_speed

        # Saltos
        if self.is_jumping:
            self.player_rect.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y
                self.is_jumping = False

        # Animaciones
        self.player.sprite.update()
        self.enemy.update()
        self.bullets.update()

        # Movimiento enemigo lento hacia el jugador
        if self.enemy_health > 0:
            self.enemy.set_action("Walk")
            if self.enemy.rect.centerx > self.player_rect.centerx:
                self.enemy.rect.x -= self.enemy_speed
            else:
                self.enemy.rect.x += self.enemy_speed
        else:
            self.enemy.set_action("Dead")
            if self.enemy.dead_animation_done and not self.level_completed:
                self.level_completed = True
                if self.lament_sound:
                    self.lament_sound.play()

        # Colisiones balas-enemigo
        for b in self.bullets:
            if self.enemy.rect.colliderect(b.rect) and self.enemy_health > 0:
                b.kill()
                self.enemy_health -= 1
                self.enemy.knockback = -10
                if self.hit_sound:
                    self.hit_sound.play()

        # Colisión enemigo-jugador
        if self.enemy_health > 0 and self.enemy.rect.colliderect(self.player_rect):
            self.player_health -= 1
            self.player_hit_timer = 15
            if self.player_health <= 0:
                self.game_over = True

        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        return None

    def draw_health_bars(self):
        # Barra jugador con número
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, 200, 20))
        pygame.draw.rect(self.screen, (0, 200, 0), (20, 20, int(200 * (self.player_health / self.player_max_health)), 20))
        font_small = pygame.font.Font(None, 24)
        text = font_small.render(f"{self.player_health}/{self.player_max_health}", True, (255, 255, 255))
        self.screen.blit(text, (20 + 210, 18))

        # Barra enemigo con número
        e_ratio = self.enemy_health / self.enemy_health_max
        pygame.draw.rect(self.screen, (50, 50, 50), (self.enemy.rect.x, self.enemy.rect.y - 15, self.enemy.rect.width, 10))
        pygame.draw.rect(self.screen, (200, 0, 0), (self.enemy.rect.x, self.enemy.rect.y - 15, int(self.enemy.rect.width * e_ratio), 10))
        e_text = font_small.render(f"{self.enemy_health}/{self.enemy_health_max}", True, (255, 255, 255))
        self.screen.blit(e_text, (self.enemy.rect.x, self.enemy.rect.y - 30))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.bullets.draw(self.screen)
        self.enemy.draw(self.screen)

        frame = self.player.sprite.frames[self.player.sprite.current_frame]
        if self.player_hit_timer % 4 < 2 and self.player_hit_timer > 0:
            tinted = frame.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(tinted, self.player_rect)
        else:
            self.screen.blit(frame, self.player_rect)

        self.draw_health_bars()

        if self.game_over:
            msg = self.font.render("GAME OVER", True, (180, 0, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        elif self.level_completed:
            msg = self.font.render("NIVEL COMPLETADO", True, (0, 255, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
