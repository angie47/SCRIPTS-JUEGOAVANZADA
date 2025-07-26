import pygame
import sys
from settings import WIDTH, HEIGHT, FPS  # Importa configuración general (tamaño de pantalla y FPS)
from menu import MainMenu  # Importa la clase del menú principal
from character_select import CharacterSelectScreen  # Importa la clase de selección de personajes
from level1 import LevelOneScreen  # Importa la clase del primer nivel

pygame.init()  # Inicializa todos los módulos de Pygame

# ---- Música de fondo ----
pygame.mixer.init()  # Inicializa el módulo de sonido
pygame.mixer.music.load("assetts/music/musicainicio.mp3")  # Carga la música de inicio
pygame.mixer.music.set_volume(0.7)  # Establece el volumen al 70%
pygame.mixer.music.play(-1)  # Reproduce la música en bucle infinito
current_music = "menu"  # Variable que indica qué música está sonando actualmente

# ---- Configuración de pantalla ----
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana del juego con tamaño definido
pygame.display.set_caption("Mi Juego")  # Título de la ventana
clock = pygame.time.Clock()  # Reloj para controlar los FPS

# ---- Instancias de pantallas ----
menu = MainMenu(screen)  # Crea el menú principal
personajes_screen = CharacterSelectScreen(screen)  # Crea la pantalla de selección de personajes
level1_screen = None  # Inicialmente no hay nivel cargado
selected_character_sprite = None  # Aún no se ha seleccionado ningún personaje

# ---- Estado inicial del juego ----
state = "MENU"  # El juego comienza en el menú principal
blink_timer = 0  # Temporizador para parpadear el mensaje de presionar espacio
show_press_space = True  # Bandera para mostrar u ocultar el mensaje

# ---- Bucle principal del juego ----
while True:
    for event in pygame.event.get():  # Recorre todos los eventos (teclas, mouse, etc.)
        if event.type == pygame.QUIT:  # Si se cierra la ventana
            pygame.quit()
            sys.exit()

        # ---- Lógica del Menú Principal ----
        if state == "MENU":
            menu.handle_event(event)  # Procesa los eventos del menú (botones)

            if menu.btn_personajes.clicked:  # Si se hace clic en el botón de personajes
                state = "PERSONAJES"  # Cambia el estado a selección de personajes
                pygame.mixer.music.set_volume(0.18)  # Baja el volumen de la música
                menu.btn_personajes.clicked = False  # Reinicia el estado del botón

            if menu.btn_salir.clicked:  # Si se hace clic en salir
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Si se presiona la barra espaciadora y ya hay un personaje seleccionado
                if selected_character_sprite:
                    state = "NIVEL1"  # Cambia al estado del nivel 1
                    level1_screen = LevelOneScreen(screen, selected_character_sprite)  # Crea el nivel 1

        # ---- Lógica de Selección de Personajes ----
        elif state == "PERSONAJES":
            personajes_screen.handle_event(event)  # Procesa eventos en pantalla de personajes

            if personajes_screen.selected_index is not None:
                # Si se seleccionó un personaje
                selected_character = personajes_screen.characters[personajes_screen.selected_index]
                selected_character_sprite = selected_character["sprite"]  # Guarda el sprite seleccionado
                print("Seleccionaste el personaje:", selected_character["name"])  # Imprime el nombre

            if personajes_screen.btn_volver.clicked:  # Si se hace clic en volver
                state = "MENU"  # Regresa al menú principal
                personajes_screen.btn_volver.clicked = False  # Reinicia el botón

        # ---- Lógica del Nivel 1 ----
        elif state == "NIVEL1" and level1_screen:
            level1_screen.handle_event(event)  # Procesa eventos del nivel 1

    # ---- Actualización y dibujo según el estado ----
    if state == "MENU":
        menu.update()  # Actualiza el menú
        menu.draw()  # Dibuja el menú
    elif state == "PERSONAJES":
        personajes_screen.update()  # Actualiza pantalla de personajes
        personajes_screen.draw()  # Dibuja pantalla de personajes
    elif state == "NIVEL1" and level1_screen:
        level1_screen.update()  # Actualiza el nivel 1
        level1_screen.draw()  # Dibuja el nivel 1

    pygame.display.flip()  # Refresca la pantalla con lo dibujado
    clock.tick(FPS)  # Mantiene la velocidad del juego en los FPS definidos
