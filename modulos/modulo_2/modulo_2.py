#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

class ConfigFileError(Exception):
    pass

def getConfigFile(ruta = "modulos/modulo_2/config.json"):
    """ Genera un archivo de configuracion a partir de unas reglas dadas
    Args:
        ruta: ruta del JSON a leer con las reglas. default: ./config.json
    Returns:
        un diccionario con las reglas implementadas
    Raises:
        ConfigFileError: cuando el archivo de configuracion contiene algun error
    """
    # Leer el archivo de configuración
    config = dict()
    with open(ruta) as data_file:    
        configRaw = json.load(data_file)
        # Procesar en busca de errores y cosas asi
        for rule in configRaw:
            tag = rule["etiqueta"]
            # Inicializar contenedor para esta etiqueta
            if not config.has_key(tag):
                config[tag] = dict()
                config[tag]["formal"] = dict()
                # config[tag]["formal"]["dejar"] = list()
                # config[tag]["formal"]["quitar"] = list()
                config[tag]["formal"]["transformar"] = dict()
                config[tag]["informal"] = dict()
                # config[tag]["informal"]["dejar"] = list()
                # config[tag]["informal"]["quitar"] = list()
                config[tag]["informal"]["transformar"] = dict()
            # Leer si es para formal o informal
            isFormal = rule.get("formal", True)
            isInformal = rule.get("informal", True)
            # Buscar errores en los arreglos
            if not( rule.has_key("dejar") \
                or rule.has_key("quitar") \
                or rule.has_key("transformar") ):
                raise ConfigFileError("Una regla para "+tag+" no especifica que quitar, dejar o transformar")
            # Leer que hay que dejar
            if rule.has_key("dejar"):
                if isFormal:
                    # Buscar conflictos en donde haya contradicciones
                    if config[tag]["formal"].has_key("quitar"):
                        for lemma in rule["dejar"]:
                            if lemma in config[tag]["formal"]["quitar"] \
                                or lemma in config[tag]["formal"]["transformar"]:
                                raise ConfigFileError("El lemma "+lemma+" de "+tag+" tiene conflictos")
                    # Inicializar la lista de ser necesario
                    if not config[tag]["formal"].has_key("dejar"):
                        config[tag]["formal"]["dejar"] = list()    
                    config[tag]["formal"]["dejar"] = config[tag]["formal"]["dejar"] + rule["dejar"]
                if isInformal:
                    if config[tag]["informal"].has_key("quitar"):
                        for lemma in rule["dejar"]:
                            if lemma in config[tag]["informal"]["quitar"] \
                                or lemma in config[tag]["informal"]["transformar"]:
                                raise ConfigFileError("El lemma "+lemma+" de "+tag+" tiene conflictos")
                    if not config[tag]["informal"].has_key("dejar"):
                        config[tag]["informal"]["dejar"] = list()
                    config[tag]["informal"]["dejar"] = config[tag]["informal"]["dejar"] + rule["dejar"]
            # Leer que hay que quitar
            if rule.has_key("quitar"):
                if isFormal:
                    if config[tag]["formal"].has_key("dejar"):
                        for lemma in rule["quitar"]:
                            if lemma in config[tag]["formal"]["dejar"] \
                                or lemma in config[tag]["formal"]["transformar"]:
                                raise ConfigFileError("El lemma "+lemma+" de "+tag+" tiene conflictos")
                    if not config[tag]["formal"].has_key("quitar"):
                        config[tag]["formal"]["quitar"] = list()    
                    config[tag]["formal"]["quitar"] = config[tag]["formal"]["quitar"] + rule["quitar"]
                if isInformal:
                    if config[tag]["informal"].has_key("dejar"):
                        for lemma in rule["quitar"]:
                            if lemma in config[tag]["informal"]["dejar"] \
                                or lemma in config[tag]["informal"]["transformar"]:
                                raise ConfigFileError("El lemma "+lemma+" de "+tag+" tiene conflictos")
                    if not config[tag]["informal"].has_key("quitar"):
                        config[tag]["informal"]["quitar"] = list()    
                    config[tag]["informal"]["quitar"] = config[tag]["informal"]["quitar"] + rule["quitar"]
            # Leer que hay que transformar
            if rule.has_key("transformar"):
                for transformation in rule["transformar"]:
                    source = transformation["lemmaOrigen"]
                    target = transformation["lemmaDestino"]
                    for s in source:
                        if isFormal:
                            listQuitar = config[tag]["formal"]["quitar"] if config[tag]["formal"].has_key("quitar") else list()
                            listDejar = config[tag]["formal"]["dejar"] if config[tag]["formal"].has_key("dejar") else list()
                            if s in listQuitar or s in listDejar:
                                #print(s + " - "+tag)
                                raise ConfigFileError("El lemma "+s+" de "+tag+" tiene conflictos")
                            config[tag]["formal"]["transformar"][s] = target
                        if isInformal:
                            listQuitar = config[tag]["informal"]["quitar"] if config[tag]["informal"].has_key("quitar") else list()
                            listDejar = config[tag]["informal"]["dejar"] if config[tag]["informal"].has_key("dejar") else list()
                            if s in listQuitar or s in listDejar:
                                raise ConfigFileError("El lemma "+s+" de "+tag+" tiene conflictos")
                            config[tag]["informal"]["transformar"][s] = target
    # TODO Buscar errores generales
    return config

def quitarStopwords(listaOriginal, archivoConfig, esFormal = True):
    """ Elimina los stopwords de acuerdo a una serie de reglas establecidas.
    Args:
        listaOriginal: lista de tuplas (lemma, etiqueta, id_coloc, palabra_original).
        esFormal: indica si la traduccion va a ser formal o informal. default: True
        archivoConfig: diccionario generado por getConfigFile con las reglas a considerar
    Returns:
        una copia de la lista original pero ya con las palabras removidas
    """
    # Procesar
    listaResultante = list()
    for (lemma, tag, id_colocacion, palabra) in listaOriginal:
        # Saltarse si es una colocacion
        if id_colocacion != -1:
            listaResultante.append( (lemma,tag, id_colocacion, palabra) )
            continue
        #print "PROBANDO CON" + lemma
        # Si no es colocacion, continuar
        typeOfTranslation = "formal" if esFormal else "informal"
        tagCopy = tag
        # del tag, solo sacar las primeras letras como corresponda
        tag = getTagPrefix(tag)
        if archivoConfig.has_key(tag):
            # Obtener las reglas para esta etiqueta
            rules = archivoConfig[tag][typeOfTranslation]
            # Buscar la regla adecuada
            if rules["transformar"].has_key(lemma):
                lemma = rules["transformar"][lemma]
            elif rules.has_key("quitar") and not rules.has_key("dejar"):
                if len(rules["quitar"]) == 0:
                    # quitar
                    continue
                else:
                    # buscar para ver si se quita o no se quita
                    if lemma in rules["quitar"]:
                        continue
                    else:
                        pass
            elif rules.has_key("dejar") and not rules.has_key("quitar"):
                if len(rules["dejar"]) == 0:
                    # dejar
                    pass
                else:
                    # buscar para ver si se quita o no se quita
                    if lemma in rules["dejar"]:
                        pass
                    else:
                        continue
            elif len(rules["quitar"]) == 0 and len(rules["dejar"]) == 0:
                # se respeta dejar
                pass
            elif len(rules["quitar"]) > 0 and len(rules["dejar"]) == 0:
                # Si se encuentra en quitar, se quita!
                if lemma in rules["quitar"]:
                    continue
                # Si no, se deja
                else:
                    pass
            elif len(rules["quitar"]) == 0 and len(rules["dejar"]) > 0:
                # Si se encuentra en dejar, se deja!
                if lemma in rules["dejar"]:
                    pass
                # Si no, se quita
                else:
                    continue
            elif len(rules["quitar"]) > 0 and len(rules["dejar"]) > 0:
                # Se supone en la verificacion al generar el archivo
                # config, el mismo lemma no va a estar en los dos
                if lemma in rules["quitar"]:
                    continue
                elif lemma in rules["dejar"]:
                    pass
                else:
                    # Si no se dijo explicitamente que se deje, se quita
                    continue
            else:
                # dejar
                pass
        listaResultante.append( (lemma,tagCopy, id_colocacion, palabra) )
    # Regresar
    return listaResultante

def getTagPrefix(completeTag):
    if completeTag != ".":
        if completeTag.startswith('A'):
            return completeTag[:2]
        elif completeTag.startswith('R'):
            return completeTag[:2]
        elif completeTag.startswith('D'):
            return completeTag[:2]
        elif completeTag.startswith('N'):
            return completeTag[:6]
        elif completeTag.startswith('V'):
            return completeTag[:4] 
        elif completeTag.startswith('P'):
            return completeTag[:2]
        elif completeTag.startswith('C'):
            return completeTag[:2]
        elif completeTag.startswith('I'):
            return completeTag[:2]
        elif completeTag.startswith('S'):
            return completeTag[:2]
        elif completeTag.startswith('F'):
            return completeTag[:2]
        elif completeTag.startswith('Z'):
            return completeTag[:2]
    return completeTag

# lista de listas(enunciados)
# tests = [[( u'aun', u'RG'),( u'ir', u'VMIP1P0'),( u'a', u'SP'),( u'jugar', u'VMN0000'),( u'ajedrez', u'NCMS000'),( u'con', u'SP'),( u'tu', u'DP2CPS'),( u'primo', u'NCMP000'),( u'.', u'Fp'),],[( u'antes_de', u'SP'),( u'ir', u'VMN0000'),( u'a', u'SP'),( u'el', u'DA0FS0'),( u'calle', u'NCFS000'),( u',', u'Fc'),( u'siempre', u'RG'),( u'tomo', u'NCMS000'),( u'uno', u'DI0FS0'),( u'sudadera', u'NCFS000'),( u'.', u'Fp'),],[( u'ni', u'CC'),( u'ayer', u'RG'),( u'ni', u'CC'),( u'nunca', u'RG'),( u'ir', u'VMIP1S0'),( u'a', u'SP'),( u'comer', u'VMN0000'),( u'zanahoria', u'NCFP000'),( u'.', u'Fp'),],[( u'detrás_de', u'SP'),( u'el', u'DA0FS0'),( u'casa', u'NCFS000'),( u'haber', u'VMIP3S0'),( u'mucho', u'DI0MS0'),( u'pasto', u'NCMS000'),( u'excepto', u'SP'),( u'cerca', u'RG'),( u'de', u'SP'),( u'el', u'DA0MS0'),( u'árbol', u'NCMS000'),( u'.', u'Fp'),],[( u'allí', u'RG'),( u'estar', u'VMIP3S0'),( u'el', u'DA0MS0'),( u'libro', u'NCMS000'),( u'que', u'PR0CN00'),( u'estar', u'VAII2S0'),( u'buscar', u'VMG0000'),( u'.', u'Fp'),],[( u'junto_a', u'SP'),( u'tu', u'DP2CSS'),( u'cuaderno', u'NCMS000'),( u'dejar', u'VMIS1S0'),( u'el', u'DA0FS0'),( u'pluma', u'NCFS000'),( u'que', u'PR0CN00'),( u'me', u'PP1CS00'),( u'prestar', u'VMIS2S0'),( u'.', u'Fp'),],[( u'bien', u'RG'),( u'hacer', u'VMP00SM'),( u',', u'Fc'),( u'mi', u'DP1CSS'),( u'amigo', u'NCMS000'),( u'!', u'Fat'),],[( u'si', u'CS'),( u'tú', u'PP2CSN0'),( u'no', u'RN'),( u'ir', u'VMIP2S0'),( u'a', u'SP'),( u'ir', u'VMN0000'),( u'a', u'SP'),( u'el', u'DA0FS0'),( u'fiesta', u'NCFS000'),( u',', u'Fc'),( u'yo', u'PP1CSN0'),( u'tampoco', u'RG'),( u'.', u'Fp'),],[( u'quizá', u'RG'),( u'empezar', u'VMSP3S0'),( u'a', u'SP'),( u'tocar', u'VMN0000'),( u'más', u'RG'),( u'despacio', u'RG'),( u',', u'Fc'),( u'salvo', u'SP'),( u'que', u'PR0CN00'),( u'aquí', u'RG'),( u'decir', u'VMM03P0'),( u'el', u'DA00S0'),( u'contrario', u'NCMS000'),( u'.', u'Fp'),],[( u'encima_de', u'SP'),( u'todo', u'PI0MS00'),( u',', u'Fc'),( u'creer', u'VMIP1S0'),( u'que', u'CS'),( u'nuestro', u'DP1FPP'),( u'familia', u'NCFP000'),( u'no', u'RN'),( u'se', u'P00CN00'),( u'llevar', u'VMIP3P0'),( u'bien', u'RG'),( u'.', u'Fp'),],[( u'qué', u'DE0CN0'),( u'bonito', u'AQ0FS00'),( u'ser', u'VSIP3S0'),( u'tu', u'DP2CSS'),( u'mascota', u'NCFS000'),( u'.', u'Fp'),],[( u'aquel', u'DD0MS0'),( u'día', u'NCMS000'),( u'que', u'PR0CN00'),( u'pensar', u'VMIP1P0'),( u'nunca', u'RG'),( u'llegar', u'VMIC3S0'),( u',', u'Fc'),( u'haber', u'VAIP3S0'),( u'llegar', u'VMP00SM'),( u'.', u'Fp'),],[( u'nuestro', u'DP1MSP'),( u'amor', u'NCMS000'),( u'por', u'SP'),( u'tu', u'DP2CSS'),( u'padre', u'NCMS000'),( u'durar', u'VMIF3S0'),( u'para', u'SP'),( u'siempre', u'RG'),( u'.', u'Fp'),],[( u'este', u'DD0MS0'),( u'[J:??/??/??:??.??:??]', u'W'),( u'planeo', u'NCMS000'),( u'salir', u'VMN0000'),( u'a', u'SP'),( u'correr', u'VMN0000'),( u'con', u'SP'),( u'mi', u'DP1CSS'),( u'perro', u'NCMS000'),( u'.', u'Fp'),],[( u'¿', u'Fia'),( u'qué', u'PT00000'),( u'creer', u'VMIP2S0'),( u'que', u'CS'),( u'deber', u'VMSP1P0'),( u'hacer', u'VMN0000'),( u'a', u'SP'),( u'el', u'DA0MS0'),( u'respecto', u'NCMS000'),( u'?', u'Fit'),],[( u'yo', u'PP1CSN0'),( u'creer', u'VMIP1S0'),( u'que', u'CS'),( u'cualquiera', u'PI0CS00'),( u'poder', u'VMIP3S0'),( u'ir', u'VMN0000'),( u'a', u'SP'),( u'el', u'DA0MS0'),( u'paseo', u'NCMS000'),( u',', u'Fc'),( u'pero', u'CC'),( u'nadie', u'PI0CS00'),( u'poder', u'VMIP3S0'),( u'ir', u'VMN0000'),( u'sin', u'SP'),( u'permiso', u'NCMS000'),( u'.', u'Fp'),],[( u'cuanto', u'RG'),( u'más', u'RG'),( u'me', u'PP1CS00'),( u'esfuerzo', u'NCMS000'),( u',', u'Fc'),( u'mejor', u'AQ0CP00'),( u'resultado', u'NCMP000'),( u'obtener', u'VMIP1S0'),( u'.', u'Fp'),],[( u'creer', u'VMIP1S0'),( u'que', u'CS'),( u'su', u'DP3CSN'),( u'cabeza', u'NCCS000'),( u'ser', u'VSIP3S0'),( u'tan', u'RG'),( u'grande', u'AQ0CS00'),( u'que', u'PR0CN00'),( u'ir', u'VMIP3S0'),( u'a', u'SP'),( u'explotar', u'VMN0000'),( u'.', u'Fp'),],[( u'lejos_de', u'SP'),( u'mejorar', u'VMN0000'),( u'el', u'DA0FP0'),( u'cosa', u'NCFP000'),( u',', u'Fc'),( u'tu', u'DP2CSS'),( u'argumento', u'NCMS000'),( u'estar', u'VAIP3S0'),( u'empeorar', u'VMG0000'),( u'el', u'DA0FS0'),( u'situación', u'NCFS000'),( u'.', u'Fp'),]]
# # Obtener el archivo de configuracion
# config = getConfigFile()
# # Hacer pruebas
# for t in tests:
#     result = quitarStopwords(t, config)
#     print result