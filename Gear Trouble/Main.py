# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import sys
import pygame
from pygame.locals import *

from Globals import *
import Globals
import PixelPerfectCollision
from PixelPerfectCollision import PPCollision

from Personaje import Personaje
from Engranaje import Engranaje
from Bala import Bala


def main():
    pygame.init()
    fpsClock=pygame.time.Clock()
    
    global screenSurface
    fullscreen_flag=0
    if FULLSCREEN:
        fullscreen_flag=pygame.FULLSCREEN;
    screenSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
    pygame.display.set_caption("Gear Trouble")
    
    cargarSurfacesEngranajes()
    
    Globals.SURFACE_BALAS_NORMALES=[]
    for player in range(2):
        Globals.SURFACE_BALAS_NORMALES.append(pygame.Surface((ANCHO_BALA_NORMAL,SCREEN_HEIGHT)))
        Globals.SURFACE_BALAS_NORMALES[player].fill(COLORES_BALAS[player])
    Globals.RH_BALAS_NORMALES = (pygame.Rect(0,0,ANCHO_BALA_NORMAL,0),
                                 PixelPerfectCollision.get_full_hitmask(pygame.Rect(0,0,ANCHO_BALA_NORMAL,SCREEN_HEIGHT)))
    
    
    personajes = pygame.sprite.Group()
    engranajes = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    # creo que tambien se podria tener un solo grupo con capas, pygame.sprite.LayeredUpdates, pero filo
    
    # aqui hay que ver que pasa si hay 1 o 2 jugadores
    ETAPA_ACTUAL = 1
    VIDAS_INIT = 5
    #me late esto va en Golbals(despues lo cambio)
    while True:
        referenciaPersonajes=[]
        referenciaPersonajes.append(Personaje(0,200))
        #referenciaPersonajes.append(Personaje(1,400)) no tengo imagenes de player2 por mientras
        personajes.add(referenciaPersonajes)
        if ETAPA_ACTUAL == 1 :
            
            engranajes.add(Engranaje(100,200, 1, PARADO, 0, 0))
            engranajes.add(Engranaje(250,200, 2, PARADO, 0, 0))
            engranajes.add(Engranaje(400,200, 3, PARADO, 0, 0))
            engranajes.add(Engranaje(550,200, 4, PARADO, 0, 0))
            engranajes.add(Engranaje(700,200, 5, PARADO, 0, 0))
            engranajes.add(Engranaje(850,200, 6, PARADO, 0, 0))
        elif ETAPA_ACTUAL ==2 :
             engranajes.add(Engranaje(100,200, 3, IZQUIERDA, 0, 0))
             engranajes.add(Engranaje(300,200, 3, IZQUIERDA, 0, 0))
             engranajes.add(Engranaje(500,200, 3, PARADO, 0, 0))
             engranajes.add(Engranaje(700,200, 3, DERECHA, 0, 0))
             engranajes.add(Engranaje(900,200, 3, DERECHA, 0, 0)) 
        elif ETAPA_ACTUAL ==3 :
             engranajes.add(Engranaje(200,200, 6, DERECHA, 0, 0))
             engranajes.add(Engranaje(700,200, 6, IZQUIERDA, 0, 0))
        elif ETAPA_ACTUAL ==4 :
             engranajes.add(Engranaje(50,200, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(150,220, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(250,240, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(350,260, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(450,280, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(550,300, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(650,320, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(750,340, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(850,180, 2, DERECHA, 0, 0))
             engranajes.add(Engranaje(950,160, 2, DERECHA, 0, 0))
        #agregar mas etapas
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
        
        movimientoPersonajes=[[False,False],[False,False]] # [p1/p2][izq/der]
        presionaDisparo=[False,False]
        balaActiva=[False,False]
        
        VariableLoop = True
        # loop principal
        while VariableLoop:
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
                    elif event.key==K_UP or event.key==K_DOWN:
                        presionaDisparo[0]=True
                    elif event.key==K_w or event.key==K_s:
                        presionaDisparo[1]=True
                        
                    elif event.key==K_F12:
                        pass # poner un breakpoint aqui -> F12 es debug
                    
                    elif event.key==K_p: # pausa
                        salir=False
                        while not salir:
                            fpsClock.tick(60)
                            for event2 in pygame.event.get():
                                if event2.type==KEYUP and event2.key==K_p: # esperar a q se suelte P
                                    salir=True
                        salir=False
                        while not salir:
                            fpsClock.tick(60)
                            for event2 in pygame.event.get():
                                if event2.type==KEYDOWN and event2.key==K_p: # esperar a q se aprete P
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
                    elif event.key==K_UP or event.key==K_DOWN:
                        presionaDisparo[0]=False
                    elif event.key==K_w or event.key==K_s:
                        presionaDisparo[1]=False
            
            # --- EJECUTAR
            # personajes
            direccionPersonajes=[PARADO,PARADO]
            for player in range(2):
                if movimientoPersonajes[player][0] and not movimientoPersonajes[player][1]:
                    direccionPersonajes[player]=IZQUIERDA
                elif movimientoPersonajes[player][1] and not movimientoPersonajes[player][0]:
                    direccionPersonajes[player]=DERECHA
            personajes.update(direccionPersonajes)
            
            # balas
            Globals._balasSacar=[]
            for player in range(2):
                if presionaDisparo[player] and not balaActiva[player]:
                    balaActiva[player]=True
                    balas.add(Bala(referenciaPersonajes[player]))
            balas.update()
            
            # engranajes
            Globals._engranajesSacar=[]
            engranajes.update()
            
            # power_ups
            #power_ups.update()
            
            # colisiones: bala contra engranaje
            engranajesAgregar=[]
            for bala in balas.sprites():
                for engranaje in engranajes.sprites():
                    if PPCollision(bala,engranaje):
                        if bala.tipo!=BALA_TORRE:
                            bala.sacar()
                        Globals._engranajesSacar.append(engranaje)
                        engranajesAgregar.extend(engranaje.sacar(True))
            
            # sacar
            for bala in Globals._balasSacar:
                balas.remove(bala)
                balaActiva[bala.num]=False
            for engranaje in Globals._engranajesSacar:
                engranajes.remove(engranaje)
            if len(engranajes.sprites())==0 and len(engranajesAgregar)==0:
                # no quedan engranajes
                #####cambiar
                if ETAPA_ACTUAL == 4 :
                    print("Ganaste!")
                    pygame.quit()
                    sys.exit(0)
                else :
                    ETAPA_ACTUAL += 1
                    VariableLoop = False
                    personajes.empty()
                    engranajes.empty()

            # --- LIMPIAR
            personajes.clear(screenSurface, backgroundSurface)
            engranajes.clear(screenSurface, backgroundSurface)
            balas .clear(screenSurface, backgroundSurface)
            power_ups .clear(screenSurface, backgroundSurface)
            
            engranajes.add(engranajesAgregar)
            
            # --- DIBUJAR
            # orden: (atras para adelante)
            # balas, personajes, power_ups, engranajes
            balas .draw(screenSurface)
            personajes.draw(screenSurface)
            power_ups .draw(screenSurface)
            engranajes.draw(screenSurface)
            # barra de estado
            # ...
            
            # colisiones: engranaje contra personaje (revisar ahora que ya esta dibujado el choque)
            for personaje in referenciaPersonajes:
                for engranaje in engranajes.sprites():
                    if PPCollision(personaje,engranaje):
                        cubreMuerte=pygame.Surface((SCREEN_WIDTH,ALTURA_PISO))
                        cubreMuerte.set_alpha(ALPHA_CUBRE_MUERTE)
                        cubreMuerte.fill((127,127,127))
                        TRANSPARENT=(0,0,0) # (cualquier color)
                        cubreMuerte.set_colorkey(TRANSPARENT)
                        pygame.draw.circle(cubreMuerte, TRANSPARENT,
                                           referenciaPersonajes[personaje.num].rect.center, RADIO_CIRCULO_MUERTE)
                        screenSurface.blit(cubreMuerte, (0,0))
                        
                        VIDAS_INIT -= 1

                        #####cambiar
                        if VIDAS_INIT == 0:
                            print("Perdiste")
                            pygame.display.update()
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit(0)
                        if not VIDAS_INIT == 0:
                             VariableLoop = False
                             personajes.empty()
                             engranajes.empty()
                        
                            
            pygame.display.update()
            fpsClock.tick(60)
        
def cargarSurfacesEngranajes():
    Globals.SURFACE_ENGRANAJES=[[None for __i in range(SIZE_ENGRANAJES+1)] for __i in range(N_COLORES_ENGRANAJES)]
    for color in range(N_COLORES_ENGRANAJES):
        surfaceOriginal=pygame.image.load("imagenes/engranaje"+str(color)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        for size in range(1,MAX_SIZE_ENGRANAJES+1):
            diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro / SIZE_ENGRANAJES )
            surface=pygame.transform.smoothscale(surfaceOriginal, (diametro2,diametro2))
            Globals.SURFACE_ENGRANAJES[color][size] = (surface, PixelPerfectCollision.get_alpha_hitmask(surface))

main()