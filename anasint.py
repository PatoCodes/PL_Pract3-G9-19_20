#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import errores


class Sintactico:
#Constructor de la clase que implementa el Analizador Sintactico
#Solicita el primer compnente lexico 
  def __init__(self, lexico):
    self.lexico= lexico
    self.token=self.lexico.Analiza()

  def Avanza(self):
    self.token=self.lexico.Analiza()

# Funcion que muestra los mensajes de error
  def Error(self, nerr, tok):
    if nerr == 1: #PROGRAMA
      print ("Linea: " + str(self.token.linea) + "  ERROR Se espera PROGRAMA en la cabecera del programa")
    elif nerr == 2: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR Se espera un identificador")
    elif nerr == 6: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba una delaración de variable o una intrucción")
    elif nerr == 7: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba ':'")
    elif nerr == 8: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba ';'")
 
# TERMINALES
  def Programa(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
      #<Programa> -> PROGRAMA id; <decl_var> <instrucciones>.
      self.Avanza()
    else:
      self.Error(1, self.token)    
  

  def decl_var(self):
    # <decl_var> -> VAR <lista_id> : <tipo> ; <decl_v>
    if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":
      self.Avanza()
      if self.lista_id():
        if self.token.cat == "DosPuntos":
          self.Avanza()
          if self.tipo():
            if self.token.cat == "PuntoComa":
              self.Avanza()
              if self.decl_v():
                return True
              else:
                return False
            else:
              self.Error(8, self.token)
              return False
          else:
            return False
        else:
          self.Error(7, self.token)
          return False
      else:
        return False
    else:
      if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
        return True
      self.Error(6, self.token)
      return False
  
  def lista_id(self):
    pass

  def tipo(self):
    pass

  def decl_v(self):
    pass

 

########################################################
##
## PRograma principal que lanza el analizador sintactico
####################################################
if __name__=="__main__":
  script, filename=argv
  txt=open(filename)
  print ("Este es tu fichero %r" % filename)
  i=0
  fl = flujo.Flujo(txt)
  anlex=analex.Analex(fl)
  S = Sintactico(anlex)
  if S.Programa():
    print ("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
  else:
    print ("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")

