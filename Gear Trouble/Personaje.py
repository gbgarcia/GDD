# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame
import os

from Globals import *
import Globals
import PixelPerfectCollision

class Personaje(pygame.sprite.Sprite):
    
    ##### por simplicidad, asumo que todas las imagenes de personaje son del mismo tamaño

    def __init__(self, color, x):
        """ Construye un personaje
color: 0 o 1 (primer o segundo player)
x: coordenada x inicial
"""
        pygame.sprite.Sprite.__init__(self)
        
        # self.stand y self.moving contienen (image,hitmask)
        
        standSurface=pygame.image.load("imagenes/p"+str(color)+"_stand.png").convert_alpha()
        self.stand = (standSurface, PixelPerfectCollision.get_alpha_hitmask(standSurface))

        # moving: [izq/der][n de animacion]
        self.moving=[[None for __i in range(IMGS_ANIMACION_P)] for __i in range(2)]
        for i in range(IMGS_ANIMACION_P):
            movingSurface=pygame.image.load("imagenes/p"+str(color)+"_left" +str(i)+".png").convert_alpha()
            self.moving[0][i] = (movingSurface, PixelPerfectCollision.get_alpha_hitmask(movingSurface))
            
            #movingSurface=pygame.image.load("imagenes/p"+str(color)+"_right"+str(i)+".png").convert_alpha()
            # o para que la derecha sea la izquierda espejada:
            movingSurface=pygame.transform.flip(movingSurface, True, False)
            ####### cuando esten las imagenes: cambiar
            self.moving[1][i] = (movingSurface, PixelPerfectCollision.get_alpha_hitmask(movingSurface))
        
        self.rect=self.stand[0].get_rect()
        
        if color!=0 and color!=1:
            raise Exception("Número de personaje inválido: "+str(color))
        self.num=color
        
        self.x=x
        self.rect.centerx=x # se pasa a int
        self.rect.bottom=ALTURA_PISO
        self.movimiento=PARADO
        self.contador_mov=0
        self.tipoBala=BALA_NORMAL
        
    def update(self, direccionPersonajes):
        
        if direccionPersonajes[self.num]==PARADO:
            self.movimiento=PARADO
        elif direccionPersonajes[self.num]!=None:
            self.movimiento=direccionPersonajes[self.num]
        
        if self.movimiento==PARADO:
            (self.image,self.hitmask) = self.stand
            self.contador_mov=0
        else:
            mov=0
            if self.movimiento==DERECHA:
                mov=1
            (self.image,self.hitmask) = self.moving[mov][ int(self.contador_mov/FRAMES_POR_IMAGEN_P) ]
            self.contador_mov = (self.contador_mov+1) % (IMGS_ANIMACION_P*FRAMES_POR_IMAGEN_P) # 0,0,1,1,2,2,3,3,0,0,1, ...
            
            self.x += VELOC_MOV_PERSONAJES * self.movimiento
            self.rect.centerx=self.x # se pasa a int
            
            while self.estoyDentroDeUnaPared():
                self.x-=self.movimiento
                self.rect.centerx=self.x # se pasa a int
                # solo correrlo, se ve mejor sin parar la animacion
            
    def estoyDentroDeUnaPared(self):
        return self.rect.collidelist(Globals._paredes)!=-1