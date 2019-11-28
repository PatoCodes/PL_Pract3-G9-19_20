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

# Funcion que muestra los mensajes de error
 def Error(self, nerr, tok):
     if nerr == 1:
         print ("Linea: " + str(self.token.linea) + "  ERROR Se espera PROGRAMA")
 
# TERMINALES
 def Programa(self):
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

