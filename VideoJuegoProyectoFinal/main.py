import os
os.system('cls' if os.name == 'nt' else 'clear')


import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c
pg.init()

#crear un reloj
clock = pg.time.Clock()

#CREAR VIDEOJUEGO WINDOW
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#Variables del Juego
placing_turrets = False

map_image = pg.image.load("levels/level.png").convert_alpha()

#torre individual imagen
turret_sheet = pg.image.load("imagen/turret_1.png").convert_alpha()

#Torre individual imagen 
cursor_turret = pg.image.load("imagen/cursor_turret.png").convert_alpha()

enemy_image = pg.image.load("imagen/enemy_1.png").convert_alpha()

#Boton 
buy_turret_image = pg.image.load("Botones/buy_turret.png").convert_alpha()
cancel_turret_image = pg.image.load("Botones/cancel.png").convert_alpha()

#Cargar el archivo json
with open("levels/level.tmj") as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_title_x = mouse_pos[0] // c.TILE_SIZE
    mouse_title_y = mouse_pos[1] // c.TILE_SIZE
    #Calcular la secuencia de numeros del titulo
    mouse_tile_num = (mouse_title_y * c.COLS) + mouse_title_x
    #Chequiar si el titulo es valido
    if world.tile_map[mouse_tile_num] == 7:
        #Chequiar si el cursor se encuentra sobre una torre
        space_is_free = True
        for turret in turret_group:
            if (mouse_title_x, mouse_title_y) == (turret.title_x, turret.title_y):
                space_is_free = False
        #Si la torre no es una torre no valida, no crearla
        if space_is_free == True:
            new_turret = Turret(turret_sheet, mouse_title_x, mouse_title_y)
            turret_group.add(new_turret)
#crear un mundo

world = World(world_data,map_image)

world.process_data()

#crear un grupo 
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#crear botones
turret_buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_buy_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_turret_image, True)


enemy = Enemy(world.waypoints,enemy_image)

#Añadir el imagen al grupo
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)

    #Actualiza los grupos
    enemy_group.update()
    turret_group.update()

    screen.fill("grey100")

    #dibujar el mundo
    world.draw(screen)

    
    #Dibujar el grupo 
    enemy_group.draw(screen)
    turret_group.draw(screen)

    #Dibujar los botones
    if turret_buy_button.draw(screen):
        placing_turrets = True
    
    #Si la colocacion de la torre es correcta, crear la torre
    if placing_turrets == True:
        #Cursor en la torre
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            cursor_rect.center = cursor_pos
        screen.blit(cursor_turret, cursor_rect)
        if cancel_buy_button.draw(screen):
            placing_turrets = False

    #Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Chequiar si el ratón se encuentra sobre una torre
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                if placing_turrets == True:
                    create_turret(mouse_pos)


    pg.display.flip()

pg.quit()

