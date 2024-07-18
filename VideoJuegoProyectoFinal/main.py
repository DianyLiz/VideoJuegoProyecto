import pygame as pg
from enemy import Enemy
import constants as c
pg.init()

#crear un reloj
clock = pg.time.Clock()


screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

enemy_image = pg.image.load("imagen/enemy_1.png").convert_alpha()

#crear un grupo de imagenes
enemy_group = pg.sprite.Group()

enemy = Enemy((200,300),enemy_image)

#Añadir el imagen al grupo
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)
    screen.fill("grey100")

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

