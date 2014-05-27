# -*- coding: utf-8 -*-
# (si no, no puedo escribir �)

from Globals import *
import Globals

# un arreglo con diccionarios con los elementos de cada etapa
# parte desde la posicion 1

# fondo: numero de fondo
# tiempo: en segundos (minimo 14 seg)
# xIniPlayerI: coordenada x inicial del player i
# engranajes: arreglo con arreglos con los argumentos para crear engranajes
# (opcional) paredes: tipo, x, id

ETAPAS = [None,
    {     # etapa 1
        "fondo":3,
        "tiempo":20,
        "xIniPlayer1":350,
        "xIniPlayer2":450,
        "engranajes":[
            [100,360,2,DERECHA,0,-2,0]
        ]
    },
    
    {   # etapa 2
    "fondo":3,
    "tiempo":60,
    "xIniPlayer1":200,
    "xIniPlayer2":400,
    "engranajes":[
        [100,200, 2, IZQUIERDA, 0, 0, 0],
        [300,200, 2, IZQUIERDA, 0, 0, 0],
        [500,200, 2, DERECHA,   2, 0, 0],
        [700,200, 2, DERECHA,   2, 0, 0]
    ]
     },
          
    {   # etapa 3
    "fondo":1,
    "tiempo":80,
    "xIniPlayer1":200,
    "xIniPlayer2":400,
    "engranajes":[[200,200,5,DERECHA,1,0,0]]
     },
          
    #{   # etapa 4
    #"xIniPlayer1":200,
    #"xIniPlayer2":400,
    #"engranajes":[
    #    [50 ,200, 2, DERECHA, 0, 0],
    #    [150,220, 2, DERECHA, 0, 0],
    #    [250,240, 2, DERECHA, 0, 0],
    #    [350,260, 2, DERECHA, 0, 0],
    #    [450,280, 2, DERECHA, 0, 0],
    #    [550,300, 2, DERECHA, 0, 0],
    #    [650,320, 2, DERECHA, 0, 0],
    #    [750,340, 2, DERECHA, 0, 0],
    #    [850,180, 2, DERECHA, 0, 0],
    #    [950,160, 2, DERECHA, 0, 0]]
    # }
    
    {     # etapa grande de prueba
    "fondo":2,
    "tiempo":140,
    "xIniPlayer1":250,
    "xIniPlayer2":200,
    "engranajes":[
        [25, 200, 1, IZQUIERDA, 2, -5, 0],
        [120,200, 2, PARADO,    0,  0, 1],
        [300,200, 3, PARADO,    0,  0, 0],
        [400,200, 4, PARADO,    0,  0, 0],
        [550,200, 5, PARADO,    3,  0, 2],
        [600,200, 6, PARADO,    0,  0, 0],
        [750,400, 1, DERECHA,   1,  0, 0],
        [740,400, 1, IZQUIERDA, 1,  0, 0],
        [745,400, 2, IZQUIERDA, 1,  0, 0],
        ],
    "paredes":[
        [PARED_NORMAL,700,2],
        [PARED_ENGRANAJES,50,0],
        [PARED_PUERTA,50,1]]
    }
]