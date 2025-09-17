import CFS3
import CFVeiculos
import json
import CFIotTwinMaker

def lambda_handler(event, context):
    try:

        cfS3 = CFS3.CS3()
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/event-v1r1.json', contentBody=str(event))
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/context-v1r1.json', contentBody=str(context))

        # pesquisa veiculo por placa

        # retorno = {'retorno': 'sucesso'}

        print('passou 1')

        retorno = VeiculoPesquisar(event)

        print('passou fim')


        return retorno
    except Exception as e:
    #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
        retorno = {'retorno': 'falha'}

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


def Testar():

    # carregar

    fileName = 'request-aws-iot-twinmaker2lambda-context.json'

    f = open(fileName)

    filedata = f.read()

    request = json.loads(filedata)


    event = {'event':'teste'}
    # lambda_handler(event,filedata)
    lambda_handler(event,request)

# Testar()