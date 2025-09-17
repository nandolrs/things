import CFAthena
import json

def Testar():

    cAthena = CFAthena.CAThena()

    placa='ABC1969A'
    retorno = cAthena.Pesquisar(DatabaseName='cmj-database', placa=placa)

    print('===')
    print(json.dumps(retorno))

Testar()  
print('testou')  