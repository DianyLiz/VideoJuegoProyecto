import os
os.system('cls' if os.name == 'nt' else 'clear')


import pygame as pg
import json
from enemy import Enemy
from world import World
import constants as c
pg.init()

#crear un reloj
clock = pg.time.Clock()


screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

map_image = pg.image.load("levels/level.png").convert_alpha()

enemy_image = pg.image.load("imagen/enemy_1.png").convert_alpha()

#Cargar el archivo json
with open("levels/level.tmj") as file:
    world_data = json.load(file)


#crear un mundo

world = World(world_data,map_image)

world.process_data()

#crear un grupo de imagenes
enemy_group = pg.sprite.Group()


enemy = Enemy(world.waypoints,enemy_image)

#Añadir el imagen al grupo
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)
    screen.fill("grey100")

    #dibujar el mundo
    world.draw(screen)

    

    #Actualiza los grupos
    enemy_group.update()
    #Dibujar el grupo 
    enemy_group.draw(screen)

    #Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False


    pg.display.flip()

pg.quit()

