# -*- coding: utf-8 -*-
# (si no, no puedo escribir �)

import pygame

from Globals import *
import Globals

class Pared(pygame.sprite.Sprite):
    
    def __init__(self, tipo, x, id_):
        """ Una pared. Puede ser completa o solo para engranajes
        x: coordenada izquierda
        imagen: depende de su altura
        tipo: PARED_NORMAL, PARED_ENGRANAJES, PARED_PUERTA
        id_: para levantarla (0 si no se usa)
        """
        
        pygame.sprite.Sprite.__init__(self)
        
        self.tipo=tipo
        if self.tipo==PARED_NORMAL:
            self.image=Globals.SURFACE_PARED_NORMAL
        elif self.tipo==PARED_ENGRANAJES:
            self.image=Globals.SURFACE_PARED_ENGRANAJE
        elif self.tipo==PARED_PUERTA:
            self.image=Globals.SURFACE_PARED_PUERTA
        else:
            raise Exception("Tipo de pared inválido: "+str(tipo))

        self.rect=self.image.get_rect()
        self.rect.left=x
        
        if id_<0:
            raise Exception("id de pared negativo: "+str(id_))
        self.id=id_
        
        self.levantar=False
        self.vy=0
        if tipo==PARED_PUERTA:
            self.rect.top=ALTURA_PUERTA
            self.ay=ACEL_SUBIDA_PUERTA
            self.tope=ALTURA_PUERTA
        else:
            self.ay=ACEL_SUBIDA_PARED
            self.tope=0
                    
    def update(self, paredesSacar, idLevantar):
        if self.id==idLevantar:
            self.levantar=True
            
            if self.tipo==PARED_ENGRANAJES:
                buscarDonde=Globals._paredesEngranajes
            else:
                buscarDonde=Globals._paredes
            
            for i in range(len(buscarDonde)):
                if buscarDonde[i].left==self.rect.left:
                    del buscarDonde[i]
                    break
            
        if self.levantar:
            self.vy+=self.ay
            self.rect.top-=self.vy
            if self.rect.bottom<self.tope:
                paredesSacar.append(self)
    