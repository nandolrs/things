import time
from  datetime import datetime, timezone
import json

from decimal import *
from dataclasses import dataclass, asdict
import random

import CFS3
import CFAthena
import CFIotTwinMaker
import CFDynamodb

# import CFVeiculos
# import json
# from decimal import Decimal

getcontext().prec = 6    


# retorno = [
#     {
#     'propertyName' : 'telemetryAssetType'
#     ,'type_' : 'STRING'
#     ,'isExternalId_' : False # true, se isRequiredInEntity_
#     ,'isStoredExternally_' : False
#     ,'isTimeSeries_' : False
#     ,'isRequiredInEntity_' : False # true, se isExternalId_
#     ,'value_' : 'ABC1969A'


#     }
#     ,
#     {
#     'propertyName' : 'telemetryAssetId'
#     ,'type_' : 'STRING'
#     ,'isExternalId_' : True # true, se isRequiredInEntity_
#     ,'isStoredExternally_' : False
#     ,'isTimeSeries_' : False
#     ,'isRequiredInEntity_' : True # true, se isExternalId_
#     ,'value_' : 'ABC1969A' #  ABDC
#     }            

#     ,
#     {
#     'propertyName' : 'placa'
#     ,'type_' : 'STRING'
#     ,'isExternalId_' : False # true, se isRequiredInEntity_
#     ,'isStoredExternally_' : True
#     ,'isTimeSeries_' : True
#     ,'isRequiredInEntity_' : False # true, se isExternalId_
#     ,'value_' : 'ABDC'
#     }            


# ]    

class CVeiculos:
    def __init__(self, startTime=None, endTime=None):
        self.startTime = startTime
        self.endTime =  endTime

    def decimal_serializer(self,obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to string to preserve precision
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def Dic2Json2Dic(self,event):
        
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

    def lambda_handler_value_history(self, eventDic , context): #event
        try:

            print('lambda_handler_value_history')

            # pesquisa veiculo por placa

            retorno_ = self.PesquisarPorRequestLambdaDynamodb(eventDic)

            retorno_ = self.RetornarGetPropertyValueHistory(
                retornoPesquisa       = retorno_
                , selectedProperties    = eventDic['selectedProperties']
                , properties            = eventDic['properties']
                , entityId              = eventDic['entityId']
                , componentName         = eventDic['componentName']           
            )

            retorno =  json.dumps(retorno_, default=self.decimal_serializer) 
            retorno = retorno.encode('utf-8')        
            
            return retorno
        except Exception as e:
            print('== erro ==')
            print (e)
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            retorno = {'retorno': 'falha'}    

    def lambda_handler_value(self,eventDic, context):
        try:
            print('lambda_handler_value')

            # pesquisa veiculo por placa

            retorno_ = self.PesquisarPorRequestLambdaDynamodb(eventDic)

            print('retorno_=', retorno_)

            retorno_ = self.RetornarGetPropertyValue(
                retornoPesquisa       = retorno_
                , selectedProperties    = eventDic['selectedProperties']
                , properties            = eventDic['properties']
                , entityId              = eventDic['entityId']
                , componentName         = eventDic['componentName']           
            )

            retorno =  json.dumps(retorno_, default=self.decimal_serializer) 
            retorno = retorno.encode('utf-8')        

            #
            
            return retorno
        except Exception as e:
            print('== erro ==')
            print (e)
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            retorno = {'retorno': 'falha'}    

    def PropriedadesBuscar(self): # aws athena

        cAthena = CFAthena.CAThena()

        CatalogName = "AwsDataCatalog"
        DatabaseName = 'cmj-database'
        TableName = 'tfrotas'
        WorkGroup = 'primary'
        metaDados  = cAthena.ConsultarMetadadosTabela(CatalogName,DatabaseName,TableName,WorkGroup)

        retorno = []

        for propriedade in metaDados:  

            # de-para tipos de dados do aws twin 
            # 'RELATIONSHIP'|'STRING'|'LONG'|'BOOLEAN'|'INTEGER'|'DOUBLE'|'LIST'|'MAP'

            tipo_ = propriedade['tipo']
            tipo__ = 'STRING'
            match tipo_:
                case 'boolean':
                    tipo__ = 'BOOLEAN'
                case 'tinyint':
                    tipo__ = 'LONG'
                case 'smallint':
                    tipo__ = 'LONG'
                case 'int':
                    tipo__ = 'LONG'
                case 'bigint':
                    tipo__ = 'LONG'
                case 'double':
                    tipo__ = 'DOUBLE'
                case 'float':
                    tipo__ = 'DOUBLE'
                case 'decimal ':
                    tipo__ = 'DOUBLE'
                case 'char ':
                    tipo__ = 'STRING'
                # case 'varchar ':
                # case 'string ':
                # case 'binary'
                # case 'date'
                # case 'timestamp'
                case 'array' :
                    tipo__ = 'LIST'
                # case 'map' 
                # case 'struct' 


            propriedade_ =  {
                'propertyName' : propriedade['nome'] # 'telemetryAssetType'
                ,'type_' : tipo__ # propriedade['tipo'] # 'STRING'
                ,'isExternalId_' : False # true, se isRequiredInEntity_
                ,'isStoredExternally_' : False
                ,'isTimeSeries_' : False
                ,'isRequiredInEntity_' : False # true, se isExternalId_
                ,'value_' : 'ABC1969A'
            }      

            retorno.append(propriedade_)            
            
        return retorno
    
    def PropriedadesBuscarPorDicionario(self, dicionario): # python dic


        retorno = []

        fields_ = dicionario.__annotations__

        # for field in fields_:
        #     nome = field
        #     tipo = fields_[field]
        #     print ('nome=',nome,';tipo=',tipo)

        for propriedade in fields_:  

            # de-para tipos de dados do aws twin 
            # 'RELATIONSHIP'|'STRING'|'LONG'|'BOOLEAN'|'INTEGER'|'DOUBLE'|'LIST'|'MAP'

            tipo_ =  str(fields_[propriedade]).replace("<class '",'').replace("'>",'')
            tipo__ = 'STRING' # 'STRING'
            match tipo_:
                case 'bool': 
                    tipo__ = "BOOLEAN"
                case 'int' :# "tinyint"
                    tipo__ = "LONG"
                case 'int': #type(int) #  "smallint"
                    tipo__ = "LONG"
                case 'int' : #type(int) # "int"
                    tipo__ = "LONG"
                case 'long' : #type(long): # "bigint"
                    tipo__ = "LONG"
                case 'float' : # type(float): # "double"
                    tipo__ = "DOUBLE"
                case 'float' : #type(float): # "float"
                    tipo__ = "DOUBLE"
                case 'decimal.Decimal' : #type(Decimal): # "decimal "
                    tipo__ = "DOUBLE"
                case 'char' : #type(char): # "char "
                    tipo__ = "STRING"
                # case "varchar ":
                # case "string ":
                # case "binary"
                # case "date"
                # case "timestamp"
                case 'array': # array  : # "array"
                    tipo__ = "LIST"
                # case "map" 
                # case "struct" 

            propriedade_ =  {
                'propertyName' : propriedade 
                ,'type_' : tipo__ 
                ,'isExternalId_' : False # true, se isRequiredInEntity_
                ,'isStoredExternally_' : False
                ,'isTimeSeries_' : False
                ,'isRequiredInEntity_' : False # true, se isExternalId_
                ,'value_' : 'ABC1969A'
            }      

            retorno.append(propriedade_)            
            
        return retorno    

    def PropriedadesExternalSetar(self, propriedades, nomes):

        # propriedades[i]['isExternalId_'] = True
        # propriedades[i]['isRequiredInEntity_'] = True

        for nome in nomes:
            i = -1
            for propriedade in propriedades:
                i = i+1
                if i == 0:
                    if propriedade['propertyName'] == nome:
                        propriedades[i]['isStoredExternally_'] = True
    
    def PropriedadesTimeSeriesSetar(self, propriedades, nomes):

        for nome in nomes:
            i = -1
            for propriedade in propriedades:
                i = i+1
                if propriedade['propertyName'] == nome:
                    propriedades[i]['isTimeSeries_'] = True
                    # propriedades[i]['isExternalId_'] = False
                propriedades[i]['isStoredExternally_'] = True




        return propriedades    
            
    def VeiculosGerar(self,placas,anos, meses, dias, horas, minutos, velocidadeInicial, velocidadeIncrementoPercentual):  


        # time_ = time.time()
        agora = datetime.now()#.isoformat()

        anoAtual = agora.year
        mesAtual = agora.month
        diaAtual = agora.day
        horaAtual = 0# agora.hour
        minutoAtual = 0# agora.minute
        segundoAtual = 1# agora.second

        unidade_ = 'RPM'            

        veiculos = []

        id_ = -1
        placa__ = 1968


        for placa in range(1969,1969+placas):
            placa__ = placa__ + 1
            placa_ = 'ABC' +  str(10000+placa__)[1:5] + 'A'
            modelo_ = 'MODELO-' + str(placa__)            
            for ano in range(anoAtual, anoAtual+anos):
                for mes in range(mesAtual, mesAtual+meses):
                    for dia in range(diaAtual, diaAtual+dias):
                        velocidademotor_ = velocidadeInicial                        
                        for hora in range(horaAtual, horaAtual+horas):
                            for minuto in range(minutoAtual, 60,int(60/minutos)):

                                time_ = datetime(year=ano, month=mes,day=dia, hour=hora, minute=minuto, second=segundoAtual)
                                # time_ = datetime.now(timezone.utc) #   "2022-08-25T00:00:00Z"
                                time_ = time_.isoformat(timespec='milliseconds') + 'Z'                
                                # time_ = int(time_.timestamp())

                                random_ = Decimal(str(random.random()))
                                temperatura_ = Decimal(random_  * velocidademotor_)

                                id_ = id_ +1
                                veiculo = {
                                    'id':id_
                                    ,'placa':placa_
                                    ,'modelo':modelo_
                                    ,'velocidademotor':velocidademotor_
                                    ,'velocidademotoratual':velocidademotor_
                                    ,'unidade':unidade_
                                    ,'time':time_
                                    ,'temperatura' : temperatura_
                                }

                                veiculo_ = CVeiculo()
                                veiculo_.id = id_
                                veiculo_.placa = placa_
                                veiculo_.modelo = modelo_
                                veiculo_.velocidademotor = velocidademotor_
                                veiculo_.velocidademotoratual = velocidademotor_
                                veiculo_.unidade = unidade_
                                veiculo_.time = time_
                                veiculo_.temperatura = temperatura_

                                velocidademotor_ = Decimal(str(velocidademotor_ )) *  Decimal(str(velocidadeIncrementoPercentual))

                                # veiculos.append(veiculo)
                                veiculo__ = asdict(veiculo_)
                                veiculos.append(veiculo__)



        return veiculos

    def JsonGerar(self):

        qtdeLinhas = 10

        veiculos = []

        for i in range(qtdeLinhas):
            veiculo = self.VeiculosGerar(i)
            veiculos.append(veiculo)

        retorno =  json.dumps(veiculos)

        return retorno

        # with open('veiculos.json', 'w') as file:
        #     json.dump(veiculos, file, indent=4)        

    def FlatGerar(self):

        qtdeLinhas = 10

        veiculos = []

        for i in range(qtdeLinhas):
            veiculo = self.VeiculosGerar(i+1969)

            veiculo_ = ''
            veiculo_ = veiculo_ + str(veiculo['id'])            + ',' + str(veiculo['placa'])            + ',' + str(veiculo['modelo'])            + ',' + str(veiculo['velocidademotor'])            + ',' + str(veiculo['unidade'])            + ',' + str(veiculo['time'])

            veiculos.append(veiculo_)

        # retorno =  json.dumps(veiculos)

        retorno = "id,placa,modelo,velocidademotor,unidade,time\r\n"
        for veiculo in veiculos:
            retorno = retorno + veiculo + '\r\n'

        return retorno

        # with open('veiculos.json', 'w') as file:
        #     json.dump(veiculos, file, indent=4)               

    def JsonDynamoGerar(self):

        veiculos = self.VeiculosGerar(placas=3, anos=1 ,meses=1,dias=2,horas=12,minutos=3,velocidadeInicial=60,velocidadeIncrementoPercentual=1.10)

        cDynamodb = CFDynamodb.CDynamodb()
        for veiculo in veiculos:

            cDynamodb.Incluir(nomeTabela='Frotas', entidade=veiculo) # veiculo

    def PesquisarPorPlacaFake(self, placa):
        retorno = {
            "statusCode": 200,
            "body": {
                "UpdateCount": 0,
                "ResultSet": {
                    "Rows": [
                        {
                            "Data": [
                                {
                                    "VarCharValue": "id"
                                },
                                {
                                    "VarCharValue": "placa"
                                },
                                {
                                    "VarCharValue": "modelo"
                                },
                                {
                                    "VarCharValue": "velocidademotor"
                                },
                                {
                                    "VarCharValue": "unidade"
                                },
                                {
                                    "VarCharValue": "time"
                                }
                            ]
                        },
                        {
                            "Data": [
                                {
                                    "VarCharValue": "1969"
                                },
                                {
                                    "VarCharValue": "ABC1969A"
                                },
                                {
                                    "VarCharValue": "MODELO-1969"
                                },
                                {
                                    "VarCharValue": "31690.1234"
                                },
                                {
                                    "VarCharValue": "RPM"
                                },
                                {
                                    "VarCharValue": "2025-09-17 13:18:34.091"
                                }
                            ]
                        }
                    ],
                    "ResultSetMetadata": {
                        "ColumnInfo": [
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "id",
                                "Label": "id",
                                "Type": "bigint",
                                "Precision": 19,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "false"
                            },
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "placa",
                                "Label": "placa",
                                "Type": "varchar",
                                "Precision": 2147483647,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "true"
                            },
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "modelo",
                                "Label": "modelo",
                                "Type": "varchar",
                                "Precision": 2147483647,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "true"
                            },
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "velocidademotor",
                                "Label": "velocidademotor",
                                "Type": "double",
                                "Precision": 17,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "false"
                            },
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "unidade",
                                "Label": "unidade",
                                "Type": "varchar",
                                "Precision": 2147483647,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "true"
                            },
                            {
                                "CatalogName": "hive",
                                "SchemaName": "",
                                "TableName": "",
                                "Name": "time",
                                "Label": "time",
                                "Type": "timestamp",
                                "Precision": 3,
                                "Scale": 0,
                                "Nullable": "UNKNOWN",
                                "CaseSensitive": "false"
                            }
                        ]
                    }
                },
                "ResponseMetadata": {
                    "RequestId": "652d232d-4dce-4967-bb6a-a03ff354ee61",
                    "HTTPStatusCode": 200,
                    "HTTPHeaders": {
                        "date": "Fri, 19 Sep 2025 12:34:38 GMT",
                        "content-type": "application/x-amz-json-1.1",
                        "content-length": "2740",
                        "connection": "keep-alive",
                        "x-amzn-requestid": "652d232d-4dce-4967-bb6a-a03ff354ee61"
                    },
                    "RetryAttempts": 0
                }
            }
        }

        return retorno
        
    def PesquisarPorPlaca(self, placa):

        cAthena = CFAthena.CAThena()

        s1 = "'"
        s2 = '"'
        QUERY = "select a.* from tfrotas a where a.placa = '" +  placa  + "'";
        
        retorno = cAthena.Pesquisar(DatabaseName='cmj-database', QUERY=QUERY)

        return retorno  

    def PesquisarPorPlacaDynamo(self, placa, startTime, endTime):

        cDynamodb = CFDynamodb.CDynamodb()

        retorno = cDynamodb.Pesquisar(
             nomeTabela="Frotas"
            ,condicao={
                 'chave': 'placa'
                ,'valor' : placa 
                ,'startTime':startTime
                ,'endTime':endTime
            }
        )

        return retorno         

    def BuscarValor(self, nomePropridadade, linhas):

        i = -1
        for linha_ in linhas['Data']:
            i = i +1
            nomePropridadade_ = linha_['VarCharValue']
            if nomePropridadade_.lower() == nomePropridadade.lower():
                return i

        return -1
    
    def BuscarTipo(self, tipo): 
            # de ==> tipo = RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP
            # para ==> booleanValue  doubleValue expression integerValue  listValue  longValue mapValue relationshipValue stringValue
            tipo__ = 'stringValue'
            match tipo:
                # case 'RELATIONSHIP':
                # case 'STRING':
                case 'LONG':
                    tipo__ = 'longValue'
                case 'BOOLEAN':
                    tipo__ = 'booleanValue'
                case 'INTEGER':
                    tipo__ = 'integerValue'
                case 'DOUBLE':
                    tipo__ = 'doubleValue'
                case 'LIST':
                    tipo__ = 'listValue'
                case 'MAP ':
                    tipo__ = 'mapValue'               
            return tipo__

    def PesquisarPorRequestLambdaFake(self,request):
           propertyValues = []
           retorno = {
                "propertyValues" :propertyValues
                # ,'nextToken': None
            }
           
           return retorno
    
    def PesquisarPorRequestLambdaAthena(self,request):
            
            # return self.PesquisarPorRequestLambdaFake(request)
          
            # dados da requisicao

            componentName = request['componentName']
            placa = componentName

            entityId = request['entityId']
                        
            selectedProperties = request['selectedProperties']

            properties =  request['properties']

            # obter placa

            request_ = request

            cComponentResponse = CFIotTwinMaker.CComponentResponse()

            # placa = cComponentResponse.RequestExtrairNome(request = request_)   

            # pesquisar por placa

            retornoPesquisa = self.PesquisarPorPlaca(placa)  

            # montar response

            status = retornoPesquisa['statusCode']

            linhas =  retornoPesquisa['body']['ResultSet']['Rows']

            propertyValues = []

            if len(linhas) >= 2:

                timestamp =  1646426606 #   time.time()
                time_ = datetime.now(timezone.utc) #   "2022-08-25T00:00:00Z"
                time = time_.isoformat(timespec='milliseconds') + 'Z'                

                for selectedProperty in selectedProperties:  

                    propertyName = selectedProperty  

                    #busca os valores
                    values = []

                    i = -1
                    for linha in linhas: 
                        i = i + 1

                        if i >= 1:
                            indice = self.BuscarValor(nomePropridadade=propertyName,linhas=linhas[0])
                                                        
                            valor = linha['Data'][indice]['VarCharValue']

                            #  busca e ajusta o tipo

                            type_ = properties[propertyName]['definition']['dataType']['type'] 
                            type = self.BuscarTipo(type_)
                            #
                            value = {
                                'timestamp' : timestamp
                                # 'time' : time                                
                                ,'value' : {
                                     type : valor # 'stringValue' : valor
                                }
                            }

                            values.append(value)
                                
                    propertyValue = {
                            'entityPropertyReference' :{
                                'entityId': entityId
                                ,'componentName': componentName
                                ,'propertyName': propertyName
                            }
                            ,
                            'values': values
                        }      
                    propertyValues.append(propertyValue)                            

            # monta retorno        

            retorno = {
                'propertyValues' :propertyValues
                ,'nextToken': None
            }

            return retorno
    
    def PesquisarPorRequestLambdaDynamodb(self,request):
        
            # dados da requisicao

            componentName = request['componentName']
            placa = componentName

            entityId = request['entityId']
                        
            selectedProperties = request['selectedProperties']
            # if selectedProperties['time'] == None:
            #     selectedProperties.append('time')

            properties =  request['properties']

            # obter placa

            request_ = request

            cComponentResponse = CFIotTwinMaker.CComponentResponse()

            # placa = cComponentResponse.RequestExtrairNome(request = request_)   

            # pesquisar por placa

            # startTime =  request['startTime']
            # endTime =  request['endTime']

            startTime = self.startTime 
            endTime =  self.endTime

            retornoPesquisa = self.PesquisarPorPlacaDynamo(placa, startTime, endTime)  

            return retornoPesquisa

            # montar response

            # status = retornoPesquisa['ResponseMetadata']['HTTPStatusCode']

            # linhas =  retornoPesquisa['Items']

            # propertyValues = []

            # if len(linhas) >= 1:

            #     timestamp = time.time()
            #     # timestamp = timestamp.isoformat(timespec='milliseconds')# + 'Z'#  1646426606 #   time.time()
            #     # time = time_.isoformat(timespec='milliseconds') + 'Z'                

            #     for selectedProperty in selectedProperties:  

            #         propertyName = selectedProperty  

            #         #busca os valores
            #         values = []

            #         for linha in linhas: 

            #             print('==linha["time"]===')                   
            #             print(linha['time'])

            #             valor = linha[propertyName]
            #             timestamp = int(datetime.fromisoformat(linha['time']).timestamp())
            #             # timestamp = linha['time'] 

            #             print('==linha[timestamp]===')                   
            #             print(timestamp)

            #             #  busca e ajusta o tipo

            #             type_ = properties[propertyName]['definition']['dataType']['type'] 
            #             type = self.BuscarTipo(type_)
            #             #
            #             value = {
            #                 'timestamp' : timestamp
            #                 ,'value' : {
            #                         type : valor # 'stringValue' : valor
            #                 }
            #             }

            #             print('===value===')
            #             print(value)

            #             values.append(value)
                            
            #         propertyValue = {
            #                 'entityPropertyReference' :{
            #                     'entityId': entityId
            #                     ,'componentName': componentName
            #                     ,'propertyName': propertyName
            #                 }
            #                 ,
            #                 'values': values
            #             }      
            #         propertyValues.append(propertyValue)                            

            # # monta retorno        

            # retorno = {
            #     'propertyValues' :propertyValues
            #     ,'nextToken': None
            # }      

            # return retorno    

    def RetornarGetPropertyValueHistory(self, retornoPesquisa, selectedProperties, properties, entityId, componentName):

        # montar response

        status = retornoPesquisa['ResponseMetadata']['HTTPStatusCode']

        linhas =  retornoPesquisa['Items']

        # montar retorno

        propertyValues = []

        if len(linhas) >= 1:

            timestamp = time.time()
            # timestamp = timestamp.isoformat(timespec='milliseconds')# + 'Z'#  1646426606 #   time.time()
            # time = time_.isoformat(timespec='milliseconds') + 'Z'                

            for selectedProperty in selectedProperties:  

                propertyName = selectedProperty  

                #busca os valores
                values = []

                for linha in linhas: 


                    valor = linha[propertyName]
                    timestamp = int(datetime.fromisoformat(linha['time']).timestamp())
                    # timestamp = linha['time'] 


                    #  busca e ajusta o tipo

                    type_ = properties[propertyName]['definition']['dataType']['type'] 
                    type = self.BuscarTipo(type_)
                    #
                    value = {
                        'timestamp' : timestamp
                        ,'value' : {
                                type : valor # 'stringValue' : valor
                        }
                    }

                    values.append(value)
                        
                propertyValue = {
                        'entityPropertyReference' :{
                            'entityId': entityId
                            ,'componentName': componentName
                            ,'propertyName': propertyName
                        }
                        ,
                        'values': values
                    }      
                propertyValues.append(propertyValue)                            

        # monta retorno        

        retorno = {
            'propertyValues' :propertyValues
            ,'nextToken': None
        }      

        return retorno    

    def RetornarGetPropertyValue(self, retornoPesquisa, selectedProperties, properties, entityId, componentName):
        # montar response

        status = retornoPesquisa['ResponseMetadata']['HTTPStatusCode']

        linhas =  retornoPesquisa['Items']

        # montar retorno

        propertyValues = {}

        if len(linhas) >= 1:

            timestamp = time.time()
            # timestamp = timestamp.isoformat(timespec='milliseconds')# + 'Z'#  1646426606 #   time.time()
            # time = time_.isoformat(timespec='milliseconds') + 'Z'                

            for selectedProperty in selectedProperties:  

                propertyName = selectedProperty  

                #busca os valores
                values = []

                for linha in linhas: 



                    valor = linha[propertyName]
                    timestamp = int(datetime.fromisoformat(linha['time']).timestamp())
                    # timestamp = linha['time'] 



                    #  busca e ajusta o tipo

                    type_ = properties[propertyName]['definition']['dataType']['type'] 
                    type = self.BuscarTipo(type_)
                    #
                    # value = {
                    #     'timestamp' : timestamp
                    #     ,'value' : {
                    #             type : valor # 'stringValue' : valor
                    #     }
                    # }

                    value = {
                                type : valor # 'stringValue' : valor
                    }                    

                    # values.append(value)

                    break
                        
                propertyValue = {
                    propertyName : 
                        { 
                                'propertyReference' :{
                                    'entityId': entityId
                                    ,'componentName': componentName
                                    ,'propertyName': propertyName
                                }
                                ,
                                'propertyValue': value# values
                        }                          
                }
                

                # propertyValues.append(propertyValue)                            

        # monta retorno        

        retorno = {
            'propertyValues' :propertyValue
            ,'nextToken': None
        }      

        return retorno    

@dataclass
class CVeiculo:
    id: int
    placa:str
    modelo:str
    velocidademotor:Decimal
    velocidademotoratual:Decimal
    unidade:str
    time:datetime
    temperatura: Decimal

    def __init__(self):
        # getcontext().prec = 6    
        None


        

