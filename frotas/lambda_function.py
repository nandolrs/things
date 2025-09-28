import CFS3
import CFVeiculos
import json
from decimal import Decimal

def lambda_handler(event, context):
    try:
        
        functionName =  context.function_name
        startTime = event['startTime']

        metodos = ['GetPropertyValueHistory','GetPropertyValue',]
        metodo = metodos[0]

        if startTime == None:
            metodo = metodos[1]

        print('metodo=', metodo)

        match metodo:
            case 'GetPropertyValueHistory':
                entidade = CFVeiculos.CVeiculos()
                retorno = entidade.lambda_handler_value_history(event, context)

        match metodo:
            case 'GetPropertyValue':
                entidade = CFVeiculos.CVeiculos()
                retorno = entidade.lambda_handler_value(event, context)                

        return retorno
    
    except Exception as e:
        print('== erro ==')
        print (e)
    #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
        retorno = {'retorno': 'falha'}

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        # Convert Decimal to string to preserve precision
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def Dic2Json2Dic(event):
     
    s1from = 'False'
    s1to = '"False"'

    s2from = 'True'
    s2to = '"True"'    

    s3from = "'"
    s3to = '"'

    eventJson = event
    eventJson = eventJson.replace(s1from,s1to)
    eventJson = eventJson.replace(s2from,s2to)
    eventJson = eventJson.replace(s3from,s3to)

    eventDic = json.loads(eventJson)    

    return eventDic

def Testar():

    # carregar

    fileName = 'request-aws-iot-twinmaker2lambda-event.json'

    f = open(fileName)

    filedata = f.read()

    # filedata = filedata.encode('utf-8')     

    print('===')
    print(filedata)   

    # eventDic = Dic2Json2Dic(filedata)
    eventDic = json.dumps(filedata)

    context = {'context':'context'}
    lambda_handler(eventDic,context)

# Testar()