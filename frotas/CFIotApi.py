from typing import Union
from fastapi import FastAPI
import uvicorn


import boto3
import boto3.dynamodb.types
from boto3.dynamodb.conditions import Key, Attr

import CFVeiculos

# from pydantic import BaseModel
from typing import Union

#import json
from  decimal import Decimal

app = FastAPI()
app.openapi_version = "3.0.2"

@app.get("/api")
def read_root():
    return {"mensagem": "to aqui, pronto e saudável"}

# localhost:8000/api/pesquisar?placa=48_55_19_C1_A7_A4&startTime=2025-11-03T21:32:46.000Z&endTime=2025-11-04T21:32:46.000Z
# https://169egekr7b.execute-api.sa-east-1.amazonaws.com/dev/api/pesquisar?placa=48_55_19_C1_A7_A4&startTime=2025-11-03T21:32:46.000Z&endTime=2025-11-04T21:32:46.000Z

@app.get("/api/pesquisar/{placa}/{startTime}/{endTime}")
def pesquisar(placa:str, startTime:str, endTime:str):

    cVeiculos = CFVeiculos.CVeiculos()
    retorno  = cVeiculos.PesquisarPorPlacaDynamo(placa, startTime, endTime)  

    return retorno
    # return {"mensagem": "to aqui, pronto e saudável"}

def parse_float(value) :
    return Decimal(str(value))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


