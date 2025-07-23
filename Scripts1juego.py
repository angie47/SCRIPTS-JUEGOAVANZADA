#Importamos las librerias necesarias
import pygame
import sys
import random
import math
import os

#Inicializa todos los modulos de pygame y el modulo de sonido
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('musicainicio.mp3') # Carga y reproduce la musica de fondo en bucle infinito
pygame.mixer.music.play(-1)
try:
    sonido_seleccion = pygame.mixer.Sound('Sonidoseleccionpersonaje.mp3')
except:
    print("Error cargando el sonido 'Sonidoseleccionpersonaje.mp3'")
    sonido_seleccion = None


# Dimensiones de la ventana
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE LEGACY OF THE MIST")

DARK_BG = (25, 25, 32)
DARKER_BG = (16, 16, 24)
DARK_BTN = (44, 44, 56)
HOVER_BTN = (90, 90, 110)
CLICK_BTN = (170, 170, 190)
NODE_UNLOCK = (140, 140, 150)
NODE_LOCK = (50, 50, 60)
NODE_SEL = (210, 210, 230)

# ------ FONDO DE LA INTERFAZ ------
try:
    fondo_interfaz = pygame.image.load('fondo_menu.png').convert()
    fondo_interfaz = pygame.transform.scale(fondo_interfaz, (WIDTH, HEIGHT))
except:
    fondo_interfaz = pygame.Surface((WIDTH, HEIGHT))
    fondo_interfaz.fill(DARK_BG)

try:
    TITLE_FONT = pygame.font.Font('epic_font.ttf', 56)
except:
    TITLE_FONT = pygame.font.SysFont('Arial', 56, bold=True)
try:
    BUTTON_FONT = pygame.font.Font('button_font.ttf', 36)
except:
    BUTTON_FONT = pygame.font.SysFont('Arial', 36, bold=True)
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)

#Generación de partículas de niebla
NUM_FOGS = 25
fog_particles = []
for _ in range(NUM_FOGS):
    x = random.randint(-200, WIDTH+200)
    y = random.randint(0, HEIGHT)
    radius = random.randint(60, 180)
    speed = random.uniform(0.2, 0.7)
    alpha = random.randint(60, 110)
    fog_particles.append([x, y, radius, speed, alpha])

#Funcion que dibuja la niebla
def draw_fog(surface, camera_x=0):
    for i, (x, y, radius, speed, alpha) in enumerate(fog_particles):
        fog_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(fog_surface, (110, 110, 110, alpha), (radius, radius), radius)
        surface.blit(fog_surface, (x - radius - camera_x//3, y - radius))
        fog_particles[i][0] += speed
        if fog_particles[i][0] - radius > WIDTH*3:
            fog_particles[i][0] = -radius
            fog_particles[i][1] = random.randint(0, HEIGHT)
            fog_particles[i][2] = random.randint(60, 180)
            fog_particles[i][4] = random.randint(60, 110)

#Clase de boton animado
class AnimatedButton:
    def __init__(self, rect, text, font, sonido=True):
        self.base_rect = pygame.Rect(rect)
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.base_color = DARK_BTN
        self.hover_color = HOVER_BTN
        self.click_color = CLICK_BTN
        self.current_color = self.base_color
        self.hovered = False
        self.clicked = False
        self.sonido = sonido

def draw(self, surface):
    # Aquí ajustamos el tamaño del botón dependiendo de si el mouse está encima (hovered) o presionado (clicked)
    scale = 1.07 if self.hovered else 1.0
    if self.clicked:
        scale = 1.15
    new_width = int(self.base_rect.width * scale)
    new_height = int(self.base_rect.height * scale)
    self.rect.width = new_width
    self.rect.height = new_height
    self.rect.center = self.base_rect.center

    # Aquí agregamos un brillo (glow) alrededor del botón cuando el mouse está encima
    if self.hovered:
        glow = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (180, 180, 250, 60), glow.get_rect())
        surface.blit(glow, (self.rect.x - 10, self.rect.y - 10))

    # Aquí definimos el color del botón dependiendo del estado
    color = self.current_color
    if self.hovered:
        # Le damos un efecto de cambio de brillo animado cuando el mouse está encima
        brightness = 10 + int(15 * math.sin(pygame.time.get_ticks() * 0.005))
        color = (
            min(self.hover_color[0] + brightness, 255),
            min(self.hover_color[1] + brightness, 255),
            min(self.hover_color[2] + brightness, 255),
        )
    if self.clicked:
        # Si está presionado, se usa un color especial de clic
        color = self.click_color

    # Aquí dibujamos el rectángulo del botón con bordes redondeados
    pygame.draw.rect(surface, color, self.rect, border_radius=16)
    if self.hovered:
        # Agregamos un borde decorativo cuando el mouse está encima
        pygame.draw.rect(surface, (200, 200, 200, 100), self.rect, 3, border_radius=16)
        # Aquí generamos pequeñas partículas dentro del botón como efecto extra
        for _ in range(3):
            px = random.randint(self.rect.left, self.rect.right)
            py = random.randint(self.rect.top, self.rect.bottom)
            pygame.draw.circle(surface, (240, 240, 255), (px, py), 1)

    # Aquí dibujamos el texto centrado del botón
    text_surf = self.font.render(self.text, True, BLACK if self.clicked else WHITE)
    surface.blit(
        text_surf,
        (self.rect.centerx - text_surf.get_width() // 2, self.rect.centery - text_surf.get_height() // 2)
    )

def handle_event(self, event):
    # Aquí comprobamos si el mouse está sobre el botón
    mouse_pos = pygame.mouse.get_pos()
    self.hovered = self.rect.collidepoint(mouse_pos)
    # Cambiamos el cursor según si está sobre el botón o no
    if self.hovered:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    clicked = False
    # Aquí detectamos si se presionó el botón con el mouse
    if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
        self.clicked = True
        clicked = True
        # Si existe un sonido "click.wav" lo reproducimos
        if os.path.exists("click.wav"):
            try:
                pygame.mixer.Sound("click.wav").play()
            except:
                pass
    elif event.type == pygame.MOUSEBUTTONUP:
        self.clicked = False
    return clicked

class SpriteSheetAnim:
    def __init__(self, image_path, num_frames, frame_width, frame_height, size_final, orientation='horizontal', colorkey=None):
        # Aquí intentamos cargar el spritesheet de la animación
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
        except:
            # Si no se encuentra, creamos un surface de color de error
            self.sheet = pygame.Surface((frame_width*num_frames if orientation=='horizontal' else frame_width,
                                         frame_height*num_frames if orientation=='vertical' else frame_height), pygame.SRCALPHA)
            self.sheet.fill((180,120,120,200))
        self.frames = []
        # Aquí recortamos cada frame de la imagen dependiendo de la orientación
        for i in range(num_frames):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            if orientation == 'horizontal':
                frame.blit(self.sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            else:
                frame.blit(self.sheet, (0, 0), (0, i * frame_height, frame_width, frame_height))
            if colorkey:
                frame.set_colorkey(colorkey)
            # Escalamos el frame al tamaño final
            frame = pygame.transform.smoothscale(frame, size_final)
            self.frames.append(frame)
        # Inicializamos el índice de la animación
        self.idx = 0
        self.last_time = pygame.time.get_ticks()
        self.cooldown = 120  # Tiempo entre frames de animación

    def actualizar(self):
        # Aquí actualizamos el frame actual dependiendo del tiempo
        now = pygame.time.get_ticks()
        if now - self.last_time > self.cooldown:
            self.idx = (self.idx + 1) % len(self.frames)
            self.last_time = now

    def obtener_frame(self):
        # Aquí devolvemos el frame actual de la animación
        return self.frames[self.idx]

def draw_instructions_panel():
    # Aquí dibujamos el panel de instrucciones del juego
    panel = pygame.Surface((600, 350), pygame.SRCALPHA)
    pygame.draw.rect(panel, (32, 32, 42, 235), (0,0,600,350), border_radius=25)
    pygame.draw.rect(panel, (180,180,180,60), (0,0,600,350), 3, border_radius=25)
    font = pygame.font.Font('button_font.ttf', 26)
    lines = [
        "INSTRUCCIONES",
        "",
        "• Usa las flechas para moverte",
        "• Salta con ESPACIO",
        "• Z para destruir obstáculos (Ailith o Borin)",
        "",
        "¡Buena suerte!"
    ]
    y = 40
    for line in lines:
        surf = font.render(line, True, (220, 220, 230))
        panel.blit(surf, (40, y))
        y += 44
    screen.blit(panel, (WIDTH//2-300, HEIGHT//2-175))

# Aquí definimos los personajes con sus descripciones
PERSONAJES = [
    {"nombre": "Borin", "desc": "Hechicero del místico velo.\nControla la niebla y lanza conjuros."},
    {"nombre": "Kael", "desc": "Guerrero ancestral.\nDefensa inquebrantable y gran fuerza."},
    {"nombre": "Ailith", "desc": "Maestra de las sombras y la niebla.\nEspecialista en sigilo y agilidad."}
]

# Aquí definimos las animaciones de los personajes en tamaño estándar
PERSONAJES_SPRITES = [
    SpriteSheetAnim('borin.png', 8, 250, 250, (220, 280), 'horizontal'),
    SpriteSheetAnim('kael.png', 10, 96, 96, (220, 280), 'horizontal'),
    SpriteSheetAnim('ailith.png', 6, 32, 48, (220, 280), 'vertical'),
]

# Aquí definimos las animaciones de los personajes en tamaño grande
SPRITE_GRANDE = [
    SpriteSheetAnim('borin.png', 8, 250, 250, (460, 540), 'horizontal'),
    SpriteSheetAnim('kael.png', 10, 96, 96, (460, 540), 'horizontal'),
    SpriteSheetAnim('ailith.png', 6, 32, 48, (460, 540), 'vertical')
]
