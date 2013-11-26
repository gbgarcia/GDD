import sys
import pygame
from pygame.locals import *
from random import randint

from Personaje import *

# constantes
SCREEN_WIDTH    = 1024
SCREEN_HEIGHT   = 768
FULLSCREEN      = False
ALTURA_PISO     = 600

class Main:

    def _init__(self):
        pygame.init()
        fpsClock=pygame.time.Clock()
    
        global windowSurface
        fullscreen_flag=0
        if FULLSCREEN:
            fullscreen_flag=pygame.FULLSCREEN;
        windowSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
        
        personajes = pygame.sprite.Group()
        engranajes = pygame.sprite.Group()
        balas      = pygame.sprite.Group()
        power_ups  = pygame.sprite.Group()
        
        # crear dos personajes, para probar
        personajes.add(Personaje(0,200))
        personajes.add(Personaje(1,400))
        
        
        
        # loop principal
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type==KEYDOWN:
                    # procesar teclas...
                    pass
                
            # orden de ejecucion: personajes, balas, engranajes, power_ups
            
            
            # borrar rastros
            
            
            # orden de dibujo: (atras para adelante)
            # balas, power_ups, personajes, engranajes
            
            
            pygame.display.update()
            fpsClock.tick(60)
            
Main()