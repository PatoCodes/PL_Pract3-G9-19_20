#!/usr/bin/env python
# -*- coding: latin-1 -*-

class Error(Exception):
  def __init__(self, mensaje):
    self.mensaje= mensaje

  def __str__(self):
    return self.mensaje

class ErrorLexico(Error):
  def __init__(self, mensaje):
    self.mensaje= "ERROR LEX: %s" % mensaje

class ErrorSintactico(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error sint�ctico: %s" % mensaje

class ErrorSemantico(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error sem�ntico: %s" % mensaje

class ErrorEjecucion(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error de ejecuci�n: %s" % mensaje
