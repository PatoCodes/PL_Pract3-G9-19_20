#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import errores


class Sintactico:
  # Constructor de la clase que implementa el Analizador Sintactico
  # Solicita el primer compnente lexico 
  def __init__(self, lexico):
    self.lexico= lexico
    self.token=self.lexico.Analiza()

  # Wrapper para obtener el siguiente componente léxico
  def Avanza(self):
    self.token=self.lexico.Analiza()

  # Método de sincronización para tratamiento de errores en modo pánico
  # Se toman por separado las palabras reservadas 
  # El método se llama siempre que existe un error
  # Las categorías y palabras reservadas se corresponden con los siguientes de la clase
  def Sincroniza(self, categorias, reservadas):
    
    # Nos aseguramos de que EOF esté en las categorias
    categorias.append("EOF")

    # Avanzamos hasta que encontramos una categoría de sincronización
    while self.token.cat not in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra not in reservadas):
      self.Avanza()


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
    elif nerr == 23: #Acceso erroneo a variable
      print ("Linea: " + str(self.token.linea) + "  ERROR: Acceso erroneo a la variable")
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
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un operador de suma, multiplicación o relacional; un ')', un ';',un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 32: #factor
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un identificador, un número, un operador un '(', un 'NO', un 'CIERTO', un 'FALSO', un 'HACER', un 'SINO' o un 'ENTONCES'")
    elif nerr == 33: #OpSuma
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba un símbolo '+' o un '-'")
    elif nerr == 34: #HACER
      print ("Linea: " + str(self.token.linea) + "  ERROR: Se esperaba 'HACER'")


  # No Terminal Programa
  def Programa(self):

    # Siguientes y palabras reservadas
    categorias = []
    reservadas = []

    # Aceptacion
    aceptacion = True

    if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
      #<Programa> -> PROGRAMA id; <decl_var> <instrucciones>.
      self.Avanza()
      if self.token.cat == "Identificador":
        self.Avanza()
        if self.token.cat == "PuntoComa":
          self.Avanza()
          aceptacion = aceptacion and self.decl_var()
          aceptacion = aceptacion and self.instrucciones()
          if self.token.cat == "Punto":
            #FINAL DE FICHERO
            self.Avanza()
            if self.token.cat == "EOF":
              return aceptacion
            else:
              self.Error(5, self.token)
              self.Sincroniza(categorias, reservadas)
              return False
          else:
            self.Error(4, self.token)
            self.Sincroniza(categorias, reservadas)
            return False
        else:
          self.Error(3, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(2, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      self.Error(1, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Decl_Var  
  def decl_var(self):
    
    # Siguientes y palabras reservadas
    categorias = []
    reservadas = ["INICIO"]

    # Aceptacion
    aceptacion = True

    # <decl_var> -> VAR <lista_id> : <tipo> ; <decl_v>
    if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":
      self.Avanza()
      aceptacion = aceptacion and self.lista_id()
      if self.token.cat == "DosPuntos":
        self.Avanza()
        aceptacion = aceptacion and self.tipo()
        if self.token.cat == "PuntoComa":
          self.Avanza()
          return aceptacion and self.decl_v()  
        else:
          self.Error(3, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(7, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      if self.token.cat == "PalabraReservada" and self.token.palabra in reservadas:
        # Siguientes
        return True
      else:
        self.Error(6, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
  

  # No Terminal Decl_V
  def decl_v(self):

    # Siguientes y palabras reservadas
    categorias = []
    reservadas = ["INICIO"]

    # Aceptacion
    aceptacion = True

    if self.token.cat == "Identificador":
      #<decl_v> → <lista_id> : <tipo> ; <decl_v>
      aceptacion = aceptacion and self.lista_id()
      if self.token.cat == "DosPuntos":
        self.Avanza()
        aceptacion = aceptacion and self.tipo()
        if self.token.cat == "PuntoComa":
          self.Avanza()
          return aceptacion and self.decl_v()
        else:
          self.Error(3, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(7, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    elif self.token.cat == "PalabraReservada" and self.token.palabra in reservadas:
      #Siguientes
      return True
    else:
      self.Error(2, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Lista_Id
  def lista_id(self):

    # Siguientes y palabras reservadas
    categorias = ["DosPuntos"]
    reservadas = []

    #<lista_id> → id <resto_listaid>
    if self.token.cat == "Identificador":
      self.Avanza()
      return self.resto_listaid()
    else:
      self.Error(2, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Resto_Listaid
  def resto_listaid(self):

    # Siguientes y palabras reservadas
    categorias = ["DosPuntos"]
    reservadas = []
    
    #<resto_listaid> →  , <lista_id>
    if self.token.cat == "Coma":
      self.Avanza()
      return self.lista_id()
    # Siguientes
    elif self.token.cat in categorias:
      return True
    else:
      self.Error(17, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Tipo
  def tipo(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = []
    
    if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
      #<Tipo> → <tipo_std>
      return self.tipo_std()	
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
              self.Sincroniza(categorias, reservadas)
              return False
          else:
            self.Error(15, self.token)
            self.Sincroniza(categorias, reservadas)
            return False
        else:
          self.Error(14, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(13, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      self.Error(10, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Tipo_Std
  def tipo_std(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = []
    
    if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO","REAL","BOOLEANO"]:
      #<Tipo_std> → ENTERO
      #<Tipo_std> → REAL
      #<Tipo_std> → BOOLEANO
      self.Avanza()
      return True
    else:
      self.Error(19, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Instrucciones
  def instrucciones(self):

    # Siguientes y palabras reservadas
    categorias = ["Punto"]
    reservadas = []

    # Aceptacion
    aceptacion = True
    
    #<instrucciones> → INICIO <lista_inst> FIN
    if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
      self.Avanza()
      aceptacion = aceptacion and self.lista_inst()
      if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
        self.Avanza()            
        return aceptacion
      else:
        self.Error(12, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      self.Error(11, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Lista_Inst
  def lista_inst(self):

    # Siguientes y palabras reservadas
    categorias = []
    reservadas = ["FIN"]

    # Aceptacion
    aceptacion = True
    
    # <lista_inst> → <instrucción> ; <lista_inst>
    if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
      aceptacion = aceptacion and self.instruccion()
      if self.token.cat == "PuntoComa":
        self.Avanza()
        return aceptacion and self.lista_inst()
      else:
        self.Error(3, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    # Siguientes
    elif self.token.cat == "PalabraReservada" and self.token.palabra in reservadas:
      return True
    else:
      self.Error(12, self.token)
      self.Sincroniza(categorias, reservadas)
      return False
  

  # No Terminal Instruccion
  def instruccion(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = ["SINO"]

    # Aceptacion
    aceptacion = True
    
    # <instrucción> → INICIO <lista_inst> FIN
    if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
      self.Avanza()
      aceptacion = aceptacion and self.lista_inst()
      if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
        self.Avanza()
        return aceptacion
      else:
        self.Error(12, self.token)
        self.Sincroniza(categorias, reservadas)
    # <instrucción> → <inst_simple>	
    elif self.token.cat == "Identificador":
      return self.inst_simple()
    # <instrucción> → <inst_es>	
    elif self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:
      return self.inst_es()
    # <instrucción> →  SI <expresion> ENTONCES <instrucción> SINO <instrucción>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "SI":
      self.Avanza()
      aceptacion = aceptacion and self.expresion()
      if self.token.cat == "PalabraReservada" and self.token.palabra == "ENTONCES":
        self.Avanza()
        aceptacion = aceptacion and self.instruccion()
        if self.token.cat == "PalabraReservada" and self.token.palabra == "SINO":
          self.Avanza()
          return aceptacion and self.instruccion()
        else:
          self.Error(21, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(18, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    # <instrucción> →  MIENTRAS <expresión> HACER <instrucción>	
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "MIENTRAS":
      self.Avanza()
      aceptacion = aceptacion and self.expresion()
      if self.token.cat == "PalabraReservada" and self.token.palabra == "HACER":
        self.Avanza()
        return aceptacion and self.instruccion()
      else:
        self.Error(34, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      self.Error(25, self.token)
      self.Sincroniza(categorias, reservadas)
      return False
    

  # No Terminal Inst_Simple
  def inst_simple(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = ["SINO"]
    
    if self.token.cat == "Identificador":
      #<inst_simple> -> id <resto_instsimple>
      self.Avanza()
      return self.resto_instsimple()
    else:
      self.Error(2, self.token)
      self.Sincroniza(categorias, reservadas)
      return False

  # No Terminal Resto_Instsimple
  def resto_instsimple(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = ["SINO"]

    # Aceptacion
    aceptacion = True
    
    if self.token.cat == "OpAsigna":
      # <resto_instsimple> -> opasigna <expresion>
      self.Avanza()
      return self.expresion()
    elif self.token.cat == "CorcheteApertura":
      # <resto_instsimple> -> [<expr_simple>] opasigna <expresion>
      self.Avanza()
      aceptacion = aceptacion and self.expr_simple()
      if self.token.cat == "CorcheteCierre":
        self.Avanza()
        if self.token.cat == "OpAsigna":
          self.Avanza()
          return aceptacion and self.expresion()
        else:
          self.Error(20, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(15, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
      # Siguientes
      return True
    else:
      self.Error(8, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Variable
  def variable(self):

    # Siguientes y palabras reservadas
    categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre", "ParentesisCierre","OpRelacional", "PuntoComa"]
    reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]
    
    if self.token.cat == "Identificador":
      # <variable> -> id <resto_var>
      self.Avanza()
      return self.resto_var()
    else:
      self.Error(22, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Resto_Var
  def resto_var(self):

    # Siguientes y palabras reservadas
    categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre", "ParentesisCierre","OpRelacional", "PuntoComa"]
    reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    if self.token.cat == "CorcheteApertura":
      # <resto_var> -> [<expr_simple>]
      self.Avanza()
      aceptacion = aceptacion and self.expr_simple()
      if self.token.cat == "CorcheteCierre":
        self.Avanza()
        return aceptacion
      else:
        self.Error(15, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
      # SIGUIENTES
      return True
    else:
      self.Error(23, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Inst_Es
  def inst_es(self):

    # Siguientes y palabras reservadas
    categorias = ["PuntoComa"]
    reservadas = ["SINO"]

    # Aceptacion
    aceptacion = True
    
    # <inst_es> → LEE(id)
    if self.token.cat == "PalabraReservada" and self.token.palabra == "LEE":
      self.Avanza()
      if self.token.cat == "ParentesisApertura":
        self.Avanza()
        if self.token.cat == "Identificador":
          self.Avanza()
          if self.token.cat == "ParentesisCierre":
            self.Avanza()
            return True
          else:
            self.Error(27, self.token)
            self.Sincroniza(categorias, reservadas)
            return False
        else:
          self.Error(2, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(26, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    # <inst_es> → ESCRIBE (<expr_simple>)	
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "ESCRIBE":
      self.Avanza()
      if self.token.cat == "ParentesisApertura":
        self.Avanza()
        aceptacion = aceptacion and self.expr_simple()
        if self.token.cat == "ParentesisCierre":
          self.Avanza()
          return aceptacion
        else:     
          self.Error(27, self.token)
          self.Sincroniza(categorias, reservadas)
          return False
      else:
        self.Error(26, self.token)
        self.Sincroniza(categorias, reservadas)
        return False
    else:
      self.Error(9, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Expresion
  def expresion(self):

    # Siguientes y palabras reservadas
    categorias = ["ParentesisCierre", "PuntoComa"]
    reservadas = ["HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    # <expresión> → <expr_simple> <expresiónPrime> 
    if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
      aceptacion = aceptacion and self.expr_simple()
      return aceptacion and self.expresionPrime()
    else:
      self.Error(24, self.token)
      self.Sincroniza(categorias, reservadas)
      return


  # No Terminal ExpresionPrime
  def expresionPrime(self):

    # Siguientes y palabras reservadas
    categorias = ["ParentesisCierre", "PuntoComa"]
    reservadas = ["HACER", "SINO", "ENTONCES"]
    
    # <expresiónPrime> → oprel <expr_simple>
    if self.token.cat == "OpRelacional":
      self.Avanza()
      return self.expr_simple()
    # <expresiónPrime> → λ
    elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
      return True
    else:
      self.Error(28, self.token)
      self.Sincroniza(categorias, reservadas)
      return False
    

  # No Terminal Expr_Simple
  def expr_simple(self):

    # Siguientes y palabras reservadas
    categorias = ["CorcheteCierre", "ParentesisCierre", "OpRelacional", "PuntoComa"]
    reservadas = ["HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    # <expr_simple> → <término> <resto_exsimple>
    if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
      aceptacion = aceptacion and self.termino()
      return aceptacion and self.restoexpr_simple()
    # <expr_simple> → <signo> <término> <resto_exsimple>		
    elif self.token.cat == "OpSuma":
      aceptacion = aceptacion and self.signo()
      aceptacion = aceptacion and self.termino()
      return aceptacion and self.restoexpr_simple()
    else:
      self.Error(29, self.token)
      self.Sincroniza(categorias, reservadas)
      return False
  

  # No Terminal Restoexpr_Simple
  def restoexpr_simple(self):

    # Siguientes y palabras reservadas
    categorias = ["CorcheteCierre", "ParentesisCierre", "OpRelacional", "PuntoComa"]
    reservadas = ["HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    # <resto_exsimple> → opsuma <término> <resto_exsimple>
    if self.token.cat == "OpSuma":
      self.Avanza()
      aceptacion = aceptacion and self.termino()
      return aceptacion and self.restoexpr_simple()
    #	<resto_exsimple> → O <término> <resto_exsimple>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "O":
      self.Avanza()
      aceptacion = aceptacion and self.termino()
      return aceptacion and self.restoexpr_simple()
    elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
      return True
    else:
      self.Error(30, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Termino
  def termino(self):

    # Aceptacion
    aceptacion = True
    
    # <término> → <factor> <resto_term>
    if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
      aceptacion = aceptacion and self.factor()
      return aceptacion and self.resto_term()
    else:
      return False
  

  # No Terminal Resto_Term
  def resto_term(self):

    # Siguientes y palabras reservadas
    categorias = ["OpSuma", "CorcheteCierre", "ParentesisCierre", "OpRelacional", "PuntoComa"]
    reservadas = ["O", "HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    # <resto_term> → opmult <factor> <resto_term>
    if self.token.cat == "OpMultiplicacion":
      self.Avanza()
      aceptacion = aceptacion and self.factor()
      return aceptacion and self.resto_term()
    # <resto_term> → Y <factor> <resto_term>
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "Y":
      self.Avanza()
      aceptacion = aceptacion and self.factor()
      return aceptacion and self.resto_term()
    # <resto_term> → λ	
    elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
      return True
    else:
      self.Error(31, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Factor
  def factor(self):

    # Siguientes y palabras reservadas
    categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre", "ParentesisCierre", "OpRelacional", "PuntoComa"]
    reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

    # Aceptacion
    aceptacion = True
    
    #	<factor> → <variable>
    if self.token.cat == "Identificador":
      return self.variable()
    # <factor> → num
    elif self.token.cat == "Numero":
      self.Avanza()
      return True
    # <factor> → ( <expresión> )
    elif self.token.cat == "ParentesisApertura":
      self.Avanza()
      aceptacion = aceptacion and self.expresion()
      if self.token.cat == "ParentesisCierre":
        self.Avanza()
        return aceptacion
      else:
        self.Error(27, self.token)
        self.Sincroniza(categorias, reservadas)
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
    elif self.token.cat == "PalabraReservada" and self.token.palabra == "FALSO":
      self.Avanza()
      return True
    else:
      self.Error(32, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


  # No Terminal Signo
  def signo(self):

    # Siguientes y palabras reservadas
    categorias = ["Identificador", "Numero", "ParentesisApertura"]
    reservadas = ["NO", "CIERTO", "FALSO"]
    
    # <signo> → +
    # <signo> → -
    if self.token.cat == "OpSuma":
      self.Avanza()
      return True
    else:
      self.Error(33, self.token)
      self.Sincroniza(categorias, reservadas)
      return False


########################################################
#
# Programa principal que lanza el analizador sintactico
#
########################################################
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

