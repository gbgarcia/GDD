import pygame
import os

# const
IMGS_ANIMACION  = 4 ############### cambiar

IZQUIERDA   = 0
DERECHA     = 1
PARADO      = 2

class Personaje(pygame.sprite.Sprite):
    
    def _init__(self, num, x, ALTURA_PISO):
        """ Construye un personaje
        num: 0 o 1 (primer o segundo player)
        x: coordenada x inicial
        """
        self.ALTURA_PISO=ALTURA_PISO;
        pygame.sprite.Sprite.__init__(self)
        
        """self.standSurface=pygame.image.load("imagenes/stand.png").convert()
        self.standSurface_rect=self.standSurface.get_rect()
        
        # movingSurfaces: [izq/der][n de animacion]
        self.movingSurfaces=[[None for i in range(IMGS_ANIMACION)] for i in range(2)]
        self.movingSurfaces_rect=[[None for i in range(IMGS_ANIMACION)] for i in range(2)]
        for i in range(IMGS_ANIMACION):
            self.movingSurfaces[0][i]=pygame.image.load("imagenes/move"+str(i)+".png").convert()
            self.movingSurfaces[1][i]=pygame.transform.flip( self.movingSurfaces[0][i], True, False )
            
            self.movingSurfaces_rect[0][i]=self.movingSurfaces[0][i].get_rect()
            self.movingSurfaces_rect[1][i]=self.movingSurfaces[1][i].get_rect()

        self.num=num
        self.x=x
        self.y=ALTURA_PISO
        self.movimiento=PARADO
        self.contador_mov=-1"""
        
    def update(self,accion):
        
        #if accion==

        if self.movimiento==PARADO:
            self.image = self.standSurface
            self.rect  = self.standSurface_rect
        else:
            self.image = self.movingSurfaces[self.movimiento][self.contador_mov]
            self.rect  = self.movingSurfaces_rect[self.movimiento][self.contador_mov]
            
        
            