import CFS3
import CFVeiculos
import json
from decimal import Decimal

def lambda_handler(event, context):
    try:

        cfS3 = CFS3.CS3()
        cfS3.Incluir( bucketName='cmj-motores', key='dados/rascunho/event-v1r1-ENTRADA.json', contentBody=str(event))
        cfS3.Incluir( bucketName='cmj-motores', key='dados/rascunho/context-v1r1-ENTRADA.json', contentBody=str(context))
        
        function_name = context.function_name
        print('function_name=', function_name)

        #

        try:
            eventDic = entidade.Dic2Json2Dic(str(event)) 
            # print('passou 1')
        except Exception as e:
            # print('passou 2')
            eventDic = event

        # 

        cfS3.Incluir( bucketName='cmj-motores', key='dados/rascunho/event-v1r1-SAIDA.json', contentBody=str(eventDic))

        match function_name:
            case 'cmj-get-property-value-history':

                startTime =  eventDic['startTime'] # utilizado na pesquisa
                endTime =  eventDic['endTime']     # utilizado na pesquisa      

                entidade = CFVeiculos.CVeiculos(startTime=startTime, endTime=endTime)

                retorno = entidade.lambda_handler_value_history(eventDic, context)

            case 'cmj-get-property-value':

                entidade = CFVeiculos.CVeiculos()

                retorno = entidade.lambda_handler_value(eventDic, context)     

            case 'IotReceptor':

                entidade = CFVeiculos.CVeiculos()

                retorno = entidade.lambda_handler_iotcore(eventDic, context)  

                print('=========================retorno====================')                             
                print(retorno)        

            case 'IotConsumidor': # IotFornecedor

                entidade = CFVeiculos.CVeiculos()

                retorno = entidade.lambda_handler_value_history_porApi(eventDic, context)  

                print('=========================retorno====================')                             
                print(retorno)                                          

        cfS3.Incluir( bucketName='cmj-motores', key='dados/rascunho/event-v1r1-SAIDA.json', contentBody=retorno)
        
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


    # eventDic = Dic2Json2Dic(filedata)
    eventDic = json.dumps(filedata)

    context = {'context':'context'}
    lambda_handler(eventDic,context)

# Testar()