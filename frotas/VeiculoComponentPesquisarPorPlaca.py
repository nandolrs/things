import json
import CFVeiculos

def Testar():

        placa='ABC1969A'

        cVeiculos = CFVeiculos.CVeiculos()

        retorno = cVeiculos.PesquisarPorPlaca(placa)

        print('===tipo===')
        print (type(retorno))

        print('===')
        print(json.dumps(retorno))    


Testar()  
print('testou')  