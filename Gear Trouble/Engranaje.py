# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame
import os

from Globals import *
import Globals

class Engranaje(pygame.sprite.Sprite):
    
    def __init__(self, x,y , size, direccion, color, veloc_y):
        """ Construye un engranaje
x,y: centro de la posicion inicial
size (no se puede 'tamaño'): cuantos golpes le faltan para romperse
direccion: IZQUIERDA/DERECHA/PARADO
color: 1,2,3,... para cargar la imagen
veloc_y: velocidad en y
"""
        pygame.sprite.Sprite.__init__(self)
        
        self.x=x
        self.y=y
        
        if size<1 or size>MAX_SIZE_ENGRANAJES:
            raise Exception("Tamaño de engranaje fuera de rango: "+str(size))
        self.size=size
        
        if direccion<-1 or direccion>1:
            raise Exception("Dirección de engranaje inválida: "+str(direccion))
        self.direccion=direccion
        
        if color<0 or color>=N_COLORES_ENGRANAJES:
            raise Exception("Color de engranaje fuera de rango: "+str(color))
        self.color=color
        
        self.veloc_y=veloc_y

        (self.image,self.hitmask) = Globals.SURFACE_ENGRANAJES[color][size]
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y) # se pasa a int
        
    def update(self):
        
        # movimiento horizontal
        self.x += VELOC_X_ENGRANAJES * self.direccion
        self.rect.centerx=self.x
        
        # rebote horizontal
        paredContraLaQueChoco=None
        
        indexCollide=self.rect.collidelist(Globals._paredes)
        if indexCollide!=-1:
            paredContraLaQueChoco=Globals._paredes[indexCollide]
            
        indexCollide=self.rect.collidelist(Globals._paredesEngranajes)
        if indexCollide!=-1:
            paredContraLaQueChoco=Globals._paredesEngranajes[indexCollide]
            
        if paredContraLaQueChoco:
            if self.direccion==DERECHA:
                self.x += (paredContraLaQueChoco.left-self.rect.right) * 2
            else:
                self.x -= (self.rect.left-paredContraLaQueChoco.right) * 2
            self.rect.centerx=self.x
            self.direccion*=-1
        
        # movimiento vertical
        self.veloc_y += ACEL_Y_ENGRANAJES
        self.y += self.veloc_y
        self.rect.centery=self.y
        
        # rebote vertical
        if self.rect.bottom >= ALTURA_PISO:
            self.veloc_y = VELOC_Y_REBOTE_ENG * pow(self.size, FACTOR_REBOTE_SIZE)
            self.y -= (self.rect.bottom-ALTURA_PISO) * 2
            self.rect.centery=self.y

        """ lo lamento, esto esta harcode-eado a este tamaño de engranaje, en un nivel sin paredes
if self.x - 73.411 <= 0 or self.x + 73.411 >= SCREEN_WIDTH:
self.direccion = -self.direccion

if self.y + 73.411 >= ALTURA_PISO or self.y - 73.65778 <= 0:
self.sube = -self.sube """
              
        # choque contra el techo
        if self.rect.top <= ALTURA_TECHO:
            self.sacar(False)
            # TODO: combo!
        
    def sacar(self,crearOtros):
        Globals._engranajesSacar.append(self)
        if crearOtros:
            # retorna una lista con los creados
            if self.size==1:
                return []
            else:
                despl_x=self.rect.width*DIST_CENTRO_ENGRS_CREADOS
                nueva_vy=0################## cambiar
                lista=[]
                lista.append(Engranaje(self.x-despl_x, self.y, self.size-1, IZQUIERDA, self.color, nueva_vy))
                lista.append(Engranaje(self.x+despl_x, self.y, self.size-1, DERECHA , self.color, nueva_vy))
                return lista