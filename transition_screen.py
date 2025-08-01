import pygame
import os
from settings import WIDTH, HEIGHT

class TransitionScreen:
    def __init__(self, screen, message="Preparando nivel..."):
        self.screen = screen
        self.message = message
        self.clock = pygame.time.Clock()

        # Cargar imagen de fondo
        image_path = "assetts/images/transitions/loading_screen.png"
        if os.path.exists(image_path):
            self.background = pygame.image.load(image_path).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        else:
            # Fallback si no existe la imagen
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((30, 30, 30))

        # Fuente estilo retro
        font_path = "assetts/fonts/PressStart2P-Regular.ttf"
        self.font = pygame.font.Font(font_path, 32) if os.path.exists(font_path) else pygame.font.Font(None, 32)

        # Parpadeo + escala
        self.show_text = True
        self.text_timer = 0
        self.scale_direction = 1
        self.scale = 1.0

    def run(self, duration=2000):
        start_time = pygame.time.get_ticks()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Fondo
            self.screen.blit(self.background, (0, 0))

            # Control de parpadeo
            self.text_timer += self.clock.get_time()
            if self.text_timer > 400:
                self.show_text = not self.show_text
                self.text_timer = 0

            # Efecto de escala suave (zoom in/out)
            self.scale += 0.01 * self.scale_direction
            if self.scale >= 1.2:
                self.scale_direction = -1
            elif self.scale <= 1.0:
                self.scale_direction = 1

            # Renderizar texto con escala
            if self.show_text:
                text_surface = self.font.render(self.message, True, (255, 255, 0))
                text_surface = pygame.transform.rotozoom(text_surface, 0, self.scale)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

            if pygame.time.get_ticks() - start_time > duration:
                running = False
