def lambda_handler(event, context):
    try:
        retorno = {
            "propertyValues" :[


            ]
        }
      
        return retorno
    except Exception as e:
        print('== erro ==')
        print (e)
    #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
        retorno = {'retorno': 'falha'}

    return retorno


# retorno = lambda_handler(event=None, context=None)
# print(retorno)
