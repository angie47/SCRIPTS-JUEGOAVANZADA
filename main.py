# Importamos las librerias necesarias
import pygame
import sys

# Importamos configuraciones globales desde el archivo settings.py
# WIDTH y HEIGHT: dimensiones de la pantalla
# FPS: frames por segundo para controlar la velocidad del juego
from settings import WIDTH, HEIGHT, FPS

#Importamos las pantallas que hemos diseñado en otros modulos
from menu import MainMenu                        # Pantalla del menu principal
from character_select import CharacterSelectScreen 
from level1 import LevelOneScreen               

# Inicializamos Pygame
pygame.init()

#Configuración de la muica de fondo
pygame.mixer.init()  # Inicializa el mezclador de audio
pygame.mixer.music.load("assetts/music/musicainicio.mp3")  # Cargamos la musica inicial del menu
pygame.mixer.music.set_volume(0.7) 
pygame.mixer.music.play(-1) 
current_music = "menu" 

#Configuracio de la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Mi Juego")  
clock = pygame.time.Clock()  


menu = MainMenu(screen)                       # Pantalla de menu principal
personajes_screen = CharacterSelectScreen(screen)  # Pantalla de seleccion de personajes
level1_screen = LevelOneScreen(screen)          

#Variable que define el estado actual del juego
state = "MENU"

#Variables para el parpadeo del texto "Presione ESPACIO para jugar"
blink_timer = 0  
show_press_space = True  

#Bucle principal del juego
while True:
    #Procesamiento de eventos 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()

        #Estado del menu principal
        if state == "MENU":
            menu.handle_event(event)  # Procesa eventos de botones del menú
            # Si el boton de personajes fue presionado
            if menu.btn_personajes.clicked:
                state = "PERSONAJES"           # Cambiamos al estado de selección de personajes
                pygame.mixer.music.set_volume(0.18)  # Bajamos el volumen mientras estamos en la selección
                menu.btn_personajes.clicked = False  # Reiniciamos el estado del botón

            # Si el boton de salir fue presionado
            if menu.btn_salir.clicked:
                pygame.quit()
                sys.exit()

            # Si se presiona la tecla espacio en el menu, iniciamos el Nivel 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "NIVEL1"
                #Cambiamos la musica si no esta la del nivel 1
                if current_music != "nivel1":
                    pygame.mixer.music.load("assetts/music/music_nivel1.mp3")
                    pygame.mixer.music.set_volume(0.23)
                    pygame.mixer.music.play(-1)
                    current_music = "nivel1"

        #Estado:Pantalla de personajes
        elif state == "PERSONAJES":
            personajes_screen.handle_event(event) #Procesa eventos de esta pantalla
            # Si el boton volver fue pesionado
            if personajes_screen.btn_volver.clicked:
                state = "MENU"  #Regresamos al menu principal
                #Cambiamos la música de vuelta a la del menú
                if current_music != "menu":
                    pygame.mixer.music.load("assetts/music/musicainicio.mp3")
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play(-1)
                    current_music = "menu"
                personajes_screen.btn_volver.clicked = False  

        #Estado: Nivel 1 
        elif state == "NIVEL1":
            level1_screen.handle_event(event) 

    #Actualizacion dibujo de cada estado
    if state == "MENU":
        menu.update()  
        menu.draw()    # Dibuja los elementos del menú en pantalla

        #Control del texto parpadeante "Presione ESPACIO para jugar"
        blink_timer += clock.get_time()
        if blink_timer > 500: 
            show_press_space = not show_press_space
            blink_timer = 0
        if show_press_space: 
            font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 20)
            txt = font.render("Presione ESPACIO para jugar", True, (255, 255, 160))
            y_pos = HEIGHT - 60
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y_pos))

    elif state == "PERSONAJES":
        personajes_screen.update()  
        personajes_screen.draw()    # Dibuja la pantalla de personajes

    elif state == "NIVEL1":
        level1_screen.update()  
        level1_screen.draw()   

    pygame.display.flip() 
    clock.tick(FPS)        
