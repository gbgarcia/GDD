# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame

from Globals import *
import Globals

class Efecto(pygame.sprite.Sprite):
    
    def __init__(self, x,y , imagenes, framesPorImagen):
        """ Un efecto, por ejemplo el pop! de cuando se rompe un engranaje
        x,y: centro de la posicion inicial
        imagenes: arreglo con imagenes a mostrar
        framesPorImagen: cuantos frames dura cada imagen"""
        
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.imagenes=imagenes
        self.framesPorImagen=framesPorImagen
        self.contadorImagen=0
        self.update()
    
    def update(self):
        self.image=self.imagenes[ self.contadorImagen/self.framesPorImagen ]
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)
        self.contadorImagen+=1
        if self.contadorImagen== len(self.imagenes)*self.framesPorImagen:
            Globals._efectosSacar.append(self)
    