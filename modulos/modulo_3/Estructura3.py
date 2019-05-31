#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from Trees import *

class Parser_Estructura_3:
    # Definir los tokens
    tokens = ('Determinante', 'Sustantivo', 'Verbo')
    t_Determinante      = r'[D|P][A-Z0-9]+'
    t_Sustantivo        = r'N[A-Z0-9]+'
    t_Verbo             = r'V[A-Z0-9]+'
    t_ignore            = " "

    def t_error(self, t):
        # print "Skipping %s " % t
        t.lexer.skip(1)

    def __init__(self):
        self.arbol = None
        self.nodos = []

    def p_Oracion(self, t):
        """Oracion : SV SN"""
        o = Nodo('O', None)
        o.derecha = self.nodos.pop()
        o.izquierda = self.nodos.pop()
        self.arbol = Arbol(o)
        

    def p_Verbo(self, t):
        """SV : Verbo"""
        etiqueta = t[1]
        sn = Nodo('SV')
        sn.centro = Nodo(etiqueta, self.mapToOriginalValues(etiqueta))
        self.nodos.append(sn)

    def p_SN(self, t):
        """SN : Determinante Sustantivo"""
        sv = Nodo('SN')
        etiqueta_determinante = t[1]
        etiqueta_sustantivo = t[2]
        sv.izquierda = Nodo(etiqueta_determinante, self.mapToOriginalValues(etiqueta_determinante))
        sv.derecha = Nodo(etiqueta_sustantivo, self.mapToOriginalValues(etiqueta_sustantivo))
        self.nodos.append(sv)

    def p_error(self, t):
        # print "Error en %s" % t
        pass

    # Buscar los valores originales del lemma y si es colocacion o no de esta etiqueta
    def mapToOriginalValues(self, etiqueta):
        for tupla in self.listaOriginal:
            # Extraer tupla
            lemma = tupla[0]
            etiqueta_original = tupla[1]
            es_colocacion = tupla[2]
            palabra_original = tupla[3]
            if etiqueta_original == etiqueta:
                # Borrar original
                self.listaOriginal.remove(tupla)
                return (lemma, es_colocacion, palabra_original)
        return None

    def parse(self, data):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self, debug=False)
        self.listaOriginal = data[:]
         # Build oracion
        oracion = " ".join( [l[1] for l in data] )
        # Parse
        self.parser.parse(oracion)
        return self.arbol
