import time
from  datetime import datetime
import json
import CFAthena

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
        placa_ = 'ABC' + str(i)
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
            print(i)

        retorno =  json.dumps(veiculos)

        return retorno

        # with open('veiculos.json', 'w') as file:
        #     json.dump(veiculos, file, indent=4)        

    def FlatGerar(self):

        qtdeLinhas = 10

        veiculos = []

        for i in range(qtdeLinhas):
            veiculo = self.VeiculosGerar(i+100)

            veiculo_ = ''
            veiculo_ = veiculo_ + str(veiculo['id'])            + ',' + str(veiculo['placa'])            + ',' + str(veiculo['modelo'])            + ',' + str(veiculo['velocidademotor'])            + ',' + str(veiculo['unidade'])            + ',' + str(veiculo['time'])

            veiculos.append(veiculo_)
            print(i)

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
        QUERY = 'select a.* from tfrotas a where a.placa = ' + s1 + s2 + placa + s2 + s1;
        
        retorno = cAthena.Pesquisar(DatabaseName='cmj-database', QUERY=QUERY)

        return retorno    
