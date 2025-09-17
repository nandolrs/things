import json
import os
import logging

import CFS3

import CFVeiculos

def lambda_handler(event, context):
    
    try:
     
        return {
            "statusCode": 200,
            "message": "Receipt processed successfully"
        }

    except Exception as e:
        raise

def Testar():

    cfVeiculos = CFVeiculos.CVeiculos()
    # veiculos = cfVeiculos.JsonGerar()
    veiculos = cfVeiculos.FlatGerar()

    cfS3 = CFS3.CS3()
    cfS3.Incluir( bucketName='cmj-dados-lambda', key='input/veiculos-v1r2.json', contentBody=veiculos)
    cfS3.Incluir( bucketName='cmj-motores', key='dados/TFrotas/veiculos-v1r2.csv', contentBody=veiculos)

Testar()  
print('gerou')  