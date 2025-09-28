import boto3
import json

class CEntity:

    def __init__(self):
        self.cliente = boto3.client('iottwinmaker',region_name='us-east-1')

    def Incluir(self, workspaceId, entityName,components):
        try:


            retorno = self.cliente.create_entity(
                    workspaceId=workspaceId
                    ,entityName = entityName
                    ,components=components
            )
                                    

            return retorno

        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise     

    def Excluir(self, workspaceId, entityId):
        try:
            retorno = self.cliente.delete_entity(workspaceId=workspaceId
                                    ,entityId = entityId
                                    ,isRecursive=False
                                    )
            return retorno
            

        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise          
          
    def Listar(self, workspaceId):
        try:
            listaEntidades = self.cliente.list_entities(workspaceId=workspaceId)   

            entidades = listaEntidades['entitySummaries']

            retorno = []         

            for entidade in entidades:

                retorno.append({'nome':entidade['entityName']})

            return retorno
        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise   

    def Consultar(self, workspaceId,entityName):
        try:
            listaEntidades = self.cliente.list_entities(workspaceId=workspaceId)   

            entidades = listaEntidades['entitySummaries']

            retorno = None         

            for entidade in entidades:
                if entidade['entityName'] == entityName:
                    retorno={'nome':entidade['entityName'],'id':entidade['entityId']}

            return retorno
        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise   

class CComponent:
    def __init__(self):
        self.cliente = boto3.client('iottwinmaker',region_name='us-east-1')

    def Gerar(self, componentes, properties): #, nome, componentTypeId
        try:
            retorno = {}
            for componente in componentes:
                componente_ = {
                        'componentTypeId' : componente['componentTypeId']
                        ,'properties' : properties

                }

                retorno[
                    componente['nome'] 

                ] =  componente_

            return retorno
        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise   


class CComponentResponse:
    def __init__(self):
        self.cliente = boto3.client('iottwinmaker',region_name='us-east-1')

    def RequestExtrairNome(self, request): # entityId, componentName, selectedProperties
        try:

            componentName = request['componentName']

            return componentName

            # properties =  request['properties']

            # telemetryAssetId = properties['telemetryAssetId']

            # value = telemetryAssetId['value']

            # stringValue = value['stringValue']

            # retorno = stringValue

            # return retorno
        except Exception as e:
            print('== erro ==')
            print (e)            
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise       

class CComponentType:

    def __init__(self):
        self.cliente = boto3.client('iottwinmaker',region_name='us-east-1')

    def Gerar(self, componentTypeId, lambdaArn,  propriedades, gerarApenasExternal=False):

        propertyDefinitions = {}

        for propriedade in propriedades:

            if gerarApenasExternal and not propriedade['isExternalId_']:
                continue
            
            propertyDefinition =    {
                'dataType' : {
                    'type': propriedade['type_']
                }
                ,'isExternalId':propriedade['isExternalId_']
                ,'isStoredExternally': propriedade['isStoredExternally_']
                ,'isTimeSeries': propriedade['isTimeSeries_']
                ,'isRequiredInEntity': propriedade['isRequiredInEntity_']

            }
            
            propertyDefinitions[
                propriedade['propertyName'] 

            ] =  propertyDefinition

        retorno = {
            'componentTypeId':componentTypeId
            ,'functions':{
                'dataReader':{
                    'implementedBy':{
                        'lambda':{
                            'arn' : lambdaArn
                        }

                    }

                }

            }
            ,'propertyDefinitions':propertyDefinitions

            
        }

        functions =  {
                'dataReader':{
                    'implementedBy':{
                        'lambda':{
                            'arn' : lambdaArn
                        }

                    }

                }

            }
        

        retorno = propertyDefinitions, functions

        return retorno

    def GerarProperty(self, componentTypeId, lambdaArn,  propriedades, gerarApenasExternal=False):

        propertyDefinitions = {}

        for propriedade in propriedades:

            if gerarApenasExternal and not propriedade['isExternalId_']:
                continue
            
            propertyDefinition =    {
                'dataType' : {
                    'type': propriedade['type_']
                }
                ,'isExternalId':propriedade['isExternalId_']
                ,'isStoredExternally': propriedade['isStoredExternally_']
                ,'isTimeSeries': propriedade['isTimeSeries_']
                ,'isRequiredInEntity': propriedade['isRequiredInEntity_']

            }
            
            propertyDefinitions[
                propriedade['propertyName'] 

            ] =  propertyDefinition

        retorno = {
            'componentTypeId':componentTypeId
            ,'functions':{
                'dataReader':{
                    'implementedBy':{
                        'lambda':{
                            'arn' : lambdaArn
                        }

                    }

                }

            }
            ,'propertyDefinitions':propertyDefinitions

            
        }

        # functions =  {
        #         'dataReader':{
        #             'implementedBy':{
        #                 'lambda':{
        #                     'arn' : lambdaArn
        #                 }

        #             }

        #         }

        #     }

        functions =  {
                'attributePropertyValueReaderByEntity':{
                    'scope':'ENTITY'
                   ,'implementedBy':{
                        # 'isNative':False
                        'lambda':{
                            'arn' : lambdaArn
                        }

                    }

                }

            }


        retorno = propertyDefinitions, functions

        return retorno

    def DePara(self, de):
        if de == 'STRING' :
            return 'stringValue'
        else:
            return 'none'
        
    def GerarProperties(self, componentTypeId, lambdaArn,  propriedades, gerarApenasExternal=False):

        propertyDefinitions = {}

        for propriedade in propriedades:

            if gerarApenasExternal and not propriedade['isExternalId_']:
                continue

            depara_ = self.DePara(propriedade['type_'])
            valor_ = propriedade['value_']

            propertyDefinition =   {
                'value':{
                    depara_ : valor_
                }
                # ,

                # 'definition':{
                #     'dataType' : {
                #         'type': propriedade['type_']
                #     }
                #     ,'isExternalId':propriedade['isExternalId_']
                #     ,'isStoredExternally': propriedade['isStoredExternally_']
                #     ,'isTimeSeries': propriedade['isTimeSeries_']
                #     ,'isRequiredInEntity': propriedade['isRequiredInEntity_']                    

                # }

            }
            
            propertyDefinitions[
                propriedade['propertyName'] 

            ] =  propertyDefinition

        # retorno = {
        #     'properties':propertyDefinitions            
        # }

        retorno = propertyDefinitions

        return retorno

    def Incluir(self, workspaceId, componentTypeId , functions, propertyDefinitions): # ,  extendsFrom
        try:
            retorno = self.cliente.create_component_type(
                 workspaceId        =workspaceId
                ,componentTypeId    = componentTypeId
                # , extendsFrom       = extendsFrom
                ,functions          = functions
                ,propertyDefinitions=propertyDefinitions
            )

            return retorno

        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise 

    def Excluir(self, workspaceId, componentTypeId):
        try:
            retorno = self.cliente.delete_component_type(
                 workspaceId=workspaceId
                ,componentTypeId = componentTypeId
            )

            return retorno

        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise          
