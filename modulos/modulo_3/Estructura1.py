#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import logging
logger = logging.getLogger(__name__)
from Trees import *

class Parser_Estructura_1(object):
    # Definir los tokens
    tokens               = ('Determinante', 'Sustantivo', 'Verbo', 'AdjetivoCalif', 'Adverbio')
    t_Determinante       = r'[D|P][A-Z0-9]+'
    t_Sustantivo         = r'N[A-Z0-9]+'
    t_Verbo              = r'V[A-Z0-9]+'
    t_AdjetivoCalif      = r'AQ[A-Z0-9]+'
    t_Adverbio           = r'R[A-Z0-9]+'
    t_ignore             = " "

    def t_error(self, t):
        # print "Skipping %s " % t
        t.lexer.skip(1)

    def __init__(self):
        self.arbol = None
        self.nodos = []

    def p_Oracion(self, t):
        """Oracion : SN SV"""
        o = Nodo('O', None)
        o.derecha = self.nodos.pop()
        o.izquierda = self.nodos.pop()
        self.arbol = Arbol(o)

    def p_SN(self, t):
        """SN : Determinante Sustantivo"""
        sn = Nodo('SN', None)
        sn.izquierda = Nodo(t[1], self.mapToOriginalValues(t[1]))
        sn.derecha = Nodo(t[2], self.mapToOriginalValues(t[2]))
        self.nodos.append(sn)

    def p_SN1(self, t):
        """SN : Determinante"""
        sn = Nodo('SN', None)
        sn.centro = Nodo(t[1], self.mapToOriginalValues(t[1]))
        self.nodos.append(sn)

    def p_SV(self, t):
        """SV : Verbo AdjetivoCalif
              | Verbo Adverbio
              | Verbo Sustantivo"""
        sv = Nodo('SV', None)
        sv.izquierda = Nodo(t[1], self.mapToOriginalValues(t[1]))
        sv.derecha = Nodo(t[2], self.mapToOriginalValues(t[2]))
        self.nodos.append(sv)

    def p_SV1(self, t):
        """SV : Verbo SAdv"""
        sv = Nodo('SV', None)
        sv.izquierda = Nodo(t[1], self.mapToOriginalValues(t[1]))
        sv.derecha = self.nodos.pop()
        self.nodos.append(sv)

    def p_SAdv(self, t):
        """SAdv : Adverbio AdjetivoCalif"""
        sv = Nodo('SV', None)
        sv.izquierda = Nodo(t[1], self.mapToOriginalValues(t[1]))
        sv.derecha = Nodo(t[2], self.mapToOriginalValues(t[2]))
        self.nodos.append(sv)

    def p_error(self, t):
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
        # Build
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self, debug=False)
        self.listaOriginal = data[:]
         # Build oracion
        oracion = " ".join( [l[1] for l in data] )
        # Parse
        self.parser.parse(oracion, lexer=self.lexer)
        return self.arbol
