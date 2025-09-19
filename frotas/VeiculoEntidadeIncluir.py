import CFIotTwinMaker
import json
import CFVeiculos

def Testar():

    # propriedades


    # propriedades = [
    #     {
    #     'propertyName' : 'telemetryAssetType'
    #     ,'type_' : 'STRING'
    #     ,'isExternalId_' : False # true, se isRequiredInEntity_
    #     ,'isStoredExternally_' : False
    #     ,'isTimeSeries_' : False
    #     ,'isRequiredInEntity_' : False # true, se isExternalId_
    #     ,'value_' : 'ABDC'


    #     }
    #     ,
    #     {
    #     'propertyName' : 'telemetryAssetId'
    #     ,'type_' : 'STRING'
    #     ,'isExternalId_' : True # true, se isRequiredInEntity_
    #     ,'isStoredExternally_' : False
    #     ,'isTimeSeries_' : False
    #     ,'isRequiredInEntity_' : True # true, se isExternalId_
    #     ,'value_' : 'ABDC'
    #     }            

        
    # ]    

    cVeiculos = CFVeiculos.CVeiculos()

    propriedades = cVeiculos.PropriedadesBuscar()

    propriedades =  cVeiculos.PropriedadesExternalSetar(propriedades=propriedades, nomes=['placa'])


    # propriedades do componente

    cComponentType = CFIotTwinMaker.CComponentType()

    propertyDefinitions, functions = cComponentType.Gerar(
         componentTypeId='com.cmj.timeseries-connector'
        ,lambdaArn      ='arn:aws:lambda:sa-east-1:105254198021:function:VeiculosTimeSeries'              
        ,propriedades           = propriedades
        ,gerarApenasExternal    = True
    )


    print('---')
    print( json.dumps(propertyDefinitions) )    

    properties = cComponentType.GerarProperties(
         componentTypeId='com.cmj.timeseries-connector'
        ,lambdaArn      ='arn:aws:lambda:sa-east-1:105254198021:function:VeiculosTimeSeries'              
        ,propriedades           = propriedades
        ,gerarApenasExternal    = True
    )    


    print('---')
    print( json.dumps(properties) )        


    # componentes

    cComponent = CFIotTwinMaker.CComponent()

    componentTypeId = 'com.cmj.timeseries-connector'

    componentes = [
        {
            'nome':'ABC1969A'
            ,'componentTypeId':componentTypeId
        }
        ,
        {
            'nome':'ABC1970A'
            ,'componentTypeId':componentTypeId
        }
        ,
        {
            'nome':'ABC1971A'
            ,'componentTypeId':componentTypeId
        }

    ]

    components = cComponent.Gerar(
        # nome             = 'MotorDC-componente-v1r1'
        # ,componentTypeId = 'com.cmj.timeseries-connector'
        componentes = componentes
        ,properties = properties
    )    

    print('---')
    print( json.dumps(components) )
    # print( components)

    # entidade

    cEntity = CFIotTwinMaker.CEntity()
    
    retorno = cEntity.Incluir(
        workspaceId = 'VehicleFleetWorkspace1'
        ,entityName = 'MotorDC-entidade-v1r1'
        ,components = components
    )

    print(retorno)


Testar()  
print('testou')  