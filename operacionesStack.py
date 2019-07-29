#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import dataBase

"""
def unirLista(codigo,traduccion,lista):
    alumnos=dataBase.numeroAlumnos(codigo)
    resultado=list()
    aux=[codigo,alumnos,traduccion]
    resultado=lista+aux
    return resultado"""

def unirLista(codigo,traduccion,lista):
    if len(traduccion)>0:
        alumnos=dataBase.listaAlumnos(codigo)
        resultado=list()
        aux=[codigo,alumnos,traduccion]
        resultado=lista+aux
        print resultado
        return resultado
    return lista

def buscarTraduccion(codigo,lista):
    indice=0
    for x in lista:
        if x==codigo:
            return indice
        indice+=1
    return "Sin coincidencia"

def validarStack(codigo,stack,correo):
    indice=buscarTraduccion(codigo,stack)
    if indice!="Sin coincidencia":
        alumnos=stack[indice+1]
        palabras=stack[indice+2]
        if correo in alumnos:
            if len(alumnos)!=1:
                print stack[indice+1]
                stack[indice+1].remove(correo)
                print stack[indice+1]
                return [palabras,stack]
            else:
                stack.pop(indice+2)
                stack.pop(indice+1)
                stack.pop(indice)
                return [palabras,stack]
        else:
            return [['sin traduccion'],stack]
    else:
        return [['sin traduccion'],stack]