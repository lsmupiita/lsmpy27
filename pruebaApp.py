#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import dataBase, operaciones

import threading
import Queue as queue

def dosomething(oracion):
    return operaciones.traduccionAutomatica(oracion)

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
oracionTraducida="Sin oracion"
token="00000000"

class Traduccion(Resource):
    
    def get(self):
        return {
            'token': token,
            'traduccion': oracionTraducida
        }

    def post(self):
        parser.add_argument('codigo', type=str)
        parser.add_argument('oracion', type=str)
        args = parser.parse_args()
        print "aqui esta la oracion"
        print args['oracion']
        global token
        token=args['codigo']

        que = queue.Queue()
        thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, args['oracion']))
        thr.start()
        thr.join()
        while not que.empty():
            global oracionTraducida
            oracionTraducida=que.get()
        return {
            'palabras':oracionTraducida
        }
    
class Codigo(Resource):
    def post(self):
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            return { 'codigo':dataBase.generarCodigo(args['correo']) }

class EntrarClase(Resource):
    def post(self):
            parser.add_argument('codigo', type=str)
            args = parser.parse_args()
            return { 'mensaje':dataBase.comprobarExistencia(args['codigo']) }

class Registro(Resource):
    def post(self):
        parser.add_argument('correo',type=str)  
        args = parser.parse_args()
        return {'mensaje':dataBase.nuevoregistro(args['correo'])}   

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


api.add_resource(Traduccion,'/traduccion')

api.add_resource(Codigo,'/codigo')
api.add_resource(Registro,'/registro')
api.add_resource(EntrarClase,'/entrarClase')
api.add_resource(Prueba,'/prueba')

if __name__ == '__main__':
    #app.run(debug=True, host='localhost', port=5000)
    app.run(debug=True, host='10.0.1.4', port=5000) 