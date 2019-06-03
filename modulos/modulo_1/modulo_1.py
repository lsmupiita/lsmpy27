#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import sys
import dataBase

def tokenLemmaColoc(tk, sp, sid, mf, tg, sen, parser, dep, text):
  """ Separa oraciones, lematiza, etiqueta y busca colocaciones
  Args:
      tk, sp, sid, mf, tg, sen, parser, dep: elementos de Freeling
      text: cadena de texto a analizar
  Returns:
      Una lista de tuplas con el formato (lemma, etiqueta, id_colocacion, palabra_original)
      Si la tupla no es una colocacion, se regresa un -1
  """
  resultado = list()
  # Obtencion de oraciones
  text = unicode(text, 'utf-8')
  text = text if text.endswith('.') else (text + '.')
  l = tk.tokenize(text);
  # Lematizar
  ls = sp.split(sid,l,False);
  ls = mf.analyze(ls);
  ls = tg.analyze(ls);
  ls = sen.analyze(ls);
  ls = parser.analyze(ls);
  ls = dep.analyze(ls);
  for s in ls :
    ws = s.get_words();
    for w in ws :
      # for each analysis
      a = w.get_analysis()[0]
      # TODO tambien quitar todos los signos de puntuacion, Tambien de intorrgacion?
      if a.get_lemma() != ".":
        if a.get_tag()[0] == 'A':
          tag = a.get_tag()[:3]
        elif a.get_tag()[0] == 'R':
          tag = a.get_tag()[:2]
        elif a.get_tag()[0] == 'D':
          tag = a.get_tag()[:3]
        elif a.get_tag()[0] == 'N':
          tag = a.get_tag()[:6]
        elif a.get_tag()[0] == 'V':
          tag = a.get_tag()[:4] 
        elif a.get_tag()[0] == 'P':
          tag = a.get_tag()[:3]
        elif a.get_tag()[0] == 'C':
          tag = a.get_tag()[:2]
        elif a.get_tag()[0] == 'I':
          tag = a.get_tag()[:2]
        elif a.get_tag()[0] == 'S':
          tag = a.get_tag()[:3]
        elif a.get_tag()[0] == 'F':
          tag = a.get_tag()[:2]
        elif a.get_tag()[0] == 'Z':
            tag = a.get_tag()[:2]
        # Guardar (lemma, etiqueta, id_colocacion)
        resultado.append( (a.get_lemma(), tag, -1, w.get_form()) )
        print "resultado"
        print resultado
    # Iterar hasta que no haya colocaciones
    foundColocacion = True
    while foundColocacion:
      foundColocacion = False
      # Buscar colocaciones de 3 en 3
      index = 0
      for agrupacion in zip(resultado, resultado[1:], resultado[2:]):
        (idColocacion, regla) = dataBase.buscarColocacion(agrupacion)
        # Agrupar en una sola palabra
        if idColocacion != -1:
          parte1 = resultado.pop(index)
          parte2 = resultado.pop(index)
          parte3 = resultado.pop(index)
          nuevaPalabra = parte1[3] + "_" + parte2[3] + "_" + parte3[3]
          nuevoLemma = parte1[0] + "_" + parte2[0] + "_" + parte3[0]
          # Poner etiqueta de acuerdo a la regla
          colTag = ""
          if regla == 1:
            colTag = parte1[1]
          elif regla == 2:
            colTag = parte2[1]
          else:
            colTag = parte3[1]
          nuevaTupla = (nuevoLemma, colTag, idColocacion, nuevaPalabra)
          resultado.insert(index, nuevaTupla)
          # Volver a iterar
          foundColocacion = True
          break
        index = index + 1
      if foundColocacion:
        continue
      # Buscar colocaciones de 2 en 2
      index = 0
      for agrupacion in zip(resultado, resultado[1:]):
        (idColocacion, regla) = dataBase.buscarColocacion(agrupacion)
        # Agrupar en una sola palabra
        if idColocacion != -1:
          parte1 = resultado.pop(index)
          parte2 = resultado.pop(index)
          nuevaPalabra = parte1[3] + "_" + parte2[3]
          nuevoLemma = parte1[0] + "_" + parte2[0]
          # Poner etiqueta de acuerdo a la regla
          colTag = ""
          if regla == 1:
            colTag = parte1[1]
          elif regla == 2:
            colTag = parte2[1]
          nuevaTupla = (nuevoLemma, colTag, idColocacion, nuevaPalabra)
          resultado.insert(index, nuevaTupla)
          # Volver a iterar
          foundColocacion = True
          break
        index = index + 1
      if foundColocacion:
        continue

  # Regresar
  #sp.close_session(sid);
  return resultado


    
