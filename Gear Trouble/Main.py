# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import os
import sys
import random
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
from PowerUp import *

def main():
    pygame.init()
    fpsClock=pygame.time.Clock()
    
    fullscreen_flag=0
    if FULLSCREEN:
        fullscreen_flag=pygame.FULLSCREEN;
    else:
        os.environ['SDL_VIDEO_WINDOW_POS']="400,100"
    screenSurface=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],fullscreen_flag)
    pygame.display.set_caption("Gear Trouble")
    pygame.mouse.set_visible(False)
    
    # inicio
    intro=pygame.movie.Movie("intro.mpg")
    intro.set_display(screenSurface, Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
    intro.play()
    while intro.get_busy():
        for event in pygame.event.get():
            if event.type==KEYDOWN:     # skip
                intro.stop()
                break
        pygame.display.update()
        fpsClock.tick(60)
    
    
    # musica y sonidos
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.music.load('Sonidos/musica.ogg')
    pygame.mixer.music.set_volume(0.5)
    Globals._sonidos["bala"] = pygame.mixer.Sound('Sonidos/Disparo.ogg')
    Globals._sonidos["bala"].set_volume(0.5)
    Globals._sonidos["romper"] = pygame.mixer.Sound('Sonidos/romper.ogg')
    Globals._sonidos["romper"].set_volume(0.5)
    Globals._sonidos["combo"] = pygame.mixer.Sound('Sonidos/combo.ogg')
    Globals._sonidos["ganar"] = pygame.mixer.Sound('Sonidos/ganar.ogg')
    Globals._sonidos["perder"] = pygame.mixer.Sound('Sonidos/perder.ogg')
    Globals._sonidos["fugaz"] = pygame.mixer.Sound('Sonidos/fugaz.ogg')
    
    cargarSurfaces()
    
    dosJugadores=False #TODO
    
    nEtapaActual=1
    
    vidas=[]
    vidas.append(VIDAS_INIT)
    if (dosJugadores):
        vidas.append(VIDAS_INIT)
    else:
        vidas.append(0)
    for player in range(2):     # resetear lo dibujado sobre statuBar
        for i in range(MAX_VIDAS_DRAW):
            if vidas[player]>i:
                delete=0
            else:
                delete=1
            drawHeart(None,player,i,delete)
    
    Globals._puntuacion=[0,0]
        
    screenSurface.blit(Globals.SURFACE_STATUSBAR, (0,ALTURA_PISO))
    getReadySurface=pygame.image.load("imagenes/getReady.png")
    getReadyRect=getReadySurface.get_rect()
    rectPosGetReady = Rect((SCREEN_WIDTH-getReadyRect.width)/2, (ALTURA_PISO-getReadyRect.height)/2, getReadyRect.width, getReadyRect.height)
        
    while True:     # nueva etapa: aqui va lo que no cambia
        etapaActual=ETAPAS[nEtapaActual]

        # fondo
        backgroundSurface=pygame.Surface((SCREEN_WIDTH,ALTURA_PISO))
        backgroundSurface.blit(pygame.image.load("imagenes/fondo"+str(etapaActual["fondo"])+".png"), (ANCHO_PAREDES_BORDES,0))
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
        
        while True:     # nueva vida: aqui reiniciar todo lo que pueda haber cambiado        
            pygame.mixer.music.play(-1)
             
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
            
            tiempo=etapaActual["tiempo"]+1/60.0
            if tiempo<ANCHO_BARRA_TIEMPO/60.0:
                raise Exception("Tiempo demasiado corto")   # la barra se achicaria a mas de 1px/seg
            Globals.SURFACE_STATUSBAR.blit(Globals.SURFACE_BARRA_TIEMPO, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO))
            screenSurface            .blit(Globals.SURFACE_BARRA_TIEMPO, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO + ALTURA_PISO))
            
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
            
            # variables
            movimientoPersonajes=[[False,False],[False,False]]  # [p1/p2][izq/der]
            presionaDisparo=[False,False]
            tiempoSinDisparo=[0,0]
            balaActiva=[False,False]
            powerupsSpawn=[]
            
            # dibujar todo...
            screenSurface.blit(backgroundSurface,(0,0))
            personajes.update([PARADO,PARADO])
            balas     .draw(screenSurface)
            personajes.draw(screenSurface)
            power_ups .draw(screenSurface)
            engranajes.draw(screenSurface)
            puertas   .draw(screenSurface)
            paredes   .draw(screenSurface)
            efectos   .draw(screenSurface)
            # ...y dibujar el getReady
            screenSurface.blit(getReadySurface, rectPosGetReady)
            pygame.display.update() # mostrar
            pygame.time.wait(1000)
            screenSurface.blit(backgroundSurface, rectPosGetReady, rectPosGetReady)  # restaurar


            gana=None
            while gana==None:     # loop principal de mientras se juega
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
                # tiempo
                tiempo-=1/60.0
                if tiempo<0:
                    gana=False
                    nPerdedores=[]
                    for personaje in referenciaPersonajes:
                        nPerdedores.append(personaje.num)
                    break
                x = X_BARRA_TIEMPO+ANCHO_BARRA_TIEMPO*tiempo/etapaActual["tiempo"]
                Globals.SURFACE_STATUSBAR.blit(Globals.SURFACE_1px_BARRA_T, (x,Y_BARRA_TIEMPO))
                screenSurface            .blit(Globals.SURFACE_1px_BARRA_T, (x,Y_BARRA_TIEMPO + ALTURA_PISO))
                
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
                powerupsSacar=[]
                power_ups.update(powerupsSacar)
                power_ups.remove(powerupsSacar)
                
                # efectos
                efectos.add(Globals._efectosAgregar)
                Globals._efectosSacar=[]
                efectos.update()
                
                # colisiones: power-up contra personaje
                for personaje in referenciaPersonajes:
                    for pu in power_ups:
                        if PPCollision(pu,personaje):
                            power_ups.remove(pu)
                            # SWITCH (PU.TIPO) {    !!!!!!!!!!!!!!!!!!!!
                            if 10 <= pu.tipo < 20:
                                personaje.tipoBala=pu.tipo
                                
                            elif pu.tipo==SILVER_COIN:
                                Globals._puntuacion[personaje.num]+=PUNTAJE_SILVER
                                
                            elif pu.tipo==GOLD_COIN:
                                Globals._puntuacion[personaje.num]+=PUNTAJE_GOLD
                            
                            elif pu.tipo==VIDA_EXTRA:
                                drawHeart(screenSurface, personaje.num, vidas[personaje.num], 0)
                                vidas[personaje.num]+=1
                            
                            elif pu.tipo==TIEMPO_EXTRA:
                                tiempo+=SEGUNDOS_TIEMPO_EXTRA
                                if tiempo>etapaActual["tiempo"]:
                                    tiempo=etapaActual["tiempo"]+1/60.0
                                rect=Rect(0, 0, ANCHO_BARRA_TIEMPO*tiempo/etapaActual["tiempo"], ALTO_BARRA_TIEMPO)
                                Globals.SURFACE_STATUSBAR.blit(Globals.SURFACE_BARRA_TIEMPO, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO), rect)
                                screenSurface            .blit(Globals.SURFACE_BARRA_TIEMPO, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO + ALTURA_PISO), rect)
                            
                            #elif pu.tipo==...:
                                
                # colisiones: bala contra engranaje
                engranajesAgregar=[]
                for bala in balas.sprites():
                    for engranaje in engranajes.sprites():
                        if PPCollision(bala,engranaje):
                            bala.sacar()
                            engranajesAgregar.extend( engranaje.sacar(True, bala.num, bala.tipo==BALA_FUGAZ) )
                            efectos.add(Efecto(engranaje.x, engranaje.y, Globals.SURFACE_POP[engranaje.size], Globals.FRAMES_POR_IMAGEN_POP))
                            Globals._sonidos["romper"].play()
                            if engranaje.size>1:
                                generarPowerUp(engranaje.x,engranaje.y,power_ups,powerupsSpawn)
                            break
                    else:           # http://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
                        continue    # executed if the loop ended normally (no break)
                    break           # executed if 'continue' was skipped (break)
                
                # sacar balas y engranajes
                for bala in Globals._balasSacar:
                    balas.remove(bala)
                    balaActiva[bala.num]=False
                    
                engranajes.remove(Globals._engranajesSacar)
                
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
                # orden: de atras para adelante
                balas     .draw(screenSurface)
                personajes.draw(screenSurface)
                engranajes.draw(screenSurface)
                power_ups .draw(screenSurface)
                puertas   .draw(screenSurface)
                paredes   .draw(screenSurface)
                efectos   .draw(screenSurface)
                
                for bala in balas.sprites():    # desdibujar balas sobre barra de estado
                    screenSurface.blit(Globals.SURFACE_STATUSBAR, (bala.rect.left,ALTURA_PISO), Rect(bala.rect.left,0,3,STATUS_BAR_H))
                
                if len(engranajes.sprites())==0:  # no quedan engranajes
                    gana=True
                
                efectos.remove(Globals._efectosSacar)
                
                # colisiones: engranaje contra personaje (revisar ahora que ya esta dibujado el choque)
                for personaje in referenciaPersonajes:
                    for engranaje in engranajes.sprites():
                        if PPCollision(personaje,engranaje):
                            gana=False
                            nPerdedores=[personaje.num]
                            break   # la variable "personaje" queda
                    else:               # http://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
                        continue        # executed if the loop ended normally (no break)
                    break               # executed if 'continue' was skipped (break)
                
                pygame.display.update()
                fpsClock.tick(60)
            
            
            # --------------------------------------------------------------------------
            # fuera del loop principal, perdió o ganó
            pygame.mixer.music.stop()
            if gana:
                
                #myfont = pygame.font.SysFont("Verdana", 64)
                #label = myfont.render("Ganaste!", 1, (0,0,0))
                #screenSurface.blit(label, ((SCREEN_WIDTH-label.get_width())/2, (ALTURA_PISO-label.get_height())/2))
                
                channel=Globals._sonidos["ganar"].play()
                
                while channel.get_busy():
                    Globals._efectosSacar=[]
                    efectos.update()
                    efectos.clear(screenSurface, backgroundSurface)
                    efectos.draw(screenSurface)
                    efectos.remove(Globals._efectosSacar)
                    
                    if tiempo>0:    
                        tiempo-=1# TODO
                        #puntuacion...
                    
                    pygame.display.update()
                    fpsClock.tick(60)
                    
                nEtapaActual+=1
                if nEtapaActual==len(ETAPAS):
                    #####cambiar
                    pygame.quit()
                    sys.exit(0)
                break   # pasar al loop de nueva etapa
                    
            else: # pierde
                Globals._sonidos["perder"].play()
                for np in nPerdedores:
                    vidas[np]-=1
                
                if len(nPerdedores)==1:     # uno choca contra engranaje
                    screenSurface.blit(Globals.SURFACE_CUBRE_MUERTE, (personaje.rect.centerx-SCREEN_WIDTH, 0))
                    screenSurface.blit(paredBordeSurface, (0,0))
                    screenSurface.blit(paredBordeSurface, (SCREEN_WIDTH-ANCHO_PAREDES_BORDES,0))
                    screenSurface.blit(techoSurface, (0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)
                else:       # pierden por tiempo
                    screenSurface.blit(Globals.SURFACE_CUBRE_TODO, (ANCHO_PAREDES_BORDES,0))
                    screenSurface.blit(techoSurface, (0,0))
                    for i in range(2):
                        screenSurface.blit(Globals.SURFACE_BARRA_TIEMPO, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO + ALTURA_PISO))
                        pygame.display.update()
                        pygame.time.wait(500)
                        screenSurface.blit(Globals.SURFACE_BARRA_T_VACIA, (X_BARRA_TIEMPO,Y_BARRA_TIEMPO + ALTURA_PISO))
                        pygame.display.update()
                        pygame.time.wait(500)

                vidasRestantes=0
                for v in vidas:
                    vidasRestantes+=v
                if vidasRestantes==0:
                    #####cambiar
                    pygame.quit()
                    sys.exit(0)
                else:
                    for np in nPerdedores:
                        drawHeart(screenSurface,np,vidas[np],1)


def generarPowerUp(x,y,power_ups,powerupsSpawn):
    if random.random()<PROBA_GET_PU:
        r=random.uniform(0,PROBAS_SUMADAS[-1])
        for i in range(len(PROBAS_SUMADAS)):
            if r<PROBAS_SUMADAS[i]:
                index=i
                break
        tipo=POWERUPS[index][0]
        powerupsSpawn.append(tipo)
        power_ups.add(PowerUp(x,y,tipo))
    else:
        powerupsSpawn.append(0)
        
def drawHeart(screenSurface,player,n,delete):
    if n>=MAX_VIDAS_DRAW:
        return
    
    Y=48
    if player==0:
        x=13+32*n
    else:
        x=775-32*n
    Globals.SURFACE_STATUSBAR.blit(Globals.SURFACE_HEARTS[delete],(x,Y))
    if screenSurface:
        #screenSurface.blit(Globals.SURFACE_STATUSBAR, (rect.left,rect.top+ALTURA_PISO), rect)
        screenSurface.blit(Globals.SURFACE_HEARTS[delete], (x,Y+ALTURA_PISO))
        
def cargarSurfaces():
    # engranajes
    Globals.SURFACE_ENGRANAJES=[[None for __i in range(MAX_SIZE_ENGRANAJES+1)] for __i in range(N_COLORES_ENGRANAJES)]
    for color in range(N_COLORES_ENGRANAJES):
        surfaceOriginal=pygame.image.load("imagenes/engranaje"+str(color)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        for size in range(1,MAX_SIZE_ENGRANAJES+1):
            diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro * SIZE_ENGRANAJES )
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
    
    # bala fugaz
    Globals.SURFACE_BALAS_FUGAZ=[]
    surfaceOriginal=pygame.image.load("imagenes/balaFugaz.png").convert_alpha()
    ancho=surfaceOriginal.get_width()
    alto =surfaceOriginal.get_height()
    
    framesTotal=0
    y=ALTURA_PISO-ALTURA_SALIDA_BALA
    vy=VELOC_INI_BALA_FUGAZ
    while y>=ALTURA_TECHO:
        vy+=ACEL_SUBIDA_BALA_FUGAZ
        y-=vy
        framesTotal+=1

    for i in range(0,framesTotal):
        height=int(ALTURA_INI_BALA_FUGAZ+float(i)*alto/framesTotal)
        surface=pygame.transform.smoothscale(surfaceOriginal, (ancho,height))
        Globals.SURFACE_BALAS_FUGAZ.append((surface, surface.get_rect(), PixelPerfectCollision.get_alpha_hitmask(surface)))
    
    # pop
    Globals.SURFACE_POP=[[None for __i in range(IMAGENES_POP)] for __i in range(MAX_SIZE_ENGRANAJES+1)]
    for i in range(0,IMAGENES_POP):
        surfaceOriginal=pygame.image.load("imagenes/pop"+str(i+1)+".png").convert_alpha()
        diametro=surfaceOriginal.get_width()
        for size in range(1,MAX_SIZE_ENGRANAJES+1):
            if size>1:
                diametro2=int( pow(size,FACTOR_DIAMETRO_SIZE) * diametro * SIZE_ENGRANAJES )
            else:
                diametro2=15
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
    Globals.SURFACE_PARED_NORMAL    = pygame.image.load("imagenes/paredNormal.png").convert()
    Globals.SURFACE_PARED_ENGRANAJE = pygame.image.load("imagenes/paredEngranajes.png").convert()
    Globals.SURFACE_PARED_PUERTA    = pygame.image.load("imagenes/paredPuerta.png").convert_alpha()
    
    # power-ups
    Globals.SURFACE_POWERUPS=dict()
    for pu in POWERUPS:
        surf = pygame.image.load("imagenes/"+pu[2]+".png").convert_alpha()
        Globals.SURFACE_POWERUPS[pu[0]] = []
        Globals.SURFACE_POWERUPS[pu[0]].append(surf)
        
        # imagen semitransparente
        transp=pygame.PixelArray(surf.copy())
        for x in range(0,surf.get_width()):
            for y in range(0,surf.get_height()):
                color=surf.unmap_rgb(transp[x,y])
                color.a=int(color.a/1.5)
                transp[x,y]=color
        Globals.SURFACE_POWERUPS[pu[0]].append(transp.make_surface())
        
        Globals.SURFACE_POWERUPS[pu[0]].append(PixelPerfectCollision.get_alpha_hitmask(surf))   # hitmask
    
    # status bar
    Globals.SURFACE_STATUSBAR=pygame.image.load("imagenes/statusBar.png").convert()
    
    # heart
    Globals.SURFACE_HEARTS=[]
    Globals.SURFACE_HEARTS.append(pygame.image.load("imagenes/heart.png").convert())
    Globals.SURFACE_HEARTS.append(pygame.image.load("imagenes/blankHeart.PNG").convert())
    
    # cubre todo
    Globals.SURFACE_CUBRE_TODO=pygame.Surface((SCREEN_WIDTH-2*ANCHO_PAREDES_BORDES,ALTURA_PISO))
    Globals.SURFACE_CUBRE_TODO.fill(Color(0,0,0))
    Globals.SURFACE_CUBRE_TODO.set_alpha(ALPHA_CUBRE_NEGRO)
    
    # barra tiempo
    Globals.SURFACE_BARRA_TIEMPO  = pygame.Surface((ANCHO_BARRA_TIEMPO,ALTO_BARRA_TIEMPO))
    Globals.SURFACE_BARRA_TIEMPO .fill(Color(215,0,0))
    Globals.SURFACE_BARRA_T_VACIA = pygame.Surface((ANCHO_BARRA_TIEMPO,ALTO_BARRA_TIEMPO))
    Globals.SURFACE_BARRA_T_VACIA.fill(Color(255,255,255))
    Globals.SURFACE_1px_BARRA_T=pygame.Surface((1,ALTO_BARRA_TIEMPO))
    Globals.SURFACE_1px_BARRA_T.fill(Color(255,255,255))
    

# no-launcher:
#main()

# launcher:
class NuestroJuego():
    def Go(self,services):
        main()

