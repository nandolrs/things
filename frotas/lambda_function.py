import CFS3
import CFVeiculos
import json
import CFIotTwinMaker

def lambda_handler(event, context):
    try:

        cfS3 = CFS3.CS3()
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/event-v1r1.json', contentBody=str(event))
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/context-v1r1.json', contentBody=str(context))

        eventDic = Dic2Json2Dic(str(event)) 
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/event-v1r1-JSON.json', contentBody=str(eventDic))

        # pesquisa veiculo por placa

        # retorno = {'retorno': 'sucesso'}

        print('passou 1')

        retorno = VeiculoPesquisar(eventDic ) # event

        print('passou fim')


        return retorno
    except Exception as e:
        print('== erro ==')
        print (e)
    #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
        retorno = {'retorno': 'falha'}

def Dic2Json2Dic(self, event):
     
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

def VeiculoPesquisar(request):
        
        # obter placa

        # request = json.loads(filedata)
        # request_ = json.loads(request)
        request_ = request

        print('passou 2')

        cComponentResponse = CFIotTwinMaker.CComponentResponse()

        placa = cComponentResponse.GetPropertyValueHistory(request = request_)   

        # placa='ABC1969A'

        ### pesquisar por placa

        cVeiculos = CFVeiculos.CVeiculos()

        retorno = cVeiculos.PesquisarPorPlaca(placa)

        print('===')
        print(json.dumps(retorno))    

        return retorno


def Testar1() :
    event = {'event':'teste'}
    context = {'context':'teste'}
    retorno = lambda_handler(event,context)

    print ('===')
    print (retorno)


def Testar2():

    # carregar

    fileName = 'request-aws-iot-twinmaker2lambda-event.json'

    f = open(fileName)

    filedata = f.read()

    request = json.loads(filedata)


    event = {'event':'teste'}
    # lambda_handler(event,filedata)
    lambda_handler(event,request)


def Testar():

    # carregar

    fileName = 'request-aws-iot-twinmaker2lambda-event-ANTES.json'

    f = open(fileName)

    filedata = f.read()

    eventDic = Dic2Json2Dic(None,filedata)

    context = {'context':'context'}
    lambda_handler(eventDic,context)

Testar()