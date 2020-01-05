#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import errores
import copy

# Acceso a la tabla de símbolos
import tablaSimbolos as ts

# AST
import AST as ast

# Wrapper para los atributos de los no terminales
class Atributos:
  at = {}
  
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

    # Funcion para comprobar e imprimir automaticamente los errores de un nodo del AST
    # Devuelve TRUE si no ha habido errores, FALSE si ha habido errores
    def comprobacionSemanticaAST(self, nodo):

        # Como error espera un token, se crea un token "falso" para pasarselo con la linea
        token = componentes.Punto(nodo.linea)

        # Comprobamos uno a uno los errores para imprimir el mensaje apropiado
        for error in nodo.errores:
            if error == "asignacion_invalida":
                self.Error(72, token)
            elif error == "condicion_no_logica":
                self.Error(71, token)
            elif error == "clase_erronea_lee":
                self.Error(64, token)
            elif error == "tipo_erroneo_comp":
                self.Error(65, token)
            elif error == "tipo_erroneo_arit":
                self.Error(66, token)
            elif error == "sin_declarar":
                self.Error(67, token, id = nodo.var)
            elif error == "clase_erronea_var":
                self.Error(68, token, id = nodo.var)
            elif error == "clase_erronea_vect":
                self.Error(69, token, id = nodo.var)
            elif error == "tipo_erroneo_log":
                self.Error(70, token)
            
        # Devolvemos valor adecuado
        return len(nodo.errores) == 0


    # Funcion que muestra los mensajes de error
    def Error(self, nerr, tok, **opcional):
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
                      "  ERROR: Se esperaba una declaración de variable o una declaración de instrucciones")
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
                      "  ERROR: Se esperaba un numero valido como indice")
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
                      "  ERROR: El identificador " + str(opcional["id"]) + " ya ha sido declarado previamente")
            elif nerr == 61:  # Los identificadores no pueden tener nombre de palabra reservada
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El identificador " + str(opcional["id"]) + " esta tomando un valor prohibido (los identificadores no pueden tomar valores de palabras reservadas)")
            elif nerr == 62:  # Los indices de un vector deben ser numeros enteros
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El tamaño del vector debe ser un numero entero")
            elif nerr == 63:  # Los vectores no pueden tener tamaño negativo
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El tamaño del vector no puede ser cero")
            elif nerr == 64:  # Se intenta leer una variable no simple
                print("Linea: " + str(tok.linea) +
                      "  ERROR: La instruccion LEE solo permite utilizar variables simples (no se permiten vectores)")
            elif nerr == 65:  # Hay booleanos en una comparacion
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Las comparaciones deben ser realizadas entre expresiones numericas")
            elif nerr == 66:  # Hay booleanos en una operacion aritmetica
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Las operaciones aritmeticas no pueden contener valores de tipo logico")
            elif nerr == 67:  # Se intenta acceder a una variable no declarada
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El identificador " + str(opcional["id"]) + " no ha sido declarado previamente")
            elif nerr == 68:  # Se esperaba una variable simple
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una variable simple, el identificador " + str(opcional["id"]) + " no lo es")
            elif nerr == 69:  # Se esperaba un vector
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba un vector, el identificador " + str(opcional["id"]) + " no lo es")
            elif nerr == 70:  # Hay numeros en una operacion logica
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Las operaciones logicas solo pueden contener valores logicos")
            elif nerr == 71:  # La condicion debe ser de tipo logico
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Se esperaba una condicion de tipo logico")
            elif nerr == 72:  # El tipo de la variable no concuerda con el de la asignacion
                print("Linea: " + str(tok.linea) +
                      "  ERROR: El valor que se intenta asignar a la variable no es compatible con el tipo de la variable")
                      


            # ERROR EOF (99)
            elif nerr == 99:  # Final de fichero inesperado
                print("Linea: " + str(tok.linea) +
                      "  ERROR: Final de fichero inesperado")
                # Se deshabilitan el resto de mensajes de error
                self.finFichero = True

    # No Terminal Programa
    def Programa(self, Programa):

        # Atributos de los no terminales
        Instrucciones = Atributos()

        # Arbol (por defecto asumimos arbol con error)
        Programa.at["arbol"] = ast.NodoVacio(1)

        # Variable para comprobar errores durante la construccion (de cara a generar el arbol)
        error = False

        # <Programa> -> PROGRAMA id; <decl_var> <instrucciones>.
        if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
            self.Avanza()

            if self.token.cat == "Identificador":

                # Comprobacion semantica (nombre del identificador)
                resultadoVariable = ts.anadeSimbolo(self.token.valor, "programa")
                if resultadoVariable == "invalido":
                    self.Error(61, self.tokenAnterior)
                    error = True
                elif resultadoVariable == "duplicado":
                    self.Error(60, self.tokenAnterior)
                    error = True
                else:
                    ts.actualizaInfo(self.token.valor, "clase", "programa")

                self.Avanza()
            else:
                error = True
                self.Error(38, self.token)
                self.Sincroniza(["PuntoComa"], [], "Identificador", None)
                if self.token.cat == "EOF":
                    return

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                error = True
                self.Error(3, self.tokenAnterior)
                self.Sincroniza([], ["VAR", "INICIO"], "PuntoComa", None)
                if self.token.cat == "EOF":
                    return

            self.decl_var()

            self.instrucciones(Instrucciones)

            if self.token.cat == "Punto":
                # FINAL DE FICHERO

                # Comprobamos errores en la produccion
                if not error:
                    # Construccion
                    Programa.at["arbol"] = Instrucciones.at["arbol"]

                self.Avanza()
            else:
                self.Error(4, self.token)
                self.Sincroniza(["EOF"], [], "Punto", None)
                if self.token.cat == "EOF":
                    return

            if self.token.cat != "EOF":
                self.Error(5, self.token)

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(1, self.token)
            self.Sincroniza(["Identificador"], [], None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra == "PROGRAMA":
                self.Programa(copy.deepcopy(Programa))

    # No Terminal Decl_Var
    def decl_var(self):

        # Siguientes y palabras reservadas
        categorias = []
        reservadas = ["INICIO"]

        # Atributos de los no terminales
        Lista_id = Atributos()
        Tipo = Atributos()

        # <decl_var> -> VAR <lista_id> : <tipo> ; <decl_v>
        if self.token.cat == "PalabraReservada" and self.token.palabra == "VAR":

            self.Avanza()

            self.lista_id(Lista_id)

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

            self.tipo(Tipo)

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

            # Comprobaciones semanticas (declaraciones de las variables)

            for v in Lista_id.at["lista"]:
                # Comprobacion semantica (nombre del identificador)
                resultadoVariable = ts.anadeSimbolo(v, Tipo.at["t"])
                if resultadoVariable == "invalido":
                    self.Error(61, self.tokenAnterior, id = v)
                elif resultadoVariable == "duplicado":
                    self.Error(60, self.tokenAnterior, id = v)
                else:
                    ts.actualizaInfo(v, "clase", Tipo.at["clase"])
                    # Si es un vector, se añade el tamaño
                    if Tipo.at["clase"] == "vector":
                        ts.actualizaInfo(v, "longitud", Tipo.at["longitud"])

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

        # Atributos de los no terminales
        Lista_id = Atributos()
        Tipo = Atributos()

        if self.token.cat == "Identificador":
            # <decl_v> → <lista_id> : <tipo> ; <decl_v>
            self.lista_id(Lista_id)

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

            self.tipo(Tipo)

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

            # Comprobaciones semanticas (declaraciones de las variables)
            for v in Lista_id.at["lista"]:
                # Comprobacion semantica (nombre del identificador)
                resultadoVariable = ts.anadeSimbolo(v, Tipo.at["t"])
                if resultadoVariable == "invalido":
                    self.Error(61, self.tokenAnterior, id = v)
                elif resultadoVariable == "duplicado":
                    self.Error(60, self.tokenAnterior, id = v)
                else:
                    ts.actualizaInfo(v, "clase", Tipo.at["clase"])
                    # Si es un vector, se añade el tamaño
                    if Tipo.at["clase"] == "vector":
                        ts.actualizaInfo(v, "longitud", Tipo.at["longitud"])

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
    def lista_id(self, Lista_id):

        # Siguientes y palabras reservadas
        categorias = ["DosPuntos"]
        reservadas = []

        # Atributos de los no terminales
        Resto_listaid = Atributos()

        # <lista_id> → id <resto_listaid>
        if self.token.cat == "Identificador":

            # Comprobaciones semanticas
            id = self.token.valor

            self.Avanza()

            self.resto_listaid(Resto_listaid)

            # Comprobaciones semanticas
            Lista_id.at["lista"] = [id] + Resto_listaid.at["lista"]

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + []
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.lista_id(Lista_id)

    # No Terminal Resto_Listaid
    def resto_listaid(self, Resto_listaid):

        # Siguientes y palabras reservadas
        categorias = ["DosPuntos"]
        reservadas = []

        # Atributos de los no terminales
        Lista_id = Atributos()

        # <resto_listaid> →  , <lista_id>
        if self.token.cat == "Coma":
            self.Avanza()

            self.lista_id(Lista_id)

            # Comprobaciones semanticas
            if "lista" in Lista_id.at:
                Resto_listaid.at["lista"] = Lista_id.at["lista"]
            else:
                Resto_listaid.at["lista"] = []

        # Siguientes
        elif self.token.cat == "DosPuntos":

            # Comprobaciones semanticas
            Resto_listaid.at["lista"] = []

            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(17, self.token)
            categoriasLocal = categorias[:] + ["Coma"]
            reservadasLocal = reservadas[:] + []
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Coma":
                self.resto_listaid(Resto_listaid)

    # No Terminal Tipo
    def tipo(self, Tipo):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = []

        # <Tipo> → <tipo_std>
        if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:

            # Atributos de los no terminales
            Tipo_std = Atributos()

            self.tipo_std(Tipo_std)

            # Comprobaciones semanticas
            Tipo.at["t"] = Tipo_std.at["t"]
            Tipo.at["clase"] = "variable"
            Tipo.at["longitud"] = 0

        # <Tipo> → VECTOR [num] DE <Tipo_std>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "VECTOR":

            # Atributos de los no terminales
            Tipo_std = Atributos()

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

                # Comprobaciones semanticas

                # El tamaño del vector debe ser entero
                if self.token.tipo != "int":
                    self.Error(62, self.token)
                    Tipo.at["longitud"] = int(self.token.numero)
                else:
                    Tipo.at["longitud"] = self.token.numero

                # El tamaño del vector no debe ser cero (se trata posteriormente)
                if self.token.numero == 0:
                    self.Error(63, self.token)

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

            self.tipo_std(Tipo)

            # Comprobaciones semanticas
            Tipo.at["t"] = Tipo_std.at["t"]
            Tipo.at["clase"] = "vector"

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(10, self.token)
            categoriasLocal = categorias[:] + []
            reservadasLocal = reservadas[:] + \
                ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["VECTOR", "ENTERO", "REAL", "BOOLEANO"]:
                self.tipo(Tipo)

    # No Terminal Tipo_Std
    def tipo_std(self, Tipo_std):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = []

        if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
            # <Tipo_std> → ENTERO
            # <Tipo_std> → REAL
            # <Tipo_std> → BOOLEANO

            # Comprobaciones semanticas
            if self.token.palabra == "ENTERO":
                Tipo_std.at["t"] = "entero"
            elif self.token.palabra == "REAL":
                Tipo_std.at["t"] = "real"
            else:
                Tipo_std.at["t"] = "booleano"

            self.Avanza()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(19, self.token)
            categoriasLocal = categorias[:]
            reservadasLocal = reservadas[:] + ["ENTERO, REAL, BOOLEANO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra in ["ENTERO", "REAL", "BOOLEANO"]:
                self.tipo_std(Tipo_std)

    # No Terminal Instrucciones
    def instrucciones(self, Instrucciones):

        # Siguientes y palabras reservadas
        categorias = ["Punto"]
        reservadas = []

        # Atributos de los no terminales
        Lista_inst = Atributos()

        # Construccion del arbol
        Instrucciones.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea

        # <instrucciones> → INICIO <lista_inst> FIN
        if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":

            self.Avanza()

            self.lista_inst(Lista_inst)

            if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":

                # Analisis correcto, creacion del arbol
                # (No hay comprobaciones semanticas en el arbol)
                Instrucciones.at["arbol"] = ast.NodoCompuesta(Lista_inst.at["lista"], linea)
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
                self.instrucciones(copy.deepcopy(Instrucciones))

    # No Terminal Lista_Inst
    def lista_inst(self, Lista_inst):

        # Siguientes y palabras reservadas
        categorias = []
        reservadas = ["FIN"]

        # Atributos de los no terminales
        Instruccion = Atributos()
        Lista_Inst1 = Atributos()

        # Construccion del arbol
        Lista_inst.at["lista"] = [ast.NodoVacio(self.token.linea)]
        error = False

        # <lista_inst> → <instrucción> ; <lista_inst>
        if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):

            self.instruccion(Instruccion)

            if self.token.cat == "PuntoComa":
                self.Avanza()
            else:
                error = True
                self.Error(37, self.tokenAnterior)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "PuntoComa", None)
                if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":
                    return

            self.lista_inst(Lista_Inst1)

            # Comprobamos errores
            if not error:
                # Analisis con exito, construccion del arbol
                Lista_inst.at["lista"] = [Instruccion.at["arbol"]] + Lista_Inst1.at["lista"]

        # Siguientes
        elif self.token.cat == "PalabraReservada" and self.token.palabra in reservadas:

            # Construccion del arbol
            Lista_inst.at["lista"] = []
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(12, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + \
                ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
                self.lista_inst(copy.deepcopy(Lista_inst))

    # No Terminal Instruccion
    def instruccion(self, Instruccion):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # Construccion del arbol
        Instruccion.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea
        error = False

        # <instrucción> → INICIO <lista_inst> FIN
        if self.token.cat == "PalabraReservada" and self.token.palabra == "INICIO":

            # Atributos de los no terminales
            Lista_inst = Atributos()

            self.Avanza()

            self.lista_inst(Lista_inst)

            if self.token.cat == "PalabraReservada" and self.token.palabra == "FIN":

                # Construccion del arbol
                # (No son necesarias comprobaciones semanticas)
                Instruccion.at["arbol"] = ast.NodoCompuesta(Lista_inst.at["lista"], linea)

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

            # Atributos de los no terminales
            Inst_simple = Atributos()

            self.inst_simple(Inst_simple)

            # Construccion del arbol
            # (No es necesario realizar comprobaciones semanticas)
            Instruccion.at["arbol"] = Inst_simple.at["arbol"]

        # <instrucción> → <inst_es>
        elif self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:

            # Atributos de los no terminales
            Inst_es = Atributos()

            self.inst_es(Inst_es)

            # Construccion del arbol
            # (No es necesario realizar comprobaciones semanticas)
            Instruccion.at["arbol"] = Inst_es.at["arbol"]

        # <instrucción> →  SI <expresion> ENTONCES <instrucción> SINO <instrucción>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "SI":

            # Atributos de los no terminales
            Expresion = Atributos()
            Instruccion1 = Atributos()
            Instruccion2 = Atributos()

            self.Avanza()

            self.expresion(Expresion)

            if self.token.cat == "PalabraReservada" and self.token.palabra == "ENTONCES":
                self.Avanza()
            else:
                error = True
                self.Error(18, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "ENTONCES")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion(Instruccion1)

            if self.token.cat == "PalabraReservada" and self.token.palabra == "SINO":
                self.Avanza()
            else:
                error = True
                self.Error(21, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "SINO")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion(Instruccion2)

            # Construccion del arbol
            if not error:

                nodoSi = ast.NodoSi(Expresion.at["arbol"], Instruccion1.at["arbol"], Instruccion2.at["arbol"], linea)
                if self.comprobacionSemanticaAST(nodoSi):
                    Instruccion.at["arbol"] = nodoSi

        # <instrucción> → MIENTRAS <expresión> HACER <instrucción>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "MIENTRAS":

            # Atributos de los no terminales
            Expresion = Atributos()
            Instruccion1 = Atributos()

            self.Avanza()

            self.expresion(Expresion)

            if self.token.cat == "PalabraReservada" and self.token.palabra == "HACER":
                self.Avanza()
            else:
                error = True
                self.Error(34, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:] + \
                    ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "PalabraReservada", "HACER")
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.instruccion(Instruccion1)

            # Construccion del arbol
            if not error:
                nodoMientras = ast.NodoMientras(Expresion.at["arbol"], Instruccion1.at["arbol"], linea)
                if self.comprobacionSemanticaAST(nodoMientras):
                    Instruccion.at["arbol"] = nodoMientras

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(25, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:] + \
                ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador" or (self.token.cat == "PalabraReservada" and self.token.palabra in ["INICIO", "LEE", "ESCRIBE", "SI", "MIENTRAS"]):
                self.instruccion(copy.deepcopy(Instruccion))

    # No Terminal Inst_Simple
    def inst_simple(self, Inst_simple):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # Atributos de los no terminales
        Resto_instsimple = Atributos()

        # Construccion del arbol
        Inst_simple.at["arbol"] = ast.NodoVacio(self.token.linea)


        if self.token.cat == "Identificador":
            # <inst_simple> -> id <resto_instsimple>

            # Atributos de los no terminales
            Resto_instsimple.at["h"] = self.token

            self.Avanza()

            self.resto_instsimple(Resto_instsimple)

            # Construccion del arbol
            # (No es necesario realizar comprobaciones semanticas)
            Inst_simple.at["arbol"] = Resto_instsimple.at["arbol"]

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.inst_simple(copy.deepcopy(Inst_simple))

    # No Terminal Resto_Instsimple
    def resto_instsimple(self, Resto_instsimple):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # Construccion del arbol
        Resto_instsimple.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea
        error = False

        if self.token.cat == "OpAsigna":
            # <resto_instsimple> -> opasigna <expresion>

            # Atributos de los no terminales
            Expresion = Atributos()

            self.Avanza()

            self.expresion(Expresion)

            # Construccion del arbol
            variable = ast.NodoAccesoVariable(Resto_instsimple.at["h"].valor, Resto_instsimple.at["h"].linea)
            if not self.comprobacionSemanticaAST(variable):
                variable = ast.NodoVacio(Resto_instsimple.at["h"].linea)

            nodoAsignacion = ast.NodoAsignacion(variable, Expresion.at["arbol"], linea)
            if self.comprobacionSemanticaAST(nodoAsignacion):
                Resto_instsimple.at["arbol"] = nodoAsignacion
            

        elif self.token.cat == "CorcheteApertura":
            # <resto_instsimple> -> [<expr_simple>] opasigna <expresion>

            # Atributos de los no terminales
            Expr_simple = Atributos()
            Expresion = Atributos()

            self.Avanza()

            self.expr_simple(Expr_simple)

            if self.token.cat == "CorcheteCierre":
                self.Avanza()
            else:
                error = True
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
                error = True
                self.Error(20, self.token)
                categoriasLocal = categorias[:] + ["Identificador",
                                                   "Numero", "ParentesisApertura", "OpSuma"]
                reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
                self.Sincroniza(categoriasLocal,
                                reservadasLocal, "OpAsigna", None)
                if self.token.cat == "PuntoComa" or (self.token.cat == "PalabraReservada" and self.token.palabra == "SINO"):
                    return

            self.expresion(Expresion)

            # Construccion del arbol
            if not error:
                vector = ast.NodoAccesoVector(Resto_instsimple.at["h"].valor, Expr_simple.at["arbol"], linea)
                if not self.comprobacionSemanticaAST(vector):
                    vector = ast.NodoVacio(linea)

                nodoAsignacion = ast.NodoAsignacion(vector, Expresion.at["arbol"], linea)
                if self.comprobacionSemanticaAST(nodoAsignacion):
                    Resto_instsimple.at["arbol"] = nodoAsignacion

        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            # Siguientes

            # Construccion del arbol
            accesoVariable = ast.NodoAccesoVariable(Resto_instsimple.at["h"].valor, linea)
            if self.comprobacionSemanticaAST(accesoVariable):
                Resto_instsimple.at["arbol"] = accesoVariable
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(8, self.token)
            categoriasLocal = categorias[:] + ["OpAsigna", "CorcheteApertura"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["OpAsigna", "CorcheteApertura"]:
                self.resto_instsimple(copy.deepcopy(Resto_instsimple))

    # No Terminal Variable
    def variable(self, Variable):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        # Atributos de los no terminales
        Resto_var = Atributos()

        # Construccion del arbol
        Variable.at["arbol"] = ast.NodoVacio(self.token.linea)

        # <variable> -> id <resto_var>
        if self.token.cat == "Identificador":
            
            # Atributos de los no terminales
            Resto_var.at["h"] = self.token

            self.Avanza()

            self.resto_var(Resto_var)

            # Construccion del arbol
            # (No es necesaria comprobacion semantica)
            Variable.at["arbol"] = Resto_var.at["arbol"]

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(2, self.token)
            categoriasLocal = categorias[:] + ["Identificador"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "Identificador":
                self.variable(copy.deepcopy(Variable))

    # No Terminal Resto_Var
    def resto_var(self, Resto_var):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        # Construccion del arbol
        Resto_var.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea
        error = False

        if self.token.cat == "CorcheteApertura":
            # <resto_var> -> [<expr_simple>]
            
            # Atributos de los no terminales
            Expr_simple = Atributos()

            self.Avanza()

            self.expr_simple(Expr_simple)

            if self.token.cat == "CorcheteCierre":
                self.Avanza()
            else:
                error = True
                self.Error(15, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "CorcheteCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            # Construccion del arbol
            if not error:
                accesoVector = ast.NodoAccesoVector(Resto_var.at["h"].valor, Expr_simple.at["arbol"], linea)
                if self.comprobacionSemanticaAST(accesoVector):
                    Resto_var.at["arbol"] = accesoVector
                

        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            # Siguientes

            # Construccion del arbol
            accesoVariable = ast.NodoAccesoVariable(Resto_var.at["h"].valor, linea)
            if self.comprobacionSemanticaAST(accesoVariable):
                Resto_var.at["arbol"] = accesoVariable

            return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(23, self.token)
            categoriasLocal = categorias[:] + ["CorcheteApertura"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "CorcheteApertura":
                self.resto_var(copy.deepcopy(Resto_var))

    # No Terminal Inst_Es
    def inst_es(self, Inst_es):

        # Siguientes y palabras reservadas
        categorias = ["PuntoComa"]
        reservadas = ["SINO"]

        # Construccion del arbol
        Inst_es.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea
        error = False
        id = None

        # <inst_es> → LEE(id)
        if self.token.cat == "PalabraReservada" and self.token.palabra == "LEE":
            self.Avanza()

            if self.token.cat == "ParentesisApertura":
                self.Avanza()
            else:
                error = True
                self.Error(26, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisApertura", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            if self.token.cat == "Identificador":
                id = self.token
                self.Avanza()
            else:
                error = True
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
                error = True
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            # Construccion del arbol
            if not error:
                nodoLee = ast.NodoLee(id.valor, linea)
                if self.comprobacionSemanticaAST(nodoLee):
                    Inst_es.at["arbol"] = nodoLee

        # <inst_es> → ESCRIBE (<expr_simple>)
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "ESCRIBE":
            # Atributos de los no terminales
            Expr_simple = Atributos()
            
            self.Avanza()

            if self.token.cat == "ParentesisApertura":
                self.Avanza()
            else:
                error = True
                self.Error(26, self.token)
                categoriasLocal = categorias[:] + ["Identificador"]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisApertura", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return

            self.expr_simple(Expr_simple)

            if self.token.cat == "ParentesisCierre":
                self.Avanza()
            else:
                error = True
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return
            
            # Construccion del arbol
            if not error:
                # El nodo Escribe no tiene comprobaciones semanticas
                Inst_es.at["arbol"] = ast.NodoEscribe(Expr_simple.at["arbol"], linea)

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(9, self.token)
            categoriasLocal = categorias[:]
            reservadasLocal = reservadas[:] + ["LEE", "ESCRIBE"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "PalabraReservada" and self.token.palabra in ["LEE", "ESCRIBE"]:
                self.inst_es(copy.deepcopy(Inst_es))

    # No Terminal Expresion
    def expresion(self, Expresion):

        # Siguientes y palabras reservadas
        categorias = ["ParentesisCierre", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # Atributos de los no terminales
        Expr_simple = Atributos()
        ExpresionPrime = Atributos()

        # Construccion del arbol
        Expresion.at["arbol"] = ast.NodoVacio(self.token.linea)

        # <expresión> → <expr_simple> <expresiónPrime>
        if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
            
            self.expr_simple(Expr_simple)

            ExpresionPrime.at["h"] = Expr_simple.at["arbol"]

            self.expresionPrime(ExpresionPrime)

            # Construccion del arbol
            # (No es necesaria comprobacion semantica)
            Expresion.at["arbol"] = ExpresionPrime.at["arbol"]

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(24, self.token)
            categoriasLocal = categorias[:] + ["Identificador",
                                               "Numero", "OpSuma", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "OpSuma", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.expresion(copy.deepcopy(Expresion))

    # No Terminal ExpresionPrime
    def expresionPrime(self, ExpresionPrime):

        # Siguientes y palabras reservadas
        categorias = ["ParentesisCierre", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # Atributos de los no terminales
        Expr_simple = Atributos()

        # Construccion del arbol
        ExpresionPrime.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea
        op = None

        # <expresiónPrime> → oprel <expr_simple>
        if self.token.cat == "OpRelacional":
            op = self.token

            self.Avanza()

            self.expr_simple(Expr_simple)

            # Construccion del arbol
            nodoComparacion = ast.NodoComparacion(ExpresionPrime.at["h"], Expr_simple.at["arbol"], linea, op.operacion)
            if self.comprobacionSemanticaAST(nodoComparacion):
                ExpresionPrime.at["arbol"] = nodoComparacion

        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            ExpresionPrime.at["arbol"] = ExpresionPrime.at["h"]

            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(28, self.token)
            categoriasLocal = categorias[:] + ["OpRelacional"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpRelacional":
                self.expresionPrime(copy.deepcopy(ExpresionPrime))

    # No Terminal Expr_Simple
    def expr_simple(self, Expr_simple):

        # Siguientes y palabras reservadas
        categorias = ["CorcheteCierre", "ParentesisCierre",
                      "OpRelacional", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # Construccion del arbol
        Expr_simple.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea

        # <expr_simple> → <término> <resto_exsimple>
        if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):

            # Atributos de los no terminales
            Termino = Atributos()
            Resto_exprsimple = Atributos()

            self.termino(Termino)

            # Atributos de los no terminales
            Resto_exprsimple.at["h"] = Termino.at["arbol"]

            self.restoexpr_simple(Resto_exprsimple)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Expr_simple.at["arbol"] = Resto_exprsimple.at["arbol"]

        # <expr_simple> → <signo> <término> <resto_exsimple>
        elif self.token.cat == "OpSuma":

            # Atributos de los no terminales
            Signo = Atributos()
            Termino = Atributos()
            Resto_exprsimple = Atributos()

            self.signo(Signo)

            self.termino(Termino)

            # Atributos de los no terminales
            Resto_exprsimple.at["h"] = Termino.at["arbol"]

            self.restoexpr_simple(Resto_exprsimple)

            # Construccion del arbol
            # (No hace falta comprobacion semantica, el nodo signo no hace comprobaciones)
            Expr_simple.at["arbol"] = ast.NodoSigno(Signo.at["signo"], Resto_exprsimple.at["arbol"], linea)

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(29, self.token)
            categoriasLocal = categorias[:] + ["Identificador",
                                               "Numero", "ParentesisApertura", "OpSuma"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura", "OpSuma"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.expr_simple(copy.deepcopy(Expr_simple))

    # No Terminal Restoexpr_Simple
    def restoexpr_simple(self, Resto_exprsimple):

        # Siguientes y palabras reservadas
        categorias = ["CorcheteCierre", "ParentesisCierre",
                      "OpRelacional", "PuntoComa"]
        reservadas = ["HACER", "SINO", "ENTONCES"]

        # Construccion del arbol
        Resto_exprsimple.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea

        # <resto_exsimple> → opsuma <término> <resto_exsimple>
        if self.token.cat == "OpSuma":

            # Atributos de los no terminales
            Termino = Atributos()
            Resto_exprsimple1 = Atributos()
            op = self.token

            self.Avanza()

            self.termino(Termino)

            # Atributos de los no terminales y construccion/comprobacion del nodo aritmetico
            Resto_exprsimple1.at["h"] = ast.NodoVacio(linea)
            nodoAritmetico = ast.NodoAritmetico(Resto_exprsimple.at["h"], Termino.at["arbol"], linea, op.operacion)
            if self.comprobacionSemanticaAST(nodoAritmetico):
                Resto_exprsimple1.at["h"] = nodoAritmetico

            self.restoexpr_simple(Resto_exprsimple1)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_exprsimple.at["arbol"] = Resto_exprsimple1.at["arbol"]


        #	<resto_exsimple> → O <término> <resto_exsimple>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "O":
            
            # Atributos de los no terminales
            Termino = Atributos()
            Resto_exprsimple1 = Atributos()

            self.Avanza()

            self.termino(Termino)

            # Atributos de los no terminales
            Resto_exprsimple1.at["h"] = ast.NodoVacio(linea) 
            nodoLogico = ast.NodoLogico(Resto_exprsimple.at["h"], Termino.at["arbol"], linea, "o")
            if self.comprobacionSemanticaAST(nodoLogico):
                Resto_exprsimple1.at["h"] = nodoLogico

            self.restoexpr_simple(Resto_exprsimple1)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_exprsimple.at["arbol"] = Resto_exprsimple1.at["arbol"]

        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            
            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_exprsimple.at["arbol"] = Resto_exprsimple.at["h"]
            
            return

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(30, self.token)
            categoriasLocal = categorias[:] + ["OpSuma"]
            reservadasLocal = reservadas[:] + ["O"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpSuma" or (self.token.cat == "PalabraReservada" and self.token.palabra == "O"):
                self.restoexpr_simple(copy.deepcopy(Resto_exprsimple))

    # No Terminal Termino
    def termino(self, Termino):

        # Siguientes y palabras reservadas
        categorias = ["OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["O", "HACER", "SINO", "ENTONCES"]

        # Atributos de los no terminales
        Factor = Atributos()
        Resto_Term = Atributos()

        # Construccion del arbol
        Termino.at["arbol"] = ast.NodoVacio(self.token.linea)

        # <término> → <factor> <resto_term>
        if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
            
            self.factor(Factor)

            # Atributos de los no terminales
            Resto_Term.at["h"] = Factor.at["arbol"]

            self.resto_term(Resto_Term)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Termino.at["arbol"] = Resto_Term.at["arbol"]

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(35, self.token)
            categoriasLocal = categorias[:] + \
                ["Identificador", "Numero", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat in "PalabraReservada" and self.token.palabra == ["NO", "CIERTO", "FALSO"]):
                self.termino(copy.deepcopy(Termino))

    # No Terminal Resto_Term
    def resto_term(self, Resto_Term):

        # Siguientes y palabras reservadas
        categorias = ["OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["O", "HACER", "SINO", "ENTONCES"]

        # Construccion del arbol
        Resto_Term.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea

        # <resto_term> → opmult <factor> <resto_term>
        if self.token.cat == "OpMultiplicacion":

            # Atributos de los no terminales
            Factor = Atributos()
            Resto_Term1 = Atributos()
            op = self.token

            self.Avanza()

            self.factor(Factor)

            # Atributos de los no terminales y construccion del nodo aritmetico
            Resto_Term1.at["h"] = ast.NodoVacio(linea)
            nodoAritmetico = ast.NodoAritmetico(Resto_Term.at["h"], Factor.at["arbol"], linea, op.operacion)
            if self.comprobacionSemanticaAST(nodoAritmetico):
                Resto_Term1.at["h"] = nodoAritmetico

            self.resto_term(Resto_Term1)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_Term.at["arbol"] = Resto_Term1.at["arbol"]


        # <resto_term> → Y <factor> <resto_term>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "Y":
            
            # Atributos de los no terminales
            Factor = Atributos()
            Resto_Term1 = Atributos()
            op = self.token

            self.Avanza()

            self.factor(Factor)

            # Atributos de los no terminales y construccion del nodo logico
            Resto_Term1.at["h"] = ast.NodoVacio(linea)
            nodoLogico = ast.NodoLogico(Resto_Term.at["h"], Factor.at["arbol"], linea, "y")
            if self.comprobacionSemanticaAST(nodoLogico):
                Resto_Term1.at["h"] = nodoLogico

            self.resto_term(Resto_Term1)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_Term.at["arbol"] = Resto_Term1.at["arbol"]


        # Siguientes
        elif self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
            
            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Resto_Term.at["arbol"] = Resto_Term.at["h"]
            
            return

        # No se ha encontrado ningún primero ni siguientes, sincronizacion
        else:
            self.Error(31, self.tokenAnterior)
            categoriasLocal = categorias[:] + ["OpMultiplicacion"]
            reservadasLocal = reservadas[:] + ["Y"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpMultiplicacion" or (self.token.cat == "PalabraReservada" and self.token.palabra == "Y"):
                self.resto_term(copy.deepcopy(Resto_Term))

    # No Terminal Factor
    def factor(self, Factor):

        # Siguientes y palabras reservadas
        categorias = ["OpMultiplicacion", "OpSuma", "CorcheteCierre",
                      "ParentesisCierre", "OpRelacional", "PuntoComa"]
        reservadas = ["Y", "O", "HACER", "SINO", "ENTONCES"]

        # Construccion del arbol
        Factor.at["arbol"] = ast.NodoVacio(self.token.linea)
        linea = self.token.linea

        #	<factor> → <variable>
        if self.token.cat == "Identificador":

            # Atributos de los no terminales
            Variable = Atributos()

            self.variable(Variable)

            # Construccion del arbol
            # (No hace falta comprobacion semantica)
            Factor.at["arbol"] = Variable.at["arbol"]

        # <factor> → num
        elif self.token.cat == "Numero":

            # Guardamos num
            num = self.token

            self.Avanza()

            # Construccion del arbol
            # (La comprobacion se hace implicitamente)
            if num.tipo == "real":
                Factor.at["arbol"] = ast.NodoReal(num.valor, linea)
            else:
                Factor.at["arbol"] = ast.NodoEntero(num.valor, linea)


        # <factor> → ( <expresión> )
        elif self.token.cat == "ParentesisApertura":
            
            # Atributos de los no terminales
            Expresion = Atributos()
            error = False
            
            self.Avanza()

            self.expresion(Expresion)

            if self.token.cat == "ParentesisCierre":
                self.Avanza()
            else:
                error = True
                self.Error(27, self.token)
                categoriasLocal = categorias[:]
                reservadasLocal = reservadas[:]
                self.Sincroniza(categoriasLocal, reservadasLocal,
                                "ParentesisCierre", None)
                if self.token.cat in categorias or (self.token.cat == "PalabraReservada" and self.token.palabra in reservadas):
                    return
            
            # Construccion del arbol
            # (No es necesaria comprobacion semantica)
            if not error:
                Factor.at["arbol"] = Expresion.at["arbol"]


        # <factor> → NO <factor>
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "NO":
            
            # Atributos de los no terminales
            Factor1 = Atributos()
            
            self.Avanza()

            self.factor(Factor1)

            # Construccion del arbol
            Factor.at["arbol"] = ast.NodoVacio(linea)
            nodoNo = ast.NodoNo(Factor1.at["arbol"], linea)
            if self.comprobacionSemanticaAST(nodoNo):
                Factor.at["arbol"] = nodoNo

        # <factor> → CIERTO
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "CIERTO":            
            self.Avanza()

            # Construccion del arbol
            # (1 simboliza un valor cierto)
            Factor.at["arbol"] = ast.NodoBooleano(1, linea)


        # <factor> → FALSO
        elif self.token.cat == "PalabraReservada" and self.token.palabra == "FALSO":
            self.Avanza()

            # Construccion del arbol
            # (1 simboliza un valor falso)
            Factor.at["arbol"] = ast.NodoBooleano(0, linea)


        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(32, self.token)
            categoriasLocal = categorias[:] + \
                ["Identificador", "Numero", "ParentesisApertura"]
            reservadasLocal = reservadas[:] + ["NO", "CIERTO", "FALSO"]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat in ["Identificador", "Numero", "ParentesisApertura"] or (self.token.cat == "PalabraReservada" and self.token.palabra in ["NO", "CIERTO", "FALSO"]):
                self.factor(copy.deepcopy(Factor))

    # No Terminal Signo
    def signo(self, Signo):

        # Siguientes y palabras reservadas
        categorias = ["Identificador", "Numero", "ParentesisApertura"]
        reservadas = ["NO", "CIERTO", "FALSO"]

        # <signo> → +
        # <signo> → -
        if self.token.cat == "OpSuma":
            
            # Atributos de los no terminales
            Signo.at["signo"] = self.token.operacion
            self.Avanza()

        # No se ha encontrado ningún primero, sincronizacion
        else:
            self.Error(33, self.token)
            categoriasLocal = categorias[:] + ["OpSuma"]
            reservadasLocal = reservadas[:]
            self.Sincroniza(categoriasLocal, reservadasLocal, None, None)
            if self.token.cat == "OpSuma":
                self.signo(copy.deepcopy(Signo))


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

    # Atributos de programa
    Programa = Atributos()

    S.Programa(Programa)
    if S.aceptacion:
        print("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
        print("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")

    # Imprime el AST
    print("\nAST generado:")
    print(Programa.at["arbol"])
