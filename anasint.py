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
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se espera PROGRAMA en la cabecera del programa")
    elif nerr == 2: #Identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un identificador")
    elif nerr == 3: #Falta punto y coma
      print ("Linea: " + str(self.token.linea) + "  ERROR: Las sentencias deben acabar con punto y coma")
    elif nerr == 4: #Programa debe acabar con .
      print ("Linea: " + str(self.token.linea) + "  ERROR: La definición del programa debe acabar con un .")
    elif nerr == 5: #Se deben declarar variables
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una declaración de variables tras la cabecera.")
    elif nerr == 6: #Se deben declarar instrucciones
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una declaración de instrucciones tras la cabecera.")
    
    
 
# TERMINALES
  def Programa(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
      #<Programa> -> PROGRAMA id; <decl_var> <instrucciones>.
      self.Avanza()
      if self.token.cat == "Identificador":
        self.Avanza()
        if self.token.cat == "PuntoComa":
          self.Avanza()
          if self.decl_var():
            self.Avanza()
            if self.instrucciones():
              self.Avanza()
              if self.token.cat == "Punto":
                #Analizado con exito
                return True
              else:
                self.Error(4, self.token)
                return False
            else:
              self.Error(6, self.token)
              return False
          else:
            self.Error(5, self.token)
            return False
        else:
          self.Error(3, self.token)
          return False
      else:
        self.Error(2, self.token)
        return False
    else:
      self.Error(1, self.token) 
      return False
      
  

  def decl_var(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":
      # <decl_var> → VAR <lista_id> : <tipo> ; <decl_v>
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

