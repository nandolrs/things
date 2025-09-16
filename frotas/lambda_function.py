import CFS3

def lambda_handler(event, context):
    try:

        cfS3 = CFS3.CS3()
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/event-v1r1.json', contentBody=str(event))
        cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/context-v1r1.json', contentBody=str(context))

        retorno = {'retorno': 'sucesso'}

        return retorno
    except Exception as e:
    #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
        retorno = {'retorno': 'falha'}


def Testar() :
    event = {'event':'teste'}
    context = {'context':'teste'}
    lambda_handler(event,context)

# Testar()