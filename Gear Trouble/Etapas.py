# -*- coding: utf-8 -*-
# (si no, no puedo escribir �)

from Globals import *
import Globals

# un arreglo con diccionarios con los elementos de cada etapa
# parte desde la posicion 1

# tiempo: en segundos
# xIniPlayerI: coordenada x inicial del player i
# engranajes: arreglo con arreglos con los argumentos para crear engranajes
# (opcional) paredes: tipo, x, id

ETAPAS = [None,
          
    {     # etapa 1
    "tiempo":300,
    "xIniPlayer1":150,
    "xIniPlayer2":400,
    "engranajes":[
        [25, 200, 1, IZQUIERDA, 2, -5, 0],
        [100,200, 1, PARADO,    0,  0, 1],
        [200,200, 2, PARADO,    0,  0, 0],
        [300,200, 3, PARADO,    0,  0, 0],
        [400,200, 4, PARADO,    0,  0, 0],
        [550,200, 5, PARADO,    3,  0, 2],
        [600,200, 6, PARADO,    0,  0, 0],
        [750,400, 1, IZQUIERDA, 1,  0, 0],
        [760,400, 1, DERECHA,   1,  0, 0],
        [770,400, 1, DERECHA,   1,  0, 0],
        [780,400, 1, IZQUIERDA, 1,  0, 0],
        [770,400, 2, IZQUIERDA, 1,  0, 0],
        ],
    "paredes":[
        [PARED_NORMAL,720,2],
        [PARED_ENGRANAJES,50,0],
        [PARED_PUERTA,50,1]]
    },
    
    {   # etapa 2
    "xIniPlayer1":200,
    "xIniPlayer2":400,
    "engranajes":[
        [100,200, 3, IZQUIERDA, 0, 0],
        [300,200, 3, IZQUIERDA, 0, 0],
        [500,200, 3, PARADO,    0, 0],
        [700,200, 3, DERECHA,   0, 0],
        [900,200, 3, DERECHA,   0, 0]]
     },
          
    {   # etapa 3
    "xIniPlayer1":200,
    "xIniPlayer2":400,
    "engranajes":[
        [200,200, 6, DERECHA,   0, 0],
        [700,200, 6, IZQUIERDA, 0, 0]]
     },
          
    {   # etapa 4
    "xIniPlayer1":200,
    "xIniPlayer2":400,
    "engranajes":[
        [50 ,200, 2, DERECHA, 0, 0],
        [150,220, 2, DERECHA, 0, 0],
        [250,240, 2, DERECHA, 0, 0],
        [350,260, 2, DERECHA, 0, 0],
        [450,280, 2, DERECHA, 0, 0],
        [550,300, 2, DERECHA, 0, 0],
        [650,320, 2, DERECHA, 0, 0],
        [750,340, 2, DERECHA, 0, 0],
        [850,180, 2, DERECHA, 0, 0],
        [950,160, 2, DERECHA, 0, 0]]
     }
]