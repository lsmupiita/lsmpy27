def separarNumero(numero):
    numeros=[]
    numero=int(numero)
    centenas=numero/100*100
    tmp = numero % 100
    decenas = tmp / 10*10
    unidades = tmp % 10
    return[centenas,decenas,unidades]

for x in separarNumero(167):
    print x
