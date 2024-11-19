from typing import Union
from fastapi import FastAPI
import uvicorn


import boto3
import boto3.dynamodb.types
from boto3.dynamodb.conditions import Key, Attr

from pydantic import BaseModel
from typing import Union

import json
from  decimal import Decimal

class Clima(BaseModel) :
    id: int
    nome: Union[str, None] = None
    temperatura: Union[Decimal, None] = None
    pressao: Union[Decimal, None] = None
    umidade: Union[Decimal, None] = None    

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "to aqui, pronto e saudável"}

@app.post("/api/clima")
async def incluir_item(entidade: Clima) :
    Incluir('Clima',entidade, 1)
    return entidade

@app.put("/api/clima")
async def alterar_item(entidade: Clima) :
    Alterar('Clima',entidade, 1)
    return entidade

@app.get("/api/clima/{id}")
async def consultar_item(id: int) :
    entidade = Consultar('Clima',id, 0)
    return entidade




def parse_float(value) :
    return Decimal(str(value))

def DynamoTabela(nomeTabela) :

    dynamodb = boto3.resource('dynamodb')

    return dynamodb.Table(nomeTabela)    

def DynamoBuscaS(nomeTabela, filtro) :
    
    tabela = DynamoTabela(nomeTabela)   

    return tabela.scan(FilterExpression=filtro)
 
    
def IncluirID(tabelaNome) :

    table = DynamoTabela('TabelasIndices')

    documento = {"tabelaNome" : tabelaNome, "ultimoIndice" : 1}

    table.put_item(Item=documento)

    return  1

def ConsultarID(tabelaNome) :

    scan = DynamoBuscaS('TabelasIndices', Attr('tabelaNome').eq(tabelaNome) ) #table.scan(FilterExpression=Attr('tabelaNome').eq(tabelaNome))

    retorno = 0

    if len(scan['Items']) == 0 : # adicionar
        retorno = IncluirID(tabelaNome)
    else : # alterar
        documento = scan['Items'][0]
        documento['ultimoIndice'] = documento['ultimoIndice'] + 1
        Alterar('TabelasIndices', documento,0)
        retorno = documento['ultimoIndice']

    return retorno

def Incluir(nomeTabela, entidade, api) :

    entidade.id = ConsultarID(nomeTabela)

    table = DynamoTabela(nomeTabela)

    if (api == 1) :
        entidadeDicionario = entidade.dict()
    else :
        entidadeDicionario = entidade

    #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

    table.put_item(Item=entidadeDicionario)

    return entidade

def Alterar(nomeTabela, entidade, api) :

    table = DynamoTabela(nomeTabela)

    if (api == 1) :
        entidadeDicionario = entidade.dict()
    else :
        entidadeDicionario = entidade

    #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

    table.put_item(Item=entidadeDicionario)
    
def Consultar(nomeTabela, ID, api) :

    table = DynamoTabela(nomeTabela)

    entidade = {'id': ID}

    if (api == 1) :
        entidadeDicionario = entidade.dict()
    else :
        entidadeDicionario = entidade

    #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

    retorno = table.get_item(Key=entidadeDicionario)    

    return retorno['Item']

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


