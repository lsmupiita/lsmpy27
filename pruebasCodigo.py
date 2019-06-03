import dataBase

def unirLista(codigo,traduccion,lista):
    alumnos=dataBase.numeroAlumnos(codigo)
    resultado=list()
    aux=[codigo,alumnos,traduccion]
    resultado=aux+lista
    return resultado

def buscarTraduccion(codigo,lista):
    indice=0
    for x in lista:
        if x==codigo:
            return indice
        indice+=1
    return "Sin coincidencia"
        

traduccion=["cama","suave"]
stack=["123456","3",["mujer","correr","sola"]]
codigo="04440224"
print stack
stack=unirLista(codigo,traduccion,stack)
print "resultado final"
print stack

print "######################"
print buscarTraduccion("123456",stack)

print "hacer pop"
stack.pop(1)
print stack