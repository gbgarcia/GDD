# -*- coding: utf-8 -*-
# (si no, no puedo escribir �)

import pygame
import os

from Globals import *
import Globals

class Bala(pygame.sprite.Sprite):
    
    def __init__(self, personajePadre):
        """ Una bala, de cualquier tipo
personajePadre: el personaje que disparó esta bala
"""
        pygame.sprite.Sprite.__init__(self)
        
        self.tipo=personajePadre.tipoBala
        self.num=personajePadre.num
        
        if self.tipo==BALA_NORMAL or self.tipo==BALA_GANCHO:
            """self.image=pygame.Surface((ANCHO_BALA_NORMAL,SCREEN_HEIGHT))
self.image.fill(COLORES_BALAS[self.num])
self.rect=pygame.Rect(0,0,ANCHO_BALA_NORMAL,0)
self.hitmask=Globals.HITMASK_BALAS_NORMALES"""
            self.image=Globals.SURFACE_BALAS_NORMALES[self.num]
            (self.rect,self.hitmask) = Globals.RH_BALAS_NORMALES
            
        self.rect.centerx=personajePadre.x
        self.y = self.rect.top = ALTURA_PISO-ALTURA_SALIDA_BALA
        
    def update(self):
        
        # movimiento
        if self.tipo==BALA_NORMAL or self.tipo==BALA_GANCHO:
            self.y-=VELOC_SUBIDA_BALA_NORMAL
            self.rect.top=self.y
            self.rect.height=ALTURA_PISO-self.rect.top
            
        # choque con techo
        if self.y<=ALTURA_TECHO:
            self.sacar()
            
    def sacar(self):
        Globals._balasSacar.append(self)
            