#!/usr/bin/env python

# Acceso a la tabla de símbolos
import tablaSimbolos as ts

# Observaciones generales:
# - Donde sea necesario, hay conversion implicita de entero a real
# - NO existe ninguna conversion implicita con booleanos (los tipos booleanos y numericos no son compatibles)
# - El tipo vacio representa un nodo vacio (un error) y se asume compatible siempre que se compruebe compatibilidad

class AST:
	def __str__(self):
		return self.arbol()

	# Metodo a implementar por todos los nodos
	def arbol(self):
		pass


class NodoAsignacion(AST):
    def __init__(self, izda, exp, linea):
        self.izda = izda
        self.exp = exp
        self.linea = linea

        # Errores
        self.errores = []

        self.compsem()

    def compsem(self):
        # Se comprueba previamente en la parte izquierda si se ha declarado la variable o no
        # (sabemos con garantia que si no es vacio, sera variable o vector)

        # Obtenemos el tipo de la variable
        tipo = self.izda.tipo

        # Si la expresion no concuerda con el tipo de la variable, se emite error
		# Combinaciones validas:
        # (var int, expr int)
        # (var real, expr int o real)
        # (var bool, expr bool)
        # Vacio es compatible con todo

        if (tipo == "entero" and self.exp.tipo in ["real", "booleano"]) or (tipo == "real" and self.exp.tipo == "booleano") or (tipo == "booleano" and self.exp.tipo in ["entero", "real"]):
            self.errores = self.errores + ["asignacion_invalida"]

    def arbol(self):
        return '( "Asignacion"\n  "linea: %s" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)


class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea

        # Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		
		# La expresion debe ser de tipo logico
		if self.exp.tipo in ["entero", "real"]:
			self.errores = self.errores + ["condicion_no_logica"]

	def arbol(self):
		return '( "Si" "linea: %s" %s\n %s\n %s\n )' % (self.linea, self.exp, self.si, self.sino)


class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		
		# La expresion debe ser de tipo logico
		if self.exp.tipo in ["entero", "real"]:
			self.errores = self.errores + ["condicion_no_logica"]


	def arbol(self):
		return '( "Mientras" "linea: %s" %s\n %s\n )' % (self.linea, self.exp, self.inst)


class NodoLee(AST):
	def __init__(self, var, linea):
		self.var = var
		self.linea = linea

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):

		# Se deben leer unicamente variables simples (no se permite leer identificadores que sean vectores o programa)
		clase = ts.devuelveInfo(self.var, "clase")
		if clase != "variable":
			errores = errores + ["clase_erronea_lee"]

	def arbol(self):
		return '( "Lee" "linea: %s" %s )' % (self.linea, self.var)


class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		# No son necesarias comprobaciones semanticas en el nodo Escribe
		# (no hay restricciones en la expresion que puede escribir)
		pass

	def arbol(self):
		return '( "Escribe" "linea: %s" %s )' % (self.linea, self.exp)


class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		# No son necesarias comprobaciones semanticas en el nodo Compuesta
		# (cada instruccion contenida hara sus propias comprobaciones)
		pass

	def arbol(self):
		r = ""
		for sent in self.lsen:
			r += sent.arbol()+"\n"

		return '( "Compuesta"\n %s)' % r


class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "booleano"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):

		# Es necesario comparar valores numericos, no se pueden comparar valores booleanos
		if self.izq.tipo == "booleano" or self.dcha.tipo == "booleano":
			errores = errores + ["tipo_erroneo_comp"]

	def arbol(self):
		return '( "Comparacion" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)


class NodoAritmetico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "desconocido"

		# Errores
		self.errores = []

		self.compsem()
	
	def compsem(self):
		
		# Comprobamos que ninguna de las dos expresiones sea un booleano
		if self.izq.tipo == "booleano" or self.dcha.tipo == "booleano":
			self.errores = self.errores + ["tipo_erroneo_arit"]
		else:
			# Si ambos son numericos, se comprueba el tipo mas general
			# Real > Entero; Vacio es indiferente.
			# (Conversion implicita de entero a real si es necesario)
			
			# Tipo de la izquierda
			tipo = self.izq.tipo

			# Comparacion con la derecha
			# Derecha es entero
			if self.dcha.tipo == "entero":
				# Izd real, dcha entera
				if tipo == "real":
					self.tipo = "real"
				# Cualquier otro caso
				else:
					self.tipo = "entero"
			# Derecha es real
			elif self.dcha.tipo == "real":
				# El tipo sera siempre real
				self.tipo = "real"
			# Derecha es vacio (se conserva el tipo de la izquierda)
			else:
				self.tipo = tipo

			# Si ambos son vacio, hacemos por defecto tipo real
			if self.tipo == "vacio":
				self.tipo = "real"

	def arbol(self):
		return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)


class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "entero"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante entera)
		pass

	def arbol(self):
		return '( "Entero" "valor: %s" "tipo: entero" "linea: %s" )' % (self.valor, self.linea)


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "real"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante real)
		pass

	def arbol(self):
		return '( "Real" "valor: %s" "tipo: real" "linea: %s" )' % (self.valor, self.linea)


class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "booleano"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante booleana)
		pass

	def arbol(self):
		return '( "Booleano" "valor: %s" "tipo: booleano" "linea: %s" )' % (self.valor, self.linea)


class NodoAccesoVariable(AST):
    def __init__(self, var, linea):
        self.var = var
        self.linea = linea
        self.tipo = "desconocido"

        # Errores
        self.errores = []

        self.compsem()

    def compsem(self):
        # Comprobamos el tipo de la variable (e indirectamente si existe)
        tipo = ts.devuelveInfo(self.var, "tipo")
        if tipo is None:
            # La variable no ha sido declarada previamente
            self.errores = self.errores + ["sin_declarar"]
        else:
            # Variable declarada correctamente
            self.tipo = tipo

            # Comprobamos que la variable ES una variable (no es programa ni vector)
            if ts.devuelveInfo(self.var, "clase") != "variable":
                self.errores = self.errores + ["clase_erronea"]

    def arbol(self):
        return '( "AccesoVariable" "v: %s" "tipo: %s" "linea: %s" )' % (self.var, self.tipo, self.linea)


class NodoAccesoVector(AST):
    def __init__(self, vect, exp, linea):
        self.var = vect
        self.exp = exp
        self.linea = linea
        self.tipo = "desconocido"

        # Errores
        self.errores = []

        self.compsem()

    def compsem(self):
        # Comprobamos el tipo del vector (e indirectamente si existe)
        tipo = ts.devuelveInfo(self.var, "tipo")
        if tipo is None:
            # El vector no ha sido declarado previamente
            self.errores = self.errores + ["sin_declarar"]
        else:
            # Vector declarado correctamente
            self.tipo = tipo

            # Comprobamos que el vector ES un vector (no es programa ni variable)
            if ts.devuelveInfo(self.var, "clase") != "vector":
                self.errores = self.errores + ["clase_erronea"]

        # TODO ¿Comprobacion de que el indice del vector es correcto?

    def arbol(self):
        return '( "AccesoVector" "tipo: %s" "linea: %s" %s\n %s\n)' % (self.tipo, self.linea, self.var, self.exp)


# Nodos añadidos

class NodoSigno(AST):
	def __init__(self, signo, term, linea):
		self.signo = signo
		self.term = term
		self.linea = linea

		# Errores
		self.errores = []

		self.compsem()
	
	def compsem(self):
		# No son necesarias comprobaciones semanticas para este nodo
		pass

	def arbol(self):
		return '( "Signo" "valor: %s" "linea: %s" \n %s\n)' % (self.signo, self.linea, self.term)


class NodoLogico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "booleano"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):

		# Ambas expresiones (izquierda y derecha) deben de ser de tipo booleano
		if self.izq.tipo in ["entero", "real"] or self.dcha.tipo in ["entero", "real"]:
			self.errores = self.errores + ["tipo_erroneo_log"]

	def arbol(self):
		return '( "Logica" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)


class NodoNo(AST):
	def __init__(self, fact, linea):
		self.fact = fact
		self.linea = linea
		self.tipo = "booleano"

		# Errores
		self.errores = []

		self.compsem()

	def compsem(self):

		# El factor debe de ser de tipo booleano
		if self.fact.tipo in ["entero", "real"]:
			self.errores = self.errores + ["tipo_erroneo_log"]

	def arbol(self):
		return '( "No" "tipo: booleano" "linea: %s" \n %s\n)' % (self.linea, self.fact)


class NodoVacio(AST):
    def __init__(self, linea):
        self.linea = linea

        # Usado para identificar el nodo Vacio
        self.tipo = "vacio"

    def arbol(self):
        return '( "Vacio (ERROR)" "linea: %s" )' % (self.linea)
