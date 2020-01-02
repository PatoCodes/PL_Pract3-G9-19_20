#!/usr/bin/env python

# Acceso a la tabla de símbolos
import tablaSimbolos as ts

class AST:
	def __str__(self):
		return self.arbol()

	# Metodos estandar a implementar (si es necesario) por los nodos especificos
	def arbol(self):
		pass

	# NOTA: Compsem devolverá TRUE si las comprobaciones son correctas y FALSE si se detecta algún error.
	# Este valor se almacenará en una variable de la clase, "correcto", que se usará para emitir errores.
	def compsem(self):
		pass

class NodoAsignacion(AST):
	def __init__(self, izda, exp, linea):
		self.izda = izda
		self.exp = exp
		self.linea = linea
		self.compsem()

	def arbol(self):
		return '( "Asignacion"\n  "linea: %s" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)

class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea
		self.compsem()

	def arbol(self):
		return '( "Si" "linea: %s" %s\n %s\n %s\n )' % (self.linea, self.exp, self.si, self.sino)

class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea
		self.compsem()

	def arbol(self):
		return '( "Mientras" "linea: %s" %s\n %s\n )' % (self.linea, self.exp, self.inst)

class NodoLee(AST):
	def __init__(self,var,linea):
		self.var = var
		self.linea = linea
		self.compsem()

	def arbol(self):
		return '( "Lee" "linea: %s" %s )' % (self.linea, self.var)

class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea
		self.compsem()

	def arbol(self):
		return '( "Escribe" "linea: %s" %s )' % (self.linea, self.exp)

class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea
		self.compsem()

	def arbol(self):
		r = ""
		for sent in self.lsen:
			r+= sent.arbol()+"\n"

		return '( "Compuesta"\n %s)' % r

class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None
		self.compsem()

	def arbol(self):
		return '( "Comparacion" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoAritmetico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None
		self.compsem()

	def arbol(self):
		return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()
	
	def arbol(self):
		return '( "Entero" "valor: %s" "tipo: %s" "linea: %s" )' % (self.valor, self.tipo, self.linea)


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()
	
	def arbol(self):
		return '( "Real" "valor: %s" "tipo: %s" "linea: %s" )' % (self.valor, self.tipo, self.linea)

class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()
	
	def arbol(self):
		return '( "BOOLEANO" "valor: %s" "tipo: %s" "linea: %s" )' % (self.valor, self.tipo, self.linea)

class NodoAccesoVariable(AST):
	def __init__(self, var, linea, tipo):
		self.var = var
		self.linea = linea
		self.tipo = tipo
		self.compsem()

	def arbol(self):
		return '( "AccesoVariable" "v: %s" "linea: %s" )' % (self.var, self.linea)

class NodoAccesoVector(AST):
	def __init__(self, vect, exp, linea, tipo):
		self.vect = vect
		self.exp = exp
		self.linea = linea
		self.tipoVar = tipo
		self.compsem()

	def arbol(self):
		return '( "AccesoVector" "tipo: %s" "linea: %s" %s\n %s\n)' % (self.tipo, self.linea, self.vect, self.exp)

class Vacio(AST):
	def __init__(self, linea):
		self.linea = linea

	def arbol(self):
		return '( "Vacio (ERROR)" "linea: %s" )' % (self.linea)
