#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print "ñaña app"

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import dataBase, moduloFreeling, operacionesStack

import threading
import Queue as queue
######################################################
######################################################
def dosomething(oracion):
    return moduloFreeling.traduccionAutomatica(oracion)


########################################################
#######################################################
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
oracionTraducida=["Sin oracion"]
token="00000000"
stack=list()

class EnviarTraduccion(Resource):
    def post(self):
        parser.add_argument('codigo', type=str)
        parser.add_argument('oracion', type=str)
        args = parser.parse_args()
        codigo=args['codigo']
    
        que = queue.Queue()
        thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, args['oracion']))
        thr.start()
        thr.join()
        while not que.empty():
            global oracionTraducida
            oracionTraducida=que.get()
            global stack
            stack=operacionesStack.unirLista(codigo,oracionTraducida,stack)
        return {'palabras':stack}

class RecibirTraduccion(Resource):
    def post(self):
            parser.add_argument('codigo', type=str)
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            global stack
            [palabras,stack]=operacionesStack.validarStack(args['codigo'],stack,args['correo'])
            return {'traduccion': palabras}

    
class Codigo(Resource):
    def post(self):
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            return { 'codigo':dataBase.generarCodigo(args['correo']) }

class Clase(Resource):
    def post(self):
            parser.add_argument('codigo', type=str)
            parser.add_argument('tipo', type=str)
            parser.add_argument('accion', type=str)
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            if args['tipo']=="alumno" and args['accion']=="entrar":
                return { 'mensaje':dataBase.entrarClase(args['codigo'],args['correo']) }
            elif args['tipo']=="alumno" and args['accion']=="salir":
                return { 'mensaje':dataBase.salirClase(args['codigo'],args['correo']) }
            elif args['tipo']=="profesor" and args['accion']=="terminar":
                return { 'mensaje':dataBase.terminarClase(args['codigo']) }

class LoginAlumno(Resource):
    def post(self):
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            return { 'mensaje':dataBase.existenciaAlumno(args['correo']) }

class RegistroProfesor(Resource):
    def post(self):
        parser.add_argument('correo',type=str)  
        args = parser.parse_args()
        return {'mensaje':dataBase.registroProfesor(args['correo'])}   

class RegistroAlumno(Resource):
    def post(self):
        parser.add_argument('nombre', type=str)
        parser.add_argument('apellidoP', type=str) 
        parser.add_argument('apellidoM', type=str) 
        parser.add_argument('correo', type=str)
        args = parser.parse_args()
        return {'mensaje':dataBase.registroAlumno(args['nombre'],args['apellidoP'],args['apellidoM'],args['correo'])}   

class Prueba(Resource):
    def post(self):
        parser.add_argument('oracion',type=str)  
        args = parser.parse_args()
        que = queue.Queue()
        thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, args['oracion']))
        thr.start()
        thr.join()
        while not que.empty():
            resultado=que.get()

        return {'palabras':resultado}        


api.add_resource(EnviarTraduccion,'/enviarTraduccion')
api.add_resource(RecibirTraduccion,'/recibirTraduccion')

api.add_resource(Codigo,'/codigo')
api.add_resource(RegistroProfesor,'/registroProfesor')
api.add_resource(RegistroAlumno,'/registroAlumno')
api.add_resource(Clase,'/clase')
api.add_resource(LoginAlumno,'/loginAlumno')

api.add_resource(Prueba,'/prueba')

if __name__ == '__main__':
    #app.run(debug=True, host='localhost', port=5000)
    app.run(debug=True, host='10.0.1.4', port=5000) 