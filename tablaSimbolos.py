# Wrapper para la tabla de simbolos. Nos permite acceder a ella directamente desde cualquier fichero que lo necesitemos,
# y añadir métodos para manipularla de forma "limpia" y ordenada.

# Tabla de símbolos propiamente dicha

tablaSimbolos = {}

# Nombres de identificadores no validos
PR = frozenset(["PROGRAMA", "VAR", "VECTOR", "DE", "ENTERO", "REAL", "BOOLEANO", "INICIO","PROC","FUNCION",
                      "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "CIERTO", "FALSO","Y","O","NO" ])

# Metodos:

# añadeSimbolo: intenta añadir un símbolo a la tabla.
# Devuelve TRUE si se añade con éxito o FALSE si hay un error añadiendolo (el símbolo ya existe o es un símbolo no valido)
def anadeSimbolo(simbolo, tipo):
    
    global tablaSimbolos

    # Comprobamos si el simbolo es valido
    if simbolo.upper() in PR:
        # Simbolo invalido: error
        return "invalido"
    else:
        # Si el simbolo es valido, comprobamos si ya existe previamente
        if simbolo in tablaSimbolos:
            # Simbolo duplicado: error
            return "duplicado"
        else:
            # Añadido con exito
            tablaSimbolos = {"tipo": tipo}
            return True

# actualizaInfo: intenta añadir información a un símbolo de la tabla.
# Devuelve TRUE si se puede añadir con éxito, o FALSE si hay un error añadiendola (el símbolo no existe)
def actualizaInfo(simbolo, nombreInfo, valorInfo):

    if simbolo not in tablaSimbolos:
        # Error, falta simbolo
        return False
    else:
        # Se puede añadir con éxito la información
        tablaSimbolos[simbolo][nombreInfo] = valorInfo
        return True

# RecuperaInfo: intenta recuperar información sobre un símbolo de la tabla.
# Devuelve la información apropiada si existe, o None en caso contrario
def devuelveInfo(simbolo, nombreInfo):

    if simbolo not in tablaSimbolos:
        # Error, el simbolo no existe
        return None
    else:
        # Devuelve el valor que contenga el diccionario
        return tablaSimbolos[simbolo].get(nombreInfo)
