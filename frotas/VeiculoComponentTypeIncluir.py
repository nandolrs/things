import CFIotTwinMaker
import json
import CFVeiculos

def Testar():

    # busca propriedades do veiculo

    cVeiculos = CFVeiculos.CVeiculos()

    propriedades = cVeiculos.PropriedadesBuscar()    

    #

    cComponentType = CFIotTwinMaker.CComponentType()


    propertyDefinitions, functions = cComponentType.Gerar(
         componentTypeId='com.cmj.timeseries-connector' 
        # ,lambdaArn      ='arn:aws:lambda:sa-east-1:105254198021:function:VeiculosTimeSeries'              
        ,lambdaArn      ='arn:aws:lambda:us-east-1:105254198021:function:VeiculosTimeSeries'
        ,propriedades = propriedades
    )

    print(json.dumps(propertyDefinitions))

    extendsFrom = ['com.example.timestream-telemetry']

    retornoComponentType = cComponentType.Incluir(
         workspaceId            = 'VehicleFleetWorkspace1'
        ,componentTypeId        = 'com.cmj.timeseries-connector'
        # ,extendsFrom            = extendsFrom
        ,functions              = functions
        ,propertyDefinitions    = propertyDefinitions
    )

    print(retornoComponentType)

Testar()  
print('testou')  