import pygame
import os
import random
from settings import WIDTH, HEIGHT  # Importa configuración de pantalla

class LevelOneScreen:
    def __init__(self, screen, player_sprite):
        self.screen = screen  # Pantalla principal del juego
        self.clock = pygame.time.Clock()  # Reloj para controlar FPS

        # --- FONDO ANIMADO ---
        self.background_frames = []  # Lista para los fotogramas del fondo animado
        bg_path = "assetts/images/level1/background"  # Ruta donde están las imágenes del fondo
        for file in sorted(os.listdir(bg_path)):  # Ordena y recorre los archivos
            if file.endswith(".png"):  # Solo toma archivos .png
                img = pygame.image.load(os.path.join(bg_path, file)).convert_alpha()  # Carga imagen con transparencia
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # Escala al tamaño de la pantalla
                self.background_frames.append(img)  # Agrega imagen a la lista de fondos
        self.current_bg_frame = 0  # Índice actual del fondo que se mostrará
        self.bg_frame_rate = 8  # Cuántos frames esperar antes de cambiar fondo
        self.bg_frame_counter = 0  # Contador de frames para animar el fondo

        # --- JUGADOR ---
        self.player_sprite = player_sprite  # Sprite animado del personaje
        self.player_rect = self.player_sprite.frames[0].get_rect(topleft=(100, HEIGHT - 180))  # Posición inicial del jugador
        self.player_speed = 5  # Velocidad del jugador

        # --- NIEBLA (PERSECUCIÓN) ---
        self.fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Superficie transparente para la niebla
        self.fog.fill((200, 200, 200, 50))  # Color de niebla con transparencia
        self.fog_x = -WIDTH  # Posición inicial fuera de pantalla (izquierda)

        # --- OBSTÁCULOS ---
        self.obstacles = []  # Lista de obstáculos que aparecerán
        self.spawn_timer = 0  # Temporizador para controlar aparición de obstáculos

        # --- GAME OVER ---
        self.game_over = False  # Bandera para saber si el juego terminó
        self.font = pygame.font.Font(None, 60)  # Fuente para mostrar mensaje de Game Over

        # --- MÚSICA NIVEL ---
        pygame.mixer.music.load("assetts/music/music_nivel1.mp3")  # Carga la música del nivel
        pygame.mixer.music.set_volume(0.6)  # Establece el volumen
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle

    def handle_event(self, event):
        # Si se presiona R mientras está en Game Over, reinicia el nivel
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.__init__(self.screen, self.player_sprite)  # Reinicia la clase

    def update(self):
        if self.game_over:
            return  # Si el juego terminó, no se actualiza nada

        # --- Movimiento del jugador con teclas WASD ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_rect.top > 0:
            self.player_rect.y -= self.player_speed
        if keys[pygame.K_s] and self.player_rect.bottom < HEIGHT:
            self.player_rect.y += self.player_speed
        if keys[pygame.K_a] and self.player_rect.left > 0:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_d] and self.player_rect.right < WIDTH:
            self.player_rect.x += self.player_speed

        # Actualiza la animación del jugador
        self.player_sprite.update()

        # --- Movimiento de la niebla (persiguiendo al jugador) ---
        self.fog_x += 1  # La niebla se mueve hacia la derecha
        if self.fog_x > 0:  # No pasa del borde izquierdo
            self.fog_x = 0

        # --- Generación de obstáculos ---
        self.spawn_timer += 1
        if self.spawn_timer > 90:  # Cada 1.5 segundos aprox (si FPS = 60)
            size = random.randint(30, 60)  # Tamaño aleatorio del obstáculo
            x = WIDTH + 50  # Aparecen fuera de la pantalla (derecha)
            y = random.randint(HEIGHT - 200, HEIGHT - 100)  # Altura aleatoria
            rect = pygame.Rect(x, y, size, size)  # Crea el obstáculo como un rectángulo
            self.obstacles.append(rect)  # Agrega a la lista
            self.spawn_timer = 0  # Reinicia el temporizador

        # --- Movimiento de obstáculos ---
        for rect in self.obstacles:
            rect.x -= 5  # Se mueven hacia la izquierda (como si el jugador avanzara)

        # --- Detección de colisiones entre jugador y obstáculos ---
        for rect in self.obstacles:
            if self.player_rect.colliderect(rect):  # Si hay colisión
                self.game_over = True  # Termina el juego

        # --- Animación del fondo ---
        self.bg_frame_counter += 1  # Aumenta contador de frames
        if self.bg_frame_counter >= self.bg_frame_rate:  # Si se cumple el tiempo de cambio
            self.current_bg_frame = (self.current_bg_frame + 1) % len(self.background_frames)  # Cambia al siguiente fondo
            self.bg_frame_counter = 0  # Reinicia el contador

    def draw(self):
        # --- Dibuja el fondo animado ---
        self.screen.blit(self.background_frames[self.current_bg_frame], (0, 0))

        # --- Dibuja los obstáculos ---
        for rect in self.obstacles:
            pygame.draw.rect(self.screen, (200, 0, 0), rect)  # Rectángulos rojos

        # --- Dibuja el jugador ---
        current_frame = self.player_sprite.frames[self.player_sprite.current_frame]  # Frame actual del sprite animado
        self.screen.blit(current_frame, self.player_rect)

        # --- Dibuja la niebla ---
        self.screen.blit(self.fog, (self.fog_x, 0))

        # --- Si el juego terminó, muestra "GAME OVER" ---
        if self.game_over:
            text = self.font.render("GAME OVER - R para reiniciar", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))  # Centra el texto
