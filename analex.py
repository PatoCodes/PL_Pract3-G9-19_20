#!/usr/bin/env python

import componentes
import errores
import flujo
import string
import sys

from sys import argv

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
  # Almacenamos el primer número y preparamos para seguir leyendo
  l=ch
  real = False
  ch = self.flujo.siguiente()
  # Mientras leamos números, seguimos avanzando
  while ch and ch in string.digits:
   l += ch
   ch = self.flujo.siguiente()
  # Comprobamos si el siguiente caracter leido despues de los números es un punto
  if ch and ch == ".":
   # Punto encontrado: esperamos número real
   l += ch
   real = True
   ch = self.flujo.siguiente()
   # Esperamos encontrar al menos un decimal
   if ch and ch in string.digits:
    # Mientras leamos dígitos, seguimos en el bucle
    while ch and ch in string.digits:
     l += ch
     ch = self.flujo.siguiente()
    if ch:
     self.flujo.devuelve(ch)
   else:
     # Si no hay decimales, ha habido un error leyendo el numero real
     raise errores.ErrorLexico("Numero real erroneo")
  # Punto no encontrado: hemos leido un entero
  elif ch:
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
 def TrataIdent(self, flujo, ch):
  l = ch
  ch = self.flujo.siguiente()
  while ch and (ch in string.ascii_letters or ch in string.digits):
   l += ch
   ch = self.flujo.siguiente()
  if ch :
   self.flujo.devuelve(ch)
  return l

#Funcion Aparte
 def TrataBlanco(self, ch):
   ch = self.flujo.siguiente()
   while ch and (ch == " " or ch == "\t"):
     ch=self.flujo.siguiente()
   if ch:
    self.flujo.devuelve(ch)

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
   while ch and (ch!="\r" and ch!="\n"):
    ch = self.flujo.siguiente()
   if ch:
    self.flujo.devuelve(ch)

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

  ## Acciones si hemos encontrado un blanco o un tabulador
  if ch==" " or ch=="\t":
    self.TrataBlanco(ch)
    return self.Analiza()

  ## Acciones si hemos encontrado un salto de linea
  elif ch=="\r":
    return self.Analiza()
  elif ch== "\n":
   self.nlinea = self.nlinea + 1
   return self.Analiza()

  ## Acciones al encontrar un número
  elif ch.isdigit():
   resultado = self.TrataNum(self.flujo, ch)
   if isinstance(resultado, int):
     ## Int
     return componentes.Numero(self.nlinea, resultado, "int")
   else:
     ## Real
     return componentes.Numero(self.nlinea, resultado, "real")

  ## Acciones al encontrar un identificador
  elif ch.isalpha():
    resultado = self.TrataIdent(self.flujo, ch)
    #Palabra reservada
    if resultado in self.PR:
      return componentes.PalabraReservada(self.nlinea, resultado)
    #Identificador
    else:
      return componentes.Identificador(self.nlinea, resultado)

  ## Parentesis, llaves y corchetes
  elif ch =="(":
    return componentes.ParentesisApertura(self.nlinea)
  elif ch ==")":
    return componentes.ParentesisCierre(self.nlinea)
  elif ch =="{":
    return componentes.LlaveApertura(self.nlinea)
  elif ch =="}":
    return componentes.LlaveCierre(self.nlinea)
  elif ch =="[":
    return componentes.CorcheteApertura(self.nlinea)
  elif ch =="]":
    return componentes.CorcheteCierre(self.nlinea)

  ## Dos puntos y operador de asignacion
  elif ch == ":":
    # Comprobamos si es asignación
    ch = self.flujo.siguiente()
    if ch == "=":
      return componentes.OpAsigna(self.nlinea)
    else:
      self.flujo.devuelve(ch)
      return componentes.DosPuntos(self.nlinea)

  ## Punto y coma, punto, coma
  elif ch == ";":
    return componentes.PuntoComa(self.nlinea)
  elif ch == ".":
    return componentes.Punto(self.nlinea)
  elif ch == ",":
    return componentes.Coma(self.nlinea)
  
  ## Operadores relacionales
  elif ch == "=":
    return componentes.OpRelacional(self.nlinea, "=")
  elif ch == "<":
    ch = self.flujo.siguiente()
    if ch == ">":
      return componentes.OpRelacional(self.nlinea, "<>")
    elif ch == "=":
      return componentes.OpRelacional(self.nlinea, "<=")
    else:
      self.flujo.devuelve(ch)
      return componentes.OpRelacional(self.nlinea, "<")
  elif ch == ">":
    ch = self.flujo.siguiente()
    if ch == "=":
      return componentes.OpRelacional(self.nlinea, ">=")
    else:
      self.flujo.devuelve(ch)
      return componentes.OpRelacional(self.nlinea, ">")

  ## Operadores aritméticos
  elif ch == "+":
    return componentes.OpSuma(self.nlinea, "+")
  elif ch == "-":
    return componentes.OpSuma(self.nlinea, "-")
  elif ch == "*":
    return componentes.OpMultiplicacion(self.nlinea, "*")
  ## Posiblemente comentario
  elif ch == "/":
    ch = self.flujo.siguiente()
    if ch == "/":
      self.TrataComent(self.flujo)
      return self.Analiza()
    else:
      self.flujo.devuelve(ch)
      return componentes.OpMultiplicacion(self.nlinea, "/")


  elif ch:
    # se ha encontrado un caracter no permitido
    print ("ERROR LEXICO  Linea "+  str(self.nlinea) +" ::  Caracter "+ ch +" invalido ")
    return self.Analiza()
  else:
    # el final de fichero
    return componentes.EOF(self.nlinea)

  

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
      print(c)
      c=analex.Analiza()
    i=i+1


