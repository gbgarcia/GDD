# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame
import os

from Globals import *
import Globals

class Engranaje(pygame.sprite.Sprite):
    
    def __init__(self, x,y , size, direccion, color):
        """ Construye un engranaje
        x,y: centro de la posicion inicial
        size (no se puede 'tamaño'): cuantos golpes le faltan para romperse
        direccion: IZQUIERDA/DERECHA
        color: 1,2,3,... para cargar la imagen
        """
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.size=size
        self.direccion=direccion
        self.color=color

        self.image=Globals.SURFACE_ENGRANAJES[color][size]
        self.rect=self.image.get_rect() 
        
    def update(self):
        self.x += VELOC_X_ENGRANAJES * self.direccion
        
        self.rect.center=(self.x,self.y)    # se pasa a int