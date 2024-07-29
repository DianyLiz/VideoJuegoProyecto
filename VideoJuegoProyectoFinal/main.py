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
selected_turret = None

map_image = pg.image.load("levels/level.png").convert_alpha()

#torre individual imagen
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f"imagen/turret_{x}.png").convert_alpha()
    turret_spritesheets.append(turret_sheet)

#Torre individual imagen 
cursor_turret = pg.image.load("imagen/cursor_turret.png").convert_alpha()
enemy_images = {
    "weak": pg.image.load("imagen/enemy_1.png").convert_alpha(),
    "medium": pg.image.load("imagen/enemy_2.png").convert_alpha(),
    "strong": pg.image.load("imagen/enemy_3.png").convert_alpha(),
    "elite": pg.image.load("imagen/enemy_4.png").convert_alpha()
    
}

#Boton 
buy_turret_image = pg.image.load("Botones/buy_turret.png").convert_alpha()
cancel_turret_image = pg.image.load("Botones/cancel.png").convert_alpha()
upgrade_turret_image = pg.image.load("Botones/upgrade_turret.png").convert_alpha()

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
            new_turret = Turret(turret_spritesheets, mouse_title_x, mouse_title_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
  mouse_title_x = mouse_pos[0] // c.TILE_SIZE
  mouse_title_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_title_x, mouse_title_y) == (turret.title_x, turret.title_y):
      return turret
    
def clear_selection():
    for turret in turret_group:
        turret.selected = False

#crear un mundo

world = World(world_data,map_image)

world.process_data()
world.process_enemies()

#crear un grupo 
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#crear botones
turret_buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_buy_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_turret_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)


enemy_type = "weak"
enemy = Enemy(enemy_type,world.waypoints,enemy_images)

#Añadir el imagen al grupo
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)

    #Actualiza los grupos
    enemy_group.update()
    turret_group.update(enemy_group)

    #seleccionada en el cursor del ratón 
    if selected_turret:
        selected_turret.selected = True

    screen.fill("grey100")

    #dibujar el mundo
    world.draw(screen)

    
    #Dibujar el grupo 
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

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

        #Si la torre es seleccionada actualizar la torre
    if selected_turret:
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()
                        

    #Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
      #Chequiar si el mouse se encuentra en el area del juego
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
             #Limpiar la torre seleccionada
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)


    pg.display.flip()

pg.quit()

