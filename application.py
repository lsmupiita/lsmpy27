from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import dataBase

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
oraciontraducida="Sin oracion"
token="00000000"

class Traduccion(Resource):
    
    def get(self):
        return {
            'token': token,
            'sujeto': 'perro',
            'verbo': 'juega',
            'predicado': 'pelota'
        }

    def post(self):
        parser.add_argument('codigo', type=str)
        parser.add_argument('oracion', type=str)
        args = parser.parse_args()
        global oracionTraducida
        oracionTraducida=args['oracion']
        global token
        token=args['codigo']
        print args['oracion']
        print args['codigo']
        return {
            'estado':'envio exitoso'
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