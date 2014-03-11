# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

# Constantes

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FULLSCREEN = False
ALTURA_PISO = SCREEN_HEIGHT-40 # por ejemplo, una barra informativa abajo de 40px de alto
ALTURA_TECHO = 10

IMGS_ANIMACION_P = 4
FRAMES_POR_IMAGEN_P = 6
RADIO_CIRCULO_MUERTE = 60
ALPHA_CUBRE_MUERTE = 255*2/3
VIDAS_INIT = 5

IZQUIERDA = -1
DERECHA = 1
PARADO = 0
VELOC_MOV_PERSONAJES = SCREEN_WIDTH/60/5.42 # el BT de verdad se demora 5.42 seg en ir de lado a lado
VELOC_X_ENGRANAJES = SCREEN_WIDTH/60/9.38

N_COLORES_ENGRANAJES = 4
SIZE_ENGRANAJES = 35
MAX_SIZE_ENGRANAJES = 6
FACTOR_DIAMETRO_SIZE = 1.4
ACEL_Y_ENGRANAJES = 0.12 # velocidad aleatoria para poder hacer pruebas, despues cambiar por definitiva
VELOC_Y_REBOTE_ENG = -4
FACTOR_REBOTE_SIZE = 0.52
##### pelota mas chica se demora 1.16 seg en subir y bajar
DIST_CENTRO_ENGRS_CREADOS = 0.25

BALA_NORMAL = 0
BALA_GANCHO = 1
BALA_FUGAZ = 2
BALA_TORRE = 3
ANCHO_BALA_NORMAL = 5
COLORES_BALAS = [(255,0,0), (0,0,255)]
ALTURA_SALIDA_BALA = 45 # respecto a ALTURA_PISO
VELOC_SUBIDA_BALA_NORMAL = 9


SURFACE_ENGRANAJES = None # [color][tamaño], (image,hitmask)
SURFACE_BALAS_NORMALES = None
RH_BALAS_NORMALES = None # (rect,hitmask)


# No constantes

_paredes = None
_paredesEngranajes = None

_balasSacar = None
_engranajesSacar = None