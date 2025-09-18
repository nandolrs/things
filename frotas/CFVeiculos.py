import time
from  datetime import datetime
import json
import CFAthena
import CFIotTwinMaker

class CVeiculos:

    def PropriedadesBuscar(self):
            
        retorno = [
            {
            'propertyName' : 'telemetryAssetType'
            ,'type_' : 'STRING'
            ,'isExternalId_' : False # true, se isRequiredInEntity_
            ,'isStoredExternally_' : False
            ,'isTimeSeries_' : False
            ,'isRequiredInEntity_' : False # true, se isExternalId_
            ,'value_' : 'ABDC'


            }
            ,
            {
            'propertyName' : 'telemetryAssetId'
            ,'type_' : 'STRING'
            ,'isExternalId_' : True # true, se isRequiredInEntity_
            ,'isStoredExternally_' : False
            ,'isTimeSeries_' : False
            ,'isRequiredInEntity_' : True # true, se isExternalId_
            ,'value_' : 'ABDC'
            }            

            ,
            {
            'propertyName' : 'PLACA'
            ,'type_' : 'STRING'
            ,'isExternalId_' : False # true, se isRequiredInEntity_
            ,'isStoredExternally_' : True
            ,'isTimeSeries_' : True
            ,'isRequiredInEntity_' : False # true, se isExternalId_
            ,'value_' : 'ABDC'
            }            


        ]    

        return retorno
        
    def VeiculosGerar(self,i):    

        id_ = i
        placa_ = 'ABC' + str(i) + 'A'
        modelo_ = 'MODELO-' + str(i)
        velocidademotor_ = 12000 + (10*i) + 0.1234
        unidade_ = 'RPM'
        time_ = time.time()
        time_ = datetime.now().isoformat()

        veiculo = {
            'id':id_
            ,'placa':placa_
            ,'modelo':modelo_
            ,'velocidademotor':velocidademotor_
            ,'unidade':unidade_
            ,'time':time_
        }

        return veiculo

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

    def PesquisarPorPlaca(self, placa):

        cAthena = CFAthena.CAThena()

        s1 = "'"
        s2 = '"'
        QUERY = "select a.* from tfrotas a where a.placa = '" +  placa  + "'";
        
        retorno = cAthena.Pesquisar(DatabaseName='cmj-database', QUERY=QUERY)

        return retorno    

    def BuscarValor(self, nomePropridadade, linhas):

        i = -1
        for linha_ in linhas['Data']:
            i = i +1
            nomePropridadade_ = linha_['VarCharValue']
            if nomePropridadade_.lower() == nomePropridadade.lower():
                return i

        return -1

    def PesquisarPorRequestLambda(self,request):
          
            # dados da requisicao

            componentName = request['componentName']

            entityId = request['entityId']
                        
            selectedProperties = request['selectedProperties']

            # obter placa

            request_ = request

            cComponentResponse = CFIotTwinMaker.CComponentResponse()

            placa = cComponentResponse.GetPropertyValueHistory(request = request_)   

            # pesquisar por placa

            retornoPesquisa = self.PesquisarPorPlaca(placa) 

            # montar response

            status = retornoPesquisa['statusCode']

            linhas =  retornoPesquisa['body']['ResultSet']['Rows']

            propertyValues = []

            timestamp = 1646426606

            for selectedProperty in selectedProperties:  

                propertyName = selectedProperty  

                #busca os valores
                values = []

                i = -1
                for linha in linhas: 
                    i = i + 1
                    if i > 0:
                        
                        indice = self.BuscarValor(nomePropridadade=propertyName,linhas=linhas[0])
                        
                        valor = linha['Data'][indice]['VarCharValue']

                        value = {
                            'timestamp' : timestamp
                            ,'value' : {
                                'stringValue' : valor
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

            # retorno = json.dumps(retorno)

            return retorno