# -*- coding: utf-8 -*-
# (si no, no puedo escribir �)

import pygame

from Globals import *
import Globals

# Power-ups
# 10-19: balas (ya definidas en Globals)
SILVER_COIN     = 20
GOLD_COIN       = 21
ESCUDO          = 30
VIDA_EXTRA      = 31
TIEMPO_EXTRA    = 32

PROBA_GET_PU    = 0.45

POWERUPS = [    # [ <id> , <probabilidad entre 0 y 1> , <nombre imagen (sin .png)> ]
    [SILVER_COIN,   0.4,  "silverCoin"],
    [GOLD_COIN,     0.1,  "goldCoin"],
    
    [BALA_NORMAL,   0.4,  "puBNorm"],
    [BALA_GANCHO,   0.4,  "puGancho"],
    [BALA_FUGAZ,    0.2,  "puFugaz"],
    #[BALA_TORRE,    0.1, "puTorre"],
    
    #[ESCUDO,        0.2, "puShield"],
    [VIDA_EXTRA,    0.05, "extraLife"],
    [TIEMPO_EXTRA,  0.2,  "extraTime"]
]

PROBAS_SUMADAS = [0 for __i in range(len(POWERUPS))]
for i in range(len(POWERUPS)):
    PROBAS_SUMADAS[i] = PROBAS_SUMADAS[i-1] + POWERUPS[i][1]      # i==-1 igual me da un 0



class PowerUp(pygame.sprite.Sprite):
    
    def __init__(self, x, y, tipo):
        """ Un power-up que cae al dividir un engranaje
        x,y: coordenadas donde aparece """
        
        pygame.sprite.Sprite.__init__(self)
        
        self.tipo=tipo
        self.image=Globals.SURFACE_POWERUPS[tipo][0]
        self.hitmask=Globals.SURFACE_POWERUPS[tipo][2]
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.y=y
        self.rect.centery=y
        self.framesEnPiso=-1
        self.transparente=False
        
    def update(self, powerupsSacar):
        if self.framesEnPiso==-1:   # cayendo
            self.y+=VELOC_CAIDA_POWERUP
            self.rect.centery=self.y
            if self.rect.bottom>=ALTURA_PISO:
                self.rect.bottom=ALTURA_PISO
                self.framesEnPiso=0
        else:                       # en piso
            self.framesEnPiso+=1
            if not self.transparente:
                if self.framesEnPiso>POWERUP_FRAMES_PISO:
                    self.transparente=True
                    self.image=Globals.SURFACE_POWERUPS[self.tipo][1]
            elif self.framesEnPiso>POWERUP_FRAMES_TRANSP:
                powerupsSacar.append(self)
                