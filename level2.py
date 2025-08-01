import pygame
import os
import array
import math
from settings import WIDTH, HEIGHT

GROUND_Y = HEIGHT - 100

# ===================== GENERAR SONIDO HIT =====================
def generar_hit_sound():
    sample_rate = 44100
    duration = 0.15
    frequency = 300
    volume = 0.5
    n_samples = int(sample_rate * duration)
    buf = array.array("h", [0] * n_samples)
    for i in range(n_samples):
        t = i / sample_rate
        sample = int(volume * 32767 * math.sin(2 * math.pi * frequency * t) * math.exp(-20 * t))
        buf[i] = sample
    return pygame.mixer.Sound(buffer=buf)

# ===================== GENERAR SONIDO LAMENTO =====================
def generar_lamento_sound():
    sample_rate = 44100
    duration = 1.0
    start_freq = 500
    end_freq = 100
    volume = 0.5
    n_samples = int(sample_rate * duration)
    buf = array.array("h", [0] * n_samples)
    for i in range(n_samples):
        t = i / sample_rate
        freq = start_freq + (end_freq - start_freq) * (i / n_samples)
        sample = int(volume * 32767 * math.sin(2 * math.pi * freq * t) * math.exp(-3 * t))
        buf[i] = sample
    return pygame.mixer.Sound(buffer=buf)

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

        # Cargar animaciones
        self.load_animations(path, scale)

        # Imagen inicial y posición
        self.image = self.animations[self.current_action][0]
        self.rect = self.image.get_rect(midbottom=(900, GROUND_Y))
        self.speed = 2  # Velocidad hacia el jugador

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

    def set_action(self, action):
        if action in self.animations and action != self.current_action:
            self.current_action = action
            self.timer = 0
            self.current_frame = 0

    def update(self):
        if self.current_action not in self.animations:
            return

        # Knockback
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

    def move_towards(self, player_rect):
        if self.rect.centerx > player_rect.centerx:
            self.rect.x -= self.speed
        elif self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ===================== BULLETS =====================
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=12, color=(255, 255, 0)):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()

# ===================== LEVEL TWO =====================
class LevelTwoScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Fondo
        bg_path = "assetts/images/level2/background2.png"
        self.background = pygame.image.load(bg_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Player
        self.player = player
        self.player_rect = self.player.sprite.frames[self.player.sprite.current_frame].get_rect(midbottom=(100, GROUND_Y))
        self.player_speed = 6
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1

        # Salud del jugador (más vida)
        self.player_max_health = 20
        self.player_health = self.player_max_health
        self.player_hit_timer = 0

        # Sonidos
        self.hit_sound = generar_hit_sound()
        self.enemy_death_sound = generar_lamento_sound()

        # Balas jugador
        self.bullets = pygame.sprite.Group()
        snd_path = "assetts/sounds/shoot.wav"
        self.shoot_sound = pygame.mixer.Sound(snd_path) if os.path.exists(snd_path) else None

        # Enemigo
        enemy_path = "assetts/images/enemies/Minotaur_2"
        self.enemy = EnemySprite(enemy_path, scale=3.5)
        self.enemy_health_max = 10
        self.enemy_health = self.enemy_health_max

        # Balas del enemigo
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_shoot_timer = 0

        # Estados
        self.game_over = False
        self.level_completed = False
        self.font = pygame.font.Font(None, 80)
        self.scroll_speed = 4

        # Mensaje inicial
        self.start_message_timer = 120  # 2 segundos
        self.enemy_death_sound_played = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_jumping and not self.game_over:
                self.is_jumping = True
                self.jump_velocity = -15
            if event.key == pygame.K_r and (self.game_over or self.level_completed):
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

    def enemy_shoot(self):
        bullet = Bullet(self.enemy.rect.left, self.enemy.rect.centery, speed=-8, color=(255, 0, 0))
        self.enemy_bullets.add(bullet)

    def update(self):
        if self.start_message_timer > 0:
            self.start_message_timer -= 1
            return None

        if self.game_over:
            return "GAME_OVER"
        if self.level_completed:
            return "LEVEL_COMPLETE"

        keys = pygame.key.get_pressed()
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

        # Actualizar animaciones
        self.player.sprite.update()
        self.enemy.update()
        self.enemy.move_towards(self.player_rect)
        self.bullets.update()
        self.enemy_bullets.update()

        # Disparo enemigo
        self.enemy_shoot_timer += 1
        if self.enemy_shoot_timer > 90 and self.enemy_health > 0:
            self.enemy_shoot()
            self.enemy_shoot_timer = 0

        # Colisiones balas jugador-enemigo
        for b in self.bullets:
            if self.enemy.rect.colliderect(b.rect) and self.enemy_health > 0:
                b.kill()
                self.enemy_health -= 1
                self.enemy.knockback = -10

        # Colisiones balas enemigo-jugador
        for eb in self.enemy_bullets:
            if self.player_rect.colliderect(eb.rect):
                eb.kill()
                self.player_health -= 2
                self.hit_sound.play()
                self.player_hit_timer = 15
                if self.player_health <= 0:
                    self.game_over = True

        # Colisión jugador-enemigo
        if self.enemy_health > 0 and self.enemy.rect.colliderect(self.player_rect):
            if self.player_hit_timer == 0:
                self.player_health -= 1
                self.hit_sound.play()
                self.player_hit_timer = 20
                self.player_rect.x -= 30
                if self.player_health <= 0:
                    self.game_over = True

        # Temporizador de daño
        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        # Animación muerte enemigo con sonido
        if self.enemy_health <= 0:
            self.enemy.set_action("Dead")
            if not self.enemy_death_sound_played:
                self.enemy_death_sound.play()
                self.enemy_death_sound_played = True
            if self.enemy.dead_animation_done:
                self.level_completed = True

        return None

    def draw_health_bars(self):
        # Barra jugador
        bar_width = 200
        bar_height = 20
        ratio = self.player_health / self.player_max_health
        border_rect = pygame.Rect(20, 20, bar_width, bar_height)
        fill_rect = pygame.Rect(20, 20, int(bar_width * ratio), bar_height)
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect, border_radius=5)
        pygame.draw.rect(self.screen, (0, 200, 0), fill_rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2, border_radius=5)

        # Texto jugador
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.player_health} / {self.player_max_health}", True, (255, 255, 255))
        self.screen.blit(text, (border_rect.x + bar_width + 10, border_rect.y))

        # Barra enemigo
        e_bar_width = self.enemy.rect.width
        e_bar_height = 10
        e_ratio = self.enemy_health / self.enemy_health_max
        e_bar_rect = pygame.Rect(self.enemy.rect.x, self.enemy.rect.y - 15, e_bar_width, e_bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), e_bar_rect, border_radius=3)
        pygame.draw.rect(self.screen, (200, 0, 0), (e_bar_rect.x, e_bar_rect.y, int(e_bar_width * e_ratio), e_bar_height), border_radius=3)

        # Texto enemigo
        enemy_font = pygame.font.Font(None, 20)
        enemy_text = enemy_font.render(f"{self.enemy_health} / {self.enemy_health_max}", True, (255, 255, 255))
        self.screen.blit(enemy_text, (e_bar_rect.x + e_bar_width + 5, e_bar_rect.y - 5))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.enemy.draw(self.screen)

        # Jugador
        frame = self.player.sprite.frames[self.player.sprite.current_frame]
        if self.player_hit_timer % 4 < 2 and self.player_hit_timer > 0:
            tinted = frame.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(tinted, self.player_rect)
        else:
            self.screen.blit(frame, self.player_rect)

        # Texto nivel
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Nivel 2", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

        # Mensaje inicial
        if self.start_message_timer > 0:
            msg_font = pygame.font.Font(None, 60)
            msg = msg_font.render("¡Buena suerte derrotando al enemigo!", True, (255, 255, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))

        # Barras de salud
        self.draw_health_bars()

        # Mensajes finales
        if self.game_over:
            msg = self.font.render("GAME OVER", True, (180, 0, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            retry_msg = pygame.font.Font(None, 40).render("Presiona 'R' para Reintentar", True, (255, 255, 255))
            self.screen.blit(retry_msg, (WIDTH // 2 - retry_msg.get_width() // 2, HEIGHT // 2 + 80))
        elif self.level_completed:
            fancy_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 60)
            msg = fancy_font.render("NIVEL COMPLETADO", True, (0, 255, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))


# Función externa para aumentar dificultad
def aumentar_dificultad(level_obj, incremento=1):
    """Aumenta la velocidad del enemigo y la frecuencia de disparo"""
    level_obj.enemy.speed += incremento
    level_obj.enemy_shoot_timer = max(0, level_obj.enemy_shoot_timer - incremento * 10)
    level_obj.enemy.animation_speed += 0.05
