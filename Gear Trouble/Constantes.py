# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

SCREEN_WIDTH    = 1024
SCREEN_HEIGHT   = 768
FULLSCREEN      = False
ALTURA_PISO     = SCREEN_HEIGHT-40    # por ejemplo, una barra informativa abajo de 40px de alto

IMGS_ANIMACION      = 4
FRAMES_POR_IMAGEN   = 6

IZQUIERDA   = 0
DERECHA     = 1
PARADO      = 2
VELOC_MOV_PERSONAJES = SCREEN_WIDTH/60/5.42     # el BT de verdad se demora 5.42 seg en ir de lado a lado
