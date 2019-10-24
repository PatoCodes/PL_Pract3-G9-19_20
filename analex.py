#!/usr/bin/env python

import componentes
import errores
import flujo
import string
import sys

from sys import argv
from sets import ImmutableSet

class Analex:
 PR = frozenset(["PROGRAMA", "VAR", "VECTOR", "DE", "ENTERO", "REAL", "BOOLEANO", "INICIO","PROC","FUNCION",
                      "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "CIERTO", "FALSO","Y","O","NO" ])

 ############################################################################
 #
 #  Funcion: __init__
 #  Tarea:  Constructor de la clase
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
 def __init__(self, flujo):
    self.flujo= flujo
    self.poserror= 0
    self.nlinea=1

 ############################################################################
 #
 #  Funcion: TrataNum
 #  Tarea:  Lee un numero del flujo
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: primera caractera tratar
 #  Devuelve: El valor numerico de la cadena leida
 #
 ############################################################################
 def TrataNum(self,flujo, ch):
  l=ch
  real = False
  ch = self.flujo.siguiente()
  while ch and ch in string.digits:
   l += ch
   ch = self.flujo.siguiente()
  if ch == ".":
   l += ch
   real = True
   ch = self.flujo.siguiente()
   if ch and ch in string.digits:
    while ch and ch in string.digits:
     l += ch
     ch = self.flujo.siguiente()
     self.flujo.devuelve(ch)
   else:
    raise errores.ErrorLexico("Numero real erroneo")
  else:
   self.flujo.devuelve(ch)
  if real:
   v = float(l)
  else:
   v = int(l)
  return v

 ############################################################################
 #
 #  Funcion: TrataIdent
 #  Tarea:  Lee identificadores
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: Primer caracter a tratar
 #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
 #
 ############################################################################
 def TrataIdent(self,flujo, ch):
  l = ch
  ch = self.flujo.siguiente()
  while ch and (ch in string.letters or ch in string.digits):
   l += ch
   ch = self.flujo.siguiente()
  if ch :
   self.flujo.devuelve(ch)
  return l

  ############################################################################
  #
  #  Funcion: TrataIdent
  #  Tarea:  Lee identificadores
  #  Prametros:  flujo:  flujo de caracteres de entrada
  #              ch: Primer caracter a tratar
  #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
  #
  ############################################################################
 def TrataComent(self, flujo):
   ch = self.flujo.siguiente()
   ini=self.nlinea
   while ch and ch!="}":
    ch = self.flujo.siguiente()
  #  print "caracter", ch
   if ch and ch=="}":
    pass #self.flujo.devuelve(ch)
    #self.Analiza()
   else:
    s="ERROR LEXICO Linea "+str(ini) +":: Comentario abierto y no cerrado antes de finalizar el fichero"
    print s
   # raise errores.ErrorLexico(s)
 ############################################################################
 #
 #  Funcion: EliminaBlancos
 #  Tarea:  Descarta todos los caracteres blancos que hay en el flujo de entrada
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
 def EliminaBlancos(self,flujo):
  ch = self.flujo.siguiente()
  while ch and ch == " ":
   ch = self.flujo.siguiente()
  self.flujo.devuelve(ch)

 ############################################################################
 #
 #  Funcion: Analiza
 #  Tarea:  Identifica los diferentes componentes lexicos
 #  Prametros:  --
 #  Devuelve: Devuelve un componente lexico
 #
 ############################################################################
 def Analiza(self):
  l = ""
  ch=self.flujo.siguiente()
  if ch==" ":
    ##acciones si hemos encontrado un blancoi
  elif ch=="\r":
    #acciones si hemos encontrado un salto de linea
  elif 
#    completar aqui para todas las categorias lexicasw
  elif ch== "\n":
   ## acciones al encontrar un salto de linea
   self.nlinea = self.nlinea + 1
   return componentes.nl()
  elif ch.isdecimal():
   resultado = self.TrataNum(self.flujo, ch)
   if isinstance(resultado, int):
     return componentes.Numero(self.nlinea, resultado, "int")
   else:
     return componentes.Numero(self.nlinea, resultado, "real")

  elif ch:
    # se ha encontrado un caracter no permitido
    print ("ERROR LEXICO  Linea "+  str(self.nlinea) +" ::  Caracter "+ ch +" invalido ")
    return self.Analiza()
  else:
    # el final de fichero
    return componentes.EOF()

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__=="__main__":
    script, filename=argv
    # Apertura del fichero que se va a procesar
    txt=open(filename)
    print ("Este es tu fichero %r" % filename)
    i=0
    #asociamos un flujo al fichero
    fl = flujo.Flujo(txt)
    #creamos una instancia del analizador    
    analex=Analex(fl)
    #inciamos el analisis
    c=analex.Analiza()
    while c.cat!="EOF" :
      print c
      c=analex.Analiza()
    i=i+1

