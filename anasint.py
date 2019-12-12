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
    elif nerr == 2: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se espera un identificador")
    elif nerr == 3: #Falta punto y coma
      print ("Linea: " + str(self.token.linea) + "  ERROR: Las sentencias deben acabar con punto y coma")
    elif nerr == 4: #Programa debe acabar con .
      print ("Linea: " + str(self.token.linea) + "  ERROR: La definición del programa debe acabar con un .")
    elif nerr == 5: #Categorías despues del final de fichero
      print ("Linea: " + str(self.token.linea) + "  ERROR: Componentes inesperados tras el final del programa")
    elif nerr == 6: #decl_var
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una delaración de variable o una instrucción")
    elif nerr == 7: #:
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba ':' para declaración de tipo")
    elif nerr == 8: #
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba ':=', una expresion entre corchetes, un SINO o un ';'") #ERROR LIBRE
    elif nerr == 9: #,
      print ("Linea: " + str(self.token.linea) + "  ERROR: ") #ERROR LIBRE
    elif nerr == 10: #Tipo
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un tipo válido (ENTERO, REAL, BOOLEANO) o un vector")
    elif nerr == 11: #INICIO
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba INICIO")
    elif nerr == 12: #FIN
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba FIN")
    elif nerr == 13: #Inicio corchete
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba '['")
    elif nerr == 14: #Número para índice
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un numero como indice")
    elif nerr == 15: #Cierre corchete
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba ']'")
    elif nerr == 16: #DE
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se espera la palabra DE para indicar el tipo de un vector")
    elif nerr == 17: #lista_instr
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una ',' o ':'")
    elif nerr == 18: #ENTONCES
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un 'ENTONCES'")
    elif nerr == 19: #TIPO VALIDO
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un tipo valido (ENTERO, REAL o BOOLEANO)")    
    elif nerr == 20:
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un operador de asignación ':='")    
    elif nerr == 21: #SINO
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un 'SINO'")

  # No Terminal Programa
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

  # No Terminal Decl_Var  
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
              return self.decl_v()
            else:
              self.Error(3, self.token)
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
  
  #  No Terminal Decl_V
  def decl_v(self):
    if self.token.cat == "Identificador":
      #<decl_v> → <lista_id> : <tipo> ; <decl_v>
      if self.lista_id():
        if self.token.cat == "DosPuntos":
          self.Avanza()
          if self.tipo():
            if self.token.cat == "PuntoComa":
              self.Avanza()
              return self.decl_v()
            else:
              self.Error(3, self.token)
              return False
          else:
            return False
        else:
          self.Error(7, self.token)
          return False
    elif self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO"]:
      #Siguientes
      return True
    else:
      self.Error(2, self.token)
      return False

  def lista_id(self):
    #<lista_id> → id <resto_listaid>
    if self.token.cat == "Identificador":
      self.Avanza()
      return self.resto_listaid()
    else:
      self.Error(2, self.token)
      return False

  def resto_listaid(self):
    #<resto_listaid> →  , <lista_id>
    if self.token.cat == "Coma":
      self.Avanza()
      return self.lista_id()
    #Siguientes
    elif self.token.cat == "DosPuntos":
      return True
    else:
      self.Error(17, self.token)
      return False

  def tipo(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
      #<Tipo> → <tipo_std>
      if self.tipo_std(): 	
        return True
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "VECTOR":
      #<Tipo> → VECTOR [num] DE <Tipo_std>
      self.Avanza()
      if self.token.cat == "CorcheteApertura":
        self.Avanza()
        if self.token.cat == "Numero":
          self.Avanza()
          if self.token.cat == "CorcheteCierre":
            self.Avanza()
            if self.token.cat == "PalabraReservada" and self.token.palabra == "DE":
              self.Avanza()
              return self.tipo_std()
            else:
              self.Error(16, self.token)
              return False
          else:
            self.Error(15, self.token)
            return False
        else:
          self.Error(14, self.token)
          return False
      else:
        self.Error(13, self.token)
        return False
    else:
      self.Error(10, self.token)
      return False

  def tipo_std(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO","REAL","BOOLEANO"]:
      #<Tipo_std> → ENTERO
      #<Tipo_std> → REAL
      #<Tipo_std> → BOOLEANO
      self.Avanza()
      return True
    else:
      self.Error(19, self.token)
      return False

  def instrucciones(self):
    #<instrucciones> → INICIO <lista_inst> FIN
    if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
      self.Avanza()
      if self.lista_inst():
        if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
          self.Avanza()            
          return True
        else:
          self.Error(12, self.token)
          return False
      else:
        return False
    else:
      self.Error(11, self.token)
      return False

  def lista_inst(self):
    #<lista_inst> → <instrucción> ; <lista_inst>
    if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
      if self.instruccion():
        if self.token.cat == "PuntoComa":
          self.Avanza()
          return True
        else:
          self.Error(3, self.token)
          return False
      else:
        return False
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
      return True
    else:
      self.Error(12, self.token)
      return False
  
  def instruccion(self):
    if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
      self.Avanza()
      if self.lista_inst():
        if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
          self.Avanza()
          return True
      else:
        return False
    elif self.token.cat == "Identificador":
      return self.inst_simple()
    elif self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:
      return self.inst_es()
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "SI":
      self.Avanza()
      if self.expresion():
        if self.token.cat == "PalabraReservada" and self.token.palabra == "ENTONCES":
          self.Avanza()
          if self.instruccion():
            if self.token.cat == "PalabraReservada" and self.token.palabra == "SINO":
              return self.instruccion()
            else:
              self.Error(21, self.token)
              return False
          else:
            return False
        else:
          self.Error(18, self.token)
          return False
      else:
        return False

  def inst_simple(self):
    if self.token.cat == "Identificador":
      #<inst_simple> -> id <resto_instsimple>
      self.Avanza()
      return self.resto_instsimple()
    else:
      self.Error(2, self.token)
      return False

  def resto_instsimple(self):
    if self.token.cat == "OpAsigna":
      # <resto_instsimple> -> opasigna <expresion>
      self.Avanza()
      return self.expresion()
    elif self.token.cat == "CorcheteApertura":
      # <resto_instsimple> -> [<expr_simple>] opasigna <expresion>
      self.Avanza()
      if self.expr_simple():
        if self.token.cat == "CorcheteCierre":
          self.Avanza()
          if self.token.cat == "OpAsigna":
            self.Avanza()
            return self.expresion()
          else:
            self.Error(20, self.token)
            return False
        else:
          self.Error(15, self.token)
          return False
      else:
        return False
    elif self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
      # Siguientes
      return True
    else:
      self.Error(8, self.token)
      return False

  def expresion(self):
    return True
    
  def expr_simple(self):
    return True


    

########################################################
##
## Programa principal que lanza el analizador sintactico
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

