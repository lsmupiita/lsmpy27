def crearCodigo(correo):
    st = str(correo)
    res="00000000"
    temp=""
    for ch in st:
        aux=bin(ord(ch))[2:].zfill(8)
        for x in range(8):
            aux2=(int(aux[x])+int(res[x]))%10
            temp=temp+str(aux2)
        res=temp
        temp=""
    return res

print crearCodigo("zunecull@gmail.com")