import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, title_x, title_y):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")#rango de la torre
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        #posicion de la variable
        self.title_x = title_x
        self.title_y = title_y

        #calcular centro de las coordenadas
        self.x = (self.title_x + 0.5)* c.TILE_SIZE
        self.y = (self.title_y + 0.5)* c.TILE_SIZE

        #animacion de la variable
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #Actualizar imagen
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)

        #crear circulo transparente para el rango
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    def load_images(self, sprite_sheet):
        #Extraer las imagenes de la hoja de animacion
        size = sprite_sheet.get_height()
        animation_list = []

        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group):
        #si el rango esta seleccionado
        if self.target:
            self.play_animation()
        else:
        #Busqueda desde nueva posicion a la actual
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        #mas cercano a la torre
        x_dist = 0
        y_dist = 0

        #Chequiar la distancia entre el enemigo y la torre
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= c.DAMAGE
                    break #salir del bucle

    def play_animation(self):
        #actualizar imagen
        self.original_image = self.animation_list[self.frame_index]

        #actualizar tiempo
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            #Chequear si la animacion ha terminado
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                #recorrer completo tiempo y limpieza de torres
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")#rango de la torre
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")

        #actualizar imagen de la torre
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        #actualizar circulo transparente para el rango
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw (self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
            