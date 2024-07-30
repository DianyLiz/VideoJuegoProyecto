import os
os.system('cls' if os.name == 'nt' else 'clear')


from typing import Any
import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

#Clase enemigo 
class Enemy(pg.sprite.Sprite):
    def __init__(self,enemy_type,waypoints,images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    #Movimiento
    def move(self, world):
        #definir el punto de destino
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemigo ha llegado al destino
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        #calcular la distancia entre el punto de destino y el enemigo
        dist = self.movement.length()

        #chequiar si el enemigo ha alcanzado el punto de destino
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            #si no ha alcanzado el punto de destino, se mueve al siguiente punto de destino
            if dist > 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1
   
    def rotate(self):
        #calcular la distancia entre el punto de destino y el enemigo
        dist = self.target - self.pos
        #usar la formula para rotar el enemigo
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        #rotar la imagen del enemigo
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.kill_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()