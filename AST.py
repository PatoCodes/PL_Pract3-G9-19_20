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

	# Metodo para calcular la profundidad de cada nodo. Se utilizara de cara a imprimir tabulaciones
	# Inicialmente, todas las profundidades se inicializan a 0
	# Las profundidades se utilizan unicamente para imprimir el arbol con profundidad
	def calculaProfundidad(self, profundidad):
		pass

class NodoAsignacion(AST):
    def __init__(self, izda, exp, linea):
        self.izda = izda
        self.exp = exp
        self.linea = linea
        self.profundidad = 0

        # Errores
        self.errores = []

        self.compsem()

    def calculaProfundidad(self, profundidad):
        # Calcula profundidades
        self.profundidad = profundidad
        self.izda.calculaProfundidad(profundidad + 1)
        self.exp.calculaProfundidad(profundidad + 1)


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
        tabulacion = self.profundidad * '    '
        return tabulacion + '("Asignacion" "linea: {linea}"\n{izda}\n{exp}\n'.format(linea = self.linea, izda = self.izda, exp = self.exp) + tabulacion + ')'


class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea
		self.profundidad = 0

        # Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad
		self.exp.calculaProfundidad(self.profundidad + 1)
		self.si.calculaProfundidad(self.profundidad + 1)
		self.sino.calculaProfundidad(self.profundidad + 1)

	def compsem(self):
		
		# La expresion debe ser de tipo logico
		if self.exp.tipo in ["entero", "real"]:
			self.errores = self.errores + ["condicion_no_logica"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Si" "linea: {linea}"\n{exp}\n{si}\n{sino}\n'.format(linea = self.linea, exp = self.exp, si = self.si, sino = self.sino) + tabulacion + ')'


class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad
		self.exp.calculaProfundidad(self.profundidad + 1)
		self.inst.calculaProfundidad(self.profundidad + 1)

	def compsem(self):
		
		# La expresion debe ser de tipo logico
		if self.exp.tipo in ["entero", "real"]:
			self.errores = self.errores + ["condicion_no_logica"]


	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Mientras" "linea: {linea}"\n{exp}\n{inst}\n'.format(linea = self.linea, exp = self.exp, inst = self.inst) + tabulacion + ')'


class NodoLee(AST):
	def __init__(self, var, linea):
		self.var = var
		self.linea = linea
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

	def compsem(self):

		# Se deben leer unicamente variables simples (no se permite leer identificadores que sean vectores o programa) y que sean ENTERO O REAL
		clase = ts.devuelveInfo(self.var, "clase")
		if clase != "variable":
			errores = errores + ["clase_erronea_lee"]
		else:
			tipo = ts.devuelveInfo(self.var, "tipo")
			if tipo == "booleano":
				errores = errores + ["tipo_erroneo_lee"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Lee" "var: {var}" "linea: {linea}")'.format(linea = self.linea, var = self.var)


class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad
		self.exp.calculaProfundidad(self.profundidad + 1)

	def compsem(self):
		# No son necesarias comprobaciones semanticas en el nodo Escribe
		# (no hay restricciones en la expresion que puede escribir)
		pass

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Escribe" "linea: {linea}"\n{exp}\n'.format(linea = self.linea, exp = self.exp) + tabulacion + ')'


class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()
	
	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidades de los hijos
		for sent in self.lsen:
			sent.calculaProfundidad(self.profundidad + 1)

	def compsem(self):
		# No son necesarias comprobaciones semanticas en el nodo Compuesta
		# (cada instruccion contenida hara sus propias comprobaciones)
		pass

	def arbol(self):
		tabulacion = self.profundidad * '    '
		compuesta = tabulacion + '("Compuesta" "linea: {linea}"\n'.format(linea = self.linea)
		for sent in self.lsen:
			compuesta += sent.arbol() + '\n'
		return compuesta + tabulacion + ')'


class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "booleano"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidades de los hijos
		self.izq.calculaProfundidad(self.profundidad + 1)
		self.dcha.calculaProfundidad(self.profundidad + 1)

	def compsem(self):

		# Es necesario comparar valores numericos, no se pueden comparar valores booleanos
		if self.izq.tipo == "booleano" or self.dcha.tipo == "booleano":
			errores = errores + ["tipo_erroneo_comp"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Comparacion" "op: {op}" "tipo: {tipo}" "linea: {linea}"\n{izq}\n{dcha}\n'.format(op = self.op, tipo = self.tipo, linea = self.linea, izq = self.izq, dcha = self.dcha) + tabulacion + ')'


class NodoAritmetico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "desconocido"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidades de los hijos
		self.izq.calculaProfundidad(self.profundidad + 1)
		self.dcha.calculaProfundidad(self.profundidad + 1)
	
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
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Aritmetica" "op: {op}" "tipo: {tipo}" "linea: {linea}"\n{izq}\n{dcha}\n'.format(op = self.op, tipo = self.tipo, linea = self.linea, izq = self.izq, dcha = self.dcha) + tabulacion + ')'


class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "entero"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante entera)
		pass

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Entero" "valor: {valor}" "tipo: {tipo}" "linea: {linea}")'.format(valor = self.valor, tipo = self.tipo, linea = self.linea)


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "real"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante real)
		pass

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Real" "valor: {valor}" "tipo: {tipo}" "linea: {linea}")'.format(valor = self.valor, tipo = self.tipo, linea = self.linea)


class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.tipo = "booleano"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

	def compsem(self):
		# No hace falta comprobacion semantica
		# (solo se crea este nodo cuando se lee una constante booleana)
		pass

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Booleano" "valor: {valor}" "tipo: {tipo}" "linea: {linea}")'.format(valor = self.valor, tipo = self.tipo, linea = self.linea)


class NodoAccesoVariable(AST):
	def __init__(self, var, linea):
		self.var = var
		self.linea = linea
		self.tipo = "desconocido"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

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
				self.errores = self.errores + ["clase_erronea_var"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("AccesoVariable" "var: {var}" "tipo: {tipo}" "linea: {linea}")'.format(var = self.var, tipo = self.tipo, linea = self.linea)


class NodoAccesoVector(AST):
	def __init__(self, vect, exp, linea):
		self.var = vect
		self.exp = exp
		self.linea = linea
		self.tipo = "desconocido"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

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
				self.errores = self.errores + ["clase_erronea_vect"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("AccesoVector" "var: {var}" "tipo: {tipo}" "linea: {linea}"\n{exp}\n'.format(var = self.var, tipo = self.tipo, linea = self.linea, exp = self.exp) + tabulacion + ')'


# Nodos añadidos

class NodoSigno(AST):
	def __init__(self, signo, term, linea):
		self.signo = signo
		self.term = term
		self.linea = linea
		self.profundidad = 0
		self.tipo = "desconocido"

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidad de los hijos
		self.term.calculaProfundidad(self.profundidad + 1)
	
	def compsem(self):
		# TODO: Comprueba que es numerico y pon tipo adecuado

		# El tipo del termino debe ser numerico (no puede ser booleano)
		if self.term.tipo == "booleano":
			errores = errores + ["tipo_erroneo_signo"]
		else:
			# Ponemos el tipo adecuado al signo.
			# (si la expresion es de tipo Vacio, tomamos tipo real por defecto)
			self.tipo = self.term.tipo
			if self.tipo == "vacio":
				self.tipo == "real"

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Signo" "signo: {signo}" "tipo: {tipo}" "linea: {linea}"\n{term}\n'.format(signo = self.signo, tipo = self.tipo, linea = self.linea, term = self.term) + tabulacion + ')'


class NodoLogico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = "booleano"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidad de los hijos
		self.izq.calculaProfundidad(self.profundidad + 1)
		self.dcha.calculaProfundidad(self.profundidad + 1)

	def compsem(self):

		# Ambas expresiones (izquierda y derecha) deben de ser de tipo booleano
		if self.izq.tipo in ["entero", "real"] or self.dcha.tipo in ["entero", "real"]:
			self.errores = self.errores + ["tipo_erroneo_log"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Logica" "op: {op}" "tipo: {tipo}" "linea: {linea}"\n{izq}\n{dcha}\n'.format(op = self.op, tipo = self.tipo, linea = self.linea, izq = self.izq, dcha = self.dcha) + tabulacion + ')'


class NodoNo(AST):
	def __init__(self, fact, linea):
		self.fact = fact
		self.linea = linea
		self.tipo = "booleano"
		self.profundidad = 0

		# Errores
		self.errores = []

		self.compsem()

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

		# Profundidad de los hijos
		self.fact.calculaProfundidad(self.profundidad + 1)

	def compsem(self):

		# El factor debe de ser de tipo booleano
		if self.fact.tipo in ["entero", "real"]:
			self.errores = self.errores + ["tipo_erroneo_log"]

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("No" "tipo: {tipo}" "linea: {linea}"\n{fact}\n'.format(tipo = self.tipo, linea = self.linea, fact = self.fact) + tabulacion + ')'


class NodoVacio(AST):
	def __init__(self, linea):
		self.linea = linea
		self.profundidad = 0

		# Usado para identificar el nodo Vacio
		self.tipo = "vacio"

	def calculaProfundidad(self, profundidad):
		# Calcula profundidades
		self.profundidad = profundidad

	def arbol(self):
		tabulacion = self.profundidad * '    '
		return tabulacion + '("Vacio (ERROR)" "linea: {linea}")'.format(linea = self.linea)
