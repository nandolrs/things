import CFIotTwinMaker
import json

def Testar():

    # carregar

    fileName = 'request-aws-iot-twinmaker.json'

    f = open(fileName)

    filedata = f.read()

    request = json.loads(filedata)

    #

    cComponentResponse = CFIotTwinMaker.CComponentResponse()

    retorno = cComponentResponse.GetPropertyValueHistory(request = request)


    print(retorno)

Testar()  
print('testou')  