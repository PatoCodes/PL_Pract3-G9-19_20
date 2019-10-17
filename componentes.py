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
class OpAsigna (Componente): 
  def __init__(self,nl):
    Componente.__init__(self)
    self.linea=nl


# componente lexico. Final de fichero
class EOF(Componente):
  pass


# componente lexico.  Operadores de suma
class OpSuma(Componente):
  def __init__(self,nl,operacion):
	Componente.__init(self)
	self.linea = nl
	selft.operacion = operacion
	
#  componente lexico. operadores de multiplicacion
#  componente lexico. Numeros
# componente lexico.  identificadores
# componente lexico. Palabras reservadas
# componente lexico. operadores relacionales 
# componente lexico. llaves, parentesis y corchetes 
# componente lexico. otros simbolos  (punto, dospuntos, coma, punto y coma)

 
