# health_bar.py
import pygame

class HealthBar:
    # Constructor de la clase HealthBar
    def __init__(self, x, y, width, height, max_hp):
        # Almacena la posición y dimensiones de la barra de vida
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Almacena la vida máxima y establece la vida actual al máximo al inicio
        self.max_hp = max_hp
        self.current_hp = max_hp

    # Método para actualizar la vida actual de la barra
    def update(self, current_hp):
        # Actualiza el valor de la vida actual
        self.current_hp = current_hp

    # Método para dibujar la barra de vida en la pantalla
    def draw(self, screen):
        # 1. Dibuja el fondo de la barra (el "contenedor" de la vida)
        # Crea un objeto Rect que representa el fondo de la barra
        background_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Dibuja el rectángulo de fondo en la pantalla con un color gris oscuro
        pygame.draw.rect(screen, (50, 50, 50), background_rect)

        # 2. Calcula y dibuja la porción de vida restante
        # Calcula el ancho de la barra de vida actual basándose en el porcentaje de vida
        health_width = (self.current_hp / self.max_hp) * self.width
        # Crea un objeto Rect para la porción de vida (el color verde)
        health_rect = pygame.Rect(self.x, self.y, health_width, self.height)
        
        # Dibuja el rectángulo de vida en la pantalla con un color verde
        pygame.draw.rect(screen, (0, 200, 0), health_rect)

        # 3. Dibuja un borde alrededor de toda la barra
        # Dibuja un borde blanco de 2 píxeles de grosor alrededor de la barra completa
        pygame.draw.rect(screen, (255, 255, 255), background_rect, 2)