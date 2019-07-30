#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import freeling
# Para hacer operaciones con la BD
import dataBase
# Importar modulos
from modulos.modulo_1.modulo_1 import *
from modulos.modulo_2.modulo_2 import *
#from modulos.modulo_3.modulo_3 import *

# Constantes Freelinsg
FREELINGDIR = "/usr/local"
DATA = FREELINGDIR+"/share/freeling/"
LANG = "es"
tk = None
sp = None
sid = None
mf = None
tg = None
sen = None
parser = None
dep = None

# Consulta una lista de palabras en la BD
def separarNumero(numero):
    numeros=[]
    numero=int(numero)
    centenas=numero/100*100
    tmp = numero % 100
    decenas = tmp / 10*10
    unidades = tmp % 10
    return[centenas,decenas,unidades]

def consultarLista(listaArbol):
    listaBD = []
    # Busca las imagenes contenidas en la lista
    for tupla in listaArbol:
        busq = dataBase.buscarPalabra(tupla)
        # El resultado puede ser una lista (si fue deletreada), itera sobre ella
        for fila in busq:
            # Guarda la palabra como fue obtenida de la BD
            listaBD.append(fila[0])
    #return (lista, listaBD)
    #return (lista, listaBD)
    return listaBD


def hacerListaTraducir(listaArbol):
    lista = []
    for tupla in listaArbol:
        """ PALABRA ORIGINAL """
        palabraOriginal = tupla[3]
        lemma = tupla[0]
        etiqueta = tupla[1]
        colocacion = tupla[2]
        etiqueta = getTagPrefix(etiqueta)
        if colocacion == -1:  # Si no es una colocacion
            if etiqueta[0] == 'N':  # Revisa si es sustantivo para agregar femenino y muchos
                genero = etiqueta[2]
                numero = etiqueta[3]
                lista.append((lemma, etiqueta, colocacion))
                if genero == 'F':  # Si es femenino
                    if numero == 'P':  # Si es plural quitara la s o la es al final de la palabra
                        """
                        if palabraOriginal[-1] == 's' and palabraOriginal[-2] == 'e':
                            palabraComp = palabraOriginal[:-2]
                        else:
                            palabraComp = palabraOriginal[:-1]
                        
                        #palabraComp = palabraOriginal[:-1]
                    else:
                        palabraComp = palabraOriginal"""
                    # Compara con el lemma, si no es el mismo lemma añade la seña mujer
                    #if palabraComp != lemma:
                    if lemma.lower() not in palabraOriginal.lower():
                        lista.append(('mujer', 'NCFS00', colocacion))
                if numero == 'P' and palabraOriginal!="gracias" and palabraOriginal!="rostros":  # Añade seña de muchos si es plural
                    lista.append(('mucho', 'RG', colocacion))
            elif etiqueta[0]=='Z':
                for x in separarNumero(palabraOriginal):
                    lista.append((str(x), 'Z', colocacion))
            else:
                lista.append((lemma, etiqueta, colocacion))
        else:
            lista.append((lemma, etiqueta, colocacion))
    return lista

def acomodarPalabras(listaPalabras):
    lista = []
    listaaux=[]
    for tupla in listaPalabras:
        """ PALABRA ORIGINAL """
        lemma = tupla[0]
        etiqueta = tupla[1]
        colocacion = tupla[2]
        etiqueta = getTagPrefix(etiqueta)
        if etiqueta[0] == 'V':
            lista.append((lemma, etiqueta, colocacion))
        elif lemma=="nueva_españa":
            lista.append(("nuevo", "AQ0", colocacion))
            lista.append(("español", "AQ0", colocacion))
        else:
            listaaux.append((lemma, etiqueta, colocacion))
    
    return listaaux+lista

# Inicializar Freeling


def iniciarFreeling():
    # "default" no funciono aqui y se tuvo que cambiar a "es_MX.UTF-8"
    # este valor se obtuvo de poner en la terminal "locale"
    freeling.util_init_locale("default")
    # create options set for maco analyzer. Default values are Ok, except for data files.
    op = freeling.maco_options("es")
    op.set_data_files("",
                      DATA + "common/punct.dat",
                      DATA + LANG + "/dicc.src",
                      DATA + LANG + "/afixos.dat",
                      "",
                      DATA + LANG + "/locucions.dat",
                      DATA + LANG + "/np.dat",
                      DATA + LANG + "/quantities.dat",
                      DATA + LANG + "/probabilitats.dat")
    # create analyzers
    tk = freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
    sp = freeling.splitter(DATA+LANG+"/splitter.dat")
    sid = sp.open_session()
    mf = freeling.maco(op)
    # activate mmorpho odules to be used in next call
    # select which among created submodules are to be used.
    # default: all created submodules are used
    mf.set_active_options(False, True, True, True, True,
                          True, False, True, True, True, True, True)
    # create tagger, sense anotator, and parsers
    tg = freeling.hmm_tagger(DATA+LANG+"/tagger.dat", False, 5)
    sen = freeling.senses(DATA+LANG+"/senses.dat")
    parser = freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat")
    dep = freeling.dep_txala(
        DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol())
    return(tk, sp, sid, mf, tg, sen, parser, dep)


(tk, sp, sid, mf, tg, sen, parser, dep) = iniciarFreeling()


def traduccionAutomatica(texto):
    tipo = "formal"
    if len(texto) != 0 and texto is not None and texto != "":
            procesado = tokenLemmaColoc(tk, sp, sid, mf, tg, sen, parser, dep, texto)
            print "Procesamiento de Lenguaje Natural"
            print "Tokenizado, Lemmatizado y Detección de Colocaciones"
            print procesado
            # Modulo 2
            config = getConfigFile()  # Obtener el archivo de configuracion
            procesado=colocBusc(procesado)
            print "Texto despues de busqueda de colocaciones"
            print procesado
            sinStopwords = quitarStopwords(procesado, config, esFormal=(tipo == 'formal'))
            listaTraducir= colocBusc(sinStopwords)
            print "Texto sin StopWords"
            print listaTraducir
            listaTraducir = hacerListaTraducir(listaTraducir)
            print "Agregacion del femenino y el plural a las palabras"
            print listaTraducir
            respuesta=acomodarPalabras(listaTraducir)
            print "Acomodo de los elementos de la oracion con base en las reglas establecidas"
            print respuesta
            respuesta=consultarLista(respuesta)
            print "Oracion resultante con las palabras recopiladas de una clase de historia"
            print respuesta
            
    return respuesta







