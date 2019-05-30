#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import dataBase, operaciones

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
        #parser.__format__('utf-8')
        parser.add_argument('codigo', type=str)
        parser.add_argument('oracion', type=str)
        args = parser.parse_args()
        #aux=args['oracion'].decode('utf-8')
        #aux=aux.encode('utf-8')
        print "aqui esta la oracion"
        print args['oracion']
        global token
        token=args['codigo']
        global oracionTraducida
        oracionTraducida=operaciones.traduccionAutomatica(args['oracion'])
        print oracionTraducida
        return {
            'palabras':operaciones.traduccionAutomatica(args['oracion'])
            #'palabras': aux
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


api.add_resource(Traduccion,'/traduccion')

api.add_resource(Codigo,'/codigo')
api.add_resource(Registro,'/registro')
api.add_resource(EntrarClase,'/entrarClase')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    #app.run(debug=True, host='10.0.1.4', port=5000) 