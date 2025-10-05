import time

from typing import Union
# from fastapi import FastAPI
# import uvicorn


import boto3
import boto3.dynamodb.types
from boto3.dynamodb.conditions import Key, Attr

# from pydantic import BaseModel
from typing import Union

#import json
from  decimal import Decimal

class CDynamodb:

    def __init__(self):
        # self.cliente = boto3.client('dynamodb',region_name='us-east-1')
        # self.recurso = boto3.resource('dynamodb',region_name='us-east-1')

        self.cliente = boto3.client('dynamodb') # ,region_name='sa-east-1'
        self.recurso = boto3.resource('dynamodb') # ,region_name='sa-east-1'

#
    # class Clima(BaseModel) :
    #     id: int
    #     nome: Union[str, None] = None
    #     temperatura: Union[Decimal, None] = None
    #     pressao: Union[Decimal, None] = None
    #     umidade: Union[Decimal, None] = None    
    #     situacao: Union[str, None] = None
    #     IP: Union[str, None] = None

    def parse_float(value) :
        return Decimal(str(value))

    def DynamoTabela(self,nomeTabela) :

        # dynamodb = boto3.resource('dynamodb')

        # return dynamodb.Table(nomeTabela)    

        retorno = self.recurso.Table(nomeTabela)

        return retorno

    def DynamoBuscaS(self,nomeTabela, filtro) :
        
        tabela = self.DynamoTabela(nomeTabela)   

        return tabela.scan(FilterExpression=filtro)
    
        
    def IncluirID(self,tabelaNome) :

        table = self.DynamoTabela('TabelasIndices')

        documento = {"tabelaNome" : tabelaNome, "ultimoIndice" : 1}

        table.put_item(Item=documento)

        return  1

    def ConsultarID(self, tabelaNome) :

        scan = self.DynamoBuscaS('TabelasIndices', Attr('tabelaNome').eq(tabelaNome) ) #table.scan(FilterExpression=Attr('tabelaNome').eq(tabelaNome))

        retorno = 0

        if len(scan['Items']) == 0 : # adicionar
            retorno = self.IncluirID(tabelaNome)
        else : # alterar
            documento = scan['Items'][0]
            documento['ultimoIndice'] = documento['ultimoIndice'] + 1
            self.Alterar('TabelasIndices', documento,0)
            retorno = documento['ultimoIndice']

        return retorno

    def Incluir(self,nomeTabela, entidade) :

        if entidade['id'] == 0:
            entidade['id'] =self.ConsultarID(nomeTabela)

        table = self.DynamoTabela(nomeTabela)

        table.put_item(Item=entidade)

        return entidade

    # def Incluir(self,nomeTabela, entidade) :

    #     entidade.id =self.ConsultarID(nomeTabela)

    #     table = DynamoTabela(nomeTabela)

    #     entidadeDicionario = entidade

    #     #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

    #     table.put_item(Item=entidadeDicionario)

    #     return entidade

    def Alterar(self,nomeTabela, entidade, api) :

        table = self.DynamoTabela(nomeTabela)

        if (api == 1) :
            entidadeDicionario = entidade.dict()
        else :
            entidadeDicionario = entidade

        #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

        table.put_item(Item=entidadeDicionario)
        
    def Consultar(self,nomeTabela, ID, api) :

        table = self.DynamoTabela(nomeTabela)

        entidade = {'id': ID}

        if (api == 1) :
            entidadeDicionario = entidade.dict()
        else :
            entidadeDicionario = entidade

        #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

        retorno = table.get_item(Key=entidadeDicionario)    

        return retorno['Item']


    def Consultar(self,nomeTabela, ID) :

        table = self.DynamoTabela(nomeTabela)

        entidade = {'id': ID}

        # if (api == 1) :
        #     entidadeDicionario = entidade.dict()
        # else :
        entidadeDicionario = entidade

        #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

        retorno = table.get_item(Key=entidadeDicionario)    

        return retorno['Item']
    
    def Pesquisar(self,nomeTabela, condicao) :     

        table = self.DynamoTabela(nomeTabela)

        retorno = self.PesquisarScan(
             tabela      =  table
            ,condicao   = condicao  
            
        )

        return retorno    

    def PesquisarScan(self,tabela,condicao) :   

        if condicao['startTime'] != None :
            filterExpression_ =  Attr(condicao['chave']).eq(condicao['valor']) & Attr('time').between(condicao['startTime'],condicao['endTime'])
        else:
            filterExpression_ =  Attr(condicao['chave']).eq(condicao['valor']) 

        retorno = tabela.scan(
            FilterExpression= filterExpression_
        )

        return retorno

    def PesquisarQuery(self,tabela,condicao) :

        chave_ = condicao['chave']
        valor_ =  condicao['valor']
        retorno = tabela.query(
            KeyConditionExpression = Key(chave_).eq(valor_) 
        )

        return retorno

    def ConsultarNOME(self,nomeTabela, nome, api) :

        table = self.DynamoTabela(nomeTabela)

        entidadeFilter = {'nome': nome}
        entidadeFilter = {'FilterExpression': Attr('nome').eq(nome)
                        , 'ProjectionExpression' : "id, nome, temperatura, pressao, umidade, situacao, IP"
                        }

        
        # aws dynamodb scan ^
        # --table-name Produto ^
        # --filter-expression 'contains(nome,:nome)' ^
        # --expression-attribute-values '{":nome":{"S":"chocolate"}}'
        #

        if (api == 1) :
            entidadeDicionario = entidadeFilter.dict()
        else :
            entidadeDicionario = entidadeFilter

        #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

        retorno = table.scan(**entidadeFilter)    

        return retorno['Items']


