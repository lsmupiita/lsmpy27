# -*- coding: utf-8 -*-
from modulo_3 import *

textos_1 = [ [(u"el", u"DA0FS0", -1, u"La"), (u"cama", u"NCFS000", -1, u"cama"), (u"estar", u"VMIP3S0", -1, u"está"),(u"suave", u"AQ0CS00", -1, u"suave")],[(u"mi", u"DP1CSS", -1, u"Mi"), (u"casa", u"NCFS000", -1, u"casa"), (u"estar", u"VMIP3S0", -1, u"está"), (u"limpio", u"AQ0FS00", -1, u"limpia")],[(u"el", u"DA0MS0", -1, u"El"), (u"cabello", u"NCMS000", -1, u"cabello"), (u"correr", u"VMIP3S0", -1, u"corre"), (u"rápido", u"AQ0MS00", -1, u"rápido")],[(u"mi", u"DP1CSS", -1, u"Mi"), (u"papá", u"NCMS000", -1, u"papá"),(u"bajo", u"AQ0FS00", -1, u"baja"),(u"rápidamente", u"RG", -1, u"rápidamente")],[(u"el", u"DA0MS0", -1, u"El"), (u"juego", u"NCMS000", -1, u"juego"), (u"ser", u"VSIP3S0", -1, u"es"),(u"muy", u"RG", -1, u"muy"), (u"temprano", u"AQ0MS00", -1, u"temprano")],[(u"él", u"PP3FS00", -1, u"Ella"), (u"ser", u"VSIP3S0", -1, u"es"),(u"bonito", u"AQ0FS00", -1, u"bonita")],[(u"yo", u"PP1CSN0", -1, u"Yo"),(u"camino", u"NCMS000", -1, u"camino"),(u"despacio", u"RG", -1, u"despacio")],[(u"el", u"DA0FS0", -1, u"La"),  (u"niño", u"NCFS000", -1, u"niña"), (u"jugar", u"VMIP3S0", -1, u"juega"),(u"pelota", u"NCFS000", -1, u"pelota")],[(u"él", u"PP3MS00", -1, u"Él"), (u"bailar", u"VMIP3S0", -1, u"baila"),(u"muy", u"RG", -1, u"muy"), (u"rápido", u"AQ0MS00", -1, u"rápido")],[(u"él", u"PP3MS00", -1, u"Él"), (u"tener", u"VMIP3S0", -1, u"tiene"),(u"comida", u"NCFS000", -1, u"comida")] ]

textos_2 = [ [(u"mi",     u"DP1CSS", -1, "Mi"  ),(u"gato",   u"NCMS000", -1, "gato" ),(u"tomar",  u"VMIP3S0", -1, "toma"),(u"leche",  u"NCFS000", -1, "leche" )],[(u"yo",           u"PP1CSN0", -1, "Yo" ),(u"ser",          u"VSIP1S0", -1, "soy"),(u"politécnico",  u"AQ0MS00", -1, "politécnico" )],[(u"él",       u"PP3MS00", -1, "Él" ),(u"quitar",   u"VMIP3S0", -1, "quita"),(u"el",       u"DA0FS0", -1, "la"  ),(u"cebolla",  u"NCFS000", -1, "cebolla" )],[(u"su", u"DP3CSN", -1, u"Su"),(u"perro", u"NCMS000", -1, u"perro"),(u"seguir", u"VMIP3S0", -1, u"sigue"),(u"a", u"SP", -1, u"a"),(u"el", u"DA0MS0", -1, u"el"),(u"gato", u"NCMS000", -1, u"gato")],[(u"el", u"DA0MS0", -1, u"El"),(u"niño", u"NCMS000", -1, u"niño"),(u"recoger", u"VMIP3S0", -1, u"recoge"),(u"el", u"DA0MS0", -1, u"el"),(u"cuarto", u"NCMS000", -1, u"cuarto")] ]

textos_3 = [ [( u'pasar', u'VMM02S0', -1, u'Pasa'), (u'me', u'PP1CS00', -1, u'me'), (u'el', u'DA0FS0', -1, u'la'), (u'sal', u'NCFS000', -1, u'sal')] ]

textos_4 = [[ ( u"el", u"DA0MS0" , -1, u"El"),( u"gato", u"NCMS000", -1, u"gato"),( u"estar", u"VMIP3S0", -1, u"está"),( u"en", u"SP", -1, u"en"),( u"el", u"DA0MS0" , -1, u"el"),( u"patio", u"NCMS000", -1, u"patio")],[(u"él", u"PP3MS00", -1, u"Él"),(u"cantar", u"VMIP3S0", -1, u"canta"),(u"para", u"SP", -1, u"para"),(u"el", u"DA0FS0", -1, u"la"),(u"abuelo", u"NCFS000", -1, u"abuela")],[(u"el",    u"DA0MS0", -1, u"El"),  (u"papá",  u"NCMS000", -1, u"papá"), (u"bañar", u"VMIP3S0", -1, u"baña"),(u"a",     u"SP", -1, u"a"),      (u"el",    u"DA0MP0", -1, u"los"),  (u"perro", u"NCMP000", -1, u"perros")]]

textos = textos_1 + textos_2 + textos_3 + textos_4

for ejemplo in textos:
    arboles = modulo_main(ejemplo, debug=True)
    print ""
