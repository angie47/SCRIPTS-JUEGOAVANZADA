import pygame
import sys
import os
from settings import WIDTH, HEIGHT, FPS
from menu import MainMenu
from character_select import CharacterSelectScreen
from overworld_map import OverworldMap
from instructions_screen import InstructionsScreen
from level1 import LevelOneScreen
from level2 import LevelTwoScreen
from level3 import LevelThreeScreen
from background import Background

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assetts/music/musicainicio.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego")
clock = pygame.time.Clock()

click_sound_general = pygame.mixer.Sound(os.path.join("assetts/sounds/click.mp3"))

menu = MainMenu(screen)
personajes_screen = CharacterSelectScreen(screen)
overworld_map_screen = OverworldMap(screen, click_sound_general)
instructions_screen = InstructionsScreen(screen, click_sound_general)

level1_screen = None
level2_screen = None
level3_screen = None
selected_player = None

state = "MENU"
show_congratulations = False

# Fondo animado para la pantalla de felicitaciones
congratulations_bg = Background("assetts/images/backgrounds/frames/", fps=10)

# --- Pantalla de transición ---
def show_transition(message="Preparando nivel..."):
    transition_image = pygame.image.load("assetts/images/transitions/loading_screen.png").convert()
    transition_image = pygame.transform.scale(transition_image, (WIDTH, HEIGHT))
    font = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 36)

    blink = True
    blink_timer = 0
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:  # 2 segundos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(transition_image, (0, 0))

        text_surface = font.render(message, True, (255, 255, 255))
        shadow_surface = font.render(message, True, (50, 50, 50))
        screen.blit(shadow_surface, (WIDTH // 2 - text_surface.get_width() // 2 + 3,
                                     HEIGHT - 100 + 3))
        if blink:
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 100))
        blink_timer += 1
        if blink_timer > 30:
            blink = not blink
            blink_timer = 0

        pygame.display.flip()
        clock.tick(FPS)

# --- Pantalla final de felicitaciones ---
def draw_congratulations(animated_bg):
    animated_bg.update()
    frame = animated_bg.frames[animated_bg.current_frame]
    screen.blit(frame, (0, 0))

    font_big = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 60)
    font_small = pygame.font.Font("assetts/fonts/PressStart2P-Regular.ttf", 32)

    text_main = "¡FELICIDADES!"
    text_sub = "¡Has completado todos los niveles!"
    text_info = "Presiona M para volver al menú"

    def draw_text_with_shadow(text, font, color, pos):
        shadow = font.render(text, True, (0, 0, 0))
        surface = font.render(text, True, color)
        screen.blit(shadow, (pos[0] + 3, pos[1] + 3))
        screen.blit(surface, pos)

    draw_text_with_shadow(text_main, font_big, (0, 255, 0),
                          (WIDTH // 2 - font_big.size(text_main)[0] // 2, 200))
    draw_text_with_shadow(text_sub, font_small, (255, 255, 0),
                          (WIDTH // 2 - font_small.size(text_sub)[0] // 2, 300))
    draw_text_with_shadow(text_info, font_small, (255, 255, 255),
                          (WIDTH // 2 - font_small.size(text_info)[0] // 2, 400))

# ================= Bucle principal =================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if show_congratulations:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                show_congratulations = False
                state = "MENU"

        if state == "MENU":
            if menu.handle_event(event):
                if menu.btn_personajes.is_selected:
                    state = "PERSONAJES"
                    pygame.mixer.music.set_volume(0.18)
                    menu.btn_personajes.set_selected(False)
                elif menu.btn_salir.is_selected:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "OVERWORLD_MAP"

        elif state == "PERSONAJES":
            personajes_screen.handle_event(event)
            if personajes_screen.selected_player_instance:
                selected_player = personajes_screen.selected_player_instance
                personajes_screen.selected_player_instance = None
            if personajes_screen.should_return_to_menu:
                state = "MENU"
                personajes_screen.should_return_to_menu = False

        elif state == "OVERWORLD_MAP":
            if overworld_map_screen.handle_event(event):
                if overworld_map_screen.selected_level_state:
                    if selected_player:
                        state = overworld_map_screen.selected_level_state
                        if state == "NIVEL1":
                            show_transition("Preparando Nivel 1...")
                            level1_screen = LevelOneScreen(screen, selected_player)
                        elif state == "NIVEL2":
                            show_transition("Preparando Nivel 2...")
                            level2_screen = LevelTwoScreen(screen, selected_player)
                        elif state == "NIVEL3":
                            show_transition("Preparando Nivel 3...")
                            level3_screen = LevelThreeScreen(screen, selected_player)
                        else:
                            state = "OVERWORLD_MAP"
                    else:
                        state = "PERSONAJES"
                elif overworld_map_screen.should_return_to_menu:
                    state = "MENU"
                elif overworld_map_screen.should_show_instructions:
                    state = "INSTRUCTIONS"

        elif state == "INSTRUCTIONS":
            instructions_screen.handle_event(event)
            if instructions_screen.should_return_to_map:
                state = "OVERWORLD_MAP"
                instructions_screen.should_return_to_map = False

        elif state == "NIVEL1" and level1_screen:
            level_event_result = level1_screen.handle_event(event)
            if level_event_result == "RETURN_TO_MAP":
                state = "OVERWORLD_MAP"

        elif state == "NIVEL2" and level2_screen:
            level_event_result = level2_screen.handle_event(event)
            if level_event_result == "RETURN_TO_MAP":
                state = "OVERWORLD_MAP"

        elif state == "NIVEL3" and level3_screen:
            level_event_result = level3_screen.handle_event(event)
            if level_event_result == "RETURN_TO_MAP":
                state = "OVERWORLD_MAP"

    # --- Dibujar estados ---
    if show_congratulations:
        draw_congratulations(congratulations_bg)

    elif state == "MENU":
        menu.update()
        menu.draw()

    elif state == "PERSONAJES":
        personajes_screen.update()
        personajes_screen.draw()

    elif state == "OVERWORLD_MAP":
        overworld_map_screen.update()
        overworld_map_screen.draw()

    elif state == "INSTRUCTIONS":
        instructions_screen.update()
        instructions_screen.draw()

    elif state == "NIVEL1" and level1_screen:
        result = level1_screen.update()
        level1_screen.draw()
        if result == "NEXT_LEVEL":
            show_transition("Preparando Nivel 2...")
            level2_screen = LevelTwoScreen(screen, selected_player)
            state = "NIVEL2"

    elif state == "NIVEL2" and level2_screen:
        result = level2_screen.update()
        level2_screen.draw()
        if result == "LEVEL_COMPLETE":
            show_transition("Preparando Nivel 3...")
            level3_screen = LevelThreeScreen(screen, selected_player)
            state = "NIVEL3"

    elif state == "NIVEL3" and level3_screen:
        result = level3_screen.update()
        level3_screen.draw()
        if result == "LEVEL_COMPLETE":
            show_congratulations = True

    pygame.display.flip()
    clock.tick(FPS)
