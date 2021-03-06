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
            self.image=Globals.SURFACE_BALAS_NORMALES[self.num]
            (self.rect,self.hitmask) = Globals.RH_BALAS_NORMALES
            Globals._sonidos["bala"].play()
        elif self.tipo==BALA_FUGAZ:
            self.vy=VELOC_INI_BALA_FUGAZ
            self.nFrame=0
            self.rect=Globals.SURFACE_BALAS_FUGAZ[0][1]
            self.x=personajePadre.x
            Globals._sonidos["fugaz"].play()
            
        self.rect.centerx=personajePadre.x
        self.y = self.rect.top = ALTURA_PISO-ALTURA_SALIDA_BALA
        self.framesClavada=0
        
    def update(self):
        if self.tipo==BALA_NORMAL or self.tipo==BALA_GANCHO:
            if self.framesClavada==0:   
                # movimiento
                self.y-=VELOC_SUBIDA_BALA_NORMAL
                self.rect.top=self.y
                self.rect.height=ALTURA_PISO-self.rect.top
                if self.y<=ALTURA_TECHO:    # choque con techo
                    if self.tipo!=BALA_GANCHO:
                        self.sacar()
                    else:
                        self.framesClavada=1
                        self.rect.top=ALTURA_TECHO
                        self.image=Globals.SURFACE_BALAS_GANCHO[self.num]
            
            else:       # bala gancho clavada
                self.framesClavada+=1
                if self.framesClavada>FRAMES_B_GANCHO_CLAVADA:
                    self.sacar()
        
        elif self.tipo==BALA_FUGAZ:
            (self.image, self.rect, self.hitmask) = Globals.SURFACE_BALAS_FUGAZ[self.nFrame]
            self.rect.centerx=self.x
            self.nFrame+=1
            self.vy+=ACEL_SUBIDA_BALA_FUGAZ
            self.y-=self.vy
            self.rect.top=self.y
            if self.y<=ALTURA_TECHO:    # choque con techo
                self.sacar()
        
        elif self.tipo==BALA_TORRE:
            pass

            
    def sacar(self):
        Globals._balasSacar.append(self)
            