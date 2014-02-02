import pygame
from pygame. locals import *  
from pygame.display import set_mode  
from pygame import time as pytime  
  
pygame.init()  
  
def movie(archivo):
    try : movie = pygame.movie.Movie(archivo)
    except pygame.error, message:
        raise SystemExit, message
    return movie
visor = pygame.display.set_mode((960,720),0,0)
pygame.display.set_caption('fondo')
fondo = movie('fondo.mpg')

fondo.play()
