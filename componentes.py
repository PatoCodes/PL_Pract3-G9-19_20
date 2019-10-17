#!/usr/bin/env python

import string
import sys
######################################################################################
##
##  Define varias clases que definen cada uno de los diferentes componentes lexicos
##
##
##
######################################################################################

# Clase generica que define un componente lexico 
class Componente:
  def __init__(self):
    self.cat= str(self.__class__.__name__)

  def __str__(self):
    s=[]
    for k,v in self.__dict__.items():
      if k!= "cat": s.append("%s: %s" % (k,v))
    if s:
      return "%s (%s)" % (self.cat,", ".join(s))
    else:
      return self.cat

# componente lexico salto de linea
class nl(Componente):
  pass

# componente lexico espacios en blanco
class blanco(Componente):
  pass

# componente lexico operador de asignacion
class OpAsigna(Componente): 
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl


# componente lexico. Final de fichero
class EOF(Componente):
  pass


# componente lexico.  Operadores de suma
class OpSuma(Componente):
  def __init__(self, nl, operacion):
	Componente.__init__(self)
	self.linea = nl
	# + o -
	self.operacion = operacion
	
	
#  componente lexico. operadores de multiplicacion
class OpMultiplicacion(Componente):
  def __init__(self,nl,operacion):
	Componente.__init(self)
	self.linea = nl
	self.operacion = operacion


#  componente lexico. Numeros

class Numero(Componente):
  def __init__(self, nl, tipo):
    Componente.__init__(self)
	self.linea = nl
	# Entero o real
	self.tipo = tipo

# componente lexico.  identificadores
class identificador(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl
	self.valor = valor


# componente lexico. Palabras reservadas

class PalabraReservada(Componente):
  def __init__(self, nl, palabra):
	Componente.__init__(self)
	self.linea = nl
	# PRO-GRAMA,  VAR,  VECTOR,  ENTERO,  REAL,  BOOLEANO,  INICIO,  FIN,  SI,  ENTON-CES, SINO, MIENTRAS, HACER, LEE, ESCRIBE, Y, O, NO, CIERTO y FALSO.
	self.palabra = palabra
	
# componente lexico. operadores relacionales 
class OpRelacional(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl
	self.operacion = operacion


# componente lexico. llaves, parentesis y corchetes 

class LlaveApertura(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
	
class LlaveCierre(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
		
class ParentesisApertura(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
	
class ParentesisCierre(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
	
class CorcheteApertura(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
	
class CorcheteCierre(Componente):
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl
	
# componente lexico. otros simbolos  (punto, dospuntos, coma, punto y coma)
class punto(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl
	
	
class dosPuntos(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl


class coma(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl


class puntoComa(Componente, valor):
  def __init__(self,nl):
	Componente.__init(self)
	self.linea = nl


 
