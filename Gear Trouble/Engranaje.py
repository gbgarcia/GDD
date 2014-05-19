# -*- coding: utf-8 -*-
# (si no, no puedo escribir ñ)

import pygame

from Globals import *
import Globals
from Efecto import Efecto

class Engranaje(pygame.sprite.Sprite):
    
    def __init__(self, x,y , size, direccion, color, vy, id_):
        """ Construye un engranaje
        x,y: centro de la posicion inicial
        size (no se puede 'tamaño'): cuantos golpes le faltan para romperse
        direccion: IZQUIERDA/DERECHA/PARADO
        color: 1,2,3,... para cargar la imagen
        vy: velocidad en y
        id: identificador para abrir puertas y paredes (0 si no se usa)
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.x=x
        self.y=y
        
        if size<1 or size>MAX_SIZE_ENGRANAJES:
            raise Exception("Tamaño de engranaje fuera de rango: "+str(size))
        self.size=size
        
        if direccion<-1 or direccion>1:
            raise Exception("Dirección de engranaje inválida: "+str(direccion))
        self.direccion=direccion
        
        if color<0 or color>=N_COLORES_ENGRANAJES:
            raise Exception("Color de engranaje fuera de rango: "+str(color))
        self.color=color
        
        self.vy=vy
        
        if id_<0:
            raise Exception("id negativo: "+str(id_))
        self.id=id_
        Globals._idsEngranajes[self.id]+=1

        (self.image,self.hitmask) = Globals.SURFACE_ENGRANAJES[color][size]
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y) # se pasa a int
        
    @classmethod
    def fromArray(cls,arr):
        return cls(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6])
        
    def update(self):
        
        # movimiento horizontal
        self.x += VELOC_X_ENGRANAJES * self.direccion
        self.rect.centerx=self.x
        
        # rebote horizontal
        paredContraLaQueChoco=None
        
        indexCollide=self.rect.collidelist(Globals._paredes)
        if indexCollide!=-1:
            paredContraLaQueChoco=Globals._paredes[indexCollide]
            
        indexCollide=self.rect.collidelist(Globals._paredesEngranajes)
        if indexCollide!=-1:
            paredContraLaQueChoco=Globals._paredesEngranajes[indexCollide]
            
        if paredContraLaQueChoco:
            if self.direccion==DERECHA:
                self.x += (paredContraLaQueChoco.left-self.rect.right) * 2  
            else:
                self.x -= (self.rect.left-paredContraLaQueChoco.right) * 2
            self.rect.centerx=self.x
            self.direccion*=-1
        
        # movimiento vertical
        self.vy += ACEL_Y_ENGRANAJES
        self.y += self.vy
        self.rect.centery=self.y
        
        # rebote vertical
        if self.rect.bottom >= ALTURA_PISO:
            self.vy = VY_REBOTE_ENG * pow(self.size, FACTOR_REBOTE_SIZE)
            self.y -= (self.rect.bottom-ALTURA_PISO) * 2
            self.rect.centery=self.y
              
        # choque contra el techo
        if self.rect.top <= ALTURA_TECHO:
            self.sacar(False)
            Globals._efectosAgregar.append(Efecto(self.x, Y_COMBO, Globals.SURFACE_COMBO, 1))
        
    def sacar(self,crearOtros):
        Globals._engranajesSacar.append(self)
        Globals._idsEngranajes[self.id]-=1
        
        if crearOtros:
            lista=[]
            if self.size>1:
                despl_x=self.rect.width*DIST_CENTRO_ENGRS_CREADOS
                
                # no tiene sentido pasar estos numeros a constantes
                p1 = 0.9 - self.size/9.0                # plot(0.9-size/9,size=1..6,y=0..1);
                p2 = 1/( (1+pow(self.vy,2))/4 + 1.25)   # plot(1/((1+vy^2)/4+1.25),vy=-3..3,y=0..1);
                nueva_vy = -10.25*p1*p2                 # plot3d(10.25*(0.9-size/9)*1/((1+vy^2)/4+1.25),size=1..6,vy=-3..3,axes=normal,shading=zhue);
                #print "%0.4f , %0.4f -> %0.4f" % (p1,p2,nueva_vy)
                
                lista.append(Engranaje(self.x-despl_x, self.y, self.size-1, IZQUIERDA, self.color, nueva_vy, self.id))
                lista.append(Engranaje(self.x+despl_x, self.y, self.size-1, DERECHA  , self.color, nueva_vy, self.id))
            return lista
        