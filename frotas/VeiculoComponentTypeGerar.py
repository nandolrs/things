import CFIotTwinMaker
import json

def Testar():

    cComponentType = CFIotTwinMaker.CComponentType()

    # extendsFrom = ['com.example.timestream-telemetry']

    propertyDefinitions, functions = cComponentType.Gerar(
         componentTypeId='com.cmj.timeseries-connector'
        ,lambdaArn      ='arn:aws:lambda:sa-east-1:105254198021:function:VeiculosTimeSeries'              
    )

    print(json.dumps(propertyDefinitions))


Testar()  
print('testou')  