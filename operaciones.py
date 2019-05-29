# -*- coding: utf-8 -*-

import freeling
import sys
# Para hacer operaciones con la BD
import dataBase
# Importar modulos
from modulos.modulo_1.modulo_1 import *
from modulos.modulo_2.modulo_2 import *
from modulos.modulo_3.modulo_3 import *

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


def consultarLista(listaArbol):
    lista = []
    listaBD = []
    # Busca las imagenes contenidas en la lista
    for tupla in listaArbol:
        busq = bd.buscarPalabra(tupla)
        # El resultado puede ser una lista (si fue deletreada), itera sobre ella
        for fila in busq:
            # Guarda la ruta de la imagen
            img = fila[0].decode('utf-8').upper() + '/' + \
                fila[1].decode('utf-8')
            lista.append(img)
            # Guarda la palabra como fue obtenida de la BD
            listaBD.append(fila[0])
    return (lista, listaBD)


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
                        if palabraOriginal[-1] == 's' and palabraOriginal[-2] == 'e':
                            palabraComp = palabraOriginal[:-2]
                        else:
                            palabraComp = palabraOriginal[:-1]
                    else:
                        palabraComp = palabraOriginal
                    # Compara con el lemma, si no es el mismo lemma añade la seña mujer
                    if palabraComp != lemma:
                        lista.append(('mujer', 'NCFS00', colocacion))
                if numero == 'P':  # Añade seña de muchos si es plural
                    lista.append(('mucho', 'RG', colocacion))
            else:
                lista.append((lemma, etiqueta, colocacion))
        else:
            lista.append((lemma, etiqueta, colocacion))
    return lista

# Inicializar Freeling


def iniciarFreeling():
    # "default" no funciono aqui y se tuvo que cambiar a "es_MX.UTF-8"
    # este valor se obtuvo de poner en la terminal "locale"
    freeling.util_init_locale("es_MX.UTF-8")
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
    tipo = "informal"
    if len(texto) != 0 and texto is not None and texto != "":
            procesado = tokenLemmaColoc(tk, sp, sid, mf, tg, sen, parser, dep, texto)
            # PONE ACEITUNA SI EL ARBOL NO ES VALIDO
            listaTraducir = [('aceituna', 'NCFS00', -1), ]
            # Modulo 2
            config = getConfigFile()  # Obtener el archivo de configuracion
            sinStopwords = quitarStopwords(procesado, config, esFormal=(tipo == 'formal'))
            # Modulo 3
            arbolValido = ''
            pasarARicardo = list(sinStopwords)
            print pasarARicardo
            pruebaReturn = modulo_main(pasarARicardo)
            if pruebaReturn is not None:
                (inOrden, posOrden) = modulo_main(pasarARicardo)
                if inOrden is not None and posOrden is not None:
                    if len(inOrden) > 0 or len(posOrden) > 0:
                        print "LISTA: ", inOrden
                        # Revisa resultado de lista de prueba
                        if tipo == 'formal':
                            listaTraducir = hacerListaTraducir(inOrden)
                        else:
                            listaTraducir = hacerListaTraducir(posOrden)
                    else:
                        arbolValido = 'La oración no coincide con ninguna gramática registrada. Se hará una traducción literal'
                        listaTraducir = hacerListaTraducir(sinStopwords)
                        print "Arbol no encontrado"
                else:
                    arbolValido = 'La oración no coincide con ninguna gramática registrada. Se hará una traducción literal'
                    listaTraducir = hacerListaTraducir(sinStopwords)

                    print "Arbol no encontrado"

            print "#######################################"
            print "#######################################"
            print "#######################################"
            print "texto ingresado "+texto
            palabras=""
            for tupla in listaTraducir:
                lemma=tupla[0]
                palabras+=lemma+","
                print lemma
            print palabras


    return palabras