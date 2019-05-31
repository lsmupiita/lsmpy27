#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Estructura1 import Parser_Estructura_1
from Estructura2 import Parser_Estructura_2
from Estructura3 import Parser_Estructura_3
from Estructura4 import Parser_Estructura_4

def modulo_main(oracion, debug=False):
    print "aqui esta la oracion que se envia a lo que nos importa"
    print oracion
    readable = " ".join([ x[3] for x in oracion])
    parsers = [Parser_Estructura_1(), Parser_Estructura_2(), Parser_Estructura_3(), Parser_Estructura_4()]
    for parser in parsers:
        # Probar para esta oracion
        arbol = parser.parse(oracion)
        if arbol:
            if debug:
                print "'%s' fue parseado con %s" % (readable, parser.__class__.__name__)
            return (arbol.innorden, arbol.posorden)
    if debug:
        print "'%s' no tiene estructura valida" % (readable)
    return None
