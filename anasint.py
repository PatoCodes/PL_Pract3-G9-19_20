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
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba PROGRAMA en la cabecera del programa")
    elif nerr == 2: #identificador
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un identificador")
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
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba ':=', una expresion entre corchetes, un SINO o un ';'")
    elif nerr == 9: #inst_es
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un 'LEE' o un 'ESCRIBE'")
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
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba la palabra DE para indicar el tipo de un vector")
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
    elif nerr == 22: #Se esperaba una declaración válida de variable
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una declaración válida de variable")
    elif nerr == 23: #SINO
      print ("Linea: " + str(self.token.linea) + "  ERROR: Acceso inconsistente a variable")
    elif nerr == 24: #Expresión
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una expresión")
    elif nerr == 25: #Instrucción
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba una instrucción")
    elif nerr == 26: #Paréntesis apertura
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un '('")
    elif nerr == 27: #Paréntesis cierre
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un ')'")
    elif nerr == 28: #Expr_prime
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un operador relacional, un ')', un ';', un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 29: #Expr_simple
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un identificador, un número, un signo '+' o un '-' un '(', un 'NO', un 'CIERTO', o un 'FALSO'")
    elif nerr == 30: #resto_exprsimple
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un signo '+' o uno '-', un ')', un ';', un 'O',un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 31: #resto_term
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un operador de suma, multiplicación o relacional, un ')', un ';',un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 32: #factor
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un identificador, un número, un operador un '(', un 'NO', un 'CIERTO', un 'FALSO', un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 33: #OpSuma
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un símbolo '+' o un '-')



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
    # <instrucción> → INICIO <lista_inst> FIN
    if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
      self.Avanza()
      if self.lista_inst():
        if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
          self.Avanza()
          return True
      else:
        return False
    # <instrucción> → <inst_simple>	
    elif self.token.cat == "Identificador":
      return self.inst_simple()
    # <instrucción> → <inst_es>	
    elif self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:
      return self.inst_es()
    # <instrucción> →  SI <expresion> ENTONCES <instrucción> SINO <instrucción>
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
    else:
      self.Error(25, self.token)
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

  def variable(self):
    if self.token.cat == "Identificador":
      # <variable> -> id <resto_var>
      self.Avanza()
      return self.resto_var()
    else:
      self.Error(22, self.token)
      return False

  def resto_var(self):
    if self.token.cat == "CorcheteApertura":
      # <resto_var> -> [<expr_simple>]
      self.Avanza()
      if self.expr_simple():
        if self.token.cat == "CorcheteCierre":
          self.Avanza()
          return True
        else:
          self.Error(15, self.token)
          return False
      else:
        return False
    elif self.token.cat in ["OpMultiplicacion","OpSuma","CorcheteCierre","ParentesisCierre", "OpRelacional", "PuntoComa"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["Y","O","HACER","SINO","ENTONCES"]):
      # SIGUIENTES
      return True
    else:
      self.Error(23, self.token)
      return False

  def inst_es(self):
    # <inst_es> → LEE(id)
    if self.token.cat == "PalabraReservada" and self.token.palabra == "LEE":
      self.Avanza()
      if self.token.cat == "ParentesisApertura":
        self.Avanza()
        if self.token.cat == "Identificador":
          self.Avanza()
          if self.token.cat == "ParentesisApertura":
            self.Avanza()
            return True
          else:
            self.Error(27, self.token)
            return False
        else:
          self.Error(2, self.token)
          return False
      else:
        self.Error(26, self.token)
        return False
    # <inst_es> → ESCRIBE ( <expr_simple>)	
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "ESCRIBE":
      self.Avanza()
      if self.token.cat == "ParentesisApertura":
        self.Avanza()
        if self.expr_simple():
          if self.token.cat == "ParentesisApertura":
            self.Avanza()
            return True
          else:
            self.Error(27, self.token)
            return False
        else:
          self.Error(2, self.token)
          return False
      else:
        self.Error(26, self.token)
        return False
    else:
      self.Error(9, self.token)  
      return False

  def expresion(self):
    # <expresión> → <expr_simple> <expresiónPrime> 
    if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
      if self.expr_simple():
        return self.expresionPrime()
      else:
        return False
    else:
      self.Error(24, self.token)
      return

  def expresionPrime(self):
    # <expresiónPrime> → oprel <expr_simple>	
    if self.token.cat == "OpRelacional":
      self.Avanza()
      return self.expr_simple()
    # <expresiónPrime> → λ
    elif self.token.cat in ["ParentesisCierre", "PuntoComa"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["HACER", "SINO", "ENTONCES"]):
      return True
    else:
      self.Error(28, self.token)
      return False
    
    
  def expr_simple(self):
    # <expr_simple> → <término> <resto_exsimple>
    if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
      if self.termino():
        return self.restoexpr_simple()
      else:
        return False
    # <expr_simple> → <signo> <término> <resto_exsimple>		
    elif self.token.cat == "OpSuma":
      if self.signo():
        if self.termino():
          return self.restoexpr_simple()
        else:
          return False
      else:
        return False
    else:
      self.Error(29, self.token)
      return False
  
  def restoexpr_simple(self):
    # <resto_exsimple> → opsuma <término> <resto_exsimple>
    if self.token.cat == "OpSuma":
      self.Avanza()
      if self.termino():
        return self.restoexpr_simple()
      else:
        return False
    #	<resto_exsimple> → O <término> <resto_exsimple>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "O":
      self.Avanza()
      if self.termino():
        return self.restoexpr_simple()
      else:
        return False
    elif self.token.cat in ["ParentesisCierre", "CorcheteCierre", "OpRelacional", "PuntoComa"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["HACER", "SINO", "ENTONCES"]):
      return True
    else:
      self.Error(30, self.token)
      return False


  def termino(self):
    # <término> → <factor> <resto_term>	
    if self.factor():
      return self.resto_term()
    else:
      return False
  
  def resto_term(self):
    # <resto_term> → opmult <factor> <resto_term>
    if self.token.cat == "OpMultiplicacion":
      self.Avanza()
      if self.factor():
        return self.resto_term()
      else:
        return False
    # <resto_term> → Y <factor> <resto_term>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "Y":
      if self.factor():
        return self.resto_term()
      else:
        return False
    # <resto_term> → λ	
    elif self.token.cat in ["ParentesisCierre", "CorcheteCierre", "OpRelacional", "PuntoComa", "OpSuma"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["HACER", "SINO", "ENTONCES", "O"]):
      return True
    else:
      self.Error(31, self.token)
      return False


  def factor(self):
    #	<factor> → <variable>
    if self.token.cat == "Identificador":
      return self.variable()
    # <factor> → num
    elif self.token.cat == "Numero":
      self.Avanza()
      return True
    #	<factor> → ( <expresión> )
    elif self.token.cat == "ParentesisApertura":
      self.Avanza
      if self.expresion():
        if self.token.cat == "ParentesisCierre":
          self.Avanza()
          return True
        else:
          self.Error(27, self.token)
          return False
      else:
        return False
    # <factor> → NO <factor>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "NO":
      self.Avanza()
      return self.factor()
    # <factor> → CIERTO
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "CIERTO":
      self.Avanza()
      return True
    # <factor> → FALSO
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "FALSE":
      self.Avanza()
      return True
    else:
      self.Error(32, self.token)
      return False


  def signo(self):
    # <signo> → +
    # <signo> → -
    if self.token.cat == "OpSuma":
      self.Avanza()
      return True
    else:
      self.Error(33, self.token)
      return False


    

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

