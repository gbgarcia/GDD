# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import sys
import pygame
from pygame.locals import *
#from random import randint

from Globals import *
import Globals
from Personaje import Personaje
from Engranaje import Engranaje

def main():
    pygame.init()
    fpsClock=pygame.time.Clock()
    
    global screenSurface
    fullscreen_flag=0
    if FULLSCREEN:
        fullscreen_flag=pygame.FULLSCREEN;
    screenSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
    
    cargarSurfacesEngranajes()
    
    personajes = pygame.sprite.Group()
    engranajes = pygame.sprite.Group()
    balas      = pygame.sprite.Group()
    power_ups  = pygame.sprite.Group()
    # creo que tambien se podria tener un solo grupo con capas, pygame.sprite.LayeredUpdates, pero filo
    
    # aqui hay que ver que pasa si hay 1 o 2 jugadores
    personajes.add(Personaje(0,200))
    #personajes.add(Personaje(1,400))    no tengo imagenes de player2 por mientras
    
    engranajes.add(Engranaje(300,300, 6, DERECHA, 0))
    
    # un fondo
    backgroundSurface=pygame.image.load("imagenes/fondo1.png").convert()
    screenSurface.blit(backgroundSurface, (0,0))
    
    # paredes que limitan el movimiento en horizontal
    # _paredes bloquea personajes y engranajes, _paredesEngranajes solo a engranajes
    # deben ir en vertical de 0 a SCREEN_HEIGHT
    Globals._paredes=[Rect(0,0,10,SCREEN_HEIGHT), Rect(SCREEN_WIDTH-10,0,10,SCREEN_HEIGHT)]   # paredes de los lados con un ancho de 10
    Globals._paredesEngranajes=[]
    # ... agregar otros muros y puertas de cada nivel
    
    # loop principal
    while True:
        movimientoPersonajes=[None,None]

        # --- TECLAS
        for event in pygame.event.get():
            if (    event.type==QUIT or
                    (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT))):  # alt-f4 no me funciona sin esto
                pygame.quit()
                sys.exit(0)
                
            elif event.type==KEYDOWN:
                if event.key==K_LEFT:
                    movimientoPersonajes[0]=IZQUIERDA
                elif event.key==K_RIGHT:
                    movimientoPersonajes[0]=DERECHA
                # El arcade (se supone que) va a ser con palanca, asi que filo con detectar si se apretan las flechas izq/der al mismo tiempo
                elif event.key==K_a:
                    movimientoPersonajes[1]=IZQUIERDA
                elif event.key==K_d:
                    movimientoPersonajes[1]=DERECHA
                    
                elif event.key==K_F12:
                    pass    # poner un breakpoint aqui -> F12 es debug
                        
            elif event.type==KEYUP:
                if event.key==K_LEFT or event.key==K_RIGHT:
                    movimientoPersonajes[0]=PARADO
                elif event.key==K_a or event.key==K_d:
                    movimientoPersonajes[1]=PARADO
        
        # --- EJECUTAR
        # orden: personajes, balas, engranajes, power_ups
        personajes.update(movimientoPersonajes)
        #balas.update()
        engranajes.update()
        #power_ups.update()
        
        # --- LIMPIAR
        personajes.clear(screenSurface, backgroundSurface)
        engranajes.clear(screenSurface, backgroundSurface)
        balas     .clear(screenSurface, backgroundSurface)
        power_ups .clear(screenSurface, backgroundSurface)
        
        # --- DIBUJAR
        # orden: (atras para adelante)
        # balas, personajes, power_ups, engranajes
        balas     .draw(screenSurface)
        personajes.draw(screenSurface)
        power_ups .draw(screenSurface)
        engranajes.draw(screenSurface)
        
        
        pygame.display.update()
        fpsClock.tick(60)
        
def cargarSurfacesEngranajes():
    N_COLORES=4
    #TAMAÑO_MAX=6
    MAX_SIZE=25
    
    Globals.SURFACE_ENGRANAJES=[[None for __i in range(MAX_SIZE+1)] for __i in range(N_COLORES)]
    for color in range(N_COLORES):
        surfaceOriginal=pygame.image.load("imagenes/engranaje"+str(color)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        Globals.SURFACE_ENGRANAJES[color][MAX_SIZE]=surfaceOriginal
        for size in range(MAX_SIZE):
            diametro2=size*diametro/MAX_SIZE
            Globals.SURFACE_ENGRANAJES[color][size]=pygame.transform.smoothscale(surfaceOriginal, (diametro2,diametro2))

main()
