import pygame as pg
import json
from enemy import Enemy
from turret import Turret
from button import Button
from world import World
from pygame import mixer
import random
import constants as c
pg.init()

import os
os.system('cls' if os.name == 'nt' else 'clear')

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")


# Establecer el tamaño de la pantalla que quieres en pantalla completa
screen_width = 1020
screen_height = 720

screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)



#Variables del Juego
in_menu = True
in_background = False
in_credits = False
game_over = False
game_outcome = 0 # -1 Si pierde, 1 si gana
game_speed_toggle = False
game_paused = False
afford = False
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
confirm_exit = False
confirm_restart = False
show_logo = True
nivel = 0
kill_count = 0
missed_count = 0
inicio_nivel = False
volumen = True

# Mapa
map_image = pg.image.load('levels/Background (1).png').convert_alpha()
# Menu principal
main_menu_image = pg.image.load('gui/main_menu.png').convert_alpha()
# Fondo e informacion de juego
background_image = pg.image.load('gui/background.png').convert_alpha()
sinopsis_image = pg.image.load('gui/sinopsis.png').convert_alpha()
credits_image = pg.image.load('gui/creditos.png').convert_alpha()
# Flechas de direccion
direccion_image = pg.image.load('Iconos/direcciones.png').convert_alpha()
comienzo = pg.transform.rotate(direccion_image, -90)
meta = pg.transform.rotate(direccion_image, -180)

# Enemigo
enemy_images = {
    "weak": pg.image.load('enemigos/enemy_1.png').convert_alpha(),
    "medium": pg.image.load('enemigos/enemy_2.png').convert_alpha(),
    "strong": pg.image.load('enemigos/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('enemigos/enemy_4.png').convert_alpha()
}
enemy_image = pg.image.load('enemigos/enemy_1.png').convert_alpha()

# Botones
play_image = pg.image.load('Botones/play.png').convert_alpha()
buy_turret_image = pg.image.load('Botones/buy_turret_true.png').convert_alpha()
buy_turret_false_image = pg.image.load('Botones/buy_turret_false.png').convert_alpha()
cancel_image = pg.image.load('Botones/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('Botones/upgrade_turret_true.png').convert_alpha()
upgrade_turret_false_image = pg.image.load('Botones/upgrade_turret_false.png').convert_alpha()
sell_turret_image = pg.image.load('Botones/sell_turret.png').convert_alpha()
begin_image = pg.image.load('Botones/begin.png').convert_alpha()
restart_image = pg.image.load('Botones/restart.png').convert_alpha()
fast_forward_false_image = pg.image.load('Botones/fast_forward_false.png').convert_alpha()
fast_forward_true_image = pg.image.load('Botones/fast_forward_true.png').convert_alpha()
exit_image = pg.image.load('Botones/exit.png').convert_alpha()
yes_image = pg.image.load('Botones/yes.png').convert_alpha()
not_image = pg.image.load('Botones/no.png').convert_alpha()
pause_image = pg.image.load('Botones/pause.png').convert_alpha()
continue_image = pg.image.load('Botones/continue.png').convert_alpha()
restart_level_image = pg.image.load('Botones/restart_level.png').convert_alpha()
about_image = pg.image.load('Botones/about.png').convert_alpha()
quit_game_image = pg.image.load('Botones/quit_game.png').convert_alpha()
next_image = pg.image.load('Botones/next.png').convert_alpha()
close_image = pg.image.load('Botones/close.png').convert_alpha()
volume_on_image = pg.image.load('Botones/volume_on.png').convert_alpha()
volume_off_image = pg.image.load('Botones/volume_off.png').convert_alpha()

# Cargar efectos de sonido
disparo_1 = pg.mixer.Sound('Audio/disparo_1x.mp3')
disparo_1.set_volume(0.5)
disparo_2 = pg.mixer.Sound('Audio/disparo_2x.mp3')
disparo_2.set_volume(0.5)
disparo_3 = pg.mixer.Sound('Audio/disparo_3x.mp3')
disparo_3.set_volume(0.5)
colocar_fx = pg.mixer.Sound('Audio/colocar_torre.mp3')
colocar_fx.set_volume(0.5)
mejorar_fx = pg.mixer.Sound('Audio/mejorar_torre.mp3')
mejorar_fx.set_volume(0.5)
vender_fx = pg.mixer.Sound('Audio/vender_torre.mp3')
vender_fx.set_volume(0.5)
click_fx = pg.mixer.Sound('Audio/click.mp3')
click_fx.set_volume(0.5)

# Interfaz grafica
heart_image = pg.image.load('Iconos/heart.png').convert_alpha()
coin_image = pg.image.load('Iconos/coin.png').convert_alpha()
logo_image = pg.image.load('Iconos/game_logo.png').convert_alpha()

# Imagen de la torreta
turret_spritesheets = []
# Cambiar la imagen de la torreta si sufre mejoras
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'torretas/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)

# Imagen del cursor de la torreta
cursor_turret = pg.image.load('torretas/cursor_turret.png').convert_alpha()

# Cargar el archivo json para la ruta del nivel
with open('levels/level.tmj') as file:
    world_data = json.load(file)

# Cargar fuentes para mostrar texto en pantalla
font_path = 'fuente/Capture_it.ttf'
text_font = pg.font.Font(font_path, 24)
large_font = pg.font.Font(font_path, 36)

# Funciones para colocar texto en pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    # Dibujar el panel
    pg.draw.rect(screen, "grey40", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    if show_logo:
        screen.blit(logo_image, (c.SCREEN_WIDTH, 400))

    # Dibujar iconos
    draw_text("NIVEL: " + str(world.level - nivel) + " / " + str(c.TOTAL_LEVELS), text_font, "grey100", c.SCREEN_WIDTH + 10, 10) # Nivel
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35)) # Icono de salud
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40) # Salud
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65)) # Icono de dinero
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70) # Dinero
    

# Crear un grupo de torretas
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    #Calcular la secuencia de numeros del titulo
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    #Chequiar si el titulo es valido
    if world.tile_map[mouse_tile_num] == 7:

        #Chequiar si el cursor se encuentra sobre una torre
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        #Si la torre no es una torre no valida, no crearla
        if space_is_free == True:
            disparo = random.choice([disparo_1, disparo_2, disparo_3])
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, disparo)
            turret_group.add(new_turret)
            colocar_fx.play()

            # Deducir el costo de la torreta
            world.money -= c.BUY_COST

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

# Crear el mundo
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Crear grupos de imagenes
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Crear botones
turret_buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, click_fx, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, click_fx, True)
upgrade_button = Button(c.SCREEN_WIDTH + 30, 180, upgrade_turret_image, "", True)
sell_turret_button = Button(c.SCREEN_WIDTH + 30, 240, sell_turret_image, "", True)
begin_button = Button(c.SCREEN_WIDTH + 60, 315, begin_image, click_fx, True)
restart_button = Button(230, 370, restart_image, click_fx, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 60, 315, fast_forward_false_image, click_fx, False)
play_button = Button((1020 // 2) - 75, 400, play_image, click_fx, True)
next_button = Button(630, 450, next_image, click_fx, True)
about_game_button = Button((1020 // 2) - 75, 465, about_image, click_fx, True)
quit_game_button = Button((1020 // 2) - 75, 530, quit_game_image, click_fx, True)
exit_button = Button(965, 5, exit_image, click_fx, True)
exit2_button = Button(420, 370, quit_game_image, click_fx, True)
pause_button = Button(910, 5, pause_image, click_fx, True)
restart_level_button = Button(965, 60, restart_level_image, click_fx, True)
close_button = Button(770, 175, close_image, click_fx, True)
volume_button = Button(910, 60, volume_on_image, click_fx, True)

mixer.music.load('Audio/main_theme.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)  # Reproducir en bucle

#Crear un reloj
clock = pg.time.Clock()
run = True
while run:
    dt = clock.tick(c.FPS) / 1000  # Limitar FPS y calcular delta time
    world.delta_time = dt  # Pasar delta time al mundo
    # Pantalla de inicio
    if not game_paused:
        if in_menu:
            # Dibujar el menú
            screen.blit(main_menu_image, (0, 0))
            if play_button.draw(screen):
                in_menu = False
                in_background = True
            if about_game_button.draw(screen):
                in_menu = False
                in_credits = True
            if quit_game_button.draw(screen):
                run = False
        elif in_background:
            screen.blit(background_image, (0, 0))
            # Dibujar la sinopsis
            screen.blit(sinopsis_image, ((1020 // 2) - (600 // 2), (720 // 2) - (350 // 2)))
            # Avanzar a la siguiente ventana
            if next_button.draw(screen):
                in_background = False
        elif in_credits:
            screen.blit(background_image, (0, 0))
            screen.blit(credits_image, ((1020 // 2) - (600 // 2), (720 // 2) - (350 // 2)))
            # Cerrar la ventana de creditos
            if close_button.draw(screen):
                in_credits = False
                in_menu = True
        #SECCION DE ACTUALIZACION

        elif not game_over:
            # Revisar si el juagador ha perdido
            if world.health <= 0:
                game_over = True
                game_outcome = -1 # Perdió
            
            # Revisar si el jugador ha ganado
            if world.level > c.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1 # Ganó
                nivel = 1

            # Actualizar los grupos
            enemy_group.update(world) 
            turret_group.update(enemy_group, world)

            # Marcar la torre seleccionada
            if selected_turret:
                selected_turret.selected = True

            # SECCION DE DIBUJO


            # Dibujar el mundo
            world.draw(screen)

            # Dibujar grupos
            enemy_group.draw(screen)
            for turret in turret_group:
                turret.draw(screen)

            display_data()

            # LOGICA DEL NIVEL

            # Mostrar flechas de direccion
            if not inicio_nivel:
                screen.blit(comienzo, (607, 20))
                screen.blit(meta, (20, 607))

            # Verificar si el jugador ha perdido
            if not game_over:
                # Revisar si el juego ha iniciado o no
                if not level_started:
                    if begin_button.draw(screen):
                        level_started = True
                        inicio_nivel = True
                else:
                    # Opcion de Aceleracion de juego
                    if fast_forward_button.draw(screen):
                        game_speed_toggle = not game_speed_toggle

                    if game_speed_toggle:
                        world.game_speed = 1
                        fast_forward_button.image = fast_forward_false_image
                    else:
                        world.game_speed = 3
                        fast_forward_button.image = fast_forward_true_image
                    
                    # Spawn de enemigos
                    if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                        if world.spawned_enemies < len(world.enemy_list):
                            enemy_type = world.enemy_list[world.spawned_enemies]
                            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                            enemy_group.add(enemy)
                            world.spawned_enemies += 1
                            last_enemy_spawn = pg.time.get_ticks()

                # Revisar si la ola de enemigos ha finalizado
                if world.check_level_complete() == True:
                    # Comenzar un nuevo nivel
                    world.money += c.LEVEL_COMPLETE_REWARD
                    world.level += 1
                    level_started = False
                    last_enemy_spawn = pg.time.get_ticks()
                    kill_count += world.killed_enemies
                    missed_count += world.missed_enemies
                    world.reset_level()
                    world.process_enemies()
                    world.game_speed = 1

                # Dibujar botones para colocar torretas
                # Para el boton de la torreta, mostrar el costo de la torreta y dibujar el boton
                draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))

                # Actualizar la imagen del botón de compra de torretas si hay o no suficiente dinero
                if world.money >= c.BUY_COST:
                    turret_buy_button.image = buy_turret_image
                else:
                    turret_buy_button.image = buy_turret_false_image

                if turret_buy_button.draw(screen):
                    placing_turrets = True
                
                #Si la colocacion de la torreta es correcta, crear la torreta
                if placing_turrets == True:
                    #Cursor en la torre
                    cursor_rect = cursor_turret.get_rect()
                    cursor_pos = pg.mouse.get_pos()
                    if cursor_pos[0] <= c.SCREEN_WIDTH:
                        cursor_rect.center = cursor_pos
                    screen.blit(cursor_turret, cursor_rect)
                    if cancel_button.draw(screen):
                        placing_turrets = False
                
                # Si la torreta es seleccionada, entonces mostrar el boton de mejora
                if selected_turret:
                    # Mostrar el nivel en que se encuentra la torreta
                    pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 400, 300, 320))
                    screen.blit(selected_turret.original_image, (c.SCREEN_WIDTH + 10, 400))
                    draw_text("TORRE DE BATALLA", text_font, "grey100", c.SCREEN_WIDTH + 10, 490)
                    draw_text("NIVEL: " + str(selected_turret.upgrade_level), text_font, "grey100", c.SCREEN_WIDTH + 10, 530)
                    # Barra para mostrar el nivel en que se encuentra la torreta
                    pg.draw.rect(screen, "grey100", (c.SCREEN_WIDTH + 10, 560, 280, 30))
                    pg.draw.rect(screen, "green", (c.SCREEN_WIDTH + 10, 560, (280 // c.TURRET_LEVELS) * selected_turret.upgrade_level, 30))
                    draw_text("ENEMIGOS ELIMINADOS: ", text_font, "grey100", c.SCREEN_WIDTH + 10, 610)
                    draw_text(str(selected_turret.kill_count), text_font, "grey100", c.SCREEN_WIDTH + 10, 640)

                    show_logo = False
                    comision = 0
                    # Si la torreta puede ser mejorada, entonces mostrar el boton de mejora
                    if selected_turret.upgrade_level < c.TURRET_LEVELS:
                        # Mostrar el costo de la mejora
                        if selected_turret.upgrade_level == 2:
                            comision = 50
                        elif selected_turret.upgrade_level == 3:
                            comision = 100
                        # Calcular el costo total si la torreta se encuentra en un nivel mayor
                        costo_total = c.UPGRADE_COST + comision
                        draw_text(str(costo_total), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
                        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
                        # Actualizar la imagen del botón de mejora de torretas si hay o no suficiente dinero
                        if world.money >= costo_total:
                            upgrade_button.image = upgrade_turret_image
                        else:
                            upgrade_button.image = upgrade_turret_false_image
                        if upgrade_button.draw(screen):
                            # Verificar Si hay suficiente dinero para mejorar la torreta
                            if world.money >= costo_total:
                                selected_turret.upgrade()
                                mejorar_fx.play()
                                world.money -= costo_total
                    # Calcular el monto a devolver al vender la torreta
                    base_value = c.BUY_COST
                    upgrade_cost = costo_total * (selected_turret.upgrade_level - 1)
                    sell_value = (base_value + upgrade_cost) // 2
                    # Mostrar la devolucion de dinero al vender la torreta
                    draw_text(str(sell_value), text_font, "grey100", c.SCREEN_WIDTH + 215, 255)
                    screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 250))
                    # Mostrar el boton de vender torreta
                    if sell_turret_button.draw(screen):
                        world.money += sell_value
                        turret_group.remove(selected_turret)
                        vender_fx.play()
                        selected_turret = None
                else:
                    show_logo = True

                # Revisar si el boton de salir es presionado
                if exit_button.draw(screen):
                    game_paused = True
                    confirm_exit = True
                
                # Revisar si el boton de pausa es presionado
                if pause_button.draw(screen):
                    game_paused = True
                
                # Revisar si el boton de reinicio es presionado
                if restart_level_button.draw(screen):
                    game_paused = True
                    confirm_restart = True
                
                # Revisar si el boton de volumen es presionado
                if volume_button.draw(screen):
                    if not volumen:
                        pg.mixer.music.set_volume(0.5)
                        volume_button.image = volume_on_image
                        volumen = True
                    else:
                        pg.mixer.music.set_volume(0)
                        volume_button.image = volume_off_image
                        volumen = False
        else:
            pg.draw.rect(screen, "grey", (200, 200, 400, 250), border_radius = 30)
            if game_outcome == -1:
                draw_text("FIN DEL JUEGO", large_font, "grey0", 285, 220)
                draw_text("HAS PERDIDO LA BATALLA", text_font, "grey0", 255, 270)
                draw_text("PUNTUACION: " + str((kill_count + world.health)), text_font, "grey0", 255, 310)
            elif game_outcome == 1:
                draw_text("¡HAS GANADO!", large_font, "grey0", 285, 220)
                draw_text("SOLDADOS ELIMINADOS: " + str(kill_count), text_font, "grey0", 255, 270)
                draw_text("SOLDADOS FALTANTES: " + str(missed_count), text_font, "grey0", 255, 300)
                draw_text("PUNTUACION: " + str((kill_count + world.health)), text_font, "grey0", 255, 330)
            # Reiniciar el nivel
            if restart_button.draw(screen):
                # Restablecer las variables de juego a su posicion inicial
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                nivel = 0
                kill_count = 0
                missed_count = 0
                inicio_nivel = False
                volumen = True
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                # Limpiar los grupos de enemigos y torretas
                enemy_group.empty()
                turret_group.empty()
            elif exit2_button.draw(screen):
                run = False
    else:
        # Confirmar la salida del juego
        if confirm_exit:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("¿QUIERES SALIR?", large_font, "grey0", 270, 240)
            yes_button = Button(275, 320, yes_image, click_fx, True)
            no_button = Button(425, 320, not_image, click_fx, True)

            if yes_button.draw(screen):
                in_menu = True
                game_over = False
                confirm_exit = False
                game_paused = False
                # Restablecer el juego a su posición inicial
                level_started = False
                placing_turrets = False
                selected_turret = None
                nivel = 0
                kill_count = 0
                missed_count = 0
                inicio_nivel = False
                volumen = True
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                enemy_group.empty()
                turret_group.empty()

            if no_button.draw(screen):
                confirm_exit = False
                game_paused = False
        # Confirmar el reinicio del nivel
        elif confirm_restart:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("¿REINICIAR NIVEL?", large_font, "grey0", 255, 240)
            yes_button = Button(275, 320, yes_image, click_fx, True)
            no_button = Button(425, 320, not_image, click_fx, True)

            if yes_button.draw(screen):
                game_over = False
                confirm_restart = False
                game_paused = False
                # Restablecer el juego a su posición inicial
                level_started = False
                placing_turrets = False
                selected_turret = None
                nivel = 0
                kill_count = 0
                missed_count = 0
                inicio_nivel = False
                volumen = True
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                enemy_group.empty()
                turret_group.empty()

            if no_button.draw(screen):
                confirm_restart = False
                game_paused = False
        # Pausar el juego
        elif game_paused:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("JUEGO PAUSADO", large_font, "grey0", 270, 240)
            continue_button = Button(325, 320, continue_image, click_fx, True)
            if continue_button.draw(screen):
                game_paused = False

    # Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Chequiar si el ratón se encuentra sobre una torreta
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Limpiar la seleccion de la torre
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    # Revisar si hay suficiente dinero para poner una torreta
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    pg.display.flip()

pg.quit()