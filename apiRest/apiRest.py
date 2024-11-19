from typing import Union

from fastapi import FastAPI

#import compara_hash

import uvicorn


import boto3
import boto3.dynamodb.types

from pydantic import BaseModel
from typing import Union

import json
from  decimal import Decimal

from boto3.dynamodb.conditions import Key, Attr



class Clima1(BaseModel) :
    id: int
    nome: Union[str, None] = None
    temperatura: Union[Decimal, None] = None
    pressao: Union[float, None] = None
    umidade: Union[float, None] = None

class Clima(BaseModel) :
    id: int
    nome: Union[str, None] = None
    temperatura: Union[Decimal, None] = None
    pressao: Union[Decimal, None] = None
    umidade: Union[Decimal, None] = None    



app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ergon2eso/{emp_codigo}/{mes}/{ano}")
def read_item(emp_codigo: int, mes: int, ano:int):
    #return {"emp_codigo": emp_codigo, "mes": mes, "ano": ano}
    #compara_hash.Iniciar(1)
    #compara_hash.ESocialComparar(emp_codigo, mes, ano)
    return {"situacao": "GERADO"}

@app.post("/api/clima")
async def create_item(entidade: Clima) :
    Incluir(entidade)
    return entidade

@app.post("/api/clima1")
async def create_item(entidade) :
    Incluir(entidade.model_dump())
    return entidade

def parse_float(value) :

    return Decimal(str(value))
    
def IncluirID(tabelaNome) :

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('TabelasIndices')

    documento = {"tabelaNome" : tabelaNome, "ultimoIndice" : 1}

    table.put_item(Item=documento)

    return  1


def ConsultarID(tabelaNome) :

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('TabelasIndices')

    scan = table.scan(FilterExpression=Attr('tabelaNome').eq(tabelaNome))

    retorno = 0

    if len(scan['Items']) == 0 : # adicionar
        retorno = IncluirID(tabelaNome)
    else :
        retorno = scan['Items'][0]['ultimoIndice']

    return retorno

def Incluir(entidade) :

    entidade.id = ConsultarID('Clima')

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Clima')

    entidadeDicionario = entidade.dict()

    #entidadeDicionario : dict = json.loads(json.dumps(entidade), parse_float=parse_float)

    table.put_item(Item=entidadeDicionario)


    # documento = {
    # }

    # # inclui 1

    # documento['id'] = 12345
    # documento['nome'] = "nome " +  documento['id']
    # table.put_item(Item=documento)
    # print('-------------------inclui 1 =', documento)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


