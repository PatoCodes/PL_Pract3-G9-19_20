# Wrapper para la tabla de simbolos. Nos permite acceder a ella directamente desde cualquier fichero que lo necesitemos,
# y añadir métodos para manipularla de forma "limpia" y ordenada.

# Tabla de símbolos propiamente dicha

tablaSimbolos = {}

# Metodos:

# añadeSimbolo: intenta añadir un símbolo a la tabla.
# Devuelve TRUE si se añade con éxito o FALSE si hay un error añadiendolo (el símbolo ya existe)
def añadeSimbolo(simbolo, tipo):
    
    if simbolo not in tablaSimbolos:
        # Añadido con exito
        tablaSimbolos = {"tipo": tipo}
        return True
    # Problema al añadirlo
    else:
        return False

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
