# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import sys
import pygame
from pygame.locals import *
#from random import randint

from Constantes import *
from Personaje import *

def main():
    pygame.init()
    fpsClock=pygame.time.Clock()
    
    global screenSurface
    fullscreen_flag=0
    if FULLSCREEN:
        fullscreen_flag=pygame.FULLSCREEN;
    screenSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
    
    personajes = pygame.sprite.Group()
    engranajes = pygame.sprite.Group()
    balas      = pygame.sprite.Group()
    power_ups  = pygame.sprite.Group()
    # creo que tambien se podria tener un solo grupo con capas, pygame.sprite.LayeredUpdates, pero filo
    
    # aqui hay que ver que pasa si hay 1 o 2 jugadores
    personajes.add(Personaje(0,200))
    #personajes.add(Personaje(1,400))    no tengo imagenes de player2 por mientras
    
    # un fondo
    backgroundSurface=pygame.image.load("imagenes/fondo1.png").convert()
    screenSurface.blit(backgroundSurface, (0,0))
    
    # loop principal
    while True:
        movimientoPersonajes=[-1,-1]

        # --- TECLAS
        for event in pygame.event.get():
            if event.type==QUIT:
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
                        
            elif event.type==KEYUP:
                if event.key==K_LEFT or event.key==K_RIGHT:
                    movimientoPersonajes[0]=PARADO
                elif event.key==K_a or event.key==K_d:
                    movimientoPersonajes[1]=PARADO
        
        # --- EJECUTAR
        # orden: personajes, balas, engranajes, power_ups
        personajes.update(movimientoPersonajes)
        #balas.update()
        #engranajes.update()
        #power_ups.update()
        
        # --- LIMPIAR
        personajes.clear(screenSurface, backgroundSurface)
        engranajes.clear(screenSurface, backgroundSurface)
        balas     .clear(screenSurface, backgroundSurface)
        power_ups .clear(screenSurface, backgroundSurface)
        
        # --- DIBUJAR
        # orden: (atras para adelante)
        # balas, power_ups, personajes, engranajes
        balas     .draw(screenSurface)
        power_ups .draw(screenSurface)
        personajes.draw(screenSurface)
        engranajes.draw(screenSurface)
        
        
        pygame.display.update()
        fpsClock.tick(60)

main()
