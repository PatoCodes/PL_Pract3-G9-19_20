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
    elif nerr == 3: #Falta punto y coma
      print ("Linea: " + str(self.token.linea) + "  ERROR: Las sentencias deben acabar con punto y coma")
    elif nerr == 4: #Programa debe acabar con .
      print ("Linea: " + str(self.token.linea) + "  ERROR: La definición del programa debe acabar con un .")
    elif nerr == 5: #Categorías despues del final de fichero
      print ("Linea: " + str(self.token.linea) + "  ERROR: Componentes inesperados tras el final del programa")
    elif nerr == 6: #decl_var
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba una delaración de variable o una intrucción")
    elif nerr == 7: #:
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba ':'")
    elif nerr == 8: #;
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba ';'")
    elif nerr == 9: #,
      print ("Linea: " + str(self.token.linea) + "  ERROR Se esperaba ','")
    
    
    
 
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
            if self.instrucciones():
              if self.token.cat == "Punto":
                #FINAL DE FICHERO
                self.Avanza()
                if self.token.cat == "EOF":
                  return True
                else:
                  self.Error(5, self.token)
                  return False
              else:
                self.Error(4, self.token)
                return False
            else:
              return False
          else:
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
      else:
        self.Error(6, self.token)
        return False
  
  def decl_v(self):
    if self.lista_id():
      #<decl_v> → <lista_id> : <tipo> ; <decl_v>
    elif self.token.cat in ["INICIO"]:
      #Siguientes
      return True
    else:
      
  
  def instrucciones(self):
    return True
    
  def lista_id(self):
    if self.token.cat == "Identificador":
      self.Avanza()
      return self.resto_listaid()
    else:
      self.Error(2, self.token)
      return False

  def resto_listaid(self):
    if self.token.cat == "Coma":
      self.Avanza()
      return self.lista_id()
    else:
      if self.token.cat == "DosPuntos":
        return True
      else:
        self.Error(2, self.token)
        return False

  def tipo(self):
    return True

  def decl_v(self):
    return True


 

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

