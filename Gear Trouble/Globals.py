# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

# Constantes (en Mayusculas)

SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 600
FULLSCREEN      = True
FULLSCREEN      = False
STATUS_BAR_H    = 140
ALTURA_PISO     = SCREEN_HEIGHT-STATUS_BAR_H
ALTURA_TECHO    = 14
ANCHO_PAREDES_BORDES    = 5
ANCHO_PARED     = 30
ALTURA_PUERTA   = 410
MAX_VIDAS_DRAW  = 6

IMGS_ANIMACION_PERS     = 4
FRAMES_POR_IMAGEN_PERS  = 8
IMAGENES_POP            = 3
FRAMES_POR_IMAGEN_POP   = 2
FRAMES_COMBO            = 12
Y_COMBO = ALTURA_TECHO + 35/4

VIDAS_INIT      = 5

IZQUIERDA   = -1
DERECHA     = 1
PARADO      = 0

PARED_NORMAL        = 0
PARED_ENGRANAJES    = 1
PARED_PUERTA        = 2

BALA_NORMAL     = 10
BALA_GANCHO     = 11
BALA_FUGAZ      = 12
BALA_TORRE      = 13

VELOC_MOV_PERSONAJES    = SCREEN_WIDTH/60/5.42  # el BT de verdad se demora 5.42 seg en ir de lado a lado
VELOC_X_ENGRANAJES      = SCREEN_WIDTH/60/9.38

N_COLORES_ENGRANAJES    = 4
SIZE_ENGRANAJES         = 0.035
MAX_SIZE_ENGRANAJES     = 6
FACTOR_DIAMETRO_SIZE    = 1.1
ACEL_Y_ENGRANAJES       = 0.085
VY_REBOTE_ENG           = -3.1
FACTOR_REBOTE_SIZE      = 0.42
DIST_CENTRO_ENGRS_CREADOS   = 0.25

FRAMES_SIN_DISPARO      = 200//(1000/60)     # no se repiten los disparos durante 200mseg
ANCHO_BALA_NORMAL           = 3
COLORES_BALAS_NORMALES      = [(255,0,0), (0,0,255)]
COLORES_BALAS_GANCHO        = [(255*2/3,0,0),(0,0,255*2/3)]
ALPHA_CUBRE_NEGRO           = 170
ALTURA_SALIDA_BALA          = 44    # respecto a ALTURA_PISO
FRAMES_B_GANCHO_CLAVADA     = 4*60  # clavada por 4 segs
ALTURA_INI_BALA_FUGAZ       = 3

ANCHO_BARRA_TIEMPO  = 785
ALTO_BARRA_TIEMPO   = 28
X_BARRA_TIEMPO      = 8
Y_BARRA_TIEMPO      = 8

VELOC_SUBIDA_BALA_NORMAL    = 9
VELOC_INI_BALA_FUGAZ        = 3.25
ACEL_SUBIDA_BALA_FUGAZ      = 1.125
ACEL_SUBIDA_PARED           = 4
ACEL_SUBIDA_PUERTA          = 1.5
VELOC_CAIDA_POWERUP         = 2
POWERUP_FRAMES_PISO         = 2.5*60
POWERUP_FRAMES_TRANSP       = POWERUP_FRAMES_PISO + 0.5*60

PUNTAJE_SILVER          = 300
PUNTAJE_GOLD            = PUNTAJE_SILVER*4
PUNTAJE_ROMPER          = [0,100,50,25,17,15,12]
PUNTAJE_SEG_RESTANTE    = 130
SEGUNDOS_TIEMPO_EXTRA   = 10


SURFACE_ENGRANAJES      = None  # [color][tamaño], (image,hitmask)
SURFACE_BALAS_NORMALES  = None
SURFACE_BALAS_GANCHO    = None
RH_BALAS_NORMALES       = None  # (rect,hitmask)
SURFACE_BALAS_FUGAZ     = None  # [frame(surface,rect,hitmask)]
SURFACE_POP             = None  # [tamaño][n]
SURFACE_CUBRE_MUERTE    = None
SURFACE_COMBO           = None  # [n]
SURFACE_PARED_NORMAL    = None
SURFACE_PARED_ENGRANAJE = None
SURFACE_PARED_PUERTA    = None
SURFACE_POWERUPS        = None  # [dict:id][opaco,transp,hitmask]
SURFACE_STATUSBAR       = None
SURFACE_HEARTS          = None  # [heart/blank]
SURFACE_CUBRE_TODO      = None
SURFACE_BARRA_TIEMPO    = None
SURFACE_BARRA_T_VACIA   = None
SURFACE_1px_BARRA_T     = None


# No constantes (en minusculas)

_paredes = None
_paredesEngranajes = None
_idsEngranajes = None

_balasSacar = None
_engranajesSacar = None
_efectosSacar = None
_efectosAgregar = None

_puntuacion = None

_sonidos = dict()

