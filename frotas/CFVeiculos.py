import time
from  datetime import datetime, timezone
import json
import CFAthena
import CFIotTwinMaker
import CFDynamodb
from decimal import *

class CVeiculos:



    def PropriedadesBuscar(self):

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

        return retorno

    def PropriedadesExternalSetar(self, propriedades, nomes):

        for nome in nomes:
            i = -1
            for propriedade in propriedades:
                i = i+1
                if propriedade['propertyName'] == nome:
                    propriedades[i]['isTimeSeries_'] = True
                    propriedades[i]['isStoredExternally_'] = True
                    # propriedades[i]['isExternalId_'] = True
                    # propriedades[i]['isRequiredInEntity_'] = True

                    


        return propriedades
            
    # def VeiculosGerar(self,i):  

    #     getcontext().prec = 6          

    #     id_ = i
    #     placa_ = 'ABC' + str(i) + 'A'
    #     modelo_ = 'MODELO-' + str(i)
    #     velocidademotor_ = Decimal(str(12000 + (10*i) + 0.1234))
    #     unidade_ = 'RPM'
    #     time_ = time.time()
    #     time_ = datetime.now().isoformat()

    #     veiculo = {
    #         'id':id_
    #         ,'placa':placa_
    #         ,'modelo':modelo_
    #         ,'velocidademotor':velocidademotor_
    #         ,'unidade':unidade_
    #         ,'time':time_
    #     }

    #     return veiculo

    def VeiculosGerar(self,placas,anos, meses, dias, horas, minutos, velocidadeInicial, velocidadeIncrementoPercentual):  

        getcontext().prec = 6    

        # time_ = time.time()
        agora = datetime.now()#.isoformat()

        anoAtual = agora.year
        mesAtual = agora.month
        diaAtual = agora.day
        horaAtual = 0# agora.hour
        minutoAtual = 0# agora.minute

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

                                time_ = datetime(year=ano, month=mes,day=dia, hour=hora, minute=minuto)
                                time_ = time_.isoformat(timespec='milliseconds') + 'Z'                


                                id_ = id_ +1
                                veiculo = {
                                    'id':id_
                                    ,'placa':placa_
                                    ,'modelo':modelo_
                                    ,'velocidademotor':velocidademotor_
                                    ,'unidade':unidade_
                                    ,'time':time_
                                }

                                velocidademotor_ = int(velocidademotor_ *  velocidadeIncrementoPercentual)


                                veiculos.append(veiculo)



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

            cDynamodb.Incluir(nomeTabela='Frotas', entidade=veiculo)

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

    def PesquisarPorPlacaDynamo(self, placa):

        # retorno_ =  self.PesquisarPorPlacaFake(placa)
        # return retorno_

        cDynamodb = CFDynamodb.CDynamodb()

        retorno = cDynamodb.Pesquisar(
             nomeTabela="Frotas"
            ,condicao={
                 'chave': 'placa'
                ,'valor' : placa 
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

            properties =  request['properties']

            # obter placa

            request_ = request

            cComponentResponse = CFIotTwinMaker.CComponentResponse()

            # placa = cComponentResponse.RequestExtrairNome(request = request_)   

            # pesquisar por placa

            retornoPesquisa = self.PesquisarPorPlacaDynamo(placa)  

            # montar response

            status = retornoPesquisa['ResponseMetadata']['HTTPStatusCode']

            linhas =  retornoPesquisa['Items']

            propertyValues = []

            if len(linhas) >= 1:

                timestamp =  1646426606 #   time.time()
                time_ = datetime.now(timezone.utc) #   "2022-08-25T00:00:00Z"
                time = time_.isoformat(timespec='milliseconds') + 'Z'                

                for selectedProperty in selectedProperties:  

                    propertyName = selectedProperty  

                    #busca os valores
                    values = []

                    for linha in linhas: 

                        if True : 
                                                        
                            valor = linha[propertyName]

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