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
import CFUtil

getcontext().prec = 6    

class CComponentes:

    def __init__(self, startTime=None, endTime=None):
        self.startTime = startTime
        self.endTime =  endTime
        self.nomeTabela = 'Componentes'
        self.cUtil = CFUtil.CUtil()

    def Incluir(self,entidade):
                
        # se existir não inclui

        mac = entidade['mac']
        entidade['time'] = self.cUtil.DataHoraBuscar()

        retorno = self.PesquisarPorMacDynamo(mac)

        if retorno['Count'] == 0: # não existe, deve incluir

            # incluir de fato

            cDynamodb = CFDynamodb.CDynamodb()
            retorno = cDynamodb.Incluir(nomeTabela=self.nomeTabela, entidade=entidade) # veiculo

        return retorno
    
    def PesquisarPorMacDynamo(self, mac):

        cDynamodb = CFDynamodb.CDynamodb()

        retorno = cDynamodb.Pesquisar(
             nomeTabela="Componentes"
            ,condicao={
                 'chave': 'mac'
                ,'valor' : mac 
                ,'startTime':None   
            }
        )

    def PesquisarDynamo(self):

        cDynamodb = CFDynamodb.CDynamodb()

        retorno = cDynamodb.Listar(
             nomeTabela="Componentes"
        )        

        return retorno         

@dataclass
class CComponente:
    id: int
    mac : str
    time:datetime

    # placa:str
    # modelo:str

    # velocidademotor:Decimal
    # velocidademotoratual:Decimal
    # unidade:str
    # temperatura: Decimal
    # alarm_status: str
    # thingname:str
    # angulo: Decimal # 0 = 180 graus = tombado pé; 1 = 90 graus = de pé

    def __init__(self):
        # getcontext().prec = 6    
        None