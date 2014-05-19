# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

# Constantes (en Mayusculas)

SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 600
FULLSCREEN      = True#False
ALTURA_PISO     = SCREEN_HEIGHT-140 # status bar de 140px
ALTURA_TECHO    = 14
ANCHO_PAREDES_BORDES    = 5
ANCHO_PARED     = 30
ALTURA_PUERTA   = 410

IMGS_ANIMACION_PERS     = 4
FRAMES_POR_IMAGEN_PERS  = 8
IMAGENES_POP            = 3
FRAMES_POR_IMAGEN_POP   = 2
FRAMES_COMBO            = 12
Y_COMBO = ALTURA_TECHO+35/4

VIDAS_INIT  = 5

IZQUIERDA   = -1
DERECHA     = 1
PARADO      = 0

PARED_NORMAL        = 0
PARED_ENGRANAJES    = 1
PARED_PUERTA        = 2

BALA_NORMAL     = 0
BALA_GANCHO     = 1
BALA_FUGAZ      = 2
BALA_TORRE      = 3

VELOC_MOV_PERSONAJES    = SCREEN_WIDTH/60/5.42  # el BT de verdad se demora 5.42 seg en ir de lado a lado
VELOC_X_ENGRANAJES      = SCREEN_WIDTH/60/9.38

N_COLORES_ENGRANAJES    = 4
SIZE_ENGRANAJES         = 40
MAX_SIZE_ENGRANAJES     = 6
FACTOR_DIAMETRO_SIZE    = 1.2
ACEL_Y_ENGRANAJES       = 0.09
VY_REBOTE_ENG           = -3.1
FACTOR_REBOTE_SIZE      = 0.47
DIST_CENTRO_ENGRS_CREADOS   = 0.25

FRAMES_SIN_DISPARO      = 200//(1000/60)     # no se repiten los disparos durante 200mseg
ANCHO_BALA_NORMAL           = 3
COLORES_BALAS_NORMALES      = [(255,0,0), (0,0,255)]
COLORES_BALAS_GANCHO        = [(255*2/3,0,0),(0,0,255*2/3)]
ALTURA_SALIDA_BALA          = 44    # respecto a ALTURA_PISO
VELOC_SUBIDA_BALA_NORMAL    = 9
VELOC_SUBIDA_PARED          = 6
VELOC_SUBIDA_PUERTA         = 2


SURFACE_ENGRANAJES      = None  # [color][tamaño], (image,hitmask)
SURFACE_BALAS_NORMALES  = None
SURFACE_BALAS_GANCHO    = None
RH_BALAS_NORMALES       = None  # (rect,hitmask)
SURFACE_POP             = None  # [tamaño][n]
SURFACE_CUBRE_MUERTE    = None
SURFACE_COMBO           = None  # [n]
SURFACE_PARED_NORMAL    = None
SURFACE_PARED_ENGRANAJE = None
SURFACE_PARED_PUERTA    = None



# No constantes (en minusculas)

_paredes = None
_paredesEngranajes = None

_idsEngranajes = None

_balasSacar = None
_engranajesSacar = None
_efectosSacar = None
_efectosAgregar = None
