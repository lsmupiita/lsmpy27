#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import random
import pymysql

#Conexion a la base de datos
def abrirConexion():
    cnx = pymysql.connect(
        host="34.68.53.40", port=3306, user="albin",
        passwd="albin", db="albin"
    )
    return cnx


##############################################################
##############################################################
###############APIS FUNCIONALIDAD#############################
##############################################################
##############################################################
def crearCodigo(correo):
    st = str(correo)
    res = "00000000"
    temp = ""
    for ch in st:
        aux = bin(ord(ch))[2:].zfill(8)
        for x in range(8):
            aux2 = (int(aux[x])+int(res[x])) % 10
            temp = temp+str(aux2)
        res = temp
        temp = ""
    return res

def comprobarExistencia(codigo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select correo from profesor where codigo = %s")
    cursor.execute(query,(codigo,))
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    if len(respuesta)!=0:
        respuesta = "Correcto"
    else:
        respuesta = "Incorrecto"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def comprobarExistenciaCorreo(correo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select correo from profesor where correo = %s")
    cursor.execute(query,(correo,))
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    if len(respuesta)!=0:
        respuesta = "Correcto"
    else:
        respuesta = "Incorrecto"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def generarCodigo(correo):
    respuesta=""
    cnx =abrirConexion()

    cursor = cnx.cursor()
    query=("select codigo from profesor where correo = %s")
    cursor.execute(query,correo)
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
        
    if len(respuesta)!=0:
        respuesta = respuesta
    else:
        respuesta = "No existe el correo solicitado"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def numeroAlumnos(codigo):
    respuesta=""
    cnx =abrirConexion()

    cursor = cnx.cursor()
    query=("select alumnos from profesor where codigo = %s")
    cursor.execute(query,codigo)
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def listaAlumnos(codigo):
    respuesta=list()
    cnx =abrirConexion()

    cursor = cnx.cursor()
    query=("select correo from alumno where clase = %s")
    cursor.execute(query,codigo)
    results = cursor.fetchall()
    for row in results:
        respuesta.append(row[0])
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta


def registroProfesor(correo):
    error=False
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("insert into profesor (correo, codigo, alumnos)values(%s,%s,0)")
    try:
        cursor.execute(query,(correo, crearCodigo(correo)))
    except:
        error=True
    if error:
        respuesta="El correo ya existe"
    else:
        respuesta="Registro exitoso"

    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def existenciaAlumno(correo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select correo from alumno where correo = %s")
    cursor.execute(query,(correo,))
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    if len(respuesta)!=0:
        respuesta = "Correcto"
    else:
        respuesta = "Incorrecto"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def buscarClase(codigo,correo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select clase from alumno where clase = %s and correo=%s")
    cursor.execute(query,(codigo,correo))
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    if len(respuesta)!=0:
        respuesta = "Correcto"
    else:
        respuesta = "Incorrecto"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta


def registroAlumno(nombre,apellidoP,apellidoM,correo):
    if existenciaAlumno(correo)!="Correcto":
        cnx =abrirConexion()
        cursor = cnx.cursor()
        query=("insert into alumno (nombre, apellidoP, apellidoM, correo, clase) values(%s,%s,%s,%s,%s)")
        cursor.execute(query, (nombre,apellidoP,apellidoM,correo,"00000000") )
        respuesta = "Registro exitoso"
        cursor.close()
        cnx.commit()
        cnx.close()
    else:
        respuesta= "El correo ya existe"
    return respuesta

def entrarClase(codigo,correo):
    respuesta=""
    if existenciaAlumno(correo)=="Correcto":
        if comprobarExistencia(codigo)=="Correcto":
            if buscarClase(codigo,correo)=="Incorrecto":
                cnx =abrirConexion()
                cursor = cnx.cursor()
                query=("select alumnos from profesor where codigo = %s")
                cursor.execute(query,codigo)
                results = cursor.fetchall()
                for row in results:
                    alumnos = row[0]
                alumnos+=1
                query=("update profesor set alumnos=%s where codigo=%s")
                cursor.execute(query,(alumnos,codigo))
                query=("update alumno set clase=%s where correo=%s")
                cursor.execute(query,(codigo,correo))
                cursor.close()
                cnx.commit()
                cnx.close()
                respuesta="Bienvenido"
            else:
                respuesta="Ya estas dentro de esta clase"
        else:
            respuesta="No existe una clase con este código"
    else:
        respuesta="No existe el correo ingresado"
    return respuesta

def salirClase(codigo,correo):
    respuesta=""
    if existenciaAlumno(correo)=="Correcto":
        if comprobarExistencia(codigo)=="Correcto":
            if buscarClase(codigo,correo)=="Correcto":
                cnx =abrirConexion()
                cursor = cnx.cursor()
                query=("select alumnos from profesor where codigo = %s")
                cursor.execute(query,codigo)
                results = cursor.fetchall()
                for row in results:
                    alumnos = row[0]
                alumnos-=1
                query=("update profesor set alumnos=%s where codigo=%s")
                cursor.execute(query,(alumnos,codigo))
                query=("update alumno set clase=%s where correo=%s")
                cursor.execute(query,("00000000",correo))
                cursor.close()
                cnx.commit()
                cnx.close()
                respuesta="Saliste con exito"
            else:
                respuesta="No estas dentro de esta clase"
        else:
            respuesta="No existe una clase con este código"
    else:
        respuesta="No existe el correo ingresado"
    return respuesta

def terminarClase(codigo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("update profesor set alumnos=%s where codigo=%s")
    cursor.execute(query,("0",codigo))
    query=("update alumno set clase=%s where clase=%s")
    cursor.execute(query,("00000000",codigo))
    cursor.close()
    cnx.commit()
    cnx.close()
    respuesta="Termino con exito"
    return respuesta



##############################################################
##############################################################
###############      LSM        #############################
##############################################################
##############################################################

# Para buscar una palabra (actualmente solo busca por LEMMA)
def buscarPalabra(tupla):
    resultado = []

    cnx = abrirConexion()
    cursor = cnx.cursor()

    lemma = tupla[0]
    etiqueta = tupla[1]
    colocacion = tupla[2]

    #print 'Entra a consulta: ', lemma.encode('utf-8')

    if colocacion == -1:
        query = ("SELECT palabra FROM general WHERE lemma LIKE %s AND etiqueta LIKE %s LIMIT 1")
        cursor.execute(query, (lemma,etiqueta[0]+'%'))

        # Llena una lista con el resultado de la busqueda
        for palabra in cursor:
            #print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
            resultado.append(palabra)

        # Si no encontro nada
        if len(resultado) == 0:
            # Revisa la tabla de sinonimos lsm
            query = ("SELECT id_general FROM sinonimoslsm WHERE lemma LIKE %s AND etiqueta LIKE %s LIMIT 1")
            cursor.execute(query, (lemma,etiqueta[0]+'%'))
            id_general = cursor.fetchone()
            if id_general: # Si encontro algo en la tabla de sinonimoslsm
                query = ("SELECT palabra FROM general WHERE id = %s LIMIT 1")
                cursor.execute(query, id_general)   
                for palabra in cursor:
                    #print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                    resultado.append(palabra)
            else:  # Si no encotro nada en sinonimos lsm
                # Revisa la tabla de sinonimos en espanol
                query = ("SELECT id_general FROM sinonimosespanol WHERE lemma LIKE %s AND etiqueta LIKE %s LIMIT 1")
                cursor.execute(query, (lemma,etiqueta[0]+'%'))
                id_general = cursor.fetchone()
                if id_general:
                    query = ("SELECT palabra FROM general WHERE id = %s LIMIT 1")
                    cursor.execute(query, id_general)   
                    for palabra in cursor:
                        #print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                        resultado.append(palabra)
                # Si no hubo coincidencia en sinonimos lo deletrea
                else:
                    for letra in lemma:
                        query = ("SELECT palabra FROM general WHERE lemma LIKE %s LIMIT 1")
                        #print 'BUSCAR: ',letra.encode('utf-8')
                        cursor.execute(query, (letra,))
                        for palabra in cursor:
                            #print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                            resultado.append(palabra)
    else:
        # Revisa la tabla de colocaciones
        query = ("SELECT id_general FROM colocaciones WHERE id = %s LIMIT 1")
        cursor.execute(query, (colocacion,))
        id_general = cursor.fetchone()
        if id_general: # Si encontro algo en la tabla de colocaciones
            query = ("SELECT palabra FROM general WHERE id = %s LIMIT 1")
            cursor.execute(query, id_general)   
            for palabra in cursor:
                #print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                resultado.append(palabra)
        else:
            print 'Error buscando la colocacion'

    cursor.close()
    cnx.commit()
    cnx.close()

    return resultado


def buscarColocacion(tuplaDeTuplas):
    # ( (pal1, tag1), (pal2, tag2) )
    cnx = abrirConexion()
    cursor = cnx.cursor()
    resultado = -1
    reglaFinal = -1
    # Buscar en la tabla de colocaciones
    if len(tuplaDeTuplas) == 3:
        query = ("SELECT id, etiqueta_1, etiqueta_2, etiqueta_3, regla FROM colocaciones WHERE palabra_1 LIKE %s AND palabra_2 LIKE %s AND palabra_3 LIKE %s")
        cursor.execute(query, ( tuplaDeTuplas[0][0] , tuplaDeTuplas[1][0], tuplaDeTuplas[2][0],))
        # Iterar resutlados
        for (id, etiqueta1, etiqueta2, etiqueta3, regla) in cursor:
            
            tag1=tuplaDeTuplas[0][1]
            tag2=tuplaDeTuplas[1][1]
            tag3=tuplaDeTuplas[2][1]
            if tag1[0]=="V":
                tag1=tag1[0:3]
            if tag2[0]=="V":
                tag2=tag2[0:3]
            if tag3[0]=="V":
                tag3=tag3[0:3]

            if regla == "1":
                if etiqueta1 == tag1:
                    reglaFinal = regla
                    resultado = id
            elif regla == "2":
                if etiqueta2 == tag2:
                    reglaFinal = regla
                    resultado = id
            elif regla == "3":
                if etiqueta3 == tag3:
                    reglaFinal = regla
                    resultado = id
    else:
        query = ("SELECT id, etiqueta_1, etiqueta_2, etiqueta_3, regla FROM colocaciones WHERE palabra_1 LIKE %s AND palabra_2 LIKE %s")
        cursor.execute(query, ( tuplaDeTuplas[0][0] , tuplaDeTuplas[1][0],))
        # Iterar resutlados
        for (id, etiqueta1, etiqueta2, etiqueta3, regla) in cursor:
            tag1=tuplaDeTuplas[0][1]
            tag2=tuplaDeTuplas[1][1]
            if tag1[0]=="V":
                tag1=tag1[0:3]
            if tag2[0]=="V":
                tag2=tag2[0:3]
            if regla == "1":
                if etiqueta1 == tag1:
                    reglaFinal = regla
                    resultado = id
            elif regla == "2":
                if etiqueta2 == tag2:
                    reglaFinal = regla
                    resultado = id

    # id, palabra1, palabra2, palabra3, etiqueta1, etiqueta2, etiqueta3, regla
    cursor.close()
    cnx.commit()
    cnx.close()
    return (resultado, int(reglaFinal))
