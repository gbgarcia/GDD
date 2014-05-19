# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import os
import sys
import pygame
from pygame.locals import *

from Globals import *
import Globals
from Etapas import ETAPAS
import PixelPerfectCollision
from PixelPerfectCollision import PPCollision

from Personaje import Personaje
from Engranaje import Engranaje
from Bala import Bala
from Efecto import Efecto
from Pared import Pared

def main():
    pygame.init()
    fpsClock=pygame.time.Clock()
    
    global screenSurface
    fullscreen_flag=0
    if FULLSCREEN:
        fullscreen_flag=pygame.FULLSCREEN;
    else:
        os.environ['SDL_VIDEO_WINDOW_POS']="550,100"
    screenSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
    pygame.display.set_caption("Gear Trouble")
    
    cargarSurfaces()
    
    dosJugadores=False #TODO
    
    nEtapaActual=1
    vidas=[]
    vidas.append(VIDAS_INIT)
    if (dosJugadores):
        vidas.append(VIDAS_INIT)
    else:
        vidas.append(0)
        
    while True:     # nueva etapa: aqui va lo que no cambia
        etapaActual=ETAPAS[nEtapaActual]
        
        # fondo
        backgroundSurface=pygame.Surface((SCREEN_WIDTH,ALTURA_PISO))
        backgroundSurface.blit(pygame.image.load("imagenes/fondo"+str(nEtapaActual)+".png"), (ANCHO_PAREDES_BORDES,0))
        paredBordeSurface=pygame.image.load("imagenes/paredBorde.png")
        backgroundSurface.blit(paredBordeSurface, (0,0))
        backgroundSurface.blit(paredBordeSurface, (SCREEN_WIDTH-ANCHO_PAREDES_BORDES,0))
        techoSurface=pygame.image.load("imagenes/techo.png")
        backgroundSurface.blit(techoSurface, (0,0))
        
        if "paredes" in etapaActual:
            backPuertaSurface=pygame.image.load("imagenes/backPuerta.png")
            for pared in etapaActual["paredes"]:
                if pared[0]==PARED_ENGRANAJES:
                    backgroundSurface.blit(backPuertaSurface, (pared[1],ALTURA_PUERTA))
        
        screenSurface.blit(backgroundSurface,(0,0))
        
        statusBarSurface=pygame.image.load("imagenes/statusBar.png").convert()
        
        while True:     # nueva vida: aqui reiniciar todo lo que pueda haber cambiado
            personajes = pygame.sprite.Group()
            engranajes = pygame.sprite.Group()
            balas      = pygame.sprite.Group()
            power_ups  = pygame.sprite.Group()
            efectos    = pygame.sprite.Group()
            paredes    = pygame.sprite.Group()
            puertas    = pygame.sprite.Group()
            
            referenciaPersonajes=[]
            for i in range(2):
                if (vidas[i]>0):
                    referenciaPersonajes.append(Personaje(i, etapaActual["xIniPlayer"+str(i+1)] ))
                    personajes.add(referenciaPersonajes)
            
            # buscar el maximo...
            maxId=0
            for eng in etapaActual["engranajes"]:
                if eng[6]>maxId:
                        maxId=eng[6]
            Globals._idsEngranajes=[0 for __i in range(maxId+1)]    # ...crear el arreglo...
            # ...y crear los engranajes
            for eng in etapaActual["engranajes"]:
                engranajes.add(Engranaje.fromArray(eng))
            
            # paredes que limitan el movimiento en horizontal
            # _paredes bloquea personajes y engranajes, _paredesEngranajes solo a engranajes
            # deben ir en vertical de 0 a SCREEN_HEIGHT
            Globals._paredes=[]
            Globals._paredesEngranajes=[]
            if "paredes" in etapaActual:
                for pared in etapaActual["paredes"]:
                    tipoPared=pared[0]
                    xPared=pared[1]
                    idPared=pared[2]
                    
                    if tipoPared==PARED_ENGRANAJES:
                        Globals._paredesEngranajes.append(Rect(xPared,0,ANCHO_PARED,SCREEN_HEIGHT))
                    else:   # paredes normales y puertas
                        Globals._paredes.append(Rect(xPared,0,ANCHO_PARED,SCREEN_HEIGHT))
                    
                    ref=Pared(tipoPared,xPared,idPared)
                    if tipoPared==PARED_PUERTA:
                        puertas.add(ref)
                    else:
                        paredes.add(ref)
                    
            Globals._paredes.append(Rect(0,0,ANCHO_PAREDES_BORDES,SCREEN_HEIGHT))
            Globals._paredes.append(Rect(SCREEN_WIDTH-ANCHO_PAREDES_BORDES,0,ANCHO_PAREDES_BORDES,SCREEN_HEIGHT))
                    
            movimientoPersonajes=[[False,False],[False,False]]  # [p1/p2][izq/der]
            presionaDisparo=[False,False]
            tiempoSinDisparo=[0,0]
            balaActiva=[False,False]
            
            while True:     # loop principal de mientras se juega
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
                        
                        elif event.key==K_p:    # pausa
                            salir=False
                            while not salir:
                                fpsClock.tick(60)
                                for event2 in pygame.event.get():
                                    if event2.type==KEYUP and event2.key==K_p:      # esperar a que se suelte P
                                        salir=True
                            salir=False
                            while not salir:
                                fpsClock.tick(60)
                                for event2 in pygame.event.get():
                                    if event2.type==KEYDOWN and event2.key==K_p:    # esperar a que se aprete P
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
                # paredes
                idLevantar=-1
                for id_ in range(1,len(Globals._idsEngranajes)):
                    if Globals._idsEngranajes[id_]==0:
                        idLevantar=id_
                        Globals._idsEngranajes[id_]-=1   # queda en -1 y no se revisa mas
                        break
                        
                paredesSacar=[]
                paredes.update(paredesSacar,idLevantar)
                puertas.update(paredesSacar,idLevantar)
                for pared in paredesSacar:
                    if pared.tipo==PARED_PUERTA:
                        puertas.remove(pared)
                    else:
                        paredes.remove(pared)
                    
                # personajes
                direccionPersonajes=[PARADO,PARADO]
                for player in range(2):
                    if   movimientoPersonajes[player][0] and not movimientoPersonajes[player][1]:
                        direccionPersonajes[player]=IZQUIERDA
                    elif movimientoPersonajes[player][1] and not movimientoPersonajes[player][0]:
                        direccionPersonajes[player]=DERECHA
                personajes.update(direccionPersonajes)
                
                # balas
                for i in range(2):
                    if tiempoSinDisparo[i]>0:
                        tiempoSinDisparo[i]-=1
                        
                Globals._balasSacar=[]
                for player in range(2):
                    if presionaDisparo[player] and not balaActiva[player] and tiempoSinDisparo[player]==0:
                        balaActiva[player]=True
                        tiempoSinDisparo[player]=FRAMES_SIN_DISPARO;
                        balas.add(Bala(referenciaPersonajes[player]))
                balas.update()
                
                # engranajes
                Globals._engranajesSacar=[]
                Globals._efectosAgregar=[]
                engranajes.update()
                
                # power_ups
                #power_ups.update()
                
                # efectos
                efectos.add(Globals._efectosAgregar)
                Globals._efectosSacar=[]
                efectos.update()
                
                # colisiones: bala contra engranaje
                engranajesAgregar=[]
                for bala in balas.sprites():
                    for engranaje in engranajes.sprites():
                        if PPCollision(bala,engranaje):
                            bala.sacar()
                            engranajesAgregar.extend(engranaje.sacar(True))
                            efectos.add(Efecto(engranaje.x, engranaje.y, Globals.SURFACE_POP[engranaje.size], Globals.FRAMES_POR_IMAGEN_POP))
                            break
                    else:           # http://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
                        continue    # executed if the loop ended normally (no break)
                    break           # executed if 'continue' was skipped (break)
                
                # sacar balas y engranajes
                for bala in Globals._balasSacar:
                    balas.remove(bala)
                    balaActiva[bala.num]=False
                    
                for engranaje in Globals._engranajesSacar:
                    engranajes.remove(engranaje)
                    
                if len(engranajes.sprites())==0 and len(engranajesAgregar)==0:
                    # no quedan engranajes
                    #####cambiar
                    print("Ganaste!")
                    pygame.quit()
                    sys.exit(0)
                
                # --- LIMPIAR
                personajes.clear(screenSurface, backgroundSurface)
                engranajes.clear(screenSurface, backgroundSurface)
                balas     .clear(screenSurface, backgroundSurface)
                power_ups .clear(screenSurface, backgroundSurface)
                efectos   .clear(screenSurface, backgroundSurface)
                paredes   .clear(screenSurface, backgroundSurface)
                puertas   .clear(screenSurface, backgroundSurface)
                
                engranajes.add(engranajesAgregar)
                
                # --- DIBUJAR
                # orden: (atras para adelante)
                # balas, personajes, power_ups, engranajes, puertas, paredes, efectos
                balas     .draw(screenSurface)
                personajes.draw(screenSurface)
                power_ups .draw(screenSurface)
                engranajes.draw(screenSurface)
                puertas   .draw(screenSurface)
                paredes   .draw(screenSurface)
                efectos   .draw(screenSurface)
                # barra de estado
                screenSurface.blit(statusBarSurface, (0,ALTURA_PISO))
                
                # sacar efectos
                for efecto in Globals._efectosSacar:
                    efectos.remove(efecto)
                
                # colisiones: engranaje contra personaje (revisar ahora que ya esta dibujado el choque)
                for personaje in referenciaPersonajes:
                    for engranaje in engranajes.sprites():
                        if PPCollision(personaje,engranaje):
                            screenSurface.blit(Globals.SURFACE_CUBRE_MUERTE,
                                               (referenciaPersonajes[personaje.num].rect.centerx-SCREEN_WIDTH,
                                                0))
                            screenSurface.blit(paredBordeSurface, (0,0))
                            screenSurface.blit(paredBordeSurface, (SCREEN_WIDTH-ANCHO_PAREDES_BORDES,0))
                            screenSurface.blit(techoSurface, (0,0))
                            
                            #####cambiar
                            print("Perdiste")
                            pygame.display.update()
                            pygame.time.wait(500)
                            pygame.quit()
                            sys.exit(0)
                
                pygame.display.update()
                fpsClock.tick(60)
        
def cargarSurfaces():
    # engranajes
    Globals.SURFACE_ENGRANAJES=[[None for __i in range(SIZE_ENGRANAJES+1)] for __i in range(N_COLORES_ENGRANAJES)]
    for color in range(N_COLORES_ENGRANAJES):
        surfaceOriginal=pygame.image.load("imagenes/engranaje"+str(color)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        for size in range(1,MAX_SIZE_ENGRANAJES+1):
            diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro / SIZE_ENGRANAJES )
            surface=pygame.transform.smoothscale(surfaceOriginal, (diametro2,diametro2))
            Globals.SURFACE_ENGRANAJES[color][size] = (surface, PixelPerfectCollision.get_alpha_hitmask(surface))
    
    # balas normales
    Globals.SURFACE_BALAS_NORMALES=[]
    Globals.SURFACE_BALAS_GANCHO  =[]
    for player in range(2):
        Globals.SURFACE_BALAS_NORMALES.append(pygame.Surface((ANCHO_BALA_NORMAL,SCREEN_HEIGHT)))
        Globals.SURFACE_BALAS_GANCHO  .append(pygame.Surface((ANCHO_BALA_NORMAL,SCREEN_HEIGHT)))
        Globals.SURFACE_BALAS_NORMALES[player].fill(COLORES_BALAS_NORMALES[player])
        Globals.SURFACE_BALAS_GANCHO  [player].fill(COLORES_BALAS_GANCHO  [player])
    Globals.RH_BALAS_NORMALES = (pygame.Rect(0,0,ANCHO_BALA_NORMAL,0),
                                 PixelPerfectCollision.get_full_hitmask(pygame.Rect(0,0,ANCHO_BALA_NORMAL,SCREEN_HEIGHT)))
    
    # pop
    Globals.SURFACE_POP=[[None for __i in range(IMAGENES_POP)] for __i in range(SIZE_ENGRANAJES+1)]
    for i in range(0,IMAGENES_POP):
        surfaceOriginal=pygame.image.load("imagenes/pop"+str(i+1)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        for size in range(1,MAX_SIZE_ENGRANAJES+1):
            if size>1:
                diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro / SIZE_ENGRANAJES )
            else:
                diametro2=12
            surface=pygame.transform.smoothscale(surfaceOriginal, (diametro2,diametro2))
            Globals.SURFACE_POP[size][i] = surface
    
    # cubre muerte     
    Globals.SURFACE_CUBRE_MUERTE=pygame.image.load("imagenes/cubreMuerte.png").convert_alpha()
    
    # combo
    Globals.SURFACE_COMBO=[]
    surfaceOriginal=pygame.image.load("imagenes/combo.png").convert_alpha()
    anchoOrig=surfaceOriginal.get_width ()
    altoOrig =surfaceOriginal.get_height()
    for i in range(1,FRAMES_COMBO):
        factor=pow(i/float(FRAMES_COMBO),0.5)
        Globals.SURFACE_COMBO.append(pygame.transform.smoothscale(surfaceOriginal, (int(anchoOrig*factor), int(altoOrig*factor))))
    for i in range(FRAMES_COMBO-2,-1,-1):
        Globals.SURFACE_COMBO.append(Globals.SURFACE_COMBO[i])
    
    # paredes
    Globals.SURFACE_PARED_NORMAL    = pygame.image.load("imagenes/paredNormal.png")
    Globals.SURFACE_PARED_ENGRANAJE = pygame.image.load("imagenes/paredEngranajes.png")
    Globals.SURFACE_PARED_PUERTA    = pygame.image.load("imagenes/paredPuerta.png")
    
main()
