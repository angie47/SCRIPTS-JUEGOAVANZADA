import pygame
import os
from settings import WIDTH, HEIGHT

GROUND_Y = HEIGHT - 100

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
        actions = ["Walk", "Attack", "Dead"]
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
                print(f"Advertencia: No se encontró {action_path}")

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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 5))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 15
        self.trail = []

    def update(self):
        self.trail.append((self.rect.x, self.rect.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

    def draw(self, screen):
        for t in self.trail:
            pygame.draw.rect(screen, (255, 200, 0), (t[0], t[1], 20, 3), border_radius=2)
        screen.blit(self.image, self.rect)


class LevelThreeScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assetts/images/level3/background3.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.player = player
        self.player_rect = self.player.sprite.frames[self.player.sprite.current_frame].get_rect(midbottom=(100, GROUND_Y))
        self.player_speed = 6
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1
        self.last_space_press_time = 0
        self.double_jump = False

        # VIDA AUMENTADA
        self.player_max_health = 30
        self.player_health = self.player_max_health
        self.player_hit_timer = 0

        self.bullets = pygame.sprite.Group()
        self.shoot_sound = pygame.mixer.Sound("assetts/sounds/shoot.wav") if os.path.exists("assetts/sounds/shoot.wav") else None
        self.hit_sound = pygame.mixer.Sound("assetts/sounds/hit.wav") if os.path.exists("assetts/sounds/hit.wav") else None
        self.enemy_death_sound = pygame.mixer.Sound("assetts/sounds/lament.wav") if os.path.exists("assetts/sounds/lament.wav") else None
        self.enemy_death_sound_played = False

        self.laugh_sound = pygame.mixer.Sound("assetts/sounds/laugh.mp3") if os.path.exists("assetts/sounds/laugh.mp3") else None

        self.enemy = EnemySprite("assetts/images/enemies/Minotaur_1", scale=3.5)
        self.enemy_health_max = 8
        self.enemy_health = self.enemy_health_max
        self.enemy_start_pos = self.enemy.rect.x

        self.respawn_timer = 0
        self.respawn_count = 0

        self.attack_cooldown = 0
        self.enemy_speed = 2
        self.enemy_damage = 2
        self.bullet_damage = 1
        self.game_over = False
        self.level_completed = False
        self.font = pygame.font.Font(None, 80)

        self.revive_message_timer = 0
        self.player_dialogue_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                now = pygame.time.get_ticks()
                if now - self.last_space_press_time < 300:
                    self.is_jumping = True
                    self.jump_velocity = -25
                    self.double_jump = True
                else:
                    self.is_jumping = True
                    self.jump_velocity = -15
                    self.double_jump = False
                self.last_space_press_time = now
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

    def update(self):
        if self.game_over:
            return None
        if self.level_completed:
            return "LEVEL_COMPLETE"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed

        if self.is_jumping:
            self.player_rect.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y
                self.is_jumping = False

        self.player.sprite.update()
        self.enemy.update()
        self.bullets.update()

        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0 and self.respawn_count < 3:
                self.enemy_health_max += 3
                self.enemy_health = self.enemy_health_max
                self.enemy.dead_animation_done = False
                self.enemy.set_action("Walk")
                self.enemy.rect.x = self.enemy_start_pos
                self.respawn_count += 1
                self.enemy_speed += 1
                self.enemy_damage += 1
                if self.laugh_sound:
                    pygame.mixer.music.set_volume(0.2)
                    self.laugh_sound.play()
                    pygame.mixer.music.set_volume(0.7)
                self.revive_message_timer = 120
                self.player_dialogue_timer = 90

        if self.enemy_health > 0:
            dist = abs(self.enemy.rect.centerx - self.player_rect.centerx)
            if dist > 100:
                self.enemy.set_action("Walk")
                if self.enemy.rect.centerx > self.player_rect.centerx:
                    self.enemy.rect.x -= self.enemy_speed
                else:
                    self.enemy.rect.x += self.enemy_speed
            else:
                self.enemy.set_action("Attack")
                if self.enemy.current_frame == len(self.enemy.animations["Attack"]) - 1 and self.attack_cooldown == 0:
                    self.player_health -= self.enemy_damage
                    self.player_rect.x -= 15 if self.enemy.rect.centerx < self.player_rect.centerx else -15
                    self.player_hit_timer = 20
                    self.attack_cooldown = 30
                    if self.hit_sound:
                        self.hit_sound.play()
                    if self.player_health <= 0:
                        self.game_over = True
        else:
            self.enemy.set_action("Dead")
            if not self.enemy_death_sound_played and self.enemy.dead_animation_done:
                if self.enemy_death_sound:
                    self.enemy_death_sound.play()
                self.enemy_death_sound_played = True

            if self.enemy.dead_animation_done and self.respawn_timer == 0:
                if self.respawn_count < 3:
                    self.respawn_timer = 120
                else:
                    self.level_completed = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        for b in self.bullets:
            if self.enemy.rect.colliderect(b.rect) and self.enemy_health > 0:
                b.kill()
                self.enemy_health -= self.bullet_damage
                self.enemy.knockback = -10

        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        return None

    def draw_health_bars(self):
        font = pygame.font.Font(None, 28)

        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, 200, 20))
        pygame.draw.rect(self.screen, (0, 200, 0), (20, 20, int(200 * (self.player_health / self.player_max_health)), 20))
        text = font.render(f"{self.player_health}/{self.player_max_health}", True, (255, 255, 255))
        self.screen.blit(text, (25, 22))

        e_ratio = self.enemy_health / self.enemy_health_max
        pygame.draw.rect(self.screen, (50, 50, 50), (self.enemy.rect.x, self.enemy.rect.y - 15, self.enemy.rect.width, 10))
        pygame.draw.rect(self.screen, (200, 0, 0), (self.enemy.rect.x, self.enemy.rect.y - 15, int(self.enemy.rect.width * e_ratio), 10))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.enemy.draw(self.screen)

        frame = self.player.sprite.frames[self.player.sprite.current_frame]
        self.screen.blit(frame, self.player_rect)

        self.draw_health_bars()

        # Texto "Nivel 3"
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Nivel 3", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

        if self.revive_message_timer > 0:
            font_msg = pygame.font.Font(None, 50)
            text = font_msg.render("¡Ja ja, pensaste que había muerto!", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
            self.revive_message_timer -= 1

        if self.player_dialogue_timer > 0:
            font_player = pygame.font.Font(None, 40)
            text = font_player.render("Ohh no...", True, (255, 255, 255))
            self.screen.blit(text, (self.player_rect.centerx - text.get_width() // 2, self.player_rect.top - 30))
            self.player_dialogue_timer -= 1

        if self.game_over:
            msg = self.font.render("GAME OVER", True, (180, 0, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        elif self.level_completed:
            fancy_font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 60)
            msg = fancy_font.render("NIVEL COMPLETADO", True, (0, 255, 0))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
