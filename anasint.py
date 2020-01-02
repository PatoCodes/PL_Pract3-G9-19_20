#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import errores

# Acceso a la tabla de símbolos
import tablaSimbolos as ts

# Wrapper para los atributos de los no terminales
class Atributos:
  pass

class Sintactico:
    # Constructor de la clase que implementa el Analizador Sintactico
    # Solicita el primer compnente lexico
    def __init__(self, lexico):
        self.lexico = lexico
        self.token = self.lexico.Analiza()

        # Se prepara un booleano global que indica aceptación o rechazo del programa. Por defecto, los programas se aceptan (y se rechazan cuando se encuentra un error)
        self.aceptacion = True

        # Booleano global para indicar un final de fichero inesperado. Utilizado para el tratamiento de errores
        self.finFichero = False

        # Token leido previamente. Utilizado para algunos mensajes de error
        self.tokenAnterior = None

    # Wrapper para obtener el siguiente componente léxico
    def Avanza(self):
        self.tokenAnterior = self.token
        self.token = self.lexico.Analiza()

    # Método de sincronización para tratamiento de errores en modo pánico
    # Se toman por separado las palabras reservadas
    # El método se llama siempre que existe un error
    # Las categorías y palabras reservadas se corresponden con los siguientes de la clase
    def Sincroniza(self, categoriasSiguientes, reservadasSiguientes, categoria, reservada):

        # Introducimos el elemento esperado en la lista
        if categoria != "PalabraReservada":
            categoriasSiguientes.append(categoria)
        elif categoria != None:
            reservadasSiguientes.append(reservada)

        # Nos aseguramos de que EOF esté en las categorias
        categoriasSiguientes.append("EOF")

        # Avanzamos hasta que encontramos una categoría de sincronización
        while (self.token.cat != "PalabraReservada" and self.token.cat not in categoriasSiguientes) or (self.token.cat == "PalabraReservada" and self.token.palabra not in reservadasSiguientes):
            self.Avanza()

        # Si hemos sincronizado con el elemento esperado, lo "eliminamos"
        if (self.token.cat == categoria) or (self.token.cat == "PalabraReservada" and self.token.palabra == reservada):
            self.Avanza()
        # Si hemos sincronizado con un EOF (y no era nuestra intención), intentamos emitir un mensaje de error adecuado
        elif (self.token.cat == "EOF"):
            self.Error(99, self.token)

    # Funcion que muestra los mensajes de error

    def Error(self, nerr, tok):
        # Los mensajes de error se imprimen únicamente si no se ha alcanzado un final de fichero inesperado
        self.aceptacion = False
        if not self.finFichero:

            # ERRORES SINTACTICOS (1 - 59)
            if nerr == 1:  # PROGRAMA
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba PROGRAMA en la cabecera del programa")
            elif nerr == 2:  # identificador
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un identificador")
            elif nerr == 3:  # Falta punto y coma en PROGRAMA id;
                print("Linea: " + str(tok.linea) +
                      "  ERROR: La identificacion del programa debe acabar con punto y coma")
            elif nerr == 4:  # Programa debe acabar con .
                print("Linea: " + str(tok.linea) +
                      "  ERROR: La definición del programa debe acabar con un .")
            elif nerr == 5:  # Categorías despues del final de fichero
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Componentes inesperados tras el final del programa")
            elif nerr == 6:  # decl_var
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una delaración de variable o una declaración de instrucciones")
            elif nerr == 7:  # :
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba ':' para declaración de tipo")
            elif nerr == 8:
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba ':=', una expresion entre corchetes, un SINO o un ';'")
            elif nerr == 9:  # inst_es
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un 'LEE' o un 'ESCRIBE'")
            elif nerr == 10:  # Tipo
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un tipo válido (ENTERO, REAL, BOOLEANO) o un vector")
            elif nerr == 11:  # INICIO
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba INICIO")
            elif nerr == 12:  # FIN
                print("Linea: " + str(tok.linea) + "  ERROR: Se esperaba FIN")
            elif nerr == 13:  # Inicio corchete
                print("Linea: " + str(tok.linea) + "  ERROR: Se esperaba '['")
            elif nerr == 14:  # Número para índice
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un numero como indice")
            elif nerr == 15:  # Cierre corchete
                print("Linea: " + str(tok.linea) + "  ERROR: Se esperaba ']'")
            elif nerr == 16:  # DE
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba la palabra DE para indicar el tipo de un vector")
            elif nerr == 17:  # lista_instr
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una ',' para declarar otra variable o ':' para una declaración de tipo")
            elif nerr == 18:  # ENTONCES
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un 'ENTONCES'")
            elif nerr == 19:  # TIPO VALIDO
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un tipo valido (ENTERO, REAL o BOOLEANO)")
            elif nerr == 20:
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un operador de asignación ':='")
            elif nerr == 21:  # SINO
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un 'SINO'")
            elif nerr == 22:  # Se esperaba una declaración válida de variable
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una declaración válida de variable")
            elif nerr == 23:  # Acceso erroneo a variable
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Acceso erroneo a la variable")
            elif nerr == 24:  # Expresión
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una expresión")
            elif nerr == 25:  # Instrucción
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una instrucción")
            elif nerr == 26:  # Paréntesis apertura
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un '('")
            elif nerr == 27:  # Paréntesis cierre
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un ')'")
            elif nerr == 28:  # Expr_prime
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un operador relacional, un ')', un ';', un 'HACER', un 'SINO' o un 'ENTONCES'")
            elif nerr == 29:  # Expr_simple
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un identificador, un número, un signo '+' o un '-' un '(', un 'NO', un 'CIERTO', o un 'FALSO'")
            elif nerr == 30:  # resto_exprsimple
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un signo '+' o uno '-', un ')', un ';', un 'O',un 'HACER', un 'SINO' o un 'ENTONCES'")
            elif nerr == 31:  # resto_term
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un operador de suma, multiplicación o relacional; un ')', un ';',un 'HACER', un 'SINO' o un 'ENTONCES'")
            elif nerr == 32:  # factor
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un identificador, un número, un operador un '(', un 'NO', un 'CIERTO', un 'FALSO', un 'HACER', un 'SINO' o un 'ENTONCES'")
            elif nerr == 33:  # OpSuma
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un símbolo '+' o un '-'")
            elif nerr == 34:  # HACER
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba 'HACER'")
            elif nerr == 35:  # Termino
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un identificador, un numero, un '(' o las palabras reservadas NO, CIERTO o FALSO")
            elif nerr == 36:  # Falta punto y coma en variables
                print("Linea: " + str(tok.linea) +
                      "  ERROR: La definicion de una variable debe acabar con punto y coma")
            elif nerr == 37:  # Falta punto y coma en instrucciones
                print("Linea: " + str(tok.linea) +
                      "  ERROR: La instruccion debe acabar con punto y coma")
            elif nerr == 38:  # El programa debe tener un identificador
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El programa debe incluir un identificador para nombrarlo")

            # ERRORES SEMANTICOS (60 - 98)
            elif nerr == 60:  # No se puede repetir el nombre de los componentes
                print("Linea: " + str(tok.linea) +
                      "  ERROR: No se pueden repetir identificadores declarados previamente")
            elif nerr == 61:  # Los identificadores no pueden tener nombre de palabra reservada
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Los identificadores no pueden tomar nombres de palabras reservadas")

            # ERROR EOF (99)
            elif nerr == 99:  # Final de fichero inesperado
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Final de fichero inesperado")
                # Se deshabilitan el resto de mensajes de error
                self.finFichero = True

    # No Terminal Programa
    def Programa(self):

        # <Programa> -> PROGRAMA id; <decl_var> <instrucciones>.
        if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
            self.Avanza()

            if self.token.cat == "Identificador":

                # Comprobacion semantica
                resultadoVariable = ts.añadeSimbolo(self.token.valor, "programa")
                if resultadoVariable == "invalido":
                    self.Error(61, self.tokenAnterior)
                elif resultadoVariable == "duplicado":
                    self.Error(60, self.tokenAnterior)

                self.Avanza()
            else:
                self.Error(38, self.token)
                self.Sincroniza(["PuntoComa"], [], "Identificador", None)
                if self.token.cat == "EOF":
                    return

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                self.Error(3, self.tokenAnterior)
                self.Sincroniza([], ["VAR", "INICIO"], "PuntoComa", None)
                if self.token.cat == "EOF":
                    return

            self.decl_var()

            self.instrucciones()

            if self.token.cat == "Punto":
                # FINAL DE FICHERO
                self.Avanza()
            else:
                self.Error(4, self.token)
                self.Sincroniza(["EOF"], [], "Punto", None)
                if self.token.cat == "EOF":
                    return

            if self.token.cat == "EOF":
                return
            else:
                self.Error(5, self.token)

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(1, self.token)
            self.Sincroniza(["Identificador"], [], None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
                self.Programa()

    # No Terminal Decl_Var
    def decl_var(self):

        # Siguientes y palabras reservadas
        categorias = []
        reservadas = ["INICIO"]

        # <decl_var> -> VAR <lista_id> : <tipo> ; <decl_v>
        if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":
            self.Avanza()

            self.lista_id()

            if self.token.cat == "DosPuntos":
                self.Avanza()
            else:
                self.Error(7, self.token)
                categoriasLocal = categorias[:] + []
                reservadasLocal = reservadas[:] + \
                    ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "DosPuntos", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
                    return

            self.tipo()

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                self.Error(36, self.tokenAnterior)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + []
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "PuntoComa", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
                    return

            self.decl_v()

        # Siguientes
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
            return

        # No se ha encontrado ningún primero ni siguiente, sincronizacion
        else:
            self.Error(6, self.token)
            categoriasLocal = categorias[:] + []
            reservadasLocal = reservadas[:] + ["VAR"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":
                self.decl_var()

    # No Terminal Decl_V
    def decl_v(self):

        # Siguientes y palabras reservadas
        categorias = []
        reservadas = ["INICIO"]

        if self.token.cat == "Identificador":
            # <decl_v> → <lista_id> : <tipo> ; <decl_v>
            self.lista_id()

            if self.token.cat == "DosPuntos":
                self.Avanza()
            else:
                self.Error(7, self.token)
                categoriasLocal = categorias[:] + []
                reservadasLocal = reservadas[:] + \
                    ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "DosPuntos", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
                    return

            self.tipo()

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                self.Error(36, self.tokenAnterior)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + []
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "PuntoComa", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
                    return

            self.decl_v()

        # Siguientes
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
            return

        # No se ha encontrado ningún primero ni siguiente, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + []
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.decl_v()

    # No Terminal Lista_Id
    def lista_id(self):

        # Siguientes y palabras reservadas
        categorias = ["DosPuntos"]
        reservadas = []

        # <lista_id> → id <resto_listaid>
        if self.token.cat == "Identificador":
            self.Avanza()

            self.resto_listaid()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + []
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.lista_id()

    # No Terminal Resto_Listaid
    def resto_listaid(self):

        # Siguientes y palabras reservadas
        categorias = ["DosPuntos"]
        reservadas = []

        # <resto_listaid> →  , <lista_id>
        if self.token.cat == "Coma":
            self.Avanza()

            self.lista_id()

        # Siguientes
        elif self.token.cat == "DosPuntos":
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(17, self.token)
            categoriasLocal = categorias[:] + ["Coma"]
            reservadasLocal = reservadas[:] + []
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Coma":
                self.resto_listaid()

    # No Terminal Tipo
    def tipo(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = []

        # <Tipo> → <tipo_std>
        if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
            self.tipo_std()

        # <Tipo> → VECTOR [num] DE <Tipo_std>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "VECTOR":
            self.Avanza()

            if self.token.cat == "CorcheteApertura":
                self.Avanza()
            else:
                self.Error(13, self.token)
                categoriasLocal = categorias[:] + ["Numero"]
                reservadasLocal = reservadas[:] + []
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "CorcheteApertura", None)
                if self.token.cat == "PuntoComa":
                    return

            if self.token.cat == "Numero":
                self.Avanza()
            else:
                self.Error(14, self.token)
                categoriasLocal = categorias[:] + ["CorcheteCierre"]
                reservadasLocal = reservadas[:] + []
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "Numero", None)
                if self.token.cat == "PuntoComa":
                    return

            if self.token.cat == "CorcheteCierre":
                self.Avanza()
            else:
                self.Error(15, self.token)
                categoriasLocal = categorias[:] + []
                reservadasLocal = reservadas[:] + ["DE"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "CorcheteCierre", None)
                if self.token.cat == "PuntoComa":
                    return

            if self.token.cat == "PalabraReservada" and self.token.palabra == "DE":
                self.Avanza()
            else:
                self.Error(16, self.token)
                categoriasLocal = categorias[:] + []
                reservadasLocal = reservadas[:] + \
                    ["ENTERO", "REAL", "BOOLEANO"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "DE")
                if self.token.cat == "PuntoComa":
                    return

            self.tipo_std()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(10, self.token)
            categoriasLocal = categorias[:] + []
            reservadasLocal = reservadas[:] + \
                ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]:
                self.tipo()

    # No Terminal Tipo_Std
    def tipo_std(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = []

        if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
            # <Tipo_std> → ENTERO
            # <Tipo_std> → REAL
            # <Tipo_std> → BOOLEANO
            self.Avanza()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(19, self.token)
            categoriasLocal = categorias[:]
            reservadasLocal = reservadas[:] + ["ENTERO, REAL, BOOLEANO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
                self.tipo_std()

    # No Terminal Instrucciones
    def instrucciones(self):

        # Siguientes y palabras reservadas
        categorias = ["Punto"]
        reservadas = []

        # <instrucciones> → INICIO <lista_inst> FIN
        if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
            self.Avanza()

            self.lista_inst()

            if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
                self.Avanza()
            else:
                self.Error(12, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "FIN")
                if self.token.cat == "Punto":
                    return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(11, self.token)
            categoriasLocal = categorias[:]
            reservadasLocal = reservadas[:] + ["INICIO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
                self.instrucciones()

    # No Terminal Lista_Inst
    def lista_inst(self):

        # Siguientes y palabras reservadas
        categorias = []
        reservadas = ["FIN"]

        # <lista_inst> → <instrucción> ; <lista_inst>
        if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
            self.instruccion()

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                self.Error(37, self.tokenAnterior)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "PuntoComa", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
                    return

            self.lista_inst()

        # Siguientes
        elif self.token.cat == "PalabraReservada" and self.token.palabra in reservadas:
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(12, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + \
                ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
                self.lista_inst()

    # No Terminal Instruccion
    def instruccion(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # <instrucción> → INICIO <lista_inst> FIN
        if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":
            self.Avanza()

            self.lista_inst()

            if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
                self.Avanza()
            else:
                self.Error(12, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "FIN")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

        # <instrucción> → <inst_simple>
        elif self.token.cat == "Identificador":
            self.inst_simple()

        # <instrucción> → <inst_es>
        elif self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:

            self.inst_es()

        # <instrucción> →  SI <expresion> ENTONCES <instrucción> SINO <instrucción>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "SI":
            self.Avanza()

            self.expresion()

            if self.token.cat == "PalabraReservada" and self.token.palabra == "ENTONCES":
                self.Avanza()
            else:
                self.Error(18, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "ENTONCES")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion()

            if self.token.cat == "PalabraReservada" and self.token.palabra == "SINO":
                self.Avanza()
            else:
                self.Error(21, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "SINO")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion()

        # <instrucción> → MIENTRAS <expresión> HACER <instrucción>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "MIENTRAS":
            self.Avanza()

            self.expresion()

            if self.token.cat == "PalabraReservada" and self.token.palabra == "HACER":
                self.Avanza()
            else:
                self.Error(34, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "HACER")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(25, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + \
                ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
                self.instruccion()

    # No Terminal Inst_Simple
    def inst_simple(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        if self.token.cat == "Identificador":
            # <inst_simple> -> id <resto_instsimple>
            self.Avanza()

            self.resto_instsimple()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.inst_simple()

    # No Terminal Resto_Instsimple
    def resto_instsimple(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        if self.token.cat == "OpAsigna":
            # <resto_instsimple> -> opasigna <expresion>
            self.Avanza()

            self.expresion()

        elif self.token.cat == "CorcheteApertura":
            # <resto_instsimple> -> [<expr_simple>] opasigna <expresion>
            self.Avanza()

            self.expr_simple()

            if self.token.cat == "CorcheteCierre":
                self.Avanza()
            else:
                self.Error(15, self.token)
                categoriasLocal = categorias[:] + ["OpAsigna"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "CorcheteCierre", None)
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            if self.token.cat == "OpAsigna":
                self.Avanza()
            else:
                self.Error(20, self.token)
                categoriasLocal = categorias[:] + ["Identificador",
                                                   "Numero", "ParentesisApertura", "OpSuma"]
                reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "OpAsigna", None)
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.expresion()

        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            # Siguientes
            return True

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(8, self.token)
            categoriasLocal = categorias[:] + ["OpAsigna", "CorcheteApertura"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["OpAsigna", "CorcheteApertura"]:
                self.resto_instsimple()

    # No Terminal Variable
    def variable(self):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        if self.token.cat == "Identificador":
            # <variable> -> id <resto_var>
            self.Avanza()

            self.resto_var()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.variable()

    # No Terminal Resto_Var
    def resto_var(self):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        if self.token.cat == "CorcheteApertura":
            # <resto_var> -> [<expr_simple>]
            self.Avanza()

            self.expr_simple()

            if self.token.cat == "CorcheteCierre":
                self.Avanza()
            else:
                self.Error(15, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "CorcheteCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            # Siguientes
            return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(23, self.token)
            categoriasLocal = categorias[:] + ["CorcheteApertura"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "CorcheteApertura":
                self.resto_var()

    # No Terminal Inst_Es
    def inst_es(self):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # <inst_es> → LEE(id)
        if self.token.cat == "PalabraReservada" and self.token.palabra == "LEE":
            self.Avanza()

            if self.token.cat == "ParentesisApertura":
                self.Avanza()
            else:
                self.Error(26, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisApertura", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            if self.token.cat == "Identificador":
                self.Avanza()
            else:
                self.Error(2, self.token)
                categoriasLocal = categorias[:] + ["ParentesisCierre"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "Identificador", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            if self.token.cat == "ParentesisCierre":
                self.Avanza()
            else:
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

        # <inst_es> → ESCRIBE (<expr_simple>)
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "ESCRIBE":
            self.Avanza()

            if self.token.cat == "ParentesisApertura":
                self.Avanza()
            else:
                self.Error(26, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisApertura", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            self.expr_simple()

            if self.token.cat == "ParentesisCierre":
                self.Avanza()
            else:
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(9, self.token)
            categoriasLocal = categorias[:]
            reservadasLocal = reservadas[:] + ["LEE", "ESCRIBE"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:
                self.inst_es()

    # No Terminal Expresion
    def expresion(self):

        # Siguientes y palabras reservadas
        categorias = ["ParentesisCierre", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # <expresión> → <expr_simple> <expresiónPrime>
        if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
            self.expr_simple()

            self.expresionPrime()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(24, self.token)
            categoriasLocal = categorias[:] + ["Identificador",
                                               "Numero", "OpSuma", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.expresion()

    # No Terminal ExpresionPrime
    def expresionPrime(self):

        # Siguientes y palabras reservadas
        categorias = ["ParentesisCierre", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # <expresiónPrime> → oprel <expr_simple>
        if self.token.cat == "OpRelacional":
            self.Avanza()

            self.expr_simple()

        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            return True

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(28, self.token)
            categoriasLocal = categorias[:] + ["OpRelacional"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpRelacional":
                self.expresionPrime()

    # No Terminal Expr_Simple
    def expr_simple(self):

        # Siguientes y palabras reservadas
        categorias = ["CorcheteCierre", "ParentesisCierre",
                      "OpRelacional", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # <expr_simple> → <término> <resto_exsimple>
        if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):

            self.termino()

            self.restoexpr_simple()

        # <expr_simple> → <signo> <término> <resto_exsimple>
        elif self.token.cat == "OpSuma":

            self.signo()

            self.termino()

            self.restoexpr_simple()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(29, self.token)
            categoriasLocal = categorias[:] + ["Identificador",
                                               "Numero", "ParentesisApertura", "OpSuma"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura", "OpSuma"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.expr_simple()

    # No Terminal Restoexpr_Simple
    def restoexpr_simple(self):

        # Siguientes y palabras reservadas
        categorias = ["CorcheteCierre", "ParentesisCierre",
                      "OpRelacional", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # <resto_exsimple> → opsuma <término> <resto_exsimple>
        if self.token.cat == "OpSuma":
            self.Avanza()

            self.termino()

            self.restoexpr_simple()

        #	<resto_exsimple> → O <término> <resto_exsimple>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "O":
            self.Avanza()

            self.termino()

            self.restoexpr_simple()

        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(30, self.token)
            categoriasLocal = categorias[:] + ["OpSuma"]
            reservadasLocal = reservadas[:] + ["O"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpSuma" or (self.token.cat == "PalabraReservada" and self.token.palabra == "O"):
                self.restoexpr_simple()

    # No Terminal Termino
    def termino(self):

        # Siguientes y palabras reservadas
        categorias = ["OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["O", "HACER", "SINO", "ENTONCES"]

        # <término> → <factor> <resto_term>
        if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
            self.factor()

            self.resto_term()

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(35, self.token)
            categoriasLocal = categorias[:] + \
                ["Identificador", "Numero", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat in "PalabraReservada" and self.token.palabra == ["NO", "CIERTO", "FALSO"]):
                self.termino()

    # No Terminal Resto_Term
    def resto_term(self):

        # Siguientes y palabras reservadas
        categorias = ["OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["O", "HACER", "SINO", "ENTONCES"]

        # <resto_term> → opmult <factor> <resto_term>
        if self.token.cat == "OpMultiplicacion":
            self.Avanza()

            self.factor()

            self.resto_term()

        # <resto_term> → Y <factor> <resto_term>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "Y":
            self.Avanza()

            self.factor()

            self.resto_term()

        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(31, self.tokenAnterior)
            categoriasLocal = categorias[:] + ["OpMultiplicacion"]
            reservadasLocal = reservadas[:] + ["Y"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpMultiplicacion" or (self.token.cat == "PalabraReservada" and self.token.palabra == "Y"):
                self.resto_term()

    # No Terminal Factor
    def factor(self):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        #	<factor> → <variable>
        if self.token.cat == "Identificador":
            self.variable()

        # <factor> → num
        elif self.token.cat == "Numero":
            self.Avanza()

        # <factor> → ( <expresión> )
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()

            self.expresion()

            if self.token.cat == "ParentesisCierre":
                self.Avanza()
            else:
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

        # <factor> → NO <factor>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "NO":
            self.Avanza()

            self.factor()
        # <factor> → CIERTO
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "CIERTO":
            self.Avanza()

        # <factor> → FALSO
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "FALSO":
            self.Avanza()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(32, self.token)
            categoriasLocal = categorias[:] + \
                ["Identificador", "Numero", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.factor()

    # No Terminal Signo
    def signo(self):

        # Siguientes y palabras reservadas
        categorias = ["Identificador", "Numero", "ParentesisApertura"]
        reservadas = ["NO", "CIERTO", "FALSO"]

        # <signo> → +
        # <signo> → -
        if self.token.cat == "OpSuma":
            self.Avanza()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(33, self.token)
            categoriasLocal = categorias[:] + ["OpSuma"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpSuma":
                self.factor()


########################################################
#
# Programa principal que lanza el analizador sintactico
#
########################################################
if __name__ == "__main__":
    script, filename = argv
    txt = open(filename)
    print("Este es tu fichero %r" % filename)
    i = 0
    fl = flujo.Flujo(txt)
    anlex = analex.Analex(fl)
    S = Sintactico(anlex)
    S.Programa()
    if S.aceptacion:
        print("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
        print("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")
