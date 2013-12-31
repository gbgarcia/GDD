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
    #personajes.add(Personaje(1,400)) no tengo imagenes de player2 por mientras
    
    engranajes.add(Engranaje(100,200, 1, PARADO, 0, 0))
    engranajes.add(Engranaje(250,200, 2, PARADO, 0, 0))
    engranajes.add(Engranaje(400,200, 3, PARADO, 0, 0))
    engranajes.add(Engranaje(550,200, 4, PARADO, 0, 0))
    engranajes.add(Engranaje(700,200, 5, PARADO, 0, 0))
    engranajes.add(Engranaje(850,200, 6, PARADO, 0, 0))
    
    # un fondo
    backgroundSurface=pygame.image.load("imagenes/fondo1.png").convert()
    screenSurface.blit(backgroundSurface, (0,0))
    
    # paredes que limitan el movimiento en horizontal
    # _paredes bloquea personajes y engranajes, _paredesEngranajes solo a engranajes
    # deben ir en vertical de 0 a SCREEN_HEIGHT
    Globals._paredes=[Rect(0,0,10,SCREEN_HEIGHT), Rect(SCREEN_WIDTH-10,0,10,SCREEN_HEIGHT)] # paredes de los lados con un ancho de 10
    Globals._paredesEngranajes=[]
    # ... agregar otros muros y puertas de cada nivel
    ####### por ej:
    #Globals._paredes.append(Rect(800,0,60,SCREEN_HEIGHT))
    #Globals._paredesEngranajes.append(Rect(100,0,60,SCREEN_HEIGHT))
    
    movimientoPersonajes=[[False,False],[False,False]]  # [p1/p2][izq/der]
    
    # loop principal
    while True:
        # --- TECLAS
        for event in pygame.event.get():
            if ( event.type==QUIT or
                    (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT))): # alt-f4 no me funciona sin esto
                pygame.quit()
                sys.exit(0)
                
            elif event.type==KEYDOWN:
                if event.key==K_LEFT:
                    movimientoPersonajes[0][0]=True
                elif event.key==K_RIGHT:
                    movimientoPersonajes[0][1]=True
                elif event.key==K_a:
                    movimientoPersonajes[1][0]=True
                elif event.key==K_d:
                    movimientoPersonajes[1][1]=True
                    
                elif event.key==K_F12:
                    pass # poner un breakpoint aqui -> F12 es debug
                
                elif event.key==K_p:    # pausa
                    salir=False
                    while not salir:
                        fpsClock.tick(60)
                        for event2 in pygame.event.get():
                            if event2.type==KEYUP and event2.key==K_p:      # esperar a q se suelte P
                                salir=True
                    salir=False
                    while not salir:
                        fpsClock.tick(60)
                        for event2 in pygame.event.get():
                            if event2.type==KEYDOWN and event2.key==K_p:    # esperar a q se aprete P
                                salir=True
                        
            elif event.type==KEYUP:
                if event.key==K_LEFT:
                    movimientoPersonajes[0][0]=False
                elif event.key==K_RIGHT:
                    movimientoPersonajes[0][1]=False
                elif event.key==K_a:
                    movimientoPersonajes[1][0]=False
                elif event.key==K_d:
                    movimientoPersonajes[1][1]=False
        
        # --- EJECUTAR
        # orden: personajes, balas, engranajes, power_ups
        
        direccionPersonajes=[PARADO,PARADO]
        for player in range(2):
            if   movimientoPersonajes[player][0] and not movimientoPersonajes[player][1]:
                direccionPersonajes[player]=IZQUIERDA
            elif movimientoPersonajes[player][1] and not movimientoPersonajes[player][0]:
                direccionPersonajes[player]=DERECHA
        personajes.update(direccionPersonajes)
        
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
    Globals.SURFACE_ENGRANAJES=[[None for __i in range(MAX_SIZE_ENGRANAJES+1)] for __i in range(N_COLORES_ENGRANAJES)]
    for color in range(N_COLORES_ENGRANAJES):
        surfaceOriginal=pygame.image.load("imagenes/engranaje"+str(color)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        Globals.SURFACE_ENGRANAJES[color][MAX_SIZE_ENGRANAJES]=surfaceOriginal
        for size in range(MAX_SIZE_ENGRANAJES):
            diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro / MAX_SIZE_ENGRANAJES )
            Globals.SURFACE_ENGRANAJES[color][size]=pygame.transform.smoothscale(surfaceOriginal, (diametro2,diametro2))

main()