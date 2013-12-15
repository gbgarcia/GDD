# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame
import os

from Globals import *
import Globals

class Personaje(pygame.sprite.Sprite):
    
    ##### por simplicidad, asumo que todas las imagenes de personaje son del mismo tamaño

    def __init__(self, num, x):
        """ Construye un personaje
        num: 0 o 1 (primer o segundo player)
        x: coordenada x inicial
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.standSurface=pygame.image.load("imagenes/p"+str(num)+"_stand.png").convert_alpha()

        # movingSurfaces: [izq/der][n de animacion]
        self.movingSurfaces=[[None for __i in range(IMGS_ANIMACION)] for __i in range(2)]
        for i in range(IMGS_ANIMACION):
            self.movingSurfaces[0][i]=pygame.image.load("imagenes/p"+str(num)+"_left" +str(i)+".png").convert_alpha()
            #self.movingSurfaces[1][i]=pygame.image.load("imagenes/p"+str(num)+"_right"+str(i)+".png").convert_alpha()
            # o para que la derecha sea la izquierda espejada:
            self.movingSurfaces[1][i]=pygame.transform.flip( self.movingSurfaces[0][i], True, False )
            ####### cuando esten las imagenes: comentar la linea de arriba, descomentar la 3 mas arriba, borrar esta linea

        
        self.rect=self.standSurface.get_rect()
        self.num=num
        self.x=x
        self.rect.bottom=ALTURA_PISO
        self.movimiento=PARADO
        self.contador_mov=0
        
    def update(self, moverseHacia):
        
        if moverseHacia[self.num]==PARADO:
            self.movimiento=PARADO
        elif moverseHacia[self.num]!=None:  
            self.movimiento=moverseHacia[self.num]
        
        if self.movimiento==PARADO:
            self.image=self.standSurface
            self.contador_mov=0
        else:
            self.image=self.movingSurfaces[self.movimiento][ int(self.contador_mov/FRAMES_POR_IMAGEN) ]
            self.contador_mov = (self.contador_mov+1) % (IMGS_ANIMACION*FRAMES_POR_IMAGEN)  # 0,0,1,1,2,2,3,3,0,0,1, ...
            
            self.x += VELOC_MOV_PERSONAJES * self.movimiento
            while self.estoyDentroDeUnaPared():
                self.x-=self.movimiento
                # solo correrlo, se ve mejor sin parar la animacion
                
        self.rect.centerx=self.x    # se pasa a int
            
    def estoyDentroDeUnaPared(self):
        return self.rect.collidelist(Globals._paredes)!=-1
