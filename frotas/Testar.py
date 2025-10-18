import CFVeiculos
import CFIotTwinMaker
import CFAthena
import CFAutenticador

import time
from  datetime import datetime, timezone
import json

class CVeiculosTestar:

    def CFVeiculosPropriedadesBuscarPorDicionario(self):

        cVeiculo = CFVeiculos.CVeiculo()

        cVeiculos = CFVeiculos.CVeiculos()
        retorno  = cVeiculos.PropriedadesBuscarPorDicionario(dicionario=cVeiculo)

        retorno =  cVeiculos.PropriedadesTimeSeriesSetar(
             propriedades=retorno
            ,nomes=NOMES #['id','placa','modelo','velocidademotor','unidade','time']
        )


        print(retorno)

    def CFVeiculosPropriedadesBuscar(self):

        cVeiculos = CFVeiculos.CVeiculos()

        retorno  = cVeiculos.PropriedadesBuscar()    

        retorno =  cVeiculos.PropriedadesTimeSeriesSetar( #  PropriedadesExternalSetar !!!
            propriedades=retorno
            , nomes=NOMES #['id','modelo','placa','temperatura','time','unidade','velocidademotor']
        )


        print('=== enternal')
        print(json.dumps(retorno))

    def CFVeiculosPesquisarPorPlaca(self):

            placa='ABC1969A'

            cVeiculos = CFVeiculos.CVeiculos()

            retorno = cVeiculos.PesquisarPorPlaca(placa)

            print('===tipo===')
            print (type(retorno))

            print('===')
            print(json.dumps(retorno))    


    def CFVeiculosPesquisarPorPlacaApi(self):
            placa="esp8266-v1r1"
            startTime="2025-10-05T19:48:00.000Z"
            endTime="2025-10-05T19:48:59.000Z"

            cVeiculos = CFVeiculos.CVeiculos()

            retorno = cVeiculos.PesquisarPorPlacaApi( placa, startTime, endTime)

            print('===tipo===')
            print (type(retorno))

            print('===')
            print(json.dumps(retorno))    

    def CFVeiculosJsonDynamoGerar(self):

        cfVeiculos = CFVeiculos.CVeiculos()
        # veiculos = cfVeiculos.JsonGerar()
        # veiculos = cfVeiculos.FlatGerar()
        veiculos = cfVeiculos.JsonDynamoGerar()

    def CFVeciculosDataHoraIsoBuscar(self):

        cVeiculos = CFVeiculos.CVeiculos()

        agora = datetime.now()
        time_ =     cVeiculos.DataHoraIsoBuscar(ano=agora.year, mes=agora.month, dia=agora.day, hora=agora.hour, minuto=agora.minute, secsegundo=agora.second)
        return time_

    def CFComponentTypeIncluir(self):

        # busca propriedades do veiculo

        cVeiculos = CFVeiculos.CVeiculos()

        propriedades_ = cVeiculos.PropriedadesBuscar()    

        propriedades =  cVeiculos.PropriedadesTimeSeriesSetar(
            propriedades=propriedades_
            , nomes=NOMES #['id','modelo','placa','temperatura','time','unidade','velocidademotor']
        )

        #

        cComponentType = CFIotTwinMaker.CComponentType()


        propertyDefinitions, functions = cComponentType.Gerar(
            componentTypeId = COMPONENT_TYPE_ID
            ,lambdaArn      = AWS_LAMBDA
            ,propriedades   = propriedades
        )

        retornoComponentType = cComponentType.Incluir(
            workspaceId             = WORK_SPACE_ID
            ,componentTypeId        = COMPONENT_TYPE_ID
            ,functions              = functions
            ,propertyDefinitions    = propertyDefinitions
        )

        print(retornoComponentType)

    def CFComponentTypeIncluirPorDicionario(self, dicionario):

        propertyDefinitions, functions = self.CFComponentTypeGerarPorDicionario(dicionario)

        cComponentType = CFIotTwinMaker.CComponentType()

        retornoComponentType = cComponentType.Incluir(
            workspaceId             = WORK_SPACE_ID
            ,componentTypeId        = COMPONENT_TYPE_ID
            ,functions              = functions
            ,propertyDefinitions    = propertyDefinitions
        )

        print(retornoComponentType)


    def CFComponentTypeGetPropertyValueIncluirPorDicionario(self, dicionario):

        propertyDefinitions, functions = self.CFComponentTypeGetPropertyValueGerarPorDicionario(dicionario)
                                              
        cComponentType = CFIotTwinMaker.CComponentType()

        retornoComponentType = cComponentType.Incluir(
            workspaceId             = WORK_SPACE_ID
            ,componentTypeId        = COMPONENT_TYPE_ID
            ,functions              = functions
            ,propertyDefinitions    = propertyDefinitions
        )

        print(retornoComponentType)

    def CFComponentGerar():

        cComponent = CFIotTwinMaker.CComponent()

        retorno = cComponent.Gerar(
                nome='MotorDC-componente-01'
                ,componentTypeId=COMPONENT_TYPE_ID
        )        

    def CFComponentResponseGetPropertyValueHistory():

        # carregar

        fileName = 'request-aws-iot-twinmaker.json'

        f = open(fileName)

        filedata = f.read()

        request = json.loads(filedata)

        #

        cComponentResponse = CFIotTwinMaker.CComponentResponse()

        retorno = cComponentResponse.GetPropertyValueHistory(request = request)

        print(retorno)

    def CFComponentTypeGerarPorDicionario(self, dicionario):

        # busca propriedades do dicionario

        cVeiculos = CFVeiculos.CVeiculos()

        propriedades_ = cVeiculos.PropriedadesBuscarPorDicionario(dicionario)    

        propriedades =  cVeiculos.PropriedadesTimeSeriesSetar(
             propriedades=propriedades_
            , nomes= NOMES #['id','modelo','placa','temperatura','time','unidade','velocidademotor']
        )

        #

        cComponentType = CFIotTwinMaker.CComponentType()

        propertyDefinitions, functions = cComponentType.Gerar(
            componentTypeId = COMPONENT_TYPE_ID
            
            ,lambdaArn      = AWS_LAMBDA
            ,propriedades   = propriedades
        )

        print('propertyDefinitions=',json.dumps(propertyDefinitions))

        print('functions=',json.dumps(functions))


        return propertyDefinitions,  functions

    def CFComponentTypeGetPropertyValueGerarPorDicionario(self, dicionario):

        # busca propriedades do dicionario

        cVeiculos = CFVeiculos.CVeiculos()

        propriedades_ = cVeiculos.PropriedadesBuscarPorDicionario(dicionario)    

        propriedades =  cVeiculos.PropriedadesTimeSeriesSetar(
             propriedades=propriedades_
            , nomes=NOMES #['id','modelo','placa','temperatura','time','unidade','velocidademotor']
        )

        #

        cComponentType = CFIotTwinMaker.CComponentType()

        propertyDefinitions, functions = cComponentType.GerarGetPropertValue(
            componentTypeId = COMPONENT_TYPE_ID
            
            ,lambdaArn      = AWS_LAMBDA
            ,propriedades   = propriedades
        )

        print('propertyDefinitions=',json.dumps(propertyDefinitions))

        print('functions=',json.dumps(functions))


        return propertyDefinitions,  functions

    def CFComponentTypeExcluir(self):

        cComponentType = CFIotTwinMaker.CComponentType()

        retorno = cComponentType.Excluir(
             workspaceId        = WORK_SPACE_ID
            ,componentTypeId    = COMPONENT_TYPE_ID
        )

        print(retorno)  

    def CFEntityIncluir(self):

        cVeiculos = CFVeiculos.CVeiculos()

        propriedades = cVeiculos.PropriedadesBuscar()

        propriedades =  cVeiculos.PropriedadesTimeSeriesSetar(
            propriedades=propriedades
            , nomes=NOMES #['id','modelo','placa','temperatura','time','unidade','velocidademotor']
        )

        # propriedades do componente

        cComponentType = CFIotTwinMaker.CComponentType()

        propertyDefinitions, functions = cComponentType.Gerar(
             componentTypeId        = COMPONENT_TYPE_ID
            ,lambdaArn              = AWS_LAMBDA
            ,propriedades           = propriedades
            ,gerarApenasExternal    = True
        )

        properties = cComponentType.GerarProperties(
             componentTypeId        = COMPONENT_TYPE_ID
            ,lambdaArn              = AWS_LAMBDA
            ,propriedades           = propriedades
            ,gerarApenasExternal    = True
        )      

        # componentes

        cComponent = CFIotTwinMaker.CComponent()

        componentes = [
            {
                'nome':'ABC1969A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }
            ,
            {
                'nome':'ABC1970A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }
            ,
            {
                'nome':'ABC1971A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }

        ]

        components = cComponent.Gerar(
            componentes = componentes
            ,properties = properties
        )    

        # entidade

        cEntity = CFIotTwinMaker.CEntity()
        
        retorno = cEntity.Incluir(
            workspaceId = WORK_SPACE_ID
            ,entityName = ENTITY_NAME
            ,components = components
        )

        print(retorno)

    def CFEntityIncluirPorDicionario(self):

        dicionario = CFVeiculos.CVeiculo()

        cVeiculos = CFVeiculos.CVeiculos()

        propriedades = cVeiculos.PropriedadesBuscarPorDicionario(dicionario)        

        propertyDefinitions, functions = self.CFComponentTypeGerarPorDicionario(dicionario)

        cComponentType = CFIotTwinMaker.CComponentType()

        properties = cComponentType.GerarProperties(
             componentTypeId        = COMPONENT_TYPE_ID
            ,lambdaArn              = AWS_LAMBDA
            ,propriedades           = propriedades
            ,gerarApenasExternal    = True
        )      

        # componentes

        cComponent = CFIotTwinMaker.CComponent()

        componentes = [
            {
                'nome':'ABC1969A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }
            ,
            {
                'nome':'ABC1970A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }
            ,
            {
                'nome':'ABC1971A'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }
            ,
            {
                'nome':'esp8266-v1r1'
                ,'componentTypeId':COMPONENT_TYPE_ID
            }            

            

        ]

        components = cComponent.Gerar(
            componentes = componentes
            ,properties = properties
        )    

        # entidade

        cEntity = CFIotTwinMaker.CEntity()
        
        retorno = cEntity.Incluir(
            workspaceId = WORK_SPACE_ID
            ,entityName = ENTITY_NAME
            ,components = components
        )

        print(retorno)

    def CFEntityConsultar():

        cEntity = CFIotTwinMaker.CEntity()

        retorno = cEntity.Consultar(
            workspaceId = WORK_SPACE_ID
            ,entityName = ENTITY_NAME
                                        )
        print(retorno)     

    def CFEntityExcluir(self):

        cEntity = CFIotTwinMaker.CEntity()

        retorno = cEntity.Consultar(
            workspaceId=WORK_SPACE_ID
            ,entityName=ENTITY_NAME
        )

        id = retorno['id']

        entidades = cEntity.Excluir(
            workspaceId=WORK_SPACE_ID
            ,entityId=id
        )

        print(json.dumps(entidades))

    def CFAthenaConsultarMetadadosTabela():

        cAthena = CFAthena.CAThena()

        CatalogName = "AwsDataCatalog"
        DatabaseName = 'cmj-database'
        TableName = 'tfrotas'
        WorkGroup = 'primary'
        retorno  = cAthena.ConsultarMetadadosTabela(CatalogName,DatabaseName,TableName,WorkGroup)

        print('===')
        print(retorno)

    def CFTokenGerar(self):

        cAutenticador = CFAutenticador.CAutenticador()

        retorno = cAutenticador.TokenGerar()

        print('authorizationToken=', retorno)   



### testar

# 'MotorDC-entidade'    'MotorDC-entidade-get-value'
# 'com.cmj.frota.connector'   'com.cmj.frota-get-value.connector' 

PARAMETROS =[ 

    {
        'WORK_SPACE_ID'     :'CmjWorkspace'
        ,'ENTITY_NAME'      :'MotorDC-entidade'
        ,'COMPONENT_TYPE_ID':'com.cmj.frota.connector'
        ,'AWS_LAMBDA'       :'arn:aws:lambda:us-east-1:105254198021:function:cmj-get-property-value-history'
    }
    ,    
    {
        'WORK_SPACE_ID'     :'CmjWorkspace'
        ,'ENTITY_NAME'      :'MotorDC-entidade-v1r1'
        ,'COMPONENT_TYPE_ID':'com.cmj.frota.connector-v1r1'
        ,'AWS_LAMBDA'       :'arn:aws:lambda:us-east-1:105254198021:function:VeiculosTimeSeries'
    }    
    ,
    {
        'WORK_SPACE_ID'     :'CmjWorkspace'
        ,'ENTITY_NAME'      :'MotorDC-entidade-get-value'
        ,'COMPONENT_TYPE_ID':'com.cmj.frota-get-value.connector'
        ,'AWS_LAMBDA'       :'arn:aws:lambda:us-east-1:105254198021:function:VeiculosTimeSeries'
    }


]

# WORK_SPACE_ID = 'CmjWorkspace'
# ENTITY_NAME = 'MotorDC-entidade-get-value' # 'MotorDC-entidade'    'MotorDC-entidade-get-value'
# COMPONENT_TYPE_ID = 'com.cmj.frota-get-value.connector'  #  'com.cmj.frota.connector'   'com.cmj.frota-get-value.connector' 
# AWS_LAMBDA = 'arn:aws:lambda:us-east-1:105254198021:function:VeiculosTimeSeries'              

WORK_SPACE_ID       = PARAMETROS[0]['WORK_SPACE_ID']
ENTITY_NAME         = PARAMETROS[0]['ENTITY_NAME']
COMPONENT_TYPE_ID   = PARAMETROS[0]['COMPONENT_TYPE_ID']
AWS_LAMBDA          = PARAMETROS[0]['AWS_LAMBDA']        
NOMES               = ['id','modelo','placa','temperatura','time','unidade','velocidademotor','alarm_status']    

cVeiculosTestar = CVeiculosTestar()

caso = 16 # inclui= [1,  9, 12 ]; exclui= [10,14]

if caso == 1:

    cVeiculosTestar.CFVeiculosJsonDynamoGerar() 

elif caso == 2:

    cVeiculosTestar.CFVeiculosPropriedadesBuscar()
    
elif caso == 3:

    cVeiculosTestar.CFVeiculosPropriedadesBuscarPorDicionario()

elif caso == 4:

    dicionario  = CFVeiculos.CVeiculo()
    cVeiculosTestar.CFComponentTypeGerarPorDicionario(dicionario)

elif caso == 40:

    dicionario  = CFVeiculos.CVeiculo()
    cVeiculosTestar.CFComponentTypeGetPropertyValueGerarPorDicionario(dicionario)

elif caso == 5:

    cVeiculosTestar.CFComponentGerar()        

elif caso == 6:

    cVeiculosTestar.CFVeiculosPesquisarPorPlaca() 

elif caso == 61:

    cVeiculosTestar.CFVeiculosPesquisarPorPlacaApi()     

elif caso == 7:

    cVeiculosTestar.CFComponentResponseGetPropertyValueHistory() 

elif caso == 8:

    cVeiculosTestar.CFComponentTypeIncluir() 

elif caso == 9:

    dicionario  = CFVeiculos.CVeiculo()

    cVeiculosTestar.CFComponentTypeIncluirPorDicionario(dicionario)    

# elif caso == 90:

#     dicionario  = CFVeiculos.CVeiculo()

#     cVeiculosTestar.CFComponentTypeGetPropertyValueIncluirPorDicionario(dicionario)    


elif caso == 10:

    cVeiculosTestar.CFComponentTypeExcluir() 

elif caso == 11:

    cVeiculosTestar.CFEntityIncluir() 

elif caso == 12:

    cVeiculosTestar.CFEntityIncluirPorDicionario()     

elif caso == 13:

    cVeiculosTestar.CFEntityConsultar() 

elif caso == 14:

    cVeiculosTestar.CFEntityExcluir()      

elif caso == 15:

    cVeiculosTestar.CFVeciculosDataHoraIsoBuscar() 

elif caso == 16:

    cVeiculosTestar.CFTokenGerar() 