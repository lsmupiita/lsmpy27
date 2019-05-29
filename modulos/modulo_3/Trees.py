# -*- coding: utf-8 -*-
import re

class Nodo:

    def __init__(self, etiqueta = None, tupla=None):
        self.etiqueta = etiqueta
        if tupla:
            self.lemma = tupla[0]
            self.colocacion = tupla[1]
            self.original = tupla[2]
        else:
            self.lemma = None
            self.colocacion = None
            self.original = None
        self.izquierda = None
        self.derecha = None
        self.centro = None

    def __str__(self):
        return "<Nodo %s, %s, %s>" % (self.etiqueta, self.lemma, self.colocacion)

    def __repr__(self):
        return "<Nodo %s, %s, %s>" % (self.etiqueta, self.lemma, self.colocacion)
         

class Arbol:

    def __init__(self,arbol):
        self.raiz = arbol
        self.innorden = []
        self.posorden = []
        self.leerInnorden(self.raiz)
        self.leerPosorden(self.raiz)


    def leerInnorden(self, raiz):
        if raiz:
            self.leerInnorden(raiz.izquierda)
            self.leerInnorden(raiz.centro)
            if raiz.lemma and raiz.etiqueta and raiz.colocacion:
                if not re.match("DA",raiz.etiqueta):
                    self.innorden.append((raiz.lemma,raiz.etiqueta,raiz.colocacion,raiz.original))
            self.leerInnorden(raiz.derecha)

    def leerPosorden(self, raiz):
        if raiz:
            self.leerPosorden(raiz.derecha)
            self.leerPosorden(raiz.izquierda)
            self.leerPosorden(raiz.centro)
            if raiz.lemma and raiz.etiqueta and raiz.colocacion:
                if not re.match("((S|s)er)|((E|e)star)", raiz.lemma) and not re.match("DA",raiz.etiqueta) and not re.match("DP1",raiz.etiqueta) and not re.match("PP1",raiz.etiqueta):
                    self.posorden.append((raiz.lemma,raiz.etiqueta,raiz.colocacion,raiz.original))
