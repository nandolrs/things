import time
import json
import random
import base64
import requests
import os
from  datetime import datetime, timezone
from decimal import *
from dataclasses import dataclass, asdict

import CFS3
import CFAthena
import CFIotTwinMaker
import CFDynamodb
import CFAutenticador
getcontext().prec = 6    

class CVeiculos:
    def __init__(self, startTime=None, endTime=None):
        self.startTime = startTime
        self.endTime =  endTime
        self.nomeTabela = 'Frotas'

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

            # pesquisa e monta retorno no formato Grafana

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

    def lambda_handler_value_history_porApi(self, eventDic , context): #event
        try:

            # pesquisa veiculo por placa

            placa = eventDic['queryStringParameters']['placa']
            startTime = eventDic['queryStringParameters']['startTime']
            endTime = eventDic['queryStringParameters']['endTime']

            retorno_  = self.PesquisarPorPlacaDynamo(placa, startTime, endTime)       
            retorno_ = json.dumps(retorno_, default=self.decimal_serializer)

            retorno_ = {
                "isBase64Encoded": True,
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" 
                },
                "body": retorno_
            }
            
            retorno =  json.dumps(retorno_, default=self.decimal_serializer) 
            retorno = retorno.encode('utf-8')        
            
            return retorno
        

        except Exception as e:
            print('== erro ==')
            print (e)
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            retorno = {'retorno': 'falha'}    

#
    def lambda_handler_value(self,eventDic, context):
        try:

            # pesquisa e monta retorno no formato grafana

            retorno_ = self.PesquisarPorRequestLambdaDynamodb(eventDic)

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

    def parse_decimal(self,valor):
        return str(Decimal(valor))
    
    def lambda_handler_iotcore(self,eventDic, context):
        try:

            agora = datetime.now()
            time_ =     self.DataHoraIsoBuscar(ano=agora.year, mes=agora.month, dia=agora.day, hora=agora.hour, minuto=agora.minute, segundo=agora.second)

            veiculo_ = CVeiculo()
            veiculo_.id = 0
            veiculo_.placa = eventDic['thingname']  # 'ABC1969A'
            veiculo_.mac = eventDic['mac']  # 'ABC1969A'
            veiculo_.thingname = eventDic['thingname']  # 'ABC1969A'
            veiculo_.modelo = 'MODELO ABC'
            veiculo_.velocidademotor = self.parse_decimal(eventDic['velocidademotor']) 
            veiculo_.velocidademotoratual = self.parse_decimal(eventDic['velocidademotor']) 
            veiculo_.unidade = 'RPM'
            veiculo_.time = time_
            veiculo_.temperatura = self.parse_decimal(eventDic['temperatura'])
            veiculo_.alarm_status = 'NORMAL'            

            veiculo__ = asdict(veiculo_)

            retorno_ =  veiculo__     

            # incluir

            retorno_ = self.Incluir(retorno_)

            #

            # retorno =  json.dumps(retorno_, default=self.decimal_serializer) 
            retorno =  json.dumps(retorno_) 
            retorno = retorno.encode('utf-8')        

            #
            
            return retorno
        except Exception as e:
            print('== erro ==')
            print (e)
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            retorno = {'retorno': 'falha'}    

    def Incluir(self,entidade):
            cDynamodb = CFDynamodb.CDynamodb()
            retorno = cDynamodb.Incluir(nomeTabela=self.nomeTabela, entidade=entidade) # veiculo

            return retorno

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
                propriedades[i]['isStoredExternally_'] = True

        return propriedades    


    def DataHoraIsoBuscar(self, ano, mes, dia, hora, minuto, segundo):
        
        time_ = datetime(year=ano, month=mes,day=dia, hour=hora, minute=minuto, second=segundo)
        time_ = time_.isoformat(timespec='milliseconds') + 'Z'    
        return time_            


    def VeiculosGerar(self,placas,anos, meses, dias, horas, minutos, velocidadeInicial, velocidadeIncrementoPercentual):  

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

                                # time_ = datetime(year=ano, month=mes,day=dia, hour=hora, minute=minuto, second=segundoAtual)
                                # time_ = time_.isoformat(timespec='milliseconds') + 'Z'                
                                time_ = self.DataHoraIsoBuscar(ano=ano, mes=mes,dia=dia, hora=hora, minuto=minuto, segundo=segundoAtual)

                                random_ = Decimal(str(random.random()))
                                temperatura_ = Decimal(random_  * velocidademotor_)

                                alarm_status_ = 'NORMAL'

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
                                    ,'alarm_status' : alarm_status_

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
                                veiculo_.alarm_status = alarm_status_

                                velocidademotor_ = Decimal(str(velocidademotor_ )) *  Decimal(str(velocidadeIncrementoPercentual))

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

    def FlatGerar(self):

        qtdeLinhas = 10

        veiculos = []

        for i in range(qtdeLinhas):
            veiculo = self.VeiculosGerar(i+1969)

            veiculo_ = ''
            veiculo_ = veiculo_ + str(veiculo['id'])            + ',' + str(veiculo['placa'])            + ',' + str(veiculo['modelo'])            + ',' + str(veiculo['velocidademotor'])            + ',' + str(veiculo['unidade'])            + ',' + str(veiculo['time'])

            veiculos.append(veiculo_)

        retorno = "id,placa,modelo,velocidademotor,unidade,time\r\n"
        for veiculo in veiculos:
            retorno = retorno + veiculo + '\r\n'

        return retorno           

    def JsonDynamoGerar(self):

        veiculos = self.VeiculosGerar(placas=3, anos=1 ,meses=1,dias=2,horas=12,minutos=3,velocidadeInicial=60,velocidadeIncrementoPercentual=1.10)

        cDynamodb = CFDynamodb.CDynamodb()
        for veiculo in veiculos:

            # cDynamodb.Incluir(nomeTabela='Frotas', entidade=veiculo) # veiculo
            self.Incluir(veiculo)

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

    def PesquisarPorPlacaApi(self, placa, startTime, endTime):

        #gera toker

        cAutenticador = CFAutenticador.CAutenticador()

        token = cAutenticador.TokenGerar()

        tokenHeaders = cAutenticador.TokenHeadersObter(token)

        # monta requisição

        url_ = "?placa="+placa+"&startTime="+startTime+"&endTime="+endTime

        url = os.environ['url']

        url =  url + url_

        #

        response = requests.get(url, tokenHeaders) # 

        if response.status_code == 200:
            retorno = response.json()
        else:
            retorno = {}
            print(f"Request failed with status code: {response.status_code}")

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
            }
           
           return retorno
    
    def PesquisarPorRequestLambdaAthena(self,request):
                      
            # dados da requisicao

            componentName = request['componentName']
            placa = componentName

            entityId = request['entityId']
                        
            selectedProperties = request['selectedProperties']

            properties =  request['properties']

            # obter placa

            request_ = request

            cComponentResponse = CFIotTwinMaker.CComponentResponse()

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
                                ,'value' : {
                                     type : valor 
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

            # pesquisar por placa

            startTime = self.startTime 
            endTime =  self.endTime

            # retornoPesquisa = self.PesquisarPorPlacaDynamo(placa, startTime, endTime)  
            retornoPesquisa = self.PesquisarPorPlacaApi(placa, startTime, endTime)  

            return retornoPesquisa

    def RetornarGetPropertyValueHistory(self, retornoPesquisa, selectedProperties, properties, entityId, componentName):

        # montar response

        status = retornoPesquisa['ResponseMetadata']['HTTPStatusCode']

        linhas =  retornoPesquisa['Items']

        # montar retorno

        propertyValues = []

        if len(linhas) >= 1:

            timestamp = time.time()

            for selectedProperty in selectedProperties:  

                propertyName = selectedProperty  

                #busca os valores
                values = []

                for linha in linhas: 

                    valor = linha[propertyName]
                    timestamp = int(datetime.fromisoformat(linha['time']).timestamp())

                    #  busca e ajusta o tipo

                    type_ = properties[propertyName]['definition']['dataType']['type'] 
                    type = self.BuscarTipo(type_)

                    #

                    value = {
                        'timestamp' : timestamp
                        ,'value' : {
                                type : valor 
                        }
                    }

                    values.append(value)
                        
                propertyValue = {
                        'entityPropertyReference' :{
                            'entityId': entityId
                            ,'componentName': componentName
                            ,'propertyName': propertyName
                            ,'externalIdProperty':{
                                'alarm_key':entityId
                            }
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

            for selectedProperty in selectedProperties:  

                propertyName = selectedProperty  

                #busca os valores

                values = []

                for linha in linhas: 

                    valor = linha[propertyName]
                    timestamp = int(datetime.fromisoformat(linha['time']).timestamp())

                    #  busca e ajusta o tipo

                    type_ = properties[propertyName]['definition']['dataType']['type'] 
                    type = self.BuscarTipo(type_)

                    value = {
                                type : valor # 'stringValue' : valor
                    }                    

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
    alarm_status: str
    mac : str
    thingname:str

    def __init__(self):
        # getcontext().prec = 6    
        None


        

