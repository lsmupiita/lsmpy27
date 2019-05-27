import random
import pymysql
import operaciones

#Conexion a la base de datos
def abrirConexion():
    cnx = pymysql.connect(
        host="104.198.31.228", port=3306, user="lsmupiita",
        passwd="lsmupiita", db="lsmupiita"
    )
    return cnx
##############################################################
##############################################################
###############APIS FUNCIONALIDAD#############################
##############################################################
##############################################################

def comprobarExistencia(codigo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select correo from usuario where codigo = %s")
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

def generarCodigo(correo):
    respuesta=""
    cnx =abrirConexion()

    cursor = cnx.cursor()
    query=("select codigo from usuario where correo = %s")
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


def nuevoregistro(correo):
    respuesta=""
    if len(generarCodigo(correo))!=8:
        cnx =abrirConexion()
        cursor = cnx.cursor()
        query=("insert into usuario values(%s,%s)")
        cursor.execute(query,(correo, operaciones.crearCodigo(correo)))
        respuesta = "Registro exitoso"
        cursor.close()
        cnx.commit()
        cnx.close()
    else:
        respuesta = "El correo ya existe"

    return respuesta
