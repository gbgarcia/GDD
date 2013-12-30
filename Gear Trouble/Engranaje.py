# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame
import os

from Globals import *
import Globals

class Engranaje(pygame.sprite.Sprite):
    
    def __init__(self, x,y , size, direccion, color, sube):
        """ Construye un engranaje
x,y: centro de la posicion inicial
size (no se puede 'tamaño'): cuantos golpes le faltan para romperse
direccion: IZQUIERDA/DERECHA
color: 1,2,3,... para cargar la imagen
sube: BAJA/SUBE
"""
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.size=size
        self.direccion=direccion
        self.color=color
        self.sube=sube

        self.image=Globals.SURFACE_ENGRANAJES[color][size]
        self.rect=self.image.get_rect()
        
    def update(self):
        self.x += VELOC_X_ENGRANAJES * self.direccion
        self.y += VELOC_Y_ENGRANAJES * self.sube
         
        if self.x - 73.411 <= 0 or self.x + 73.411 >= SCREEN_WIDTH:
              self.direccion = -self.direccion

        if self.y + 73.411 >= ALTURA_PISO or self.y - 73.65778 <= 0:
              self.sube = -self.sube 
        
        self.rect.center=(self.x,self.y) # se pasa a int