import CFVeiculos
import json

def Testar():

    cVeiculos = CFVeiculos.CVeiculos()

    retorno  = cVeiculos.PropriedadesBuscar()    

    print('=== propriedades')
    print(json.dumps(retorno))

    retorno =  cVeiculos.PropriedadesExternalSetar(propriedades=retorno, nomes=['placa'])

    print('=== enternal')
    print(json.dumps(retorno))



Testar()  
print('testou')  